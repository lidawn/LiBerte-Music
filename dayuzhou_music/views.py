#coding:utf-8
from django.shortcuts import render
from django.http import HttpResponseRedirect
from Xiami import XiamiUser as XU , XiamiSong as XS
from Netease import NeteaseUser as NU , NeteaseSong as NS

def index(request):
	if request.method=="GET":
		netease_user = NU('a','b','c')
		netease_user.get_discover()
		result_netease = {
			'new_cd' : netease_user.new_cd ,
			'hot_recommend' : netease_user.hot_recommend,
		}
		xiami_user = XU('a','b','c')
		xiami_user.get_discover()
		result_xiami = {
			'new_cd' : xiami_user.new_cd ,
			'hot_recommend' : xiami_user.hot_recommend,
			'daxia' : xiami_user.daxia,
		}
		#做一下去重
		results = {
			'result_netease' : result_netease,
			'result_xiami' : result_xiami
		}
		return render(request,'index.html',{'results':results,})