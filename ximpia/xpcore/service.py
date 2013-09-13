# coding: utf-8

# python
import traceback
import string
import json
import types
import datetime
import os
import re
import copy

# django
from django.http import HttpResponse, Http404
from django.core.mail import send_mail
from django.utils.translation import ugettext as _
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.cache import cache

from business import WorkFlowBusiness
from models import get_result_ERROR, XpMsgException
from util import TemplateParser, AppTemplateParser, get_instances, get_app_path

from models import SearchIndex, Context

from data import ParamDAO, ApplicationDAO, TemplateDAO, ViewTmplDAO
from data import MenuParamDAO, ViewMenuDAO, ActionDAO, ServiceMenuDAO, ApplicationMediaDAO
from data import SearchIndexDAO, SearchIndexParamDAO, WordDAO, SearchIndexWordDAO, ViewMenuConditionDAO, ServiceMenuConditionDAO
from ximpia.util import resources
from choices import Choices

from ximpia.util import ut_email
from models import JsResultDict, ctx

# Constants
import constants as K

# Settings
from ximpia.xpcore.util import get_class
from ximpia.xpsite.data import SettingDAO
settings = get_class(os.getenv("DJANGO_SETTINGS_MODULE"))

# Logging
import logging.config
logging.config.dictConfig(settings.LOGGING)
logger = logging.getLogger(__name__)

from data import ViewDAO
from forms import DefaultForm 

from ximpia.util.js import Form as _jsf


class CommonWorker(object):
	"""
		Common worker class
	"""
	pass

class EmailService(object):
	#python -m smtpd -n -c DebuggingServer localhost:1025
	@staticmethod
	def send(xml_message, subs_dict, from_addr, recipient_list):
		"""Send email

		@staticmethod

		Run this to simulate email server:
		python -m smtpd -n -c DebuggingServer localhost:1025

		and have this in your settings.py:
		EMAIL_HOST = 'localhost'
		EMAIL_PORT = 1025

		**Attributes**

		``xmlMessage`` : Xml message (from settings)
		``subsDict`` : Substitution dictionary, like...
			{'scheme': settings.XIMPIA_SCHEME,
							'host': settings.XIMPIA_BACKEND_HOST,
							'appSlug': K.Slugs.SITE,
							'activate': K.Slugs.ACTIVATE_USER,
							'firstName': self._f()['firstName'],
							'user': self._f()['ximpiaId'],
							'activationCode': activationCode}
			Email Xml message should have variables marked with '$', like $host, $appslug, etc...
		``fromAddr``:String
		``recipientList``:List<String>

		**Returns**
		None
		"""
		#logger.debug( 'subsDict: %s' % (subsDict) )
		subject, message = ut_email.getMessage(xml_message)
		message = string.Template(message).substitute(**subs_dict)
		#logger.debug( message )
		send_mail(subject, message, from_addr, recipient_list)


# ****************************************************
# **                DECORATORS                      **
# ****************************************************

class service(object):
	"""Build response from jsData"""
	_pageError = False
	_form = None
	_isServerTmpl = False
	def __init__(self, *argsTuple, **argsDict):
		"""
		Options
		=======
		pageError: Show error detail as a list in a popup or show error in a message bar. pageError=True : Show error message bar
		form: Form class attached to the view
		isServerTmpl: True | False : If result is jsData or Http json representation
		"""
		#logger.debug( 'service :: argsDict: %s argsTuple: %s' % (argsDict, argsTuple) )
		if argsDict.has_key('pageError'):
			self._pageError = argsDict['pageError']
		else:
			self._pageError = False
		if argsDict.has_key('form'):
			self._form = argsDict['form']
		"""if argsDict.has_key('isServerTmpl'):
			self._isServerTmpl = argsDict['isServerTmpl']"""
	def __call__(self, f):
		def wrapped_f(*argsTuple, **argsDict):
			obj = argsTuple[0]
			logger.debug( 'service :: data: %s %s' % (argsTuple, argsDict) )
			try:
				doRedirect = False
				redirectUrl = ''
				self._isServerTmpl = obj._ctx.isServerTmpl
				logger.debug('service :: isServerTmpl: %s' % (self._isServerTmpl) )
				#logger.debug( 'service :: ctx: %s' % (obj._ctx.keys()) )
				obj._ctx.jsData = JsResultDict()
				if self._form != None:
					obj._set_main_form(self._form())
				f(*argsTuple, **argsDict)
				if not obj._ctx.doneResult:
					# Instances
					dbApp = ApplicationDAO(obj._ctx)
					# View
					logger.debug( 'service :: viewNameTarget: %s' % (str(obj._ctx.viewNameTarget)) )
					logger.debug( 'service :: viewNameSource: %s' % (str(obj._ctx.viewNameSource)) )
					if len(obj._ctx.viewNameTarget) > 1:
						viewName = obj._ctx.viewNameTarget
					else:
						viewName = obj._ctx.viewNameSource
					logger.debug( 'service :: viewName: %s' % (viewName) )
					# Views
					obj._ctx.jsData['response']['view'] = viewName
					logger.debug( 'service :: view: %s' % ('*' + str(obj._ctx.jsData['response']['view']) + '*') )
					# App
					obj._ctx.jsData['response']['app'] = obj._ctx.app
					obj._ctx.jsData['response']['appSlug'] = dbApp.get(name=obj._ctx.app).slug
					obj._ctx.jsData['response']['isDefaultApp'] = obj._ctx.app == settings.XIMPIA_DEFAULT_APP
					# winType
					if len(obj._ctx.jsData['response']['view'].strip()) != 0:
						dbView = ViewDAO(obj._ctx)
						view = dbView.get(application__name=obj._ctx.app, name=obj._ctx.jsData['response']['view'])
						logger.debug( 'service :: winType: %s' % (str(view.winType)) )
						obj._ctx.jsData['response']['winType'] = view.winType
						obj._ctx.jsData['response']['viewSlug'] = view.slug
					# User authenticate and session
					logger.debug('service :: User: %s' % (obj._ctx.user) )
					if obj._ctx.user.is_authenticated():
						# login: context variable isLogin = True
						obj._ctx.jsData.addAttr('isLogin', True)
						#obj._ctx.jsData.addAttr('userid', self._ctx['user'].pk)
						keyList = obj._ctx.session.keys()
						session = {}
						for key in keyList:
							if key[0] != '_':
								try:
									# We try to serialize using django serialize
									dataEncoded = _jsf.encodeObj(obj._ctx.session[key])
									dataReal = json.loads(dataEncoded)
									if type(obj._ctx.session[key]) == types.ListType:
										session[key] = dataReal
									else:
										session[key] = dataReal[0]
								except:
									# If we cant, we try json encode
									dataEncoded = json.dumps(obj._ctx.session[key])
									session[key] = json.loads(dataEncoded)
						obj._ctx.jsData['response']['session'] = session
					else:
						obj._ctx.jsData.addAttr('isLogin', False)
					# Template
					tmpl = TemplateService(obj._ctx)
					if len(obj._ctx.jsData['response']['view'].strip()) != 0:
						templates = tmpl.resolve(obj._ctx.jsData['response']['view'])
						if templates.has_key(obj._ctx.jsData['response']['view']):
							tmplName = templates[obj._ctx.jsData['response']['view']] #@UnusedVariable
							#tmplName = tmpl.resolve(obj._ctx.jsData['response']['view'])
							logger.debug( 'service :: tmplName: %s' % (tmplName) )
						else:
							raise XpMsgException(None, _('Error in resolving template for view'))
						obj._ctx.jsData['response']['tmpl'] = templates
					else:
						# In case we show only msg with no view, no template
						logger.debug( 'service :: no View, no template...' )
						obj._ctx.jsData['response']['tmpl'] = ''
					# Forms
					logger.debug( 'service :: forms: %s' % (obj._ctx.forms) )
					for formId in obj._ctx.forms:
						form = obj._ctx.forms[formId]
						if not obj._ctx.jsData.has_key(formId):
							form.build_js_data(obj._ctx.app, obj._ctx.jsData)
						logger.debug( 'service :: form: %s app: %s' % (formId, form.base_fields['app'].initial) )
					#logger.debug( 'service :: response keys : %s' % (obj._ctx.jsData['response'].keys()) )
					# Result
					#logger.debug( 'service :: isServerTmpl: %s' % (self._isServerTmpl) )
					# Settings
					if not obj._ctx.jsData['response'].has_key('settings'):
						obj._ctx.jsData['response']['settings'] = {}
					# Get settings with mustAutoLoad=true for global and for this app
					dbSetting = SettingDAO(obj._ctx, related_depth=1)
					settingsApp = dbSetting.search_settings(obj._ctx.app)
					for setting in settingsApp:
						try:
							value = eval(setting.value)
						except NameError:
							value = setting.value
						obj._ctx.jsData['response']['settings'][setting.name.name] = value
					# Menu
					menu = MenuService(obj._ctx)
					menuDict = menu.get_menus(viewName)
					obj._ctx.jsData['response']['menus'] = menuDict
					if self._isServerTmpl == False:
						result = obj._build_JSON_result(obj._ctx.jsData)
						#logger.debug( obj._ctx.jsData )
						################# Print response
						logger.debug('')
						logger.debug( 'service :: #################### RESPONSE ##################' )
						#logger.debug( 'service :: response keys: %s' % (obj._ctx.jsData['response'].keys()) )
						keys = obj._ctx.jsData['response'].keys()
						for key in keys:
							keyValue = obj._ctx.jsData['response'][key]
							#logger.debug( 'key: %s' % (key, type(keyValue)) )
							if type(keyValue) == types.DictType and keyValue.has_key('value'):
								logger.debug( 'service :: response %s : %s' % (key, str(keyValue['value'])) )
							elif type(keyValue) != types.DictType:
								logger.debug( 'service :: response %s: %s' % (key, str(keyValue)) )
							else:
								for newKey in keyValue:
									#logger.debug( 'newKey: ', newKey )
									#logger.debug( keyValue[newKey] )
									if type(keyValue[newKey]) == types.DictType and keyValue[newKey].has_key('value'):
										logger.debug( 'service :: response %s %s: %s' % (key, newKey, str(keyValue[newKey]['value'])) )
									elif type(keyValue[newKey]) != types.DictType:
										logger.debug( 'service :: response %s %s: %s' %  (key, newKey, str(keyValue[newKey])) )

						################# Print response
						logger.debug( 'service :: #################### RESPONSE ##################' )
						logger.debug( '' )
					else:
						result = obj._ctx.jsData
						#logger.debug( result )
						################# Print response
						logger.debug( '' )
						logger.debug( 'service :: #################### RESPONSE ##################' )
						#logger.debug( 'service :: response keys: %s' % (obj._ctx.jsData['response'].keys()) )
						keys = obj._ctx.jsData['response'].keys()
						for key in keys:
							keyValue = obj._ctx.jsData['response'][key]
							#logger.debug( 'key: ', key, type(keyValue) )
							if type(keyValue) == types.DictType and keyValue.has_key('value'):
								logger.debug( 'service :: response %s: %s' % (key, str(keyValue['value'])) )
							elif type(keyValue) != types.DictType:
								logger.debug( 'service :: response %s: %s' % (key, str(keyValue)) )
							else:
								for newKey in keyValue:
									#logger.debug( 'newKey: %s' % (newKey) )
									#logger.debug( keyValue[newKey] )
									if type(keyValue[newKey]) == types.DictType and keyValue[newKey].has_key('value'):
										logger.debug( 'service :: response %s %s: %s' % (key, newKey, str(keyValue[newKey]['value'])) )
									elif type(keyValue[newKey]) != types.DictType:
										logger.debug( 'service :: response %s %s: %s' % (key, newKey, str(keyValue[newKey])) )

						################# Print response
						logger.debug( 'service :: #################### RESPONSE ##################' )
						logger.debug( '' )
						logger.debug( obj._ctx.jsData['response'].keys() )
					#obj._ctx['_doneResult'] = True
					obj._ctx.doneResult = True
				else:
					logger.debug( 'service :: I skip building response, since I already did it!!!!!' )
					if self._isServerTmpl == False:
						result = obj._build_JSON_result(obj._ctx.jsData)
					else:
						result = obj._ctx.jsData
				return result
			except XpMsgException as e:
				logger.debug( 'service :: ERROR!!!! service!!!!!' )
				errorDict = obj._get_errors()
				if len(errorDict) != 0:
					if self._isServerTmpl == False:
						result = obj._build_JSON_result(obj._get_error_result_dict(errorDict, page_error=self._pageError))
					else:
						result = obj._get_error_result_dict(errorDict, page_error=self._pageError)
					logger.debug( result )
				else:
					if settings.DEBUG == True:
						logger.debug( errorDict )
						logger.debug( e )
						logger.debug( e.myException )
						traceback.print_exc()
					raise
				return result
		return wrapped_f

