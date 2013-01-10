import traceback
import string
import simplejson as json
import types
import datetime
import os

from django.http import HttpResponse
from django.core.mail import send_mail
from django.utils.translation import ugettext as _
from django.db.models import Q
from django.contrib.auth.models import User

from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.cache import cache

from business import WorkFlowBusiness
from models import getResultERROR, XpMsgException
from util import TemplateParser

from models import SearchIndex, Context

from data import ParamDAO, ApplicationDAO, TemplateDAO, ViewTmplDAO
from data import MenuParamDAO, ViewMenuDAO, ActionDAO, ServiceMenuDAO
from data import SearchIndexDAO, SearchIndexParamDAO, WordDAO, SearchIndexWordDAO
from ximpia.util import resources
from choices import Choices
import messages

from ximpia.util import ut_email
from models import JsResultDict, ContextDecorator
import constants as K

# Settings
from ximpia.core.util import getClass
from ximpia.site.data import SettingDAO
settings = getClass(os.getenv("DJANGO_SETTINGS_MODULE"))

# Logging
import logging.config
logging.config.dictConfig(settings.LOGGING)
logger = logging.getLogger(__name__)

from data import ViewDAO
#from util import getClass
from forms import DefaultForm

from ximpia.util.js import Form as _jsf

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
	
	def __init__(self, ctx):
		self._ctx = ctx
		if False: self._ctx = ContextDecorator()
		self._resultDict = getResultERROR([])
		self._postDict = ctx.post
		self._errorDict = {}
		self._resultDict = {}
		self._isFormOK = None
		self._wf = WorkFlowBusiness(self._ctx)
		self._viewNameTarget = ''
		self._wfUserId = ''
	
	def _buildJSONResult(self, resultDict):
		"""Builds json result
		@param resultDict: dict : Dictionary with json data
		@return: result : HttpResponse"""
		#logger.debug( 'Dumping...' )
		sResult = json.dumps(resultDict)
		#logger.debug( 'sResult : %s' % (sResult) )
		result = HttpResponse(sResult)
		return result
	
	def _addErrorFields(self, idError, form, errorField):
		"""Add error
		@param idError: String : Id of error
		@param form: Form
		@param errorField: String : The field inside class form"""
		if not self._errorDict.has_key(idError):
			self._errorDict[idError] = {}
		self._errorDict[idError] = form.fields[errorField].initial
	
	def _putFlowParams(self, **args):
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
	
	def _addAttr(self, name, value):
		"""
		Add attribute to jsData response object
		
		**Attributes**
		
		* ``name``
		* ``value``
		
		** Returns **
		
		"""
		self._ctx.jsData.addAttr(name, value)
	
	def _setTargetView(self, viewName):
		"""Set the target view for navigation."""
		self._viewNameTarget = viewName
		self._ctx.viewNameTarget = viewName
	
	def _showView(self, viewName, viewAttrs={}):
		"""Show view.
		@param viewName: 
		@param viewAttrs: 
		@return: result"""
		self._setTargetView(viewName)
		db = ViewDAO(self._ctx)
		viewTarget = db.get(name=viewName)
		impl = viewTarget.implementation
		implFields = impl.split('.')
		method = implFields[len(implFields)-1]
		classPath = ".".join(implFields[:-1])
		cls = getClass( classPath )
		objView = cls(self._ctx) #@UnusedVariable
		if (len(viewAttrs) == 0) :
			result = eval('objView.' + method)()
		else:
			result = eval('objView.' + method)(**viewAttrs)
		
		return result
	
	def _getTargetView(self):
		"""Get target view."""
		return self._viewNameTarget
	
	def _getFlowParams(self, *nameList):
		"""Get parameter for list given, either from workflow dictionary or parameter dictionary in view.
		@param nameList: List of parameters to fetch"""
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
	
	def _getWFUser(self):
		"""Get Workflow user."""
		if self._ctx.cookies.has_key('wfUserId'):
			self._ctx.wfUserId = self._ctx.cookies['wfUserId']
		else:
			self._ctx.wfUserId = self._wf.genUserId()
			self._setCookie('wfUserId', self._ctx.wfUserId)
		self._wfUserId = self._ctx.wfUserId
		return self._wfUserId
	
	def _getErrorResultDict(self, errorDict, pageError=False):
		"""Get sorted error list to show in pop-up window
		@return: self._resultDict : ResultDict"""
		#dict = self._errorDict
		keyList = errorDict.keys()
		keyList.sort()
		myList = []
		for key in keyList:
			message = errorDict[key]
			index = key.find('id_')
			if pageError == False:
				if index == -1:
					myList.append(('id_' + key, message, False))
				else:
					myList.append((key, message, False))
			else:
				if index == -1:
					myList.append(('id_' + key, message, True))
				else:
					myList.append((key, message, True))
		self._resultDict = getResultERROR(myList)
		return self._resultDict

	def _doValidations(self, validationDict):
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
			result = self._buildJSONResult(self._getErrorResultDict())
			return result"""
	
	def _getForm(self):
		"""Get form"""
		#logger.debug( 'form: %s' % (self._ctx.form) )
		return self._ctx.form
	
	def _setForm(self, formInstance):
		"""Sets the form instance"""
		self._ctx.form = formInstance
		self._isFormOK = self._ctx.form.is_valid()
	
	def _getPostDict(self):
		"""Get post dictionary. This will hold data even if form is not validated. If not validated cleaned_value will have no values"""
		return self._postDict
	
	def _isBusinessOK(self):
		"""Checks that no errors have been generated in the validation methods
		@return: isOK : boolean"""
		if len(self._errorDict) == 0:
			self._businessOK = True
		return self._businessOK
	
	def _isFormValid(self):
		"""Is form valid?"""
		if self._isFormOK == None:
			self._isFormOK = self._ctx.form.is_valid()
		return self._isFormOK

	def _isFormBsOK(self):
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
	
	def _addError(self, fieldName, errMsg):
		"""Add error
		@param idError: String : Id of error
		@param form: Form
		@param errorField: String : The field inside class form"""
		#form = self._getForm()
		#logger.debug( 'form: %s' % (form) )
		#msgDict = _jsf.decodeArray(form.fields['errorMessages'].initial)
		idError = 'id_' + fieldName
		if not self._errorDict.has_key(idError):
			self._errorDict[idError] = {}
		self._errorDict[idError] = errMsg
		logger.debug( '_errorDict : %s' % (self._errorDict) )

	def _getErrors(self):
		"""Get error dict
		@return: errorDict : Dictionary"""
		return self._errorDict	

	def _getPost(self):
		"""Get post dictionary"""
		return self._ctx.post
	
	def _validateExists(self, dbDataList):
		"""Validates that db data provided exists. Error is shown in case does not exist.
		Db data contains data instance, query arguments in a dictionary
		and errorName for error message display at the front
		@param dbDataList: [dbObj, queryArgs, fieldName, errMsg]"""
		logger.debug( 'validateExists...' )
		logger.debug( 'dbDataList : %s' % (dbDataList) )
		for dbData in dbDataList:
			dbObj, qArgs, fieldName, errMsg = dbData
			exists = dbObj.check(**qArgs)
			logger.debug( 'validate Exists Data: args: %s exists: %s fieldName: %s errMsg: %s' % 
						(qArgs, str(exists), str(fieldName) + str(errMsg)) )
			if not exists:
				self._addError(fieldName, errMsg)
	
	def _validateNotExists(self, dbDataList):
		"""Validates that db data provided does not exist. Error is shown in case exists.
		Db data contains data instance, query arguments in a dictionary
		and errorName for error message display at the front
		@param dbDataList: [dbObj, queryArgs, fieldName, errMsg]"""
		logger.debug( 'validateNotExists...' )
		logger.debug( 'dbDataList : %s' % (dbDataList) )
		for dbData in dbDataList:
			dbObj, qArgs, fieldName, errMsg = dbData
			exists = dbObj.check(**qArgs)
			logger.debug( 'Exists : %s' % (exists) )
			if exists:
				logger.debug( 'I add error: %s %s' % (fieldName, errMsg) )
				self._addError(fieldName, errMsg)
		
	def _validateContext(self, ctxDataList):
		"""Validates context variable. [[name, value, fieldName, errName],...]"""
		for ctxData in ctxDataList:
			name, value, fieldName, errMsg = ctxData
			if self._ctx[name] != value:
				self._addError(fieldName, errMsg)
			
	def _authenticateUser(self, ximpiaId, password, fieldName, errorMsg):
		"""Authenticates user and password"""
		qArgs = {'username': ximpiaId, 'password': password}
		user = authenticate(**qArgs)
		if user:
			pass
		else:
			self._addError(fieldName, errorMsg)
		return user
	
	def _authenticateUserSocNet(self, ximpiaId, token, authSource, fieldName, errorMsg):
		"""Authenticates user and password"""
		qArgs = {'username': ximpiaId, 'token': token}
		user = authenticate(**qArgs)
		if user:
			pass
		else:
			self._addError(fieldName, errorMsg)
		return user
		
	def _isValid(self):
		"""Checks if no errors have been written to error container.
		If not, raises XpMsgException """
		self._errorDict = self._getErrors()
		logger.debug( '_isValid() :: errorDict : %s %s' % (self._errorDict, self._isBusinessOK()) )
		if not self._isBusinessOK():
			# Here throw the BusinessException
			logger.debug( 'I raise error on business validation!!!!!!!!!!!!!!!!!!' )
			raise XpMsgException(None, _('Error in validating business layer'))

	def _setOkMsg(self, idOK):
		"""Sets the ok message id"""
		msgDict = _jsf.decodeArray(self._ctx.form.fields['okMessages'].initial)
		self._ctx.form.fields['msg_ok'].initial = msgDict[idOK]
		logger.debug('ok message: %s' % (self._ctx.form.fields['msg_ok'].initial) )
	
	def _setCookie(self, key, value):
		"""Add to context cookies data. Decorators that build response will set cookie into respose object
		@param key: Key
		@param value: Value"""
		self._ctx.set_cookies.append({'key': key, 'value': value, 'domain': settings.SESSION_COOKIE_DOMAIN, 'expires': datetime.timedelta(days=365*5)+datetime.datetime.utcnow()})

	def _setMainForm(self, formInstance):
		"""Set form as main form: We set to context variable 'form' as add into form container 'forms'.
		@param formInstance: Form instance"""
		self._ctx.form = formInstance
		self._ctx.forms[formInstance.getFormId()] = formInstance
	
	def _addForm(self, formInstance):
		"""Set form as regular form. We add to form container 'forms'. Context variable form is not modified.
		@param formInstance: Form instance"""
		self._ctx.forms[formInstance.getFormId()] = formInstance
	
	def _getUserChannelName(self):
		"""Get user social name"""
		if self._ctx.cookies.has_key('userChannelName'):
			userChannelName = self._ctx.cookies['userChannelName']
			logger.debug( 'COOKIE :: userChannelName: %s' % (userChannelName) )
		else:
			userChannelName = K.USER
			self._setCookie('userChannelName', userChannelName)
		return userChannelName
	
	def _login(self):
		"""Do login"""
		login(self._ctx.rawRequest, self._ctx.user)
		self._ctx.isLogin = True
	
	def _logout(self):
		"""Do logout"""
		logout(self._ctx.rawRequest)
		self._ctx.isLogin = False
	
	def _addList(self, name, values):
		"""Add name to list_$name in the result JSON object"""
		dictList = []
		for entry in values:
			dd = {}
			keys = entry.keys()
			for key in keys:
				dd[key] = entry[key]
			dictList.append(dd)
		self._ctx.jsData.addAttr('list_' + name, dictList)	

class EmailService(object):
	#python -m smtpd -n -c DebuggingServer localhost:1025
	@staticmethod
	def send(xmlMessage, subsDict, fromAddr, recipientList):
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
		subject, message = ut_email.getMessage(xmlMessage)
		message = string.Template(message).substitute(**subsDict)
		#logger.debug( message )
		send_mail(subject, message, fromAddr, recipientList)


# ****************************************************
# **                DECORATORS                      **
# ****************************************************

class ServiceDecorator(object):
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
		#logger.debug( 'ServiceDecorator :: argsDict: %s argsTuple: %s' % (argsDict, argsTuple) )
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
			logger.debug( 'ServiceDecorator :: data: %s %s' % (argsTuple, argsDict) )
			try:
				self._isServerTmpl = obj._ctx.isServerTmpl
				logger.debug('ServiceDecorator :: isServerTmpl: %s' % (self._isServerTmpl) )
				#logger.debug( 'ServiceDecorator :: ctx: %s' % (obj._ctx.keys()) ) 
				obj._ctx.jsData = JsResultDict()
				if self._form != None:
					#obj._ctx.form = self._form()
					obj._setMainForm(self._form())
				f(*argsTuple, **argsDict)
				if not obj._ctx.doneResult:
					# Instances
					dbApp = ApplicationDAO(obj._ctx)
					# Menu
					logger.debug( 'ServiceDecorator :: viewNameTarget: %s' % (str(obj._ctx.viewNameTarget)) )
					logger.debug( 'ServiceDecorator :: viewNameSource: %s' % (str(obj._ctx.viewNameSource)) )
					if len(obj._ctx.viewNameTarget) > 1:
						viewName = obj._ctx.viewNameTarget
					else:
						viewName = obj._ctx.viewNameSource
					logger.debug( 'ServiceDecorator :: viewName: %s' % (viewName) )
					menu = MenuService(obj._ctx)
					menuDict = menu.getMenus(viewName)
					#menuDict = menu.getMenus('home')
					obj._ctx.jsData['response']['menus'] = menuDict
					# Views
					"""if obj._ctx['viewNameTarget'] != '':
						obj._ctx.jsData['response']['view'] = obj._ctx.viewNameTarget
					else:
						obj._ctx.jsData['response']['view'] = obj._ctx.viewNameSource"""
					obj._ctx.jsData['response']['view'] = viewName
					logger.debug( 'ServiceDecorator :: view: %s' % ('*' + str(obj._ctx.jsData['response']['view']) + '*') )
					# App
					obj._ctx.jsData['response']['app'] = obj._ctx.app
					obj._ctx.jsData['response']['appSlug'] = dbApp.get(name=obj._ctx.app).slug
					# winType
					if len(obj._ctx.jsData['response']['view'].strip()) != 0:
						dbView = ViewDAO(obj._ctx)
						view = dbView.get(application__name=obj._ctx.app, name=obj._ctx.jsData['response']['view'])
						logger.debug( 'ServiceDecorator :: winType: %s' % (str(view.winType)) )
						obj._ctx.jsData['response']['winType'] = view.winType
						obj._ctx.jsData['response']['viewSlug'] = view.slug
						# Authenticate view (if requires login and user is not logged in, raise error)
						if not obj._ctx.user.is_authenticated() and view.hasAuth:
							raise XpMsgException(None, messages.ERR_NOT_LOGGED_IN % (view.slug))
					# User authenticate and session
					logger.debug('ServiceDecorator :: User: %s' % (obj._ctx.user) )
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
							logger.debug( 'ServiceDecorator :: tmplName: %s' % (tmplName) )
						else:
							raise XpMsgException(None, _('Error in resolving template for view'))
						obj._ctx.jsData['response']['tmpl'] = templates
					else:
						# In case we show only msg with no view, no template
						logger.debug( 'ServiceDecorator :: no View, no template...' )
						obj._ctx.jsData['response']['tmpl'] = ''
					# Forms
					logger.debug( 'ServiceDecorator :: forms: %s' % (obj._ctx.forms) )
					for formId in obj._ctx.forms:
						form = obj._ctx.forms[formId]
						if not obj._ctx.jsData.has_key(formId):							
							form.buildJsData(obj._ctx.app, obj._ctx.jsData)
						logger.debug( 'ServiceDecorator :: form: %s app: %s' % (formId, form.base_fields['app'].initial) )
					#logger.debug( 'ServiceDecorator :: response keys : %s' % (obj._ctx.jsData['response'].keys()) )
					# Result
					#logger.debug( 'ServiceDecorator :: isServerTmpl: %s' % (self._isServerTmpl) )
					# Settings
					if not obj._ctx.jsData['response'].has_key('settings'):
						obj._ctx.jsData['response']['settings'] = {}
					# Get settings with mustAutoLoad=true for global and for this app
					dbSetting = SettingDAO(obj._ctx, relatedDepth=1)
					settingsApp = dbSetting.searchSettings(obj._ctx.app)
					for setting in settingsApp: 
						try:
							value = eval(setting.value)
						except NameError:
							value = setting.value
						obj._ctx.jsData['response']['settings'][setting.name.name] = value
					if self._isServerTmpl == False:
						result = obj._buildJSONResult(obj._ctx.jsData)
						#logger.debug( obj._ctx.jsData )
						################# Print response
						logger.debug('')
						logger.debug( 'ServiceDecorator :: #################### RESPONSE ##################' )
						#logger.debug( 'ServiceDecorator :: response keys: %s' % (obj._ctx.jsData['response'].keys()) )
						keys = obj._ctx.jsData['response'].keys()
						for key in keys:
							keyValue = obj._ctx.jsData['response'][key]
							#logger.debug( 'key: %s' % (key, type(keyValue)) )
							if type(keyValue) == types.DictType and keyValue.has_key('value'):
								logger.debug( 'ServiceDecorator :: response %s : %s' % (key, str(keyValue['value'])) )								
							elif type(keyValue) != types.DictType:
								logger.debug( 'ServiceDecorator :: response %s: %s' % (key, str(keyValue)) )
							else:
								for newKey in keyValue:
									#logger.debug( 'newKey: ', newKey )
									#logger.debug( keyValue[newKey] )
									if type(keyValue[newKey]) == types.DictType and keyValue[newKey].has_key('value'):
										logger.debug( 'ServiceDecorator :: response %s %s: %s' % (key, newKey, str(keyValue[newKey]['value'])) )
									elif type(keyValue[newKey]) != types.DictType:
										logger.debug( 'ServiceDecorator :: response %s %s: %s' %  (key, newKey, str(keyValue[newKey])) )
									
						################# Print response
						logger.debug( 'ServiceDecorator :: #################### RESPONSE ##################' )
						logger.debug( '' )
						for cookie in obj._ctx.set_cookies:
							maxAge = 5*12*30*24*60*60
							result.set_cookie(cookie['key'], value=cookie['value'], domain=cookie['domain'], 
									expires = cookie['expires'], max_age=maxAge)
							logger.debug( 'ServiceDecorator :: Did set cookie into result... %s' % (cookie) )
					else:
						result = obj._ctx.jsData
						#logger.debug( result )
						################# Print response
						logger.debug( '' )
						logger.debug( 'ServiceDecorator :: #################### RESPONSE ##################' )
						#logger.debug( 'ServiceDecorator :: response keys: %s' % (obj._ctx.jsData['response'].keys()) )
						keys = obj._ctx.jsData['response'].keys()
						for key in keys:
							keyValue = obj._ctx.jsData['response'][key]
							#logger.debug( 'key: ', key, type(keyValue) )
							if type(keyValue) == types.DictType and keyValue.has_key('value'):
								logger.debug( 'ServiceDecorator :: response %s: %s' % (key, str(keyValue['value'])) )								
							elif type(keyValue) != types.DictType:
								logger.debug( 'ServiceDecorator :: response %s: %s' % (key, str(keyValue)) )
							else:
								for newKey in keyValue:
									#logger.debug( 'newKey: %s' % (newKey) )
									#logger.debug( keyValue[newKey] )
									if type(keyValue[newKey]) == types.DictType and keyValue[newKey].has_key('value'):
										logger.debug( 'ServiceDecorator :: response %s %s: %s' % (key, newKey, str(keyValue[newKey]['value'])) )
									elif type(keyValue[newKey]) != types.DictType:
										logger.debug( 'ServiceDecorator :: response %s %s: %s' % (key, newKey, str(keyValue[newKey])) )
									
						################# Print response
						logger.debug( 'ServiceDecorator :: #################### RESPONSE ##################' )
						logger.debug( '' )
						logger.debug( obj._ctx.jsData['response'].keys() )
					#obj._ctx['_doneResult'] = True
					obj._ctx.doneResult = True
				else:
					logger.debug( 'ServiceDecorator :: I skip building response, since I already did it!!!!!' )
					if self._isServerTmpl == False:
						result = obj._buildJSONResult(obj._ctx.jsData)
					else:
						result = obj._ctx.jsData
				return result
			except XpMsgException as e:
				logger.debug( 'ServiceDecorator :: ERROR!!!! ServiceDecorator!!!!!' )
				errorDict = obj._getErrors()
				if len(errorDict) != 0:
					if self._isServerTmpl == False:
						result = obj._buildJSONResult(obj._getErrorResultDict(errorDict, pageError=self._pageError))
					else:
						result = obj._getErrorResultDict(errorDict, pageError=self._pageError)
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

class ValidationDecorator(object):
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
			obj._isValid()
		return wrapped_f

class ValidateFormDecorator(object):
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
			#logger.debug( 'ValidateFormDecorator :: %s %s' % (argsTuple, argsDict) )
			obj = argsTuple[0]
			#result = f(*argsTuple, **argsDict)
			obj._ctx.jsData = JsResultDict()
			obj._ctx.form = self._form(obj._ctx.post, ctx=obj._ctx)
			bForm = obj._ctx.form.is_valid()
			#obj._ctx.form = obj._f
			#logger.debug( 'ValidateFormDecorator :: Form Validation: %s' % (bForm) )
			if bForm == True:
				obj._setMainForm(obj._ctx.form)
				result = f(*argsTuple, **argsDict)
				return result
				"""try:
					f(*argsTuple, **argsDict)
					obj._f.buildJsData(obj._ctx.jsData)
					result = obj.buildJSONResult(obj._ctx.jsData)
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
						result = obj.buildJSONResult(obj.getErrorResultDict(errorDict, pageError=self._pageError))
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
					result = obj._buildJSONResult(obj._getErrorResultDict(errorDict, pageError=True))
				else:
					#errorDict = {'': 'Error validating your data. Check it out and send again'}
					# Build errordict
					errorDict = {}
					for field in obj._ctx.form.errors:
						if field != '__all__':
							errorDict[field] = obj._ctx.form.errors[field][0]
					logger.debug( 'errorDict: %s' % (errorDict) )
					result = obj._buildJSONResult(obj._getErrorResultDict(errorDict, pageError=False))
				return result
		return wrapped_f

