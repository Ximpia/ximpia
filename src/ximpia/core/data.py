from django.utils.translation import ugettext as _
from ximpia.core.models import XpMsgException 

class CommonDAO(object):	

	NUMBER_MATCHES = 100
	_ctx = None
	_model = None
	_argsTuple = ()
	_argsDict = {}

	def __init__(self, ctx, *ArgsTuple, **ArgsDict):
		self._ctx = ctx
		self._argsTuple = ArgsTuple
		self._argsDict = ArgsDict
		
	def _cleanDict(self, dict):
		"""Clean dict removing xpXXX fields.
		@param dict: Dictionary
		@return: dictNew : New dictionary without xpXXX fields"""
		list = dict.keys()
		dictNew = {}
		for sKey in list:
			if sKey.find('xp') == 0:
				pass
			else:
				dictNew[sKey] = dict[sKey]
		return dictNew
	
	def _getPagingStartEnd(self, page, numberMatches):
		"""Get tuple (iStart, iEnd)"""
		iStart = (page-1)*numberMatches
		iEnd = iStart+numberMatches
		tuple = (iStart, iEnd)
		return tuple
	
	def getMap(self, idList, bFull=False, useModel=None):
		"""Get object map for a list of ids 
		@param idList: 
		@param bFull: boolean : Follows all foreign keys
		@return: Dict[id]: object"""
		dict = {}
		if len(idList) != 0:
			if useModel != None:
				dbObj = self.useModel.objects
			else:
				dbObj = self._model.objects
			if bFull == True:
				dbObj = dbObj.select_related()
			list = dbObj.filter(id__in=idList)
			for object in list:
				dict[object.id] = object
		return dict
	
	def getById(self, id, bFull=False):
		"""Get model object by id
		@param id: Object id
		@param bFull: boolean : Follows all foreign keys
		@return: Model object"""
		try:
			dbObj = self._model.objects
			if bFull == True:
				dbObj = self._model.objects.select_related()
			object = dbObj.get(id=id)
		except Exception as e:
			raise XpMsgException(e, _('Error in get object by id ') + str(id) + _(' in model ') + str(self._model))
		return object
	
	def check(self, qsArgs):
		"""Checks if object exists
		@param qsArgs: query arguments
		@return: Boolean"""
		try:
			dbObj = self._model.objects
			exists = dbObj.filter(**qsArgs).exists()
		except Exception as e:
			raise XpMsgException(e, _('Error in get object by id ') + str(id) + _(' in model ') + str(self._model))
		return exists
	
	def get(self, qsArgs):
		"""Get object
		@param qsArgs: query arguments
		@return: Model Object"""
		try:
			dbObj = self._model.objects
			data = dbObj.get(**qsArgs)
		except Exception as e:
			raise XpMsgException(e, _('Error in get object ') + str(id) + _(' in model ') + str(self._model))
		return data
	
	def create(self, qsArgs, bPassword=False, password=''):
		"""Create object
		@param qsArgs: Query arguments
		@param bPassword: True / False if password must be set
		@param password: Password value
		@return: Data Object"""
		try:
			dbObj = self._model.objects
			data = dbObj.create(**qsArgs)
			if bPassword == True:
				data.set_password(password)
				data.save()
		except Exception as e:
			raise XpMsgException(e, _('Error in create object ') + str(id) + _(' in model ') + str(self._model))
		return data
	
	def getCreate(self, qsArgs):
		"""Get or create object. If exists, gets the current value. If does not exist, creates data.
		@param qsArgs: Query arguments
		@return: tuple (Data Object, bCreated)"""
		try:
			dbObj = self._model.objects
			xpTuple = dbObj.get_or_create(**qsArgs)
		except Exception as e:
			raise XpMsgException(e, _('Error in get or create object ') + str(id) + _(' in model ') + str(self._model))
		return xpTuple
	
	def deleteById(self, xpId):
		"""Delete model object by id
		@param id: Object id
		@return: Model object"""
		try:
			xpList = self._model.objects.filter(id=xpId)
			xpObject = xpList[0]
			xpList.delete()
		except Exception as e:
			raise XpMsgException(e, _('Error delete object by id ') + str(id))
		return xpObject
	
	def filterData(self, bFull=False, **ArgsDict):
		"""Search a model table with ordering support and paging
		@param bFull: boolean : Follows all foreign keys
		@return: list : List of model objects"""
		try:
			iNumberMatches = self.NUMBER_MATCHES
			if ArgsDict.has_key('xpNumberMatches'):
				iNumberMatches = ArgsDict['xpNumberMatches']
			page = 1
			if ArgsDict.has_key('xpPage'):
				page = int(ArgsDict['xpPage'])
			iStart, iEnd = self._getPagingStartEnd(page, iNumberMatches)
			orderByTuple = ()
			if ArgsDict.has_key('xpOrderBy'):
				orderByTuple = ArgsDict['xpOrderBy']
			ArgsDict = self._cleanDict(ArgsDict)
			dbObj = self._model.objects
			if bFull == True:
				dbObj = self._model.objects.select_related()
			if len(orderByTuple) != 0:
				dbObj = self._model.objects.order_by(*orderByTuple)
			xpList = dbObj.filter(**ArgsDict)[iStart:iEnd]			
		except Exception as e:
			raise XpMsgException(e, _('Error in search table model ') + str(self._model))
		return xpList	
		
	def getAll(self, bFull=False):
		"""Get all rows from table
		@param bFull: boolean : Follows all foreign keys
		@return: list"""
		try:
			dbObj = self._model.objects
			if bFull == True:
				dbObj = self._model.objects.select_related()
			xpList = dbObj.all()
		except Exception as e:
			raise XpMsgException(e, _('Error in getting all fields from ') + str(self._model))
		return xpList
	
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
			nameModel, bCreate = model.objects.get_or_create(name=value)
			field.add(nameModel)

	ctx = property(_getCtx, None)
