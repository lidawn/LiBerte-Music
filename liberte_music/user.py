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
				if user.bound_netease == False and user.bound_xiami == False:
					return HttpResponseRedirect('/setting/')
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
			return HttpResponseRedirect('/setting/')
		
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
			if bound_xiami:
				profile['xiami_username'] = user.xiami_username

			return render(request,'setting.html',{'profile':profile,})
		else:
			return HttpResponseRedirect('/login/')
	return HttpResponseRedirect('/login/')

def user_home(request):
	'''展示每日推荐'''
	profile = {'status':True,'titleMsg':'发生错误'}
	if request.method=="GET":
		if request.session.get('is_login',False):
			username = request.session.get('username')
			profile['username'] = username
			user = User.objects.get(username=username)
			bound_xiami = user.bound_xiami
			xiami_type = user.xiami_type
			xiami_username = user.xiami_username
			xiami_headers = user.xiami_headers
			bound_netease = user.bound_netease
			netease_username = user.netease_username
			netease_uid = user.netease_uid
			netease_cookies = user.netease_cookies

			if bound_xiami == False and bound_netease == False:
				profile['bound_xiami'] = False
				profile['bound_netease'] = False

			if bound_xiami : 
				profile['bound_xiami'] = True
				#处理一下xiami cookie 不要加session id
				xiami_headers = xiami_headers.replace('\'','\"')
				dic = json.loads(xiami_headers)
				del dic['__XIAMI_SESSID']
				xu = XU(xiami_username)
				ret = xu.get_personal_taste(dic)
				if ret[0]:
					profile['taste_xiami'] = ret[1]

			if bound_netease : 
				profile['bound_netease'] = True
				netease_cookies  = netease_cookies.replace('\'','\"')
				cookies = json.loads(netease_cookies)
				#个性化推荐 歌单 做不了 是post请求，需要密码。
				#ret = nu.get_personal_customized(cookies)
				#if ret[0]:
				#	profile['customized_netease'] = ret[1]
				#个性化 歌曲（taste）
				nu = NU(netease_username)
				ret = nu.get_personal_taste(cookies)
				if ret[0]:
					profile['taste_netease'] = ret[1]
			
			return render(request,'home.html',{'profile':profile,})
			
		else:
			return HttpResponseRedirect('/login/')
		
	return HttpResponseRedirect('/login/')

def user_home_netease(request):
	'''展示网易收藏'''
	profile = {'status':True,'titleMsg':'发生错误'}
	if request.method=="GET":
		if request.session.get('is_login',False):
			username = request.session.get('username')
			profile['username'] = username
			user = User.objects.get(username=username)
			bound_netease = user.bound_netease
			netease_username = user.netease_username
			netease_uid = user.netease_uid

			if bound_netease : 
				#收藏的歌单
				profile['bound_netease'] = True
				profile['bound_xiami'] = user.bound_xiami
				nu = NU(netease_username)
				ret = nu.get_favor_song(netease_uid)
				if ret[0]:
					profile['favor_song_netease'] = ret[1]
				#个性化推荐 歌单 做不了 是post请求，需要密码。
				#ret = nu.get_personal_customized(cookies)
				#if ret[0]:
				#	profile['customized_netease'] = ret[1]
			
				return render(request,'home_netease.html',{'profile':profile,})

			else:
				return HttpResponseRedirect('/home/')

		else:
			return HttpResponseRedirect('/login/')
		
	return HttpResponseRedirect('/login/')

def user_home_xiami(request,page='1'):
	'''展示虾米收藏'''
	profile = {'status':True,'titleMsg':'发生错误'}
	if request.method=="GET":
		if request.session.get('is_login',False):
			username = request.session.get('username')
			profile['username'] = username
			user = User.objects.get(username=username)
			bound_xiami = user.bound_xiami
			xiami_type = user.xiami_type
			xiami_username = user.xiami_username
			xiami_headers = user.xiami_headers

			if bound_xiami : 
				profile['bound_xiami'] = True
				profile['bound_netease'] = user.bound_netease
				#get 用headers
				xiami_headers = xiami_headers.replace('\'','\"')
				dic = json.loads(xiami_headers)
				del dic['__XIAMI_SESSID']
				xu = XU(xiami_username)
				ret = xu.get_favor_song(dic,page)
				
				profile['favor_song_xiami'] = ret[1]
				profile['page_total_list'] = range(1,int(ret[0])+1)
				profile['page_total'] = int(ret[0])
				if int(ret[0]) < int(page):
					profile['current_page'] = int(ret[0])
				else:
					profile['current_page'] = int(page)
					profile['current_page_pre'] = int(page)-1
					profile['current_page_next'] = int(page)+1

				return render(request,'home_xiami.html',{'profile':profile,})
			else:
				return HttpResponseRedirect('/home/')
			
		else:
			return HttpResponseRedirect('/login/')
		
	return HttpResponseRedirect('/login/')

def main(request):
	return render(request,'main.html')