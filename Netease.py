#coding:utf-8
import requests
from bs4 import BeautifulSoup as BS
import md5

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

	def search(self,keywords):
		return self.get_search_result('1',keywords)			#单曲
		#self.get_search_result(10,keywords)			#专辑
		#self.get_search_result(100,keywords)		#歌手
		#self.get_search_result(1000,keywords)		#歌单

	def get_search_result(self,type,keywords):
		song_list = []
		URL = 'http://music.163.com/api/search/get/'
		post_data = {
						's':keywords,
						'limit': '5',
						'sub': 'False',
						'type': type,
						'offset': '0'
		}

		resp = self.session.post(URL,data=post_data,cookies=cookies,headers=headers)
		print '###song###'
		results =  resp.json().get('result')
		songs = results.get('songs')
		count =  (lambda x,y: x if x<y else y)(results.get('songCount'),len(songs))

		for song in songs:
			song_id = song.get('id')
			song_is_favored = False
			song_is_playable = (lambda x:True if x==1 else False)(song.get('status'))
			song_name = song.get('name').encode('utf-8')
			album_id = song.get('album').get('id')
			#print song ,'\n'
			song_list.append(Song(song_id,album_id,song_name,song_is_favored,song_is_playable))
		return song_list


class Song:
	session = requests.Session()
	def __init__(self,id_,album_id,name,is_favored,is_playable):
		self._id = id_
		self._album_id = album_id
		self._name = name
		self._is_favored = is_favored #是否已收藏
		self._is_playable = is_playable #是否可播放

	def get_link(self):
		'''通过专辑id和歌曲id得到播放地址'''
		URL = 'http://music.163.com/api/album/%d/' % self._album_id
		resp = self.session.get(URL,cookies=cookies,headers=headers)
		songs = resp.json().get('album').get('songs')
		for song in songs:
			if song.get('id') == self._id:
				print song.get('mp3Url')


n = NeteaseUser('a','b','c')
#n.search('我怀念的')
s =  Song(287063,28520,'BE FREE (Voice Filter Mix) - remix',False,True)
s.get_link()