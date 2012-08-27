# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns

# http://buscaplus.com/view/*
urlpatterns = patterns('social_network.views',
	(r'^changePassword/(?P<ximpiaId>\w+)/(?P<reminderId>\w+)$', 'changePassword'),
	(r'^signupUser/(?P<invitationCode>\w+)$', 'signupUser')
)
