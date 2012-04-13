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
from constants import CoreConstants as K, CoreKParam

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

class CoreParam(BaseModel):
	"""User Parameters"""
	mode = models.CharField(max_length=20, 
			verbose_name=_('Mode'), help_text=_('Parameter Mode'))
	name = models.CharField(max_length=20, 
			verbose_name=_('Name'), help_text=_('Parameter Name'))
	value = models.CharField(max_length=100, null=True, blank=True, 
			verbose_name=_('Value'), help_text=_('Parameter Value for Strings'))
	valueId = models.IntegerField(null=True, blank=True, 
			verbose_name=_('Value Id'), help_text=_('Parameter Value for Integers'))
	valueDate = models.DateTimeField(null=True, blank=True, 
			verbose_name = _('Value Date'), help_text = _('Parameter Value for Date'))
	def __unicode__(self):
		return str(self.mode) + ' - ' + str(self.name)
	class Meta:
		db_table = 'CORE_PARAMETER'
		verbose_name = "Parameter"
		verbose_name_plural = "Parameters"

class CoreXmlMessage(BaseModel):
	"""XML Message"""
	name = models.CharField(max_length=255,
			verbose_name = _('Name'), help_text = _('Code name of XML'))
	lang = models.CharField(max_length=2, choices=Choices.LANG, default=Choices.LANG_ENGLISH,
			verbose_name = _('Language'), help_text = _('Language for xml'))
	body = models.TextField(verbose_name = _('Xml Content'), help_text = _('Xml content'))
	def __unicode__(self):
		return str(self.name)
	class Meta:
		db_table = 'CORE_XML_MESSAGE'
		verbose_name = _('Xml Message')
		verbose_name_plural = _('Xml Messages')

class Application(BaseModel):
	"""Applications"""
	code = models.CharField(max_length=20,
		verbose_name = _('Code'), help_text = _('Application code'))
	name = models.CharField(max_length=30,
		verbose_name = _('Name'), help_text = _('Application name'))
	developer = models.ForeignKey(UserSys, null=True, blank=True,
		verbose_name = _('Developer'), help_text = _('Developer'))
	developerOrg = models.ForeignKey(GroupSys, null=True, blank=True,
		verbose_name = _('Organization'), help_text = _('Developer organization'))
	parent = models.ForeignKey('self', null=True, blank=True,
		verbose_name = 'Parent Application', help_text = 'Used for application groups. Application which this app is related to')
	subscription = models.BooleanField(default=False, 
		verbose_name = _('Subscription'), help_text = _('Is this application subscription based?'))
	private = models.BooleanField(default=False, 
		verbose_name = _('Private'), help_text = _('Is this application private to a list of groups?'))
	def __unicode__(self):
		return str(self.name)
	class Meta:
		db_table = 'CORE_APPLICATION'
		verbose_name = _('Application')
		verbose_name_plural = _('Applications')

class ApplicationAccess(BaseModel):
	"""User that have access to application. Used for subscription and private applications."""
	application = models.ForeignKey('core.Application',
				verbose_name = _('Application'), help_text = _('Application'))
	userSocial = models.ForeignKey('core.UserSocial', 
				verbose_name = _('User Social'), help_text = _('User Social or social channel needed to access application'))
	def __unicode__(self):
		return str(self.userSocial)
	class Meta:
		db_table = 'CORE_APP_ACCESS'
		verbose_name = 'Application Access'
		verbose_name_plural = "Application Access"

class UserSocial(BaseModel):
	"""Every user can have one or more social channels. In case social channels are disabled, only one registry will
	exist for each user."""
	user = models.ForeignKey(UserSys, 
				verbose_name = _('User'), help_text = _('User'))
	groups = models.ManyToManyField(GroupSys,
				verbose_name = _('Groups'), help_text = _('Groups'))
	title = models.CharField(max_length=20, 
				verbose_name = _('Channel Title'), help_text=_('Title for the social channel'))
	name = models.CharField(max_length=20, default=K.USER,
				verbose_name = _('Social Channel Name'), help_text = _('Name for the social channel'))
	isCompany = models.BooleanField(default=False,
				verbose_name=_('Company'), help_text=_('Is Company?'))
	def __unicode__(self):
		return str(self.user.username) + '-' + str(self.name)
	def getGroupById(self, groupId):
		"""Get group by id"""
		groups = self.groups.filter(pk=groupId)
		if len(groups) != 0:
			value = groups[0]
		else:
			value = None
		return value
	def getFullName(self):
		"""Get full name: firstName lastName"""
		name = self.user.get_full_name()
		return name
	class Meta:
		db_table = 'CORE_USER'
		verbose_name = 'User'
		verbose_name_plural = "Users"
		unique_together = ("user", "name")

