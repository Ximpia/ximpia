# coding: utf-8

import types
import datetime
import random
import os

from django.contrib.auth.models import User, Group as GroupSys
from django.utils.translation import ugettext as _

from models import XpMsgException, XpRegisterException, get_blank_wf_data
from models import View, Action, Application, ViewParamValue, Param, Workflow, WFParamValue, WorkflowView, ViewMenu, Menu, MenuParam, \
	SearchIndex, SearchIndexParam, SearchIndexWord, Word, XpTemplate, ViewTmpl, WorkflowData, ApplicationMeta, ApplicationTag, Service, \
	Condition, ViewMenuCondition, ServiceMenuCondition
from ximpia.site.models import Category, Tag, Group
from ximpia.util import resources
from models import CoreParam
import constants as K

# Settings
from ximpia.core.util import get_class
from ximpia.core.models import MetaKey, ServiceMenu
settings = get_class(os.getenv("DJANGO_SETTINGS_MODULE"))

# Logging
import logging.config
logging.config.dictConfig(settings.LOGGING)
logger = logging.getLogger(__name__)

from data import WorkflowDataDAO, WorkflowDAO, WFParamValueDAO, ParamDAO, ViewDAO, WorkflowViewDAO
from models import Context, JsResultDict
from choices import Choices

from ximpia.util.js import Form as _jsf

