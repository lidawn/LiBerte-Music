#coding:utf-8
import requests
from bs4 import BeautifulSoup as BS

user_agent = '''Mozilla/5.0 (Windows NT 10.0; WOW64) 
						AppleWebKit/537.36 (KHTML, like Gecko) 
						Chrome/46.0.2490.80 
						Safari/537.36
			'''
headers = {'user-Agent':user_agent,'connection':'keep-alive','referer':'http://music.163.com'}

cookies = {'appver':'1.5.2'}

class NeteaseUser:
	'''网易用户'''
	session = requests.Session()
	hot_recommend = []		#热门推荐    #后面个性定制五个标签
	new_cd = []				#新碟上架
	def __init__(self,username,password,accountType):
		self._username = username
		self._password = password
		self._accountType = accountType
		self._personal_customized = []	#个性化推荐

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


n = NeteaseUser('a','b','c')
NeteaseUser.get_discover()
#s =  Song(287063,28520,'BE FREE (Voice Filter Mix) - remix',False,True)
#s.get_link()