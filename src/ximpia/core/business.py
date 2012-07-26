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
	SearchIndex, SearchIndexParam, SearchIndexWord, Word, XpTemplate, ViewTmpl
from ximpia.util import ut_email, resources
from ximpia.core.models import JsResultDict, ContextDecorator as Ctx, CoreParam
from ximpia.core import constants as K

from ximpia.core.data import WorkflowDataDAO, WorkflowDAO, WFParamValueDAO, ParamDAO, WFViewEntryParamDAO, ViewDAO, WorkflowViewDAO,\
	ApplicationDAO, TemplateDAO, ViewTmplDAO
from ximpia.core.data import MenuParamDAO, ViewMenuDAO, ApplicationAccessDAO, ActionDAO
from ximpia.core.data import SearchIndexDAO, SearchIndexParamDAO, WordDAO, SearchIndexWordDAO
from ximpia.core.choices import Choices
from ximpia.core.util import getClass

from ximpia.util.js import Form as _jsf

from ximpia import settings

class ComponentRegister(object):
	
	@staticmethod
	def registerApp(code=None, name=None, isAdmin=False):
		"""Register application"""
		app, created = Application.objects.get_or_create(code=code, name=name, isAdmin=isAdmin)
		print 'Register application: ', app, created
	
	@staticmethod
	def registerViewMenu(appCode=None, viewName=None, menus=[], **argsDict):
		"""Doc."""
		print 'register view Menus...'
		app = Application.objects.get(code=appCode)
		view = View.objects.get(application=app, name=viewName)
		# Menu
		print 'View menus...'
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
			menu = Menu.objects.get(name=dd[K.MENU_NAME])
			sep = dd[K.SEP] if dd.has_key(K.SEP) else False
			print view, menu, sep, dd[K.ZONE], counter
			viewMenu, created = ViewMenu.objects.get_or_create(view=view, menu=menu, separator=sep, #@UnusedVariable
										zone=dd[K.ZONE], order=counter)
			counterDict[dd[K.MENU_NAME]] = counter
			counter += 100
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
				print view, menuParent, menu, sep, dd[K.ZONE], counter
				viewMenu, created = ViewMenu.objects.get_or_create(view=view, menu=menu, separator=sep, #@UnusedVariable
										zone=dd[K.ZONE], order=counter, parent=viewMenuParent)
				counter += 10
	
	@staticmethod
	def registerView(appCode=None, viewName=None, myClass=None, method=None, menus=[], winType=Choices.WIN_TYPE_WINDOW, hasUrl=False,
			hasAuth=True, **argsDict):
		"""Registers view
		@param appCode: Application code
		@param viewName: View name
		@param myClass: Class that shows view
		@param method: Method that shows view
		@param argsDict: Dictionary that contains the view entry parameters. Having format name => [value1, value2, ...]"""
		# TODO: Validate entry arguments: There is no None arguments, types, etc...
		print 'register views...'
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
	def registerAction(appCode=None, actionName=None, myClass=None, method=None):
		"""Registers action
		@param appCode: Application code
		@param actionName: Action name
		@param myClass: Class for action
		@param method: Method that executes action"""
		classPath = str(myClass).split("'")[1]
		app = Application.objects.get(code=appCode)
		action, created = Action.objects.get_or_create(application=app, name=actionName) #@UnusedVariable
		action.implementation = classPath + '.' + method
		action.save()
	
	@staticmethod
	def registerParam(appCode=None, name=None, title=None, paramType=None, isView=False, isWorkflow=False):
		"""Register view / workflow parameter
		@param appCode: Application code
		@param name: Parameter name
		@param title: Parameter title
		@param paramType: Parameter type
		@param view: Boolean if parameter used in view
		@param action: Boolean if parameter used in flow to resolve view"""
		app = Application.objects.get(code=appCode)
		param, created = Param.objects.get_or_create(application=app, name=name)
		if created:
			param.title = title
			param.paramType=paramType
			param.view = isView
			param.workflow = isWorkflow
			param.save()

	@staticmethod
	def registerFlow(appCode=None, flowCode=None, resetStart=False, deleteOnEnd=False, jumpToView=True):
		"""Reister flow
		@param appCode: Application code
		@param flowcode: Flow code"""
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
		"""Clean all menus for application"""
		Menu.objects.filter(application__code=appCode).delete()
		print 'deleted all menus for ' + appCode
	
	@staticmethod
	def registerMenu(appCode=None, name='', titleShort='', title='', iconName='', actionName='', viewName='', **argsDict):
		"""Register menu item"""
		print 'register menus...'
		paramDict = {}
		app = Application.objects.get(code=appCode)
		# Icon
		icon, created = CoreParam.objects.get_or_create(mode=K.PARAM_ICON, name=iconName, value=iconName) #@UnusedVariable
		paramDict['application'] = app
		paramDict['name'] = name
		paramDict['titleShort'] = titleShort
		paramDict['title'] = title
		paramDict['icon'] = icon
		if actionName != '':
			action = Action.objects.get(name=actionName)
			paramDict['action'] = action
		if viewName != '':
			view = View.objects.get(application__code=appCode, name=viewName)
			paramDict['view'] = view
		print 'paramDict: ', paramDict
		"""try:
			Menu.objects.get(name=name).delete()
		except Menu.DoesNotExist:
			pass"""
		menu = Menu.objects.create(**paramDict)
		"""menu, created = Menu.objects.get_or_create(**paramDict)
		if not created:
			if paramDict.has_key('action'):
				menu.action = paramDict['action']
			if paramDict.has_key('view'):
				menu.view = paramDict['view']
			menu.titleShort = titleShort
			menu.title = title
			menu.icon = icon
			menu.save()"""
		# MenuParam
		print 'argsDict: ', argsDict
		for name in argsDict:
			operator, value = argsDict[name]
			menuValue, created = MenuParam.objects.get_or_create(menu=menu, name=name, operator=operator, value=value) #@UnusedVariable
		
	@staticmethod
	def cleanSearch(appCode=None):
		"""Clean Search information for view or action"""
		try:
			SearchIndex.objects.filter(application__code=appCode).delete()
			print 'deleted Search !!!', appCode 
		except SearchIndex.DoesNotExist:
			pass

	@staticmethod
	def registerSearch(text='', appCode=None, viewName=None, actionName=None, params={}):
		"""Register application operation. It will be used in view search."""
		wordList = resources.Index.parseText(text)
		print 'wordList: ', wordList
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
		"""Clean templates for the application"""
		pass
	
	@staticmethod
	def registerTemplate(appCode=None, viewName=None, name=None, language=None, country=None, winType=None, device=None, alias=None):
		"""Register template"""
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
		#print 'Dumping...'
		sResult = json.dumps(resultDict)
		#print 'sResult : ', sResult
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
	
	def _getTargetView(self):
		"""Get target view."""
		return self._viewNameTarget
	
	def _getFlowParams(self, *nameList):
		"""Get parameter for list given, either from workflow dictionary or parameter dictionary in view.
		@param nameList: List of parameters to fetch"""
		print 'wfUserId: ', self._ctx[Ctx.WF_USER_ID], ' flowCode: ', self._ctx[Ctx.FLOW_CODE]
		valueDict = self._wf.getFlowDataDict(self._ctx[Ctx.WF_USER_ID], self._ctx[Ctx.FLOW_CODE])['data']
		print 'valueDict: ', valueDict
		"""valueDict = {}
		for name in nameList:
			#value = self._wf.getParam(name)
			value = self._wf.getParamFromCtx(name)
			valueDict[name] = value"""
		"""if self._ctx[Ctx.IS_FLOW]:
			print 'flow!!!!'
			for name in nameList:
				#value = self._wf.getParam(name)
				value = self._wf.getParamFromCtx(name)
				valueDict[name] = value
		else:
			print 'navigation!!!'
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
		#print 'form: ', self._ctx[Ctx.FORM]
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
	
	def _addError(self, field):
		"""Add error
		@param idError: String : Id of error
		@param form: Form
		@param errorField: String : The field inside class form"""
		form = self._getForm()
		print 'form: ', form
		msgDict = _jsf.decodeArray(form.fields['errorMessages'].initial)
		idError = 'id_' + field
		if not self._errorDict.has_key(idError):
			self._errorDict[idError] = {}
		self._errorDict[idError] = msgDict['ERR_' + field]
		print '_errorDict : ', self._errorDict

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
		@param dbDataList: [dbObj, queryArgs, errorName]"""
		print 'validateExists...'
		print 'dbDataList : ', dbDataList
		for dbData in dbDataList:
			dbObj, qArgs, errName = dbData
			exists = dbObj.check(**qArgs)
			print 'validate Exists Data: args: ', qArgs, ' exists: ' + str(exists), ' errName: ' + str(errName)
			if not exists:
				self._addError(field=errName)
	
	def _validateNotExists(self, dbDataList):
		"""Validates that db data provided does not exist. Error is shown in case exists.
		Db data contains data instance, query arguments in a dictionary
		and errorName for error message display at the front
		@param dbDataList: [dbObj, queryArgs, errorName]"""
		print 'validateNotExists...'
		print 'dbDataList : ', dbDataList
		for dbData in dbDataList:
			dbObj, qArgs, errName = dbData
			exists = dbObj.check(**qArgs)
			print 'Exists : ', exists
			if exists:
				print 'I add error: ', errName
				self._addError(field=errName)
		
	def _validateContext(self, ctxDataList):
		"""Validates context variable. [[name, value, errName],...]"""
		for ctxData in ctxDataList:
			name, value, errName = ctxData
			if self._ctx[name] != value:
				self._addError(errName)
		
	def _authenticateUser(self, **dd):
		"""Authenticates user and password
		dd: {'userName': $userName, 'password': $password, 'errorName': $errorName}"""
		qArgs = {'username': dd['userName'], 'password': dd['password']}
		user = authenticate(**qArgs)
		if user:
			pass
		else:
			self._addError(dd['errorName'])
		return user
	
	def _isValid(self):
		"""Checks if no errors have been written to error container.
		If not, raises XpMsgException """
		self._errorDict = self._getErrors()
		print '_isValid() :: errorDict : ', self._errorDict, self._isBusinessOK()
		if not self._isBusinessOK():
			# Here throw the BusinessException
			print 'I raise error on business validation!!!!!!!!!!!!!!!!!!'
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
			print 'COOKIE :: userChannelName: ', userChannelName
		else:
			userChannelName = K.USER
			self._setCookie('userChannelName', userChannelName)
		return userChannelName
	
	def _login(self):
		"""Do login"""
		login(self._ctx[Ctx.RAW_REQUEST], self._ctx[Ctx.USER])
		self._ctx[Ctx.IS_LOGIN] = True
	
	def _logout(self):
		"""Do logout"""
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
		print 'flows: ', flows
		print 'All: ', self._dbWFData.getAll()
		if len(flows) > 0:
			resolvedFlow = flows[0]
		else:
			raise XpMsgException(None, _('Error in resolving workflow for user'))
		print 'resolvedFlow: ', resolvedFlow
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
		print 'wfDict: ', wfDict
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
		print '__wfData: ', self.__wfData
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
		print 'save :: flowData: ', flowData
		flow.data = _jsf.encode64Dict(flowData)
		flow.save()
		return flow
	
	def resetFlow(self, wfUserId, flowCode, viewName):
		"""Reset flow. It deletes all workflow variables and view name
		@param wfUserId: Workflow User Id
		@param flowCode: Flow code"""
		try:
			flowData = self.resolveFlowDataForUser(wfUserId, flowCode)
			print 'resetFlow :: flowData: ', flowData
			self.__wfData = getBlankWfData({})
			self.__wfData['viewName'] = viewName
			print '__wfData: ', self.__wfData
			# Update flow data
			view = self._dbView.get(name=viewName)
			flowData.data = _jsf.encode64Dict(self.__wfData)
			flowData.view = view
			flowData.save()
		except XpMsgException:
			# Create flow data
			print 'create flow...', wfUserId
			self.__wfData = getBlankWfData({})
			self.__wfData['viewName'] = viewName
			print '__wfData: ', self.__wfData
			view = self._dbView.get(name=viewName)
			workflow = self._dbWorkflow.get(code=flowCode)
			self._dbWFData.create(userId=wfUserId, flow=workflow, data = _jsf.encode64Dict(self.__wfData), view=view)

	def setViewName(self, viewName):
		"""Set view name in Workflow
		@param viewName: View name"""
		print 'setViewName :: ', self.__wfData
		self.__wfData['viewName'] = viewName
		print self.__wfData

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
		print 'flowDataDict: ', flowDataDict, type(flowDataDict)
		print 'wfData: ', self.__wfData
		return flowDataDict['data'][name]
		
	def buildFlowDataDict(self, flowData):
		"""Build the flow data dictionary having the flowData instance.
		@param flowData: Flow data
		@return: flowDataDict"""
		flowDataDict = _jsf.decode64dict(flowData.data)
		print 'build :: flowDataDict: ', flowDataDict
		return flowDataDict
	
	def getFlowDataDict(self, wfUserId, flowCode):
		"""Get flow data dictionary for user and flow code
		@param user: User
		@param flowCode: flowCode
		@return: flowData : Dictionary"""
		flowData = self.resolveFlowDataForUser(wfUserId, flowCode)
		flowDataDict = _jsf.decode64dict(flowData.data)
		print 'get :: flowDataDict: ', flowDataDict
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
		print 'params: ', params
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
		print 'wordList: ', wordList
		#results = self._dbIndexWord.search(word__word__in=wordList)[:100]
		# Build Q instance
		myQ = Q(word__word__startswith=wordList[0])
		for word in wordList[1:]:
			myQ = myQ | Q(word__word__startswith=word)
		print 'Q: ', str(myQ)
		results = self._dbIndexWord.search(myQ)[:100]
		print 'search :: results: ', results
		print results.query
		container = {}
		containerData = {}
		for data in results:
			print 'data: ', data
			if not container.has_key(data.index.pk):
				container[data.index.pk] = 0
			container[data.index.pk] += 1
			#container[data.index.pk] += 1 if container.has_key(data.index.pk) else 1
			containerData[data.index.pk] = data
		print 'conatiner: ', container
		print 'containerData: ', containerData
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
		print 'search :: results: ', results
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
		print 'templates: ', templates
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
		print 'getMenus...'
		print 'appCode: ', self._ctx[Ctx.APP]
		view = self._dbView.get(name=viewName, application__code=self._ctx[Ctx.APP])
		print 'view: ', view
		# TODO: Play around to get list of codes using common methods
		print 'userChannel: ', self._ctx[Ctx.USER_CHANNEL]
		userAccessCodeList = []
		if self._ctx[Ctx.USER_CHANNEL] != None:
			userAccessList = self._dbAppAccess.search(userChannel=self._ctx[Ctx.USER_CHANNEL])
			for userAccess in userAccessList:
				userAccessCodeList.append(userAccess.application.code)
			print 'userAccessCodeList: ', userAccessCodeList
		# TODO: Remove the SN code simulator, use the one built from userChannel
		# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
		userAccessCodeList = ['SN']
		viewMenus = self._dbViewMenu.search( 	Q(menu__application__subscription = False) | 
							Q(menu__application__subscription = True) & 
							Q(menu__application__code__in=userAccessCodeList), view=view).order_by('order')
		#viewMenus = self._dbViewMenu.search( view=view ).order_by('order')
		print 'viewMenus: ', viewMenus
		print 'viewMenus All: ', self._dbViewMenu.getAll()
		menuDict = {}
		menuDict[Choices.MENU_ZONE_SYS] = []
		menuDict[Choices.MENU_ZONE_MAIN] = []
		menuDict[Choices.MENU_ZONE_VIEW] = []
		container = {}
		for viewMenu in viewMenus:
			print 'action: ', viewMenu.menu.action
			print 'view: ', viewMenu.menu.view
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
			menuObj['app'] = viewMenu.menu.view.application.code
			# params
			params = self._dbMenuParam.search(menu=viewMenu.menu)
			paramDict = {}
			# name, operator, value
			for param in params:
				if param.operator == Choices.OP_EQ:
					paramDict[param.name] = param.value
			menuObj['params'] = paramDict
			container[viewMenu.menu.name] = menuObj
			#print 'menuObj: ', menuObj
			if viewMenu.parent == None:
				menuObj['items'] = []
				if viewMenu.zone in ['sys','main']:
					if self._ctx[Ctx.IS_LOGIN]:
						menuDict[viewMenu.zone].append(menuObj)
					else:
						if viewMenu.menu.name == 'siteHome':
							menuDict[viewMenu.zone].append(menuObj) 
				else:
					menuDict[viewMenu.zone].append(menuObj)
			else:
				parentMenuObj = container[viewMenu.parent.menu.name]
				parentMenuObj['items'].append(menuObj)
		print 'menuDict: ', menuDict
		return menuDict

