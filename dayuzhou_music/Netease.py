#coding:utf-8
import requests
from bs4 import BeautifulSoup as BS
import json,os,base64
from Crypto.Cipher import AES
import hashlib

user_agent = '''Mozilla/5.0 (Windows NT 10.0; WOW64) 
						AppleWebKit/537.36 (KHTML, like Gecko) 
						Chrome/46.0.2490.80 
						Safari/537.36
			'''
headers = {
	'user-Agent':user_agent,
	'connection':'keep-alive',
	'Referer':'http://music.163.com/',
	'Accept': '*/*',
	'Accept-Encoding': 'gzip,deflate,sdch',
	'Accept-Language': 'zh-CN,zh;q=0.8,gl;q=0.6,zh-TW;q=0.4',
	'Content-Type': 'application/x-www-form-urlencoded',
	'Host': 'music.163.com'
	}

cookies = {'appver':'2.0.2'}

class NeteaseUser:
	'''网易用户'''
	
	hot_recommend = []		#热门推荐    #后面个性定制五个标签
	new_cd = []				#新碟上架

	#resp = self._session.get('http://music.163.com/api/user/playlist/?uid=14946761&offset=0&limit=100',headers=headers)

	def __init__(self,username,password):
		self._username = username
		self._password = password
		self._uid = 0
		self._nickname = ''
		self._personal_customized = []	#个性化推荐
		self._session =  requests.Session()

	@staticmethod
	def aesEncrypt(text, secKey):
		pad = 16 - len(text) % 16
		text = text + pad * chr(pad)
		encryptor = AES.new(secKey, 2, '0102030405060708')
		ciphertext = encryptor.encrypt(text)
		ciphertext = base64.b64encode(ciphertext)
		return ciphertext

	@staticmethod
	def rsaEncrypt(text, pubKey, modulus):
		text = text[::-1]
		rs = int(text.encode('hex'), 16)**int(pubKey, 16)%int(modulus, 16)
		return format(rs, 'x').zfill(256)
	
	@staticmethod
	def createSecretKey(size):
		return (''.join(map(lambda xx: (hex(ord(xx))[2:]), os.urandom(size))))[0:16]

	def login(self):
		URL = 'http://music.163.com/weapi/login/'
		#user = User.objects.get(netease_username=self._username)
		text = {
			'username':self._username,
			'password':hashlib.md5(self._password).hexdigest(),
			'rememberLogin':'true'
		}
		modulus = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
		nonce = '0CoJUm6Qyw8W8jud'
		pubKey = '010001'

		text = json.dumps(text)
		secKey = self.createSecretKey(16)
		encText = self.aesEncrypt(self.aesEncrypt(text,nonce),secKey)
		encSecKey = self.rsaEncrypt(secKey,pubKey,modulus)

		post_data = {
			'params':encText,
			'encSecKey':encSecKey
		}

		#cookies = {
		#	'MUSIC_U' : '934e6d4051f9b826b02c927d28df2394192dba7eb4fe2cae679ba046251a51acb3dda51c0e04c53b56bae0635616e4d0bb6cc9ca2a38915441049cea1c6bb9b6',
		#	'NETEASE_WDA_UID' : '14946761#|#1417935701145',
		#	'__csrf' : 'b3729dc17e11cd606c766206cf9d4303',
		#	'__remember_me' : 'true',
		#	'appver':'2.0.2'
		#}
		#resp = requests.get('http://music.163.com/discover/recommend/taste',cookies=cookies,headers=headers)
		#f = open('txt.txt','a')
		#f.write(resp.content)
		#f.close()

		resp = self._session.post(URL,data=post_data,headers=headers,cookies=cookies)
		netease_cookie = {}
		#保存cookie
		#for key in resp.cookies.keys():
		#	print key,resp.cookies[key]
		
		#resp = self._session.get('http://music.163.com/api/user/playlist/?uid=14946761&offset=0&limit=100',headers=headers,cookies=cookies)
		#print resp.content.decode('utf-8')
		
		if resp.content.find('account') !=-1:
			self._uid = resp.json().get('account').get('id')
			self._nickname = resp.json().get('profile').get('nickname')
			for key in resp.cookies.keys():
				netease_cookie[key] = resp.cookies[key]
			message = {
				'status':True,
				'titleMsg' :'',
				'uid' : self._uid,
				'nickname' : self._nickname,
				'netease_cookie':netease_cookie
			}
			return message
		else:
			message = {
				'status':False,
				'titleMsg' :'发生错误'
			}
			return message

	def get_personal_customized(self):
		return self._personal_customized

	@classmethod
	def search(cls,keywords):
		return cls.get_search_result('1',keywords,'100')			#单曲
		#self.get_search_result(10,keywords)			#专辑
		#self.get_search_result(100,keywords)		#歌手
		#self.get_search_result(1000,keywords)		#歌单

	@classmethod
	def get_search_result(cls,type,keywords,limit):
		song_list = []
		URL = 'http://music.163.com/api/search/get/'
		post_data = {
						's':keywords,
						'limit': limit,
						'sub': 'False',
						'type': type,
						'offset': '0'
		}

		resp = requests.post(URL,data=post_data,cookies=cookies,headers=headers)
		#print '###song###'
		results =  resp.json().get('result')
		songs = results.get('songs')
		count =  (lambda x,y: x if x<y else y)(results.get('songCount'),len(songs))

		for song in songs:
			song_result = {}
			song_id = song.get('id')
			song_is_favored = False
			song_is_playable = (lambda x:True if x==1 else False)(song.get('status'))
			song_name = song.get('name').encode('utf-8')
			album_id = song.get('album').get('id')
			song_result = {
					'song_id':song_id,
					'song_is_playable':song_is_playable,
					'song_name' : song_name,
					'song_is_favored' : song_is_favored,
					'song_album_id' : album_id
					}
			#print song ,'\n'
			#print song_id,album_id,song_name,song_is_favored,song_is_playable
			song_list.append(song_result)
		return song_list

	@classmethod
	def get_discover(cls):
		cls.hot_recommend = []
		cls.new_cd = []

		URL = 'http://music.163.com/discover'
		resp = requests.get(URL,headers=headers)
		content = BS(resp.content)
		hot_list = content.find('ul',class_='m-cvrlst f-cb').find_all('li')
		for hot in hot_list:
			image = hot.find('div',class_='u-cover u-cover-1').find('img').get('src')
			a = hot.find('p',class_='dec').find('a')
			title = a.get('title')
			id_ = a.get('href')[a.get('href').find('=')+1:]
			result = {
				'image' : image,
				'title' : title,
				'id' : id_
			}
			cls.hot_recommend.append(result)

		#customized_list = content.find('ul',class_='m-cvrlst m-cvrlst-idv f-cb').find_all('li')
		##print customized_list
		#for customized in customized_list:
		#	if customized.get('data-res-action',None) is None:
		#		continue 
		#	image = customized.find('div',class_='u-cover u-cover-1').find('img').get('src')
		#	a = customized.find('p',class_='dec f-brk').find('a')
		#	title = a.string
		#	id_ = a.get('href')[a.get('href').find('=')+1:]
		#	description = customized.find('p',class_='idv f-brk s-fc4').get('title')
		#	result = {
		#		'image' : image,
		#		'title' : title,
		#		'id' : id_,
		#		'description' : description
		#	}
		#	self._personal_customized.append(result)

		cd_list = content.find('div',class_='n-disk').find_all('ul',class_='f-cb roller-flag')
		for cds in cd_list:
			for cd in cds.find_all('li'):
				a = cd.find_all('p',class_='f-thide')
				image = cd.find('img').get('data-src')
				title = a[0].find('a').string
				id_ = a[0].find('a').get('href')[a[0].find('a').get('href').find('=')+1:]
				artist = a[1].find('a').string
				artist_id = a[1].find('a').get('href')[a[1].find('a').get('href').find('=')+1:]
				result = {
					'title' : title,
					'image' : image,
					'id' : id_,
					'artist' : artist,
					'artist_id' : artist_id
				}
				cls.new_cd.append(result)

		#print resp.content

	@staticmethod
	def get_favor_song(uid):
		resp = requests.get('http://music.163.com/api/user/playlist/?uid=%s&offset=0&limit=100'%str(uid),headers=headers,cookies=cookies)
		try:
			playlists = resp.json().get('playlist')
			song_list = []
			for playlist in playlists:
				song = {}
				song['name'] = playlist.get('name')
				song['name'] = playlist.get('id')
				song['name'] = playlist.get('coverImgUrl')
				song['name'] = playlist.get('trackCount')
				song_list.append(song)
		except:
			#出错，重新登录授权
			pass


		return song_list


class NeteaseSong:
	
	def __init__(self,id_,album_id,name,is_favored,is_playable):
		self._id = id_
		self._album_id = album_id
		self._name = name
		self._is_favored = is_favored #是否已收藏
		self._is_playable = is_playable #是否可播放

	@classmethod
	def parse_id(cls,name,artist,album):
		ids = {}
		keywords = name+' '+ artist+' '+album
		song_list = NeteaseUser.get_search_result('1',keywords,'1')
		if song_list is None:
			return None
		ids = {
			'id' : song_list[0].get('song_id'),
			'album_id' : song_list[0].get('song_album_id')
		}
		return ids

	@classmethod
	def get_link(cls,id_,album_id):
		'''通过专辑id和歌曲id得到播放地址'''
		URL = 'http://music.163.com/api/album/%d/' % album_id
		resp = requests.get(URL,cookies=cookies,headers=headers)
		songs = resp.json().get('album').get('songs')
		for song in songs:
			if song.get('id') == id_:
				return song.get('mp3Url')


#n = NeteaseUser('lidawn1991@163.com','***')
#n.login()
#s =  Song(287063,28520,'BE FREE (Voice Filter Mix) - remix',False,True)
#s.get_link()