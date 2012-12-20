import random
import os
from django.utils.translation import ugettext as _

from models import XpMsgException, CoreParam, Application, Action
from models import Menu, MenuParam, View, Workflow, Param, WFParamValue, WorkflowData
from models import WorkflowView, ViewMenu, SearchIndex, SearchIndexParam, Word, SearchIndexWord, XpTemplate, ViewTmpl

# Settings
from ximpia.core.util import getClass
settings = getClass(os.getenv("DJANGO_SETTINGS_MODULE"))

# Logging
import logging.config
logging.config.dictConfig(settings.LOGGING)
logger = logging.getLogger(__name__)

class CommonDAO(object):	

	_numberMatches = 0
	_ctx = None
	_model = None
	_relatedFields = ()
	_relatedDepth = None

	def __init__(self, ctx, relatedFields=(), relatedDepth=None, numberMatches=100):
		"""@param ctx: Context: 
		@param relatedFields: tuple containing the fields to fetch data in the same query
		@param relatedDepth: Number of depth relationships to follow. The higher the number, the bigger the query
		@param numberMatches: Number of rows for queries that support paging"""
		self._ctx = ctx
		self._relatedFields = relatedFields
		self._relatedDepth = relatedDepth
		self._numberMatches = numberMatches
		if relatedDepth != None and len(relatedFields) != 0:
			raise XpMsgException(None, _('relatedFields and relatedDepth cannot be combined. One of them must only be informed.'))
	
	def _processRelated(self):
		"""Process related objects using fields and depth, class attributes _relatedFields and _relatedDepth"""
		if len(self._relatedFields) != 0 or self._relatedDepth != None:
			if len(self._relatedFields) != 0:
				dbObj = self._model.objects.select_related(self._relatedFields)
			elif self._relatedDepth != None:
				dbObj = self._model.objects.select_related(depth=self._relatedDepth)
		else:
			dbObj = self._model.objects
		return dbObj
		
	def _cleanDict(self, dd):
		"""Clean dict removing xpXXX fields.
		@param dict: Dictionary
		@return: dictNew : New dictionary without xpXXX fields"""
		fields = dd.keys()
		dictNew = {}
		for sKey in fields:
			if sKey.find('xp') == 0:
				pass
			else:
				dictNew[sKey] = dd[sKey]
		return dictNew
	
	def _getPagingStartEnd(self, page, numberMatches):
		"""Get tuple (iStart, iEnd)"""
		iStart = (page-1)*numberMatches
		iEnd = iStart+numberMatches
		values = (iStart, iEnd)
		return values
	
	def _getCtx(self):
		"""Get context"""
		return self._ctx

	def _doManyById(self, model, idList, field):
		"""Does request for map for list of ids (one query). Then processes map and adds to object obtained objects.
		@param idList: List
		@param object: Model"""
		xpDict = self.getMap(idList, userModel=model)
		for idTarget in xpDict.keys():
			addModel = xpDict[idTarget]
			field.add(addModel)
	
	def _doManyByName(self, model, nameList, field):
		"""Does request for map for list of ids (one query). Then processes map and adds to object obtained objects.
		@param idList: List
		@param object: Model"""
		for value in nameList:
			fields = model.objects.get_or_create(name=value)
			nameModel = fields[0]
			field.add(nameModel)
	
	def _resolveDbName(self):
		"""Resolves the db name to use. Supports multiple masters and multiple slaves. Views use slaves. Actions use masters.
		Data about view or action is obtained from the context."""
		#TODO: Include application mapping with settings variable XIMPIA_DATABASE_APPS = {}
		# Build master and slave lists
		dbList = settings.DATABASES.keys()
		dbListMaster = []
		dbListSlave = []
		for dbNameI in dbList:
			if dbNameI == 'default' or dbNameI.find('master') == 0:
				dbListMaster.append(dbNameI)
			elif dbNameI.find('slave') == 0:
				dbListSlave.append(dbNameI)
		dbName = ''
		if self._ctx.isView == True:
			if len(dbListSlave) != 0:
				dbName = random.choice(dbListSlave)
			else:
				dbName = 'default'
		elif self._ctx.isAction == True:
			dbName = random.choice(dbListMaster)
		logger.debug('CommonDAO :: dbName: ' + dbName + ' view: ' + self._ctx.viewNameSource )
		return dbName
	
	def getMap(self, idList):
		"""Get object map for a list of ids 
		@param idList: 
		@param bFull: boolean : Follows all foreign keys
		@return: Dict[id]: object"""
		dd = {}
		if len(idList) != 0:
			dbObj = self._processRelated()
			fields = dbObj.using(self._resolveDbName()).filter(id__in=idList)
			for obj in fields:
				dd[obj.id] = obj
		return dd
	
	def getById(self, fieldId, bFull=False):
		"""Get model object by id
		@param id: Object id
		@param bFull: boolean : Follows all foreign keys
		@return: Model object"""
		try:
			dbObj = self._processRelated()
			obj = dbObj.using(self._resolveDbName()).get(id=fieldId)
		except Exception as e:
			raise XpMsgException(e, _('Error in get object by id ') + str(fieldId) + _(' in model ') + str(self._model))
		return obj
	
	def check(self, **qsArgs):
		"""Checks if object exists
		@param qsArgs: query arguments
		@return: Boolean"""
		try:
			dbObj = self._model.objects
			exists = dbObj.using(self._resolveDbName()).filter(**qsArgs).exists()
		except Exception as e:
			raise XpMsgException(e, _('Error in check object. Args: ') + str(qsArgs) + _(' in model ') + str(self._model))
		return exists
	
	def get(self, **qsArgs):
		"""Get object
		@param qsArgs: query arguments
		@return: Model Object"""
		try:
			logger.debug('dbName:' + self._resolveDbName())
			dbObj = self._processRelated()
			data = dbObj.using(self._resolveDbName()).get(**qsArgs)
		except Exception as e:
			raise XpMsgException(e, _('Error in get object. Args: ') + str(qsArgs) + _(' in model ') + str(self._model))
		return data	

	def save(self):
		"""Save database object, either insert or update"""
		try:
			self._model.save(using=self._resolveDbName())
		except Exception as e:
			raise XpMsgException(e, _('Error in save model ') + str(self._model))
		return self._model
	
	def search(self, *qsTuple, **qsArgs):
		"""Search model using filter. Support for related objects as FK to model"""
		try:
			dbObj = self._processRelated()
			filterList = dbObj.using(self._resolveDbName()).filter(*qsTuple, **qsArgs)
		except Exception as e:
			raise XpMsgException(e, _('Error in search operation. qsTuple: ') + str(qsTuple) + ' . Args: ' + str(qsArgs) + _(' in model ') + str(self._model))
		return filterList
	
	def create(self, **qsArgs):
		"""Create object
		@param qsArgs: Query arguments
		@return: Data Object"""
		try:
			dbObj = self._model.objects
			data = dbObj.using(self._resolveDbName()).create(**qsArgs)
		except Exception as e:
			raise XpMsgException(e, _('Error in create object. Args: ') + str(qsArgs) + _(' in model ') + str(self._model))
		return data
	
	def getCreate(self, **qsArgs):
		"""Get or create object. If exists, gets the current value. If does not exist, creates data.
		@param qsArgs: Query arguments
		@return: tuple (Data Object, bCreated)"""
		try:
			dbObj = self._model.objects
			xpTuple = dbObj.using(self._resolveDbName()).get_or_create(**qsArgs)
		except Exception as e:
			raise XpMsgException(e, _('Error in get or create object. Args: ') + str(qsArgs) + _(' in model ') + str(self._model))
		return xpTuple
	
	def deleteById(self, pk, real=False):
		"""Delete model object by id
		@param id: Object id
		@return: Model object"""
		try:
			if real == False:
				xpObject = self._model.objects.using(self._resolveDbName()).get(id=pk)
				xpObject.isDeleted = True
				xpObject.save(using=self._resolveDbName())
			else:
				xpObject = self._model.objects_del.using(self._resolveDbName()).get(id=pk)
				xpObject.delete()
		except Exception as e:
			raise XpMsgException(e, _('Error delete object by id ') + str(pk))
		return xpObject
	
	def deleteIfExists(self, real=False, **qsArgs):
		"""Delete row in case item exists.If does not exist, catches a DoesNotExist exception
		@param qsArgs: query arguments"""
		try:
			dbObj = self._model.objects
			try:
				if real == False:
					dbObj = self._model.objects.using(self._resolveDbName()).get(**qsArgs)
					dbObj.isDeleted = True
					dbObj.save(using=self._resolveDbName())
				else:
					dbObj = self._model.objects_del.using(self._resolveDbName()).get(**qsArgs)
					dbObj.delete()
			except self._model.DoesNotExist:
				pass	
		except Exception as e:
			raise XpMsgException(e, _('Error delete object. Args ') + str(qsArgs) + _(' in model ') + str(self._model))
	
	def delete(self, real=False, **qsArgs):
		"""Delete row. In case does not exist, throws model.DoesNotExist
		@param qsArgs: query arguments"""
		try:						
			if real == False:
				dbObj = self._model.objects.using(self._resolveDbName()).get(**qsArgs)
				dbObj.isDeleted = True
				dbObj.save(using=self._resolveDbName())
			else:
				dbObj = self._model.objects_del.using(self._resolveDbName()).get(**qsArgs)
				dbObj.delete()
			#dbObj.using(self._resolveDbName()).get(**qsArgs).delete()
		except Exception as e:
			raise XpMsgException(e, _('Error delete object. Args ') + str(qsArgs) + _(' in model ') + str(self._model))
	
	def filterData(self, **argsDict):
		"""Search a model table with ordering support and paging
		@param xpNumberMatches: Number of matches
		@param xpPage: Page
		@param xpOrderBy: Tuple of fields to order by
		@return: list : List of model objects"""
		try:
			iNumberMatches = self._numberMatches
			if argsDict.has_key('xpNumberMatches'):
				iNumberMatches = argsDict['xpNumberMatches']
			page = 1
			if argsDict.has_key('xpPage'):
				page = int(argsDict['xpPage'])
			iStart, iEnd = self._getPagingStartEnd(page, iNumberMatches)
			orderByTuple = ()
			if argsDict.has_key('xpOrderBy'):
				orderByTuple = argsDict['xpOrderBy']
			ArgsDict = self._cleanDict(argsDict)
			dbObj = self._processRelated()
			if len(orderByTuple) != 0:
				dbObj = self._model.objects.order_by(*orderByTuple)
			logger.debug( self._resolveDbName() )
			xpList = dbObj.using(self._resolveDbName()).filter(**ArgsDict)[iStart:iEnd]
		except Exception as e:
			raise XpMsgException(e, _('Error in search table model ') + str(self._model))
		return xpList
		
	def getAll(self):
		"""Get all rows from table
		@param bFull: boolean : Follows all foreign keys
		@return: list"""
		try:
			dbObj = self._processRelated()
			xpList = dbObj.using(self._resolveDbName()).all()
		except Exception as e:
			raise XpMsgException(e, _('Error in getting all fields from ') + str(self._model))
		return xpList
	
	def searchFields(self, fields, iPage=1, numberResults=100, orderBy=[], **args):
		"""Search table with paging, ordering for set of fields. listMap allows mapping from keys to model fields.
		@param fields: List of fields, like ['field1','field2', ... ]
		@param iPage: Page to be returned. Default=1
		@param numberResults: Number of results returned: Default: 100
		@param orderBy: Tuple of fields to order by: Default: []
		@return: xpList: ValuesQuerySet."""
		try:
			xpList = self.filterData(xpPage=iPage, xpNumberMatches=numberResults, xpOrderBy=orderBy, **args).values(*fields)
			return xpList
		except Exception as e:
			raise XpMsgException(e, _('Error in searching fields in model ') + str(self._model))

	ctx = property(_getCtx, None)