class validation(object):
	"""Business validation"""
	_pageError = False
	_form = None
	_isServerTmpl = False
	def __init__(self, *argsTuple, **argsDict):
		pass
	def __call__(self, f):
		def wrapped_f(*argsTuple, **argsDict):
			obj = argsTuple[0]
			f(*argsTuple, **argsDict)
			obj._is_valid()
		return wrapped_f

class validate_form(object):
	"""Checks that form is valid, builds result, builds errors"""
	_form = None
	_pageError = False
	def __init__(self, *argsTuple, **argsDict):
		"""
		Options
		=======
		form: Form class
		"""
		# Sent by decorator
		self._form = argsTuple[0]
		"""if argsDict.has_key('pageError'):
			self._pageError = argsDict['pageError']
		else:
			self._pageError = False"""
	def __call__(self, f):
		"""Decorator call method"""
		def wrapped_f(*argsTuple, **argsDict):
			"""Doc."""
			#logger.debug( 'validate_form :: %s %s' % (argsTuple, argsDict) )
			obj = argsTuple[0]
			#result = f(*argsTuple, **argsDict)
			obj._ctx.jsData = JsResultDict()
			obj._ctx.form = self._form(obj._ctx.post, ctx=obj._ctx)
			bForm = obj._ctx.form.is_valid()
			#obj._ctx.form = obj._f
			#logger.debug( 'validate_form :: Form Validation: %s' % (bForm) )
			if bForm == True:
				obj._set_main_form(obj._ctx.form)
				result = f(*argsTuple, **argsDict)
				return result
				"""try:
					f(*argsTuple, **argsDict)
					obj._f.buildJsData(obj._ctx.jsData)
					result = obj.build_JSON_result(obj._ctx.jsData)
					#logger.debug( result )
					return result
				except XpMsgException as e:
					errorDict = obj.getErrors()
					if settings.DEBUG == True:
						logger.debug( errorDict )
						logger.debug( e )
						logger.debug( e.myException )
						traceback.printl_exc()
					if len(errorDict) != 0:
						result = obj.build_JSON_result(obj.getErrorResultDict(errorDict, page_error=self._pageError))
					else:
						raise
					return result"""
				"""except Exception as e:
					if settings.DEBUG == True:
						logger.debug( e )
						traceback.printl_exc()"""
			else:
				if settings.DEBUG == True:
					logger.debug( 'Validation error!!!!!' )
					#logger.debug( obj._f )
					logger.debug( obj._ctx.form.errors )
					if obj._ctx.form.errors.has_key('invalid'):
						logger.debug( obj._ctx.form.errors['invalid'] )
					traceback.print_exc()
				if obj._ctx.form.errors.has_key('invalid'):
					errorDict = {'': obj._ctx.form.errors['invalid'][0]}
					logger.debug( 'errorDict: %s' % (errorDict) )
					result = obj._build_JSON_result(obj._getErrorResultDict(errorDict, page_error=True))
				else:
					#errorDict = {'': 'Error validating your data. Check it out and send again'}
					# Build errordict
					errorDict = {}
					for field in obj._ctx.form.errors:
						if field != '__all__':
							errorDict[field] = obj._ctx.form.errors[field][0]
					logger.debug( 'errorDict: %s' % (errorDict) )
					result = obj._build_JSON_result(obj._getErrorResultDict(errorDict, page_error=False))
				return result
		return wrapped_f

