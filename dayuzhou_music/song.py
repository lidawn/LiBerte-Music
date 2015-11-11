#coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
from Xiami import XiamiUser as XU , XiamiSong as XS
from Netease import NeteaseUser as NU , NeteaseSong as NS

def get_link(request):
	if request.method=="POST":
		is_playable = request.POST.get('is_playable')
		id_ = request.POST.get('id')
		if is_playable :
			link =  XS.get_link(id_)
		else:
			name = request.POST.get('name')
			artist = request.POST.get('artist')
			album = request.POST.get('album')
			link =  NS.get_link(id_,name,artist,album)
		
	return HttpResponse(request,link)