class WFViewDecorator( object ):
	
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
			logger.debug( 'WFViewDecorator :: flowCode: %s' % (self.__flowCode) )
			flow = obj._wf.get(self.__flowCode)
			viewName = obj._ctx.viewNameSource
			logger.debug( 'WFViewDecorator :: View Current: %s' % (obj._ctx.viewNameSource) )
			# WorKflow User Id
			"""if obj._ctx.cookies.has_key('wfUserId'):
				obj._ctx.wfUserId = obj._ctx.cookies['wfUserId']
				logger.debug( 'WFViewDecorator :: COOKIE :: WF User Id: %s' % (obj._ctx.wfUserId) )
			else:
				obj._ctx.wfUserId = obj._wf.genUserId()
				obj._setCookie('wfUserId', obj._ctx.wfUserId)
				logger.debug( 'WFViewDecorator :: WF UserId: %s' % (obj._ctx.wfUserId) )"""
			obj._ctx.wfUserId = obj._getWFUser()
			logger.debug( 'WFViewDecorator :: WF UserId: %s' % (obj._ctx.wfUserId) )
			hasFlow = True
			try:
				flowData = obj._wf.getFlowDataDict(obj._ctx.wfUserId, self.__flowCode)
				logger.debug( 'WFViewDecorator :: flowData: %s' % (flowData) )
			except XpMsgException:
				hasFlow = False
			logger.debug( 'WFViewDecorator :: hasFlow: %s' % (hasFlow) )
			if flow.jumpToView == True and hasFlow == True:
				# Get flow data, display view in flow data
				try:
					viewName = obj._wf.getView(obj._ctx.wfUserId, self.__flowCode)
					logger.debug( 'WFViewDecorator :: Jump to View: %s %s' % (obj._ctx.viewNameSource, viewName) )
				except XpMsgException:
					pass
			else:
				isFirstView = obj._wf.isFirstView(self.__flowCode, obj._ctx.viewNameSource)
				logger.debug( 'WFViewDecorator :: Flow Data: %s %s' % (hasFlow, isFirstView) )
				# Check that this view is first in flow
				if hasFlow == False and isFirstView == True:
					logger.debug( 'WFViewDecorator :: reset Flow... no flow and first window' )
					obj._wf.resetFlow(obj._ctx.wfUserId, self.__flowCode, obj._ctx.viewNameSource)
				elif isFirstView == True and flow.resetStart == True:
					logger.debug( 'WFViewDecorator :: reset Flow... resetStart=True and first view in flow...' )
					obj._wf.resetFlow(obj._ctx.wfUserId, self.__flowCode, obj._ctx.viewNameSource)
			obj._ctx.viewNameTarget = viewName
			# Jump to View in case jumpToView = True and viewName resolved from flow is different from current view
			#logger.debug( 'WFViewDecorator :: Jumps... %s %s' % (viewName, obj._ctx.viewNameSource) )
			if viewName != obj._ctx.viewNameSource:
				logger.debug( 'WFViewDecorator :: redirect to ... %s' % (viewName) )				
				dbView = ViewDAO(obj._ctx)
				view = dbView.get(name=viewName)
				viewAttrs = obj._wf.getViewParams(self.__flowCode, viewName)
				# Show View
				impl = view.implementation
				implFields = impl.split('.')
				method = implFields[len(implFields)-1]
				classPath = ".".join(implFields[:-1])
				cls = getClass( classPath )
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