class AppCompRegCommonBusiness ( object ):
	_ctx = None
	def __init__(self, compName, ctx=None, doClean=False):
		"""Parent class for application component registering."""
		self._ctx = ctx
		appName = self.__getAppName(compName)
		self._reg = ComponentRegisterBusiness()
		if appName != None and doClean == True:
			self._reg.cleanAll(appName)
		self.views()
		self.templates()
		self.actions()
		self.flows()
		self.menus()
		self.viewMenus()
		self.search()
	def __getAppName(self, compName):
		return '.'.join(compName.split('.')[:2])
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
	
	def __getAppName(self, compName):
		return '.'.join(compName.split('.')[:2])
	
	def registerApp(self, compName, title=None, slug='', **args):
		"""
		
		Register application
		
		**Required Attributes**
		
		* ``compName``:StringType : Component name, __name__ from components module
		* ``title``:StringType : Application title
		* ``slug``:StringType : Application slug to show in urls 
		
		**Optional Attributes**
		
		* ``isAdmin``:BooleanType : Application is admin type
		* ``isSubscription``
		* ``isPrivate``
		* ``isAdmin``
		* ``developer``
		* ``developerOrg``
		* ``parentSlug``
		* ``meta``
		* ``category``:StringType
		* ``tags``:ListType
		
		**Returns**
		
		None
		
		"""
		if title == None or slug == '':
			raise XpRegisterException(AttributeError, 'registerApp requires title and slug attributes')
		name = self.__getAppName(compName)
		# Create group application if not exists
		logger.debug('registerApp :: slug: %s' % (slug) )
		category = Category.objects.get(name='Apps')
		logger.debug('registerApp :: category: %s' % (category) )
		groupSys, exists = GroupSys.objects.get_or_create(name=slug) #@UnusedVariable
		group, exists = Group.objects.get_or_create(group=groupSys, groupNameId=slug, category=category)
		try:
			app = Application.objects.get(name=name)
		except Application.DoesNotExist:
			app = Application(name=name, slug=slug) 
		app.title = title
		app.accessGroup = group
		# Optional data
		if args.has_key('isSubscription'):
			app.isSubscription = args['isSubscription']
		if args.has_key('isPrivate'):
			app.isPrivate = args['isPrivate']
		if args.has_key('isAdmin'):
			app.isAdmin = args['isAdmin']
		if args.has_key('developer'):
			app.developer = User.objects.get(username=args['developer'])
		if args.has_key('developerOrg'):
			app.developerOrg = Group.objects.get(name=args['developerOrg'])
		if args.has_key('parentSlug'):
			app.parent = Application.objects.get(slug=args['parentSlug'])
		if args.has_key('category'):
			app.category = Category.objects.get(name=args['category'])
		app.save()
		# Meta
		if args.has_key('meta'):
			# get meta keys
			metaKeys = MetaKey.objects.filter(name__in=args['meta'].keys())
			for metaKey in args['meta']:
				try:
					appMeta = ApplicationMeta.objects.get(application=app, meta=metaKeys.get(name=metaKey))
				except ApplicationMeta.DoesNotExist:
					ApplicationMeta.objects.create(application=app, meta=metaKeys.get(name=metaKey), value=args['meta'][metaKey])
		# Tags
		if args.has_key('tags'):
			tags = Tag.objects.filter(name__in=[args['tags']])
			for tag in tags:
				try:
					appTag = ApplicationTag.objects.get(application=app, tag=tags.filter(name=tag.name))
				except ApplicationTag.DoesNotExist:
					ApplicationTag.objects.create(application=app, tag=tags.filter(name=tag.name))
		logger.info( 'Registered application: %s' % (app) )
	
	def registerService(self, compName, serviceName=None, className=None):
		"""
		
		Register service
		
		**Required Attributes**
		
		* ``compName``
		* ``serviceName``
		* ``className``
		
		**Optional Attributes**
		
		**Returns**
		
		"""
		if serviceName == None or className == None:
			raise XpRegisterException(AttributeError, 'registerService requires serviceName and className')
		appName = self.__getAppName(compName)
		classPath = str(className).split("'")[1]
		app = Application.objects.get(name=appName)
		impl = classPath
		try:
			service = Service.objects.get(application=app, name=serviceName)
			service.implementation = impl
			service.save()
		except Service.DoesNotExist:
			Service.objects.create(application=app, implementation=impl, name=serviceName)
		logger.info( 'Registered service %s' % (serviceName) )
	
	def cleanAll(self, compName):
		"""
		
		Clean views, actions, workflows, menus, search and templates for application
		
		**Attributes**
		
		* ``compName`` : __name__ from components module. From this value we get the application name
		
		"""
		
		appName = self.__getAppName(compName)
		Application.objects.filter(name=appName).update(isDeleted=True)
		logger.info( 'deleted application %s' % appName )
		#View.objects.filter(application__name=appName).delete()
		#logger.info( 'deleted all views for %s' % appName )
		#Action.objects.filter(application__name=appName).delete()
		#logger.info( 'deleted all actions for %s' % appName )
		#Workflow.objects.filter(application__name=appName).delete()
		#WorkflowData.objects.filter(flow__application__name=appName).delete()
		#logger.info( 'deleted all flows for %s' % appName )
		#Menu.objects.filter(application__name=appName).delete()
		#logger.info( 'deleted all menus for %s' % appName )
		#XpTemplate.objects.filter(application__name=appName).delete()
		#logger.info( 'deleted all templates for %s' % appName )
	
	def registerServMenu(self, compName, serviceName=None, menus=[]):
		"""
		
		Register application menus for zone main and sys. Application menus will be shown for all views in an application
		
		**Required Attributes**
		
		* ``compName``
		* ``serviceName``
		* ``menus``
		
		**Optional Attributes**
		
		**Returns**
		
		None
		
		"""
		if len(menus) == 0 or serviceName == None:
			raise XpRegisterException(AttributeError, 'registerServMenu requires attributes serviceName and menus')
		appName = self.__getAppName(compName)
		app = Application.objects.get(name=appName)
		service = Service.objects.get(name=serviceName) #@UnusedVariable
		# Menu
		#ServiceMenu.objects.filter(service=service).delete()
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
				logger.debug( 'counter: %s' % (counter) )
				try:
					serviceMenu = ServiceMenu.objects.get(service=service, menu=menu)
				except ServiceMenu.DoesNotExist:
					serviceMenu = ServiceMenu(service=service, menu=menu)
				serviceMenu.hasSeparator = sep
				serviceMenu.zone=dd[K.ZONE]
				serviceMenu.order = counter
				serviceMenu.save()
				# conditions
				if K.CONDITIONS in dd:
					order = 10
					for name, action, value in map(lambda x: x.split(':'), dd[K.CONDITIONS].split(',')):
						condition = Condition.objects.get(name=name)
						ServiceMenuCondition.objects.create(serviceMenu=serviceMenu, condition=condition, action=action, value=value, 
														order=order)
						order += 10
				counterDict[dd[K.MENU_NAME]] = counter
				counter += 100
			except Menu.DoesNotExist:
				pass
		# Grouped Menus
		for groupName in groupDict:
			fields = groupDict[groupName]
			menuParent = Menu.objects.get(name=groupName)
			serviceMenuParent = ServiceMenu.objects.get(service=service, menu=menuParent)
			counter = serviceMenuParent.order + 10
			for dd in fields:
				if not dd.has_key(K.ZONE):
					dd[K.ZONE] = K.VIEW
				menu = Menu.objects.get(name=dd[K.MENU_NAME])
				sep = dd[K.SEP] if dd.has_key(K.SEP) else False
				#logger.debug( 'data: %s' % (view.name, menuParent.name, menu.name, sep, dd[K.ZONE], counter) )
				logger.debug( 'data: %s' % ( counter) )
				try:
					serviceMenu = ServiceMenu.objects.get(service=service, menu=menu)
				except ServiceMenu.DoesNotExist:
					serviceMenu = ServiceMenu(service=service, menu=menu)
				serviceMenu.hasSeparator = sep
				serviceMenu.zone=dd[K.ZONE]
				serviceMenu.order = counter
				serviceMenu.parent = serviceMenuParent
				serviceMenu.save()
				# conditions
				if K.CONDITIONS in dd:
					order = 10
					for name, action, value in map(lambda x: x.split(':'), dd[K.CONDITIONS].split(',')):
						condition = Condition.objects.get(name=name)
						ServiceMenuCondition.objects.create(serviceMenu=serviceMenu, condition=condition, action=action, value=value, 
														order=order)
						order += 10
				counter += 10
		logger.info( 'Registered menus for service %s' % (serviceName) )

	def registerCondition(self, compName, condition, rule):
		"""
		Register condition
		
		** Required Attributes **
		
		* ``compName``
		* ``condition``
		* ``rule``
		"""
		Condition.objects.get_or_create(name=condition, rule=rule)
		logger.info( 'Registered condition {}'.format(condition))

	def registerViewMenu(self, compName, viewName=None, menus=[]):
		"""
		
		Register views associated with a menu
		
		**Required Attributes**
		
		* ``compName``
		* ``viewName``
		* ``menus``: [zone, group, menu_name, conditions]

		**Optional Attributes**

		**Returns**

		None

		"""
		logger.info( 'register view Menus...' )
		if viewName == None or len(menus) == 0:
			raise XpRegisterException(AttributeError, 'registerViewMenu requires attributes viewName and menus')
		appName = self.__getAppName(compName)
		app = Application.objects.get(name=appName)
		view = View.objects.get(application=app, name=viewName)
		# Menu
		logger.info( 'View menus...' )
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
				#logger.info( 'data: %s' % (view.name, menu.name, sep, dd[K.ZONE], counter) )
				logger.info( 'data: %s' % (counter) )
				try:
					viewMenu = ViewMenu.objects.get(view=view, menu=menu)
				except ViewMenu.DoesNotExist:
					viewMenu = ViewMenu(view=view, menu=menu)
				viewMenu.hasSeparator = sep
				viewMenu.zone=dd[K.ZONE]
				viewMenu.order = counter
				viewMenu.save()
				# conditions
				if K.CONDITIONS in dd:
					order = 10
					for name, action, value in map(lambda x: x.split(':'), dd[K.CONDITIONS].split(',')):
						condition = Condition.objects.get(name=name)
						ViewMenuCondition.objects.create(viewMenu=viewMenu, condition=condition, action=action, value=value, 
														order=order)
						order += 10
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
				#logger.info( 'data: %s' % (view.name, menuParent.name, menu.name, sep, dd[K.ZONE], counter) )
				logger.info( 'data: %s' % ( counter) )
				try:
					viewMenu = ViewMenu.objects.get(view=view, menu=menu)
				except ViewMenu.DoesNotExist:
					viewMenu = ViewMenu(view=view, menu=menu)
				viewMenu.hasSeparator = sep
				viewMenu.zone=dd[K.ZONE]
				viewMenu.order = counter
				viewMenu.parent=viewMenuParent
				viewMenu.save()
				# conditions
				if K.CONDITIONS in dd:
					order = 10
					for name, action, value in map(lambda x: x.split(':'), dd[K.CONDITIONS].split(',')):
						condition = Condition.objects.get(name=name)
						ViewMenuCondition.objects.create(viewMenu=viewMenu, condition=condition, action=action, value=value, 
														order=order)
						order += 10
				counter += 10
		logger.info( 'Registered menus for view %s' % (viewName) )
	
	def cleanViews(self, compName):
		"""Clean all views for application."""
		appName = self.__getAppName(compName)
		View.objects.filter(application__name=appName).update(isDeleted=True)
		logger.info( 'deleted all views for %s' % appName )
	
	def registerView(self, compName, serviceName=None, viewName=None, className=None, method=None, winType=Choices.WIN_TYPE_WINDOW, 
				hasAuth=False, slug='', **args):
		"""Registers view
		
		**Required Attributes**
		
		* ``compName``
		* ``serviceName``
		* ``viewName``
		* ``className``
		* ``method``
		* ``winType``
		* ``hasUrl``
		* ``hasAuth``
		* ``slug``
		
		**Optional Attributes**
		
		* ``params``:DictType : View entry parameters entry by **args:DictType Having format name => [value1, value2, ...]
		* ``image``
		* ``meta``
		* ``category``
		* ``tags``
		
		**Returns**
		
		None
		
		"""		
		if viewName == None or className == None or method == None or slug == '':
			raise XpRegisterException(AttributeError, 'registerView requires viewName, className, method and slug attributes')
		appName = self.__getAppName(compName)
		# from impl take myClass and method
		# '.'.join(compName.split('.')[:2])
		classPath = str(className).split("'")[1]
		app = Application.objects.get(name=appName)
		service = Service.objects.get(name=serviceName)
		try:
			view = View.objects.get(application=app, service=service, name=viewName)
		except View.DoesNotExist:
			view = View(application=app, service=service, name=viewName)
		view.implementation = classPath + '.' + method
		view.winType = winType
		view.hasAuth = hasAuth
		view.slug = slug
		view.save()
		# Parameters
		for name in args:
			param = Param.objects.get(application=app, name=name)
			fields = args[name]
			for value in fields:
				theTuple = ViewParamValue.objects.get_or_create(view=view, name=param, operator='eq', value=value) #@UnusedVariable
		logger.info( 'Registered view %s' % (viewName) )
	
	def cleanActions(self, compName):
		"""Clean all actions for application.
		@param appCode: Application code"""
		appName = self.__getAppName(compName)
		Action.objects.filter(application__name=appName).update(isDeleted=True)
		logger.info( 'deleted all actions for %s' % appName )
	
	def registerAction(self, compName, serviceName=None, actionName=None, className=None, method=None, slug=None, **args):
		"""Registers action
		
		**Required Attributes**
		
		* ``compName``
		* ``serviceName``
		* ``actionName``
		* ``slug``
		* ``className``
		* ``method``
		
		**Optional Attributes**
		
		* ``hasAuth``
		
		**Returns**
		
		None
		"""
		if actionName == None or className == None or method == None or slug == None:
			raise XpRegisterException(AttributeError, 'registerAction requires actionName, slug, className and method attributes')
		appName = self.__getAppName(compName)
		classPath = str(className).split("'")[1]
		app = Application.objects.get(name=appName)
		service = Service.objects.get(name=serviceName)
		try:
			action = Action.objects.get(application=app, name=actionName, service=service)
		except Action.DoesNotExist:
			action = Action(application=app, name=actionName, service=service)
		action.slug = slug
		action.implementation = classPath + '.' + method
		if args.has_key('hasAuth'):
			action.hasAuth = args['hasAuth']
		action.save()
		logger.info('Registered action %s' % (actionName) )
	
	def registerParam(self, compName, name=None, title=None, paramType=None, isView=False, isWorkflow=False):
		"""Register view / workflow parameter
		
		**Required Attributes**
		
		* ``compName``
		* ``name``
		* ``title``
		* ``paramType``
		* ``isView``
		* ``isWorkflow``
		
		**Optional Attributes**
		
		**Returns**
		
		None
		
		"""
		if name == None or title == None or paramType == None:
			raise XpRegisterException(AttributeError, 'registerParam requires attributes name, title and paramType')
		appName = self.__getAppName(compName)
		app = Application.objects.get(name=appName)
		try:
			param = Param.objects.get(application=app, name=name)
		except Param.DoesNotExist:
			param = Param(application=app, name=name)
		param.title = title
		param.paramType=paramType
		param.view = isView
		param.workflow = isWorkflow
		param.save()
	
	def cleanFlows(self, compName):
		"""Clean all flows for application."""
		appName = self.__getAppName(compName)
		Workflow.objects.filter(application__name=appName).update(isDeleted=True)
		WorkflowData.objects.filter(flow__application__name=appName).update(isDeleted=True)
		logger.info( 'deleted all flows for %s' % appName )
	
	def registerFlow(self, compName, flowCode=None, resetStart=False, deleteOnEnd=False, jumpToView=True):
		"""
		Reister flow
		
		**Required Attributes**
		
		* ``flowCode``
		
		**Optional Attributes**
		
		* ``resetStart``
		* ``deleteOnEnd``
		* ``jumoToView``
		
		**Returns**
		
		None
		
		"""
		if flowCode == None:
			raise XpRegisterException(AttributeError, 'registerFlow requires flowCode')
		appName = self.__getAppName(compName)
		app = Application.objects.get(name=appName)
		try:
			flow = Workflow.objects.get(application=app, code=flowCode)
		except Workflow.DoesNotExist:
			flow = Workflow(application=app, code=flowCode)		
		flow.resetStart = resetStart
		flow.deleteOnEnd = deleteOnEnd
		flow.jumpToView = jumpToView
		flow.save()
		
	def registerFlowView(self, compName, flowCode=None, viewNameTarget=None, actionName=None, order=10, **args):
		"""
		Reister flow
		
		**Required Attributes**
		
		* ``flowCode``
		* ``viewNameTarget``
		* ``actionName``
		* ``order`` : Order to evaluate view target resolution
		
		**Optional Attributes**
		
		* ``params`` : Workflow parameters. Dictionary that contains the parameters to resolve views. Has the format name => (operator, value)
		* ``viewParams`` : View entry parameters
		* ``viewNameSource`` 
		
		**Returns**
		
		None
		
		"""
		if flowCode == None or viewNameTarget == None or actionName == None:
			raise XpRegisterException(AttributeError, """registerFlowView requires attributes flowCode, viewNameTarget,
															and actionName""")
		appName = self.__getAppName(compName)
		app = Application.objects.get(name=appName)
		
		viewTarget = View.objects.get(application=app, name=viewNameTarget)
		action = Action.objects.get(application=app, name=actionName)
		flow = Workflow.objects.get(code=flowCode)
		try:
			flow = WorkflowView.objects.get(flow=flow, viewTarget=viewTarget, action=action)
		except WorkflowView.DoesNotExist:
			flow = WorkflowView(flow=flow, viewTarget=viewTarget, action=action)
		if args.has_key('viewNameSource'):
			viewSource = View.objects.get(application=app, name=args['viewNameSource'])
			flow.viewSource = viewSource
		flow.order = order
		flow.save()		
		# Parameters
		if args.has_key('params'):
			for name in args['params']:
				operator, value = args['params'][name]
				wfParamValue, created = WFParamValue.objects.get_or_create(flow=flow, name=name, operator=operator, value=value) #@UnusedVariable
		# Entry View parameters
		# TODO: Complete entry view parameters
	
	def cleanMenu(self, compName):
		"""
		Clean all menus for application
		
		**Attributes**
		
		* ``compName``
		
		**Returns**
		
		None
		"""
		appName = self.__getAppName(compName)
		Menu.objects.filter(application__name=appName).update(isDeleted=True)
		logger.info( 'deleted all menus for %s' % appName )
	
	def registerMenu(self, compName, name='', **args):
		"""Register menu item
		
		**Required Attributes**
		
		* ``compName``
		* ``name``
		
		**Optional Attributes**
		
		* ``title``
		* ``iconName``
		* ``description``
		* ``actionName`` : Either actionName or viewName must be informed
		* ``viewName`` : Either actionName or viewName must be informed
		* ``url``
		* ``urlTarget``
		* ``params``:DictType
		
		**Returns**
		
		None
		"""
		if name == '':
			raise XpRegisterException(AttributeError, 'registerMenu requires attributes name')
		if not args.has_key('viewName') and not args.has_key('actionName'):
			raise XpRegisterException(AttributeError, """registerMenu requires menu items be lined to a view or action. Need to inform 
					either one.""")
		if not args.has_key('title') and not args.has_key('icon'):
			raise XpRegisterException(AttributeError, 'registerMenu needs either text or icon')
		appName = self.__getAppName(compName)
		app = Application.objects.get(name=appName)
		# Icon
		if args.has_key('iconName'):
			icon, created = CoreParam.objects.get_or_create(mode=K.PARAM_ICON, name=args['iconName'], value=args['iconName']) #@UnusedVariable
		# Menu
		try:
			menu = Menu.objects.get(name=name)
		except Menu.DoesNotExist:
			menu = Menu(	application=app,
							name=name
							)
			if args.has_key('title'):
				menu.title = args['title']
			if args.has_key('description'):
				menu.description = args['description']
			if args.has_key('iconName'):
				menu.icon = icon
		if args.has_key('url'):
			menu.url = args['url']
			menu.urlTarget = args['urlTarget']
		if args.has_key('actionName'):
			action = Action.objects.get(name=args['actionName'])
			menu.action = action
		if args.has_key('viewName'):
			view = View.objects.get(application__name=appName, name=args['viewName'])
			menu.view = view
		menu.save()
		# MenuParam
		if args.has_key('params'):
			for name in args['params']:
				operator, value = args['params'][name]
				menuValue, created = MenuParam.objects.get_or_create(menu=menu, name=name, operator=operator, value=value) #@UnusedVariable
	
	def registerSearch(self, compName, text='', viewName=None, actionName=None, **args):
		"""
		Register application operation. It will be used in view search.
		
		**Required Attributes**
		
		* ``compName``
		* ``text``
		* ``viewName``
		* ``actionName``
		
		**Optional Attributes**
		
		* ``params``
		
		**Returns**
		
		None
		"""
		if viewName == None and actionName == None:
			raise XpRegisterException(AttributeError, 'registerSearch requires either viewName or actionName')
		if text == '' or (viewName == None and actionName == None):
			raise XpRegisterException(AttributeError, 'registerSearch requires attributes text, viewName or actionName. ')
		appName = self.__getAppName(compName)
		wordList = resources.Index.parseText(text)
		logger.info( 'wordList: %s' % wordList )
		view = View.objects.get(name=viewName) if viewName != None else None
		action = Action.objects.get(name=actionName) if actionName != None else None
		app = Application.objects.get(name=appName)
		# Create search index
		try:
			search = SearchIndex.objects.get(application=app, title=text)
		except SearchIndex.DoesNotExist:
			search = SearchIndex(application=app, title=text)
		if view != None:
			search.view = view
		if action != None:
			search.action = action
		search.save()
		# delete all words for search in SearchIndexWord
		SearchIndexWord.objects.filter(index=search, word__word__in=wordList).delete()
		for wordName in wordList:
			# Word
			word, created = Word.objects.get_or_create(word=wordName) #@UnusedVariable
			# SearchIndexWord
			try:
				searchWord = SearchIndexWord.objects.get(word=word, index=search)
			except SearchIndexWord.DoesNotExist:
				searchWord = SearchIndexWord.objects.create(word=word, index=search) #@UnusedVariable
		if args.has_key('params'):
			for paramName in args['params']:
				param = Param.objects.get_or_create(application=app, name=paramName)
				indexParam = SearchIndexParam.objects.create(searchIndex=search, name=param, operator=Choices.OP_EQ, #@UnusedVariable
									value=args['params'][paramName])
	
	def cleanTemplates(self, compName):
		"""Clean templates for the application
		@param appCode: Application code"""
		appName = self.__getAppName(compName)
		XpTemplate.objects.filter(application__name=appName).update(isDeleted=True)
		logger.info( 'deleted all templates for %s' % appName )
	
	def registerTemplate(self, compName, viewName=None, name=None, **args):
		"""Register template
		
		**Required Attributes**
		
		* ``compName``
		* ``viewName``
		* ``name``
		
		**Optional Attributes**
		
		* ``language``
		* ``country``
		* ``winType``
		* ``device``
		* ``alias``
		
		**Returns**
		
		None
		"""
		if viewName == None or name == None:
			raise XpRegisterException(AttributeError, 'registerTemplate requires viewName and template name attributes')
		appName = self.__getAppName(compName)
		app = Application.objects.get(name=appName)
		view = View.objects.get(application=app, name=viewName) if viewName != None else None
		try:
			template = XpTemplate.objects.get(name=name)
		except XpTemplate.DoesNotExist:
			template = XpTemplate(application=app, name=name)
		if args.has_key('language'):
			template.language = args['language']
		if args.has_key('country'):
			template.country = args['country']
		if args.has_key('winType'):
			template.winType = args['winType']
		if args.has_key('device'):
			template.device = args['device']
		if args.has_key('alias'):
			template.alias = args['alias']
		else:
			template.alias = viewName		
		template.save()
		# View
		try:
			viewTmpl = ViewTmpl.objects.get(view=view, template=template)
		except ViewTmpl.DoesNotExist:
			ViewTmpl.objects.create(view=view, template=template)
		logger.info('Registered template %s for view %s' % (name, viewName) )
	
