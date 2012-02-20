import types
import traceback

from django.db import models
from django.contrib.auth.models import User as UserSys, Group as GroupSys
from django.utils.translation import ugettext as _
from ximpia import settings
from django.utils import translation
#from ximpia.core.choices import Choices
#from ximpia.core.constants import Constants
#from ximpia.core.validators import *

from choices import Choices

class DeleteManager(models.Manager):
	def get_query_set(self):
		return super(DeleteManager, self).get_query_set().filter(delete=False)

class BaseModel(models.Model):
	"""Abstract Base Model"""
	_ctx = None
	dateCreate = models.DateTimeField(auto_now_add=True, null=True, blank=True, editable=False, 
					verbose_name= _('Create Date'), help_text= _('Create Date'))
	dateModify = models.DateTimeField(auto_now=True, null=True, blank=True, editable=False, 
					verbose_name= _('Modify Date'), help_text= _('Modify Date'))
	userCreateId = models.IntegerField(null=True, blank=True, editable=False, 
					verbose_name=_('User Create Id'), help_text=_('User that data'))
	userModifyId = models.IntegerField(null=True, blank=True, editable=False, 
					verbose_name=_('User Modify Id'), help_text=_('User that madofied data'))
	delete = models.BooleanField(default=False, editable=False,
				verbose_name=_('Delete'), help_text=_('Field that sets logical deletes'))
	"""def __init__(self, ctx=None, *argsTuple, **argsDict):
		self._ctx = ctx if ctx != None else None
		super(BaseModel, self).__init__(*argsTuple, **argsDict)"""
	objects = DeleteManager()
	objects_del = models.Manager()
	"""def save(self, ctx, *argsTuple, **argsDict):
		if self.pk:
			self.userModifyId = self._ctx.user.id
		else:
			self.userCreateId = self._ctx.user.id
		super(BaseModel, self).save(*argsTuple, **argsDict)"""
	class Meta:
		abstract = True

class MasterValue(BaseModel):
	"""Master Values"""
	name = models.CharField(max_length=50,
			verbose_name=_('Name'), help_text=_('Name'))
	value = models.CharField(max_length=100,
			verbose_name=_('Value'), help_text=_('Value'))
	type = models.CharField(max_length=30, db_index=True,
			verbose_name=_('Type'), help_text=_('Type'))
	def __unicode__(self):
		return str(self.name) + ' => ' + str(self.value)
	class Meta:
		db_table = 'SN_MASTER_VALUE'
		verbose_name = _('Master Value')
		verbose_name_plural = _('Master Values')

class UserParam(BaseModel):
	"""User Parameters"""
	mode = models.CharField(max_length=20, 
			verbose_name=_('Mode'), help_text=_('Parameter Mode'))
	name = models.CharField(max_length=20, 
			verbose_name=_('Name'), help_text=_('Parameter Name'))
	value = models.CharField(max_length=100, null=True, blank=True, 
			verbose_name=_('Value'), help_text=_('Parameter Value for Strings'))
	valueId = models.IntegerField(null=True, blank=True, 
			verbose_name=_('Value Id'), help_text=_('Parameter Value for Integers'))
	def __unicode__(self):
		return str(self.mode) + ' - ' + str(self.name)
	class Meta:
		db_table = 'SN_PARAM'
		verbose_name = "User Parameter"
		verbose_name_plural = "User Parameters"

class XmlMessage(BaseModel):
	"""XML Message"""
	name = models.CharField(max_length=255,
			verbose_name = _('Name'), help_text = _('Code name of XML'))
	lang = models.CharField(max_length=2, choices=Choices.LANG, default=Choices.LANG_ENGLISH,
			verbose_name = _('Language'), help_text = _('Language for xml'))
	body = models.TextField(verbose_name = _('Xml Content'), help_text = _('Xml content'))
	def __unicode__(self):
		return str(self.name)
	class Meta:
		db_table = 'SN_XML_MESSAGE'
		verbose_name = _('Xml Message')
		verbose_name_plural = _('Xml Messages')

class XpMsgException(Exception):
	Msg = ''
	Exception = None
	ArgsDict = {}
	def __init__(self, exception, msg, **argsDict):
		"""Doc.
		@param exception: 
		@param msg: 
		@param **argsDict: """
		self.Msg = msg
		self.Exception = exception
		self.ArgsDict = argsDict
	def _log(self, exception, msg, argsDict):
		"""Will use log facility of django 1.3"""
		"""txt = repr(self.Exception)
		for name in self.ArgsDict.keys():
			txt += name + ':' + self.ArgsDict[name]
		txt += ' ' + self.Msg"""
		# Log txt  in error log
		traceback.print_exc()
	def __str__(self):
		#self._log()
		#return repr(self.Msg)
		return self.Msg