class wf_view( object ):

	__flowCode = ''

	def __init__(self, *argsTuple, **argsDict):
		"""resetStart, jumpToView"""
		self.__flowCode = argsTuple[0]

	def __call__(self, f):
		"""Doc."""
		def wrapped_f(*argsTuple, **argsDict):
			#logger.debug( 'WFViewstartDecorator :: %s %s' % (argsTuple, argsDict) )
			obj = argsTuple[0]
			#obj._wf = WorkFlowBusiness(obj._ctx)
			obj._ctx.flowCode = self.__flowCode
			obj._ctx.isFlow = True
			logger.debug( 'wf_view :: flowCode: %s' % (self.__flowCode) )
			flow = obj._wf.get(self.__flowCode)
			viewName = obj._ctx.viewNameSource
			logger.debug( 'wf_view :: View Current: %s' % (obj._ctx.viewNameSource) )
			# WorKflow User Id
			"""if obj._ctx.cookies.has_key('wfUserId'):
				obj._ctx.wfUserId = obj._ctx.cookies['wfUserId']
				logger.debug( 'wf_view :: COOKIE :: WF User Id: %s' % (obj._ctx.wfUserId) )
			else:
				obj._ctx.wfUserId = obj._wf.genUserId()
				obj._set_cookie('wfUserId', obj._ctx.wfUserId)
				logger.debug( 'wf_view :: WF UserId: %s' % (obj._ctx.wfUserId) )"""
			obj._ctx.wfUserId = obj._getWFUser()
			logger.debug( 'wf_view :: WF UserId: %s' % (obj._ctx.wfUserId) )
			hasFlow = True
			try:
				flowData = obj._wf.getFlowDataDict(obj._ctx.wfUserId, self.__flowCode)
				logger.debug( 'wf_view :: flowData: %s' % (flowData) )
			except XpMsgException:
				hasFlow = False
			logger.debug( 'wf_view :: hasFlow: %s' % (hasFlow) )
			if flow.jumpToView == True and hasFlow == True:
				# Get flow data, display view in flow data
				try:
					viewName = obj._wf.getView(obj._ctx.wfUserId, self.__flowCode)
					logger.debug( 'wf_view :: Jump to View: %s %s' % (obj._ctx.viewNameSource, viewName) )
				except XpMsgException:
					pass
			else:
				isFirstView = obj._wf.isFirstView(self.__flowCode, obj._ctx.viewNameSource)
				logger.debug( 'wf_view :: Flow Data: %s %s' % (hasFlow, isFirstView) )
				# Check that this view is first in flow
				if hasFlow == False and isFirstView == True:
					logger.debug( 'wf_view :: reset Flow... no flow and first window' )
					obj._wf.resetFlow(obj._ctx.wfUserId, self.__flowCode, obj._ctx.viewNameSource)
				elif isFirstView == True and flow.resetStart == True:
					logger.debug( 'wf_view :: reset Flow... resetStart=True and first view in flow...' )
					obj._wf.resetFlow(obj._ctx.wfUserId, self.__flowCode, obj._ctx.viewNameSource)
			obj._ctx.viewNameTarget = viewName
			# Jump to View in case jumpToView = True and viewName resolved from flow is different from current view
			#logger.debug( 'wf_view :: Jumps... %s %s' % (viewName, obj._ctx.viewNameSource) )
			if viewName != obj._ctx.viewNameSource:
				logger.debug( 'wf_view :: redirect to ... %s' % (viewName) )
				dbView = ViewDAO(obj._ctx)
				view = dbView.get(name=viewName)
				viewAttrs = obj._wf.getViewParams(self.__flowCode, viewName)
				# Show View
				impl = view.implementation
				implFields = impl.split('.')
				method = implFields[len(implFields)-1]
				classPath = ".".join(implFields[:-1])
				cls = get_class( classPath )
				objView = cls(obj._ctx) #@UnusedVariable
				obj._ctx.viewNameSource = viewName
				if (len(viewAttrs) == 0) :
					result = eval('objView.' + method)()
				else:
					result = eval('objView.' + method)(**viewAttrs)
			else:
				result = f(*argsTuple, **argsDict)
			return result
		return wrapped_f

class menu_action(object):
	__viewName = ''
	def __init__(self, *argsTuple, **argsDict):
		self.__viewName = argsTuple[0]
	def __call__(self, f):
		"""Decorator call method"""
		def wrapped_f(*argsTuple, **argsDict):
			obj = argsTuple[0]
			f(*argsTuple, **argsDict)
			# Show View
			dbView = ViewDAO(obj._ctx)
			view = dbView.get(name=self.__viewName)
			logger.debug( 'MenuAction :: %s' % (view.name) )
			obj._ctx.viewNameSource = view.name
			impl = view.implementation
			implFields = impl.split('.')
			method = implFields[len(implFields)-1]
			classPath = ".".join(implFields[:-1])
			cls = get_class( classPath )
			objView = cls(obj._ctx) #@UnusedVariable
			result = eval('objView.' + method)()
			return result
		return wrapped_f

class wf_action(object):
	__app = ''
	__flowCode = ''
	def __init__(self, *argsTuple, **argsDict):
		"""
		Options
		=======
		app: String : Application code
		"""
		# Sent by decorator
		"""if argsDict.has_key('app'):
			self._app = argsDict['app']"""
		#self.__flowCode = argsTuple[0]
		pass
	def __call__(self, f):
		"""Decorator call method"""
		def wrapped_f(*argsTuple, **argsDict):
			obj = argsTuple[0]
			try:
				#logger.debug( 'viewNameSource: %s' % (obj._ctx.viewNameSource) )
				#logger.debug( 'viewNameTarget: %s' % (obj._ctx.viewNameTarget) )
				#logger.debug( 'actionName: %s' % (obj._ctx.action) )
				#obj._wf = WorkFlowBusiness()
				actionName = obj._ctx.action
				flow = obj._wf.getFlowViewByAction(actionName).flow
				self.__app = flow.application.name
				logger.debug( 'app: %s' % (self.__app) )
				obj._ctx.flowCode = flow.code
				obj._ctx.isFlow = True
				#logger.debug( 'wf_action :: flowCode: %s' % (obj._ctx.flowCode) )
				obj._ctx.wfUserId = obj._ctx.cookies['wfUserId']
				logger.debug( 'COOKIE :: WF User Id: %s' % (obj._ctx.wfUserId) )
				result = f(*argsTuple, **argsDict)
				# Resolve View
				#logger.debug( 'session' % (obj._ctx.session) )
				viewTarget = obj._wf.resolveView(obj._ctx.wfUserId, self.__app, obj._ctx.flowCode,
								obj._ctx.viewNameSource, obj._ctx.action)
				viewName = viewTarget.name
				#logger.debug( 'viewName: %s' % (viewName) )
				# Insert view into workflow
				obj._wf.setViewName(viewName)
				viewAttrs = obj._wf.getViewParams(obj._ctx.flowCode, viewName)
				#logger.debug( 'viewAttrs: %s' % (viewAttrs) )
				# Save workflow
				flowData = obj._wf.save(obj._ctx.wfUserId, obj._ctx.flowCode)
				# Set Flow data dictionary into context
				obj._ctx.flowData = obj._wf.buildFlowDataDict(flowData)
				#logger.debug( 'flowDataDict: %s' % (obj._ctx.flowData) )
				# Delete user flow if deleteOnEnd = True
				if flow.deleteOnEnd == True and obj._wf.isLastView(obj._ctx.viewNameSource, viewName, obj._ctx.action):
					obj._wf.removeData(obj._ctx.wfUserId, obj._ctx.flowCode)
				obj._ctx.viewNameTarget = viewName
				# Show View
				impl = viewTarget.implementation
				implFields = impl.split('.')
				method = implFields[len(implFields)-1]
				classPath = ".".join(implFields[:-1])
				cls = get_class( classPath )
				objView = cls(obj._ctx) #@UnusedVariable
				if (len(viewAttrs) == 0) :
					result = eval('objView.' + method)()
				else:
					result = eval('objView.' + method)(**viewAttrs)
			except XpMsgException as e:
				logger.debug( 'ERROR!!!! wf_action!!!!!' )
				errorDict = obj._getErrors()
				if len(errorDict) != 0:
					result = obj._build_JSON_result(obj._getErrorResultDict(errorDict, page_error=True))
					logger.debug( result )
				else:
					if settings.DEBUG == True:
						logger.debug( errorDict )
						logger.debug( e )
						logger.debug( e.myException )
						traceback.print_exc()
					raise
			return result
		return wrapped_f

