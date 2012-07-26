import types
import traceback

from django.db import models
from django.contrib.auth.models import User, Group
from django.utils.translation import ugettext as _
from ximpia import settings
from django.utils import translation

from choices import Choices
import constants as K

from ximpia.util.js import Form as _jsf

def getBlankWfData(dd):
	"""Get workflow data inside flowCode by default"""
	dd['data'] = {}
	dd['viewName'] = ''
	return dd

class DeleteManager(models.Manager):
	def get_query_set(self):
		return super(DeleteManager, self).get_query_set().filter(isDeleted=False)

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
	isDeleted = models.BooleanField(default=False, editable=False,
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
	code = models.CharField(max_length=10,
		verbose_name = _('Code'), help_text = _('Application code'))
	name = models.CharField(max_length=30,
		verbose_name = _('Name'), help_text = _('Application name'))
	developer = models.ForeignKey(User, null=True, blank=True,
		verbose_name = _('Developer'), help_text = _('Developer'))
	developerOrg = models.ForeignKey(Group, null=True, blank=True,
		verbose_name = _('Organization'), help_text = _('Developer organization'))
	parent = models.ForeignKey('self', null=True, blank=True,
		verbose_name = 'Parent Application', help_text = 'Used for application groups. Application which this app is related to')
	subscription = models.BooleanField(default=False, 
		verbose_name = _('Subscription'), help_text = _('Is this application subscription based?'))
	private = models.BooleanField(default=False, 
		verbose_name = _('Private'), help_text = _('Is this application private to a list of groups?'))
	users = models.ManyToManyField('site.UserChannel', through='core.ApplicationAccess', related_name='app_access', null=True, blank=True,
			verbose_name=_('Users'), help_text=_('Users that have access to the application'))
	isAdmin = models.BooleanField(default=False,
		verbose_name = _('Is Admin?'), help_text = _('Is this application an admin backdoor?'))
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
	userChannel = models.ForeignKey('site.UserChannel', 
				verbose_name = _('User Social'), help_text = _('User Social or social channel needed to access application'))
	def __unicode__(self):
		return str(self.userChannel)
	class Meta:
		db_table = 'CORE_APP_ACCESS'
		verbose_name = 'Application Access'
		verbose_name_plural = "Application Access"

class SearchIndex(BaseModel):
	"""Index"""
	application = models.ForeignKey('core.Application',
			verbose_name=_('Application'), help_text=_('Application for seraching'))
	view = models.ForeignKey('core.View', null=True, blank=True, related_name='index_view',
			verbose_name=_('View'), help_text=_('View'))
	action = models.ForeignKey('core.Action', null=True, blank=True, related_name='index_action',
			verbose_name=_('Action'), help_text=_('Action'))
	title = models.CharField(max_length=70,
			verbose_name=_('Title'), help_text=_('Title'))
	words = models.ManyToManyField('core.Word', through='core.SearchIndexWord', related_name='index_words', 
			verbose_name=_('Index Parameters'), help_text=_('Parameters used in the search of content for views and actions'))
	params = models.ManyToManyField('core.Param', through='core.SearchIndexParam', related_name='index_params', null=True, blank=True,
			verbose_name=_('Index Parameters'), help_text=_('Parameters used in the search of content for views and actions'))
	def __unicode__(self):
		return str(self.title)
	class Meta:
		db_table = 'CORE_INDEX'
		verbose_name = 'Index'
		verbose_name_plural = "Index"
		unique_together = ("view", "action")

class SearchIndexWord(BaseModel):
	"""Index"""
	index = models.ForeignKey('core.SearchIndex',
			verbose_name=_('Index'), help_text=_('Index having application, view, action, title and parameters'))
	word = models.ForeignKey('core.Word',
			verbose_name=_('Word'), help_text=_('Word'))
	def __unicode__(self):
		return str(self.index) + '-' + str(self.word)
	class Meta:
		db_table = 'CORE_INDEX_WORD'
		verbose_name = 'Index Word'
		verbose_name_plural = "Index Words"

class Word(BaseModel):
	"""Word"""
	word = models.CharField(max_length=20, db_index=True, 
			verbose_name=_('Word'), help_text=_('Word'))
	def __unicode__(self):
		return str(self.word)
	class Meta:
		db_table = 'CORE_WORD'
		verbose_name = 'Word'
		verbose_name_plural = "Words"

class SearchIndexParam(BaseModel):
	"""Index Parameters"""
	searchIndex = models.ForeignKey('core.SearchIndex',
			verbose_name=_('Search Index'), help_text=_('Search Index'))
	name = models.ForeignKey('core.Param', 
			verbose_name=_('Parameter'), help_text=_('Parameter'))
	operator = models.CharField(max_length=10, choices=Choices.OP, 
			verbose_name=_('Operator'), help_text=_('Operator'))
	value = models.CharField(max_length=20, 
			verbose_name=_('Value'), help_text=_('Value'))
	def __unicode__(self):
		return str(self.name) + '-' + str(self.value)
	class Meta:
		db_table = 'CORE_INDEX_PARAM'
		verbose_name = 'Index Parameters'
		verbose_name_plural = "Index Parameters"

class Menu(BaseModel):
	"""Menu"""
	application = models.ForeignKey('core.Application',
			verbose_name=_('Application'), help_text=_('Application for the menu'))
	name = models.CharField(max_length=20, unique=True, 
			verbose_name=_('Menu Name'), help_text=_('Name for menu, used in json menu objects'))
	titleShort = models.CharField(max_length=12,
			verbose_name=_('Short Title'), help_text=_('Short title for menu. Used under big icons'))
	title = models.CharField(max_length=30,
			verbose_name=_('Menu Title'), help_text=_('Title for menu item'))
	icon = models.ForeignKey('core.CoreParam', limit_choices_to={'mode': K.PARAM_ICON},
			verbose_name=_('Icon'), help_text=_('Icon'))
	view = models.ForeignKey('core.View', null=True, blank=True, related_name='menu_view',
			verbose_name=_('View'), help_text=_('View'))
	action = models.ForeignKey('core.Action', related_name='menu_action', null=True, blank=True,  
			verbose_name=_('Action'), help_text=_('Action to process when click on menu item'))
	language = models.CharField(max_length=2, choices=Choices.LANG, default=Choices.LANG_ENGLISH, 
			verbose_name=_('Language'), help_text=_('Language'))
	params = models.ManyToManyField('core.Param', through='core.MenuParam', related_name='menu_params', null=True, blank=True,
			verbose_name=_('Menu Parameters'), help_text=_('Menu parameters sent to views'))
	def __unicode__(self):
		return str(self.titleShort)
	class Meta:
		db_table = 'CORE_MENU'
		verbose_name = 'Menu'
		verbose_name_plural = "Menus"

class ViewMenu(BaseModel):
	"""Menus associated to a view"""
	parent = models.ForeignKey('self', null=True, blank=True,
			verbose_name=_('Parent Menu'), help_text=_('Parent menu for menu item'))
	view = models.ForeignKey('core.View',
			verbose_name=_('View'), help_text=_('View'))
	menu = models.ForeignKey('core.Menu',
			verbose_name=_('Menu'), help_text=_('Menu'))
	order = models.IntegerField(default=10,
			verbose_name=_('Order'), help_text=_('Order for the menu item. Start with 10, increment by 10'))
	separator = models.BooleanField(default=False,
			verbose_name=_('Menu Separator'), help_text=_('Separator for menu. Will show a gray line above menu item'))
	zone = models.CharField(max_length=10, choices=Choices.MENU_ZONES,
				verbose_name=_('Menu Zone'), help_text=_('Menu Zone for menu item: sys, main and view zone'))
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
	name = models.ForeignKey('core.Param', 
			verbose_name=_('Parameter'), help_text=_('Parameter'))
	operator = models.CharField(max_length=10, choices=Choices.OP, 
			verbose_name=_('Operator'), help_text=_('Operator'))
	value = models.CharField(max_length=20, 
			verbose_name=_('Value'), help_text=_('Value'))
	def __unicode__(self):
		return str(self.menu) + '-' + str(self.name)
	class Meta:
		db_table = 'CORE_MENU_PARAM'
		verbose_name = 'Menu Param'
		verbose_name_plural = "Menu Params"

class View(BaseModel):
	"""View"""
	application = models.ForeignKey('core.Application',
			verbose_name=_('Application'), help_text=_('Application for the view'))
	name = models.CharField(max_length=30, 
			verbose_name=_('View Name'), help_text=_('View Name'))
	implementation = models.CharField(max_length=100,
			verbose_name=_('Implementation'), help_text=_('Business class and method that will show view'))
	templates = models.ManyToManyField('core.XpTemplate', through='core.ViewTmpl', related_name='view_templates',
			verbose_name=_('Templates'), help_text=_('Templates for view'))
	params = models.ManyToManyField('core.Param', through='core.ViewParamValue', related_name='view_params', null=True, blank=True,
			verbose_name=_('Parameters'), help_text=_('View entry parameters'))
	winType = models.CharField(max_length=20, choices=Choices.WIN_TYPES, default=Choices.WIN_TYPE_WINDOW,
			verbose_name=_('Window Types'), help_text=_('Window type: Window, Popup'))
	hasUrl = models.BooleanField(default=False,
			verbose_name = _('Url enabled'), help_text = _('View can be called using an url'))
	hasAuth = models.BooleanField(default=True,
			verbose_name = _('Requires Auth?'), help_text = _('View requires that user is logged in'))
	def __unicode__(self):
		return str(self.name)
	class Meta:
		db_table = 'CORE_VIEW'
		verbose_name = 'View'
		verbose_name_plural = "Views"
		unique_together = ("application", "name")

class ViewTmpl(BaseModel):
	"""View Template"""
	view = models.ForeignKey('core.View',
			verbose_name=_('View'), help_text=_('View'))
	template = models.ForeignKey('core.XpTemplate',
			verbose_name=_('Template'), help_text=_('Template'))
	def __unicode__(self):
		return str(self.view) + '-' + str(self.template)
	class Meta:
		db_table = 'CORE_VIEW_TMPL'
		verbose_name = 'View Template'
		verbose_name_plural = "View Templates"

class XpTemplate(BaseModel):
	"""Template"""
	application = models.ForeignKey('core.Application',
			verbose_name=_('Application'), help_text=_('Application for the template'))
	name = models.CharField(max_length=50,
			verbose_name=_('Name'), help_text=_('Name'))
	alias = models.CharField(max_length=20,
			verbose_name=_('Alias'), help_text=_('Alias'))
	language = models.CharField(max_length=2, choices=Choices.LANG, default=Choices.LANG_ENGLISH, 
			verbose_name=_('Language'), help_text=_('Language'))
	country = models.CharField(max_length=2, choices=Choices.COUNTRY, blank=True, null=True,
			verbose_name=_('Country'), help_text=_('Country'))
	winType = models.CharField(max_length=20, choices=Choices.WIN_TYPES, default=Choices.WIN_TYPE_WINDOW,
			verbose_name=_('Window Types'), help_text=_('Window type: Window, Popup'))
	device = models.CharField(max_length=10, choices=Choices.DEVICES, default=Choices.DEVICE_PC,
			verbose_name=_('Device'), help_text=_('Device: Personal Computer, Tablet, Phone'))
	def __unicode__(self):
		return str(self.name)
	class Meta:
		db_table = 'CORE_TEMPLATE'
		verbose_name = 'Template'
		verbose_name_plural = "Templates"
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

class Workflow(BaseModel):
	"""WorkFlow"""
	application = models.ForeignKey('core.Application',
			verbose_name = _('Application'), help_text = _('Application'))
	code = models.CharField(max_length=15, db_index=True, unique=True, 
			verbose_name=_('Flow Code'), help_text=_('Flow Code. First window in a flow identified by a flow code will reset wf variables'))
	resetStart = models.BooleanField(default=False,
			verbose_name = _('Reset Start'), help_text = _('Reset on start: The flow will be deleted when user displays first view of flow'))
	deleteOnEnd = models.BooleanField(default=False,
			verbose_name = _('Delete on End'), help_text = _('Delete On End: Weather flow user data is deleted when user displays last view in flow'))
	jumpToView = models.BooleanField(default=True,
			verbose_name = _('Jump to View'), help_text = _('Jump to View: In case user wants to display view and flow is in another view, the flow view will be shown'))
	def __unicode__(self):
		return str(self.code)
	class Meta:
		db_table = 'CORE_WF'
		verbose_name = 'Workflow'
		verbose_name_plural = "Workflow"

class WorkflowView(BaseModel):
	"""WorkFlow View"""
	flow = models.ForeignKey('core.WorkFlow', related_name='flowView', 
			verbose_name=_('Flow'), help_text=_('Work Flow'))
	viewSource = models.ForeignKey('core.View', related_name='flowViewSource',
			verbose_name=_('Source View'), help_text=_('View which starts flow'))
	viewTarget = models.ForeignKey('core.View', related_name='flowViewTarget', 
			verbose_name=_('target View'), help_text=_('View destiny for flow'))
	action = models.ForeignKey('core.Action', related_name='wf_action', unique=True, 
			verbose_name=_('Action'), help_text=_('Action to process in the workflow navigation'))
	params = models.ManyToManyField('core.Param', through='core.WFParamValue', related_name='flowView_params', null=True, blank=True,
			verbose_name=_('Navigation Parameters'), help_text=_('Parameters neccesary to evaluate to complete navigation'))
	order = models.IntegerField(default=10,
			verbose_name=_('Order'), help_text=_('Order'))
	def __unicode__(self):
		return str(self.flow) +  ' - ' + str(self.viewSource) + ' - ' + str(self.viewTarget) + ' - op - ' + str(self.action)
	class Meta:
		db_table = 'CORE_WF_VIEW'
		verbose_name = 'Workflow View'
		verbose_name_plural = "Workflow View"
		unique_together = ('flow', 'viewSource', 'action', 'viewTarget')

class WFViewEntryParam(BaseModel):
	"""Relates flows with view entry parameters."""
	flowView = models.ForeignKey('core.WorkFlowView', related_name='flowViewEntryParam', 
			verbose_name=_('Flow View'), help_text=_('Work Flow Views'))
	viewParam= models.ForeignKey('core.ViewParamValue', related_name='',
			verbose_name=_('View Param'), help_text=_('View parameter value'))
	def __unicode__(self):
		return str(self.flow) + ' - ' + str(self.viewParam)
	class Meta:
		db_table = 'CORE_WF_VIEW_PARAM'
		verbose_name = 'Workflow View Entry Param'
		verbose_name_plural = "Workflow View Entry Params"

class WorkflowData(BaseModel):
	"""Workflow Data"""
	userId = models.CharField(max_length=40,
			verbose_name = _('Workflow User Id'), help_text = _('User Id saved as a cookie for workflow'))
	flow = models.ForeignKey('core.WorkFlow', related_name='flowData', 
			verbose_name=_('Flow'), help_text=_('Work Flow'))
	view = models.ForeignKey('core.View', related_name='viewFlowData',
			verbose_name=_('View'), help_text=_('View in flow. View where users is in flow'))
	data = models.TextField(default = _jsf.encode64Dict(getBlankWfData({})),
			verbose_name=_('Data'), help_text=_('Worflow data'))
	def __unicode__(self):
		return str(self.userId) + ' - ' + str(self.flow)
	class Meta:
		db_table = 'CORE_WF_DATA'
		verbose_name = 'Workflow Data'
		verbose_name_plural = "Workflow Data"
		unique_together = ('userId', 'flow')

class Param(BaseModel):
	"""Parameters for WF and Views"""
	application = models.ForeignKey('core.Application', 
				verbose_name = _('Application'), help_text = _('Application'))
	name = models.CharField(max_length=15, 
				verbose_name=_('Name'), help_text=_('Name'))
	title = models.CharField(max_length=30, 
				verbose_name=_('Title'), help_text=_('Title text for the parameter'))
	paramType = models.CharField(max_length=10, choices=Choices.BASIC_TYPES,
				verbose_name=_('Type'), help_text=_('Type'))
	view = models.BooleanField(default=False,
				verbose_name=_('View'), help_text=_('Parameter for View?'))
	workflow = models.BooleanField(default=False,
				verbose_name=_('Workflow'), help_text=_('Parameter for workflow?'))
	def __unicode__(self):
		return str(self.title)
	class Meta:
		db_table = 'CORE_PARAM'
		verbose_name = 'Parameter'
		verbose_name_plural = "Parameters for views and workflow"
		unique_together = ('application','name')


class ViewParamValue(BaseModel):
	"""Parameter Values for WF"""
	view = models.ForeignKey('core.View', related_name='viewParam',
			verbose_name=_('View'), help_text=_('View for entry parameters'))
	name = models.ForeignKey('core.Param', 
			verbose_name=_('Parameter'), help_text=_('Parameter'))
	operator = models.CharField(max_length=10, choices=Choices.OP, 
			verbose_name=_('Operator'), help_text=_('Operator'))
	value = models.CharField(max_length=20, 
			verbose_name=_('Value'), help_text=_('Value'))
	def __unicode__(self):
		return str(self.name) + ' ' + str(self.operator) + ' ' + str(self.value)
	class Meta:
		db_table = 'CORE_VIEW_PARAM_VALUE'
		verbose_name = 'View Parameter Value'
		verbose_name_plural = "View Parameter Values"

class WFParamValue(BaseModel):
	"""Parameter Values for WF"""
	flowView = models.ForeignKey('core.WorkFlowView', related_name='flowViewParamValue', 
			verbose_name=_('Flow View'), help_text=_('Work Flow Views'))
	name = models.ForeignKey('core.Param', 
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
		if request.REQUEST.has_key('userChannel') and request.user.is_authenticated():
			ctx.userChannel = request.REQUEST['userChannel']			
		ArgsDict['ctx'] = ctx
		resp = f(*ArgsTuple, **ArgsDict)
		return resp
	return new_f

class ContextDecorator(object):
	_app = ''
	APP = 'app'
	USER = 'user'
	LANG = 'lang'
	SETTINGS = 'settings'
	SESSION = 'session'
	COOKIES = 'cookies'
	META = 'meta'
	POST = 'post'
	REQUEST = 'request'
	GET = 'get'
	USER_CHANNEL = 'userChannel'
	AUTH = 'auth'
	FORM = 'form'
	FORMS = 'forms'
	CAPTCHA = 'captcha'
	RAW_REQUEST = 'raw_request'
	CTX = 'ctx'
	JS_DATA = 'jsData'
	VIEW_NAME_SOURCE = 'viewNameSource'
	VIEW_NAME_TARGET = 'viewNameTarget'
	ACTION = 'action'
	FLOW_CODE = 'flowCode'
	FLOW_DATA = 'flowData'
	IS_FLOW = 'isFlow'
	SET_COOKIES = 'set_cookies'
	DEVICE = 'device'
	COUNTRY = 'country'
	WIN_TYPE = 'winType'
	TMPL = 'tmpl'
	WF_USER_ID = 'wfUserId'
	IS_LOGIN = 'isLogin'
	def __init__(self, **args):
		"""if args.has_key('app'):
			self._app = args['app']"""
		pass
	def __call__(self, f):
		"""Decorator call method"""
		def wrapped_f(*argsTuple, **argsDict):
			try:
				request = argsTuple[0]
				REQ = request.REQUEST
				self._app = request.REQUEST['app'] if request.REQUEST.has_key('app') else ''
				langs = ('en')
				lang = translation.get_language()
				print 'lang django: ', lang
				if lang not in langs:
					lang = 'en'
				ctx = {}
				ctx[self.APP] = self._app
				ctx['user'] = request.user
				ctx[self.LANG] = lang
				ctx['settings'] = settings
				ctx['session'] = request.session
				ctx['cookies'] = request.COOKIES
				ctx['meta'] = request.META
				ctx['post'] = request.POST
				ctx['request'] = REQ
				#ctx['raw_request'] = request
				ctx['get'] = request.GET
				ctx[self.DEVICE] = Choices.DEVICE_PC
				ctx[self.COUNTRY] = ''
				ctx[self.WIN_TYPE] = Choices.WIN_TYPE_WINDOW
				ctx[self.TMPL] = ''
				#ctx['socialChannel'] = ''
				ctx[self.USER_CHANNEL] = None
				ctx['auth'] = {}
				ctx['form'] = None
				ctx['forms'] = {}
				ctx['captcha'] = None 
				ctx[self.VIEW_NAME_SOURCE] = REQ[self.VIEW_NAME_SOURCE] if REQ.has_key(self.VIEW_NAME_SOURCE) else ''
				ctx[self.VIEW_NAME_TARGET] = REQ[self.VIEW_NAME_TARGET] if REQ.has_key(self.VIEW_NAME_TARGET) else ''
				ctx[self.ACTION] = REQ[self.ACTION] if REQ.has_key(self.ACTION) else ''
				ctx[self.FLOW_CODE] = ''
				ctx[self.FLOW_DATA] = ''
				ctx[self.IS_FLOW] = False
				ctx[self.JS_DATA] = ''
				ctx[self.WF_USER_ID] = ''
				#if request.REQUEST.has_key('socialChannel') and request.user.is_authenticated():
				if request.session.has_key('userChannel') and request.user.is_authenticated():
					# TODO: Get this from session
					ctx[self.USER_CHANNEL] = request.session['userChannel']
					print 'Context :: userChannel: ', ctx[self.USER_CHANNEL]
				if request.user.is_authenticated():
					ctx[self.IS_LOGIN] = True
				else:
					ctx[self.IS_LOGIN] = False
				# Set cookies
				ctx[self.SET_COOKIES] = []
				argsDict['ctx'] = ctx
				resp = f(*argsTuple, **argsDict)
				return resp
			except Exception as e: #@UnusedVariable
				print 'Context :: Exception...'
				if settings.DEBUG == True:
					traceback.print_exc()
					#print e.myException
				raise
		return wrapped_f


class ContextViewDecorator(object):
	_app = ''
	APP = 'app'
	USER = 'user'
	LANG = 'lang'
	SETTINGS = 'settings'
	SESSION = 'session'
	COOKIES = 'cookies'
	META = 'meta'
	POST = 'post'
	REQUEST = 'request'
	GET = 'get'
	USER_CHANNEL = 'userChannel'
	AUTH = 'auth'
	FORM = 'form'
	FORMS = 'forms'
	CAPTCHA = 'captcha'
	RAW_REQUEST = 'raw_request'
	CTX = 'ctx'
	JS_DATA = 'jsData'
	VIEW_NAME_SOURCE = 'viewNameSource'
	VIEW_NAME_TARGET = 'viewNameTarget'
	ACTION = 'action'
	FLOW_CODE = 'flowCode'
	FLOW_DATA = 'flowData'
	IS_FLOW = 'isFlow'
	SET_COOKIES = 'set_cookies'
	DEVICE = 'device'
	COUNTRY = 'country'
	WIN_TYPE = 'winType'
	TMPL = 'tmpl'
	WF_USER_ID = 'wfUserId'
	IS_LOGIN = 'isLogin'
	def __init__(self, **args):
		"""if args.has_key('app'):
			self._app = args['app']"""
		pass
	def __call__(self, f):
		"""Decorator call method"""
		def wrapped_f(request, **args):
			try:
				print 'ContextNew :: args: ', args
				if args.has_key('app') and len(args['app']) != 0:
					self._app = args['app']
					self.__viewName = args['viewName'] if args.has_key('viewName') else ''
				else:
					self._app = 'site'
					self.__viewName = 'home'
				REQ = request.REQUEST 
				langs = ('en')
				lang = translation.get_language()
				print 'lang django: ', lang
				if lang not in langs:
					lang = 'en'
				ctx = {}
				ctx[self.APP] = self._app
				ctx['user'] = request.user
				ctx[self.LANG] = lang
				ctx['settings'] = settings
				ctx['session'] = request.session
				ctx['cookies'] = request.COOKIES
				ctx['meta'] = request.META
				ctx['post'] = request.POST
				ctx['request'] = REQ
				#ctx['raw_request'] = request
				ctx['get'] = request.GET
				ctx[self.DEVICE] = Choices.DEVICE_PC
				ctx[self.COUNTRY] = ''
				ctx[self.WIN_TYPE] = Choices.WIN_TYPE_WINDOW
				ctx[self.TMPL] = ''
				#ctx['socialChannel'] = ''
				ctx[self.USER_CHANNEL] = None
				ctx['auth'] = {}
				ctx['form'] = None
				ctx['forms'] = {}
				ctx['captcha'] = None 
				ctx[self.VIEW_NAME_SOURCE] = REQ[self.VIEW_NAME_SOURCE] if REQ.has_key(self.VIEW_NAME_SOURCE) else ''
				ctx[self.VIEW_NAME_TARGET] = REQ[self.VIEW_NAME_TARGET] if REQ.has_key(self.VIEW_NAME_TARGET) else ''
				ctx[self.ACTION] = REQ[self.ACTION] if REQ.has_key(self.ACTION) else ''
				ctx[self.FLOW_CODE] = ''
				ctx[self.FLOW_DATA] = ''
				ctx[self.IS_FLOW] = False
				ctx[self.JS_DATA] = ''
				ctx[self.WF_USER_ID] = ''
				#if request.REQUEST.has_key('socialChannel') and request.user.is_authenticated():
				if request.session.has_key('userChannel') and request.user.is_authenticated():
					# TODO: Get this from session
					ctx[self.USER_CHANNEL] = request.session['userChannel']
					print 'Context :: userChannel: ', ctx[self.USER_CHANNEL]
				if request.user.is_authenticated():
					ctx[self.IS_LOGIN] = True
				else:
					ctx[self.IS_LOGIN] = False
				# Set cookies
				ctx[self.SET_COOKIES] = []
				args['ctx'] = ctx
				resp = f(request, **args)
				return resp
			except Exception as e: #@UnusedVariable
				print 'Context :: Exception...'
				if settings.DEBUG == True:
					traceback.print_exc()
					#print e.myException
				raise
		return wrapped_f

class XpTemplateDeprec(object):
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
		d = {'user': self._user, 'lang': self._lang, 'session': self._session, 'cookies': self._cookies, 'META': self._META, 'context': self._context}
		return str(d)
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
