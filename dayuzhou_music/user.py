#coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from Xiami import XiamiUser as XU , XiamiSong as XS
from Netease import NeteaseUser as NU , NeteaseSong as NS

class User:
	'''本站用户'''
	
	hot_recommend = []		#热门推荐    #后面个性定制五个标签
	new_cd = []				#新碟上架

	def __init__(self,username,password):
		self._username = username
		self._password = password
		self._bound_xiami = _bound_xiami			#是否绑定虾米账户
		self._bound_netease = bound_netease 		#是否绑定网易账户
		self._personal_customized = []	#个性化推荐（包括每日歌单，每日精选集）
		self._setting = {} 				#一些个性化设置

def login(requests):
	message = {'status':True,'titleMsg':'发生错误'}
	if request.method=="POST":
		username = request.POST.get('id')
		passwd = request.POST.get('passwd')
		
		if username.replace(' ','') == '':
			return render(request,'login.html',{'message':message,})
		if passwd.replace(' ','') == '':
			return render(request,'login.html',{'message':message,})

		user = User(username,passwd)

		#比数据库

		#print message
		if message['status']:
			return HttpResponseRedirect('/')
		
	return render(request,'login.html',{'message':message,})

def register(requests):
	message = {'status':True,'titleMsg':'发生错误'}
	if request.method=="POST":
		username = request.POST.get('id')
		passwd = request.POST.get('passwd')
		
		if username.replace(' ','') == '':
			return render(request,'register.html',{'message':message,})
		if passwd.replace(' ','') == '':
			return render(request,'register.html',{'message':message,})

		user = User(username,passwd)

		#比数据库

		#print message
		if message['status']:
			return HttpResponseRedirect('/')
		
	return render(request,'register.html',{'message':message,})

def user_home(request):
	'''用户主页，主要用来设置个性化选项'''
	message = {'status':True,'titleMsg':'发生错误'}
	if request.method=="POST":
		username = request.POST.get('id')
		passwd = request.POST.get('passwd')
		
		if username.replace(' ','') == '':
			return render(request,'register.html',{'message':message,})
		if passwd.replace(' ','') == '':
			return render(request,'register.html',{'message':message,})

		user = User(username,passwd)

		#比数据库

		#print message
		if message['status']:
			return HttpResponseRedirect('/')
		
	return render(request,'register.html',{'message':message,})