class WorkFlowBusiness (object):	
	_ctx = {}
	__wfData = {}
	
	def __init__(self, ctx):
		self._ctx = ctx
		self._dbWFData = WorkflowDataDAO(ctx, related_depth=2)
		self._dbWorkflow = WorkflowDAO(ctx, related_depth=2)
		self._dbWFView = WorkflowViewDAO(ctx, related_depth=2)
		self._dbWFParams = WFParamValueDAO(ctx, related_depth=2)
		self._dbView = ViewDAO(ctx)
		self._dbParam = ParamDAO(ctx)
		#self._dbWFViewParam = WFViewEntryParamDAO(ctx, related_depth=2)
		self.__wfData = get_blank_wf_data({})
	
	def gen_user_id(self):
		"""Generate workflow user id.
		@return: user_id"""
		user_id = ''
		while len(user_id) < 40:
			user_id += random.choice('0123456789abcde')
		return user_id
	
	def get(self, flow_code):
		"""Get flow."""
		flow = self._dbWorkflow.get(code=flow_code)
		return flow
	
	def resolve_flow_data_for_user(self, wf_user_id, flow_code):
		"""Resolves flow for user and session key.
		@param wf_user_id: Workflow User Id
		@param flow_code: Flow code
		@return: resolved_flow : Resolved flow for flow code , login user or session"""
		resolvedFlow = None
		flows = self._dbWFData.search(flow__code=flow_code, userId=wf_user_id)
		logger.debug( 'flows: %s' % (flows) )
		logger.debug( 'All: %s' % (self._dbWFData.getAll()) )
		if len(flows) > 0:
			resolvedFlow = flows[0]
		else:
			raise XpMsgException(None, _('Error in resolving workflow for user'))
		logger.debug( 'resolvedFlow: %s' % (resolvedFlow) )
		return resolvedFlow

	def resolve_view(self, wf_user_id, app_name, flow_code, view_name_source, action_name):
		"""Search destiny views with origin viewSource and operation actionName
		@param view_name_source: Origin view
		@param action_name: Action name
		@return: view_target"""
		viewTarget = ''
		flowViews = self._dbWFView.search(flow__application__name=app_name, flow__code=flow_code,
					viewSource__name=view_name_source, action__name=action_name).order_by('order')
		params = self._dbWFParams.search(flowView__in=flowViews)
		paramFlowDict = {}
		for param in params:
			if not paramFlowDict.has_key(param.flowView.flow.code):
				paramFlowDict[param.flowView.flow.code] = []
			paramFlowDict[param.flowView.flow.code].append(param)
		wfDict = self.getFlowDataDict(wf_user_id, flow_code)
		logger.debug( 'wfDict: %s' % (wfDict) )
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
		
	def put_params(self, **argsDict):
		"""Put list of workflow parameters in context
		@param argsDict: Argument dictionary"""
		flowCode = self._ctx.flowCode
		flow = self._dbWorkflow.get(code=flowCode) #@UnusedVariable
		if not self.__wfData:
			self.__wfData = get_blank_wf_data({})
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
	
	def save(self, wf_user_id, flow_code):
		"""Saves the workflow into database for user
		@param user: User
		@param flowCode: Flow code"""
		logger.debug( '__wfData: %s' % (self.__wfData) )
		flows = self._dbWFData.search(userId=wf_user_id, flow__code=flow_code)
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
		logger.debug( 'save :: flowData: %s' % (flowData) )
		flow.data = _jsf.encode64Dict(flowData)
		flow.save()
		return flow
	
	def reset_flow(self, wf_user_id, flow_code, view_name):
		"""Reset flow. It deletes all workflow variables and view name
		@param wf_user_id: Workflow User Id
		@param flow_code: Flow code"""
		try:
			flowData = self.resolveFlowDataForUser(wf_user_id, flow_code)
			logger.debug( 'resetFlow :: flowData: %s' % (flowData) )
			self.__wfData = get_blank_wf_data({})
			self.__wfData['viewName'] = view_name
			logger.debug( '__wfData: %s' % (self.__wfData) )
			# Update flow data
			view = self._dbView.get(name=view_name)
			flowData.data = _jsf.encode64Dict(self.__wfData)
			flowData.view = view
			flowData.save()
		except XpMsgException:
			# Create flow data
			logger.debug( 'create flow... %s' % (wf_user_id) )
			self.__wfData = get_blank_wf_data({})
			self.__wfData['viewName'] = view_name
			logger.debug( '__wfData: %s' % (self.__wfData) )
			view = self._dbView.get(name=view_name)
			workflow = self._dbWorkflow.get(code=flow_code)
			self._dbWFData.create(userId=wf_user_id, flow=workflow, data = _jsf.encode64Dict(self.__wfData), view=view)

	def set_view_name(self, view_name):
		"""Set view name in Workflow
		@param view_name: View name"""
		logger.debug( 'setViewName :: %s' % (self.__wfData) )
		self.__wfData['viewName'] = view_name
		logger.debug( self.__wfData )

	def get_view_name(self):
		"""Get workflow view name.
		@return: viewName"""
		return self.__wfData['viewName']
	
	def get_param(self, name):
		"""Get workflow parameter from context
		@param name: Name
		@return: Param Value"""
		return self.__wfData['data'][name]
	
	def get_param_from_ctx(self, name):
		"""Get flow parameter from context.
		@param name: Parameter name
		@return: Parameter value"""
		flowDataDict = self._ctx.flowData
		logger.debug( 'flowDataDict: %s type:%s' % (flowDataDict, type(flowDataDict)) )
		logger.debug( 'wfData: %s' % (self.__wfData) )
		return flowDataDict['data'][name]
		
	def build_flow_data_dict(self, flow_data):
		"""Build the flow data dictionary having the flowData instance.
		@param flowData: Flow data
		@return: flow_data_dict"""
		flowDataDict = _jsf.decode64dict(flow_data.data)
		logger.debug( 'build :: flowDataDict: %s' % (flowDataDict) )
		return flowDataDict
	
	def get_flow_data_dict(self, wf_user_id, flow_code):
		"""Get flow data dictionary for user and flow code
		@param wf_user_id: Workflow user id
		@param flow_code: flowCode
		@return: flow_data_dict : Dictionary"""
		flowData = self.resolveFlowDataForUser(wf_user_id, flow_code)
		flowDataDict = _jsf.decode64dict(flowData.data)
		logger.debug( 'get :: flowDataDict: %s' % (flowDataDict) )
		return flowDataDict
	
	def get_flow_view_by_action(self, action_name):
		"""Get flow by action name. It queries the workflow data and returns flow associated with actionName
		@param action_name: Action name
		@return: flow_view: Workflow view"""
		flowView = self._dbWFView.get(action__name=action_name)
		return flowView
	
	def get_view(self, wf_user_id, flow_code):
		"""Get view from flow
		@param wf_user_id: User
		@param flow_code: Flow code
		@return: view_name"""
		flowDataDict = self.getFlowDataDict(wf_user_id, flow_code)
		viewName = flowDataDict['viewName']
		return viewName
	
	def get_view_params(self, flow_code, view_name):
		"""Get view entry parameters for view and flow
		@param flow_code: Flow code
		@param view_name: View name
		@return: param_dict"""
		params = self._dbWFParams.search(flowView__flow__code=flow_code, flowView__viewTarget__name=view_name)
		logger.debug( 'params: %s' % (params) )
		paramDict = {}
		for param in params:
			paramDict[param.paramView.name] = param.paramView.value
		return paramDict

	def is_last_view(self, view_name_source, view_name_target, action_name):
		"""Checks if view is last in flow."""
		flowsView = self._dbWFView.search(viewSource__name=view_name_source, action__name=action_name).order_by('-order')
		flowView = flowsView[0] if len(flowsView) != 0 else None
		isLastView = False
		if flowView != None and flowView.viewTarget.name == view_name_target:
			isLastView = True
		return isLastView
	
	def is_first_view(self, flow_code, view_name):
		"""Checks if view is first in flow. It uses field 'order' to determine if is first view."""
		check = False
		flowViewStart = self._dbWFView.get(flow__code=flow_code, order=10)		
		if flowViewStart.viewSource.name == view_name:
			check = True
		else:
			check = False
		return check
	
	def remove_data(self, wf_user_id, flow_code):
		"""Removes the workflow data for user or session."""
		flowData = self.resolveFlowDataForUser(wf_user_id, flow_code)
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




































# =========================================
# Eclipse Dumb Classes for code completion
# =========================================

class ContextDumbClass (object):
	def __init__(self):
		if False: self._ctx = Context()
		if False: self._ctx.user = User()
		if False: self._ctx.jsData = JsResultDict()
