#coding:utf-8
from django.shortcuts import render
from django.http import HttpResponseRedirect
from Xiami import XiamiUser as XU , XiamiSong as XS
import detail

def parse(request):
	'''
	接受链接类型
	0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26  27 28 29               
	h t t p : / / m u s i  c  .  1  6   3  .  c  o  m  /  s  o  n  g  ?  i  d  = 189545
	http://music.163.com/#/                               a  l  b  u  m?id=19164
	http://music.163.com/#/                               p  l  a  y  l  i  s   t  ?id=134011933
	0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26  27 28 29    
	h t t p : / / w w w  . x  i  a   m i  .  c  o  m  /  a  l  b  u  m  /   1 6 9 0 7 1 ? spm=....
	http://www.xiami.com/                                s  o  n  g  /  1773867171?spm=a1z1s
	http://www.xiami.com/                                c  o  l  l  e  c   t  /  9 043318

	返回值：
	response = {
		status:		#输入合法
		type:		#歌曲s、专辑a、歌单l

		title:		#标题
		results:{}	#依据type返回的字典
	}
	'''

	if request.method=="GET":
		if 'keywords' in request.GET :
			keywords = request.GET.get('keywords',None)
			
			response = {
				'status' : True
			}

			if keywords.replace(' ','') :
				if keywords[0:7] == "http://":
					pass
				else:
					keywords = "http://"+keywords
				#如果是网易链接
				if keywords[7:21] == "music.163.com/":
					#判断类型
					keywords = keywords.replace('/#','')
					keywords = keywords.replace('/my/m/music','')
					keywords = keywords.replace('discover/toplist','playlist')

					if keywords[21:25] == "song":
						if keywords[25:29] == "?id=":
							id_ = keywords[29:]
							results = detail.netease_song(id_)
							if results is None:
								response['status'] = False
							else:
								response['results'] = results
								return render(request,'netease_detail.html',{'response':response,})
						else:
							response['status'] = False
					elif keywords[21:26] == "album":
						if keywords[26:30] == "?id=":
							id_ = keywords[30:]
							results = detail.netease_album(id_)
							if results is None:
								response['status'] = False
							else:
								response['results'] = results
								return render(request,'netease_detail.html',{'response':response,})
						else:
							response['status'] = False
					elif keywords[21:29] == "playlist":
						if keywords[29:33] == "?id=":
							id_ = keywords[33:]
							print id_
							results = detail.netease_playlist(id_)
							if results is None:
								response['status'] = False
							else:
								response['results'] = results
								return render(request,'netease_detail.html',{'response':response,})
						else:
							response['status'] = False
					else:
						response['status'] = False
				
				#虾米链接
				elif keywords[7:21] == "www.xiami.com/":
					index = keywords.find('?spm=')
					if index != -1:
						keywords = keywords[0:index]
					if keywords[21:25] == "song":
						if keywords[25:26] == "/":
							id_ = keywords[26:]
							return render(request,'netease_detail.html',{'profile':profile,})
						else:
							response['status'] = False
					elif keywords[21:26] == "album":
						if keywords[26:27] == "/":
							id_ = keywords[27:]
							return render(request,'netease_detail.html',{'profile':profile,})
						else:
							response['status'] = False
					elif keywords[21:28] == "collect":
						if keywords[28:29] == "/":
							id_ = keywords[29:]
							return render(request,'netease_detail.html',{'profile':profile,})
						else:
							response['status'] = False
					else:
						response['status'] = False
				#非法输入 
				else:
					response['status'] = False
				print response
				return render(request,'parse.html',{'response':response,})
		
	return render(request,'parse.html')