class Menu(BaseModel):
	"""Menu"""
	name = models.CharField(max_length=10,
			verbose_name=_('Menu Name'), help_text=_('Name for menu, used in json menu objects'))
	titleShort = models.CharField(max_length=12,
			verbose_name=_('Short Title'), help_text=_('Short title for menu. Used under big icons'))
	title = models.CharField(max_length=30,
			verbose_name=_('Menu Title'), help_text=_('Title for menu item'))
	icon = models.ForeignKey('core.CoreParam', limit_choices_to={'mode': CoreKParam.ICON})
	parent = models.ForeignKey('self', null=True, blank=True,
				verbose_name=_('Parent Menu'), help_text=_('Parent menu for menu item'))
	def __unicode__(self):
		return str(self.title)
	class Meta:
		db_table = 'CORE_MENU'
		verbose_name = 'Menu'
		verbose_name_plural = "Menus"

class View(BaseModel):
	"""View"""
	application = models.ForeignKey('core.Application',
			verbose_name=_('Application'), help_text=_('Application for the view'))
	name = models.CharField(max_length=30,
			verbose_name=_('View Name'), help_text=_('View Name'))
	implementation = models.CharField(max_length=100,
			verbose_name=_('Implementation'), help_text=_('Business class and method that will show view'))
	def __unicode__(self):
		return str(self.name)
	class Meta:
		db_table = 'CORE_VIEW'
		verbose_name = 'View'
		verbose_name_plural = "Views"
		unique_together = ("application", "name")

class Action(BaseModel):
	"""Action"""
	application = models.ForeignKey('core.Application',
			verbose_name=_('Application'), help_text=_('Application for the action'))
	name = models.CharField(max_length=30,
			verbose_name=_('Action Name'), help_text=_('Action Name'))
	implementation = models.CharField(max_length=100,
			verbose_name=_('Implementation'), help_text=_('Business class and method that will process action'))
	def __unicode__(self):
		return str(self.name)
	class Meta:
		db_table = 'CORE_ACTION'
		verbose_name = 'Action'
		verbose_name_plural = "Action"
		unique_together = ("application", "name")

class ViewMenu(BaseModel):
	"""Menus associated to a view"""
	view = models.ForeignKey('core.View',
			verbose_name=_('View'), help_text=_('View'))
	menu = models.ForeignKey('core.Menu',
			verbose_name=_('Menu'), help_text=_('Menu'))
	order = models.IntegerField(default=10, 
			verbose_name=_('Order'), help_text=_('Order for the menu item. Start with 10, increment by 10'))
	separator = models.BooleanField(default=False,
			verbose_name=_('Menu Separator'), help_text=_('Separator for menu. Will show a gray line above menu item'))
	def __unicode__(self):
		return str(self.view) + '-' + str(self.menu)
	class Meta:
		db_table = 'CORE_VIEW_MENU'
		verbose_name = 'View Menu'
		verbose_name_plural = "Views for Menus"

class MenuParam(BaseModel):
	"""Parameters or attributes feeded to views"""
	menu = models.ForeignKey('core.Menu',
			verbose_name=_('Menu'), help_text=_('Menu')) 
	name = models.CharField(max_length=15,
			verbose_name=_('Param Name'), help_text=_('Name for the parameter or attribute'))
	value = models.CharField(max_length=20,
			verbose_name=_('Param Value'), help_text=_('Value for the parameter'))
	def __unicode__(self):
		return str(self.menu) + '-' + str(self.name)
	class Meta:
		db_table = 'CORE_MENU_PARAM'
		verbose_name = 'Menu Param'
		verbose_name_plural = "Menu Params"

