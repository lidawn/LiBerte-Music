#coding:utf-8
import requests
from bs4 import BeautifulSoup as BS
import re

user_agent = '''Mozilla/5.0 (Windows NT 10.0; WOW64) 
						AppleWebKit/537.36 (KHTML, like Gecko) 
						Chrome/46.0.2490.80 
						Safari/537.36
			'''
headers = {'user-Agent':user_agent,'connection':'keep-alive'}

class XiamiUser:
	'''虾米用户'''
	session = requests.Session()
	def __init__(self,username,password,accountType):
		self._username = username
		self._password = password
		self._accountType = accountType

	def login(self):
		'''用虾米账号登录'''
		URL = 'https://login.xiami.com/member/login'
		post_data = {'_xiamitoken':'20f0e5a22def96dbe410f339a65e6600',
					'done':'http%3A%2F%2Fwww.xiami.com',
					'from':'web',
					'email':self._username,
					'password':self._password,
					'submit':'登 录'}
		resp = self.session.post(URL,headers=headers,data=post_data)
		#return session

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

		#session = requests.Session()
		resp = self.session.post(URL,headers=headers,data=post_data)

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
		'''获取收藏歌曲'''
		song_list = []
		URL = 'http://www.xiami.com/space/lib-song/page/%d'
		#session = self.login()
		resp = self.session.get(URL%1,headers=headers)
		if 'login' in resp.url:
			print 'not login'
			self.login()
			resp = self.session.get(URL%1,headers=headers)

		content = BS(resp.content)
		#获取总歌曲数
		song_total = content.find('div',class_='all_page').find('span').string
		song_total = song_total[song_total.find(u'共')+1 : -2]
		#总页数
		page_total = (lambda x : (x/25 + 1) if x % 25 else (x/25))(int(song_total))
		for p in range(page_total):
			song_name_list = content.find_all('td',class_='song_name')
			song_act_list = content.find_all('div',class_='song_do')
			length = len(song_name_list)
			for i in range(length):
				song_name = song_name_list[i].find('a').string.encode('utf-8')
				song_id = song_name_list[i].find('a').get('href')
				song_id = song_id[song_id.rfind('/')+1:]
				song_is_favored = True
				#print song_act_list[i].find('a').get('onclick').find('play')
				if song_act_list[i].find('a').get('onclick').find('play') == 0:
					song_is_playable = True
				else:
					song_is_playable = False
				print song_id,song_name,song_is_favored,song_is_playable
				song = Song(song_id,song_name,song_is_favored,song_is_playable)
				song_list.append(song)
			if p == page_total:
				break
			resp = self.session.get(URL%(p+2),headers=headers)
			content = BS(resp.content)
		return song_list
	
	def get_favor_album(self):
		'''获取收藏专辑;TODO'''
		pass

	def get_favor_artist(self):
		pass

	def set_favor_song(self):
		'''收藏一首歌'''
		pass

	def set_favor_album(self):
		pass

	def set_favor_artist(self):
		pass

	def search(self):
		URL = 'http://www.xiami.com/search?key='

class Song:
	def __init__(self,id_,name,is_favored,is_playable):
		self._id = id_
		self._name = name
		self._is_favored = is_favored #是否已收藏
		self._is_playable = is_playable #是否可播放

	def get_link(self):
	 	url = 'http://www.xiami.com/song/playlist/id/'+self._id
		xml = requests.get(url,headers=headers)
		#print xml.content
		pattern = re.compile(r'<location>(.*)</location>',re.S)
		result = pattern.findall(xml.content)
		link_encode =  result[0]
		link_encode =  link_encode[1:]
		#解密乱码得到真实url
		length_1 = link_encode.find('t',0)
		length_2 = link_encode.find('t',length_1+1)
		length_3 = link_encode.find('t',length_2+1)
		if (length_2 - length_1) == length_1 or (length_2 - length_1) == (length_1 - 1):
			length = length_1
		else:
			length = length_2 
		juzhen = []
		a = len(link_encode)
		#矩阵总行数
		if a%length :
			line = a/length +1
			yushu = length - a%length
		else :
			line = a/length
			yushu = 0
		start = 0
		end = length
		#余数
		if yushu :
			#行的长度不一致
			#较长的行数
			line_1 = line - yushu
			i = line_1
			#处理较长的行数
			while i>0: 
				juzhen.append(link_encode[start:end])
				#a = a-length
				start = end
				end += length
				i -= 1
			#处理剩余行数
			line_2 = line - line_1
			end -=1
			length -=1
			i = line_2
			while i>0 :
				juzhen.append(link_encode[start:end])
				start = end
				end += length
				i -= 1
		else:
			#行的长度一致
			i = line
			while i>0: 
				juzhen.append(link_encode[start:end])
				#a = a-length
				start = end
				end += length
				i -= 1

		real_url = ''
		length = len(juzhen[0])
		i = 0
		#拼接为正确的url
		while i<length:
			j = 0
			while j<line:
				try:
					#print juzhen[j][i]
					real_url += juzhen[j][i]
				except IndexError:
					i = length
					j = line
					break
				j += 1
			i += 1

		while 1 :
			index = real_url.find('%')
			if index == -1:
				break
			if real_url[index:index+3] == '%3A' :
				real_url = real_url[0:index] + ':' + real_url[index+3:]
			elif real_url[index:index+3] == '%2F' :
				real_url = real_url[0:index] + '/' + real_url[index+3:]
			elif real_url[index:index+3] == '%5E' :
				real_url = real_url[0:index] + '0' + real_url[index+3:]
			elif real_url[index:index+3] == '%3F' :
				real_url = real_url[0:index] + '?' + real_url[index+3:]
			elif real_url[index:index+3] == '%3D' :
				real_url = real_url[0:index] + '=' + real_url[index+3:]

		return real_url


c = XiamiUser('lidawn1991@163.com','294833369','c')
s = Song('1239160','Smells Like Teen Spirit' ,True ,True)
print s.get_link()
#c.get_favor_song()
		