class view_tmpl(object):
	""""Decorator for django views in core module."""
	__viewName = ''
	__APP = ''
	__APP_OBJ = None
	__APP_SLUG = ''
	__package = ''
	_settings = {}
	def __init__(self, *argsTuple, **argsDict):
		if len(argsTuple) != 0:
			logger.debug('view_tmpl :: argList: %s' % (argsTuple) )
			#self.__APP = '.'.join(argsTuple[0].split('.')[:2])
			self.__package = argsTuple[0].split('.')[0]
			self.__APP = argsTuple[0].split('.')[1]
	def __call__(self, f):
		"""Decorator call method"""
		def wrapped_f(request, **args):

			logger.debug( 'view_tmpl :: args: %s' % args )

			# Data instances
			dbApp = ApplicationDAO(args['ctx'])
			dbView = ViewDAO(args['ctx'])

			ctx = args['ctx']
			if False: ctx = Context()
			if args.has_key('appSlug') and len(args['appSlug']) != 0:
				self.__APP_OBJ =  dbApp.get(slug=args['appSlug'])
				self.__APP = self.__APP_OBJ.name
				self.__APP_SLUG = self.__APP_OBJ.slug
				if args.has_key('viewSlug'):
					logger.debug( 'view_tmpl :: set from args view name' )
					try:
						view = dbView.get(slug=args['viewSlug'])
						args['ctx'].viewAuth = view.hasAuth
					except XpMsgException as e:
						raise Http404
					logger.debug('view_tmpl :: viewName: %s' % (view.name) )
					self.__viewName = view.name
				else:
					self.__viewName = ''
			else:
				# TODO: Use here the default app for project settings and default view...
				#self.__APP = 'ximpia.xpsite'
				self.__viewName = 'home'
			logger.debug('view_tmpl :: app: %s' % (self.__APP) )
			ctx.viewNameSource = self.__viewName
			resultJs = f(request, **args)
			logger.debug('view_tmpl :: viewNameSource: %s viewNameTarget: %s' % (args['ctx'].viewNameSource, args['ctx'].viewNameTarget) )
			if self.__viewName != args['ctx'].viewNameSource:
				self.__viewName = args['ctx'].viewNameSource
			if len(ctx.viewNameTarget) != 0:
				self.__viewName = ctx.viewNameTarget
			logger.debug( 'view_tmpl :: resultJs: %s' % resultJs )
			logger.debug( 'view_tmpl :: viewName: %s target: %s source: %s ' %
				(self.__viewName, args['ctx'].viewNameTarget, args['ctx'].viewNameSource) )
			template = TemplateService(ctx)
			templates = template.resolve(self.__viewName)
			logger.debug( 'view_tmpl :: templates: %s' % templates )
			if resultJs['status'] == 'ERROR':
				raise XpMsgException(None, resultJs['errors'][0][1])
			if templates.has_key(self.__viewName):
				tmplName = templates[self.__viewName]
				logger.debug( 'view_tmpl :: tmplName: %s' % tmplName )
				# Get template data
				tmplService = TemplateService(ctx)
				tmplData = tmplService.get(self.__APP, 'window', tmplName)
				# Get application template data with footer, scripts and styles
				tmplApp = tmplService.get_app(self.__APP)
				#logger.debug('view_tmpl :: tmplApp: %s' % (tmplApp) )
				parserApp = AppTemplateParser()
				parserApp.feed_app(tmplApp, self.__APP)
				logger.debug('view_tmpl :: styles: %s' % (parserApp.styles) )
				#logger.debug('view_tmpl :: tmplData: %s' % (tmplData) )
				parser = TemplateParser()
				parser.feed(tmplData)
				try:
					if self.__APP.find('.') != -1:
						masterTmpl = self.__APP.split('.')[1] + '.html'
					else:
						masterTmpl = self.__APP + '.html'
					logger.debug('view_tmpl :: masterTmpl: %s' % (masterTmpl) )
					logger.debug('view_tmpl :: title: %s' % (parser.title) )
					result = render_to_response( 'xp-base.html', RequestContext(request,
													{	'id_view': parser.id_view,
														'title': parser.title,
														'titleBar': parser.titleBar,
														'content': parser.content,
														'buttons': parser.buttons,
														'result': json.dumps(resultJs),
														'settings': settings,
														'view': resultJs['response']['view'],
														'viewSlug': resultJs['response']['viewSlug'],
														'app': self.__APP,
														'appSlug': self.__APP_SLUG,
														'scripts': parserApp.scripts,
														'styles': parserApp.styles,
														'footer': parserApp.footer
													}))
				except AttributeError as e:
					raise XpMsgException(e, _('Error in getting attributes from template. Check that title, titleBar, content and bottom button area exists.'))
				#result = result.replace('{{result}}', json.dumps(resultJs))
			else:
				raise XpMsgException(None, _('Error in resolving template for view %s' % (self.__viewName) ))

			return result
		return wrapped_f

class view ( object ):
	"""

	Decorator for ximpia views

	"""

	__form = None

	def __init__(self, form):
		self.__form = form

	def __call__(self, f):
		"""Decorator call method"""
		@service(form=self.__form)
		def wrapped_f(request, *argsTuple, **argsDict):
			result = f(request, *argsTuple, **argsDict)
			return result
		return wrapped_f

class action ( object ):
	"""

	Decorator for ximpia actions

	"""

	__form = None

	def __init__(self, form):
		self.__form = form

	def __call__(self, f):
		"""Decorator call method"""
		@validate_form(self.__form)
		@service()
		def wrapped_f(request, *argsTuple, **argsDict):
			logger.debug('action :: form: %s' % self.__form)
			result = f(request, *argsTuple, **argsDict)
			return result
		return wrapped_f

class workflow_view ( object ):
	"""

	Decorator for workflow views

	"""

	__form = None
	__flowCode = None

	def __init__(self, flowCode, form):
		self.__flowCode = flowCode
		self.__form = form

	def __call__(self, f):
		"""Decorator call method"""
		@wf_view(self.__flowCode)
		@service(form = self.__form)
		def wrapped_f(request, *argsTuple, **argsDict):
			logger.debug('workflow_view :: flowCode: %s form: %s' % (self.__flowCode, self.__form))
			result = f(request, *argsTuple, **argsDict)
			return result
		return wrapped_f

class workflow_action ( object ):
	"""

	Decorator for workflow actions

	"""

	__form = None
	__flowCode = None

	def __init__(self, flowCode, form):
		self.__flowCode = flowCode
		self.__form = form

	def __call__(self, f):
		"""Decorator call method"""
		@validate_form(self.__form)
		@wf_action()
		def wrapped_f(request, *argsTuple, **argsDict):
			logger.debug('workflow_action :: form: %s' % (self.__form) )
			result = f(request, *argsTuple, **argsDict)
			return result
		return wrapped_f

# ****************************************************
# **                DECORATORS                      **
# ****************************************************


