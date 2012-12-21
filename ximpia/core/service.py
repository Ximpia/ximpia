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

from ximpia.util import ut_email
from models import JsResultDict, ContextDecorator
import constants as K

# Settings
from ximpia.core.util import getClass
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
		#logger.debug( 'sResult : ', sResult )
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
		logger.debug( 'wfUserId: ', self._ctx.wfUserId, ' flowCode: ', self._ctx.flowCode )
		valueDict = self._wf.getFlowDataDict(self._ctx.wfUserId, self._ctx.flowCode)['data']
		logger.debug( 'valueDict: ', valueDict )
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
		#logger.debug( 'form: ', self._ctx.form )
		return self._ctx.form
	
	def _setForm(self, formInstance):
		"""Sets the form instance"""
		self._ctx.form = formInstance
	
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
		form = self._getForm()
		logger.debug( 'form: ', form )
		#msgDict = _jsf.decodeArray(form.fields['errorMessages'].initial)
		idError = 'id_' + fieldName
		if not self._errorDict.has_key(idError):
			self._errorDict[idError] = {}
		self._errorDict[idError] = errMsg
		logger.debug( '_errorDict : ', self._errorDict )

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
		logger.debug( 'dbDataList : ', dbDataList )
		for dbData in dbDataList:
			dbObj, qArgs, fieldName, errMsg = dbData
			exists = dbObj.check(**qArgs)
			logger.debug( 'validate Exists Data: args: ', qArgs, ' exists: ' + str(exists), ' fieldName: ' + str(fieldName) + ' errMsg: ' + str(errMsg) )
			if not exists:
				self._addError(fieldName, errMsg)
	
	def _validateNotExists(self, dbDataList):
		"""Validates that db data provided does not exist. Error is shown in case exists.
		Db data contains data instance, query arguments in a dictionary
		and errorName for error message display at the front
		@param dbDataList: [dbObj, queryArgs, fieldName, errMsg]"""
		logger.debug( 'validateNotExists...' )
		logger.debug( 'dbDataList : ', dbDataList )
		for dbData in dbDataList:
			dbObj, qArgs, fieldName, errMsg = dbData
			exists = dbObj.check(**qArgs)
			logger.debug( 'Exists : ', exists )
			if exists:
				logger.debug( 'I add error: ', fieldName, errMsg )
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
		logger.debug( '_isValid() :: errorDict : ', self._errorDict, self._isBusinessOK() )
		if not self._isBusinessOK():
			# Here throw the BusinessException
			logger.debug( 'I raise error on business validation!!!!!!!!!!!!!!!!!!' )
			raise XpMsgException(None, _('Error in validating business layer'))

	def _setOkMsg(self, idOK):
		"""Sets the ok message id"""
		msgDict = _jsf.decodeArray(self._ctx.form.fields['okMessages'].initial)
		self._ctx.form.fields['msg_ok'].initial = msgDict[idOK]
	
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
			logger.debug( 'COOKIE :: userChannelName: ', userChannelName )
		else:
			userChannelName = K.USER
			self._setCookie('userChannelName', userChannelName)
		return userChannelName
	
	def _login(self):
		"""Do login"""
		#TODO: Call login to ximpia.com
		login(self._ctx.rawRequest, self._ctx.user)
		self._ctx.isLogin = True
	
	def _logout(self):
		"""Do logout"""
		#TODO: Call logout to ximpia.com
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
		@param keyName: keyName for datastore
		@subsDict : Dictionary with substitution values for template
		@param recipientList: List of emails to send message"""
		#logger.debug( 'subsDict: ', subsDict )
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
					# winType
					if len(obj._ctx.jsData['response']['view'].strip()) != 0:
						dbView = ViewDAO(obj._ctx)
						view = dbView.get(application__name=obj._ctx.app, name=obj._ctx.jsData['response']['view'])
						logger.debug( 'ServiceDecorator :: winType: %s' % (str(view.winType)) )
						obj._ctx.jsData['response']['winType'] = view.winType
					# User authenticate and session
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
					logger.debug( 'ServiceDecorator :: forms: ', obj._ctx.forms )
					for formId in obj._ctx.forms:
						form = obj._ctx.forms[formId]
						if not obj._ctx.jsData.has_key(formId):							
							form.buildJsData(obj._ctx.app, obj._ctx.jsData)
						logger.debug( 'ServiceDecorator :: form: %s app: %s' % (formId, form.base_fields['app'].initial) )
					#logger.debug( 'ServiceDecorator :: response keys : ', obj._ctx.jsData['response'].keys() )
					# Result
					#logger.debug( 'ServiceDecorator :: isServerTmpl: ', self._isServerTmpl )
					if self._isServerTmpl == False:
						result = obj._buildJSONResult(obj._ctx.jsData)
						#logger.debug( obj._ctx.jsData )
						################# Print response
						logger.debug('')
						logger.debug( 'ServiceDecorator :: #################### RESPONSE ##################' )
						#logger.debug( 'ServiceDecorator :: response keys: ', obj._ctx.jsData['response'].keys() )
						keys = obj._ctx.jsData['response'].keys()
						for key in keys:
							keyValue = obj._ctx.jsData['response'][key]
							#logger.debug( 'key: ', key, type(keyValue) )
							if type(keyValue) == types.DictType and keyValue.has_key('value'):
								logger.debug( 'ServiceDecorator :: response ' + key + ': ' + str(keyValue['value']) )								
							elif type(keyValue) != types.DictType:
								logger.debug( 'ServiceDecorator :: response ' + key + ': ' + str(keyValue) )
							else:
								logger.debug( 'else...' )
								for newKey in keyValue:
									#logger.debug( 'newKey: ', newKey )
									#logger.debug( keyValue[newKey] )
									if type(keyValue[newKey]) == types.DictType and keyValue[newKey].has_key('value'):
										logger.debug( 'ServiceDecorator :: response ' + key + ' ' + newKey + ': ' + str(keyValue[newKey]['value']) )
									elif type(keyValue[newKey]) != types.DictType:
										logger.debug( 'ServiceDecorator :: response ' + key + ' ' + newKey + ': ' + str(keyValue[newKey]) )
									
						################# Print response
						logger.debug( 'ServiceDecorator :: #################### RESPONSE ##################' )
						logger.debug( '' )
						for cookie in obj._ctx.set_cookies:
							maxAge = 5*12*30*24*60*60
							result.set_cookie(cookie['key'], value=cookie['value'], domain=cookie['domain'], 
									expires = cookie['expires'], max_age=maxAge)
							logger.debug( 'ServiceDecorator :: Did set cookie into result...', cookie )
					else:
						result = obj._ctx.jsData
						#logger.debug( result )
						################# Print response
						logger.debug( '' )
						logger.debug( 'ServiceDecorator :: #################### RESPONSE ##################' )
						#logger.debug( 'ServiceDecorator :: response keys: ', obj._ctx.jsData['response'].keys() )
						keys = obj._ctx.jsData['response'].keys()
						for key in keys:
							keyValue = obj._ctx.jsData['response'][key]
							#logger.debug( 'key: ', key, type(keyValue) )
							if type(keyValue) == types.DictType and keyValue.has_key('value'):
								logger.debug( 'ServiceDecorator :: response ' + key + ': ' + str(keyValue['value']) )								
							elif type(keyValue) != types.DictType:
								logger.debug( 'ServiceDecorator :: response ' + key + ': ' + str(keyValue) )
							else:
								logger.debug( 'else...' )
								for newKey in keyValue:
									#logger.debug( 'newKey: ', newKey )
									#logger.debug( keyValue[newKey] )
									if type(keyValue[newKey]) == types.DictType and keyValue[newKey].has_key('value'):
										logger.debug( 'ServiceDecorator :: response ' + key + ' ' + newKey + ': ' + str(keyValue[newKey]['value']) )
									elif type(keyValue[newKey]) != types.DictType:
										logger.debug( 'ServiceDecorator :: response ' + key + ' ' + newKey + ': ' + str(keyValue[newKey]) )
									
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
			#logger.debug( 'ValidateFormDecorator :: ', argsTuple, argsDict )
			obj = argsTuple[0]
			#result = f(*argsTuple, **argsDict)
			obj._ctx.jsData = JsResultDict()
			obj._ctx.form = self._form(obj._ctx.post, ctx=obj._ctx)
			bForm = obj._ctx.form.is_valid()
			#obj._ctx.form = obj._f
			#logger.debug( 'ValidateFormDecorator :: Form Validation: ', bForm )
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
					logger.debug( obj._ctx.form.errors['invalid'] )
					traceback.print_exc()
				if obj._ctx.form.errors.has_key('invalid'):
					errorDict = {'': obj._ctx.form.errors['invalid'][0]}
				else:
					errorDict = {'': 'Error validating your data. Check it out and send again'}
				logger.debug( 'errorDict: ', errorDict )
				result = obj._buildJSONResult(obj._getErrorResultDict(errorDict, pageError=True))
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
			#logger.debug( 'WFViewstartDecorator :: ', argsTuple, argsDict )
			obj = argsTuple[0]
			#obj._wf = WorkFlowBusiness(obj._ctx)
			obj._ctx.flowCode = self.__flowCode
			obj._ctx.isFlow = True
			logger.debug( 'flowCode: ', self.__flowCode )
			flow = obj._wf.get(self.__flowCode)
			viewName = obj._ctx.viewNameSource
			logger.debug( 'View Current: ', obj._ctx.viewNameSource )
			# WorKflow User Id
			"""if obj._ctx.cookies.has_key('wfUserId'):
				obj._ctx.wfUserId = obj._ctx.cookies['wfUserId']
				logger.debug( 'COOKIE :: WF User Id: ', obj._ctx.wfUserId )
			else:
				obj._ctx.wfUserId = obj._wf.genUserId()
				obj._setCookie('wfUserId', obj._ctx.wfUserId)
				logger.debug( 'WF UserId: ', obj._ctx.wfUserId )"""
			obj._ctx.wfUserId = obj._getWFUser()
			logger.debug( 'WF UserId: ', obj._ctx.wfUserId )
			hasFlow = True
			try:
				flowData = obj._wf.getFlowDataDict(obj._ctx.wfUserId, self.__flowCode)
				logger.debug( 'flowData: ', flowData )
			except XpMsgException:
				hasFlow = False
			logger.debug( 'hasFlow: ', hasFlow )
			if flow.jumpToView == True and hasFlow == True:
				# Get flow data, display view in flow data
				try:
					viewName = obj._wf.getView(obj._ctx.wfUserId, self.__flowCode)
					logger.debug( 'Jump to View: ', obj._ctx.viewNameSource, viewName )
				except XpMsgException:
					pass
			else:
				isFirstView = obj._wf.isFirstView(self.__flowCode, obj._ctx.viewNameSource)
				logger.debug( 'Flow Data: ', hasFlow, isFirstView )
				# Check that this view is first in flow
				if hasFlow == False and isFirstView == True:
					logger.debug( 'reset Flow... no flow and first window' )
					obj._wf.resetFlow(obj._ctx.wfUserId, self.__flowCode, obj._ctx.viewNameSource)
				elif isFirstView == True and flow.resetStart == True:
					logger.debug( 'reset Flow... resetStart=True and first view in flow...' )
					obj._wf.resetFlow(obj._ctx.wfUserId, self.__flowCode, obj._ctx.viewNameSource)
			obj._ctx['viewNameTarget'] = viewName
			# Jump to View in case jumpToView = True and viewName resolved from flow is different from current view
			#logger.debug( 'Jumps... ', viewName, obj._ctx.viewNameSource )
			if viewName != obj._ctx.viewNameSource:
				logger.debug( 'redirect to ...', viewName )				
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
			logger.debug( 'MenuAction :: ', view.name )
			obj._ctx['viewNameSource'] = view.name
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
				#logger.debug( 'viewNameSource: ', obj._ctx.viewNameSource )
				#logger.debug( 'viewNameTarget: ', obj._ctx.viewNameTarget )
				#logger.debug( 'actionName: ', obj._ctx.action )
				#obj._wf = WorkFlowBusiness()
				actionName = obj._ctx.action
				flow = obj._wf.getFlowViewByAction(actionName).flow
				self.__app = flow.application.code
				logger.debug( 'app: ', self.__app )
				obj._ctx.flowCode = flow.code
				obj._ctx.isFlow = True
				#logger.debug( 'WFActionDecorator :: flowCode: ', obj._ctx.flowCode )
				obj._ctx.wfUserId = obj._ctx.cookies['wfUserId']
				logger.debug( 'COOKIE :: WF User Id: ', obj._ctx.wfUserId )
				result = f(*argsTuple, **argsDict)
				# Resolve View
				#logger.debug( 'session', )
				viewTarget = obj._wf.resolveView(obj._ctx.wfUserId, self.__app, obj._ctx.flowCode, 
								obj._ctx.viewNameSource, obj._ctx.action)
				viewName = viewTarget.name
				#logger.debug( 'viewName: ', viewName )
				# Insert view into workflow
				obj._wf.setViewName(viewName)
				viewAttrs = obj._wf.getViewParams(obj._ctx.flowCode, viewName)
				#logger.debug( 'viewAttrs: ', viewAttrs )
				# Save workflow
				flowData = obj._wf.save(obj._ctx.wfUserId, obj._ctx.flowCode)
				# Set Flow data dictionary into context
				obj._ctx.flowData = obj._wf.buildFlowDataDict(flowData)
				#logger.debug( 'flowDataDict: ', obj._ctx.flowData )
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
			#logger.debug( 'resultJs: ', resultJs )
			template = TemplateService(args['ctx'])
			templates = template.resolve(self.__viewName)
			if templates.has_key(self.__viewName):
				tmplName = templates[self.__viewName]
				#logger.debug( 'tmplName: ', tmplName )
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
	_settings = {}
	def __init__(self, *argsTuple, **argsDict):
		if len(argsTuple) != 0:
			logger.debug('argList: %s' % (argsTuple) )
			self.__APP = '.'.join(argsTuple[0].split('.')[:2])
	def __call__(self, f):
		"""Decorator call method"""
		def wrapped_f(request, **args):
			
			logger.debug( 'ViewTmplDecorator :: args: %s' % args )
			
			# Data instances
			dbApp = ApplicationDAO(args['ctx'])
			
			ctx = args['ctx']
			if False: ctx = Context()
			if args.has_key('appSlug') and len(args['appSlug']) != 0:
				self.__APP = dbApp.get(slug=args['appSlug']).name
				if args.has_key('viewName'):
					logger.debug( 'set from args view name' )
					self.__viewName = args['viewName']
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
				self.__viewName = ctx.viewNameTargett
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
				logger.debug('ViewTmplDecorator :: title: %s' % (parser.title) )
				result = render_to_response( 'main.html', RequestContext(request, 
												{	'title': parser.title,
													'titleBar': parser.titleBar,
													'content': parser.content,
													'buttons': parser.buttons,
													'result': json.dumps(resultJs),
													'settings': settings
												}))
				#result = result.replace('{{result}}', json.dumps(resultJs))
			else:
				raise XpMsgException(None, _('Error in resolving template for view'))			
			
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
			#logger.debug( 'getMenus :: viewMenu: ', viewMenu )
			#logger.debug( 'getMenus :: action: ', viewMenu.menu.action )
			#logger.debug( 'getMenus :: view: ', viewMenu.menu.view )
			menuObj = {}
			if viewMenu.menu.view != None:
				menuObj['service'] = viewMenu.menu.view.service.name
			if viewMenu.menu.action != None:
				menuObj['service'] = viewMenu.menu.action.service.name
			menuObj['action'] = viewMenu.menu.action.name if viewMenu.menu.action != None else ''
			menuObj['view'] = viewMenu.menu.view.name if viewMenu.menu.view != None else ''
			menuObj['winType'] = viewMenu.menu.view.winType if viewMenu.menu.view != None else ''
			menuObj['sep'] = viewMenu.hasSeparator
			menuObj['name'] = viewMenu.menu.name
			menuObj['title'] = viewMenu.menu.title
			menuObj['description'] = viewMenu.menu.description
			menuObj['icon'] = viewMenu.menu.icon.value if viewMenu.menu.icon != None else ''
			menuObj['zone'] = viewMenu.zone
			if viewMenu.menu.view != None:
				menuObj['app'] = viewMenu.menu.view.application.name
			elif viewMenu.menu.action != None:
				menuObj['app'] = viewMenu.menu.action.application.name
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
			#logger.debug( 'menuObj: ', menuObj )
			if viewMenu.parent == None:
				menuObj['items'] = []
				if viewMenu.zone in ['sys','main']:
					if self._ctx.isLogin:
						menuDict[viewMenu.zone].append(menuObj)
					else:
						if viewMenu.menu.name == 'home':
							menuDict[viewMenu.zone].append(menuObj) 
				else:
					menuDict[viewMenu.zone].append(menuObj)
			else:
				parentMenuObj = container[viewMenu.parent.menu.name]
				parentMenuObj['items'].append(menuObj)
		logger.debug( 'getMenus :: menuDict: ', menuDict )
	
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
		#logger.debug( 'getMenus :: viewMenus: ', viewMenus )
		#logger.debug( 'getMenus :: viewMenus All: ', self._dbViewMenu.getAll() )
		menuDict = {}
		menuDict[Choices.MENU_ZONE_SYS] = []
		menuDict[Choices.MENU_ZONE_MAIN] = []
		menuDict[Choices.MENU_ZONE_SERVICE] = []
		menuDict[Choices.MENU_ZONE_VIEW] = []		
		
		# TODO: Get main and sys without link, from settings
		# linked to service
		menuList = self._dbServiceMenu.search( 	Q(menu__application__isSubscription=False) |
												Q(menu__application__isSubscription=True) &
												Q(menu__application__accessGroup__user=self._ctx.user) , 
												service=view.service ).order_by('order')
		self.__getList(menuDict, menuList)
		# linked to view
		menuList = self._dbViewMenu.search( 	Q(menu__application__isSubscription=False) |
												Q(menu__application__isSubscription=True) &
												Q(menu__application__accessGroup__user=self._ctx.user) , 
												view=view ).order_by('order')
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
		logger.debug( 'wordList: ', wordList )
		#results = self._dbIndexWord.search(word__word__in=wordList)[:100]
		# Build Q instance
		myQ = Q(word__word__startswith=wordList[0])
		for word in wordList[1:]:
			myQ = myQ | Q(word__word__startswith=word)
		logger.debug( 'Q: ', str(myQ) )
		results = self._dbIndexWord.search(myQ)[:100]
		logger.debug( 'search :: results: ', results )
		logger.debug( results.query )
		container = {}
		containerData = {}
		for data in results:
			logger.debug( 'data: ', data )
			if not container.has_key(data.index.pk):
				container[data.index.pk] = 0
			container[data.index.pk] += 1
			#container[data.index.pk] += 1 if container.has_key(data.index.pk) else 1
			containerData[data.index.pk] = data
		logger.debug( 'conatiner: ', container )
		logger.debug( 'containerData: ', containerData )
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
			extraDict['app'] = data.index.application.code
			myDict['extra'] = extraDict
			resultsFinal.append(myDict)
		return resultsFinal
	def searchOld(self, text):
		"""Search for views and actions
		@param text: text to search
		@return: results : List of dictionaries with "id", "text", "image" and "extra" fields."""
		results = self._dbSearch.search(title__icontains=text)[:15]
		logger.debug( 'search :: results: ', results )
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
			extraDict['app'] = data.application.code
			myDict['extra'] = extraDict
			resultsFinal.append(myDict)
		return resultsFinal

class TemplateService ( object ):
	"""Logic for templates"""
	_ctx = None
	def __init__(self, ctx):
		"""Menu building and operations"""
		self._ctx = ctx
		self._dbViewTmpl = ViewTmplDAO(self._ctx, relatedDepth=2)
		self._dbTemplate = TemplateDAO(self._ctx)
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
		
		logger.debug('TemplateService :: app: %s' % app)
		
		if settings.DEBUG == True:
			package, module = app.split('.')
			m = getClass(package + '.' + module)
			path = m.__file__.split('__init__')[0] + 'templates/' + mode + '/' + tmplName + '.html'
			f = open(path)
			tmpl = f.read()
			f.close()
			cache.set('tmpl/' + app + '/' + mode + '/' + tmplName, tmpl)
		else:
			tmpl = cache.get('tmpl/' + app + '/' + mode + '/' + tmplName)
			if not tmpl:
				package, module = app.split('.')
				m = getClass(package + '.' + module)
				path = m.__file__.split('__init__')[0] + 'templates/' + mode + '/' + tmplName + '.html'
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
		#logger.debug( 'templates: ', templates )
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
