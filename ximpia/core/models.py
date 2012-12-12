import types
import traceback
import json
import os

from django.db import models
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User, Group
from django.utils.translation import ugettext as _
from django.utils import translation

from choices import Choices
import constants as K

from ximpia.util.js import Form as _jsf

# Settings
from ximpia.core.util import getClass
settings = getClass(os.getenv("DJANGO_SETTINGS_MODULE"))

# Logging
import logging.config
logging.config.dictConfig(settings.LOGGING)
logger = logging.getLogger(__name__)

def getBlankWfData( dd ):
	"""Get workflow data inside flowCode by default"""
	dd['data'] = {}
	dd['viewName'] = ''
	return dd

class DeleteManager( models.Manager ):
	def get_query_set(self):
		return super(DeleteManager, self).get_query_set().filter(isDeleted=False)

class BaseModel( models.Model ):
	"""
	
	Abstract Base Model with fields for all other models. Ximpia models have this model as parent. This model provides audit
	informatioon like date creating and updating, as well as user involved in the update or creation.
	
	When you delete rows in Ximpia, ``isDeleted``field is set to True. You can force to physical delete by passing ``real=True`` to 
	data delete methods (db.delete, db.deleteById and db.deleteIfExists).
	
	When deleting rows with the django admin interface, you cannot delete database records physically, therefore those rows will have
	isDeleted=True and will not show in the admin pages. You can delete for ever with your application code or directly connecting to
	your database.
	
	**Attributes**
	
	* ``id`` : Primary key
	* ``dateCreate``:DateTimeField
	* ``dateModify``:DateTimeField
	* ``userCreateId``:IntegerField
	* ``userModifyId``:IntegerField
	* ``isDeleted``:BooleanField
	
	**Relatinships**
	
	"""
	dateCreate = models.DateTimeField(auto_now_add=True, null=True, blank=True, editable=False, db_column='DATE_CREATE', 
					verbose_name= _('Create Date'), help_text= _('Create Date'))
	dateModify = models.DateTimeField(auto_now=True, null=True, blank=True, editable=False, db_column='DATE_MODIFY',
					verbose_name= _('Modify Date'), help_text= _('Modify Date'))
	userCreateId = models.IntegerField(null=True, blank=True, editable=False, db_column='USER_CREATE_ID',
					verbose_name=_('User Create Id'), help_text=_('User that data'))
	userModifyId = models.IntegerField(null=True, blank=True, editable=False, db_column='USER_MODIFY_ID',
					verbose_name=_('User Modify Id'), help_text=_('User that madofied data'))
	isDeleted = models.BooleanField(default=False, editable=False, db_column='IS_DELETED',
				verbose_name=_('Delete'), help_text=_('Field that sets logical deletes'))
	objects = DeleteManager()
	objects_del = models.Manager()
	class Meta:
		abstract = True

class Param( BaseModel ):
	"""
	
	Parameters for WF and Views
	
	**Attributes**
	
	* ``id``:AutoField : Primary Key
	* ``name``:CharField(15)
	* ``title``:CharField(30)
	* ``paramType``:CharField(10) : As Choices.BASIC_TYPES
	* ``isView``:BooleanField
	* ``isWorkflow``:BooleanField
	
	**Relationships**
	
	* ``application`` -> Application
	
	"""
	id = models.AutoField(primary_key=True, db_column='ID_CORE_PARAM')
	application = models.ForeignKey('core.Application', db_column='ID_APPLICATION', 
				verbose_name = _('Application'), help_text = _('Application'))
	name = models.CharField(max_length=15, db_column='NAME',
				verbose_name=_('Name'), help_text=_('Name'))
	title = models.CharField(max_length=30, db_column='TITLE',
				verbose_name=_('Title'), help_text=_('Title text for the parameter'))
	paramType = models.CharField(max_length=10, choices=Choices.BASIC_TYPES, db_column='PARAM_TYPE',
				verbose_name=_('Type'), help_text=_('Type'))
	isView = models.BooleanField(default=False, db_column='IS_VIEW',
				verbose_name=_('View'), help_text=_('Parameter for View?'))
	isWorkflow = models.BooleanField(default=False, db_column='IS_WORKFLOW',
				verbose_name=_('Workflow'), help_text=_('Parameter for workflow?'))
	def __unicode__(self):
		return self.title
	class Meta:
		db_table = 'CORE_PARAM'
		verbose_name = 'Parameter'
		verbose_name_plural = "Parameters for views and workflow"
		unique_together = ('application','name')


class CoreParam( BaseModel ):
	"""
	
	Parameters
	
	You would place tables (key->value) in choices module inside your application for tables that will not change often. When you
	have data that will change frequently, you can user this model to record parameters, lookup tables (like choices) and any other
	parametric information you may require.
	
	You can do:
	
	MY_FIRST_PARAM = 67 by inserting name='MY_FIRST_PARAM', value='67', paramType='integer'
	
	Country
	||name||value||
	||es||spain||
	||us||United States||
	
	by...
	mode='COUNTRY', name='es', value='Spain', paramType='string'
	mode='COUNTRY', name='us', value='United States', paramType='string'
	
	**Attributes**
	
	* ``id`` : Primary key
	* ``mode``:CharField(20) : Parameter mode. This field allows you to group parameter to build lookup tables like the ones found
	in combo boxes (select boxes) with name->value pairs.
	* ``name``:CharField(20) : Parameter name
	* ``value``:CharField(100) : Parameter value
	* ``paramType``:CharField(10) : Parameter type, as Choices.PARAM_TYPE . Choices are string, integer, date.
	
	**Relationships**
	
	"""
	id = models.AutoField(primary_key=True, db_column='ID_CORE_PARAMETER')
	mode = models.CharField(max_length=20, db_column='MODE', null=True, blank=True,
			verbose_name=_('Mode'), help_text=_('Parameter Mode'))
	name = models.CharField(max_length=20, db_column='NAME',
			verbose_name=_('Name'), help_text=_('Parameter Name'))
	value = models.CharField(max_length=100, null=True, blank=True, db_column='VALUE',
			verbose_name=_('Value'), help_text=_('Parameter Value'))
	paramType = models.CharField(max_length=10, choices=Choices.PARAM_TYPE, default=Choices.PARAM_TYPE_STRING, 
			db_column='PARAM_TYPE',
			verbose_name=_('Parameter Type'), help_text=_('Type: either parameter or table'))
	def __unicode__(self):
		return '%s - %s' % (self.mode, self.name)
	class Meta:
		db_table = 'CORE_PARAMETER'
		verbose_name = "Parameter"
		verbose_name_plural = "Parameters"

class MetaKey( BaseModel ):

	"""
	
	Model to store the keys allowed for meta values
	
	**Attributes**
	
	* ``id``:AutoField : Primary key
	* ``name``:CharField(20) : Key META name
	
	**Relationships**
	
	* ``keyType`` -> CoreParam : Foreign key to CoreParam having mode='META_TYPE'
	
	"""
	
	id = models.AutoField(primary_key=True, db_column='ID_CORE_META_KEY')
	name = models.CharField(max_length=20,
	        verbose_name = _('Key Name'), help_text = _('Meta Key Name'), db_column='NAME')
	keyType = models.ForeignKey(CoreParam, limit_choices_to={'mode': K.PARAM_META_TYPE}, db_column='ID_META_TYPE',
			verbose_name=_('Key META Type'), help_text=_('Key META Type') )
	def __unicode__(self):
		return self.name
	class Meta:
		db_table = 'CORE_META_KEY'
		ordering = ['name']
		verbose_name = _('Meta Key')
		verbose_name_plural = _('Meta Keys')

class CoreXmlMessage( BaseModel ):
	"""XML Message"""
	#TODO: INCLUDE MESSAGE TYPE: EMAIL, ETC...
	id = models.AutoField(primary_key=True, db_column='ID_CORE_XML_MESSAGE')
	name = models.CharField(max_length=255, db_column='NAME',
			verbose_name = _('Name'), help_text = _('Code name of XML'))
	lang = models.CharField(max_length=2, choices=Choices.LANG, default=Choices.LANG_ENGLISH, db_column='LANG',
			verbose_name = _('Language'), help_text = _('Language for xml'))
	body = models.TextField(db_column='BODY', verbose_name = _('Xml Content'), help_text = _('Xml content'))
	def __unicode__(self):
		return self.name
	class Meta:
		db_table = 'CORE_XML_MESSAGE'
		verbose_name = _('Xml Message')
		verbose_name_plural = _('Xml Messages')