class CoreParameterDAO(CommonDAO):
	def __init__(self, ctx, *ArgsTuple, **ArgsDict):
		super(CoreParameterDAO, self).__init__(ctx, *ArgsTuple, **ArgsDict)
		self._model = CoreParam

class ApplicationDAO(CommonDAO):
	def __init__(self, ctx, *ArgsTuple, **ArgsDict):
		super(ApplicationDAO, self).__init__(ctx, *ArgsTuple, **ArgsDict)
		self._model = Application

class ActionDAO(CommonDAO):
	def __init__(self, ctx, *ArgsTuple, **ArgsDict):
		super(ActionDAO, self).__init__(ctx, *ArgsTuple, **ArgsDict)
		self._model = Action

class MenuDAO(CommonDAO):
	def __init__(self, ctx, *ArgsTuple, **ArgsDict):
		super(MenuDAO, self).__init__(ctx, *ArgsTuple, **ArgsDict)
		self._model = Menu

class ViewMenuDAO(CommonDAO):
	def __init__(self, ctx, *ArgsTuple, **ArgsDict):
		super(ViewMenuDAO, self).__init__(ctx, *ArgsTuple, **ArgsDict)
		self._model = ViewMenu

class MenuParamDAO(CommonDAO):
	def __init__(self, ctx, *ArgsTuple, **ArgsDict):
		super(MenuParamDAO, self).__init__(ctx, *ArgsTuple, **ArgsDict)
		self._model = MenuParam

