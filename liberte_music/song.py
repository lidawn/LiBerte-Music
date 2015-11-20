#coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from Xiami import XiamiUser as XU , XiamiSong as XS
from Netease import NeteaseUser as NU , NeteaseSong as NS
from models import User
import json

@csrf_exempt
def get_link(request):
	if request.method=="POST":
		is_playable = request.POST.get('is_playable')
		type = request.POST.get('type')
		id_ = request.POST.get('id')
		name = request.POST.get('name')
		artist = request.POST.get('artist')
		artist_id = request.POST.get('artist_id')
		album = request.POST.get('album')
		album_id = request.POST.get('album_id')
		cover = request.POST.get('cover')
		if type=='n' and is_playable=='True':
			link = NS.get_link(id_,album_id)
		elif type=='x' and is_playable=='True':
			link = XS.get_link(id_)+';'+cover
		elif type=='n' and is_playable=='False':
			pass
		elif type=='x' and is_playable=='False':
			pass
		else:
			link = '404;404'
	return HttpResponse(link)

@csrf_exempt
def add_to_playlist(request):
	if request.method=="POST":
		username = request.session.get('username')
		user = User.objects.get(username=username)
		
		ret = 'False'

		name = request.POST.get('name')
		artist = request.POST.get('artist')
		artist_id = request.POST.get('artist_id')
		album = request.POST.get('album')
		album_id = request.POST.get('album_id')
		type = request.POST.get('type')
		id_ = request.POST.get('id')

		if type=='n':
			playlist_id = user.netease_playlist
			netease_cookies = user.netease_cookies
			netease_cookies  = netease_cookies.replace('\'','\"')
			cookies = json.loads(netease_cookies)
			
			if NU.add_to_playlist(id_,playlist_id,cookies):
				ret = 'True'
		elif type=='x':
			xiami_headers = user.xiami_headers
			xiami_headers = xiami_headers.replace('\'','\"')
			dict = json.loads(xiami_headers)
			index_s = dict.get('Cookie').find('_xiamitoken')
			index_s = dict.get('Cookie').find('=',index_s)
			index_e = dict.get('Cookie').find(';',index_s)
			if index_e!=-1:
				token = dict.get('Cookie')[index_s+1:index_e]
			else:
				token = dict.get('Cookie')[index_s+1:]
			sessid = dict.get('__XIAMI_SESSID')
			cookie = dict.get('Cookie')
			cookie += ('; __XIAMI_SESSID='+sessid)
			li = cookie.split(';')
			xiami_cookie = {}
			for i in li:
				i_li = i.split('=')
				xiami_cookie[i_li[0]] = i_li[1]
			XU.set_favor_song(id_,token,xiami_cookie)
			#link = XU.get_link(id_)+';'+cover
		else:
			ret = 'False'
	return HttpResponse(ret)