def getDataDict(form):
	"""Doc."""
	try:
		dict = form.cleaned_data
		if type(dict) != types.DictType:
			dict = form.data
		else:
			dict = form.cleaned_data
	except:
		dict = form.data
	return dict

def getFormDataValue(form, keyName):
	"""Doc."""
	try:
		dict = form.cleaned_data
		if type(dict) != types.DictType:
			dict = form.data
			keyValue = form.data[keyName]
		else:
			dict = form.cleaned_data
			if dict.has_key(keyName):
				keyValue = dict[keyName]
			else:
				keyValue = form.data[keyName]
	except KeyError:
		keyValue = ''
	return keyValue

def setIfNotBlank():
	"""Doc."""
	pass

def getFromDict(key, dict):
	"""Get value from a dict for key. If not found, returns blank string."""
	value = ''
	if dict.has_key(key):
		value = dict[key]
	return value

def getPagingStartEnd(page, numberMatches):
	"""Get tuple (iStart, iEnd)"""
	iStart = (page-1)*numberMatches
	iEnd = iStart+numberMatches
	tuple = (iStart, iEnd)
	return tuple

def parseText(content):
	"""Parse text from content. Useful for indexing fields.
	@param content: 
	@return: parsed text"""
	text = ''
	# TODO: Finish parse with code found in B+
	return text

def parseLinks(content):
	"""Parse links from content
	@param content: 
	@return: linkList"""
	linkList = []
	# TODO: Finish parse with code found in B+
	return linkList 

##############################################################################################

def context(f):
	"""Context and inital variables packed into ArgsDict"""
	def new_f(*ArgsTuple, **ArgsDict):
		print 'context....'
		request = ArgsTuple[0]
		# ContextDict
		lang = translation.get_language()
		contextDict = {
				'lang': lang,
				'settings': settings,
				}
		#ArgsDict['contextDict'] = contextDict
		# lang
		#ArgsDict['lang'] = lang
		# Context
		ctx = ContextObj(request.user, lang, contextDict, request.session, request.COOKIES, request.META)
		# userSocial and socialChannel
		if request.REQUEST.has_key('socialChannel') and request.user.is_authenticated():
			ctx.socialChannel = request.REQUEST['socialChannel']			
		ArgsDict['ctx'] = ctx
		resp = f(*ArgsTuple, **ArgsDict)
		return resp
	return new_f

class Context(object):
	USER = 'user'
	LANG = 'lang'
	SETTINGS = 'settings'
	SESSION = 'session'
	COOKIES = 'cookies'
	META = 'meta'
	POST = 'post'
	REQUEST = 'request'
	GET = 'get'
	SOCIAL_CHANNEL = 'socialChannel'
	USER_SOCIAL = 'userSocial'
	AUTH = 'auth'
	FORM = 'form'
	CAPTCHA = 'captcha'
	RAW_REQUEST = 'raw_request'
	JS_DATA = 'jsData'
	def __init__(self, f):
		self.f = f
	def __call__(self, *argsTuple, **argsDict):
		"""Decorator call method"""
		request = argsTuple[0] 
		langs = ('en')
		lang = translation.get_language()
		if lang not in langs:
			lang = 'en'
		ctx = {}
		ctx['user'] = request.user
		ctx['lang'] = lang
		ctx['settings'] = settings
		ctx['session'] = request.session
		ctx['cookies'] = request.COOKIES
		ctx['meta'] = request.META
		ctx['post'] = request.POST
		ctx['request'] = request.REQUEST
		ctx['raw_request'] = request
		ctx['get'] = request.GET
		ctx['socialChannel'] = ''
		ctx['userSocial'] = ''
		ctx['auth'] = {}
		ctx['form'] = None
		ctx['captcha'] = None
		ctx[self.JS_DATA] = ''
		if request.REQUEST.has_key('socialChannel') and request.user.is_authenticated():
			ctx['socialChannel'] = request.REQUEST['socialChannel']
			ctx['userSocial'] = request.REQUEST['userSocial']
		argsDict['ctx'] = ctx
		resp = self.f(*argsTuple, **argsDict)
		return resp