class MenuService( object ):
	_ctx = None
	def __init__(self, ctx):
		"""Menu building and operations"""
		self._ctx = ctx

	def __checkRender(self, menuItem, conditions):
		"""
		Check menu condition for render

		** Attributes **

		* ``viewMenu``:Object : View menu model instance

		** Returns **

		* ``checkRender``:Boolean
		"""
		checkRender = True
		for conditionItem in conditions:
			conditionRule = conditionItem.condition.rule
			logger.debug('MenuService.__checkRule :: conditionItem: %s menuItem: %s' % (conditionItem.serviceMenu, menuItem) )
			if conditionRule != None and conditionRule != '' and conditionItem.serviceMenu.menu.name == menuItem.menu.name:
				# Replace javascript condition-like operators to python-like
				conditionRule = conditionRule.replace('&&', 'and')\
						.replace('||','or')\
						.replace('true','True')\
						.replace('false','False')
				resp = self._ctx.jsData.response
				patts = ['([a-zA-Z0-9._]+\ *==)','([a-zA-Z0-9._]+\ *!=)','([a-zA-Z0-9._]+\ *>)','([a-zA-Z0-9._]+\ *<)',\
							'([a-zA-Z0-9._]+\ *>=)','([a-zA-Z0-9._]+\ *<=)']
				for patt in patts:
					index = re.search(patt, conditionRule)
					if index != None:
						conditionRule = re.sub(patt, r'resp.\1', conditionRule)
				logger.debug('MenuService :: conditionRule: %s' % (conditionRule) )
				checkCondition = eval(conditionRule)
				logger.debug('MenuService :: checkCondition: %s %s' % (checkCondition, conditionItem.action) )
				if conditionItem.action == 'render':
					if checkCondition == False and conditionItem.value == True:
						logger.debug('MenuService.__checkRule :: conditionRule False and condition render set to True, no render')
						checkRender = False
					if checkCondition == True and conditionItem.value == False:
						logger.debug('MenuService.__checkRule :: conditionRule True and condition render set to False, no render')
						checkRender = False
		return checkRender

	def __getList(self, menuDict, menuList, conditionList):
		"""
		Append menu dictionary to list of menu items

		**Attributes**

		* ``menuDict`` : Menu data in dictionary format with atributes about menu item attributes
		* ``menuList`` : Queryset with menu items

		**Returns**

		None
		"""
		container = {}
		for menuItem in menuList:
			#logger.debug( 'getMenus :: menuItem: %s' % (menuItem) )
			#logger.debug( 'getMenus :: action: %s' % (menuItem.menu.action) )
			#logger.debug( 'getMenus :: view: %s' % (menuItem.menu.view) )
			# TODO: Check condition
			checkRender = self.__checkRender(menuItem, conditionList)
			if not checkRender:
				continue
			menuObj = {}
			if menuItem.menu.view != None:
				menuObj['service'] = menuItem.menu.view.service.name
			if menuItem.menu.action != None:
				menuObj['service'] = menuItem.menu.action.service.name
			menuObj['action'] = menuItem.menu.action.name if menuItem.menu.action != None else ''
			menuObj['view'] = menuItem.menu.view.name if menuItem.menu.view != None else ''
			menuObj['viewSlug'] = menuItem.menu.view.slug if menuItem.menu.view != None else ''
			if menuItem.menu.view != None and menuItem.menu.view.image != None:
				menuObj['image'] = menuItem.menu.view.image
			else:
				menuObj['image'] = ''
			menuObj['winType'] = menuItem.menu.view.winType if menuItem.menu.view != None else ''
			menuObj['sep'] = menuItem.hasSeparator
			menuObj['name'] = menuItem.menu.name
			menuObj['title'] = menuItem.menu.title
			menuObj['description'] = menuItem.menu.description
			menuObj['icon'] = menuItem.menu.icon.value if menuItem.menu.icon != None else ''
			menuObj['zone'] = menuItem.zone
			if menuItem.menu.view != None:
				menuObj['app'] = menuItem.menu.view.application.name
				menuObj['appSlug'] = menuItem.menu.view.application.slug
			elif menuItem.menu.action != None:
				menuObj['app'] = menuItem.menu.action.application.name
				menuObj['appSlug'] = menuItem.menu.action.application.slug
			# params
			params = self._dbMenuParam.search(menu=menuItem.menu)
			paramDict = {}
			# name, operator, value
			for param in params:
				if param.operator == Choices.OP_EQ:
					paramDict[param.name] = param.value
			menuObj['params'] = paramDict
			if menuItem.menu.view.application.name == settings.XIMPIA_DEFAULT_APP:
				menuObj['isDefaultApp'] = True
			container[menuItem.menu.name] = menuObj
			if menuItem.menu.view != None:
				menuObj['isCurrent'] = True if menuItem.menu.view.name == self.__viewName else False
			#logger.debug( 'menuObj: %s' % (menuObj) )
			if menuItem.parent == None:
				menuObj['items'] = []
				menuDict[menuItem.zone].append(menuObj)
				"""if menuItem.zone in ['sys','main']:
					if self._ctx.isLogin:
						menuDict[menuItem.zone].append(menuObj)
					else:
						if menuItem.menu.name == 'home':
							menuDict[menuItem.zone].append(menuObj)
				else:
					menuDict[menuItem.zone].append(menuObj)"""
			else:
				parentMenuObj = container[menuItem.parent.menu.name]
				parentMenuObj['items'].append(menuObj)
		logger.debug( 'getMenus :: menuDict: %s' % (menuDict) )

	def get_menus(self, view_Name):
		"""
		Build menus in dictionary format

		**Attributes**

		* ``view_Name`` : View name

		**Returns**

		menuDict:DictType having the format:

		{
			'sys': [...],
			'main': [...],
			'service': [
							{
								'service' : StringType,
								'action': StringType,
								'view': StringType,
								'winType': StringType,
								'hasSep' : BooleanType,
								'name' : StringType,
								'title' : StringType,
								'description' : StringType,
								'icon' : StringType,
								'zone' : StringType,
								'app' : StringType,
								'params' : DictType,
								'items' : ListType<DictType>,
								'isCurrent' : BooleanType,
								'isDefaultApp' : BooleanType
							}
			],
			'view': [...]
		}

		items value will be a list of dictionaries with menu dict keys (action, view, etc..)

		params have format key -> value as normal dictionaries.
		"""
		self.__viewName = view_Name
		# db instances
		self._dbView = ViewDAO(self._ctx, related_depth=2)
		self._dbViewMenu = ViewMenuDAO(self._ctx, related_depth=3)
		self._dbServiceMenu = ServiceMenuDAO(self._ctx, related_depth=3)
		self._dbMenuParam = MenuParamDAO(self._ctx, related_depth=3)
		self._dbViewMenuCondition = ViewMenuConditionDAO(self._ctx, related_depth=2)
		self._dbServiceMenuCondition = ServiceMenuConditionDAO(self._ctx, related_depth=2)
		# logic
		logger.debug( 'getMenus...' )
		logger.debug( 'getMenus :: appName: %s' % (self._ctx.app) )
		view = self._dbView.get(name=view_Name, application__name=self._ctx.app)
		logger.debug( 'getMenus :: view: %s' % (view) )

		#viewMenus = self._dbViewMenu.search( view=view ).order_by('order')
		#logger.debug( 'getMenus :: viewMenus: %s' % (viewMenus) )
		#logger.debug( 'getMenus :: viewMenus All: %s' % (self._dbViewMenu.getAll()) )
		logger.debug('getMenus :: user: %s %s' % (self._ctx.user, type(self._ctx.user)) )
		menuDict = {}
		menuDict[Choices.MENU_ZONE_SYS] = []
		menuDict[Choices.MENU_ZONE_MAIN] = []
		menuDict[Choices.MENU_ZONE_SERVICE] = []
		menuDict[Choices.MENU_ZONE_VIEW] = []

		# TODO: Get main and sys without link, from settings ???
		# linked to service
		# TODO: Move this to data layer????
		if self._ctx.user.is_anonymous():
			menuList = self._dbServiceMenu.search( 	menu__application__isSubscription=False,
													menu__view__hasAuth=False,
													service=view.service ).order_by('order')
		else:
			menuList = self._dbServiceMenu.search( 	Q(menu__application__isSubscription=False) |
												Q(menu__application__isSubscription=True) &
												Q(menu__application__accessGroup__group__user=self._ctx.user) ,
												service=view.service ).order_by('order')
		conditionList = self._dbServiceMenuCondition.search(serviceMenu__in=menuList)
		logger.debug('menuList Services: %s' % (menuList) )
		logger.debug('conditionList Services: %s' % (conditionList) )
		self.__getList(menuDict, menuList, conditionList)
		# linked to view
		if self._ctx.user.is_anonymous():
			menuList = self._dbViewMenu.search( 	menu__application__isSubscription=False,
													menu__view__hasAuth=False,
													view=view ).order_by('order')
		else:
			menuList = self._dbViewMenu.search( 	Q(menu__application__isSubscription=False) |
												Q(menu__application__isSubscription=True) &
												Q(menu__application__accessGroup__group__user=self._ctx.user) ,
												view=view ).order_by('order')
		conditionList = self._dbViewMenuCondition.search(viewMenu__in=menuList)
		logger.debug('menuList Views: %s' % (menuList) )
		logger.debug('conditionList Views: %s' % (conditionList) )
		self.__getList(menuDict, menuList, conditionList)
		return menuDict

class SearchService ( object ):
	_ctx = None
	def __init__(self, ctx):
		"""Search index operations"""
		self._ctx = ctx
		self._dbApp = ApplicationDAO(self._ctx)
		self._dbView = ViewDAO(self._ctx, related_depth=2)
		self._dbAction = ActionDAO(self._ctx, related_depth=2)
		self._dbSearch = SearchIndexDAO(self._ctx, related_depth=3)
		self._dbIndexWord = SearchIndexWordDAO(self._ctx, related_depth=2)
		self._dbWord = WordDAO(self._ctx)
		self._dbIndexParam = SearchIndexParamDAO(self._ctx, related_depth=3)
		self._dbParam = ParamDAO(self._ctx)
	def add_index(self, text, app_code, view_name=None, action_name=None, params={}):
		"""Add data to search index
		
		** Required Attributes **
		
		* ``text``:str : Text to index
		* ``app_code``:str : Application code
		
		** Optional Attributes **
		* ``view_name``:str : View name
		* ``action_name``:str : Action name. Either view name or action name must be called.
		* ``params``:dict : Parameters associated with the search entry.
		
		** Returns**
		None"""
		wordList = resources.Index.parseText(text)
		view = self._dbView.get(name=view_name) if view_name != None else None
		action = self._dbAction.get(name=action_name) if action_name != None else None
		app = self._dbApp.get(code=app_code)
		# delete search index
		try:
			search = self._dbSearch.get(application=app, view=view) if view_name != '' else (None, None)
			search = self._dbSearch.get(application=app, action=action) if action_name != '' else (None, None)
			search.delete()
		except SearchIndex.DoesNotExist:
			pass
		# Create search index
		search = self._dbSearch.create(application=app, view=view, action=action, title=text)
		for wordName in wordList:
			# Word
			word, created = self._dbWord.getCreate(word=wordName) #@UnusedVariable
			# SearchIndexWord
			searchWord = self._dbIndexWord.create(word=word, index=search) #@UnusedVariable
		for paramName in params:
			param = self._dbParam.getCreate(application=app, name=paramName)
			indexParam = self._dbIndexParam.create(searchIndex=search, name=param, operator=Choices.OP_EQ, #@UnusedVariable
								value=params[paramName])
	def search(self, text):
		"""Search for views and actions
		
		** Attributes **
		
		* ``text``:str : text to search
		
		** Returns**
		
		List of dictionaries with "id", "text", "image" and "extra" fields."""
		# Search first 100 matches
		# return best 15 matches with titile, link information and application icon
		# return results in format needed by autocomplete plugin
		wordList = resources.Index.parseText(text)
		logger.debug( 'wordList: %s' % (wordList) )
		#results = self._dbIndexWord.search(word__word__in=wordList)[:100]
		# Build Q instance
		# TODO: Get views / actions I have access and comply with states (logged in, etc...)
		myQ = Q(word__word__startswith=wordList[0])
		for word in wordList[1:]:
			myQ = myQ | Q(word__word__startswith=word)
		logger.debug( 'Q: %s' % (str(myQ)) )
		results = self._dbIndexWord.search(myQ)[:100]
		logger.debug( 'search :: results: %s' % (results) )
		logger.debug( results.query )
		container = {}
		containerData = {}
		apps = []
		for data in results:
			logger.debug( 'data: %s' % (data) )
			if not container.has_key(data.index.pk):
				container[data.index.pk] = 0
			container[data.index.pk] += 1
			containerData[data.index.pk] = data
			apps.append(data.index.application)
		logger.debug( 'conatiner: %s' % (container) )
		logger.debug( 'containerData: %s' % (containerData) )
		logger.debug('apps: {}'.format(apps))
		tupleList = []
		for pk in container:
			tupleList.append((container[pk], containerData[pk]))
		tupleList.sort()
		tupleListFinal = tupleList[:15]
		resultsFinal = []
		for theTuple in tupleListFinal:
			data = theTuple[1]
			myDict = {}
			extraDict = {}
			myDict['id'] = data.index.id
			myDict['text'] = data.index.title
			# get full path for image version: static...
			myDict['image'] = data.index.view.image.version_generate('thumbnail').url if data.index.view and data.index.view.image else ''
			myDict['image'] = data.index.action.image.version_generate('thumbnail').url if data.index.action and  data.index.action.image else myDict['image']
			# app image
			if  myDict['image'] == '':
				try: 
					image = data.index.application.applicationmedia_set.get(type__name=K.PARAM_ICON).image
					myDict['image'] = image.version_generate('thumbnail').url
				except:
					pass
			extraDict['view'] = data.index.view.name if data.index.view != None else ''
			if data.index.view:
				extraDict['winType'] = data.index.view.winType
			extraDict['action'] = data.index.action.name if data.index.action != None else ''
			params = data.index.params.all()
			paramDict = {}
			for param in params:
				paramDict[param.name] = param.value
			extraDict['params'] = paramDict
			extraDict['app'] = data.index.application.name
			myDict['extra'] = extraDict
			resultsFinal.append(myDict)
		return resultsFinal