class Application( BaseModel ):
	
	"""
	
	Applications. For most sites, they will have single application for N services which relate to use cases for views and actions.
	In case your application is big or have admin backdoors, your site with have more than one application.
	
	This table holds applications at your site. slug corresponds to the host name that related to the application, like 'slug.domain.com'.
	You can also access applications by /apps/slug in case application hosts is disabled.
	
	Applications can be grouped together using the ``parent`` field.
	
	Applications can have subscription business model or be free. In case subscription required, ``isSubscription`` would be ``True``
	
	Applications can be private and accessible only to a group of users. ``isPrivate`` would be ``True`` in this case. Applications can
	start private (like a private beta) and then make them public. When making public applications, you can publish at Ximpia 
	directory.
	
	Applications have meta information through model ApplicationMeta. You can attach meta values for application in this model.
	
	**Attributes**
	
	* ``id`` : Primary key
	* ``name``:CharField(15)
	* ``slug``:SlugField(30)
	* ``title``:CharField(30)
	* ``isSubscription``:BooleanField
	* ``isPrivate``:BooleanField
	* ``isAdmin``:BooleanField
	
	**Relationships**
	
	* ``developer`` -> User
	* ``developerOrg`` -> Group
	* ``parent`` -> self
	* ``users`` <-> UserChannel through ApplicationAccess and related name 'app_access'
	* ``meta`` <-> Meta through ApplicationMeta and related name 'app_meta'
	
	"""
	
	id = models.AutoField(primary_key=True, db_column='ID_CORE_APPLICATION')
	name = models.CharField(max_length=100,
		verbose_name = _('Name'), help_text = _('Application name. It must contain package and module for application with . as \
			separator, like ximpia.site'))
	slug = models.SlugField(max_length=30,
		verbose_name = _('Slug'), help_text = _('Slug'), db_column='SLUG')
	title = models.CharField(max_length=30, db_column='TITLE',
		verbose_name = _('Title'), help_text = _('Application title'))
	developer = models.ForeignKey(User, null=True, blank=True, db_column='ID_DEVELOPER',
		verbose_name = _('Developer'), help_text = _('Developer'))
	developerOrg = models.ForeignKey(Group, null=True, blank=True, db_column='ID_DEVELOPER_ORG',
		verbose_name = _('Organization'), help_text = _('Developer organization'))
	parent = models.ForeignKey('self', null=True, blank=True, db_column='ID_PARENT',
		verbose_name = 'Parent Application', help_text = 'Used for application groups. Application which this app is related to')
	isSubscription = models.BooleanField(default=False, db_column='IS_SUBSCRIPTION',
		verbose_name = _('Subscription'), help_text = _('Is this application subscription based?'))
	isPrivate = models.BooleanField(default=False, db_column='IS_PRIVATE',
		verbose_name = _('Private'), help_text = _('Is this application private to a list of groups?'))
	users = models.ManyToManyField('site.UserChannel', through='core.ApplicationAccess', related_name='app_access', null=True, blank=True,
			verbose_name=_('Users'), help_text=_('Users that have access to the application'))
	isAdmin = models.BooleanField(default=False, db_column='IS_ADMIN',
		verbose_name = _('Is Admin?'), help_text = _('Is this application an admin backdoor?'))
	meta = models.ManyToManyField(MetaKey, through='core.ApplicationMeta', related_name='app_meta',
			verbose_name=_('META Keys'), help_text=_('META Keys for application') )
	def __unicode__(self):
		return self.title
	class Meta:
		db_table = 'CORE_APPLICATION'
		verbose_name = _('Application')
		verbose_name_plural = _('Applications')

class ApplicationMeta( BaseModel ):
	"""
	
	Meta information for application.
	
	**Attributes**
	
	* ``id`` : Primary key
	* ``value``:TextField : META Key value for application
	
	**Relationships**
	
	* ``application`` -> Application
	* ``meta`` -> MetaKey
	
	"""
	id = models.AutoField(primary_key=True, db_column='ID_CORE_APPLICATION_META')
	application = models.ForeignKey(Application, db_column='ID_APPLICATION',
				verbose_name = _('Application'), help_text = _('Application'))
	meta = models.ForeignKey(MetaKey, limit_choices_to={'keyType__value': K.PARAM_META}, db_column='ID_META',
				verbose_name=_('Meta Key'), help_text=_('Meta Key') )
	value = models.TextField(db_column='VALUE', verbose_name = _('Value'), help_text = _('Value'))
	def __unicode__(self):
		return '%s' % (self.meta.name)
	class Meta:
		db_table = 'CORE_APPLICATION_META'
		verbose_name = 'Application META'
		verbose_name_plural = "Application META"

class ApplicationAccess( BaseModel ):
	"""
	
	User that have access to application. Used for subscription and private applications.
	
	**Attributes**
	
	* ``id``:AutoField : Primary key
	
	**Relationships**
	
	* ``application`` -> Application
	* ``userChannel`` -> UserChannel
	
	"""
	
	id = models.AutoField(primary_key=True, db_column='ID_CORE_APP_ACCESS')
	application = models.ForeignKey('core.Application', db_column='ID_APPLICATION',
				verbose_name = _('Application'), help_text = _('Application'))
	userChannel = models.ForeignKey('site.UserChannel', db_column='ID_USER_CHANNEL',
				verbose_name = _('User'), help_text = _('User channel needed to access application'))
	def __unicode__(self):
		return '%s' % (self.userChannel.user.username)
	class Meta:
		db_table = 'CORE_APPLICATION_ACCESS'
		verbose_name = 'Application Access'
		verbose_name_plural = "Application Access"

class SearchIndex( BaseModel ):
	"""
	
	Search index. This table maps words indexed in views and actions to result literals (string to show in search tooltip). We map
	entry parameters to view as well.
	
	Search results can come from views and actions. Words in the title are indexed in ``Word`` model. When user clicks on search result,
	we know what to do from this table. If search result applies to a view, we launch view. In case related to an action, we launch
	the action.
	
	**Attributes**
	
	* ``id``:AutoField : Primary Key
	* ``title``:CharField(70)
	
	**Relationships**
	
	* ``application`` -> Application
	* ``view`` -> View
	* ``action`` -> Action
	* ``words`` <-> Word through SearchIndexWord with related name 'index_words'
	* ``params`` <-> Param through SearchIndexParam with related name 'index_params'
	
	"""
	id = models.AutoField(primary_key=True, db_column='ID_CORE_SEARCH_INDEX')
	application = models.ForeignKey('core.Application', db_column='ID_APPLICATION',
			verbose_name=_('Application'), help_text=_('Application for seraching'))
	view = models.ForeignKey('core.View', null=True, blank=True, related_name='index_view', db_column='ID_VIEW',
			verbose_name=_('View'), help_text=_('View'))
	action = models.ForeignKey('core.Action', null=True, blank=True, related_name='index_action', db_column='ID_ACTION',
			verbose_name=_('Action'), help_text=_('Action'))
	title = models.CharField(max_length=70, db_column='TITLE',
			verbose_name=_('Title'), help_text=_('Title'))
	words = models.ManyToManyField('core.Word', through='core.SearchIndexWord', related_name='index_words', 
			verbose_name=_('Index Parameters'), help_text=_('Parameters used in the search of content for views and actions'))
	params = models.ManyToManyField('core.Param', through='core.SearchIndexParam', related_name='index_params', null=True, blank=True,
			verbose_name=_('Index Parameters'), help_text=_('Parameters used in the search of content for views and actions'))
	def __unicode__(self):
		return self.title
	class Meta:
		db_table = 'CORE_SEARCH_INDEX'
		verbose_name = 'Index'
		verbose_name_plural = "Index"
		unique_together = ("view", "action")