class MenuActionDecorator(object):
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
			cls = getClass( classPath )
			objView = cls(obj._ctx) #@UnusedVariable
			result = eval('objView.' + method)()			
			return result
		return wrapped_f

class WFActionDecorator(object):
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
				#logger.debug( 'WFActionDecorator :: flowCode: %s' % (obj._ctx.flowCode) )
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
				cls = getClass( classPath )
				objView = cls(obj._ctx) #@UnusedVariable
				if (len(viewAttrs) == 0) :
					result = eval('objView.' + method)()
				else:
					result = eval('objView.' + method)(**viewAttrs)
			except XpMsgException as e:
				logger.debug( 'ERROR!!!! WFActionDecorator!!!!!' )
				errorDict = obj._getErrors()
				if len(errorDict) != 0:
					result = obj._buildJSONResult(obj._getErrorResultDict(errorDict, pageError=True))
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

class ViewOldDecorator ( object ):
	""""Old"""
	__viewName = ''
	__APP = ''
	def __init__(self, appCode, viewName, *argsTuple, **argsDict):
		self.__APP = appCode
		self.__viewName = viewName
	def __call__(self, f):
		"""Decorator call method"""
		def wrapped_f(*argsTuple, **args):
			request = argsTuple[0]
			args['ctx'].viewNameSource = self.__viewName
			resultJs = f(*argsTuple, **args)
			#logger.debug( 'resultJs: %s' % (resultJs) )
			template = TemplateService(args['ctx'])
			templates = template.resolve(self.__viewName)
			if templates.has_key(self.__viewName):
				tmplName = templates[self.__viewName]
				#logger.debug( 'tmplName: %s' % (tmplName) )
				result = render_to_response( self.__APP + '/' + tmplName + '.html', RequestContext(request, 
													{	'result': json.dumps(resultJs),
														'settings': settings
													}))
			else:
				raise XpMsgException(None, _('Error in resolving template for view'))
			return result
		return wrapped_f

