#coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
from Netease import NeteaseUser as NU , NeteaseSong as NS
from Xiami import XiamiUser as XU , XiamiSong as XS
from models import User
import json,requests,re
from bs4 import BeautifulSoup as BS

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

user_agent = '''Mozilla/5.0 (Windows NT 10.0; WOW64) 
						AppleWebKit/537.36 (KHTML, like Gecko) 
						Chrome/46.0.2490.80 
						Safari/537.36
			'''

def netease_song(id_):
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

	URL = 'http://music.163.com/api/song/detail?ids=[' + id_+']'
	resp = requests.get(URL,cookies=cookies,headers=headers)
	song_list = []
	try:
		content = resp.json() 
		song = content['songs'][0]
		print song
		duration = song.get('duration')/1000
		prepend_zero = lambda x : ('0'+x) if (len(x)==1) else x
		duration = prepend_zero(str(duration/60)) + ':' + prepend_zero(str(duration%60))
		name = song.get('name')
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
		results = {
			'song_list' : song_list,
			'song_list_str' : json.dumps(song_list)
		}
	except:
		results = None

	return results

def netease_playlist(id_):
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

	#URL = 'http://music.163.com/playlist?id=' + id_
	URL = 'http://music.163.com/api/playlist/detail?id=' + id_
	resp = requests.get(URL,cookies=cookies,headers=headers)
	#print resp.content
	try:
		content = resp.json() 
		playlist = content.get('tracks',None)
		if playlist is None:
			playlist = content['result']['tracks']
		song_list = []
		for song in playlist:
			duration = song.get('duration')/1000
			prepend_zero = lambda x : ('0'+x) if (len(x)==1) else x
			duration = prepend_zero(str(duration/60)) + ':' + prepend_zero(str(duration%60))
			name = song.get('name')
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
			print result
			song_list.append(result)
		results = {
			'song_list' : song_list,
			'song_list_str' : json.dumps(song_list)
		}
	except:
		results = None

	return results

def netease_album(id_):
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

	URL = 'http://music.163.com/api/album/' + id_
	resp = requests.get(URL,cookies=cookies,headers=headers)
	try:
		content = resp.json() 
		playlist = content['album']['songs']
		song_list = []
		for song in playlist:

			duration = song.get('duration')/1000
			prepend_zero = lambda x : ('0'+x) if (len(x)==1) else x
			duration = prepend_zero(str(duration/60)) + ':' + prepend_zero(str(duration%60))
			name = song.get('name')
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
			#print song_list
		results = {
			'song_list' : song_list,
			'song_list_str' : json.dumps(song_list)
		}
	except:
		results = None

	return results

def xiami_playlist(request,id_):
	URL = 'http://www.xiami.com/song/playlist/id/%s/type/3' % id_
	headers = {'user-Agent':user_agent,'connection':'keep-alive'}
	xml = requests.get(URL,headers=headers)
	root = ET.fromstring(str(xml.content))
	tracklist = root[0]
	song_list = []
	for track in tracklist:
		name = track[0].text
		mp3Url = XS.decode_link(track[12].text)
		prepend_zero = lambda x : ('0'+x) if (len(x)==1) else x
		duration = int(track[18].text)
		duration = prepend_zero(str(duration/60)) + ':' + prepend_zero(str(duration%60))
		artist_name = track[9].text
		artist_id = track[20].text
		song_id = track[1].text
		album_name = track[3].text
		album_id = track[2].text
		cover = track[17].text
		result = {
				'id' : song_id,
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
		'detail' : song_list,
		'detail_str' : json.dumps(song_list)
	}
	return render(request,'xiami_detail.html',{'profile':profile,})

def xiami_album(request,id_):
	URL = 'http://www.xiami.com/song/playlist/id/%s/type/1' % id_
	headers = {'user-Agent':user_agent,'connection':'keep-alive'}
	xml = requests.get(URL,headers=headers)
	root = ET.fromstring(str(xml.content))
	tracklist = root[0]
	song_list = []
	for track in tracklist:
		name = track[0].text
		mp3Url = XS.decode_link(track[12].text)
		prepend_zero = lambda x : ('0'+x) if (len(x)==1) else x
		duration = int(track[18].text)
		duration = prepend_zero(str(duration/60)) + ':' + prepend_zero(str(duration%60))
		artist_name = track[9].text
		artist_id = track[20].text
		song_id = track[1].text
		album_name = track[3].text
		album_id = track[2].text
		cover = track[17].text
		result = {
				'id' : song_id,
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
		'detail' : song_list,
		'detail_str' : json.dumps(song_list)
	}
	return render(request,'xiami_detail.html',{'profile':profile,})