class Word( BaseModel ):
	"""
	
	Word
	
	**Attributes**
	
	* ``id``:AutoField : Primary Key
	* ``word``:CharField(20) : Word to index
	
	**Relationships**
	
	"""
	id = models.AutoField(primary_key=True, db_column='ID_CORE_WORD')
	word = models.CharField(max_length=20, db_index=True, db_column='WORD', 
			verbose_name=_('Word'), help_text=_('Word'))
	def __unicode__(self):
		return self.word
	class Meta:
		db_table = 'CORE_WORD'
		verbose_name = 'Word'
		verbose_name_plural = "Words"

class SearchIndexWord( BaseModel ):
	"""
	
	Index
	
	**Attributes**
	
	* ``id``:AutoField : Primary Key
	
	**Relationships**
	
	* ``index`` -> SearchIndex
	* ``word`` -> Word
	
	"""
	id = models.AutoField(primary_key=True, db_column='ID_CORE_SEARCH_INDEX_WORD')
	index = models.ForeignKey(SearchIndex, db_column='ID_INDEX',
			verbose_name=_('Index'), help_text=_('Index having application, view, action, title and parameters'))
	word = models.ForeignKey(Word, db_column='ID_WORD',
			verbose_name=_('Word'), help_text=_('Word'))
	def __unicode__(self):
		return '%s - %s' % (self.index, self.word)
	class Meta:
		db_table = 'CORE_SEARCH_INDEX_WORD'
		verbose_name = 'Index Word'
		verbose_name_plural = "Index Words"


class SearchIndexParam( BaseModel ):
	"""
	
	Index Parameters
	
	**Attributes**
	
	* ``id``:AutoField : Primary Key
	* ``operator``:CharField(10) : Operator for parameter, as Choices.OP : equal, less than, greater than , not equal to
	* ``value``:CharField(20)
	
	**Relationships**
	
	* ``searchIndex`` -> SearchIndex
	* ``name`` -> Param . Params for workflow, views, actions and search are registered in Param table.
	
	"""
	id = models.AutoField(primary_key=True, db_column='ID_CORE_INDEX_PARAM')
	searchIndex = models.ForeignKey(SearchIndex, db_column='ID_SEARCH_INDEX',
			verbose_name=_('Search Index'), help_text=_('Search Index'))
	name = models.ForeignKey(Param, db_column='ID_NAME', 
			verbose_name=_('Parameter'), help_text=_('Parameter'))
	operator = models.CharField(max_length=10, choices=Choices.OP, db_column='OPERATOR', 
			verbose_name=_('Operator'), help_text=_('Operator'))
	value = models.CharField(max_length=20, db_column='VALUE',
			verbose_name=_('Value'), help_text=_('Value'))
	def __unicode__(self):
		return '%s - %s' % (self.name, self.value)
	class Meta:
		db_table = 'CORE_INDEX_PARAM'
		verbose_name = 'Index Parameters'
		verbose_name_plural = "Index Parameters"

class View( BaseModel ):
	"""
	
	View. Pages in ximpia are called views. Views render content obtaine from database or other APIs. They hit the slave databases. In
	case writing content is needed, could be accomplished by calling queues. Views can show lists, record detalils in forms, reports,
	static content, etc... 
	
	In case no logic is needed by view, simply include ``pass`` in the service operation.
	
	Views have name to be used internally in component registering and code and slug which is the name used in urls.
	
	View implementation is the path to the service operation that will produce view JSON data to server the frontend. Implementation
	is built by registering a view component.
	
	Window types can be 'window', 'popup' and 'panel' (this one coming soon). Windows render full width, popups are modal windows, and
	panels are tooltip areas inside your content. Popups can be triggered using icons, buttons or any other action. Panels will be
	triggered by mouse over components, clicking on visual action components.
	
	In case view needs authentication to render, would have hasAuth = True.
	
	Views can be grouped together using the ``parent`` field.
	
	Params are entry parameters (dynamic or static) that view will accept. Parameters are inyected to service operations with **args 
	variable. The parameter name you include will be called by args['MY_PARAM'] in case your parameter name is 'MY_PARAM'.
	
	**Attributes**
	
	* ``id``:AutoField : Primary Key
	* ``name``:CharField(30)
	* ``implementation``:CharField(100)
	* ``winType``:CharField(20) : Window type, as Choices.WIN_TYPE_WINDOW
	* ``slug``:SlugField(50) : View slug to form url to call view
	* ``hasAuth``:BooleanField : Needs view authentication?
	
	**Relationships**
	
	* ``parent`` -> self
	* ``application`` -> Application
	* ``templates`` <-> XpTemplate through ViewTmpl with related name `view_templates`
	* ``params`` <-> Param through ViewParamValue with related nam 'view_params'
	* ``menus`` <-> Menu through ViewMenu with related name 'view_menus'
	
	"""
	id = models.AutoField(primary_key=True, db_column='ID_CORE_VIEW')
	parent = models.ForeignKey('self', null=True, blank=True, related_name='view_parent', 
		    verbose_name = _('Parent'), help_text = _('Parent'), db_column='ID_PARENT')
	application = models.ForeignKey(Application, db_column='ID_APPLICATION',
			verbose_name=_('Application'), help_text=_('Application for the view'))
	name = models.CharField(max_length=30, db_column='NAME', 
			verbose_name=_('View Name'), help_text=_('View Name'))
	implementation = models.CharField(max_length=100, db_column='IMPLEMENTATION',
			verbose_name=_('Implementation'), help_text=_('Service class and method that will show view'))
	templates = models.ManyToManyField('core.XpTemplate', through='core.ViewTmpl', related_name='view_templates',
			verbose_name=_('Templates'), help_text=_('Templates for view'))
	menus = models.ManyToManyField('core.Menu', through='core.ViewMenu', related_name='view_menus',
			verbose_name=_('Menus'), help_text=_('Menu items related to views'))
	params = models.ManyToManyField('core.Param', through='core.ViewParamValue', related_name='view_params', null=True, blank=True,
			verbose_name=_('Parameters'), help_text=_('View entry parameters'))
	winType = models.CharField(max_length=20, choices=Choices.WIN_TYPES, default=Choices.WIN_TYPE_WINDOW, db_column='WIN_TYPE',
			verbose_name=_('Window Type'), help_text=_('Window type: Window, Popup'))
	slug = models.SlugField(max_length=50,
		verbose_name = _('Slug'), help_text = _('Slug'), db_column='SLUG')
	hasAuth = models.BooleanField(default=True, db_column='HAS_AUTH',
			verbose_name = _('Requires Auth?'), help_text = _('View requires that user is logged in'))
	def __unicode__(self):
		return self.name
	class Meta:
		db_table = 'CORE_VIEW'
		verbose_name = 'View'
		verbose_name_plural = "Views"
		unique_together = ("application", "name")

class Action( BaseModel ):
	"""
	
	Action
	
	Actions are mapped to service operations. Actions can be triggered by clicking on a button, a link, a menu icon or any other
	visual component that triggers actions.
	
	Here we map action names, implementations, slugs and action properties. Implementations are built by component registering.
	
	**Attributes**
	
	* ``id``:AutoField : Primary key
	* ``name``:CharField(30)
	* ``implementation``:CharField(100)
	* ``slug``:SlugField(50)
	* ``hasAuth``:BooleanField
	
	**Relationships**
	
	* ``application`` -> Application
	
	"""
	id = models.AutoField(primary_key=True, db_column='ID_CORE_ACTION')
	application = models.ForeignKey(Application, db_column='ID_APPLICATION',
			verbose_name=_('Application'), help_text=_('Application for the action'))
	name = models.CharField(max_length=30, db_column='NAME',
			verbose_name=_('Action Name'), help_text=_('Action Name'))
	implementation = models.CharField(max_length=100, db_column='IMPLEMENTATION',
			verbose_name=_('Implementation'), help_text=_('Service class and method that will process action'))
	slug = models.SlugField(max_length=50,
		verbose_name = _('Slug'), help_text = _('Slug'), db_column='SLUG')
	hasAuth = models.BooleanField(default=True, db_column='HAS_AUTH',
			verbose_name = _('Requires Auth?'), help_text = _('View requires that user is logged in'))
	def __unicode__(self):
		return self.name
	class Meta:
		db_table = 'CORE_ACTION'
		verbose_name = 'Action'
		verbose_name_plural = "Actions"
		unique_together = ("application", "name")

