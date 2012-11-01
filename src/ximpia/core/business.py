import traceback
import string
import simplejson as json
import types
import datetime
import random

from django.http import HttpResponse
from django.core.mail import send_mail
from django.utils.translation import ugettext as _

from django.contrib.auth import login, authenticate, logout
from django.db.models import Q
from django.shortcuts import render_to_response
from django.template import RequestContext

from models import getResultERROR, XpMsgException, getBlankWfData
from models import View, Action, Application, ViewParamValue, Param, Workflow, WFParamValue, WorkflowView, ViewMenu, Menu, MenuParam, \
	SearchIndex, SearchIndexParam, SearchIndexWord, Word, XpTemplate, ViewTmpl, WorkflowData
from ximpia.util import ut_email, resources
from models import JsResultDict, ContextDecorator as Ctx, CoreParam
import constants as K

from ximpia import settings

# Logging
import logging.config
logging.config.dictConfig(settings.LOGGING)
logger = logging.getLogger(__name__)

from data import WorkflowDataDAO, WorkflowDAO, WFParamValueDAO, ParamDAO, WFViewEntryParamDAO, ViewDAO, WorkflowViewDAO,\
	ApplicationDAO, TemplateDAO, ViewTmplDAO
from data import MenuParamDAO, ViewMenuDAO, ApplicationAccessDAO, ActionDAO
from data import SearchIndexDAO, SearchIndexParamDAO, WordDAO, SearchIndexWordDAO
from choices import Choices
from util import getClass
from forms import DefaultForm

from ximpia.util.js import Form as _jsf

