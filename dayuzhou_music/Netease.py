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
	def __init__(self,username,password,accountType):
		self._username = username
		self._password = password
		self._accountType = accountType

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
n.search('我怀念的 孙燕姿 逆光')
#s =  Song(287063,28520,'BE FREE (Voice Filter Mix) - remix',False,True)
#s.get_link()