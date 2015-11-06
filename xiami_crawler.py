#coding:utf-8

import urllib2
import urllib
import re
import time
import pdb
#import mp3play
import os

def remove_backslash(input):
	index=input.find('\\')
	while index != -1 :
		back = input[index+1:]
		forward = input[0:index]
		input = forward + back
		index=input.find('\\')
		
	return input
	
def daxia():
	'''解析某一时刻大虾推荐'''
	base = "http://www.xiami.com/"
	url = base+"index/collect"
	headers = {'Accept':'image/webp',
	'User-Agent':'''Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6''',}
	req = urllib2.Request(url,headers=headers)
	content = urllib2.urlopen(req).read()
	pattern_song = re.compile(r'href=\\"\\/song\\/(.*?)>',re.S)
	pattern_singer = re.compile(r'singer\\"><a href=\\"\\/(.*?)target',re.S)
	result_song = pattern_song.findall(content)
	#file_song = open('info.txt',mode='a')
	#file_song.write(time.asctime())
	#file_song.write("\n===============================================\n")
	song_info = {}
	song_list = []
	for result in result_song:
		result = result.strip()
		index = result.find('\\')
		#index +=1
		link = base+"song/"+result[0:index]
		song_info['link'] = link
		song_info['id'] = link[link.rfind('/')+1:]
		#file_song.write("song_link: "+link+"\n")
		#print index
		title = result[result.find('"',index+2)+1:-1]
		title = title[0:-1]
		#print title
		title =  unicode(title,'unicode-escape')
		#print type(title)
		#file_song.write("song_title: "+title.encode('utf-8')+"\n")
		song_info['title'] = title
		song_list.append(song_info)
	
	result_singer = pattern_singer.findall(content)
	i=0
	#add singer information
	for result in result_singer:
		result = result.strip()
		index = result.find('"')
		link = base+result[0:index]
		link = remove_backslash(link)
		#print result
		#print link
		song_list[i]['singer_link'] = link
		#file_song.write("singer_link: "+link+"\n")
		#print index
		singer = result[result.find('"',index+2)+1:-1]
		singer = singer[0:-1]
		singer =  unicode(singer,'unicode-escape')
		#print title
		song_list[i]['singer'] = singer
		#file_song.write("singer_title: "+title.encode('utf-8')+"\n")
		i += 1
	
	return song_list

def xml_parse_url(list):
	'''返回带有真实播放地址，即下载地址的列表'''
	url = 'http://www.xiami.com/song/playlist/id/'
	for song in list:
		url += song['id']
		req_xml = urllib2.Request(url,headers=headers)
		xml_result = urllib2.urlopen(req_xml).read()
		pattern = re.compile(r'<location>(.*)</location>',re.S)
		result = pattern.findall(xml_result)
		luanma =  result[0]
		luanma =  luanma[1:]
		real_url = get_real_url(luanma)
		song['real_url'] = real_url
		#print luanma
		#print '\n'
	return list
		
#解密乱码得到真实url
def get_real_url(luanma):
	'''解密乱码得到真实url'''
	length = luanma.find('t',0)	
	juzhen = []
	a = len(luanma)
	#####矩阵总行数
	if a%length :
		line = a/length +1
		yushu = length - a%length
	else :
		line = a/length
		yushu = 0
	start = 0
	end = length
	#余数
	if yushu :
		#行的长度不一致，虾米黑科技
		#较长的行数
		line_1 = line - yushu
		i = line_1
		#处理较长的行数
		while i>0: 
			juzhen.append(luanma[start:end])
			#a = a-length
			start = end
			end += length
			i -= 1
		#处理剩余行数
		line_2 = line - line_1
		end -=1
		length -=1
		i = line_2
		while i>0 :
			juzhen.append(luanma[start:end])
			start = end
			end += length
			i -= 1
	else:
		#行的长度一致
		i = line
		while i>0: 
			juzhen.append(luanma[start:end])
			#a = a-length
			start = end
			end += length
			i -= 1

	#print juzhen[0]
	#pdb.set_trace()
	real_url = ''
	length = len(juzhen[0])
	i = 0
	#拼接为正确的url
	while i<length:
		j = 0
		while j<line:
			try:
				#print juzhen[j][i]
				real_url += juzhen[j][i]
			except IndexError:
				i = length
				j = line
				break
			j += 1
		i += 1

	while 1 :
		index = real_url.find('%')
		if index == -1:
			break
		if real_url[index:index+3] == '%3A' :
			real_url = real_url[0:index] + ':' + real_url[index+3:]
		elif real_url[index:index+3] == '%2F' :
			real_url = real_url[0:index] + '/' + real_url[index+3:]
		elif real_url[index:index+3] == '%5E' :
			real_url = real_url[0:index] + '0' + real_url[index+3:]
		elif real_url[index:index+3] == '%3F' :
			real_url = real_url[0:index] + '?' + real_url[index+3:]
		elif real_url[index:index+3] == '%3D' :
			real_url = real_url[0:index] + '=' + real_url[index+3:]

	return real_url

def play(list):
	#要加判断
	os.mkdir('.\\cache')
	#download
	for song in list:
		urllib.urlretrieve(song['real_url'],'.\\cache\\'+song['title']+'.mp3')
#file = open('xml.txt','a')
#file.write(xml_result)
#file.close()

def main():
	os.argv

if __name__=='__main__':
	main()