class ComponentRegister(object):
	
	@staticmethod
	def registerApp(code=None, name=None, isAdmin=False):
		"""Register application
		@param code: Application code
		@param name: Application name
		@param isAdmin: Is app admin backdoor?. Values True / False"""
		app, created = Application.objects.get_or_create(code=code, name=name, isAdmin=isAdmin)
		logger.debug( 'Register application: ', app, created )
	
	@staticmethod
	def registerViewMenu(appCode=None, viewName=None, menus=[], **argsDict):
		"""Register views associated with a menu
		@param appCode: Application code
		@param viewName: View name
		@param menus: List of menus dictionaries"""
		logger.debug( 'register view Menus...' )
		app = Application.objects.get(code=appCode)
		view = View.objects.get(application=app, name=viewName)
		# Menu
		logger.debug( 'View menus...' )
		ViewMenu.objects.filter(view=view).delete()
		groupDict = {}
		singleList = []
		counterDict = {}
		for dd in menus:
			if dd.has_key(K.GROUP):
				if not groupDict.has_key(dd[K.GROUP]):
					groupDict[dd[K.GROUP]] = []
				groupDict[dd[K.GROUP]].append(dd)
			else:
				singleList.append(dd)
		# Single Menus - Not Grouped
		counter = 100
		for dd in singleList:
			if not dd.has_key(K.ZONE):
				dd[K.ZONE] = K.VIEW
			try:
				menu = Menu.objects.get(name=dd[K.MENU_NAME])
				sep = dd[K.SEP] if dd.has_key(K.SEP) else False
				logger.debug( view, menu, sep, dd[K.ZONE], counter )
				viewMenu, created = ViewMenu.objects.get_or_create(view=view, menu=menu, separator=sep, #@UnusedVariable
										zone=dd[K.ZONE], order=counter)
				counterDict[dd[K.MENU_NAME]] = counter
				counter += 100
			except Menu.DoesNotExist:
				pass
		# Grouped Menus
		for groupName in groupDict:
			fields = groupDict[groupName]
			menuParent = Menu.objects.get(name=groupName)
			viewMenuParent = ViewMenu.objects.get(view=view, menu=menuParent)
			counter = viewMenuParent.order + 10
			for dd in fields:
				if not dd.has_key(K.ZONE):
					dd[K.ZONE] = K.VIEW
				menu = Menu.objects.get(name=dd[K.MENU_NAME])
				sep = dd[K.SEP] if dd.has_key(K.SEP) else False
				logger.debug( view, menuParent, menu, sep, dd[K.ZONE], counter )
				viewMenu, created = ViewMenu.objects.get_or_create(view=view, menu=menu, separator=sep, #@UnusedVariable
										zone=dd[K.ZONE], order=counter, parent=viewMenuParent)
				counter += 10
	
	@staticmethod
	def cleanViews(appCode=None):
		"""Clean all views for application."""
		View.objects.filter(application__code=appCode).delete()
		logger.debug( 'deleted all views for ' + appCode )
	
	@staticmethod
	def registerView(appCode=None, viewName=None, myClass=None, method=None, menus=[], winType=Choices.WIN_TYPE_WINDOW, hasUrl=False,
			hasAuth=True, **argsDict):
		"""Registers view
		@param appCode: Application code
		@param viewName: View name
		@param myClass: Class that shows view
		@param method: Method that shows view
		@param menus: List of menu dictionaries
		@param winType: Type of window: window or popup
		@param hasUrl: Is view triggered with a server url?
		@param hasAuth: Does view needs login?
		@param argsDict: Dictionary that contains the view entry parameters. Having format name => [value1, value2, ...]"""
		# TODO: Validate entry arguments: There is no None arguments, types, etc...
		logger.debug( 'register views...' )
		classPath = str(myClass).split("'")[1]
		app = Application.objects.get(code=appCode)
		view, created = View.objects.get_or_create(application=app, name=viewName) #@UnusedVariable
		view.implementation = classPath + '.' + method
		view.winType = winType
		view.isUrl = hasUrl
		view.isAuth = hasAuth
		view.save()
		# Parameters
		for name in argsDict:
			param = Param.objects.get(application=app, name=name)
			fields = argsDict[name]
			for value in fields:
				theTuple = ViewParamValue.objects.get_or_create(view=view, name=param, operator='eq', value=value) #@UnusedVariable
		
	
	@staticmethod
	def cleanActions(appCode=None):
		"""Clean all actions for application.
		@param appCode: Application code"""
		Action.objects.filter(application__code=appCode).delete()
		logger.debug( 'deleted all actions for ' + appCode )		
	
	@staticmethod
	def registerAction(appCode=None, actionName=None, myClass=None, method=None, hasUrl=False, hasAuth=True):
		"""Registers action
		@param appCode: Application code
		@param actionName: Action name
		@param myClass: Class for action
		@param method: Method that executes action"""
		classPath = str(myClass).split("'")[1]
		app = Application.objects.get(code=appCode)
		action, created = Action.objects.get_or_create(application=app, name=actionName) #@UnusedVariable
		action.implementation = classPath + '.' + method
		action.hasUrl = hasUrl
		action.hasAuth = hasAuth
		action.save()
	
	@staticmethod
	def registerParam(appCode=None, name=None, title=None, paramType=None, isView=False, isWorkflow=False):
		"""Register view / workflow parameter
		@param appCode: Application code
		@param name: Parameter name
		@param title: Parameter title
		@param paramType: Parameter type
		@param isView: Boolean if parameter used in view
		@param isWorkflow: Boolean if parameter used in flow to resolve view"""
		app = Application.objects.get(code=appCode)
		param, created = Param.objects.get_or_create(application=app, name=name)
		if created:
			param.title = title
			param.paramType=paramType
			param.view = isView
			param.workflow = isWorkflow
			param.save()

	@staticmethod
	def cleanFlows(appCode=None):
		"""Clean all flows for application."""
		Workflow.objects.filter(application__code=appCode).delete()
		WorkflowData.objects.filter(flow__application__code=appCode).delete()
		logger.debug( 'deleted all flows for ' + appCode )
	
	@staticmethod
	def registerFlow(appCode=None, flowCode=None, resetStart=False, deleteOnEnd=False, jumpToView=True):
		"""Reister flow
		@param appCode: Application code
		@param flowcode: Flow code
		@param resetStart: Is flow reset at start of flow?
		@param deleteOnEnd: Is flow data deleted at end of flow?
		@param jumpToView: Does flow needs to jump to last view in flow?"""
		app = Application.objects.get(code=appCode)
		flow, created = Workflow.objects.get_or_create(application=app, code=flowCode) #@UnusedVariable
		flow.resetStart = resetStart
		flow.deleteOnEnd = deleteOnEnd
		flow.jumpToView = jumpToView
		flow.save()
		
	@staticmethod
	def registerFlowView(appCode=None, flowCode=None, viewNameSource=None, viewNameTarget=None, actionName=None, order=10, 
			paramDict={}, viewParamDict={}):
		"""Reister flow
		@param appCode: Application code
		@param flowcode: Flow code
		@param viewNameSource: View name origin for flow
		@param viewNameTarget: View name destiny for flow
		@param actionName: Action name
		@param order: Order to evaluate view target resolution
		@param paramDict: Dictionary that contains the parameters to resolve views. Has the format name => (operator, value)"""
		app = Application.objects.get(code=appCode)
		viewSource = View.objects.get(application=app, name=viewNameSource)
		viewTarget = View.objects.get(application=app, name=viewNameTarget)
		action = Action.objects.get(application=app, name=actionName)
		flow = Workflow.objects.get(code=flowCode)
		flowView, created = WorkflowView.objects.get_or_create(flow=flow, viewSource=viewSource, viewTarget=viewTarget, #@UnusedVariable
								action=action, order=order)
		# Parameters
		for name in paramDict:
			operator, value = paramDict[name]
			wfParamValue, created = WFParamValue.objects.get_or_create(flow=flow, name=name, operator=operator, value=value) #@UnusedVariable
		# Entry View parameters
		# TODO: Complete entry view parameters
	
	@staticmethod
	def cleanMenu(appCode=None):
		"""Clean all menus for application
		@param appCode: Application code"""
		Menu.objects.filter(application__code=appCode).delete()
		logger.debug( 'deleted all menus for ' + appCode )
	
	@staticmethod
	def registerMenu(appCode=None, name='', titleShort='', title='', iconName='', actionName='', viewName='', url='', 
			urlTarget='', **argsDict):
		"""Register menu item
		@param appCode: Application code
		@param name: Menu name
		@param titleShort: Menu short title
		@param title: Menu title
		@param iconName: Name of icon
		@param actionName: Name of action
		@param viewName: View name
		@param url: Url to trigger
		@param urlTarget: Target to open window: same or new tab"""
		logger.debug( 'register menus...' )
		paramDict = {}
		app = Application.objects.get(code=appCode)
		# Icon
		icon, created = CoreParam.objects.get_or_create(mode=K.PARAM_ICON, name=iconName, value=iconName) #@UnusedVariable
		paramDict['application'] = app
		paramDict['name'] = name
		paramDict['titleShort'] = titleShort
		paramDict['title'] = title
		paramDict['icon'] = icon
		if len(url) != 0:
			paramDict['url'] = url
			paramDict['urlTarget'] = urlTarget
		if actionName != '':
			action = Action.objects.get(name=actionName)
			paramDict['action'] = action
		if viewName != '':
			view = View.objects.get(application__code=appCode, name=viewName)
			paramDict['view'] = view
		logger.debug( 'paramDict: ', paramDict )
		menu = Menu.objects.create(**paramDict)
		# MenuParam
		logger.debug( 'argsDict: ', argsDict )
		for name in argsDict:
			operator, value = argsDict[name]
			menuValue, created = MenuParam.objects.get_or_create(menu=menu, name=name, operator=operator, value=value) #@UnusedVariable
		
	@staticmethod
	def cleanSearch(appCode=None):
		"""Clean Search information for view or action
		@param appCode: Application code"""
		try:
			SearchIndex.objects.filter(application__code=appCode).delete()
			logger.debug( 'deleted Search !!!', appCode ) 
		except SearchIndex.DoesNotExist:
			pass

	@staticmethod
	def registerSearch(text='', appCode=None, viewName=None, actionName=None, params={}):
		"""Register application operation. It will be used in view search.
		@param text: Text to index
		@param appCode: Application code
		@param viewName: View name
		@param actionName: Action name"""
		wordList = resources.Index.parseText(text)
		logger.debug( 'wordList: ', wordList )
		view = View.objects.get(name=viewName) if viewName != None else None
		action = Action.objects.get(name=actionName) if actionName != None else None
		app = Application.objects.get(code=appCode)
		# Create search index
		search = SearchIndex.objects.create(application=app, view=view, action=action, title=text)
		for wordName in wordList:
			# Word
			word, created = Word.objects.get_or_create(word=wordName) #@UnusedVariable
			# SearchIndexWord
			searchWord = SearchIndexWord.objects.create(word=word, index=search) #@UnusedVariable
		for paramName in params:
			param = Param.objects.get_or_create(application=app, name=paramName)
			indexParam = SearchIndexParam.objects.create(searchIndex=search, name=param, operator=Choices.OP_EQ, #@UnusedVariable
								value=params[paramName])
	
	@staticmethod
	def cleanTemplates(appCode=None):
		"""Clean templates for the application
		@param appCode: Application code"""
		XpTemplate.objects.filter(application__code=appCode).delete()
		logger.debug( 'deleted all templates for ' + appCode )
	
	@staticmethod
	def registerTemplate(appCode=None, viewName=None, name=None, language=None, country=None, winType=Choices.WIN_TYPE_WINDOW, 
			device=None, alias=None):
		"""Register template
		@param appCode: Application code
		@param viewName: View name
		@param name: Template name
		@param language: Language to target template
		@param country: Country to target template
		@param winType: Type of window for template, window or popup
		@param device: Device to target template
		@param alias: Template alias"""
		app = Application.objects.get(code=appCode)
		view = View.objects.get(application=app, name=viewName) if viewName != None else None
		paramDict = {}
		paramDict['application'] = app
		paramDict['name'] = name
		if language != None:
			paramDict['language'] = language
		if country != None:
			paramDict['country'] = country
		if winType != None:
			paramDict['winType'] = winType
		if device != None:
			paramDict['device'] = device
		if alias != None:
			paramDict['alias'] = alias
		else:
			paramDict['alias'] = viewName		
		try:
			XpTemplate.objects.get(name=name).delete()
		except XpTemplate.DoesNotExist:
			pass
		template = XpTemplate.objects.create( **paramDict )
		# View
		ViewTmpl.objects.create(view=view, template=template)