class TemplateService ( object ):
	"""
	Template service with operations to resolve and obtain templates
	"""
	_ctx = None
	__MODES = ['window','popup']
	__app = ''
	__mode = ''
	__tmplName = ''
	def __init__(self, ctx):
		"""Menu building and operations"""
		self._ctx = ctx
		self._dbViewTmpl = ViewTmplDAO(self._ctx, related_depth=2)
		self._dbTemplate = TemplateDAO(self._ctx)
	def __findTemplPath(self, module):
		"""
		Find template searching on templates/ directory in application

		**Attributes**

		* ``module``:Object : Application module. For app='ximpia.xpsite', module would be same as from ximpia import site
		* ``mode``:String : window or popup

		**Returns**

		* ``path``:String : Path to template
		"""
		#path = m.__file__.split('__init__')[0] + 'templates/' + mode + '/' + tmplName + '.html'
		path = ''
		pathMain = module.__file__.split('__init__')[0] + 'templates'
		logger.debug('TemplateService.__findTemplPath :: pathMain: %s' % (pathMain) )
		fileList = os.listdir(pathMain)
		logger.debug('TemplateService.__findTemplPath :: fileList: %s' % (fileList) )
		logger.debug('TemplateService.__findTemplPath :: tmplName: %s mode: %s' % (self.__tmplName, self.__mode) )
		for item in fileList:
			if item != 'site' and os.path.isdir(pathMain + '/' + item):
				if item in self.__MODES:
					fileList = os.listdir(pathMain + '/' + item)
					for myFile in fileList:
						if myFile == self.__tmplName + '.html':
							path = pathMain + '/' + item + '/' + myFile
							break
				else:
					if os.path.exists(pathMain + '/' + item + '/' + self.__mode):
						fileList = os.listdir(pathMain + '/' + item + '/' + self.__mode)
						for myFile in fileList:
							if myFile == self.__tmplName + '.html':
								path = pathMain + '/' + item + '/' + self.__mode + '/' +  myFile
								break
					else:
						raise XpMsgException(None, _('Template directory has no ' + ' or '.join(self.__MODES) + ' modes') )
			if path != '':
				break
		if path == '':
			raise XpMsgException(None, _('Could not get template file for application=%s, mode=%s, templName=%s' %\
										 (self.__app, self.__mode, self.__tmplName) ))
		return path

	def __discover_site_path(self, app):
		project_name, app_name = app.split('.')
		site_path = cache.get('app_' + app_name + '_site_path')
		if not site_path:
			appModulePath = settings.__file__.split('settings')[0]
			file_list = os.listdir(appModulePath)
			site_path = ''
			for app in file_list:
				try:
					if os.path.isdir(appModulePath + app) and 'xpsite' in os.listdir(appModulePath + app + '/templates'):
						site_path = appModulePath + app + '/templates/xpsite'
				except OSError:
					# templates directory not found
					pass
			cache.set('app_' + app_name + '_xpsite_path', site_path)
		return site_path

	def get_app(self, app):
		"""
		Get application template with styles, scripts and footer

		** Attributes **

		* ``app``:string : Application, like 'ximpia.xpsite'

		** Returns **

		* ``tmpl``:string
		"""
		self.__app = app
		logger.debug('TemplateService.get_app :: app: %s' % app)
		# go to project. Search in all apps for site templates, write path into cache
		if settings.DEBUG == True:
			package, module = get_app_path(app).split('.')
			m = get_class(package + '.' + module)
			if app == 'ximpia.xpsite':
				#appModulePath = settings.__file__.split('settings')[0]
				# would get this from cache
				pathSite = self.__discover_site_path(app)
				#pathSite = appModulePath + 'web/templates/site'
				if os.path.exists(pathSite) and os.path.isdir(pathSite):
					path = pathSite + '/' + app.split('.')[1] + '.html'
			else:
				path = m.__file__.split('__init__')[0] + 'templates/' + module + '/' + module + '.html'
			logger.debug('path: {}'.format(path))
			if os.path.isfile(path):
				with open(path) as f:
					tmpl = f.read()
				cache.set('tmpl/' + app, tmpl)
			else:
				raise XpMsgException(None, _('application template is not found.'))
		else:
			tmpl = cache.get('tmpl/' + app)
			if not tmpl:
				package, module = app.split('.')
				m = get_class(package + '.' + module)
				path = m.__file__.split('__init__')[0] + 'templates/' + module + '/' + module + '.html'
				if os.path.isfile(path):
					with open(path) as f:
						tmpl = f.read()
				else:
					raise XpMsgException(None, _('application template is not found.'))
		return tmpl

	def get(self, app, mode, tmpl_name):
		"""
		Get template

		**Attributes**

		* ``app``:String
		* ``mode``:String
		* ``tmplName``:String

		**Returns**

		* ``tmpl``:String

		"""
		self.__app, self.__mode, self.__tmplName = app, mode, tmpl_name

		logger.debug('TemplateService.get :: app: %s tmpl_name: %s' % (app, tmpl_name))

		if settings.DEBUG == True:
			if app.find('.') != -1:
				package, module = app.split('.')
			else:
				logger.debug('path: {}'.format(get_app_path(app)))
				package, module = get_app_path(app).split('.')
			m = get_class(package + '.' + module)
			if app == 'ximpia.xpsite':
				#appModulePath = settings.__file__.split('settings')[0]
				pathSite = self.__discover_site_path(app)
				if os.path.exists(pathSite) and os.path.isdir(pathSite):
					path = pathSite + '/' + mode + '/' + tmpl_name + '.html'
				else:
					raise XpMsgException(None, _('site directory inside templates does not exist'))
			else:
				path = self.__findTemplPath(m)
			logger.debug('TemplateService.get :: path: %s' % (path) )
			with open(path) as f:
				tmpl = f.read()
			cache.set('tmpl/' + app + '/' + mode + '/' + tmpl_name, tmpl)
		else:
			tmpl = cache.get('tmpl/' + app + '/' + mode + '/' + tmpl_name)
			if not tmpl:
				package, module = app.split('.')
				m = get_class(package + '.' + module)
				if app == 'ximpia.xpsite':
					#appModulePath = settings.__file__.split('settings')[0]
					pathSite = self.__discover_site_path(app)
					if os.path.exists(pathSite) and os.path.isdir(pathSite):
						path = pathSite + '/' + mode + '/' + tmpl_name + '.html'
					else:
						raise XpMsgException(None, _('site directory inside templates does not exist'))
				else:
					path = self.__findTemplPath(m)
				logger.debug('TemplateService.get :: path: %s' % (path) )
				with open(path) as f:
					tmpl = f.read()
				cache.set('tmpl/' + app + '/' + mode + '/' + tmpl_name, tmpl)
		return tmpl

	def resolve(self, view_name):
		"""Resolve template """
		# Context: device, lang, country
		#tmplName = ''
		templates = {}
		if self._ctx.lang != 'en' or self._ctx.country != '' or self._ctx.device != Choices.DEVICE_PC:
			# TODO: Complete for language and device templates
			"""tmplList = self._dbViewTmpl.search(view__name=viewName, template__language=self._ctx.lang)
			if len(tmplList) > 1:
				tmplName = tmplList.filter(template__winType=Choices.WIN_TYPE_WINDOW)[0].template.name
			else:
				if len(tmplList) != 0:
					tmplName = tmplList[0].template.name
				else:
					pass"""
		else:
			tmplList = self._dbViewTmpl.search(view__name=view_name, template__language=self._ctx.lang)
			logger.debug('TemplateService.resolve :: tmplList: {}'.format(tmplList))
			for viewTmpl in tmplList:
				tmpl = viewTmpl.template
				# alias? name?
				templates[tmpl.alias] = tmpl.name
			"""if len(tmplList) > 1:
				#tmplName = tmplList.filter(template__winType=Choices.WIN_TYPE_WINDOW)[0].template.name
				tmpl = tmplList.filter(template__winType=Choices.WIN_TYPE_WINDOW)[0].template
				templates[tmpl.alias] = tmpl.name
			else:
				if len(tmplList) != 0:
					tmplName = tmplList[0].template.name
				else:
					pass"""
		logger.debug( 'TemplateService.resolve :: templates: {}'.format(templates))
		return templates


