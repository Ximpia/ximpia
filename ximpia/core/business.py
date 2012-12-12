import types
import datetime
import random
import os

from django.utils.translation import ugettext as _

from models import XpMsgException, getBlankWfData
from models import View, Action, Application, ViewParamValue, Param, Workflow, WFParamValue, WorkflowView, ViewMenu, Menu, MenuParam, \
	SearchIndex, SearchIndexParam, SearchIndexWord, Word, XpTemplate, ViewTmpl, WorkflowData
from ximpia.util import resources
from models import CoreParam
import constants as K

# Settings
from ximpia.core.util import getClass
settings = getClass(os.getenv("DJANGO_SETTINGS_MODULE"))

# Logging
import logging.config
logging.config.dictConfig(settings.LOGGING)
logger = logging.getLogger(__name__)

from data import WorkflowDataDAO, WorkflowDAO, WFParamValueDAO, ParamDAO, ViewDAO, WorkflowViewDAO
from choices import Choices

from ximpia.util.js import Form as _jsf

class AppCompRegCommonBusiness ( object ):
	_ctx = None
	def __init__(self, ctx=None):
		"""Parent class for application component registering."""
		self._ctx = ctx
		self._reg = ComponentRegisterBusiness()
		self.main()
		self.views()
		self.templates()
		self.actions()
		self.flows()
		self.menus()
		self.viewMenus()
		self.search()
	def main(self):
		"""Doc."""
		pass
	def views(self):
		"""Doc."""
		pass
	def templates(self):
		"""Doc."""
		pass
	def actions(self):
		"""Doc."""
		pass
	def flows(self):
		"""Doc."""
		pass
	def menus(self):
		"""Doc."""
		pass
	def viewMenus(self):
		"""Doc."""
		pass
	def search(self):
		pass

class ComponentRegisterBusiness ( object ):
	
	def __init__(self):
		pass
	
	def registerApp(self, code=None, name=None, isAdmin=False):
		"""Register application
		@param code: Application code
		@param name: Application name
		@param isAdmin: Is app admin backdoor?. Values True / False"""
		app, created = Application.objects.get_or_create(code=code, name=name, isAdmin=isAdmin)
		logger.debug( 'Register application: %s %s' % (app, created) )
	
	def registerViewMenu(self, appCode=None, viewName=None, menus=[], **argsDict):
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
				#logger.debug( 'data: %s' % (view.name, menu.name, sep, dd[K.ZONE], counter) )
				logger.debug( 'data: %s' % (counter) )
				viewMenu, created = ViewMenu.objects.get_or_create(view=view, menu=menu, hasSeparator=sep, #@UnusedVariable
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
				#logger.debug( 'data: %s' % (view.name, menuParent.name, menu.name, sep, dd[K.ZONE], counter) )
				logger.debug( 'data: %s' % ( counter) )
				viewMenu, created = ViewMenu.objects.get_or_create(view=view, menu=menu, hasSeparator=sep, #@UnusedVariable
										zone=dd[K.ZONE], order=counter, parent=viewMenuParent)
				counter += 10
	
	def cleanViews(self, appCode=None):
		"""Clean all views for application."""
		View.objects.filter(application__code=appCode).delete()
		logger.debug( 'deleted all views for %s' % appCode )
	
	def registerView(self, appCode=None, viewName=None, myClass=None, method=None, menus=[], winType=Choices.WIN_TYPE_WINDOW, hasUrl=False,
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
		
	
	def cleanActions(self, appCode=None):
		"""Clean all actions for application.
		@param appCode: Application code"""
		Action.objects.filter(application__code=appCode).delete()
		logger.debug( 'deleted all actions for %s' % appCode )		
	
	def registerAction(self, appCode=None, actionName=None, myClass=None, method=None, hasUrl=False, hasAuth=True):
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
	
	def registerParam(self, appCode=None, name=None, title=None, paramType=None, isView=False, isWorkflow=False):
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

	def cleanFlows(self, appCode=None):
		"""Clean all flows for application."""
		Workflow.objects.filter(application__code=appCode).delete()
		WorkflowData.objects.filter(flow__application__code=appCode).delete()
		logger.debug( 'deleted all flows for %s' % appCode )
	
	def registerFlow(self, appCode=None, flowCode=None, resetStart=False, deleteOnEnd=False, jumpToView=True):
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
		
	def registerFlowView(self, appCode=None, flowCode=None, viewNameSource=None, viewNameTarget=None, actionName=None, order=10, 
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
	
	def cleanMenu(self, appCode=None):
		"""Clean all menus for application
		@param appCode: Application code"""
		Menu.objects.filter(application__code=appCode).delete()
		logger.debug( 'deleted all menus for %s' % appCode )
	
	def registerMenu(self, appCode=None, name='', titleShort='', title='', iconName='', actionName='', viewName='', url='', 
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
		logger.debug( 'paramDict: %s' % paramDict )
		menu = Menu.objects.create(**paramDict)
		# MenuParam
		logger.debug( 'argsDict: %s' % argsDict )
		for name in argsDict:
			operator, value = argsDict[name]
			menuValue, created = MenuParam.objects.get_or_create(menu=menu, name=name, operator=operator, value=value) #@UnusedVariable
		
	def cleanSearch(self, appCode=None):
		"""Clean Search information for view or action
		@param appCode: Application code"""
		try:
			SearchIndex.objects.filter(application__code=appCode).delete()
			logger.debug( 'deleted Search !!! %s' % appCode ) 
		except SearchIndex.DoesNotExist:
			pass

	def registerSearch(self, text='', appCode=None, viewName=None, actionName=None, params={}):
		"""Register application operation. It will be used in view search.
		@param text: Text to index
		@param appCode: Application code
		@param viewName: View name
		@param actionName: Action name"""
		wordList = resources.Index.parseText(text)
		logger.debug( 'wordList: %s' % wordList )
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
	
	def cleanTemplates(self, appCode=None):
		"""Clean templates for the application
		@param appCode: Application code"""
		XpTemplate.objects.filter(application__code=appCode).delete()
		logger.debug( 'deleted all templates for %s' % appCode )
	
	def registerTemplate(self, appCode=None, viewName=None, name=None, language=None, country=None, winType=Choices.WIN_TYPE_WINDOW, 
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
		#self._dbWFViewParam = WFViewEntryParamDAO(ctx, relatedDepth=2)
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
		flowCode = self._ctx.flowCode
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
		flowDataDict = self._ctx.flowData
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

class CommonBusiness ( object ):
	
	"""
	
	Common Business class for ximpia business logic.
	
	**Attributes**
	
	* ``ctx``:Dict : Context
	
	"""
	
	_ctx = None
	
	def __init__(self, ctx):
		self._ctx = ctx
