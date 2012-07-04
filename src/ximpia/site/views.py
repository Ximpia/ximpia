import oauth2
import urlparse
import simplejson as json
import httplib2
import types
import traceback

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import login, authenticate
from django.utils import translation
from django.utils.translation import ugettext as _

from ximpia.core.models import context, Context, XpMsgException
from ximpia.core.data import ActionDAO, ViewDAO
from ximpia.core.util import getClass
from ximpia.core.business import Search, ViewDecorator
from constants import Constants as K
import forms
import business
from ximpia.util.http import Request
from ximpia.util.content import getContentRelaseDict
from ximpia import settings
from yacaptcha.models import Captcha

@Context(app=K.APP)
@ViewDecorator(K.APP, 'home')
def home(request, **args):
	print 'home....'
	video = business.VideoBusiness(args['ctx'])
	result = video.showHome()
	return result

@Context(app=K.APP)
def showVideo(request, videoName):
	result = None
	return result

@Context(app=K.APP)
def showContact(request):
	result = None
	return result

@Context(app=K.APP)
def doSendMessage(request):
	result = None
	return result
