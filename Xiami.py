#coding:utf-8
import requests
from bs4 import BeautifulSoup as BS

user_agent = '''Mozilla/5.0 (Windows NT 10.0; WOW64) 
						AppleWebKit/537.36 (KHTML, like Gecko) 
						Chrome/46.0.2490.80 
						Safari/537.36
			'''
headers = {'user-Agent':user_agent,'connection':'keep-alive'}

class XiamiUser:
	'''虾米用户'''
	
	def __init__(self,username,password,accountType):
		self._username = username
		self._password = password
		self._accountType = accountType

	def login(self):
		'''用虾米账号登录'''
		URL = 'https://login.xiami.com/member/login'
		user_agent = '''Mozilla/5.0 (Windows NT 10.0; WOW64) 
						AppleWebKit/537.36 (KHTML, like Gecko) 
						Chrome/46.0.2490.80 
						Safari/537.36
					'''
		post_data = {'_xiamitoken':'20f0e5a22def96dbe410f339a65e6600',
					'done':'http%3A%2F%2Fwww.xiami.com',
					'from':'web',
					'email':self._username,
					'password':self._password,
					'submit':'登 录'}

		session = requests.Session()
		resp = session.post(URL,headers=headers,data=post_data)
		return session

	def login_with_taobao(self):
		'''用淘宝账号登录
			TODO
		'''
		URL_taobao = 'https://login.xiami.com/accounts/taobao-login-iframe'
		URL = 'https://login.xiami.com/member/login'
		
		post_data = {'_xiamitoken':'20f0e5a22def96dbe410f339a65e6600',
					'done':'http%3A%2F%2Fwww.xiami.com',
					'from':'web',
					'email':self._username,
					'password':self._password,
					'submit':'登 录'}

		session = requests.Session()
		resp = session.post(URL,headers=headers,data=post_data)

		print '###content###'
		print resp.content.decode('utf-8')
		print '###cookie###'
		print resp.cookies
		headers = {'user-Agent':self.user_agent,'connection':'keep-alive'}
		resp = session.get('http://www.xiami.com/space/lib-song',headers=headers)
		print '###session###'
		#f = open('test.txt','a')
		#f.writelines(resp.content)
		#f.close()
		#print resp.content.decode('utf-8')
		print resp.content
		print '###session###'
		print session.headers

	def get_favor_song(self):
		song_list = []
		session = self.login()
		resp = session.get('http://www.xiami.com/space/lib-song',headers=headers)
		content = BS(resp.content)
		song_name_list = content.find_all('td',class_='song_name')
		song_act_list = content.find_all('div',class_='song_do')
		length = len(song_name_list)
		for i in range(length):
			song_name = song_name_list[i].find('a').string.encode('utf-8')
			song_id = song_name_list[i].find('a').get('href')
			song_id = song_id[song_id.rfind('/')+1:]
			song_is_favored = True
			if song_act_list[i].find('a').get('onclick').find('play'):
				song_is_playable = True
			else:
				song_is_playable = False
			print song_id,song_name,song_is_favored,song_is_playable
			song = Song(song_id,song_name,song_is_favored,song_is_playable)
			song_list.append(song)
		return song_list
		
		#print song_name

class Song:
	def __init__(self,id_,name,is_favored,is_playable):
		self._id = id_
		self._name = name
		self._is_favored = is_favored #是否已收藏
		self._is_playable = is_playable #是否可播放

	def get_link(self):
	 	url = 'http://www.xiami.com/song/playlist/id/'+self._id
		xml = requests.get(url,headers=headers)
		print xml.content
		#pattern = re.compile(r'<location>(.*)</location>',re.S)
		#result = pattern.findall(xml_result)
		#luanma =  result[0]
		#luanma =  luanma[1:]
		#real_url = get_real_url(luanma)
		#song['real_url'] = real_url
			#print luanma
			#print '\n'
		#return list

c = XiamiUser('lidawn1991@163.com','294833369','c')
c.get_favor_song()
		