class ViewTmplDecorator ( object ):
	""""Decorator for django views in core module."""
	__viewName = ''
	__APP = ''
	__APP_OBJ = None
	__APP_SLUG = ''
	_settings = {}
	def __init__(self, *argsTuple, **argsDict):
		if len(argsTuple) != 0:
			logger.debug('ViewTmplDecorator :: argList: %s' % (argsTuple) )
			self.__APP = '.'.join(argsTuple[0].split('.')[:2])
	def __call__(self, f):
		"""Decorator call method"""
		def wrapped_f(request, **args):
			
			logger.debug( 'ViewTmplDecorator :: args: %s' % args )
			
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
					logger.debug( 'ViewTmplDecorator :: set from args view name' )
					view = dbView.get(slug=args['viewSlug'])
					logger.debug('ViewTmplDecorator :: viewName: %s' % (view.name) )
					self.__viewName = view.name
				else:
					self.__viewName = ''
			else:
				# TODO: Use here the default app for project settings and default view...
				#self.__APP = 'ximpia.site'
				self.__viewName = 'home'
			logger.debug('ViewTmplDecorator :: app: %s' % (self.__APP) )
			ctx.viewNameSource = self.__viewName
			resultJs = f(request, **args)
			if len(ctx.viewNameTarget) != 0:
				self.__viewName = ctx.viewNameTarget
			logger.debug( 'ViewTmplDecorator :: resultJs: %s' % resultJs )
			logger.debug( 'ViewTmplDecorator :: viewName: %s target: %s source: %s ' % 
				(self.__viewName, args['ctx'].viewNameTarget, args['ctx'].viewNameSource) )
			template = TemplateService(ctx)
			templates = template.resolve(self.__viewName)
			logger.debug( 'ViewTmplDecorator :: templates: %s' % templates )
			if templates.has_key(self.__viewName):
				tmplName = templates[self.__viewName]
				logger.debug( 'ViewTmplDecorator :: tmplName: %s' % tmplName )
				# Get template data
				tmplService = TemplateService(ctx)
				tmplData = tmplService.get(self.__APP, 'window', tmplName)
				#logger.debug('ViewTmplDecorator :: tmplData: %s' % (tmplData) )
				parser = TemplateParser()
				parser.feed(tmplData)
				try:
					logger.debug('ViewTmplDecorator :: title: %s' % (parser.title) )
					result = render_to_response( 'main.html', RequestContext(request, 
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
														'appSlug': self.__APP_SLUG
													}))
				except AttributeError as e:
					raise XpMsgException(e, _('Error in getting attributes from template. Check that title, titleBar, content and bottom button area exists.'))
				#result = result.replace('{{result}}', json.dumps(resultJs))
			else:
				raise XpMsgException(None, _('Error in resolving template for view %s' % (self.__viewName) ))			
			
			return result
		return wrapped_f

