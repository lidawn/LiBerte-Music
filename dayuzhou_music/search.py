#coding:utf-8
from django.shortcuts import render
from django.http import HttpResponseRedirect
from Xiami import XiamiUser as XU , XiamiSong as XS

def search(request):
	if request.method=="GET":
		if 'keywords' in request.GET :
			keywords = request.GET.get('keywords')
			if keywords is not None:
				results = XU.search(keywords)
				return render(request,'search.html',{'results':results,})
		
	return render(request,'search.html')
