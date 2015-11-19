#coding:utf-8
from django.shortcuts import render
from django.http import HttpResponseRedirect
from Xiami import XiamiUser as XU , XiamiSong as XS

def search(request):
	if request.method=="GET":
		if 'keywords' in request.GET :
			keywords = request.GET.get('keywords',None)
			print type(keywords)
			if keywords.replace(' ','') :
				results = XU.search(keywords)
				return render(request,'search.html',{'results':results,})
		
	return render(request,'search.html')