class ViewDAO(CommonDAO):
	def __init__(self, ctx, *ArgsTuple, **ArgsDict):
		super(ViewDAO, self).__init__(ctx, *ArgsTuple, **ArgsDict)
		self._model = View

class WorkflowDAO(CommonDAO):
	def __init__(self, ctx, *ArgsTuple, **ArgsDict):
		super(WorkflowDAO, self).__init__(ctx, *ArgsTuple, **ArgsDict)
		self._model = Workflow

class WorkflowDataDAO(CommonDAO):
	def __init__(self, ctx, *ArgsTuple, **ArgsDict):
		super(WorkflowDataDAO, self).__init__(ctx, *ArgsTuple, **ArgsDict)
		self._model = WorkflowData

class ParamDAO(CommonDAO):
	def __init__(self, ctx, *ArgsTuple, **ArgsDict):
		super(ParamDAO, self).__init__(ctx, *ArgsTuple, **ArgsDict)
		self._model = Param

class WFParamValueDAO(CommonDAO):
	def __init__(self, ctx, *ArgsTuple, **ArgsDict):
		super(WFParamValueDAO, self).__init__(ctx, *ArgsTuple, **ArgsDict)
		self._model = WFParamValue

class WorkflowViewDAO(CommonDAO):
	def __init__(self, ctx, *ArgsTuple, **ArgsDict):
		super(WorkflowViewDAO, self).__init__(ctx, *ArgsTuple, **ArgsDict)
		self._model = WorkflowView

