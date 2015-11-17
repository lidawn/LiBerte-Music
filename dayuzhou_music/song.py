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
		print is_playable
		id_ = request.POST.get('id')
		if is_playable == 'True' :
			link =  XS.get_link(id_)
		else:
			name = request.POST.get('name')
			artist = request.POST.get('artist')
			album = request.POST.get('album')
			ids = NS.parse_id(name,artist,album)
			if ids :
				link =  NS.get_link(ids.get('id'),ids.get('album_id'))
			else:
				link = '404'
		
	return HttpResponse(link)

@csrf_exempt
def get_net_link(request):
	if request.method=="POST":
		name = request.POST.get('name')
		artist = request.POST.get('artist')
		album = request.POST.get('album')
		ids = NS.parse_id(name,artist,album)
		if ids :
			link =  NS.get_link(ids.get('id'),ids.get('album_id'))
		else:
			link = ('404',)
		
	return HttpResponse(link)

#def test_put(request):
#	return render(request,'test_put.html')
#
#def test_get(request):
#	return render(request,'test_get.html')
#
#def test_open(request):
#	return render(request,'test_open.html')
#
#def add_song(request):
#	if request.method=="GET":
#		
#		return HttpResponse("1235678")