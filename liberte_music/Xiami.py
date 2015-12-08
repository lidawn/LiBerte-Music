#coding:utf-8
import requests
from bs4 import BeautifulSoup as BS
import re,rsa
import platform
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

if platform.system() == 'Darwin':
	import requests.packages.urllib3.util.ssl_
	requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL'

user_agent = '''Mozilla/5.0 (Windows NT 10.0; WOW64) 
						AppleWebKit/537.36 (KHTML, like Gecko) 
						Chrome/46.0.2490.80 
						Safari/537.36
			'''
headers = {'user-Agent':user_agent,'connection':'keep-alive'}

url = 'https://passport.alipay.com/mini_login.htm?lang=&appName=xiami&appEntrance=taobao&cssLink=&styleType=vertical&bizParams=&notLoadSsoView=&notKeepLogin=&rnd=0.6477347570091512?lang=zh_cn&appName=xiami&appEntrance=taobao&cssLink=https%3A%2F%2Fh.alipayobjects.com%2Fstatic%2Fapplogin%2Fassets%2Flogin%2Fmini-login-form-min.css%3Fv%3D20140402&styleType=vertical&bizParams=&notLoadSsoView=true&notKeepLogin=true&rnd=0.9090916193090379'
bs = BS(requests.get(url).content)

class XiamiUser:
	'''虾米用户'''	
	bs = bs
	#http://www.xiami.com/index/recommend  猜你喜欢
	def __init__(self,username):
		self._username = username

	def login_with_xiami(self,password):
		'''用虾米账号登录'''
		URL = 'https://login.xiami.com/member/login'
		post_data = {'_xiamitoken':'20f0e5a22def96dbe410f339a65e6600',
					'done':'http://www.xiami.com',
					'from':'web',
					'email':self._username,
					'password':password,
					'submit':'登 录'}
		self._session.post(URL,headers=headers,data=post_data)
		resp = self._session.get('http://www.xiami.com/account',headers=headers)
		content = BS(resp.content)

		#虾米返回的是header
		xiami_header = {}
		if content.find('div',class_='account'):
			nickname = content.find('div',class_='account').find('a',class_='avatar').get('title')
			#是herf
			uid = content.find('div',class_='account').find('a',class_='avatar').get('herf')[3:]
			xiami_header = resp.request.headers
			for key in resp.cookies.keys():
				xiami_header[key] = resp.cookies[key]
			#for key in resp.cookies.keys():
			#	xiami_cookie[key] = resp.cookies[key]
			message = {
				'status':True,
				'titleMsg' :'',
				'nickname' : nickname,
				'uid' : uid,
				'xiami_header':str(xiami_header)
			}
		else:
			message = {
				'status':False,
				'titleMsg' :'发生错误'
			}

		return message

	#用headers可以取到
	def get_favor_song(self,xiami_headers,page):
		'''获取收藏歌曲'''
		song_list = []
		URL = 'http://www.xiami.com/space/lib-song/page/'+page
		resp = requests.get(URL,headers=xiami_headers)
		content = BS(resp.content)
		#加一个是否抓取成功的判断
		#获取总歌曲数
		song_total = content.find('div',class_='all_page').find('span').string
		song_total = song_total[song_total.find(u'共')+1 : -2]
		#总页数
		page_total = (lambda x : (x/25 + 1) if x % 25 else (x/25))(int(song_total))
		if int(page)>int(page_total):
			return page_total,[]
		song_name_list = content.find_all('td',class_='song_name')
		song_act_list = content.find_all('div',class_='song_do')
		length = len(song_name_list)
		for i in range(length):
			song_name = song_name_list[i].find('a').string.encode('utf-8')
			#print song_name
			artist_name = song_name_list[i].find('a',class_='artist_name').string.encode('utf-8')
			song_id = song_name_list[i].find('a').get('href')
			song_id = song_id[song_id.rfind('/')+1:]
			artist_id = song_name_list[i].find('a',class_='artist_name').get('href')
			artist_id = artist_id[artist_id.rfind('/')+1:]
			#print song_act_list[i].find('a').get('onclick').find('play')
			if song_act_list[i].find('a').get('onclick').find('play') == 0:
				song_is_playable = True
			else:
				song_is_playable = False
			#print song_id,song_name,song_is_favored,song_is_playable
			song = {
				'song_id':song_id,
				'song_name':song_name,
				'artist_name':artist_name,
				'artist_id':artist_id,
				'song_is_playable':song_is_playable
			}
			song_list.append(song)
			
		return page_total,song_list
	
	def get_favor_album(self):
		'''获取收藏专辑;TODO'''
		pass

	def get_favor_artist(self):
		pass

	@staticmethod
	def set_favor_song(id_,token,xiami_cookie):
		'''收藏一首歌'''
		URL = 'http://www.xiami.com/ajax/addtag'
		data = {
			'tags':'like',
			'type':3,
			'id':id_,
			'desc':'like',
			'grade':5,
			'share':0,
			'shareTo':'all',
			'_xiamitoken':token
		}
		headers = {'user-Agent':user_agent,'connection':'keep-alive','Referer':'http://www.xiami.com/song/'+id_}
		#xiami_headers['Referer'] =  'http://www.xiami.com/song/'+id_

		resp = requests.post(URL,data=data,headers=headers,cookies=xiami_cookie)
		if resp.json().get('status') =='ok':
			return True
		return False

	@classmethod
	def search(cls,keywords):
		return cls.get_search_result('song',keywords,40)			#单曲
		#self.get_search_result('album',keywords)			#专辑
		#self.get_search_result('artist',keywords)		#歌手
		#self.get_search_result('collect',keywords)		#歌单/精选集

	@classmethod
	def get_search_result(cls,type_,keywords,limit):
		#两个平台 用歌曲名，歌手，(专辑名)标识同一首歌
		#返回一个字典列表，不创建对象
		#要改成抓取所有歌曲，分页返回
		search_results = []

		URL = 'http://www.xiami.com/search/%s/page/%d?key=%s' 
		#print keywords
		resp = requests.get(URL % (type_,1,keywords),headers=headers)
		content = BS(resp.content)
		results = content.find('div',class_='search_result_box')
		#print results
		#搜索结果多少条,最多显示limit条
		count = results.find('b').string
		count = (lambda x : x if x<limit else limit)(int(count))
		page_total = (lambda x : (x/20 + 1) if x % 20 else (x/20))(count)
		#print page_total
		for p in range(page_total):
			#print results
			#print "aaaa"
			result  = results.find('tbody')
			#print result
			for tr in result.find_all('tr'):
				#每一个tr代表一首歌
				song = {}
				song_is_playable = (lambda x : True if x is not None else False)(tr.find('td',class_='chkbox').find('input').get('checked'))
				song_name = tr.find('td',class_='song_name').find('a',target='_blank').find('b')
				if song_name:
					song_name = song_name.string
				else:
					song_name = tr.find('td',class_='song_name').find('a',target='_blank').string
				song_album = tr.find('td',class_='song_album').find('a',target='_blank').find('b')
				if song_album:
					song_album = song_album.string
				else:
					song_album = tr.find('td',class_='song_album').find('a',target='_blank').string
				song_artist = tr.find('td',class_='song_artist').find('a',target='_blank').string
				if song_artist:
					song_artist = song_artist.string
				else:
					song_artist = tr.find('td',class_='song_artist').find('a',target='_blank').string
				
				song_id = tr.find('td',class_='song_name').find('a',target='_blank').get('href')
				song_id = song_id[song_id.rfind('/')+1:]
				
				song = {
				'song_id':song_id,
				'song_is_playable':song_is_playable,
				'song_name' : song_name,
				'song_album' : song_album,
				'song_artist' : song_artist
				}
				search_results.append(song)
			if p == page_total:
				break
			resp = requests.get(URL%(type_,p+2,keywords),headers=headers)
			content = BS(resp.content)
			results = content.find('div',class_='search_result_box')

		return search_results