class Menu( BaseModel ):
	"""
	
	Menu
	
	**Attributes**
	
	* ``id``:AutoField : Primary Key
	* ``name``:CharField(20) : Menu item name
	* ``titleShort``:CharField(15) : Title short. Text shown in icon. Default menu shows this text right to the icon image.
	* ``title``:CharField(30) : Title shown in tooptip when mouse goes over.
	* ``url``:URLField : Url to launch . Used for external urls mapped to menu items.
	* ``urlTarget``:CharField(10) : target to launch url
	* ``language``:CharField(2) : Language code, like ``es``, ``en``, etc...
	* ``country``:CharField(2) : Country as Choices.COUNTRY
	* ``device``:CharField(10) : Device. Smartphones, tablets can have their own menu, customized to screen width
	
	**Relationships**
	
	* ``application`` -> Application
	* ``icon`` -> CoreParam
	* ``view`` -> View
	* ``action`` -> Action
	* ``params`` <-> Param through MenuParam with related name 'menu_params'
	
	"""
	id = models.AutoField(primary_key=True, db_column='ID_CORE_MENU')
	application = models.ForeignKey('core.Application', db_column='ID_APPLICATION',
			verbose_name=_('Application'), help_text=_('Application for the menu'))
	name = models.CharField(max_length=20, unique=True, db_column='NAME',
			verbose_name=_('Menu Name'), help_text=_('Name for menu, used in json menu objects'))
	titleShort = models.CharField(max_length=15, db_column='TITLE_SHORT',
			verbose_name=_('Short Title'), help_text=_('Short title for menu. Used under big icons'))
	title = models.CharField(max_length=30, db_column='TITLE',
			verbose_name=_('Menu Title'), help_text=_('Title for menu item'))
	icon = models.ForeignKey(CoreParam, limit_choices_to={'mode': K.PARAM_ICON}, db_column='ID_ICON',
			verbose_name=_('Icon'), help_text=_('Icon'))
	view = models.ForeignKey(View, null=True, blank=True, related_name='menu_view', db_column='ID_VIEW',
			verbose_name=_('View'), help_text=_('View'))
	action = models.ForeignKey(Action, related_name='menu_action', null=True, blank=True,  db_column='ID_ACTION',
			verbose_name=_('Action'), help_text=_('Action to process when click on menu item'))
	url = models.URLField(null=True, blank=True, db_column='URL',
			verbose_name=_('Url'), help_text=_('Url to trigger for this menu item'))
	urlTarget = models.CharField(max_length=10, null=True, blank=True, db_column='URL_TARGET',
			verbose_name = _('Url Target'), help_text=_('Target to open url: Same window or new window. It will open in a tab in most browsers'))
	language = models.CharField(max_length=2, choices=Choices.LANG, default=Choices.LANG_ENGLISH, db_column='LANGUAGE', 
			verbose_name=_('Language'), help_text=_('Language'))
	country = models.CharField(max_length=2, choices=Choices.COUNTRY, blank=True, null=True, db_column='COUNTRY',
			verbose_name=_('Country'), help_text=_('Country'))
	device = models.CharField(max_length=10, choices=Choices.DEVICES, default=Choices.DEVICE_PC, db_column='DEVICE',
			verbose_name=_('Device'), help_text=_('Device: Personal Computer, Tablet, Phone'))
	params = models.ManyToManyField('core.Param', through='core.MenuParam', related_name='menu_params', null=True, blank=True,
			verbose_name=_('Menu Parameters'), help_text=_('Menu parameters sent to views'))
	def __unicode__(self):
		return self.titleShort
	class Meta:
		db_table = 'CORE_MENU'
		verbose_name = 'Menu'
		verbose_name_plural = "Menus"

class ViewMenu( BaseModel ):
	"""
	
	Menus associated to a view
	
	**Attributes**
	
	* ``id``:AutoField : Primary Key
	* ``order``:IntegerField
	* ``hasSeparator``:BooleanField
	* ``zone``:CharField(10)
	
	**Relationships**
	
	* ``parent`` -> self
	* ``view`` -> View
	* ``menu`` -> Menu
	
	"""
	id = models.AutoField(primary_key=True, db_column='ID_CORE_VIEW_MENU')
	parent = models.ForeignKey('self', null=True, blank=True, db_column='ID_PARENT',
			verbose_name=_('Parent Menu'), help_text=_('Parent menu for menu item'))
	view = models.ForeignKey('core.View', db_column='ID_VIEW',
			verbose_name=_('View'), help_text=_('View'))
	menu = models.ForeignKey('core.Menu', db_column='ID_MENU',
			verbose_name=_('Menu'), help_text=_('Menu'))
	order = models.IntegerField(default=10, db_column='ORDER',
			verbose_name=_('Order'), help_text=_('Order for the menu item. Start with 10, increment by 10'))
	hasSeparator = models.BooleanField(default=False, db_column='HAS_SEPARATOR',
			verbose_name=_('Menu Separator'), help_text=_('Separator for menu. Will show a gray line above menu item'))
	zone = models.CharField(max_length=10, choices=Choices.MENU_ZONES, db_column='ZONE',
				verbose_name=_('Menu Zone'), help_text=_('Menu Zone for menu item: sys, main and view zone'))
	def __unicode__(self):
		return '%s - %s' % (self.view, self.menu)
	class Meta:
		unique_together = (('menu','view'),)
		db_table = 'CORE_VIEW_MENU'
		verbose_name = 'View Menu'
		verbose_name_plural = "Views for Menus"

class MenuParam( BaseModel ):
	"""
	
	Parameters or attributes feeded to views through menus. 
	
	Views have entry parameters that can be inserted statically through the menu (are not variables). 
	
	You can have a view that accept a parameter and create as many menu items as static entry parameters to the view.
	
	**Attributes**
	
	* ``id``:AutoField : Primary Key
	* ``operator``:CharField(10) : Operator as Choices.OP
	* ``value``:CharField(20)
	
	**Relationships**
	
	* ``menu`` -> Menu
	* ``name`` -> Param
	
	"""
	id = models.AutoField(primary_key=True, db_column='ID_CORE_MENU_PARAM')
	menu = models.ForeignKey('core.Menu', db_column='ID_MENU',
			verbose_name=_('Menu'), help_text=_('Menu'))
	name = models.ForeignKey('core.Param',db_column='ID_NAME',
			verbose_name=_('Parameter'), help_text=_('Parameter'))
	operator = models.CharField(max_length=10, choices=Choices.OP, db_column='OPERATOR', 
			verbose_name=_('Operator'), help_text=_('Operator'))
	value = models.CharField(max_length=20, db_column='VALUE',
			verbose_name=_('Value'), help_text=_('Value'))
	def __unicode__(self):
		return '%s' % (self.name)
	class Meta:
		db_table = 'CORE_MENU_PARAM'
		verbose_name = 'Menu Param'
		verbose_name_plural = "Menu Params"


class ViewMeta( BaseModel ):
	"""
	
	Meta information for views
	
	**Attributes**
	
	* ``id`` : Primary key
	* ``value``:TextField : Key value
	
	**Relationships**
	
	* ``view`` : View
	* ``meta`` : Meta Key
	
	"""
	id = models.AutoField(primary_key=True, db_column='ID_CORE_VIEW_META')
	view = models.ForeignKey(View, db_column='ID_VIEW',
				verbose_name = _('View'), help_text = _('View'))
	meta = models.ForeignKey(MetaKey, db_column='ID_META', limit_choices_to={'keyType__value': K.PARAM_META},
				verbose_name=_('Meta Key'), help_text=_('Meta Key') )
	value = models.TextField(db_column='VALUE', verbose_name = _('Value'), help_text = _('Value'))
	def __unicode__(self):
		return '%s %s' % (self.view, self.meta)
	class Meta:
		db_table = 'CORE_VIEW_META'
		verbose_name = 'View META'
		verbose_name_plural = "View META"

