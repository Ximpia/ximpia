# coding: utf-8

from django.conf.urls.defaults import patterns, url

from ximpia.xpcore import views

urlpatterns = patterns('',
    # Ximpia Templates
    #url(r'^jxTemplate/(?P<app>.*)/(?P<mode>.*)/(?P<tmplName>.*)$', views.jxTemplate, name='template'),
    #url(r'^jxAppTemplate/(?P<app>.*)$', views.jxAppTemplate, name='app-template'),
    # Exec Server action
    url(r'^(?P<appSlug>[a-zA-Z0-9-]+)/do/(?P<actionSlug>[a-zA-Z0-9-]+)/(?P<actionAttrs>.*)$', views.execActionMsg, name='action-msg'),
    # Show Server View.
    url(r'^(?P<appSlug>[a-zA-Z0-9-]+)/$', views.showView, name='server-view-app'),
    url(r'^(?P<viewSlug>[a-zA-Z0-9-]+)/(?P<viewAttrs>.*)$', views.showView, name='server-view'),
    url(r'^(?P<appSlug>[a-zA-Z0-9-]+)/(?P<viewSlug>[a-zA-Z0-9-]+)/(?P<viewAttrs>.*)$', views.showView, name=''),
    # Ajax Urls
    #url(r'^jxSuggestList$', views.jxSuggestList, name='suggest'),
    #url(r'^jxJSON$', views.jxJSON, name='json'),
    #url(r'^jxService$', views.jxService, name='service'),
    #url(r'^jxDataQuery$', views.jxDataQuery, name='data-query'),
    #url(r'^jxSave$', views.jxSave, name='save'),
    #url(r'^jxDelete$', views.jxDelete, name='delete'),
    #url(r'^jxSearchHeader$', views.jxSearchHeader, name='search-header'),
    # server-side entities: service, model, collection
    # service would call ximpia service for view or action
    # model would call model data query
    # collection would call collection definition where we have data query details        
    url(r'^api/(?P<app_slug>[a-zA-Z0-9-]+)/(?P<slug>[a-zA-Z0-9-]+)/(?P<id>[0-9]+)$', 
        views.jx_api, name='api'),
    url(r'^api-model/(?P<app_slug>[a-zA-Z0-9-]+)/(?P<model>[a-zA-Z0-9-]+)/(?P<id>[0-9]+)$', 
        views.jx_model, name='api-model'),
)
