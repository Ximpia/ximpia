import base64
import time
import os
import cPickle
import random

from django.db import models
from django.contrib.auth.models import User as UserSys, Group as GroupSys
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session
from django.utils.hashcompat import md5_constructor
from django.http import HttpResponse

from ximpia import settings

class DeleteManager(models.Manager):
	def get_query_set(self):
		return super(DeleteManager, self).get_query_set().filter(Delete=False)

class Table(models.Model):
	Mode = models.CharField(max_length=20)
	Name = models.CharField(max_length=20)
	Value = models.CharField(max_length=100, null=True, blank=True)
	ValueId = models.IntegerField(null=True, blank=True)
	DateCreate = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	DateModify = models.DateTimeField(auto_now=True, null=True, blank=True)
	UserCreateId = models.IntegerField(null=True, blank=True)
	UserModifyId = models.IntegerField(null=True, blank=True)
	Delete = models.BooleanField(default=False)
	objects = DeleteManager()
	objects_del = models.Manager()
	def __unicode__(self):
		if self.ValueId:
			return str(self.ValueId)
		else:
			return str(self.Value)
	class Meta:
		db_table = 'MN_TABLES'
