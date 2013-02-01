# coding: utf-8

from django.conf.urls.defaults import patterns

urlpatterns = patterns('',
    # Ximpia Templates
    (r'^jxTemplate/(?P<app>.*)/(?P<mode>.*)/(?P<tmplName>.*)$', 'ximpia.core.views.jxTemplate'),
    # Exec Server action
    (r'^apps/(?P<appSlug>[a-zA-Z0-9-]+)/do/(?P<actionSlug>[a-zA-Z0-9-]+)/(?P<actionAttrs>.*)$', 'ximpia.core.views.execActionMsg'),		
    # Show Server View
    (r'^apps/(?P<appSlug>[a-zA-Z0-9-]+)/(?P<viewSlug>[a-zA-Z0-9-]+)/(?P<viewAttrs>.*)$', 'ximpia.core.views.showView'),
    # Ajax Urls
    (r'^jxSuggestList$', 'ximpia.core.views.jxSuggestList'),
    (r'^jxJSON$', 'ximpia.core.views.jxJSON'),
    (r'^jxService$', 'ximpia.core.views.jxService'),
    (r'^jxSearchHeader$', 'ximpia.core.views.searchHeader'),        
)