class Workflow(BaseModel):
	"""WorkFlow"""
	application = models.ForeignKey('core.Application',
				verbose_name = _('Application'), help_text = _('Application'))
	viewSource = models.ForeignKey('core.View', related_name='viewSource', null=True, blank=True,
			verbose_name=_('Source View'), help_text=_('View which starts navigation'))
	viewTarget = models.ForeignKey('core.View', related_name='viewTarget', 
			verbose_name=_('target View'), help_text=_('View destiny for navigation'))
	action = models.ForeignKey('core.Action', related_name='wf_action',
			verbose_name=_('Action'), help_text=_('Action to process in the workflow navigation'))
	params = models.ManyToManyField('core.WFParam', through='core.WFParamValue', null=True, blank=True,
			verbose_name=_('Navigation Parameters'), help_text=_('Parameters neccesary to evaluate to complete navigation'))
	order = models.IntegerField(default=10,
			verbose_name=_('Order'), help_text=_('Order'))
	def __unicode__(self):
		return str(self.viewSource) + ' - ' + str(self.viewTarget) + ' - op - ' + str(self.action)
	class Meta:
		db_table = 'CORE_WF'
		verbose_name = 'Workflow'
		verbose_name_plural = "Workflow"
		unique_together = ('viewSource', 'action', 'viewTarget')

class WFParam(BaseModel):
	"""Parameters for WF"""
	application = models.ForeignKey('core.Application', 
				verbose_name = _('Application'), help_text = _('Application'))
	name = models.CharField(max_length=15, 
				verbose_name=_('Name'), help_text=_('Name'))
	title = models.CharField(max_length=30, 
				verbose_name=_('Title'), help_text=_('Title text for the parameter'))
	paramType = models.CharField(max_length=10, choices=Choices.BASIC_TYPES,
				verbose_name=_('Type'), help_text=_('Type'))
	def __unicode__(self):
		return str(self.title)
	class Meta:
		db_table = 'CORE_WF_PARAM'
		verbose_name = 'Workflow Parameter'
		verbose_name_plural = "Workflow Parameters"
		unique_together = ('application','name')

class WFParamValue(BaseModel):
	"""Parameter Values for WF"""
	flow = models.ForeignKey('core.WorkFlow', related_name='flow', 
			verbose_name=_('Flow'), help_text=_('Work Flow'))
	name = models.ForeignKey('core.WFParam', 
			verbose_name=_('Parameter'), help_text=_('Parameter'))
	operator = models.CharField(max_length=10, choices=Choices.OP, 
			verbose_name=_('Operator'), help_text=_('Operator'))
	value = models.CharField(max_length=20, 
			verbose_name=_('Value'), help_text=_('Value'))
	def __unicode__(self):
		return str(self.name) + ' ' + str(self.operator) + ' ' + str(self.value)
	class Meta:
		db_table = 'CORE_WF_PARAM_VALUE'
		verbose_name = 'Workflow Parameter Value'
		verbose_name_plural = "Workflow Parameter Values"

class XpMsgException(Exception):
	Msg = ''
	myException = None
	ArgsDict = {}
	def __init__(self, exception, msg, **argsDict):
		"""Doc.
		@param exception: 
		@param msg: 
		@param **argsDict: """
		self.Msg = msg
		self.myException = exception
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

class XpRegisterException(Exception):
	Msg = ''
	myException = None
	ArgsDict = {}
	def __init__(self, exception, msg, **argsDict):
		"""Doc.
		@param exception: 
		@param msg: 
		@param **argsDict: """
		self.Msg = msg
		self.myException = exception
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
		dd = form.cleaned_data
		if type(dd) != types.DictType:
			dd = form.data
		else:
			dd = form.cleaned_data
	except:
		dd = form.data
	return dd

def getFormDataValue(form, keyName):
	"""Doc."""
	try:
		dd = form.cleaned_data
		if type(dd) != types.DictType:
			dd = form.data
			keyValue = form.data[keyName]
		else:
			dd = form.cleaned_data
			if dd.has_key(keyName):
				keyValue = dd[keyName]
			else:
				keyValue = form.data[keyName]
	except KeyError:
		keyValue = ''
	return keyValue

def setIfNotBlank():
	"""Doc."""
	pass

def getFromDict(key, dd):
	"""Get value from a dict for key. If not found, returns blank string."""
	value = ''
	if dd.has_key(key):
		value = dd[key]
	return value

def getPagingStartEnd(page, numberMatches):
	"""Get tuple (iStart, iEnd)"""
	iStart = (page-1)*numberMatches
	iEnd = iStart+numberMatches
	fields = (iStart, iEnd)
	return fields

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
	FORMS = 'forms'
	CAPTCHA = 'captcha'
	RAW_REQUEST = 'raw_request'
	CTX = 'ctx'
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
		ctx['forms'] = {}
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
