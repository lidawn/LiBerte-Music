#coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from Xiami import XiamiUser as XU , XiamiSong as XS
from Netease import NeteaseUser as NU , NeteaseSong as NS

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
		xiami_id = request.POST.get('xiami_id')
		passwd = request.POST.get('passwd')
		
		if xiami_id.replace(' ','') == '':
			return render(request,'bound_xiami.html',{'message':message,})
		if passwd.replace(' ','') == '':
			return render(request,'bound_xiami.html',{'message':message,})

		xu = XU(xiami_id,passwd)

		message = xu.login_with_xiami()
		#print message
		if message['status']:
			return HttpResponseRedirect('/')
		
	return render(request,'bound_xiami.html',{'message':message,})

@csrf_exempt
def bound_netease(request):
	message = {'status':True,'titleMsg':'发生错误'}
	if request.method=="POST":
		netease_id = request.POST.get('netease_id')
		passwd = request.POST.get('passwd')
		
		if netease_id.replace(' ','') == '':
			return render(request,'bound_netease.html',{'message':message,})
		if passwd.replace(' ','') == '':
			return render(request,'bound_netease.html',{'message':message,})

		nu = NU(netease_id,passwd)

		message = nu.login()
		#print message
		if message['status']:
			return HttpResponseRedirect('/')
		
	return render(request,'bound_netease.html',{'message':message,})