class EmailBusiness(object):
	#python -m smtpd -n -c DebuggingServer localhost:1025
	@staticmethod
	def send(xmlMessage, subsDict, recipientList):
		"""Send email
		@param keyName: keyName for datastore
		@subsDict : Dictionary with substitution values for template
		@param recipientList: List of emails to send message"""
		subject, message = ut_email.getMessage(xmlMessage)
		message = string.Template(message).substitute(**subsDict)
		send_mail(subject, message, settings.WEBMASTER_EMAIL, recipientList)


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
			#print 'DoBusinessDecorator :: data: ', argsTuple, argsDict
			try:
				#print 'DoBusinessDecorator :: ctx: ', obj._ctx.keys() 
				obj._ctx[Ctx.JS_DATA] = JsResultDict()
				if self._form != None:
					#obj._ctx[Ctx.FORM] = self._form()
					obj._setMainForm(self._form())
				f(*argsTuple, **argsDict)
				if not obj._ctx.has_key('_doneResult'):
					# Menu
					menu = MenuBusiness(obj._ctx)
					#menuDict = menu.getMenus(obj._ctx['viewNameSource'])
					menuDict = menu.getMenus('home')
					obj._ctx[Ctx.JS_DATA]['response']['menus'] = menuDict
					# Views
					if obj._ctx['viewNameTarget'] != '':
						obj._ctx[Ctx.JS_DATA]['response']['view'] = obj._ctx['viewNameTarget']
					else:
						obj._ctx[Ctx.JS_DATA]['response']['view'] = obj._ctx['viewNameSource']
					print 'DoBusinessDecorator :: view: ', '*' + obj._ctx[Ctx.JS_DATA]['response']['view'] + '*'
					# App
					obj._ctx[Ctx.JS_DATA]['response']['app'] = obj._ctx['app']
					# winType
					if len(obj._ctx[Ctx.JS_DATA]['response']['view'].strip()) != 0:
						dbView = ViewDAO(obj._ctx)
						view = dbView.get(application__code=obj._ctx[Ctx.APP], name=obj._ctx[Ctx.JS_DATA]['response']['view'])
						print 'winType: ', view.winType
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
							print 'tmplName: ', tmplName
						else:
							raise XpMsgException(None, _('Error in resolving template for view'))
						obj._ctx[Ctx.JS_DATA]['response'][Ctx.TMPL] = templates
					else:
						# In case we show only msg with no view, no template
						print 'no View, no template...'
						obj._ctx[Ctx.JS_DATA]['response'][Ctx.TMPL] = ''
					# Forms
					print 'forms: ', obj._ctx[Ctx.FORMS]
					for formId in obj._ctx[Ctx.FORMS]:
						form = obj._ctx[Ctx.FORMS][formId]
						if not obj._ctx[Ctx.JS_DATA].has_key(formId):
							form.buildJsData(obj._ctx[Ctx.JS_DATA])
							form.setApp(obj._ctx[Ctx.APP])
					print obj._ctx[Ctx.JS_DATA]['response'].keys()
					# Result
					print 'isServerTmpl: ', self._isServerTmpl
					if self._isServerTmpl == False:
						result = obj._buildJSONResult(obj._ctx[Ctx.JS_DATA])
						#print obj._ctx[Ctx.JS_DATA]
						print result
						for cookie in obj._ctx[Ctx.SET_COOKIES]:
							maxAge = 5*12*30*24*60*60
							result.set_cookie(cookie['key'], value=cookie['value'], domain=cookie['domain'], 
									expires = cookie['expires'], max_age=maxAge)
							print 'Did set cookie into result...', cookie
					else:
						result = obj._ctx[Ctx.JS_DATA]
						print result
					obj._ctx['_doneResult'] = True
				else:
					print 'I skip building response, since I already did it!!!!!'
					if self._isServerTmpl == False:
						result = obj._buildJSONResult(obj._ctx[Ctx.JS_DATA])
					else:
						result = obj._ctx[Ctx.JS_DATA]
				return result
			except XpMsgException as e:
				print 'ERROR!!!! DoBusinessDecorator!!!!!'
				errorDict = obj._getErrors()
				if len(errorDict) != 0:
					if self._isServerTmpl == False:
						result = obj._buildJSONResult(obj._getErrorResultDict(errorDict, pageError=self._pageError))
					else:
						result = obj._getErrorResultDict(errorDict, pageError=self._pageError)
					print result
				else:
					if settings.DEBUG == True:
						print errorDict
						print e
						print e.myException
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
			#print 'ValidateFormDecorator :: ', argsTuple, argsDict
			obj = argsTuple[0]
			#result = f(*argsTuple, **argsDict)
			obj._ctx[Ctx.JS_DATA] = JsResultDict()
			obj._ctx[Ctx.FORM] = self._form(obj._ctx[Ctx.POST])
			bForm = obj._ctx[Ctx.FORM].is_valid()
			#obj._ctx[Ctx.FORM] = obj._f
			print 'Form Validation: ', bForm
			if bForm == True:
				obj._setMainForm(obj._ctx[Ctx.FORM])
				result = f(*argsTuple, **argsDict)
				return result
				"""try:
					f(*argsTuple, **argsDict)
					obj._f.buildJsData(obj._ctx[Ctx.JS_DATA])
					result = obj.buildJSONResult(obj._ctx[Ctx.JS_DATA])
					#print result
					return result
				except XpMsgException as e:
					errorDict = obj.getErrors()
					if settings.DEBUG == True:
						print errorDict
						print e
						print e.myException
						traceback.print_exc()
					if len(errorDict) != 0:
						result = obj.buildJSONResult(obj.getErrorResultDict(errorDict, pageError=self._pageError))
					else:
						raise
					return result"""
				"""except Exception as e:
					if settings.DEBUG == True:
						print e
						traceback.print_exc()"""
			else:
				if settings.DEBUG == True:
					print 'Validation error!!!!!'
					#print obj._f
					print obj._ctx[Ctx.FORM].errors
					traceback.print_exc()
				errorDict = {'': 'Error validating your data. Check it out and send again'}
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
			#print 'WFViewstartDecorator :: ', argsTuple, argsDict
			obj = argsTuple[0]
			#obj._wf = WorkFlowBusiness(obj._ctx)
			obj._ctx[Ctx.FLOW_CODE] = self.__flowCode
			obj._ctx[Ctx.IS_FLOW] = True
			print 'flowCode: ', self.__flowCode
			flow = obj._wf.get(self.__flowCode)
			viewName = obj._ctx[Ctx.VIEW_NAME_SOURCE]
			print 'View Current: ', obj._ctx[Ctx.VIEW_NAME_SOURCE]
			# WorKflow User Id
			"""if obj._ctx[Ctx.COOKIES].has_key('wfUserId'):
				obj._ctx[Ctx.WF_USER_ID] = obj._ctx[Ctx.COOKIES]['wfUserId']
				print 'COOKIE :: WF User Id: ', obj._ctx[Ctx.WF_USER_ID]
			else:
				obj._ctx[Ctx.WF_USER_ID] = obj._wf.genUserId()
				obj._setCookie('wfUserId', obj._ctx[Ctx.WF_USER_ID])
				print 'WF UserId: ', obj._ctx[Ctx.WF_USER_ID]"""
			obj._ctx[Ctx.WF_USER_ID] = obj._getWFUser()
			print 'WF UserId: ', obj._ctx[Ctx.WF_USER_ID]
			hasFlow = True
			try:
				flowData = obj._wf.getFlowDataDict(obj._ctx[Ctx.WF_USER_ID], self.__flowCode)
				print 'flowData: ', flowData
			except XpMsgException:
				hasFlow = False
			print 'hasFlow: ', hasFlow
			if flow.jumpToView == True and hasFlow == True:
				# Get flow data, display view in flow data
				try:
					viewName = obj._wf.getView(obj._ctx[Ctx.WF_USER_ID], self.__flowCode)
					print 'Jump to View: ', obj._ctx[Ctx.VIEW_NAME_SOURCE], viewName
				except XpMsgException:
					pass
			else:
				isFirstView = obj._wf.isFirstView(self.__flowCode, obj._ctx[Ctx.VIEW_NAME_SOURCE])
				print 'Flow Data: ', hasFlow, isFirstView
				# Check that this view is first in flow
				if hasFlow == False and isFirstView == True:
					print 'reset Flow... no flow and first window'
					obj._wf.resetFlow(obj._ctx[Ctx.WF_USER_ID], self.__flowCode, obj._ctx[Ctx.VIEW_NAME_SOURCE])
				elif isFirstView == True and flow.resetStart == True:
					print 'reset Flow... resetStart=True and first view in flow...'
					obj._wf.resetFlow(obj._ctx[Ctx.WF_USER_ID], self.__flowCode, obj._ctx[Ctx.VIEW_NAME_SOURCE])
			obj._ctx['viewNameTarget'] = viewName
			# Jump to View in case jumpToView = True and viewName resolved from flow is different from current view
			#print 'Jumps... ', viewName, obj._ctx[Ctx.VIEW_NAME_SOURCE]
			if viewName != obj._ctx[Ctx.VIEW_NAME_SOURCE]:
				print 'redirect to ...', viewName				
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
			print 'MenuAction :: ', view.name
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
				#print 'viewNameSource: ', obj._ctx[Ctx.VIEW_NAME_SOURCE]
				#print 'viewNameTarget: ', obj._ctx[Ctx.VIEW_NAME_TARGET]
				#print 'actionName: ', obj._ctx[Ctx.ACTION]
				#obj._wf = WorkFlowBusiness()
				actionName = obj._ctx[Ctx.ACTION]
				flow = obj._wf.getFlowViewByAction(actionName).flow
				self.__app = flow.application.code
				print 'app: ', self.__app
				obj._ctx[Ctx.FLOW_CODE] = flow.code
				obj._ctx[Ctx.IS_FLOW] = True
				#print 'WFActionDecorator :: flowCode: ', obj._ctx[Ctx.FLOW_CODE]
				obj._ctx[Ctx.WF_USER_ID] = obj._ctx[Ctx.COOKIES]['wfUserId']
				print 'COOKIE :: WF User Id: ', obj._ctx[Ctx.WF_USER_ID]
				result = f(*argsTuple, **argsDict)
				# Resolve View
				#print 'session', 
				viewTarget = obj._wf.resolveView(obj._ctx[Ctx.WF_USER_ID], self.__app, obj._ctx[Ctx.FLOW_CODE], 
								obj._ctx[Ctx.VIEW_NAME_SOURCE], obj._ctx[Ctx.ACTION])
				viewName = viewTarget.name
				#print 'viewName: ', viewName
				# Insert view into workflow
				obj._wf.setViewName(viewName)
				viewAttrs = obj._wf.getViewParams(obj._ctx[Ctx.FLOW_CODE], viewName)
				#print 'viewAttrs: ', viewAttrs
				# Save workflow
				flowData = obj._wf.save(obj._ctx[Ctx.WF_USER_ID], obj._ctx[Ctx.FLOW_CODE])
				# Set Flow data dictionary into context
				obj._ctx[Ctx.FLOW_DATA] = obj._wf.buildFlowDataDict(flowData)
				#print 'flowDataDict: ', obj._ctx[Ctx.FLOW_DATA]
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
				print 'ERROR!!!! WFActionDecorator!!!!!'
				errorDict = obj._getErrors()
				if len(errorDict) != 0:
					result = obj._buildJSONResult(obj._getErrorResultDict(errorDict, pageError=True))
					print result
				else:
					if settings.DEBUG == True:
						print errorDict
						print e
						print e.myException
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
			#print 'resultJs: ', resultJs
			template = Template(args['ctx'])
			templates = template.resolve(self.__viewName)
			if templates.has_key(self.__viewName):
				tmplName = templates[self.__viewName]
				#print 'tmplName: ', tmplName
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
				self.__viewName = args['viewName'] if args.has_key('viewName') else ''
			else:
				self.__APP = 'site'
				self.__viewName = 'home'
			args['ctx'][Ctx.VIEW_NAME_SOURCE] = self.__viewName
			resultJs = f(request, **args)
			#print 'resultJs: ', resultJs
			template = Template(args['ctx'])
			templates = template.resolve(self.__viewName)
			if templates.has_key(self.__viewName):
				tmplName = templates[self.__viewName]
				#print 'tmplName: ', tmplName
				result = render_to_response( self.__APP + '/' + tmplName + '.html', RequestContext(request, 
													{	'result': json.dumps(resultJs),
														'settings': settings
													}))
			else:
				raise XpMsgException(None, _('Error in resolving template for view'))
			return result
		return wrapped_f
