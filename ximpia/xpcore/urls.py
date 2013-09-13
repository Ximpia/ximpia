# coding: utf-8

from django.conf.urls.defaults import patterns

urlpatterns = patterns('',
    # Ximpia Templates
    (r'^jxTemplate/(?P<app>.*)/(?P<mode>.*)/(?P<tmplName>.*)$', 'ximpia.xpcore.views.jxTemplate'),
    (r'^jxAppTemplate/(?P<app>.*)$', 'ximpia.xpcore.views.jxAppTemplate'),
    # Exec Server action
    (r'^(?P<appSlug>[a-zA-Z0-9-]+)/do/(?P<actionSlug>[a-zA-Z0-9-]+)/(?P<actionAttrs>.*)$', 'ximpia.xpcore.views.execActionMsg'),
    # Show Server View
    (r'^(?P<viewSlug>[a-zA-Z0-9-]+)/(?P<viewAttrs>.*)$', 'ximpia.xpcore.views.showView'),
    (r'^(?P<appSlug>[a-zA-Z0-9-]+)/(?P<viewSlug>[a-zA-Z0-9-]+)/(?P<viewAttrs>.*)$', 'ximpia.xpcore.views.showView'),
    # Ajax Urls
    (r'^jxSuggestList$', 'ximpia.xpcore.views.jxSuggestList'),
    (r'^jxJSON$', 'ximpia.xpcore.views.jxJSON'),
    (r'^jxService$', 'ximpia.xpcore.views.jxService'),
    (r'^jxDataQuery$', 'ximpia.xpcore.views.jxDataQuery'),
    (r'^jxSave$', 'ximpia.xpcore.views.jxSave'),
    (r'^jxDelete$', 'ximpia.xpcore.views.jxDelete'),
    (r'^jxSearchHeader$', 'ximpia.xpcore.views.jxSearchHeader'),        
)