class CommonBusiness( object ):
	
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
		self._resultDict = getResultERROR([])
		self._postDict = ctx['post']
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
		"""if self._ctx[Ctx.IS_FLOW]:
			self._wf.putParams(**args)
		else:
			dd = json.loads(self._ctx[Ctx.FORM].base_fields['entryFields'].initial)
			for name in args:
				dd[name] = args[name]
			self._ctx[Ctx.FORM].base_fields['entryFields'].initial = json.dumps(dd)"""
	
	def _setTargetView(self, viewName):
		"""Set the target view for navigation."""
		self._viewNameTarget = viewName
		self._ctx[Ctx.VIEW_NAME_TARGET] = viewName
	
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
		logger.debug( 'wfUserId: ', self._ctx[Ctx.WF_USER_ID], ' flowCode: ', self._ctx[Ctx.FLOW_CODE] )
		valueDict = self._wf.getFlowDataDict(self._ctx[Ctx.WF_USER_ID], self._ctx[Ctx.FLOW_CODE])['data']
		logger.debug( 'valueDict: ', valueDict )
		"""valueDict = {}
		for name in nameList:
			#value = self._wf.getParam(name)
			value = self._wf.getParamFromCtx(name)
			valueDict[name] = value"""
		"""if self._ctx[Ctx.IS_FLOW]:
			logger.debug( 'flow!!!!' )
			for name in nameList:
				#value = self._wf.getParam(name)
				value = self._wf.getParamFromCtx(name)
				valueDict[name] = value
		else:
			logger.debug( 'navigation!!!' )
			dd = json.loads(self._ctx[Ctx.FORM].base_fields['entryFields'].initial)
			for name in nameList:
				if dd.has_key(name):
					valueDict[name] = dd[name]"""
		return valueDict
	
	def _getWFUser(self):
		"""Get Workflow user."""
		if self._ctx[Ctx.COOKIES].has_key('wfUserId'):
			self._ctx[Ctx.WF_USER_ID] = self._ctx[Ctx.COOKIES]['wfUserId']
		else:
			self._ctx[Ctx.WF_USER_ID] = self._wf.genUserId()
			self._setCookie('wfUserId', self._ctx[Ctx.WF_USER_ID])
		self._wfUserId = self._ctx[Ctx.WF_USER_ID]
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
		bFormOK = self._ctx[Ctx.FORM].is_valid()
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
		#logger.debug( 'form: ', self._ctx[Ctx.FORM] )
		return self._ctx[Ctx.FORM]
	
	def _setForm(self, formInstance):
		"""Sets the form instance"""
		self._ctx[Ctx.FORM] = formInstance
	
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
			self._isFormOK = self._ctx[Ctx.FORM].is_valid()
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
		return self._ctx[Ctx.FORM]
	
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
		return self._ctx[Ctx.POST]
	
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
		msgDict = _jsf.decodeArray(self._ctx[Ctx.FORM].fields['okMessages'].initial)
		self._ctx[Ctx.FORM].fields['msg_ok'].initial = msgDict[idOK]
	
	def _setCookie(self, key, value):
		"""Add to context cookies data. Decorators that build response will set cookie into respose object
		@param key: Key
		@param value: Value"""
		self._ctx[Ctx.SET_COOKIES].append({'key': key, 'value': value, 'domain': settings.SESSION_COOKIE_DOMAIN, 'expires': datetime.timedelta(days=365*5)+datetime.datetime.utcnow()})

	def _setMainForm(self, formInstance):
		"""Set form as main form: We set to context variable 'form' as add into form container 'forms'.
		@param formInstance: Form instance"""
		self._ctx[Ctx.FORM] = formInstance
		self._ctx[Ctx.FORMS][formInstance.getFormId()] = formInstance
	
	def _addForm(self, formInstance):
		"""Set form as regular form. We add to form container 'forms'. Context variable form is not modified.
		@param formInstance: Form instance"""
		self._ctx[Ctx.FORMS][formInstance.getFormId()] = formInstance
	
	def _getUserChannelName(self):
		"""Get user social name"""
		if self._ctx[Ctx.COOKIES].has_key('userChannelName'):
			userChannelName = self._ctx[Ctx.COOKIES]['userChannelName']
			logger.debug( 'COOKIE :: userChannelName: ', userChannelName )
		else:
			userChannelName = K.USER
			self._setCookie('userChannelName', userChannelName)
		return userChannelName
	
	def _login(self):
		"""Do login"""
		#TODO: Call login to ximpia.com
		login(self._ctx[Ctx.RAW_REQUEST], self._ctx[Ctx.USER])
		self._ctx[Ctx.IS_LOGIN] = True
	
	def _logout(self):
		"""Do logout"""
		#TODO: Call logout to ximpia.com
		logout(self._ctx[Ctx.RAW_REQUEST])
		self._ctx[Ctx.IS_LOGIN] = False
	
	def _addList(self, name, values):
		"""Add name to list_$name in the result JSON object"""
		dictList = []
		for entry in values:
			dd = {}
			keys = entry.keys()
			for key in keys:
				dd[key] = entry[key]
			dictList.append(dd)
		self._ctx[Ctx.JS_DATA].addAttr('list_' + name, dictList)
	
