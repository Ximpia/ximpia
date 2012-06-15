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
from ximpia.core.business import Search

from constants import Constants as K
import forms

from ximpia.util.http import Request
from ximpia.util.content import getContentRelaseDict

from ximpia import settings
from yacaptcha.models import Captcha

@Context(app=K.APP)
def listMedia(request, categoryName=None, **args):
	result = None
	return result

@Context(app=K.APP)
def showMedia(request, mediaName):
	result = None
	return result

@Context(app=K.APP)
def showContact(request, mediaName):
	result = None
	return result

@Context(app=K.APP)
def doSendMessage(request, mediaName):
	result = None
	return result