class ViewDecorator ( object ):
	"""
	
	Decorator for ximpia views
	
	"""
	
	__form = None
	
	def __init__(self, form):
		self.__form = form

	def __call__(self, f):
		"""Decorator call method"""
		@ServiceDecorator(form=self.__form)
		def wrapped_f(request, *argsTuple, **argsDict):
			result = f(request, *argsTuple, **argsDict)			
			return result
		return wrapped_f

class ActionDecorator ( object ):
	"""
	
	Decorator for ximpia actions
	
	"""
	
	__form = None
	
	def __init__(self, form):
		self.__form = form

	def __call__(self, f):
		"""Decorator call method"""		
		@ValidateFormDecorator(self.__form)
		@ServiceDecorator()
		def wrapped_f(request, *argsTuple, **argsDict):
			logger.debug('ActionDecorator :: form: %s' % self.__form)
			result = f(request, *argsTuple, **argsDict)			
			return result
		return wrapped_f

class WorkflowViewDecorator ( object ):
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
		@WFViewDecorator(self.__flowCode)
		@ServiceDecorator(form = self.__form)
		def wrapped_f(request, *argsTuple, **argsDict):
			logger.debug('WorkflowViewDecorator :: flowCode: %s form: %s' % (self.__flowCode, self.__form))
			result = f(request, *argsTuple, **argsDict)			
			return result
		return wrapped_f

