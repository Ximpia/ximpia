from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

#from django.views.static import serve

urlpatterns = patterns('',
    
    # Example:
    # (r'^ximpia/', include('ximpia.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    
    (r'^oauth/(?P<service>.*)$', 'social_network.views.oauth'),
    (r'^oauth2/(?P<service>.*)$', 'social_network.views.oauth20'),
    
    (r'^captcha/', include('yacaptcha.urls')),
    
    # Media
    #(r'^site_media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': '/mnt/django_projects/ximpia/media'}),
    #(r'^site_media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': '/media/truecrypt1/workspace/Ximpia/media'}),
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': 'H:/workspace/Ximpia/media'}),
    
    # signupUser
    (r'^signup/(?P<invitationCode>\w+)$', 'social_network.views.signup'),
    (r'^signup$', 'social_network.views.signup'),
    
    # signupOrganization
    #(r'^signupOrganization/(?P<invitationCode>\w+)$', 'social_network.views.signupOrganization'),
    #(r'^signupOrganization$', 'social_network.views.signupOrganization'),
    
    # activateUser
    #(r'^activateUser/(?P<user>.*)/(?P<activationCode>[0-9]+)$', 'social_network.views.activateAccount'),

    # Reload captcha
    (r'^reloadCaptcha$', 'social_network.views.reloadCaptcha'),
    
    # Ajax Urls
    (r'^jxSuggestList$', 'social_network.views.jxSuggestList'),
    (r'^jxJSON$', 'social_network.views.jxJSON'),
    (r'^jxBusiness$', 'social_network.views.jxBusiness'),

    # Social network and applications
    (r'^$', 'social_network.views.staticContent'),
    #(r'^', 'social_network.views.test'),
    (r'^(?P<templateName>\w+)$', 'social_network.views.staticContent'),        
    
    # Ajax
    
    # User profile
    
    # Organization profile
    
    # Social Network    
    (r'^view/', include('ximpia.social_network.urls')),    
)
