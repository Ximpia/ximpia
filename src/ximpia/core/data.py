from django.utils.translation import ugettext as _
from ximpia.core.models import XpMsgException, CoreParam, Application, Action, ApplicationAccess, CoreXmlMessage
from ximpia.core.models import Menu, MenuParam, View, Workflow, Param, WFParamValue, WorkflowData, WFViewEntryParam
from ximpia.core.models import WorkflowView, ViewMenu, SearchIndex, SearchIndexParam, Word, SearchIndexWord, XpTemplate, ViewTmpl

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
	
	def getMap(self, idList):
		"""Get object map for a list of ids 
		@param idList: 
		@param bFull: boolean : Follows all foreign keys
		@return: Dict[id]: object"""
		dd = {}
		if len(idList) != 0:
			"""if useModel != None:
				dbObj = self.useModel.objects
			else:
				dbObj = self._model.objects
			if bFull == True:
				dbObj = dbObj.select_related()"""
			dbObj = self._processRelated()
			fields = dbObj.filter(id__in=idList)
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
			obj = dbObj.get(id=fieldId)
		except Exception as e:
			raise XpMsgException(e, _('Error in get object by id ') + str(fieldId) + _(' in model ') + str(self._model))
		return obj
	
	def check(self, **qsArgs):
		"""Checks if object exists
		@param qsArgs: query arguments
		@return: Boolean"""
		try:
			dbObj = self._model.objects
			exists = dbObj.filter(**qsArgs).exists()
		except Exception as e:
			raise XpMsgException(e, _('Error in check object. Args: ') + str(qsArgs) + _(' in model ') + str(self._model))
		return exists
	
	def get(self, **qsArgs):
		"""Get object
		@param qsArgs: query arguments
		@return: Model Object"""
		try:
			dbObj = self._processRelated()
			data = dbObj.get(**qsArgs)
		except Exception as e:
			raise XpMsgException(e, _('Error in get object. Args: ') + str(qsArgs) + _(' in model ') + str(self._model))
		return data	
	
	def search(self, *qsTuple, **qsArgs):
		"""Search model using filter. Support for related objects as FK to model"""
		try:
			dbObj = self._processRelated()
			filterList = dbObj.filter(*qsTuple, **qsArgs)
		except Exception as e:
			raise XpMsgException(e, _('Error in search operation. qsTuple: ') + str(qsTuple) + ' . Args: ' + str(qsArgs) + _(' in model ') + str(self._model))
		return filterList
	
	def create(self, **qsArgs):
		"""Create object
		@param qsArgs: Query arguments
		@return: Data Object"""
		try:
			dbObj = self._model.objects
			data = dbObj.create(**qsArgs)
		except Exception as e:
			raise XpMsgException(e, _('Error in create object. Args: ') + str(qsArgs) + _(' in model ') + str(self._model))
		return data
	
	def getCreate(self, **qsArgs):
		"""Get or create object. If exists, gets the current value. If does not exist, creates data.
		@param qsArgs: Query arguments
		@return: tuple (Data Object, bCreated)"""
		try:
			dbObj = self._model.objects
			xpTuple = dbObj.get_or_create(**qsArgs)
		except Exception as e:
			raise XpMsgException(e, _('Error in get or create object. Args: ') + str(qsArgs) + _(' in model ') + str(self._model))
		return xpTuple
	
	def deleteById(self, xpId, real=False):
		"""Delete model object by id
		@param id: Object id
		@return: Model object"""
		try:
			xpObject = self._model.objects.get(id=xpId)
			if real == False:
				xpObject.isDeleted = True
				xpObject.save()
			else:
				xpObject.delete()
		except Exception as e:
			raise XpMsgException(e, _('Error delete object by id ') + str(xpId))
		return xpObject
	
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
			xpList = dbObj.filter(**ArgsDict)[iStart:iEnd]
		except Exception as e:
			raise XpMsgException(e, _('Error in search table model ') + str(self._model))
		return xpList
		
	def getAll(self):
		"""Get all rows from table
		@param bFull: boolean : Follows all foreign keys
		@return: list"""
		try:
			dbObj = self._processRelated()
			xpList = dbObj.all()
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

class ApplicationAccessDAO(CommonDAO):
	def __init__(self, ctx, *ArgsTuple, **ArgsDict):
		super(ApplicationAccessDAO, self).__init__(ctx, *ArgsTuple, **ArgsDict)
		self._model = ApplicationAccess

class CoreXMLMessageDAO(CommonDAO):
	def __init__(self, ctx, *ArgsTuple, **ArgsDict):
		super(CoreXMLMessageDAO, self).__init__(ctx, *ArgsTuple, **ArgsDict)
		self._model = CoreXmlMessage

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

class WFViewEntryParamDAO(CommonDAO):
	def __init__(self, ctx, *ArgsTuple, **ArgsDict):
		super(WFViewEntryParamDAO, self).__init__(ctx, *ArgsTuple, **ArgsDict)
		self._model = WFViewEntryParam

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
