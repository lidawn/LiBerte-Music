#coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from Xiami import XiamiUser as XU , XiamiSong as XS
from Netease import NeteaseUser as NU , NeteaseSong as NS

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