class XiamiSong:
	def __init__(self,id_,name,is_favored,is_playable):
		self._id = id_
		self._name = name
		self._is_favored = is_favored #是否已收藏
		self._is_playable = is_playable #是否可播放

	@classmethod
	def parse_id(cls,name,artist,album):
		keywords = name+' '+ artist+' '+album
		song_list = XiamiUser.get_search_result('song',keywords,1)
		if song_list is None:
			return None
		id_ = song_list[0]['song_id']
		return id_

	@classmethod
	def get_link(cls,id_,is_cover):
	 	url = 'http://www.xiami.com/song/playlist/id/'+id_
		xml = requests.get(url,headers=headers)
		#print xml.content
		pattern = re.compile(r'<location>(.*)</location>',re.S)
		result = pattern.findall(xml.content)
		link_encode =  result[0]
		real_url = cls.decode_link(link_encode)
		if not is_cover:
			pattern = re.compile(r'<album_pic>(.*)</album_pic>',re.S)
			result = pattern.findall(xml.content)
			cover =  result[0]
			pattern = re.compile(r'<album_name>(.*)</album_name>',re.S)
			result = pattern.findall(xml.content)
			album =  result[0]
			album = album[9:-2].replace(']','')
			#print album
			return real_url+';'+cover+';'+album
		return real_url

	@classmethod
	def decode_link(cls,link_encode):
		#print link_encode
		#第一个数代表行数
		line = int(link_encode[0])
		link_encode =  link_encode[1:]
		length_total = len(link_encode)
		juzhen = []
		
		#短行长度
		length_1 = length_total/line
		length_2 = length_1+1
		for i in range(0,line+1):
			if length_1*i + length_2*(line-i) == length_total:
				break
		line_2 = i
		line_1 = line - line_2
		i = line_1
		start = 0
		end = length_2
		while i>0: 
			juzhen.append(link_encode[start:end])
			start = end
			end += length_2
			i -= 1
		end -=1
		i = line_2
		while i>0 :
			juzhen.append(link_encode[start:end])
			start = end
			end += length_1
			i -= 1

		real_url = ''
		i = 0
		#拼接为正确的url
		while i<length_2:
			j = 0
			while j<line:
				try:
					#print juzhen[j][i]
					real_url += juzhen[j][i]
				except IndexError:
					i = length_1
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