class WorkFlowBusiness (object):	
	_ctx = {}
	__wfData = {}
	
	def __init__(self, ctx):
		self._ctx = ctx
		self._dbWFData = WorkflowDataDAO(ctx, relatedDepth=2)
		self._dbWorkflow = WorkflowDAO(ctx, relatedDepth=2)
		self._dbWFView = WorkflowViewDAO(ctx, relatedDepth=2)
		self._dbWFParams = WFParamValueDAO(ctx, relatedDepth=2)
		self._dbView = ViewDAO(ctx)
		self._dbParam = ParamDAO(ctx)
		self._dbWFViewParam = WFViewEntryParamDAO(ctx, relatedDepth=2)
		self.__wfData = getBlankWfData({})
	
	def genUserId(self):
		"""Generate workflow user id.
		@return: userId"""
		userId = ''
		while len(userId) < 40:
			userId += random.choice('0123456789abcde')
		return userId
	
	def get(self, flowCode):
		"""Get flow."""
		flow = self._dbWorkflow.get(code=flowCode)
		return flow
	
	def resolveFlowDataForUser(self, wfUserId, flowCode):
		"""Resolves flow for user and session key.
		@param wfUserId: Workflow User Id
		@param flowCode: Flow code
		@return: resolvedFlow : Resolved flow for flow code , login user or session"""
		resolvedFlow = None
		flows = self._dbWFData.search(flow__code=flowCode, userId=wfUserId)
		logger.debug( 'flows: ', flows )
		logger.debug( 'All: ', self._dbWFData.getAll() )
		if len(flows) > 0:
			resolvedFlow = flows[0]
		else:
			raise XpMsgException(None, _('Error in resolving workflow for user'))
		logger.debug( 'resolvedFlow: ', resolvedFlow )
		return resolvedFlow

	def resolveView(self, wfUserId, appCode, flowCode, viewNameSource, actionName):
		"""Search destiny views with origin viewSource and operation actionName
		@param viewNameSource: Origin view
		@param actionName: Action name
		@return: List of views"""
		viewTarget = ''
		flowViews = self._dbWFView.search(flow__application__code=appCode, flow__code=flowCode,
					viewSource__name=viewNameSource, action__name=actionName).order_by('order')
		params = self._dbWFParams.search(flowView__in=flowViews)
		paramFlowDict = {}
		for param in params:
			if not paramFlowDict.has_key(param.flowView.flow.code):
				paramFlowDict[param.flowView.flow.code] = []
			paramFlowDict[param.flowView.flow.code].append(param)
		wfDict = self.getFlowDataDict(wfUserId, flowCode)
		logger.debug( 'wfDict: ', wfDict )
		if len(flowViews) == 1:
			viewTarget = flowViews[0].viewTarget
		else:
			for flowCode in paramFlowDict:
				params = paramFlowDict[flowCode]
				check = True
				numberEval = 0
				for param in params:
					if wfDict['data'].has_key(param.name):
						if param.operator == Choices.OP_EQ:
							check = wfDict['data'][param.name] == param.value
						elif param.operator == Choices.OP_LT:
							check = wfDict['data'][param.name] < param.value
						elif param.operator == Choices.OP_GT:
							check = wfDict['data'][param.name] > param.value
						elif param.operator == Choices.OP_NE:
							check = wfDict['data'][param.name] != param.value
						if check == True:
							numberEval += 1
				if check == True and numberEval > 0:					
					viewTarget = flowViews.filter(flowView__code=flowCode).viewTarget
					break
		return viewTarget
		
	def putParams(self, **argsDict):
		"""Put list of workflow parameters in context
		@param flowCode: Flow code
		@param argsDict: Argument dictionary"""
		flowCode = self._ctx[Ctx.FLOW_CODE]
		flow = self._dbWorkflow.get(code=flowCode) #@UnusedVariable
		if not self.__wfData:
			self.__wfData = getBlankWfData({})
		nameList = argsDict.keys()
		params = self._dbParam.search(name__in=nameList)
		if len(params) != 0:
			for name in argsDict:
				checkType = True
				paramFilter = params.filter(name=name)
				if not paramFilter:
					raise XpMsgException(None, _('Parameter "') + str(name) + _('" has not been registered'))
				paramDbType = paramFilter[0].paramType
				paramType = type(argsDict[name])
				if paramDbType == Choices.BASIC_TYPE_BOOL:
					checkType = paramType == types.BooleanType
				elif paramDbType == Choices.BASIC_TYPE_DATE:
					checkType = paramType is datetime.date
				elif paramDbType == Choices.BASIC_TYPE_FLOAT:
					checkType = paramType == types.FloatType
				elif paramDbType == Choices.BASIC_TYPE_INT:
					checkType = paramType == types.IntType
				elif paramDbType == Choices.BASIC_TYPE_LONG:
					checkType = paramType == types.LongType
				elif paramDbType == Choices.BASIC_TYPE_STR:
					checkType = paramType == types.StringType
				elif paramDbType == Choices.BASIC_TYPE_TIME:
					checkType = paramType is datetime.time
				#paramValue, created = self._dbWFParams.getCreate()
				if checkType == True:
					self.__wfData['data'][name] = argsDict[name]
				else:
					raise XpMsgException(None, _('Error in parameter type. "') + str(paramDbType) + _('" was expected and "') + str(paramType) + _('" was provided for parameter "') + str(name) + '"')
		else:
			raise XpMsgException(None, _('Parameters "') + ''.join(nameList) + _('" have not been registered'))
	
	def save(self, wfUserId, flowCode):
		"""Saves the workflow into database for user
		@param user: User
		@param flowCode: Flow code"""
		logger.debug( '__wfData: ', self.__wfData )
		flows = self._dbWFData.search(userId=wfUserId, flow__code=flowCode)
		flow = flows[0]
		if flows > 0:
			flowData = _jsf.decode64dict(flow.data)
			for name in self.__wfData['data']:
				flowData['data'][name] = self.__wfData['data'][name]
		else:
			raise XpMsgException(None, _('Flow data not found'))
		#if self.__wfData['viewName'] != '':
		flowData['viewName'] = self.__wfData['viewName']
		view = self._dbView.get(name=self.__wfData['viewName'])
		flow.view = view
		logger.debug( 'save :: flowData: ', flowData )
		flow.data = _jsf.encode64Dict(flowData)
		flow.save()
		return flow
	
	def resetFlow(self, wfUserId, flowCode, viewName):
		"""Reset flow. It deletes all workflow variables and view name
		@param wfUserId: Workflow User Id
		@param flowCode: Flow code"""
		try:
			flowData = self.resolveFlowDataForUser(wfUserId, flowCode)
			logger.debug( 'resetFlow :: flowData: ', flowData )
			self.__wfData = getBlankWfData({})
			self.__wfData['viewName'] = viewName
			logger.debug( '__wfData: ', self.__wfData )
			# Update flow data
			view = self._dbView.get(name=viewName)
			flowData.data = _jsf.encode64Dict(self.__wfData)
			flowData.view = view
			flowData.save()
		except XpMsgException:
			# Create flow data
			logger.debug( 'create flow...', wfUserId )
			self.__wfData = getBlankWfData({})
			self.__wfData['viewName'] = viewName
			logger.debug( '__wfData: ', self.__wfData )
			view = self._dbView.get(name=viewName)
			workflow = self._dbWorkflow.get(code=flowCode)
			self._dbWFData.create(userId=wfUserId, flow=workflow, data = _jsf.encode64Dict(self.__wfData), view=view)

	def setViewName(self, viewName):
		"""Set view name in Workflow
		@param viewName: View name"""
		logger.debug( 'setViewName :: ', self.__wfData )
		self.__wfData['viewName'] = viewName
		logger.debug( self.__wfData )

	def getViewName(self):
		"""Get workflow view name.
		@return: viewName"""
		return self.__wfData['viewName']
	
	def getParam(self, name):
		"""Get workflow parameter from context
		@param name: Name
		@return: Param Value"""
		return self.__wfData['data'][name]
	
	def getParamFromCtx(self, name):
		"""Get flow parameter from context.
		@param name: Parameter name
		@return: Parameter value"""
		flowDataDict = self._ctx[Ctx.FLOW_DATA]
		logger.debug( 'flowDataDict: ', flowDataDict, type(flowDataDict) )
		logger.debug( 'wfData: ', self.__wfData )
		return flowDataDict['data'][name]
		
	def buildFlowDataDict(self, flowData):
		"""Build the flow data dictionary having the flowData instance.
		@param flowData: Flow data
		@return: flowDataDict"""
		flowDataDict = _jsf.decode64dict(flowData.data)
		logger.debug( 'build :: flowDataDict: ', flowDataDict )
		return flowDataDict
	
	def getFlowDataDict(self, wfUserId, flowCode):
		"""Get flow data dictionary for user and flow code
		@param user: User
		@param flowCode: flowCode
		@return: flowData : Dictionary"""
		flowData = self.resolveFlowDataForUser(wfUserId, flowCode)
		flowDataDict = _jsf.decode64dict(flowData.data)
		logger.debug( 'get :: flowDataDict: ', flowDataDict )
		return flowDataDict
	
	def getFlowViewByAction(self, actionName):
		"""Get flow by action name. It queries the workflow data and returns flow associated with actionName
		@param actionName: Action name
		@return: flow: Workflow"""
		flowView = self._dbWFView.get(action__name=actionName)
		return flowView
	
	def getView(self, wfUserId, flowCode):
		"""Get view from flow
		@param user: User
		@param flowCode: Flow code
		@return: viewName"""
		flowDataDict = self.getFlowDataDict(wfUserId, flowCode)
		viewName = flowDataDict['viewName']
		return viewName
	
	def getViewParams(self, flowCode, viewName):
		"""Get view entry parameters for view and flow
		@param flowCode: Flow code
		@param viewName: View name
		@return: params : List of WFViewEntryParam"""
		params = self._dbWFViewParam.search(flowView__flow__code=flowCode, viewParam__view__name = viewName)
		logger.debug( 'params: ', params )
		paramDict = {}
		for param in params:
			paramDict[param.paramView.name] = param.paramView.value
		return paramDict

	def isLastView(self, viewNameSource, viewNameTarget, actionName):
		"""Checks if view is last in flow."""
		flowsView = self._dbWFView.search(viewSource__name=viewNameSource, action__name=actionName).order_by('-order')
		flowView = flowsView[0] if len(flowsView) != 0 else None
		isLastView = False
		if flowView != None and flowView.viewTarget.name == viewNameTarget:
			isLastView = True
		return isLastView
	
	def isFirstView(self, flowCode, viewName):
		"""Checks if view is first in flow. It uses field 'order' to determine if is first view."""
		check = False
		flowViewStart = self._dbWFView.get(flow__code=flowCode, order=10)		
		if flowViewStart.viewSource.name == viewName:
			check = True
		else:
			check = False
		return check
	
	def removeData(self, wfUserId, flowCode):
		"""Removes the workflow data for user or session."""
		flowData = self.resolveFlowDataForUser(wfUserId, flowCode)
		self._dbWFData.deleteById(flowData.id, real=True)
		

