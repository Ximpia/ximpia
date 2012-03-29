# Django settings for ximpia project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

#python -m smtpd -n -c DebuggingServer localhost:1025

# Ximpia Config
PRIVATE_BETA = True
AFFILIATES = False
WEBMASTER_EMAIL = '"Webmaster :: Ximpia" <webmaster@ximpia.com>'
MAIL_HOST = '127.0.0.1:8000'

# Ximpia Email
XP_EMAIL_USERNAME = 'jorge.alegre'
XP_EMAIL_PASSWORD = 'tarraco24'
XP_EMAIL_HOST = 'smtp.zoho.com'
# Real Email server
#EMAIL_HOST = 'smtp.zoho.com'
#EMAIL_PORT = 465
#EMAIL_HOST_USER = 'jorge.alegre'
#EMAIL_HOST_PASSWORD = 'tarraco24'
#EMAIL_USE_TLS = True

# Dumb email server
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025

# Facebook
FACEBOOK_APP_COOKIE = 'fbs_180219935334975'
FACEBOOK_APP_ID = '180219935334975'
FACE_APP_SECRET = '59cd2a9eafc76ed2262d317a25059daa'

OAUTH2_REDIRECT = 'http://localhost:8000/oauth2/'

# Scopes
FACEBOOK_SCOPE = 'email,user_birthday'

# CONSUMER_DICT
CONSUMER_DICT = {}
CONSUMER_DICT['linkedin'] = ('UqqNxkAHjuhRzW4PMdyq2H-_MqWyFTDmTtTOfa6TiIX_Nu73_f7YdWNtI__yUnl5','Gy75y7RJrq1T5_JJrTs55B6r04_ntUgSpoy-9WwMoFdFBTF1EikomP1dbWxxtYXv','1.0')
CONSUMER_DICT['twitter'] = ('IKVUuIYtnNRCTyCksySXkg', 'fqsB8GAz8xtqvirPyaEFLTCGUPMHQ5h2rAiASkpsg', '1.0')
CONSUMER_DICT['facebook'] = ('180219935334975', '59cd2a9eafc76ed2262d317a25059daa', '2.0')

# OAUTH_URL_DICT
OAUTH_URL_DICT = {}
OAUTH_URL_DICT['linkedin'] = {
                 'request': ('https://api.linkedin.com/uas/oauth/requestToken', 'POST'),
                 'access': ('https://api.linkedin.com/uas/oauth/accessToken','POST'),
                 'authorized': ('https://api.linkedin.com/uas/oauth/authenticate','')
                 }
OAUTH_URL_DICT['twitter'] = {
                 'request': ('https://api.twitter.com/oauth/request_token', 'POST'),
                 'access': ('https://api.twitter.com/oauth/access_token','POST'),
                 'authorized': ('https://api.twitter.com/oauth/authenticate','')
                 }
OAUTH_URL_DICT['facebook'] = {
                 'authorize': ('https://graph.facebook.com/oauth/authorize?client_id=180219935334975&display=popup&redirect_uri=' + OAUTH2_REDIRECT + 'facebook&scope=' + FACEBOOK_SCOPE, ''),
                 'access': ('https://graph.facebook.com/oauth/access_token','')
                 }
#https://graph.facebook.com/oauth/authorize?client_id=180219935334975&redirect_uri=http://localhost:8000/oauth2/facebook


ADMINS = (
     ('Jorge Alegre', 'jorge.alegre@tecor.com'),
)

MANAGERS = ADMINS

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
#        'NAME': 'XIMPIA',                      # Or path to database file if using sqlite3.
#        'USER': 'buscaplus',                      # Not used with sqlite3.
#        'PASSWORD': '1V0!ppbF',                  # Not used with sqlite3.
#        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
#        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
#    }
#}

# Windows
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'XIMPIA',                      # Or path to database file if using sqlite3.
        'USER': 'root',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Madrid'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/site_media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'
#ADMIN_MEDIA_PREFIX = 'http://static.buscaplus.com/admin_media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '&$xqvgkb-q@g0cyfzhe^euu^0@v_a$x((dobrr&9j4*=y)cb^9'

SESSION_COOKIE_DOMAIN = ''
SESSION_COOKIE_AGE = 150000000
SESSION_COOKIE_NAME = 'test-sessionid'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
)

ROOT_URLCONF = 'ximpia.urls'
FONT_HOME = '/mnt/django_projects/Ximpia/fonts/'

# CAPTCHA
CAPTCHA_LETTERS = 'WwEeRrTtYUPASFfGgKZXCVBNnM123456789'
CAPTCHA_COLOURS = ((255,0,0), (0,100,255), (0,255,0), (0,0,255), (0,0,0)) 
CAPTCHA_FONTS = (
    FONT_HOME + 'arial.ttf',
    FONT_HOME + 'verdana.ttf',
)
CAPTCHA_FONT_SIZE = 25
CAPTCHA_LENGTH = 6
CAPTCHA_NAME = 'captcha'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    "H:/workspace/Ximpia/templates"
    #"/home/jalegre/workspace/Ximpia/templates"
    #"/media/truecrypt1/workspace/Ximpia/templates"
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.humanize',
    'ximpia.site',
    'ximpia.social_network',
    'ximpia.core',
    #'ximpia.tasks',
    #'ximpia.notes',
    #'ximpia.messages',
    #'ximpia.sales',
    #'ximpia.support',
    #'ximpia.human_resources',
    #'ximpia.business',
    #'ximpia.data',
    'ximpia.util'
)
