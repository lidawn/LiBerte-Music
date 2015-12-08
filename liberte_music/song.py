#coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from Xiami import XiamiUser as XU , XiamiSong as XS
from Netease import NeteaseUser as NU , NeteaseSong as NS
from models import User
import json
#输出爆炸了！！！！！

@csrf_exempt
def get_link(request):
	if request.method=="POST":
		link = '404;404;404'
		is_playable = request.POST.get('is_playable')
		type_ = request.POST.get('type')
		id_ = request.POST.get('id')
		name = request.POST.get('name')
		artist = request.POST.get('artist')
		artist_id = request.POST.get('artist_id')
		album = request.POST.get('album')
		album_id = request.POST.get('album_id')
		cover = request.POST.get('cover')
		if type_=='n' and is_playable=='True':
			link = NS.get_link(id_,album_id,True)
		elif type_=='x' and is_playable=='True':
			#不一定有封面的
			if cover!='cover':
				#有封面
				link = XS.get_link(id_,True)+';'+cover
			else:
				#无封面,无专辑
				link = XS.get_link(id_,False)

		elif type_=='n' and is_playable=='False':
			#解决网易不能播放的问题
			id_ = XS.parse_id(name,artist,' ')
			#print ids
			if id_:
				#虾米有源
				link = XS.get_link(id_,False)

		elif type_=='x' and is_playable=='False':
			#解决虾米不能播放的问题
			ids = NS.parse_id(name,artist,' ')
			#print ids
			if ids:
				#网易有源
				link = NS.get_link(str(ids['id']),str(ids['album_id']),False)

	#print link
	return HttpResponse(link)

@csrf_exempt
def add_to_playlist(request):
	#收藏歌曲
	if request.method=="POST":
		username = request.session.get('username')
		if not username:
			return HttpResponse('False')

		user = User.objects.get(username=username)

		ret = 'False'

		name = request.POST.get('name')
		artist = request.POST.get('artist')
		artist_id = request.POST.get('artist_id')
		album = request.POST.get('album')
		album_id = request.POST.get('album_id')
		type = request.POST.get('type')
		id_ = request.POST.get('id')

		#print name , artist , artist_id , album,album_id,type,id_

		if type=='n':
			if not user.bound_netease:
				return HttpResponse('False')
			playlist_id = user.netease_playlist
			netease_cookies = user.netease_cookies
			netease_cookies  = netease_cookies.replace('\'','\"')
			cookies = json.loads(netease_cookies)

			if NU.add_to_playlist(id_,playlist_id,cookies):
				ret = 'True'
		elif type=='x':
			if not user.bound_xiami:
				return HttpResponse('False')
			xiami_headers = user.xiami_headers
			xiami_headers = xiami_headers.replace('\'','\"')
			dic = json.loads(xiami_headers)
			index_s = dic.get('Cookie').find('_xiamitoken')
			index_s = dic.get('Cookie').find('=',index_s)
			index_e = dic.get('Cookie').find(';',index_s)
			if index_e!=-1:
				token = dic.get('Cookie')[index_s+1:index_e]
			else:
				token = dic.get('Cookie')[index_s+1:]
			sessid = dic.get('__XIAMI_SESSID')
			cookie = dic.get('Cookie')
			cookie += ('; __XIAMI_SESSID='+sessid)
			li = cookie.split(';')
			xiami_cookie = {}
			for i in li:
				i_li = i.split('=')
				xiami_cookie[i_li[0]] = i_li[1]
			if XU.set_favor_song(id_,token,xiami_cookie):
				ret = 'True'
			#link = XU.get_link(id_)+';'+cover
		else:
			ret = 'False'
	return HttpResponse(ret)