class Search( object ):
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

class Template( object ):
	"""Logic for templates"""
	_ctx = None
	def __init__(self, ctx):
		"""Menu building and operations"""
		self._ctx = ctx
		self._dbViewTmpl = ViewTmplDAO(self._ctx, relatedDepth=2)
		self._dbTemplate = TemplateDAO(self._ctx)
	def resolve(self, viewName):
		"""Resolve template """
		# Context: device, lang, country
		#tmplName = ''
		templates = {}
		if self._ctx[Ctx.LANG] != 'en' or self._ctx[Ctx.COUNTRY] != '' or self._ctx[Ctx.DEVICE] != Choices.DEVICE_PC:
			# TODO: Complete for language and device templates
			"""tmplList = self._dbViewTmpl.search(view__name=viewName, template__language=self._ctx[Ctx.LANG])
			if len(tmplList) > 1:
				tmplName = tmplList.filter(template__winType=Choices.WIN_TYPE_WINDOW)[0].template.name
			else:
				if len(tmplList) != 0:
					tmplName = tmplList[0].template.name
				else:
					pass"""
		else:
			tmplList = self._dbViewTmpl.search(view__name=viewName, template__language=self._ctx[Ctx.LANG])
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

class MenuBusiness( object ):
	_ctx = None
	def __init__(self, ctx):
		"""Menu building and operations"""
		self._ctx = ctx
		self._dbViewMenu = ViewMenuDAO(self._ctx, relatedDepth=3)
		self._dbView = ViewDAO(self._ctx, relatedDepth=2)
		self._dbMenuParam = MenuParamDAO(self._ctx, relatedDepth=3)
		self._dbAppAccess = ApplicationAccessDAO(self._ctx)
	def getMenus(self, viewName):
		"""Build menus in a dictionary
		@param viewName: View name"""
		logger.debug( 'getMenus...' )
		#logger.debug( 'getMenus :: appCode: ', self._ctx[Ctx.APP] )
		view = self._dbView.get(name=viewName, application__code=self._ctx[Ctx.APP])
		#logger.debug( 'getMenus :: view: ', view )
		# TODO: Play around to get list of codes using common methods
		#logger.debug( 'getMenus :: userChannel: ', self._ctx[Ctx.USER_CHANNEL] )
		userAccessCodeList = []
		if self._ctx[Ctx.USER_CHANNEL] != None:
			userAccessList = self._dbAppAccess.search(userChannel=self._ctx[Ctx.USER_CHANNEL])
			for userAccess in userAccessList:
				userAccessCodeList.append(userAccess.application.code)
			logger.debug( 'getMenus :: userAccessCodeList: ', userAccessCodeList )
		# TODO: Remove the SN code simulator, use the one built from userChannel
		# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
		userAccessCodeList = ['SN']
		viewMenus = self._dbViewMenu.search( 	Q(menu__application__subscription = False) | 
							Q(menu__application__subscription = True) & 
							Q(menu__application__code__in=userAccessCodeList), view=view).order_by('order')
		#viewMenus = self._dbViewMenu.search( view=view ).order_by('order')
		#logger.debug( 'getMenus :: viewMenus: ', viewMenus )
		#logger.debug( 'getMenus :: viewMenus All: ', self._dbViewMenu.getAll() )
		menuDict = {}
		menuDict[Choices.MENU_ZONE_SYS] = []
		menuDict[Choices.MENU_ZONE_MAIN] = []
		menuDict[Choices.MENU_ZONE_VIEW] = []
		container = {}
		for viewMenu in viewMenus:
			#logger.debug( 'getMenus :: viewMenu: ', viewMenu )
			#logger.debug( 'getMenus :: action: ', viewMenu.menu.action )
			#logger.debug( 'getMenus :: view: ', viewMenu.menu.view )
			menuObj = {}
			menuObj['action'] = viewMenu.menu.action.name if viewMenu.menu.action != None else ''
			menuObj['view'] = viewMenu.menu.view.name if viewMenu.menu.view != None else ''
			menuObj['winType'] = viewMenu.menu.view.winType if viewMenu.menu.view != None else ''
			menuObj['sep'] = viewMenu.separator
			menuObj['name'] = viewMenu.menu.name
			menuObj['title'] = viewMenu.menu.title
			menuObj['titleShort'] = viewMenu.menu.titleShort
			menuObj['icon'] = viewMenu.menu.icon.value
			menuObj['zone'] = viewMenu.zone
			if viewMenu.menu.view != None:
				menuObj['app'] = viewMenu.menu.view.application.code
			elif viewMenu.menu.action != None:
				menuObj['app'] = viewMenu.menu.action.application.code
			# params
			params = self._dbMenuParam.search(menu=viewMenu.menu)
			paramDict = {}
			# name, operator, value
			for param in params:
				if param.operator == Choices.OP_EQ:
					paramDict[param.name] = param.value
			menuObj['params'] = paramDict
			container[viewMenu.menu.name] = menuObj
			#logger.debug( 'menuObj: ', menuObj )
			if viewMenu.parent == None:
				menuObj['items'] = []
				if viewMenu.zone in ['sys','main']:
					if self._ctx[Ctx.IS_LOGIN]:
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
		return menuDict