class WorkflowActionDecorator ( object ):
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
		@ValidateFormDecorator(self.__form)
		@WFActionDecorator()
		def wrapped_f(request, *argsTuple, **argsDict):
			logger.debug('WorkflowActionDecorator :: form: %s' % (self.__form) )
			result = f(request, *argsTuple, **argsDict)			
			return result
		return wrapped_f

class MenuService( object ):
	_ctx = None
	def __init__(self, ctx):
		"""Menu building and operations"""
		self._ctx = ctx
		"""self._dbViewMenu = ViewMenuDAO(self._ctx, relatedDepth=3)
		self._dbView = ViewDAO(self._ctx, relatedDepth=2)
		self._dbMenuParam = MenuParamDAO(self._ctx, relatedDepth=3)"""
		#self._dbAppAccess = ApplicationAccessDAO(self._ctx)
	
	def __getList(self, menuDict, menuList):
		"""
		Append menu dictionary to list of menu items
		
		**Attributes**
		
		* ``menuDict`` : Menu data in dictionary format with atributes about menu item attributes
		* ``menuList`` : Queryset with menu items
		
		**Returns**
		
		None
		"""
		container = {}
		for viewMenu in menuList:
			#logger.debug( 'getMenus :: viewMenu: %s' % (viewMenu) )
			#logger.debug( 'getMenus :: action: %s' % (viewMenu.menu.action) )
			#logger.debug( 'getMenus :: view: %s' % (viewMenu.menu.view) )
			menuObj = {}
			if viewMenu.menu.view != None:
				menuObj['service'] = viewMenu.menu.view.service.name
			if viewMenu.menu.action != None:
				menuObj['service'] = viewMenu.menu.action.service.name
			menuObj['action'] = viewMenu.menu.action.name if viewMenu.menu.action != None else ''
			menuObj['view'] = viewMenu.menu.view.name if viewMenu.menu.view != None else ''
			menuObj['viewSlug'] = viewMenu.menu.view.slug if viewMenu.menu.view != None else ''
			if viewMenu.menu.view != None and viewMenu.menu.view.image != None:
				menuObj['image'] = viewMenu.menu.view.image
			else:
				menuObj['image'] = ''
			menuObj['winType'] = viewMenu.menu.view.winType if viewMenu.menu.view != None else ''
			menuObj['sep'] = viewMenu.hasSeparator
			menuObj['name'] = viewMenu.menu.name
			menuObj['title'] = viewMenu.menu.title
			menuObj['description'] = viewMenu.menu.description
			menuObj['icon'] = viewMenu.menu.icon.value if viewMenu.menu.icon != None else ''
			menuObj['zone'] = viewMenu.zone
			if viewMenu.menu.view != None:
				menuObj['app'] = viewMenu.menu.view.application.name
				menuObj['appSlug'] = viewMenu.menu.view.application.slug
			elif viewMenu.menu.action != None:
				menuObj['app'] = viewMenu.menu.action.application.name
				menuObj['appSlug'] = viewMenu.menu.action.application.slug
			# params
			params = self._dbMenuParam.search(menu=viewMenu.menu)
			paramDict = {}
			# name, operator, value
			for param in params:
				if param.operator == Choices.OP_EQ:
					paramDict[param.name] = param.value
			menuObj['params'] = paramDict
			container[viewMenu.menu.name] = menuObj
			if viewMenu.menu.view != None:
				menuObj['isCurrent'] = True if viewMenu.menu.view.name == self.__viewName else False
			#logger.debug( 'menuObj: %s' % (menuObj) )
			if viewMenu.parent == None:
				menuObj['items'] = []
				menuDict[viewMenu.zone].append(menuObj)
				"""if viewMenu.zone in ['sys','main']:
					if self._ctx.isLogin:
						menuDict[viewMenu.zone].append(menuObj)
					else:
						if viewMenu.menu.name == 'home':
							menuDict[viewMenu.zone].append(menuObj) 
				else:
					menuDict[viewMenu.zone].append(menuObj)"""
			else:
				parentMenuObj = container[viewMenu.parent.menu.name]
				parentMenuObj['items'].append(menuObj)
		logger.debug( 'getMenus :: menuDict: %s' % (menuDict) )
	
	def getMenus(self, viewName):
		"""
		Build menus in dictionary format
		
		**Attributes**
		
		* ``viewName`` : View name
		
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
								'isCurrent' : BooleanType
							}
			],
			'view': [...]
		}
		
		items value will be a list of dictionaries with menu dict keys (action, view, etc..)
		
		params have format key -> value as normal dictionaries.
		"""
		self.__viewName = viewName
		# db instances
		self._dbView = ViewDAO(self._ctx, relatedDepth=2)
		self._dbViewMenu = ViewMenuDAO(self._ctx, relatedDepth=3)
		self._dbServiceMenu = ServiceMenuDAO(self._ctx, relatedDepth=3)
		self._dbMenuParam = MenuParamDAO(self._ctx, relatedDepth=3)
		# logic		
		logger.debug( 'getMenus...' )
		logger.debug( 'getMenus :: appName: %s' % (self._ctx.app) )
		view = self._dbView.get(name=viewName, application__name=self._ctx.app)
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
		
		# TODO: Get main and sys without link, from settings
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
		self.__getList(menuDict, menuList)
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
		logger.debug('menuList: %s' % (menuList) )
		self.__getList(menuDict, menuList)
		return menuDict

