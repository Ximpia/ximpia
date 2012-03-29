# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *

# http://buscaplus.com/view/*
urlpatterns = patterns('social_network.views',

	(r'^changePassword/(?P<userAccount>\w+)$', 'changePassword'),
	(r'^signupUser/(?P<invitationCode>\w+)$', 'signupUser')

)
