#coding:utf-8
from django.db import models

class User(models.Model):
	username = models.CharField(max_length=100)
	password = models.CharField(max_length=40)
	bound_xiami = models.BooleanField(default=False)
	xiami_type = models.IntegerField(default=1)			#1 虾米用户
	xiami_username =  models.CharField(max_length=100)    #是否有必要
	bound_netease = models.BooleanField(default=False)
	netease_username =  models.CharField(max_length=100)
	netease_uid = models.CharField(max_length=40)
	netease_cookies = models.CharField(max_length=1000)