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

	@staticmethod
	def add_to_playlist(track_id,playlist_id,cookies):
		'''收藏至默认列表'''
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
		'''搜索'''
		return cls.get_search_result('1',keywords,'100')			#单曲
		#self.get_search_result(10,keywords)			#专辑
		#self.get_search_result(100,keywords)		#歌手
		#self.get_search_result(1000,keywords)		#歌单

	@classmethod
	def get_search_result(cls,type_,keywords,limit):
		song_list = []
		URL = 'http://music.163.com/api/search/get/'
		post_data = {
						's':keywords,
						'limit': limit,
						'sub': 'False',
						'type': type_,
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

	@staticmethod
	def get_favor_song(uid):
		'''个人收藏'''
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
				#song['trackCount'] = playlist.get('trackCount')
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

		return ids

	@classmethod
	def get_link(cls,id_,album_id,is_album_name):
		'''通过专辑id和歌曲id得到播放地址'''
		URL = 'http://music.163.com/api/album/%s/' % album_id
		resp = requests.get(URL,cookies=cookies,headers=headers)
		#print resp.content
		songs = resp.json().get('album').get('songs')
		cover = resp.json().get('album').get('blurPicUrl')
		album = resp.json().get('album').get('name')
		#print songs,cover,album
		for song in songs:
			if str(song.get('id')) == id_:
				#print song
				if is_album_name:
					return song.get('mp3Url')+";"+cover
				else:
					return song.get('mp3Url')+";"+cover+";"+album