class CommonService( object ):

	_ctx = None
	_request = None
	_errorDict = {}
	_resultDict = {}
	_form = None
	_postDict = {}
	_businessOK = False
	_viewNameTarget = ''
	_isFormOK = None
	_views = {}
	_actions = {}
	_wf = None
	_wfUserId = ''
	request = None

	def __init__(self, ctx):
		self._ctx = ctx
		self._ctx_min = copy.copy(self._ctx)
		self._ctx_min.to_min()
		if False: self._ctx = ctx()
		self._resultDict = get_result_ERROR([])
		self._postDict = ctx.post
		self._errorDict = {}
		self._resultDict = {}
		self._isFormOK = None
		self._wf = WorkFlowBusiness(self._ctx)
		self._viewNameTarget = ''
		self._wfUserId = ''

	def get_request(self):
		return self.__request


	def set_request(self, value):
		self.__request = value


	def del_request(self):
		del self.__request


	def _build_JSON_result(self, result_dict):
		"""Builds json result
		@param resultDict: dict : Dictionary with json data
		@return: result : HttpResponse"""
		#logger.debug( 'Dumping...' )
		sResult = json.dumps(result_dict)
		#logger.debug( 'sResult : %s' % (sResult) )
		result = HttpResponse(sResult)
		return result

	def _add_error_fields(self, id_error, form, error_field):
		"""Add error
		@param id_error: String : Id of error
		@param form: Form
		@param error_field: String : The field inside class form"""
		if not self._errorDict.has_key(id_error):
			self._errorDict[id_error] = {}
		self._errorDict[id_error] = form.fields[error_field].initial

	def _put_flow_params(self, **args):
		"""Put parameters into workflow or navigation system.
		@param args: Arguments to insert into persistence"""
		self._wf.putParams(**args)
		"""if self._ctx.isFlow:
			self._wf.putParams(**args)
		else:
			dd = json.loads(self._ctx.form.base_fields['entryFields'].initial)
			for name in args:
				dd[name] = args[name]
			self._ctx.form.base_fields['entryFields'].initial = json.dumps(dd)"""

	def _add_attr(self, name, value):
		"""
		Add attribute to jsData response object

		**Attributes**

		* ``name``
		* ``value``

		** Returns **

		"""
		self._ctx.jsData.addAttr(name, value)

	def _set_target_view(self, view_name):
		"""Set the target view for navigation."""
		self._viewNameTarget = view_name
		self._ctx.viewNameTarget = view_name

	def _show_view(self, view_name, view_attrs={}):
		"""Show view.
		@param view_name:
		@param view_attrs:
		@return: result"""
		self._set_target_view(view_name)
		db = ViewDAO(self._ctx)
		viewTarget = db.get(name=view_name)
		impl = viewTarget.implementation
		implFields = impl.split('.')
		method = implFields[len(implFields)-1]
		classPath = ".".join(implFields[:-1])
		cls = get_class( classPath )
		objView = cls(self._ctx) #@UnusedVariable
		if (len(view_attrs) == 0) :
			result = eval('objView.' + method)()
		else:
			result = eval('objView.' + method)(**view_attrs)

		return result

	def _get_target_view(self):
		"""Get target view."""
		return self._viewNameTarget

	def _get_flow_params(self, *name_list):
		"""Get parameter for list given, either from workflow dictionary or parameter dictionary in view.
		@param name_list: List of parameters to fetch"""
		logger.debug( 'wfUserId: %s flowCode: %s' % (self._ctx.wfUserId, self._ctx.flowCode) )
		valueDict = self._wf.getFlowDataDict(self._ctx.wfUserId, self._ctx.flowCode)['data']
		logger.debug( 'valueDict: %s' % (valueDict) )
		"""valueDict = {}
		for name in nameList:
			#value = self._wf.getParam(name)
			value = self._wf.getParamFromCtx(name)
			valueDict[name] = value"""
		"""if self._ctx.isFlow:
			logger.debug( 'flow!!!!' )
			for name in nameList:
				#value = self._wf.getParam(name)
				value = self._wf.getParamFromCtx(name)
				valueDict[name] = value
		else:
			logger.debug( 'navigation!!!' )
			dd = json.loads(self._ctx.form.base_fields['entryFields'].initial)
			for name in nameList:
				if dd.has_key(name):
					valueDict[name] = dd[name]"""
		return valueDict

	def _get_wf_user(self):
		"""Get Workflow user."""
		if self._ctx.cookies.has_key('XP_WFUID'):
			self._ctx.wfUserId = self._ctx.cookies['XP_WFUID']
		else:
			self._ctx.wfUserId = self._wf.genUserId()
			self._set_cookie('XP_WFUID', self._ctx.wfUserId)
		self._wfUserId = self._ctx.wfUserId
		return self._wfUserId

	def _get_error_result_dict(self, error_dict, page_error=False):
		"""Get sorted error list to show in pop-up window
		@return: self._result_dict : ResultDict"""
		#dict = self._errorDict
		keyList = error_dict.keys()
		keyList.sort()
		myList = []
		for key in keyList:
			message = error_dict[key]
			index = key.find('id_')
			if page_error == False:
				if index == -1:
					myList.append(('id_' + key, message, False))
				else:
					myList.append((key, message, False))
			else:
				if index == -1:
					myList.append(('id_' + key, message, True))
				else:
					myList.append((key, message, True))
		self._result_dict = get_result_ERROR(myList)
		return self._result_dict

	def _get_setting(self, setting_name):
		"""
		Get setting model instance.

		** Attributes **

		* ``settingName``:String : Setting name

		** Returns **

		models.site.Setting model instance
		"""
		self._dbSetting = SettingDAO(self._ctx, related_depth=2)
		setting = self._dbSetting.get(name__name=setting_name)
		return setting

	def _do_validations(self, validation_dict):
		"""Do all validations defined in validation dictionary"""
		bFormOK = self._ctx.form.is_valid()
		if bFormOK:
			keys = self.validationDict.keys()
			for key in keys:
				oVal = eval(key)(self._ctx)
				for sFunc in self.validationDict[key]:
					oVal.eval(sFunc)()
				self._doErrors(oVal.getErrors())
		"""if self.isBusinessOK() and bFormOK:
			result = f(*argsTuple, **argsDict)
			# check errors
			return wrapped_f
		else:
			# Errors
			result = self._build_JSON_result(self._getErrorResultDict())
			return result"""

	def _get_form(self):
		"""Get form"""
		#logger.debug( 'form: %s' % (self._ctx.form) )
		return self._ctx.form

	def _set_form(self, form_instance):
		"""Sets the form instance"""
		self._ctx.form = form_instance
		self._isFormOK = self._ctx.form.is_valid()

	def _get_main_form_id(self):
		""""
		Get main form id, like ``form_xxxx`` where xxxx is the returned value
		"""
		logger.debug('main formId: %s' % (self._ctx.form._XP_FORM_ID) )
		return self._ctx.form._XP_FORM_ID

	def _get_post_dict(self):
		"""Get post dictionary. This will hold data even if form is not validated. If not validated cleaned_value will have no values"""
		return self._postDict

	def _is_business_ok(self):
		"""Checks that no errors have been generated in the validation methods
		@return: isOK : boolean"""
		if len(self._errorDict) == 0:
			self._businessOK = True
		return self._businessOK

	def _is_form_valid(self):
		"""Is form valid?"""
		if self._isFormOK == None:
			self._isFormOK = self._ctx.form.is_valid()
		return self._isFormOK

	def _is_form_bs_ok(self):
		"""Is form valid and business validations passed?"""
		bDo = False
		if len(self._errorDict.keys()) == 0:
			self._isBusinessOK = True
		if self._isFormOK == True and self._isBusinessOK == True:
			bDo = True
		return bDo

	def _f(self):
		"""Returns form from context"""
		return self._ctx.form

	def _add_error(self, field_name, err_msg):
		"""Add error
		"""
		#form = self._getForm()
		#logger.debug( 'form: %s' % (form) )
		#msgDict = _jsf.decodeArray(form.fields['errorMessages'].initial)
		idError = 'id_' + field_name
		if not self._errorDict.has_key(idError):
			self._errorDict[idError] = {}
		self._errorDict[idError] = err_msg
		logger.debug( '_errorDict : %s' % (self._errorDict) )

	def _get_errors(self):
		"""Get error dict
		@return: errorDict : Dictionary"""
		return self._errorDict

	def _get_post(self):
		"""Get post dictionary"""
		return self._ctx.post

	def _validate_exists(self, db_data_list):
		"""Validates that db data provided exists. Error is shown in case does not exist.
		Db data contains data instance, query arguments in a dictionary
		and errorName for error message display at the front
		@param dbDataList: [dbObj, queryArgs, fieldName, errMsg]"""
		logger.debug( 'validateExists...' )
		logger.debug( 'dbDataList : %s' % (db_data_list) )
		for dbData in db_data_list:
			dbObj, qArgs, fieldName, errMsg = dbData
			exists = dbObj.check(**qArgs)
			logger.debug( 'validate Exists Data: args: %s exists: %s fieldName: %s errMsg: %s' %
						(qArgs, str(exists), str(fieldName), str(errMsg)) )
			if not exists:
				self._add_error(fieldName, errMsg)

	def _validate_not_exists(self, db_data_list):
		"""Validates that db data provided does not exist. Error is shown in case exists.
		Db data contains data instance, query arguments in a dictionary
		and errorName for error message display at the front
		@param dbDataList: [dbObj, queryArgs, fieldName, errMsg]"""
		logger.debug( 'validateNotExists...' )
		logger.debug( 'dbDataList : %s' % (db_data_list) )
		for dbData in db_data_list:
			dbObj, qArgs, fieldName, errMsg = dbData
			exists = dbObj.check(**qArgs)
			logger.debug( 'Exists : %s' % (exists) )
			if exists:
				logger.debug( 'I add error: %s %s' % (fieldName, errMsg) )
				self._add_error(fieldName, errMsg)

	def _validate_context(self, ctx_data_list):
		"""Validates context variable. [[name, value, fieldName, errName],...]"""
		for ctxData in ctx_data_list:
			name, value, fieldName, errMsg = ctxData
			if self._ctx[name] != value:
				self._add_error(fieldName, errMsg)

	def _authenticate_user(self, ximpia_id, password, field_name, error_msg):
		"""Authenticates user and password"""
		q_args = {'username': ximpia_id, 'password': password}
		user = authenticate(**q_args)
		if user:
			pass
		else:
			self._add_error(field_name, error_msg)
		return user

	def _authenticate_user_soc_net(self, social_id, social_token, auth_source, field_name, error_msg):
		"""Authenticates user and password"""
		q_args = {'socialId': social_id, 'socialToken': social_token}
		logger.debug('_authenticateUsersocNet :: Arguments: %s' % (q_args) )
		user = authenticate(**q_args)
		if user:
			pass
		else:
			self._add_error(field_name, error_msg)
		return user

	def _is_valid(self):
		"""Checks if no errors have been written to error container.
		If not, raises XpMsgException """
		self._errorDict = self._get_errors()
		logger.debug( '_isValid() :: errorDict : %s %s' % (self._errorDict, self._is_business_ok()) )
		if not self._is_business_ok():
			# Here throw the BusinessException
			logger.debug( 'I raise error on business validation!!!!!!!!!!!!!!!!!!' )
			raise XpMsgException(None, _('Error in validating business layer'))

	def _set_ok_msg(self, idOK):
		"""Sets the ok message id"""
		msgDict = _jsf.decodeArray(self._ctx.form.fields['okMessages'].initial)
		self._ctx.form.fields['msg_ok'].initial = msgDict[idOK]
		logger.debug('ok message: %s' % (self._ctx.form.fields['msg_ok'].initial) )

	def _set_cookie(self, key, value):
		"""
		Add key and value to context cookies data.

		** Attributes **

		* ``key``
		* ``value``

		** Returns **

		None
		"""
		self._ctx.set_cookies.append({'key': key, 'value': value, 'domain': settings.SESSION_COOKIE_DOMAIN,
										'expires': datetime.timedelta(days=365*5)+datetime.datetime.utcnow()})

	def _set_main_form(self, form_instance):
		"""Set form as main form: We set to context variable 'form' as add into form container 'forms'.
		@param formInstance: Form instance"""
		self._ctx.form = form_instance
		self._ctx.forms[form_instance.get_form_id()] = form_instance

	def _add_form(self, form_instance):
		"""Set form as regular form. We add to form container 'forms'. Context variable form is not modified.
		@param formInstance: Form instance"""
		self._ctx.forms[form_instance.get_form_id()] = form_instance

	def _put_form_value(self, field_name, field_value, form_id=None):
		"""
		Add form value to field already defined in the forms for the service

		** Required Attributes **

		* ``fieldName`` : field name as appears in form definition
		* ``fieldValue`` : Field value

		** Optional Attributes **

		* ``formId`` : Id for the form ro modify field, like ``signup``. Default value None. In case None,
		we get formId from self._getMainFormId()

		** Returns **

		None
		"""
		if form_id == None:
			form_id = self._get_main_form_id()
		self._ctx.forms[form_id].fields[field_name].initial = field_value

	def _get_user_channel_name(self):
		"""Get user social name"""
		if self._ctx.cookies.has_key('userChannelName'):
			userChannelName = self._ctx.cookies['userChannelName']
			logger.debug( 'COOKIE :: userChannelName: %s' % (userChannelName) )
		else:
			userChannelName = K.USER
			self._set_cookie('userChannelName', userChannelName)
		return userChannelName

	def _login(self):
		"""Do login"""
		login(self.request, self._ctx.user)
		self._ctx.isLogin = True

	def _logout(self):
		"""Do logout"""
		logout(self.request)
		self._ctx.isLogin = False

	def _add_list(self, name, values):
		"""Add name to list_$name in the result JSON object

		** Attributes **

		* ``name``:str
		* ``values``:list<dict>

		** Returns **

		"""
		# TODO: Check option to have values() for queryset and include values() list of dicts in 'list_xxxx'
		dictList = []
		for entry in values:
			dd = {}
			keys = entry.keys()
			for key in keys:
				dd[key] = entry[key]
			dictList.append(dd)
		self._ctx.jsData.addAttr('list_' + name, dictList)

	@service()
	def save(self):
		"""
		Save data associated to form
		"""
		logger.debug('CommonService.save ...')
		self._f().save()

	@service()
	def delete(self):
		"""
		Delete register associated with form
		"""
		logger.debug('CommonService.delete ...')
		instances = {}
		dbObjects = json.loads(self._ctx.post['dbObjects'].replace("'", '"'))
		logger.debug('CommonService.delete :: dbObjects: %s' % (dbObjects) )
		for key in dbObjects:
			# Get instance model by pk
			impl = dbObjects[key]['impl']
			cls = get_class( impl )
			instances[key] = cls.objects.using('default').get(pk=dbObjects[key]['pk'])
		logger.debug('CommonService.delete :: instances: %s' % (instances) )
		if len(instances) == 1:
			instances[instances.keys()[0]].delete()
			logger.debug('CommonService.delete :: deleted instance: %s pk: %s' % (instances.keys()[0], instances[instances.keys()[0]].pk) )
		else:
			# Get instances to delete from button parameters
			# TODO: Include support for deleting more than one instance for forms with multiple instances associated
			pass

	def _get_list_pk_values(self, field_name):
		pks = [int(x) for x in self._ctx.request.getlist(field_name)]
		return pks
	request = property(get_request, set_request, del_request, "service request object")

	def _instances(self, *args):
		"""
		Builds instances list from list of classes. Inyects context.
		
		** Attributes **
		
		* ``*args``: List of class names or path to class names.
		
		** Returns **
		
		List of business, data instances with context inyected
		"""
		instances = get_instances(args, self._ctx_min)
		return instances

class DefaultService ( CommonService ):

	def __init__(self, ctx):
		super(DefaultService, self).__init__(ctx)

	@service(form=DefaultForm)
	def show(self):
		"""Method to execute for view with no business code, only showing a html template."""
		pass
