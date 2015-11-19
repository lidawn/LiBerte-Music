#coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from Xiami import XiamiUser as XU , XiamiSong as XS
from Netease import NeteaseUser as NU , NeteaseSong as NS
from models import User

@csrf_exempt
def bound_xiami_taobao(request):
	message = {'status':True,'data':{}}
	if request.method=="POST":
		taobao_id = request.POST.get('taobao_id')
		passwd = request.POST.get('passwd')
		captcha = request.POST.get('captcha',None)
		if taobao_id.replace(' ','') == '':
			return render(request,'bound_xiami_taobao.html',{'message':message,})
		if passwd.replace(' ','') == '':
			return render(request,'bound_xiami_taobao.html',{'message':message,})
		if captcha is None :
			captcha = ''
		elif captcha.replace(' ','') == '':
			captcha = ''

		xu = XU(taobao_id,passwd)

		message = xu.login_with_taobao(captcha)
		print message
		if message['status']:
			return HttpResponseRedirect('/')
		print 'message',message
		
	return render(request,'bound_xiami_taobao.html',{'message':message,})

@csrf_exempt
def bound_xiami(request):
	message = {'status':True,'titleMsg':'发生错误'}
	if request.method=="POST":
		#如果已绑定，跳走（还要解绑，检查cookie有效期）
		xiami_id = request.POST.get('xiami_id')
		passwd = request.POST.get('passwd')
		
		if xiami_id.replace(' ','') == '':
			return render(request,'bound_xiami.html',{'message':message,})
		if passwd.replace(' ','') == '':
			return render(request,'bound_xiami.html',{'message':message,})

		xu = XU(xiami_id)
		message = xu.login_with_xiami(passwd)
		#print message
		if message['status']:
			username = request.session.get('username')
			user = User.objects.get(username=username)
			user.bound_xiami = True
			user.xiami_username = message['nickname']
			user.xiami_uid = message['uid']
			user.xiami_headers = message['xiami_header']
			user.save()
			profile = {
				'username' : username,
				'xiami_username' : message['nickname']
			}
			return HttpResponseRedirect('/setting/')
		
	return render(request,'bound_xiami.html',{'message':message,})

@csrf_exempt
def bound_netease(request):
	message = {'status':True,'titleMsg':'发生错误'}
	#如果已绑定，跳走（还要解绑，检查cookie有效期）
	if request.method=="POST":
		netease_id = request.POST.get('netease_id')
		passwd = request.POST.get('passwd')
		
		if netease_id.replace(' ','') == '':
			return render(request,'bound_netease.html',{'message':message,})
		if passwd.replace(' ','') == '':
			return render(request,'bound_netease.html',{'message':message,})

		nu = NU(netease_id)
		message = nu.login(passwd)
		#print message
		if message['status']:
			username = request.session.get('username')
			user = User.objects.get(username=username)
			user.bound_netease = True
			user.netease_uid = message['uid']
			user.netease_username = message['nickname']
			user.netease_cookies = str(message['netease_cookie'])
			user.save()
			profile = {
				'username' : username,
				'netease_username' : message['nickname']
			}
			return HttpResponseRedirect('/setting/')
		
	return render(request,'bound_netease.html',{'message':message,})

