#coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from Xiami import XiamiUser as XU , XiamiSong as XS
from Netease import NeteaseUser as NU , NeteaseSong as NS
from models import User
import json

@csrf_exempt
def login(request):
	message = {'status':True,'titleMsg':'发生错误'}
	if request.method=="POST":
		username = request.POST.get('id')
		passwd = request.POST.get('passwd')
		remember_me = request.POST.get('remember_me')
		
		if username.replace(' ','') == '':
			return render(request,'register.html',{'message':message,})
		if passwd.replace(' ','') == '':
			return render(request,'register.html',{'message':message,})

		try :
			user = User.objects.get(username=username)
			if user.password == passwd:
				request.session['is_login'] = True
				request.session['username'] = username
				return HttpResponseRedirect('/home/')
			else:
				message = {'status':False,'titleMsg':'密码错误'}
				return render(request,'login.html',{'message':message,})
		except User.DoesNotExist:
			message = {'status':False,'titleMsg':'用户不存在'}
			return render(request,'login.html',{'message':message,})

	elif request.method == "GET":
		if request.session.get('is_login',False):
			return HttpResponseRedirect('/home/')

	return render(request,'login.html',{'message':message,})

def logout(request):
	if request.method=="GET":
		request.session['is_login'] = False
		request.session['username'] = ''
		return HttpResponseRedirect('/login/')

	return HttpResponseRedirect('/login/')

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
		if passwd_again!=passwd:
			message = {'status':False,'titleMsg':'两次密码不一致'}
			return render(request,'register.html',{'message':message,})
		if invitation!='abcd':
			message = {'status':False,'titleMsg':'邀请码无效'}
			return render(request,'register.html',{'message':message,})

		try :
			user = User.objects.get(username=username)
			message = {'status':False,'titleMsg':'用户已存在'}
			return render(request,'register.html',{'message':message,})
		except User.DoesNotExist:
			user = User(username=username,password=passwd)
			user.save()
			return HttpResponseRedirect('/home/setting/')
		
	return render(request,'register.html',{'message':message,})

def user_setting(request):
	'''用户设置，主要用来设置个性化选项'''
	message = {'status':True,'titleMsg':'发生错误'}
	if request.method=="GET":
		profile = {}
		if request.session.get('is_login',False):
			username = request.session.get('username')
			profile['username'] = username
			user = User.objects.get(username=username)
			
			bound_xiami = user.bound_xiami
			xiami_type = user.xiami_type
			xiami_username = user.xiami_username
			
			bound_netease = user.bound_netease
			
			if bound_netease:
				profile['netease_username'] = user.netease_username

			return render(request,'setting.html',{'profile':profile,})
		else:
			return HttpResponseRedirect('/login/')
	return HttpResponseRedirect('/login/')

def user_home(request):
	'''用户主页，展示用户收藏'''
	profile = {'status':True,'titleMsg':'发生错误'}
	if request.method=="GET":
		if request.session.get('is_login',False):
			username = request.session.get('username')
			profile['username'] = username
			user = User.objects.get(username=username)
			bound_xiami = user.bound_xiami
			xiami_type = user.xiami_type
			xiami_username = user.xiami_type
			bound_netease = user.bound_netease
			netease_username = user.netease_username
			netease_uid = user.netease_uid
			netease_cookies = user.netease_cookies

			#if bound_xiami : 
			#	xu = XU(xiami_username,"***")
			#	if user.xiami_type == 1:     #xiami
			#		message = xu.login_with_xiami()
			#		if message['status']:
			#			favor_song = xu.get_favor_song()
			#			profile['favor_song_xiami'] = favor_song
			#		else:
			#			profile['message'] = '虾米登录错误'
			#	else:
			#		message = xu.login_with_xiami()
			#		if message['status']:
			#			favor_song = xu.get_favor_song()
			#			profile['favor_song_xiami'] = favor_song
			#		else:
			#			profile['message'] = '虾米(淘宝)登录错误'

			if bound_netease : 
				#收藏的歌单
				nu = NU(netease_username)
				ret = nu.get_favor_song(netease_uid)
				if ret[0]:
					profile['favor_song_netease'] = ret[1]
				netease_cookies  = netease_cookies.replace('\'','\"')
				cookies = json.loads(netease_cookies)
				#个性化推荐 歌单 做不了 是post请求，需要密码。
				#ret = nu.get_personal_customized(cookies)
				#if ret[0]:
				#	profile['customized_netease'] = ret[1]
				#个性化 歌曲（taste）
				ret = nu.get_personal_taste(cookies)
				if ret[0]:
					profile['taste_netease'] = ret[1]
			
			return render(request,'home.html',{'profile':profile,})
			
		else:
			return HttpResponseRedirect('/login/')
		
	return HttpResponseRedirect('/login/')

def main(request):
	return render(request,'main.html')