#coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from Xiami import XiamiUser as XU , XiamiSong as XS
from Netease import NeteaseUser as NU , NeteaseSong as NS
import requests
from bs4 import BeautifulSoup as BS

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
		#id_ = request.POST.get('id')
		#if is_playable == 'True' :
		#	link =  XS.get_link(id_)
		#else:
		#	name = request.POST.get('name')
		#	artist = request.POST.get('artist')
		#	album = request.POST.get('album')
		#	ids = NS.parse_id(name,artist,album)
		#	if ids :
		#		link =  NS.get_link(ids.get('id'),ids.get('album_id'))
		#	else:
		#		link = '404'
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

		xu.login_with_xiami()
		#print message
		if message['status']:
			return HttpResponseRedirect('/')
		#print 'message',message
		#id_ = request.POST.get('id')
		#if is_playable == 'True' :
		#	link =  XS.get_link(id_)
		#else:
		#	name = request.POST.get('name')
		#	artist = request.POST.get('artist')
		#	album = request.POST.get('album')
		#	ids = NS.parse_id(name,artist,album)
		#	if ids :
		#		link =  NS.get_link(ids.get('id'),ids.get('album_id'))
		#	else:
		#		link = '404'
	return render(request,'bound_xiami.html',{'message':message,})