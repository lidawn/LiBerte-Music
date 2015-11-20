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

#这个类定义貌似没有必要
class NeteaseUser:
	'''网易用户'''
	
	hot_recommend = []		#热门推荐    #后面个性定制五个标签
	new_cd = []				#新碟上架

	def __init__(self,username):
		self._username = username
		self._uid = 0
		self._nickname = ''
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

	def login(self,password):
		URL = 'http://music.163.com/weapi/login/'
		text = {
			'username':self._username,
			'password':hashlib.md5(password).hexdigest(),
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

		resp = self._session.post(URL,data=post_data,headers=headers,cookies=cookies)
		netease_cookie = {}
		
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
		else:
			message = {
				'status':False,
				'titleMsg' :'发生错误'
			}
		return message

	def get_personal_customized(self,cookies):
		URL = 'http://music.163.com/discover'
		#需要实时登录 POST请求
		URL_recommmed = 'http://music.163.com/weapi/discovery/recommend/resource'
		#cookie 传进来是个字典
		cookies['appver'] = '2.0.2'
		resp = requests.get(URL,headers=headers,cookies=cookies)
		content = BS(resp.content)
		#f = open("text.txt","a")
		#f.write(resp.content)
		#f.close()
		customized_list = content.find('ul',class_='m-cvrlst m-cvrlst-idv f-cb').find_all('li',{"data-res-action":"log"})
		##print customized_list
		personal_customized = []
		
		for customized in customized_list:
			#print customized.string,
			if customized.get('data-res-action',None) is None:
				continue 
			image = customized.find('div',class_='u-cover u-cover-1').find('img').get('src')
			a = customized.find('p',class_='dec f-brk').find('a')
			title = a.string
			id_ = a.get('href')[a.get('href').find('=')+1:]
			description = customized.find('p',class_='idv f-brk s-fc4').get('title')
			result = {
				'image' : image,
				'title' : title,
				'id' : id_,
				'description' : description
			}
			personal_customized.append(result)
		return True,personal_customized

	def get_personal_taste(self,cookies):
		#cookie 传进来是个字典
		cookies['appver'] = '2.0.2'
		resp = requests.get('http://music.163.com/discover/recommend/taste',cookies=cookies,headers=headers)
		content = BS(resp.content)
		#f = open("text.txt","a")
		#f.write(resp.content)
		#f.close()
		taste_list = content.find('div',class_='n-songtb n-songtb-1 j-flag').find('tbody').find_all('tr')
		#print 'taste_list',taste_list
		personal_taste = []
		for taste in taste_list:
			id_ = taste.get('data-id')
			#print id_,
			infos  = taste.find_all('td')
			#print infos
			name = infos[1].find('a').string.replace('\'','\\\'')
			duration = infos[2].string
			artist_name = infos[3].find('a').string.replace('\'',' ')
			get_id = lambda x : x[x.find('=')+1:]
			artist_id = get_id(infos[3].find('a').get('href'))
			album_name = infos[4].find('a').string.replace('\'',' ')
			album_id = get_id(infos[4].find('a').get('href'))

			result = {
				'id' : id_,
				'name' : name,
				'duration' : duration,
				'artist_name' : artist_name,
				'artist_id' : artist_id,
				'album_name' : album_name,
				'album_id' : album_id
			}
			personal_taste.append(result)
		return True,personal_taste

	@staticmethod
	def add_to_playlist(track_id,playlist_id,cookies):
		#cookie 传进来是个字典
		cookies['appver'] = '2.0.2'
		data = {
			'trackIds':'["'+track_id+'"]',
			'pid':playlist_id,
			'op':'add',
			'imme':'true'
		}
		resp = requests.post('http://music.163.com/api/v1/playlist/manipulate/tracks',data=data,cookies=cookies,headers=headers)
		if resp.status_code ==200:
			return True
		return False
		
		#return True,personal_taste

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
		#print results
		#print 'ke',keywords
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
		song_list = []
		status = True
		try:
			playlists = resp.json().get('playlist')
			#print playlists
			
			for playlist in playlists:
				song = {}
				song['name'] = playlist.get('name')
				song['id'] = playlist.get('id')
				song['coverImgUrl'] = playlist.get('coverImgUrl')
				song['trackCount'] = playlist.get('trackCount')
				song_list.append(song)
		except:
			#出错，重新登录授权
			status = False

		return status,song_list

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
		if name.find("-") !=-1:
			name = name[0:name.find("-")]
		if name.find("(") !=-1:
			name = name[0:name.find("(")]
		#print 'name',name 
		keywords = name+' '+ artist+' '+album
		song_list = NeteaseUser.get_search_result('1',keywords,'1')
		if song_list is None:
			return None
		ids = {
			'id' : song_list[0].get('song_id'),
			'album_id' : song_list[0].get('song_album_id')
		}
		#print ids
		return ids

	@classmethod
	def get_link(cls,id_,album_id):
		'''通过专辑id和歌曲id得到播放地址'''
		URL = 'http://music.163.com/api/album/%s/' % album_id
		resp = requests.get(URL,cookies=cookies,headers=headers)
		songs = resp.json().get('album').get('songs')
		cover = resp.json().get('album').get('blurPicUrl')
		for song in songs:
			if str(song.get('id')) == id_:
				return song.get('mp3Url')+";"+cover