class ViewTmpl( BaseModel ):
	"""
	
	View Template
	
	**Attributes**
	
	* ``id``:AutoField : Primary Key 
	
	**Relationships**
	
	* ``view`` -> View
	* ``template`` -> XpTemplate
	
	"""
	id = models.AutoField(primary_key=True, db_column='ID_CORE_VIEW_TMPL')
	view = models.ForeignKey('core.View', db_column='ID_VIEW',
			verbose_name=_('View'), help_text=_('View'))
	template = models.ForeignKey('core.XpTemplate', db_column='ID_TEMPLATE',
			verbose_name=_('Template'), help_text=_('Template'))
	def __unicode__(self):
		return '%s - %s' % (self.view, self.template)
	class Meta:
		db_table = 'CORE_VIEW_TMPL'
		verbose_name = 'View Template'
		verbose_name_plural = "View Templates"

class XpTemplate( BaseModel ):
	"""
	
	Ximpia Template.
	
	Views can have N templates with language, country and device target features. You can target templates with device and localization.
	In case you want to provide different templates for user groups, profiles, etc... you would need to create different views and then
	map those views to access groups. Each of those views would have default templates and templates targetted at pads, smartphones,
	desktop and localization if required.
	
	Templates can window types:
	
	* Window - Views which render whole available screen area.
	* Popup - Modal views that popup when user clicks on actions or menu items.
	* Panel (Coming soon) - This window types is embedded within content, as a tooltip when user clicks on action or mouse goes
	over
	
	**Attributes**
	
	* ``id``:AutoField : Primary Key
	* ``name``:CharField(50)
	* ``alias``:CharField(20)
	* ``language``:CharField(2) : As Choices.LANG
	* ``country``:CharField(2) : As Choices.COUNTRY
	* ``winType``:CharField(20) : As Choices.WIN_TYPES
	* ``device``:CharField(10) : As Choices.DEVICES : Desktop computer, smartphones and tablets
	
	**Relationships**
	
	* ``application`` -> Application 
	
	"""
	id = models.AutoField(primary_key=True, db_column='ID_CORE_TEMPLATE')
	application = models.ForeignKey('core.Application', db_column='ID_APPLICATION',
			verbose_name=_('Application'), help_text=_('Application for the template'))
	name = models.CharField(max_length=50, db_column='NAME',
			verbose_name=_('Name'), help_text=_('Name'))
	alias = models.CharField(max_length=20, db_column='ALIAS',
			verbose_name=_('Alias'), help_text=_('Alias'))
	language = models.CharField(max_length=2, choices=Choices.LANG, default=Choices.LANG_ENGLISH, db_column='LANGUAGE', 
			verbose_name=_('Language'), help_text=_('Language'))
	country = models.CharField(max_length=2, choices=Choices.COUNTRY, blank=True, null=True, db_column='COUNTRY',
			verbose_name=_('Country'), help_text=_('Country'))
	winType = models.CharField(max_length=20, choices=Choices.WIN_TYPES, default=Choices.WIN_TYPE_WINDOW, db_column='WIN_TYPE',
			verbose_name=_('Window Type'), help_text=_('Window type: Window, Popup'))
	device = models.CharField(max_length=10, choices=Choices.DEVICES, default=Choices.DEVICE_PC, db_column='DEVICE',
			verbose_name=_('Device'), help_text=_('Device: Personal Computer, Tablet, Phone'))
	def __unicode__(self):
		return self.name
	class Meta:
		db_table = 'CORE_TEMPLATE'
		verbose_name = 'Template'
		verbose_name_plural = "Templates"
		unique_together = ("application", "name")

class Workflow( BaseModel ):
	"""
	
	WorkFlow.
	
	Ximpia comes with a basic application workflow to provide navigation for your views.
	
	Navigation is provided in window and popup window types.
	
	You "mark" as workflow view any service method with flow code (decorator). Actions are also "marked" as worflow actions with
	decorators.
	
	When actions are triggered by clicking on a button or similar, action logic is executed, and user displays view based on flow
	information and data inserted in the flow by actions. You do not have to map navigation inside your service operations.
	
	Plugging in a new view is pretty simple. You code the service view operation, include it in your flow, and view (window or popup)
	will be displayed when requirements are met 
	
	**Attributes**
	
	* ``id``:AutoField : Primary Key
	* ``code``:CharField(15) : Flow code
	* ``resetStart``:BooleanField : The flow data will be deleted when user displays first view of flow. The flow will be reset when
	user visits again any page in the flow.
	* ``deleteOnEnd``:BooleanField : Flow data is deleted when user gets to final view in the flow.
	* ``jumpToView``:BooleanField : When user visits first view in the flow, will get redirected to last visited view in the flow. User
	jumps to last view in the flow.
	
	**Relationships**
	
	* ``application`` -> Application
	
	"""
	id = models.AutoField(primary_key=True, db_column='ID_CORE_WORKFLOW')
	application = models.ForeignKey('core.Application', db_column='ID_APPLICATION',
			verbose_name = _('Application'), help_text = _('Application'))
	code = models.CharField(max_length=15, db_index=True, unique=True, db_column='CODE',
			verbose_name=_('Flow Code'), help_text=_('Flow Code. First window in a flow identified by a flow code will reset wf variables'))
	resetStart = models.BooleanField(default=False, db_column='RESET_START',
			verbose_name = _('Reset Start'), help_text = _('Reset on start: The flow will be deleted when user displays first view of flow'))
	deleteOnEnd = models.BooleanField(default=False, db_column='DELETE_ON_END',
			verbose_name = _('Delete on End'), help_text = _('Delete On End: Weather flow user data is deleted when user displays last view in flow'))
	jumpToView = models.BooleanField(default=True, db_column='JUMP_TO_VIEW',
			verbose_name = _('Jump to View'), help_text = _('Jump to View: In case user wants to display view and flow is in another view, the flow view will be shown'))
	def __unicode__(self):
		return self.code
	class Meta:
		db_table = 'CORE_WORKFLOW'
		verbose_name = 'Workflow'
		verbose_name_plural = "Workflows"

class WorkflowView( BaseModel ):
	"""
	
	WorkFlow View. Relationship between flows and your views.
	
	Source view triggers action, logic is executed and target view is displayed to user.
	
	**Attributes**
	
	* ``id``:AutoField : Primary Key
	* ``order``:IntegerField : View orderi flow. You can place order like 10, 20, 30 for views in our flow. And then later inyect views
	between those values, like 15, for example.
	
	**Relationships**
	
	* ``flow`` -> WorkFlow
	* ``viewSource`` -> View : Source view for flow
	* ``viewTarget`` -> View : Target view for flow
	* ``action`` -> Action : Action mapped to flow. Source view triggers action, logic is executed and target view is rendered and
	displayed.
	* ``params`` <-> Param through WFParamValue with related name 'flowView_params'
	
	"""
	id = models.AutoField(primary_key=True, db_column='ID_CORE_WORKFLOW_VIEW')
	flow = models.ForeignKey(Workflow, related_name='flowView', db_column='ID_FLOW', 
			verbose_name=_('Flow'), help_text=_('Work Flow'))
	viewSource = models.ForeignKey(View, related_name='flowViewSource', db_column='ID_VIEW_SOURCE',
			verbose_name=_('Source View'), help_text=_('View which starts flow'))
	viewTarget = models.ForeignKey(View, related_name='flowViewTarget', db_column='ID_VIEW_TARGET',
			verbose_name=_('target View'), help_text=_('View destiny for flow'))
	action = models.ForeignKey(Action, related_name='wf_action', unique=True, db_column='ID_ACTION',
			verbose_name=_('Action'), help_text=_('Action to process in the workflow navigation'))
	params = models.ManyToManyField(Param, through='core.WFParamValue', related_name='flowView_params', null=True, blank=True,
			verbose_name=_('Navigation Parameters'), help_text=_('Parameters neccesary to evaluate to complete navigation'))
	order = models.IntegerField(default=10, db_column='ORDER',
			verbose_name=_('Order'), help_text=_('Order'))
	def __unicode__(self):
		return '%s - %s - %s - op - %s' % (self.flow, self.viewSource, self.viewTarget, self.action)
	class Meta:
		db_table = 'CORE_WORKFLOW_VIEW'
		verbose_name = 'Workflow View'
		verbose_name_plural = "Workflow Views"
		unique_together = ('flow', 'viewSource', 'action', 'viewTarget')