class SearchService ( object ):
	_ctx = None
	def __init__(self, ctx):
		"""Search index operations"""
		self._ctx = ctx
		self._dbApp = ApplicationDAO(self._ctx)
		self._dbView = ViewDAO(self._ctx, relatedDepth=2)
		self._dbAction = ActionDAO(self._ctx, relatedDepth=2)
		self._dbSearch = SearchIndexDAO(self._ctx, relatedDepth=3)
		self._dbIndexWord = SearchIndexWordDAO(self._ctx, relatedDepth=2)
		self._dbWord = WordDAO(self._ctx)
		self._dbIndexParam = SearchIndexParamDAO(self._ctx, relatedDepth=3)
		self._dbParam = ParamDAO(self._ctx)
	def addIndex(self, text, appCode, viewName=None, actionName=None, params={}):
		"""Add data to search index"""
		wordList = resources.Index.parseText(text)
		view = self._dbView.get(name=viewName) if viewName != None else None
		action = self._dbAction.get(name=actionName) if actionName != None else None
		app = self._dbApp.get(code=appCode)
		# delete search index
		try:
			search = self._dbSearch.get(application=app, view=view) if viewName != '' else (None, None) 
			search = self._dbSearch.get(application=app, action=action) if actionName != '' else (None, None)
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
		@param text: text to search
		@return: results : List of dictionaries with "id", "text", "image" and "extra" fields."""
		# Search first 100 matches
		# return best 15 matches with titile, link information and application icon
		# return results in format needed by autocomplete plugin
		wordList = resources.Index.parseText(text)
		logger.debug( 'wordList: %s' % (wordList) )
		#results = self._dbIndexWord.search(word__word__in=wordList)[:100]
		# Build Q instance
		myQ = Q(word__word__startswith=wordList[0])
		for word in wordList[1:]:
			myQ = myQ | Q(word__word__startswith=word)
		logger.debug( 'Q: %s' % (str(myQ)) )
		results = self._dbIndexWord.search(myQ)[:100]
		logger.debug( 'search :: results: %s' % (results) )
		logger.debug( results.query )
		container = {}
		containerData = {}
		for data in results:
			logger.debug( 'data: %s' % (data) )
			if not container.has_key(data.index.pk):
				container[data.index.pk] = 0
			container[data.index.pk] += 1
			#container[data.index.pk] += 1 if container.has_key(data.index.pk) else 1
			containerData[data.index.pk] = data
		logger.debug( 'conatiner: %s' % (container) )
		logger.debug( 'containerData: %s' % (containerData) )
		tupleList = []
		for pk in container:
			tupleList.append((container[pk], containerData[pk]))
		tupleList.sort()
		tupleListFinal = tupleList[:15]
		resultsFinal = []
		for theTuple in tupleListFinal:
			data = theTuple[1]
			myDict = {}
			myDict['id'] = data.index.id
			myDict['text'] = data.index.title
			myDict['image'] = ''
			extraDict = {}
			extraDict['view'] = data.index.view.name if data.index.view != None else ''
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
	def searchOld(self, text):
		"""Search for views and actions
		@param text: text to search
		@return: results : List of dictionaries with "id", "text", "image" and "extra" fields."""
		results = self._dbSearch.search(title__icontains=text)[:15]
		logger.debug( 'search :: results: %s' % (results) )
		resultsFinal = []
		for data in results:
			myDict = {}
			myDict['id'] = data.id
			myDict['text'] = data.title
			myDict['image'] = ''
			extraDict = {}
			extraDict['view'] = data.view.name if data.view != None else ''
			extraDict['action'] = data.action.name if data.action != None else ''
			params = data.params.all()
			paramDict = {}
			for param in params:
				paramDict[param.name] = param.value
			extraDict['params'] = paramDict
			extraDict['app'] = data.application.name
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
		self._dbViewTmpl = ViewTmplDAO(self._ctx, relatedDepth=2)
		self._dbTemplate = TemplateDAO(self._ctx)
	def __findTemplPath(self, module):
		"""
		Find template searching on templates/ directory in application
		
		**Attributes**
		
		* ``module``:Object : Application module. For app='ximpia.site', module would be same as from ximpia import site
		* ``mode``:String : window or popup
		
		**Returns**
		
		* ``path``:String : Path to template
		"""
		#path = m.__file__.split('__init__')[0] + 'templates/' + mode + '/' + tmplName + '.html'
		path = ''
		pathMain = module.__file__.split('__init__')[0] + 'templates'
		fileList = os.listdir(pathMain)
		for item in fileList:
			if item != 'site':
				if item in self.__MODES:
					fileList = os.listdir(pathMain + '/' + item)
					for file in fileList:
						if file == self.__tmplName + '.html':
							path = pathMain + '/' + item + '/' + file
							break
				else:
					if os.path.exists(pathMain + '/' + item + '/' + self.__mode):
						fileList = os.listdir(pathMain + '/' + item + '/' + self.__mode)
						for file in fileList:
							if file == self.__tmplName + '.html':
								path = pathMain + '/' + item + '/' + self.__mode + '/' +  file
								break
					else:
						raise XpMsgException(None, _('Template directory has no ' + ' or '.join(self.__MODES) + ' modes') )
			if path != '':
				break
		if path == '':
			raise XpMsgException(None, _('Could not obtaine template file for applciation=%s, mode=%s, templName=%s' %\
										 (self.__app, self.__mode, self.__tmplName) ))
		return path
	def get(self, app, mode, tmplName):
		"""
		Get template
		
		**Attributes**
		
		* ``app``:String
		* ``mode``:String
		* ``tmplName``:String
		
		**Returns**
		
		* ``tmpl``:String
		
		"""
		self.__app, self.__mode, self.__tmplName = app, mode, tmplName
		
		logger.debug('TemplateService :: app: %s' % app)
		
		if settings.DEBUG == True:
			package, module = app.split('.')
			m = getClass(package + '.' + module)
			if app == 'ximpia.site':
				appModulePath = settings.__file__.split('settings')[0]
				pathSite = appModulePath + 'web/templates/site'
				if os.path.exists(pathSite) and os.path.isdir(pathSite):
					path = pathSite + '/' + mode + '/' + tmplName + '.html'
				else:
					raise XpMsgException(None, _('site directory inside templates does not exist'))
			else:
				path = self.__findTemplPath(m)
			logger.debug('TemplateService.get :: path: %s' % (path) )
			f = open(path)
			tmpl = f.read()
			f.close()
			cache.set('tmpl/' + app + '/' + mode + '/' + tmplName, tmpl)
		else:
			tmpl = cache.get('tmpl/' + app + '/' + mode + '/' + tmplName)
			if not tmpl:
				package, module = app.split('.')
				m = getClass(package + '.' + module)
				if app == 'ximpia.site':
					appModulePath = settings.__file__.split('settings')[0]
					pathSite = appModulePath + 'web/templates/site'
					if os.path.exists(pathSite) and os.path.isdir(pathSite):
						path = pathSite + '/' + mode + '/' + tmplName + '.html'
					else:
						raise XpMsgException(None, _('site directory inside templates does not exist'))
				else:
					path = self.__findTemplPath(m)
				logger.debug('TemplateService.get :: path: %s' % (path) )
				f = open(path)
				tmpl = f.read()
				f.close()
				cache.set('tmpl/' + app + '/' + mode + '/' + tmplName, tmpl)
		return tmpl

	def resolve(self, viewName):
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
			tmplList = self._dbViewTmpl.search(view__name=viewName, template__language=self._ctx.lang)
			for viewTmpl in tmplList:
				tmpl = viewTmpl.template
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
		#logger.debug( 'templates: %s' % (templates) )
		return templates

class DefaultService ( CommonService ):
	
	def __init__(self, ctx):
		super(DefaultService, self).__init__(ctx)
	
	@ServiceDecorator(form=DefaultForm)
	def show(self):
		"""Method to execute for view with no business code, only showing a html template."""
		pass


































# =========================================
# Eclipse Dumb Classes for code completion
# =========================================

class ContextDumbClass (object):
	def __init__(self):
		if False: self._ctx = Context()
		if False: self._ctx.user = User()
		if False: self._ctx.jsData = JsResultDict()
