from django.conf.urls.defaults import patterns, include

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

#from django.views.static import serve

urlpatterns = patterns('',
		
	# Uncomment the admin/doc line below and add 'django.contrib.admindocs'
	# to INSTALLED_APPS to enable admin documentation:
	(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	
	# Uncomment the next line to enable the admin:
	(r'^admin/', include(admin.site.urls)),
	
	# CoreDjango
	(r'^site_media/apps/core/(?P<path>.*)$', 'django.views.static.serve',{'document_root': 'H:/workspace/CoreDjango/media/apps/core'}),
	# XimpiaDjango
	(r'^site_media/apps/site/(?P<path>.*)$', 'django.views.static.serve',{'document_root': 'H:/workspace/XimpiaDjango/media/apps/site'}),
	#(r'^site_media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': 'H:/workspace/XimpiaDjango/media'}),
	# XimpiaApps
	(r'^site_media/apps/testScrap/(?P<path>.*)$', 'django.views.static.serve',{'document_root': 'H:/workspace/XimpiaApps/media/apps/testScrap'}),
	# Frontend
	(r'^site_media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': 'H:/workspace/XimpiaFront/media'}),
	# captcha
	(r'^captcha/', include('yacaptcha.urls')),
)

urlpatterns += patterns('ximpia',
    
    # Example:
    # (r'^ximpia/', include('ximpia.foo.urls')),

    # backdoor?????
    #(r'^backDoor/', include(admin.site.urls)),
    
    # Home
    (r'^$', 'site.views.home'),
    
    #(r'^oauth/(?P<service>.*)$', 'social_network.views.oauth'),
    #(r'^oauth2/(?P<service>.*)$', 'social_network.views.oauth20'),
    
    # Media
    #(r'^site_media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': '/mnt/django_projects/ximpia/media'}),
    #(r'^site_media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': '/media/truecrypt1/workspace/Ximpia/media'}),
    #(r'^site_media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': 'H:/workspace/Ximpia/media'}),
    
    # signupUser
    #(r'^signup/(?P<invitationCode>\w+)$', 'social_network.views.signup'),
    #(r'^signup$', 'social_network.views.signup'),
    
    # signupOrganization
    #(r'^signupOrganization/(?P<invitationCode>\w+)$', 'social_network.views.signupOrganization'),
    #(r'^signupOrganization$', 'social_network.views.signupOrganization'),
    
    # activateUser
    #(r'^activateUser/(?P<user>.*)/(?P<activationCode>[0-9]+)$', 'social_network.views.activateAccount'),

    # Reload captcha
    #(r'^reloadCaptcha$', 'social_network.views.reloadCaptcha'),    

    # Social network and applications
    #(r'^$', 'social_network.views.staticContent'),
    #(r'^', 'social_network.views.test'),
    #(r'^(?P<templateName>\w+)$', 'social_network.views.staticContent'),
    #(r'^view/', include('ximpia.social_network.urls')),
    
    # Where $appUrlName will be the url friendly name for the application
    #(r'^view/$appUrlName/', include('ximpia.social_network.urls')),
)

urlpatterns += patterns('ximpia_core',

    # Ximpia Templates
    (r'^jxTemplate/(?P<app>.*)/(?P<mode>.*)/(?P<tmplName>.*)$', 'core.views.jxTemplate'),
    # Exec Server action
    (r'^apps/(?P<app>.*)/do/(?P<actionName>.*)/(?P<actionAttrs>.*)$', 'core.views.execActionMsg'),		
    # Show Server View
    (r'^apps/(?P<app>.*)/(?P<viewName>.*)/(?P<viewAttrs>.*)$', 'core.views.showView'),
    # Ajax Urls
    (r'^jxSuggestList$', 'core.views.jxSuggestList'),
    (r'^jxJSON$', 'core.views.jxJSON'),
    (r'^jxBusiness$', 'core.views.jxBusiness'),
    (r'^jxSearchHeader$', 'core.views.searchHeader'),        
)
