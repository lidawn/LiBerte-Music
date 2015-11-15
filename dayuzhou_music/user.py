#coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from Xiami import XiamiUser as XU , XiamiSong as XS
from Netease import NeteaseUser as NU , NeteaseSong as NS
from django.db import models

class User(models.Model):
	username = models.CharField(max_length=100)
	password = models.CharField(max_length=40)
	bound_xiami = models.BooleanField(default=False)
	xiami_type = models.IntegerField()
	xiami_username =  models.CharField(max_length=100)    #是否有必要
	xiami_password =  models.CharField(max_length=40)
	bound_netease = models.BooleanField(default=False)
	netease_username =  models.CharField(max_length=100)
	netease_uid = models.CharField(max_length=40)
	netease_cookies = models.CharField(max_length=1000)

@csrf_exempt
def login(request):
	message = {'status':True,'titleMsg':'发生错误'}
	if request.method=="POST":
		username = request.POST.get('id')
		passwd = request.POST.get('passwd')
		remember_me = request.POST.get('remember_me','off')
		
		if username.replace(' ','') == '':
			return render(request,'login.html',{'message':message,})
		if passwd.replace(' ','') == '':
			return render(request,'login.html',{'message':message,})
		
		#try:
		#	user = User.objects.get(username=username)
		#	if user.password == passwd:
		#		request.session['is_login'] = True
		#		request.session['username'] = username
		#		return HttpResponseRedirect('/home/')
		#	else:
		#		message['titleMsg'] = '密码错误'
		#except User.DoesNotExist:
		#	message['titleMsg'] = '无此用户名'
#
		#message['status'] = False

		#比数据库
		if username == 'lidawn' and passwd =='1234':
			request.session['is_login'] = True
			request.session['username'] = username
			return HttpResponseRedirect('/home/')
		else:
			message['status'] = False
		
	return render(request,'login.html',{'message':message,})

@csrf_exempt
def register(request):
	message = {'status':True,'titleMsg':'发生错误'}
	if request.method=="POST":
		username = request.POST.get('id')
		passwd = request.POST.get('passwd')
		passwd_again = request.POST.get('passwd_again')
		invitation = request.POST.get('invitation')
		
		if username.replace(' ','') == '':
			return render(request,'register.html',{'message':message,})
		if passwd.replace(' ','') == '':
			return render(request,'register.html',{'message':message,})
		if passwd_again.replace(' ','') == '':
			return render(request,'register.html',{'message':message,})
		if invitation.replace(' ','') == '':
			return render(request,'register.html',{'message':message,})
		if invitation!='abcd':
			message['titleMsg'] = '邀请码无效'
			return render(request,'register.html',{'message':message,})
		if passwd_again!=passwd:
			message['titleMsg'] = '两次密码不一致'
			return render(request,'register.html',{'message':message,})

		user = User(username=username,passwd=passwd)


		#比数据库

		#print message
		if message['status']:
			return HttpResponseRedirect('/home/setting/')
		
	return render(request,'register.html',{'message':message,})


def user_setting(request):
	'''用户设置，主要用来设置个性化选项'''

	message = {'status':True,'titleMsg':'发生错误'}
	if request.method=="GET":
		if request.session.get('is_login',False):
			return HttpResponseRedirect('/login/')
		else:
			return render(request,'setting.html')
	return HttpResponseRedirect('/login/')

def user_home(request):
	'''用户主页，展示用户收藏'''
	if request.method=="GET":
		profile = {}
		if request.session.get('is_login',False):
			username = request.session.get('username')
			profile['username'] = username

			user = User.objects.get(username=username)
			if user.bound_xiami : 
				xu = XU(user.xiami_username,user.xiami_password)
				if user.xiami_type == 1:     #xiami
					message = xu.login_with_xiami()
					if message['status']:
						favor_song = xu.get_favor_song()
						profile['favor_song_xiami'] = favor_song
					else:
						profile['message'] = '虾米登录错误'
				else:
					message = xu.login_with_xiami()
					if message['status']:
						favor_song = xu.get_favor_song()
						profile['favor_song_xiami'] = favor_song
					else:
						profile['message'] = '虾米(淘宝)登录错误'

			if user.bound_netease : 
				uid = user.netease_uid
				#不需要登录，这里只要用uid获取歌单就可以
				favor_song = NU.get_favor_song(uid)
				profile['favor_song_netease'] = favor_song
				
				if message['status']:
					#favor_song = nu.get_favor_song()
					
				else:
					profile['message'] = '网易登录错误'
			
			return render(request,'home.html',{'profile':profile,})
			
		else:
			return HttpResponseRedirect('/login/')
		
	return HttpResponseRedirect('/login/')