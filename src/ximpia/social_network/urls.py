# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *
#from buscaplusweb import app_Main, app_SearchAccounts, util, search_themes

# http://buscaplus.com/view/*
urlpatterns = patterns('social_network.views',
		
	(r'^changePassword/(?P<userAccount>\w+)$', 'changePassword')

)