class ViewParamValue( BaseModel ):
	"""
	
	Parameter Values for Workflow.
	
	This table holds the parameter values that trigger redirection to target views.
	
	**Attributes**
	
	* ``id``:AutoField : Primary Key
	* ``operator``:CharField(10) : Operator comparisson : equal, not equal, greater, etc..., as Choices.OP
	* ``value``:CharField(20)
	
	**Relationships**
	
	* ``view`` -> View
	* ``name`` -> Param
	
	"""
	id = models.AutoField(primary_key=True, db_column='ID_CORE_VIEW_PARAM_VALUE')
	view = models.ForeignKey(View, related_name='viewParam', db_column='ID_VIEW',
			verbose_name=_('View'), help_text=_('View for entry parameters'))
	name = models.ForeignKey(Param, db_column='ID_NAME',
			verbose_name=_('Parameter'), help_text=_('Parameter'))
	operator = models.CharField(max_length=10, choices=Choices.OP, db_column='OPERATOR', 
			verbose_name=_('Operator'), help_text=_('Operator'))
	value = models.CharField(max_length=20, db_column='VALUE',
			verbose_name=_('Value'), help_text=_('Value'))
	def __unicode__(self):
		return '%s %s %s' % (self.name, self.operator, self.value)
	class Meta:
		db_table = 'CORE_VIEW_PARAM_VALUE'
		verbose_name = 'View Parameter Value'
		verbose_name_plural = "View Parameter Values"


"""class WFViewEntryParam( BaseModel ):
	
	
	Relates flows with view entry parameters.
	
	**Attributes**
	
	* ``id``:AutoField : Primary Key
	
	**Relationships**
	
	* ``flowView`` -> WorkflowView
	* ``viewParam`` -> ViewParamValue
	
	"""
"""id = models.AutoField(primary_key=True, db_column='ID_CORE_WORKFLOW_VIEW_PARAM')
	flowView = models.ForeignKey(WorkflowView, related_name='flowViewEntryParam', db_column='ID_FLOW_VIEW', 
			verbose_name=_('Flow View'), help_text=_('Work Flow Views'))
	viewParam= models.ForeignKey(ViewParamValue, db_column='ID_VIEW_PARAM',
			verbose_name=_('View Param'), help_text=_('View parameter value'))
	def __unicode__(self):
		return '%s - %s' % (self.flowView, self.viewParam)
	class Meta:
		db_table = 'CORE_WORKFLOW_VIEW_PARAM'
		verbose_name = 'Workflow View Entry Param'
		verbose_name_plural = "Workflow View Entry Params" """

class WorkflowData( BaseModel ):
	"""
	
	User Workflow Data
	
	userId is the workflow user id. Flows support authenticated users and anonymous users. When flows start, in case not authenticated,
	workflow user id is generated. This feature allows having a flow starting at non-authenticated views and ending in authenticated 
	views, as well as non-auth flows.
	
	**Attributes**
	
	* ``id``:AutoField : Primary Key
	* ``userId``:CharField(40) : Workflow user id
	* ``data``:TextField : Workflow data encoded in json and base64
	
	**Relationships**
	
	* ``flow`` -> Workflow
	* ``view`` -> View
	
	"""
	id = models.AutoField(primary_key=True, db_column='ID_CORE_WORKFLOW_DATA')
	userId = models.CharField(max_length=40, db_column='USER_ID',
			verbose_name = _('Workflow User Id'), help_text = _('User Id saved as a cookie for workflow'))
	flow = models.ForeignKey(Workflow, related_name='flowData', db_column='ID_FLOW', 
			verbose_name=_('Flow'), help_text=_('Work Flow'))
	view = models.ForeignKey(View, related_name='viewFlowData', db_column='ID_VIEW',
			verbose_name=_('View'), help_text=_('View in flow. View where users is in flow'))
	data = models.TextField(default = _jsf.encode64Dict(getBlankWfData({})), db_column='DATA',
			verbose_name=_('Data'), help_text=_('Worflow data'))
	def __unicode__(self):
		return '%s - %s' % (self.userId, self.flow)
	class Meta:
		db_table = 'CORE_WORKFLOW_DATA'
		verbose_name = 'Workflow Data'
		verbose_name_plural = "Workflow Data"
		unique_together = ('userId', 'flow')


class WFParamValue( BaseModel ):
	"""
	
	Parameter Values for Workflow.
	
	**Attributes**
	
	* ``id``:AutoField : Primary Key
	* ``operator``:CharField(10) : Operator as Choices.OP
	* ``value``:CharField(20) : Workflow parameter value
	
	**Relationships**
	
	* ``flowView`` -> WorkflowView
	* ``name`` -> Param
	
	"""
	id = models.AutoField(primary_key=True, db_column='ID_CORE_WORKFLOW_PARAM_VALUE')
	flowView = models.ForeignKey(WorkflowView, related_name='flowViewParamValue', db_column='ID_FLOW_VIEW', 
			verbose_name=_('Flow View'), help_text=_('Work Flow Views'))
	name = models.ForeignKey(Param, db_column='ID_NAME',
			verbose_name=_('Parameter'), help_text=_('Parameter'))
	operator = models.CharField(max_length=10, choices=Choices.OP, db_column='OPERATOR', 
			verbose_name=_('Operator'), help_text=_('Operator'))
	value = models.CharField(max_length=20, db_column='VALUE',
			verbose_name=_('Value'), help_text=_('Value'))
	def __unicode__(self):
		return '%s %s %s' % (self.name, self.operator, self.value)
	class Meta:
		db_table = 'CORE_WORKFLOW_PARAM_VALUE'
		verbose_name = 'Workflow Parameter Value'
		verbose_name_plural = "Workflow Parameter Values"

class Settings ( BaseModel ):
	"""
	Settings model
	
	**Attributes**
	
	* ``value``:TextField : Settings value.
	* ``description``:CharField(255) : Setting description.
	* ``mustAutoload``:BooleanField : Has to load settings on cache?
	
	**Relationships**
	
	* ``name`` -> MetaKey : Foreign key to MetaKey model.
	
	"""
	
	name = models.ForeignKey(MetaKey, db_column='ID_META', limit_choices_to={'keyType__name': K.PARAM_SETTINGS},
				verbose_name=_('Name'), help_text=_('Settings name'))
	value = models.TextField(verbose_name = _('Value'), help_text = _('Settings value'), db_column='VALUE')
	description = models.CharField(max_length=255,
	        verbose_name = _('Description'), help_text = _('Description'), db_column='DESCRIPTION')
	mustAutoload = models.BooleanField(default=False,
	        verbose_name = _('Must Autoload?'), help_text = _('Must Autoload?'), db_column='MUST_AUTOLOAD')
	def __unicode__(self):
		return self.name.name
	class Meta:
		db_table = 'CORE_SETTINGS'
		verbose_name = _('Settings')
		verbose_name_plural = _('Settings')



##############################################################################################



class XpMsgException( Exception ):
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
		logger.debug( exception )
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

class XpRegisterException( Exception ):
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
		logger.debug('context....' )
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

