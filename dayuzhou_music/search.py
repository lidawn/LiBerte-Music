#coding:utf-8
from django.shortcuts import render
from django.http import HttpResponseRedirect


def search(request):
	if request.method=="GET":
		if 'keywords' in request.GET :
			keywords = request.GET.get('keywords')
			return HttpResponseRedirect('/search_result/')
		else:
			return render(request,'search.html')

def search_result(request):
	boundmessage = {'text':quyu_text+louhao_text+str(fangjian_text)}
	print boundmessage
	return render(request,'success.html',{'boundmessage':boundmessage,})