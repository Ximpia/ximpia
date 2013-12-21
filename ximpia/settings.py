# Django settings for ximpia project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG
DEFAULT_CHARSET = 'utf-8'

# Dumb email server
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025

# Facebook
FACEBOOK_APP_COOKIE = ''
FACEBOOK_APP_ID = ''
FACE_APP_SECRET = ''
# Scopes
FACEBOOK_SCOPE = 'email'

RECAPTCHA_PRIVATE_KEY = ''

XIMPIA_OAUTH2_REDIRECT = 'http://localhost:8000/oauth2/'

ADMINS = (
     ('Jorge Alegre', 'ximpia.home@gmail.com'),
)

MANAGERS = ADMINS

# Windows
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# CACHE, used for ximpia templates
# TODO: Integrate with memcache: Having option to integrate with memecache, include config for memcache here...
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'default'
    }
}

# LOGGING
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(asctime)s %(message)s'
        },
    },
    'filters': {
    },
    'handlers': {
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
    'ximpia': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
    'ximpia.xpcore.data': {
        'handlers': ['console'],
        'level': 'DEBUG'
    },
    'ximpia.xpcore.views': {
        'handlers': ['console'],
        'level': 'DEBUG'
    },
    'ximpia_site': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
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

# Grappelli
GRAPPELLI_INDEX_DASHBOARD = 'ximpia_apps.dashboard.CustomIndexDashboard'
GRAPPELLI_ADMIN_TITLE = 'Ximpia Site'

# FileBrowser
FILEBROWSER_MEDIA_ROOT = ''
FILEBROWSER_MEDIA_URL = '/static/media/'
FILEBROWSER_DIRECTORY = ''
FILEBROWSER_SHOW_PLACEHOLDER = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/static/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Static
STATIC_URL = '/static/'
STATIC_ROOT = ''
STATICFILES_FINDERS = (
                       "django.contrib.staticfiles.finders.FileSystemFinder",
                       "django.contrib.staticfiles.finders.AppDirectoriesFinder"
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '&$xqvgkb-q@g0cyfzhe^euu^0@v_a$x((dobrr&9j4*=y)cb^9'

SESSION_COOKIE_DOMAIN = ''
SESSION_COOKIE_AGE = 5200000
SESSION_COOKIE_NAME = 'sessionid'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'ximpia.xpcore.backends.auth.SocialNetBackend'
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.locale.LocaleMiddleware',    
)

ROOT_URLCONF = 'ximpia.xpcore.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    "django.core.context_processors.request",
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
)

INSTALLED_APPS = (
    'grappelli.dashboard',
    'grappelli',
    'filebrowser',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.humanize',
    'django.contrib.staticfiles',
    'south',
    'ximpia.xpcore',
    'ximpia.xpsite'
)