class Context ( object ):

	app = None
	user = None
	lang = None
	settings = None
	session = None
	cookies = None
	meta = None
	post = None
	request = None
	get = None
	userChannel = None
	auth = {}
	form = None
	forms = {}
	captcha = None
	rawRequest = None
	ctx = None
	jsData = None
	viewNameSource = None
	viewNameTarget = None
	action = None
	isView = False
	isAction = False
	flowCode = None
	flowData = None
	isFlow = False
	set_cookies = []
	device = None
	country = None
	winType = None
	tmpl = None
	wfUserId = None
	isLogin = False
	container = {}
	
	"""
	
	Context
	
	**Attributes**
	
	* ``app``:String
	* ``user``:User
	* ``lang``:String
	* ``settings``:String
	* ``session``:String
	* ``cookies``:object
	* ``meta``:object
	* ``post``:object
	* ``request``:object
	* ``get``:object
	* ``userChannel``:String
	* ``auth``:Dict
	* ``form``:object
	* ``forms``:Dict
	* ``captcha``:String
	* ``rawRequest``:object
	* ``ctx``:object
	* ``jsData``:JsResultDict
	* ``viewNameSource``:String
	* ``viewNameTarget``:String
	* ``action``:String
	* ``isView``:Boolean
	* ``isAction``:Boolean
	* ``flowCode``:String
	* ``flowData``:String
	* ``isFlow``:Boolean
	* ``set_cookies``:List
	* ``device``:String
	* ``country``:String
	* ``winType``:String
	* ``tmpl``:String
	* ``wfUserId``:String
	* ``isLogin``:Boolean
	* ``container``:Dict
	
	"""
	
	def __init__(self):
		self.app = None
		self.user = User()
		self.lang = None
		self.settings = None
		self.session = None
		self.cookies = None
		self.meta = None
		self.post = None
		self.request = None
		self.get = None
		self.userChannel = None
		self.auth = {}
		self.form = None
		self.forms = {}
		self.captcha = None
		self.rawRequest = None
		self.ctx = None
		self.jsData = None
		self.viewNameSource = None
		self.viewNameTarget = None
		self.action = None
		self.isView = False
		self.isAction = False
		self.flowCode = None
		self.flowData = None
		self.isFlow = False
		self.set_cookies = []
		self.device = None
		self.country = None
		self.winType = None
		self.tmpl = None
		self.wfUserId = None
		self.isLogin = False
		self.container = {}

	def get_app(self):
		return self.__app
	def get_user(self):
		return self.__user
	def get_lang(self):
		return self.__lang
	def get_session(self):
		return self.__session
	def get_cookies(self):
		return self.__cookies
	def get_meta(self):
		return self.__meta
	def get_post(self):
		return self.__post
	def get_request(self):
		return self.__request
	def get_get(self):
		return self.__get
	def get_user_channel(self):
		return self.__userChannel
	def get_auth(self):
		return self.__auth
	def get_form(self):
		return self.__form
	def get_forms(self):
		return self.__forms
	def get_captcha(self):
		return self.__captcha
	def get_raw_request(self):
		return self.__rawRequest
	def get_ctx(self):
		return self.__ctx
	def get_js_data(self):
		return self.__jsData
	def get_view_name_source(self):
		return self.__viewNameSource
	def get_view_name_target(self):
		return self.__viewNameTarget
	def get_action(self):
		return self.__action
	def get_is_view(self):
		return self.__isView
	def get_is_action(self):
		return self.__isAction
	def get_flow_code(self):
		return self.__flowCode
	def get_flow_data(self):
		return self.__flowData
	def get_is_flow(self):
		return self.__isFlow
	def get_set_cookies(self):
		return self.__set_cookies
	def get_device(self):
		return self.__device
	def get_country(self):
		return self.__country
	def get_win_type(self):
		return self.__winType
	def get_tmpl(self):
		return self.__tmpl
	def get_wf_user_id(self):
		return self.__wfUserId
	def get_is_login(self):
		return self.__isLogin
	def get_container(self):
		return self.__container
	def set_app(self, value):
		self.__app = value
	def set_user(self, value):
		self.__user = value
	def set_lang(self, value):
		self.__lang = value
	def set_session(self, value):
		self.__session = value
	def set_cookies(self, value):
		self.__cookies = value
	def set_meta(self, value):
		self.__meta = value
	def set_post(self, value):
		self.__post = value
	def set_request(self, value):
		self.__request = value
	def set_get(self, value):
		self.__get = value
	def set_user_channel(self, value):
		self.__userChannel = value
	def set_auth(self, value):
		self.__auth = value
	def set_form(self, value):
		self.__form = value
	def set_forms(self, value):
		self.__forms = value
	def set_captcha(self, value):
		self.__captcha = value
	def set_raw_request(self, value):
		self.__rawRequest = value
	def set_ctx(self, value):
		self.__ctx = value
	def set_js_data(self, value):
		self.__jsData = value
	def set_view_name_source(self, value):
		self.__viewNameSource = value
	def set_view_name_target(self, value):
		self.__viewNameTarget = value
	def set_action(self, value):
		self.__action = value
	def set_is_view(self, value):
		self.__isView = value
	def set_is_action(self, value):
		self.__isAction = value
	def set_flow_code(self, value):
		self.__flowCode = value
	def set_flow_data(self, value):
		self.__flowData = value
	def set_is_flow(self, value):
		self.__isFlow = value
	def set_set_cookies(self, value):
		self.__set_cookies = value
	def set_device(self, value):
		self.__device = value
	def set_country(self, value):
		self.__country = value
	def set_win_type(self, value):
		self.__winType = value
	def set_tmpl(self, value):
		self.__tmpl = value
	def set_wf_user_id(self, value):
		self.__wfUserId = value
	def set_is_login(self, value):
		self.__isLogin = value
	def set_container(self, value):
		self.__container = value
	def del_app(self):
		del self.__app
	def del_user(self):
		del self.__user
	def del_lang(self):
		del self.__lang
	def del_session(self):
		del self.__session
	def del_cookies(self):
		del self.__cookies
	def del_meta(self):
		del self.__meta
	def del_post(self):
		del self.__post
	def del_request(self):
		del self.__request
	def del_get(self):
		del self.__get
	def del_user_channel(self):
		del self.__userChannel
	def del_auth(self):
		del self.__auth
	def del_form(self):
		del self.__form
	def del_forms(self):
		del self.__forms
	def del_captcha(self):
		del self.__captcha
	def del_raw_request(self):
		del self.__rawRequest
	def del_ctx(self):
		del self.__ctx
	def del_js_data(self):
		del self.__jsData
	def del_view_name_source(self):
		del self.__viewNameSource
	def del_view_name_target(self):
		del self.__viewNameTarget
	def del_action(self):
		del self.__action
	def del_is_view(self):
		del self.__isView
	def del_is_action(self):
		del self.__isAction
	def del_flow_code(self):
		del self.__flowCode
	def del_flow_data(self):
		del self.__flowData
	def del_is_flow(self):
		del self.__isFlow
	def del_set_cookies(self):
		del self.__set_cookies
	def del_device(self):
		del self.__device
	def del_country(self):
		del self.__country
	def del_win_type(self):
		del self.__winType
	def del_tmpl(self):
		del self.__tmpl
	def del_wf_user_id(self):
		del self.__wfUserId
	def del_is_login(self):
		del self.__isLogin
	def del_container(self):
		del self.__container

	app = property(get_app, set_app, del_app, "app's docstring")
	user = property(get_user, set_user, del_user, "user's docstring")
	lang = property(get_lang, set_lang, del_lang, "lang's docstring")
	session = property(get_session, set_session, del_session, "session's docstring")
	cookies = property(get_cookies, set_cookies, del_cookies, "cookies's docstring")
	meta = property(get_meta, set_meta, del_meta, "meta's docstring")
	post = property(get_post, set_post, del_post, "post's docstring")
	request = property(get_request, set_request, del_request, "request's docstring")
	get = property(get_get, set_get, del_get, "get's docstring")
	userChannel = property(get_user_channel, set_user_channel, del_user_channel, "userChannel's docstring")
	auth = property(get_auth, set_auth, del_auth, "auth's docstring")
	form = property(get_form, set_form, del_form, "form's docstring")
	forms = property(get_forms, set_forms, del_forms, "forms's docstring")
	captcha = property(get_captcha, set_captcha, del_captcha, "captcha's docstring")
	rawRequest = property(get_raw_request, set_raw_request, del_raw_request, "rawRequest's docstring")
	ctx = property(get_ctx, set_ctx, del_ctx, "ctx's docstring")
	jsData = property(get_js_data, set_js_data, del_js_data, "jsData's docstring")
	viewNameSource = property(get_view_name_source, set_view_name_source, del_view_name_source, "viewNameSource's docstring")
	viewNameTarget = property(get_view_name_target, set_view_name_target, del_view_name_target, "viewNameTarget's docstring")
	action = property(get_action, set_action, del_action, "action's docstring")
	isView = property(get_is_view, set_is_view, del_is_view, "isView's docstring")
	isAction = property(get_is_action, set_is_action, del_is_action, "isAction's docstring")
	flowCode = property(get_flow_code, set_flow_code, del_flow_code, "flowCode's docstring")
	flowData = property(get_flow_data, set_flow_data, del_flow_data, "flowData's docstring")
	isFlow = property(get_is_flow, set_is_flow, del_is_flow, "isFlow's docstring")
	set_cookies = property(get_set_cookies, set_set_cookies, del_set_cookies, "set_cookies's docstring")
	device = property(get_device, set_device, del_device, "device's docstring")
	country = property(get_country, set_country, del_country, "country's docstring")
	winType = property(get_win_type, set_win_type, del_win_type, "winType's docstring")
	tmpl = property(get_tmpl, set_tmpl, del_tmpl, "tmpl's docstring")
	wfUserId = property(get_wf_user_id, set_wf_user_id, del_wf_user_id, "wfUserId's docstring")
	isLogin = property(get_is_login, set_is_login, del_is_login, "isLogin's docstring")
	container = property(get_container, set_container, del_container, "container's docstring")