class EmailBusiness(object):
	#python -m smtpd -n -c DebuggingServer localhost:1025
	@staticmethod
	def send(xmlMessage, subsDict, recipientList):
		"""Send email
		@param keyName: keyName for datastore
		@subsDict : Dictionary with substitution values for template
		@param recipientList: List of emails to send message"""
		#logger.debug( 'subsDict: ', subsDict )
		subject, message = ut_email.getMessage(xmlMessage)
		message = string.Template(message).substitute(**subsDict)
		#logger.debug( message )
		send_mail(subject, message, settings.XIMPIA_WEBMASTER_EMAIL, recipientList)


# ****************************************************
# **                DECORATORS                      **
# ****************************************************

class DoBusinessDecorator(object):
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
		#logger.debug( 'DoBusinessDecorator :: argsDict: ', argsDict, 'argsTuple: ', argsTuple )
		if argsDict.has_key('pageError'):
			self._pageError = argsDict['pageError']
		else:
			self._pageError = False
		if argsDict.has_key('form'):
			self._form = argsDict['form']
		if argsDict.has_key('isServerTmpl'):
			self._isServerTmpl = argsDict['isServerTmpl'] 
	def __call__(self, f):
		def wrapped_f(*argsTuple, **argsDict):
			obj = argsTuple[0]
			#logger.debug( 'DoBusinessDecorator :: data: ', argsTuple, argsDict )
			try:
				#logger.debug( 'DoBusinessDecorator :: ctx: ', obj._ctx.keys() ) 
				obj._ctx[Ctx.JS_DATA] = JsResultDict()
				if self._form != None:
					#obj._ctx[Ctx.FORM] = self._form()
					obj._setMainForm(self._form())
				f(*argsTuple, **argsDict)
				if not obj._ctx.has_key('_doneResult'):
					# Menu
					#logger.debug( 'DoBusinessDecorator :: viewNameTarget: ', str(obj._ctx['viewNameTarget']) )
					#logger.debug( 'DoBusinessDecorator :: viewNameSource: ', str(obj._ctx['viewNameSource']) )
					if len(obj._ctx['viewNameTarget']) > 1:
						viewName = obj._ctx['viewNameTarget']
					else:
						viewName = obj._ctx['viewNameSource']
					#logger.debug( 'DoBusinessDecorator :: viewName: ', viewName )
					menu = MenuBusiness(obj._ctx)
					menuDict = menu.getMenus(viewName)
					#menuDict = menu.getMenus('home')
					obj._ctx[Ctx.JS_DATA]['response']['menus'] = menuDict
					# Views
					"""if obj._ctx['viewNameTarget'] != '':
						obj._ctx[Ctx.JS_DATA]['response']['view'] = obj._ctx['viewNameTarget']
					else:
						obj._ctx[Ctx.JS_DATA]['response']['view'] = obj._ctx['viewNameSource']"""
					obj._ctx[Ctx.JS_DATA]['response']['view'] = viewName
					#logger.debug( 'DoBusinessDecorator :: view: ', '*' + str(obj._ctx[Ctx.JS_DATA]['response']['view']) + '*' )
					# App
					obj._ctx[Ctx.JS_DATA]['response']['app'] = obj._ctx['app']
					# winType
					if len(obj._ctx[Ctx.JS_DATA]['response']['view'].strip()) != 0:
						dbView = ViewDAO(obj._ctx)
						view = dbView.get(application__code=obj._ctx[Ctx.APP], name=obj._ctx[Ctx.JS_DATA]['response']['view'])
						#logger.debug( 'DoBusinessDecorator :: winType: ', str(view.winType) )
						obj._ctx[Ctx.JS_DATA]['response']['winType'] = view.winType
					# User authenticate and session
					if obj._ctx[Ctx.USER].is_authenticated():
						# login: context variable isLogin = True
						obj._ctx[Ctx.JS_DATA].addAttr('isLogin', True)
						#obj._ctx[Ctx.JS_DATA].addAttr('userid', self._ctx['user'].pk)
						keyList = obj._ctx[Ctx.SESSION].keys()
						session = {}
						for key in keyList:
							if key[0] != '_':
								try:
									# We try to serialize using django serialize
									dataEncoded = _jsf.encodeObj(obj._ctx[Ctx.SESSION][key])
									dataReal = json.loads(dataEncoded)
									if type(obj._ctx[Ctx.SESSION][key]) == types.ListType:
										session[key] = dataReal
									else:
										session[key] = dataReal[0]
								except:
									# If we cant, we try json encode
									dataEncoded = json.dumps(obj._ctx[Ctx.SESSION][key])
									session[key] = json.loads(dataEncoded)
						obj._ctx[Ctx.JS_DATA]['response']['session'] = session
					else:
						obj._ctx[Ctx.JS_DATA].addAttr('isLogin', False)
					# Template
					tmpl = Template(obj._ctx)
					if len(obj._ctx[Ctx.JS_DATA]['response']['view'].strip()) != 0:
						templates = tmpl.resolve(obj._ctx[Ctx.JS_DATA]['response']['view'])
						if templates.has_key(obj._ctx[Ctx.JS_DATA]['response']['view']):
							tmplName = templates[obj._ctx[Ctx.JS_DATA]['response']['view']]
							#tmplName = tmpl.resolve(obj._ctx[Ctx.JS_DATA]['response']['view'])
							#logger.debug( 'DoBusinessDecorator :: tmplName: ', tmplName )
						else:
							raise XpMsgException(None, _('Error in resolving template for view'))
						obj._ctx[Ctx.JS_DATA]['response'][Ctx.TMPL] = templates
					else:
						# In case we show only msg with no view, no template
						logger.debug( 'DoBusinessDecorator :: no View, no template...' )
						obj._ctx[Ctx.JS_DATA]['response'][Ctx.TMPL] = ''
					# Forms
					logger.debug( 'DoBusinessDecorator :: forms: ', obj._ctx[Ctx.FORMS] )
					for formId in obj._ctx[Ctx.FORMS]:
						form = obj._ctx[Ctx.FORMS][formId]
						if not obj._ctx[Ctx.JS_DATA].has_key(formId):							
							form.buildJsData(obj._ctx[Ctx.APP], obj._ctx[Ctx.JS_DATA])
						#logger.debug( 'DoBusinessDecorator :: form: ' + formId + ' app: ', form.base_fields['app'].initial )
					#logger.debug( 'DoBusinessDecorator :: response keys : ', obj._ctx[Ctx.JS_DATA]['response'].keys() )
					# Result
					#logger.debug( 'DoBusinessDecorator :: isServerTmpl: ', self._isServerTmpl )
					if self._isServerTmpl == False:
						result = obj._buildJSONResult(obj._ctx[Ctx.JS_DATA])
						#logger.debug( obj._ctx[Ctx.JS_DATA] )
						################# Print response
						logger.debug('')
						logger.debug( 'DoBusinessDecorator :: #################### RESPONSE ##################' )
						#logger.debug( 'DoBusinessDecorator :: response keys: ', obj._ctx[Ctx.JS_DATA]['response'].keys() )
						keys = obj._ctx[Ctx.JS_DATA]['response'].keys()
						for key in keys:
							keyValue = obj._ctx[Ctx.JS_DATA]['response'][key]
							#logger.debug( 'key: ', key, type(keyValue) )
							if type(keyValue) == types.DictType and keyValue.has_key('value'):
								logger.debug( 'DoBusinessDecorator :: response ' + key + ': ' + str(keyValue['value']) )								
							elif type(keyValue) != types.DictType:
								logger.debug( 'DoBusinessDecorator :: response ' + key + ': ' + str(keyValue) )
							else:
								logger.debug( 'else...' )
								for newKey in keyValue:
									#logger.debug( 'newKey: ', newKey )
									#logger.debug( keyValue[newKey] )
									if type(keyValue[newKey]) == types.DictType and keyValue[newKey].has_key('value'):
										logger.debug( 'DoBusinessDecorator :: response ' + key + ' ' + newKey + ': ' + str(keyValue[newKey]['value']) )
									elif type(keyValue[newKey]) != types.DictType:
										logger.debug( 'DoBusinessDecorator :: response ' + key + ' ' + newKey + ': ' + str(keyValue[newKey]) )
									
						################# Print response
						logger.debug( 'DoBusinessDecorator :: #################### RESPONSE ##################' )
						logger.debug( '' )
						for cookie in obj._ctx[Ctx.SET_COOKIES]:
							maxAge = 5*12*30*24*60*60
							result.set_cookie(cookie['key'], value=cookie['value'], domain=cookie['domain'], 
									expires = cookie['expires'], max_age=maxAge)
							logger.debug( 'DoBusinessDecorator :: Did set cookie into result...', cookie )
					else:
						result = obj._ctx[Ctx.JS_DATA]
						#logger.debug( result )
						################# Print response
						logger.debug( '' )
						logger.debug( 'DoBusinessDecorator :: #################### RESPONSE ##################' )
						#logger.debug( 'DoBusinessDecorator :: response keys: ', obj._ctx[Ctx.JS_DATA]['response'].keys() )
						keys = obj._ctx[Ctx.JS_DATA]['response'].keys()
						for key in keys:
							keyValue = obj._ctx[Ctx.JS_DATA]['response'][key]
							#logger.debug( 'key: ', key, type(keyValue) )
							if type(keyValue) == types.DictType and keyValue.has_key('value'):
								logger.debug( 'DoBusinessDecorator :: response ' + key + ': ' + str(keyValue['value']) )								
							elif type(keyValue) != types.DictType:
								logger.debug( 'DoBusinessDecorator :: response ' + key + ': ' + str(keyValue) )
							else:
								logger.debug( 'else...' )
								for newKey in keyValue:
									#logger.debug( 'newKey: ', newKey )
									#logger.debug( keyValue[newKey] )
									if type(keyValue[newKey]) == types.DictType and keyValue[newKey].has_key('value'):
										logger.debug( 'DoBusinessDecorator :: response ' + key + ' ' + newKey + ': ' + str(keyValue[newKey]['value']) )
									elif type(keyValue[newKey]) != types.DictType:
										logger.debug( 'DoBusinessDecorator :: response ' + key + ' ' + newKey + ': ' + str(keyValue[newKey]) )
									
						################# Print response
						logger.debug( 'DoBusinessDecorator :: #################### RESPONSE ##################' )
						logger.debug( '' )
						logger.debug( obj._ctx[Ctx.JS_DATA]['response'].keys() )
					obj._ctx['_doneResult'] = True
				else:
					logger.debug( 'DoBusinessDecorator :: I skip building response, since I already did it!!!!!' )
					if self._isServerTmpl == False:
						result = obj._buildJSONResult(obj._ctx[Ctx.JS_DATA])
					else:
						result = obj._ctx[Ctx.JS_DATA]
				return result
			except XpMsgException as e:
				logger.debug( 'DoBusinessDecorator :: ERROR!!!! DoBusinessDecorator!!!!!' )
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
			obj._ctx[Ctx.JS_DATA] = JsResultDict()
			obj._ctx[Ctx.FORM] = self._form(obj._ctx[Ctx.POST], ctx=obj._ctx)
			bForm = obj._ctx[Ctx.FORM].is_valid()
			#obj._ctx[Ctx.FORM] = obj._f
			#logger.debug( 'ValidateFormDecorator :: Form Validation: ', bForm )
			if bForm == True:
				obj._setMainForm(obj._ctx[Ctx.FORM])
				result = f(*argsTuple, **argsDict)
				return result
				"""try:
					f(*argsTuple, **argsDict)
					obj._f.buildJsData(obj._ctx[Ctx.JS_DATA])
					result = obj.buildJSONResult(obj._ctx[Ctx.JS_DATA])
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
					logger.debug( obj._ctx[Ctx.FORM].errors )
					logger.debug( obj._ctx[Ctx.FORM].errors['invalid'] )
					traceback.print_exc()
				if obj._ctx[Ctx.FORM].errors.has_key('invalid'):
					errorDict = {'': obj._ctx[Ctx.FORM].errors['invalid'][0]}
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
			obj._ctx[Ctx.FLOW_CODE] = self.__flowCode
			obj._ctx[Ctx.IS_FLOW] = True
			logger.debug( 'flowCode: ', self.__flowCode )
			flow = obj._wf.get(self.__flowCode)
			viewName = obj._ctx[Ctx.VIEW_NAME_SOURCE]
			logger.debug( 'View Current: ', obj._ctx[Ctx.VIEW_NAME_SOURCE] )
			# WorKflow User Id
			"""if obj._ctx[Ctx.COOKIES].has_key('wfUserId'):
				obj._ctx[Ctx.WF_USER_ID] = obj._ctx[Ctx.COOKIES]['wfUserId']
				logger.debug( 'COOKIE :: WF User Id: ', obj._ctx[Ctx.WF_USER_ID] )
			else:
				obj._ctx[Ctx.WF_USER_ID] = obj._wf.genUserId()
				obj._setCookie('wfUserId', obj._ctx[Ctx.WF_USER_ID])
				logger.debug( 'WF UserId: ', obj._ctx[Ctx.WF_USER_ID] )"""
			obj._ctx[Ctx.WF_USER_ID] = obj._getWFUser()
			logger.debug( 'WF UserId: ', obj._ctx[Ctx.WF_USER_ID] )
			hasFlow = True
			try:
				flowData = obj._wf.getFlowDataDict(obj._ctx[Ctx.WF_USER_ID], self.__flowCode)
				logger.debug( 'flowData: ', flowData )
			except XpMsgException:
				hasFlow = False
			logger.debug( 'hasFlow: ', hasFlow )
			if flow.jumpToView == True and hasFlow == True:
				# Get flow data, display view in flow data
				try:
					viewName = obj._wf.getView(obj._ctx[Ctx.WF_USER_ID], self.__flowCode)
					logger.debug( 'Jump to View: ', obj._ctx[Ctx.VIEW_NAME_SOURCE], viewName )
				except XpMsgException:
					pass
			else:
				isFirstView = obj._wf.isFirstView(self.__flowCode, obj._ctx[Ctx.VIEW_NAME_SOURCE])
				logger.debug( 'Flow Data: ', hasFlow, isFirstView )
				# Check that this view is first in flow
				if hasFlow == False and isFirstView == True:
					logger.debug( 'reset Flow... no flow and first window' )
					obj._wf.resetFlow(obj._ctx[Ctx.WF_USER_ID], self.__flowCode, obj._ctx[Ctx.VIEW_NAME_SOURCE])
				elif isFirstView == True and flow.resetStart == True:
					logger.debug( 'reset Flow... resetStart=True and first view in flow...' )
					obj._wf.resetFlow(obj._ctx[Ctx.WF_USER_ID], self.__flowCode, obj._ctx[Ctx.VIEW_NAME_SOURCE])
			obj._ctx['viewNameTarget'] = viewName
			# Jump to View in case jumpToView = True and viewName resolved from flow is different from current view
			#logger.debug( 'Jumps... ', viewName, obj._ctx[Ctx.VIEW_NAME_SOURCE] )
			if viewName != obj._ctx[Ctx.VIEW_NAME_SOURCE]:
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
				obj._ctx[Ctx.VIEW_NAME_SOURCE] = viewName
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
				#logger.debug( 'viewNameSource: ', obj._ctx[Ctx.VIEW_NAME_SOURCE] )
				#logger.debug( 'viewNameTarget: ', obj._ctx[Ctx.VIEW_NAME_TARGET] )
				#logger.debug( 'actionName: ', obj._ctx[Ctx.ACTION] )
				#obj._wf = WorkFlowBusiness()
				actionName = obj._ctx[Ctx.ACTION]
				flow = obj._wf.getFlowViewByAction(actionName).flow
				self.__app = flow.application.code
				logger.debug( 'app: ', self.__app )
				obj._ctx[Ctx.FLOW_CODE] = flow.code
				obj._ctx[Ctx.IS_FLOW] = True
				#logger.debug( 'WFActionDecorator :: flowCode: ', obj._ctx[Ctx.FLOW_CODE] )
				obj._ctx[Ctx.WF_USER_ID] = obj._ctx[Ctx.COOKIES]['wfUserId']
				logger.debug( 'COOKIE :: WF User Id: ', obj._ctx[Ctx.WF_USER_ID] )
				result = f(*argsTuple, **argsDict)
				# Resolve View
				#logger.debug( 'session', )
				viewTarget = obj._wf.resolveView(obj._ctx[Ctx.WF_USER_ID], self.__app, obj._ctx[Ctx.FLOW_CODE], 
								obj._ctx[Ctx.VIEW_NAME_SOURCE], obj._ctx[Ctx.ACTION])
				viewName = viewTarget.name
				#logger.debug( 'viewName: ', viewName )
				# Insert view into workflow
				obj._wf.setViewName(viewName)
				viewAttrs = obj._wf.getViewParams(obj._ctx[Ctx.FLOW_CODE], viewName)
				#logger.debug( 'viewAttrs: ', viewAttrs )
				# Save workflow
				flowData = obj._wf.save(obj._ctx[Ctx.WF_USER_ID], obj._ctx[Ctx.FLOW_CODE])
				# Set Flow data dictionary into context
				obj._ctx[Ctx.FLOW_DATA] = obj._wf.buildFlowDataDict(flowData)
				#logger.debug( 'flowDataDict: ', obj._ctx[Ctx.FLOW_DATA] )
				# Delete user flow if deleteOnEnd = True
				if flow.deleteOnEnd == True and obj._wf.isLastView(obj._ctx[Ctx.VIEW_NAME_SOURCE], viewName, obj._ctx[Ctx.ACTION]):
					obj._wf.removeData(obj._ctx[Ctx.WF_USER_ID], obj._ctx[Ctx.FLOW_CODE])
				obj._ctx[Ctx.VIEW_NAME_TARGET] = viewName
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
			args['ctx'][Ctx.VIEW_NAME_SOURCE] = self.__viewName
			resultJs = f(*argsTuple, **args)
			#logger.debug( 'resultJs: ', resultJs )
			template = Template(args['ctx'])
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

class ViewDecorator ( object ):
	""""Decorator for django views in core module."""
	__viewName = ''
	__APP = ''
	def __init__(self, *argsTuple, **argsDict):
		pass
	def __call__(self, f):
		"""Decorator call method"""
		def wrapped_f(request, **args):
			if args.has_key('app') and len(args['app']) != 0:
				self.__APP = args['app']
				if args.has_key('viewName'):
					logger.debug( 'set from args view name' )
					self.__viewName = args['viewName']
				else:
					self.__viewName = ''
			else:
				self.__APP = 'site'
				self.__viewName = 'home'
			args['ctx'][Ctx.VIEW_NAME_SOURCE] = self.__viewName
			logger.debug( f )
			resultJs = f(request, **args)
			logger.debug( f )
			if len(args['ctx'][Ctx.VIEW_NAME_TARGET]) != 0:
				self.__viewName = args['ctx'][Ctx.VIEW_NAME_TARGET]
			logger.debug( 'ViewDecorator :: resultJs: ', resultJs )
			#logger.debug( 'ViewDecorator :: viewName: ', self.__viewName, 'target:', args['ctx'][Ctx.VIEW_NAME_TARGET], 'source:', args['ctx'][Ctx.VIEW_NAME_SOURCE] )
			template = Template(args['ctx'])
			templates = template.resolve(self.__viewName)
			logger.debug( 'ViewDecorator :: templates: ', templates )
			if templates.has_key(self.__viewName):
				tmplName = templates[self.__viewName]
				#logger.debug( 'ViewDecorator :: tmplName: ', tmplName )
				result = render_to_response( self.__APP + '/' + tmplName + '.html', RequestContext(request, 
													{	'result': json.dumps(resultJs),
														'settings': settings
													}))
			else:
				raise XpMsgException(None, _('Error in resolving template for view'))
			return result
		return wrapped_f



class DefaultBusiness ( CommonBusiness ):
	
	def __init__(self, ctx):
		super(DefaultBusiness, self).__init__(ctx)
	
	@DoBusinessDecorator(form=DefaultForm)
	def show(self):
		"""Method to execute for view with no business code, only showing a html template."""
		pass