class SearchIndexDAO(CommonDAO):
	def __init__(self, ctx, *ArgsTuple, **ArgsDict):
		super(SearchIndexDAO, self).__init__(ctx, *ArgsTuple, **ArgsDict)
		self._model = SearchIndex

class SearchIndexParamDAO(CommonDAO):
	def __init__(self, ctx, *ArgsTuple, **ArgsDict):
		super(SearchIndexParamDAO, self).__init__(ctx, *ArgsTuple, **ArgsDict)
		self._model = SearchIndexParam

class WordDAO(CommonDAO):
	def __init__(self, ctx, *ArgsTuple, **ArgsDict):
		super(WordDAO, self).__init__(ctx, *ArgsTuple, **ArgsDict)
		self._model = Word

class SearchIndexWordDAO(CommonDAO):
	def __init__(self, ctx, *ArgsTuple, **ArgsDict):
		super(SearchIndexWordDAO, self).__init__(ctx, *ArgsTuple, **ArgsDict)
		self._model = SearchIndexWord

class TemplateDAO(CommonDAO):
	def __init__(self, ctx, *ArgsTuple, **ArgsDict):
		super(TemplateDAO, self).__init__(ctx, *ArgsTuple, **ArgsDict)
		self._model = XpTemplate

class ViewTmplDAO(CommonDAO):
	def __init__(self, ctx, *ArgsTuple, **ArgsDict):
		super(ViewTmplDAO, self).__init__(ctx, *ArgsTuple, **ArgsDict)
		self._model = ViewTmpl