class XpTemplate(object):
	_tmplDict = {}
	def __init__(self, tmplDict, *argsTuple, **argsDict):
		self._tmplDict = tmplDict
	def __call__(self, f):
		"""Decorator call method"""		
		def wrapped_f(*argsTuple, **argsDict):
			"""Doc."""
			argsDict['tmplDict'] = self._tmplDict
			resp = f(*argsTuple, **argsDict)
			return resp			
		return wrapped_f

##############################################################################################

class ContextObj(object):
	_user = None
	_userSocial= None
	_socialChannel = ''
	_lang = ''
	_context = {}
	_session = {}
	_cookies = {}
	_META = {}
	def __init__(self, user, lang, contextDict, session, cookies, META):
		self._user = user
		self._lang = lang
		self._context = contextDict
		self._session = session
		self._cookies= cookies
		self._META = META
	def _getUser(self):
		"""Get user"""
		return self._user
	def _getLang(self):
		return self._lang
	def _getContextDict(self):
		"""Doc."""
		return self._context
	def _setUser(self, user):
		"""Sets user"""
		self._user = user
	def _setLang(self, lang):
		"""Doc."""
		self._lang = lang
	def _setContextDict(self, contextDict):
		"""Doc."""
		self._context = contextDict
	def _getSession(self):
		"""Doc."""
		return self._session
	def _getCookies(self):
		"""Doc."""
		return self._cookies
	def _getMETA(self):
		"""Doc."""
		return self._META
	def _getUserSocial(self):
		"""Doc."""
		return self._userSocial
	def _getSocialChannel(self):
		"""Doc."""
		return self._socialChannel
	def _setSession(self, session):
		"""Doc."""
		self._session = session
	def _setCookies(self, cookies):
		"""Doc."""
		self._cookies = cookies
	def _setMETA(self, meta):
		"""Doc."""
		self._META = meta
	def _setUserSocial(self, userSocial):
		"""Doc."""
		self._userSocial = userSocial
	def _setSocialChannel(self, socialChannel):
		"""Doc."""
		self._socialChannel = socialChannel
	def __str__(self):
		dict = {'user': self._user, 'lang': self._lang, 'session': self._session, 'cookies': self._cookies, 'META': self._META, 'context': self._context}
		return str(dict)
	user = property(_getUser, _setUser)
	lang = property(_getLang, _setLang)
	context = property(_getContextDict, _setContextDict)
	session = property(_getSession, _setSession)
	cookies = property(_getCookies, _setCookies)
	META = property(_getMETA, _setMETA)
	userSocial = property(_getUserSocial, _setUserSocial)
	socialChannel = property(_getSocialChannel, _setSocialChannel)


class JsResultDict(dict):
	OK = 'OK'
	ERROR = 'ERROR'
	STATUS = 'status'
	RESPONSE = 'response'
	ERRORS = 'errors'
	def __init__(self):
		#print 'dict : ', statusIn, responseIn, errorsIn
		dict.__init__(self, status=self.OK, response={}, errors=[])
	def setStatus(self, status):
		"""Set status"""
		dict.__setitem__(self, self.STATUS, status)
	def setResponse(self, response):
		"""Set response"""
		dict.__setitem__(self, self.RESPONSE, response)
	def setErrors(self, errorList):
		"""Set error list"""
		dict.__setitem__(self, self.ERRORS, errorList)
	def addAttr(self, attrName, attrValue):
		"""Set attribute"""
		myDict = dict.__getitem__(self, self.RESPONSE)
		myDict[attrName] = attrValue
		dict.__setitem__(self, self.RESPONSE, myDict)
	def getAttr(self, attrName):
		"""Get attribute"""
		myDict = dict.__getitem__(self, self.RESPONSE)
		return myDict[attrName]
	def buildError(self, errorList):
		"""build error response"""
		dict.__setitem__(self, self.STATUS, self.ERROR)
		dict.__setitem__(self, self.ERRORS, errorList)
		dict.__setitem__(self, self.RESPONSE, {})

def getResultOK(dataDict, status='OK'):
	"""Build result dict for OK status. resultList is a list of objects or content to show in client"""
	resultDict = {}
	resultDict['status'] = status
	resultDict['response'] = dataDict
	resultDict['errors'] = []
	return resultDict

def getResultERROR(errorList, response={}):
	"""Build result dict for errors. status ir "ERROR" and response empty as default. "errors" has the errorList attribute"""
	resultDict = {}
	resultDict['status'] = 'ERROR'
	resultDict['response'] = response
	resultDict['errors'] = errorList
	return resultDict
