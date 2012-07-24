from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

#from django.views.static import serve

urlpatterns = patterns('',
	(r'^site_media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': 'H:/workspace/Ximpia/media'}),
	(r'^captcha/', include('yacaptcha.urls')),
)

urlpatterns += patterns('ximpia',
    
    # Example:
    # (r'^ximpia/', include('ximpia.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    
    # backdoor?????
    #(r'^backDoor/', include(admin.site.urls)),
    
    # Show Server View
    (r'^apps/(?P<app>.*)/(?P<viewName>.*)/(?P<viewAttrs>.*)$', 'core.views.showView'),
    
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
    
    # Ajax Urls
    (r'^jxSuggestList$', 'social_network.views.jxSuggestList'),
    (r'^jxJSON$', 'social_network.views.jxJSON'),
    (r'^jxBusiness$', 'social_network.views.jxBusiness'),
    (r'^jxSearchHeader$', 'social_network.views.searchHeader'),

    # Social network and applications
    #(r'^$', 'social_network.views.staticContent'),
    #(r'^', 'social_network.views.test'),
    #(r'^(?P<templateName>\w+)$', 'social_network.views.staticContent'),
    (r'^view/', include('ximpia.social_network.urls')),
    
    # Where $appUrlName will be the url friendly name for the application
    #(r'^view/$appUrlName/', include('ximpia.social_network.urls')),
)
