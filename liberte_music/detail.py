#coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
from Netease import NeteaseUser as NU , NeteaseSong as NS
from models import User
import json,requests
from bs4 import BeautifulSoup as BS

user_agent = '''Mozilla/5.0 (Windows NT 10.0; WOW64) 
						AppleWebKit/537.36 (KHTML, like Gecko) 
						Chrome/46.0.2490.80 
						Safari/537.36
			'''

def netease_playlist(request,id_):
	'''网易歌单详情'''
	#id_是字符串
	#print id_
	headers = {
		'user-Agent':user_agent,
		'connection':'keep-alive',
		'Referer':'http://music.163.com/',
		'Accept': '*/*',
		'Accept-Encoding': 'gzip,deflate,sdch',
		'Accept-Language': 'zh-CN,zh;q=0.8,gl;q=0.6,zh-TW;q=0.4',
		'Content-Type': 'application/x-www-form-urlencoded',
		'Host': 'music.163.com'
	}

	cookies = {'appver':'2.0.2'}

	URL = 'http://music.163.com/playlist?id=' + id_
	resp = requests.get(URL,cookies=cookies,headers=headers)
	content = BS(resp.content)
	
	playlist_str = str(content.find('textarea'))[32:]
	playlist_str = playlist_str[ : playlist_str.rfind('<')]
	#print playlist_str[125200:125246]
	#playlist_str = playlist_str.replace('\'','\"')
	#print playlist_str[125211:125246]
	playlist = json.loads(playlist_str)
	song_list = []
	for song in playlist:
		name = song.get('name')
		duration = song.get('duration')/1000
		duration = str(duration/60) + ':' + str(duration%60)
		id_ = song.get('id')
		artist_name = song.get('artists')[0].get('name')
		artist_id = song.get('artists')[0].get('id')
		album_name = song.get('album').get('name')
		album_id = song.get('album').get('id')
		cover = song.get('album').get('blurPicUrl')
		mp3Url = song.get('mp3Url')

		result = {
				'id' : id_,
				'name' : name,
				'duration' : duration,
				'artist_name' : artist_name,
				'artist_id' : artist_id,
				'album_name' : album_name,
				'album_id' : album_id,
				'cover' : cover,
				'mp3Url' : mp3Url
		}
		song_list.append(result)

	profile = {
		'detail' : song_list
	}

	return render(request,'netease_detail.html',{'profile':profile,})


def xiami_playlist(request):
	pass