class ContextDecorator(object):
	_app = ''
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
				logger.debug( 'lang django: ' + lang )
				if lang not in langs:
					lang = 'en'
				# Instantiate app Context
				cls = getClass( self._app + '.service.Context' )
				ctx = cls()
				if False: ctx = Context()
				ctx.app = self._app
				ctx.user = request.user
				ctx.lang = lang
				ctx.settings = settings
				ctx.session = request.session
				ctx.cookies = request.COOKIES
				ctx.meta = request.META
				ctx.post = request.POST
				ctx.request = REQ
				ctx.rawRequest = request
				ctx.get = request.GET
				ctx.device = Choices.DEVICE_PC
				ctx.country = ''
				ctx.winType = Choices.WIN_TYPE_WINDOW
				ctx.tmpl = ''
				ctx.userChannel = None
				ctx.auth = {}
				ctx.form = None
				ctx.forms = {}
				ctx.captcha = None 
				ctx.viewNameSource = REQ[self.VIEW_NAME_SOURCE] if REQ.has_key(self.VIEW_NAME_SOURCE) else ''
				ctx.viewNameTarget = REQ[self.VIEW_NAME_TARGET] if REQ.has_key(self.VIEW_NAME_TARGET) else ''
				ctx.action = REQ[self.ACTION] if REQ.has_key(self.ACTION) else ''
				# Set isView and isAction. Used by data layer, to define which database name to use
				if request.REQUEST.has_key('view'):
					ctx.isView = True
					ctx.isAction = False
				elif request.REQUEST.has_key('action'):
					ctx.isAction = True
					ctx.isView = False
				else:
					ctx.isView = True
					ctx.isAction = False
				ctx.flowCode = ''
				ctx.flowData = ''
				ctx.isFlow = False
				ctx.jsData = ''
				ctx.wfUserId = ''
				#if request.REQUEST.has_key('socialChannel') and request.user.is_authenticated():
				if request.session.has_key('userChannel') and request.user.is_authenticated():
					# TODO: Get this from session
					ctx.userChannel = request.session['userChannel']
					logger.debug( 'Context :: userChannel: ' + ctx[self.USER_CHANNEL] )
				if request.user.is_authenticated():
					ctx.isLogin = True
				else:
					ctx.isLogin = False
				# Set cookies
				ctx.set_cookies = []
				argsDict['ctx'] = ctx
				resp = f(*argsTuple, **argsDict)
				return resp
			except Exception as e: #@UnusedVariable
				logger.debug( 'Context :: Exception...' )
				if settings.DEBUG == True:
					traceback.print_exc()
					#logger.debug( e.myException )
				raise
		return wrapped_f


class ContextViewDecorator(object):
	_app = ''
	__mode = ''
	def __init__(self, *argList, **args):
		if args.has_key('mode'):
			self.__mode = args['mode']
		else:
			self.__mode = 'view'
	def __call__(self, f):
		"""Decorator call method"""
		def wrapped_f(request, **args):
			try:
				logger.debug( 'ContextViewDecorator :: args: %s' % json.dumps(args) )
				logger.debug( 'ContextViewDecorator :: userAgent: %s' % request.META['HTTP_USER_AGENT'] )
								
				if request.META['HTTP_USER_AGENT'].find('MSIE 6') != -1 or request.META['HTTP_USER_AGENT'].find('MSIE 7') != -1 or \
					request.META['HTTP_USER_AGENT'].find('MSIE 8') != -1:
					result = render_to_response( 'noHTML5.html', RequestContext(request) )
					return result				

				if self.__mode == 'view':
					if args.has_key('app') and len(args['app']) != 0:
						self._app = args['app']
						self.__viewName = args['viewName'] if args.has_key('viewName') else ''
					else:
						self._app = 'site'
						self.__viewName = 'home'
				else:
					if args.has_key('app') and len(args['app']) != 0:
						self._app = args['app']
						#self.__viewName = args['viewName'] if args.has_key('viewName') else ''
					else:
						self._app = 'site'
						#self.__viewName = 'home'
				
				REQ = request.REQUEST 
				langs = ('en')
				lang = translation.get_language()
				logger.debug( 'ContextViewDecorator :: lang django: %s' % lang )
				if lang not in langs:
					lang = 'en'
				# Instantiate app Context
				cls = getClass( self._app + '.service.Context' )
				ctx = cls()
				if False: ctx = Context()
				ctx.ap = self._app
				ctx.user = request.user
				ctx.lang = lang
				ctx.settings = settings
				ctx.session = request.session
				ctx.cookies = request.COOKIES
				ctx.meta = request.META
				ctx.post = request.POST
				ctx.request = REQ
				ctx.rawRequest = request
				ctx.get = request.GET
				ctx.device = Choices.DEVICE_PC
				ctx.country = ''
				ctx.winType = Choices.WIN_TYPE_WINDOW
				ctx.tmpl = ''
				ctx.userChannel = None
				ctx.auth = {}
				ctx.form = None
				ctx.forms = {}
				ctx.captcha = None 
				ctx.viewNameSource = REQ[self.VIEW_NAME_SOURCE] if REQ.has_key(self.VIEW_NAME_SOURCE) else ''
				ctx.viewNameTarget = REQ[self.VIEW_NAME_TARGET] if REQ.has_key(self.VIEW_NAME_TARGET) else ''
				ctx.action = REQ[self.ACTION] if REQ.has_key(self.ACTION) else ''
				# Set isView and isAction. Used by data layer, to define which database name to use
				if request.REQUEST.has_key('view'):
					ctx.isView = True
					ctx.isAction = False
				elif request.REQUEST.has_key('action'):
					ctx.isAction = True
					ctx.isView = False
				else:
					ctx.isView = True
					ctx.isAction = False
				ctx.flowCode = ''
				ctx.flowData = ''
				ctx.isFlow = False
				ctx.jsData = ''
				ctx.wfUserId = ''
				#if request.REQUEST.has_key('socialChannel') and request.user.is_authenticated():
				if request.session.has_key('userChannel') and request.user.is_authenticated():
					# TODO: Get this from session
					ctx.userChannel = request.session['userChannel']
					logger.debug( 'Context :: userChannel: ' + ctx[self.USER_CHANNEL] )
				if request.user.is_authenticated():
					ctx.isLogin = True
				else:
					ctx.isLogin = False
				# Set cookies
				ctx.set_cookies = []
				args['ctx'] = ctx
				resp = f(request, **args)
				return resp
			except Exception as e: #@UnusedVariable
				logger.debug( 'Context :: Exception...' )
				if settings.DEBUG == True:
					traceback.print_exc()
					#logger.debug( e.myException )
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
		#logger.debug( 'dict : ' + statusIn + ' ' + responseIn + ' ' + errorsIn )
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
