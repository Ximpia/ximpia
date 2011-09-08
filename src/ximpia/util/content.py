# -*- coding: utf-8 -*-

import string
import os
import MySQLdb
import socket
import re
import zlib
import time
import cPickle
import types

#import octopusdbm
#from octopusdbm.client import Dbm
from bsddb3 import db

#import config
import xml_lib
import http

"""Copyright (c) 2010 Tecor Communications S.L.
All rights reserved."""

DEVELOPMENT_ENVIRONMENT = False
DEVELOPMENT_ENVIRONMENT_FS = True
ENVIRONMENT_TRAC = False
DEVELOPMENT_HOME = 'H:/workspace/'
UNICODE_CHARSET = 'utf-8'

INDEX_TYPE_TAG = 'tag'
INDEX_TYPE_TOPIC = 'topic'
INDEX_TYPE_KEYWORD = 'keyword'
CONTENT_WEIGHT_DEFAULT = 75

def showStatic(request, sLang, sTheme, LinksDict, sXmlKey):
	ParameterDict = {}
	ParameterDict['lnk_d'] = LinksDict
	ParameterDict['theme'] = sTheme
	ParameterDict['lang'] = sLang
	ParameterDict['user'] = request.user
	ContextDict = {'p': ParameterDict, 'tables_xml': None}
	return ContextDict

def writeTmp(fileName, value):
	if DEVELOPMENT_ENVIRONMENT_FS:
		pathTmp = 'H:/workspace/BuscaplusWeb/tmp/' + fileName
	else:
		pathTmp = '/mnt/django_projects/BuscaplusWeb/tmp/' + fileName
	f = open(pathTmp, 'w')
	f.write(value)
	f.close()

def writeListTmp(TupleList):
	PathList = []
	for Tuple in TupleList:
		fileName, value = Tuple
		if DEVELOPMENT_ENVIRONMENT_FS:
			pathTmp = 'H:/workspace/BuscaplusWeb/tmp/' + fileName
		else:
			pathTmp = '/mnt/django_projects/BuscaplusWeb/tmp/' + fileName
		f = open(pathTmp, 'w')
		f.write(value)
		f.close()
		PathList.append(pathTmp)
	return PathList

def deleteListTmp(PathList):
	for path in PathList:
		os.remove(path)

def getTmp(fileName):
	if DEVELOPMENT_ENVIRONMENT_FS:
		pathTmp = 'H:/workspace/BuscaplusWeb/tmp/' + fileName
	else:
		pathTmp = '/mnt/django_projects/BuscaplusWeb/tmp/' + fileName
	f = open(pathTmp)
	value = f.read()
	f.close()
	return value

def getXml(sEnv, sTableName, sKey, **ArgsDict):
	"""Get xml for sEnv and table sTableName. -> xml."""
	if DEVELOPMENT_ENVIRONMENT:
		sKey = sKey.replace('/', '_')
		path = 'H:/workspace/BuscaplusWeb/xml/' + sEnv + '/' + sTableName + '/' + sKey + '.xml'
		f = open(path)
		xml = f.read()
		f.close()
	else:
		#xmlMainTables = config.getDirectEnv(sEnv, sTableName, sKey)
		if type(sKey) == types.UnicodeType:
			sKeyNew = sKey.encode(UNICODE_CHARSET)
		else:
			sKeyNew = sKey
		oDbmd = config.Dbmd()
		MyDbm = oDbmd.connectByHost(config.DBM_HOSTNAME, sEnv)
		xml = MyDbm.getDirect(sTableName, sKeyNew, **ArgsDict)
	return xml

def putXml(sEnv, sTableName, sKey, sValue, bDup=None):
	"""Put xml for sEnv and table sTableName. -> xml."""
	if DEVELOPMENT_ENVIRONMENT:
		sKey = sKey.replace('/', '_')
		path = 'H:/workspace/BuscaplusWeb/xml/' + sEnv + '/' + sTableName + '/' + sKey + '.xml'
		f = open(path, 'w')
		f.write(sValue)
		f.close()
	else:
		#xmlMainTables = config.getDirectEnv(sEnv, sTableName, sKey)
		if type(sKey) == types.UnicodeType:
			sKeyNew = sKey.encode(UNICODE_CHARSET)
		else:
			sKeyNew = str(sKey)
		if type(sValue) == types.UnicodeType:
			sValueNew = sValue.encode(UNICODE_CHARSET)
		else:
			sValueNew = str(sValue)
		oDbmd = config.Dbmd()
		MyDbm = oDbmd.connectByHost(config.DBM_HOSTNAME, sEnv)
		if bDup == None:
			MyDbm.putDirect(sTableName, sKeyNew, sValueNew)
		else:
			if bDup == True:
				MyDbm.set_flags(db.DB_DUP)
				MyDbm.putDirect(sTableName, sKeyNew, sValueNew)
			else:
				MyDbm.putDirect(sTableName, sKeyNew, sValueNew)

def putXmlList(sEnv, sTableName, DataList, **ArgsDict):
	"""Get xml for sEnv and table sTableName. -> xml."""
	if DEVELOPMENT_ENVIRONMENT:
		XmlList = []
		for Tuple in DataList:
			sKey, sValue = Tuple
			sKey = sKey.replace('/', '_')
			path = 'H:/workspace/BuscaplusWeb/xml/' + sEnv + '/' + sTableName + '/' + sKey + '.xml'
			f = open(path, 'w')
			f.write(sValue)
			f.close()
	else:
		#xmlMainTables = config.getDirectEnv(sEnv, sTableName, sKey)
		oDbmd = config.Dbmd()
		MyDbm = oDbmd.connectByHost(config.DBM_HOSTNAME, sEnv)
		oDbmd.putListDirect(sTableName, DataList, **ArgsDict)

def getXmlList(sEnv, sTableName, KeyList, **ArgsDict):
	"""Get xml for sEnv and table sTableName. -> xml."""
	if DEVELOPMENT_ENVIRONMENT:
		XmlList = []
		for sKey in KeyList:
			sKey = sKey.replace('/', '_')
			path = DEVELOPMENT_HOME + 'BuscaplusWeb/xml/' + sEnv + '/' + sTableName + '/' + sKey + '.xml'
			f = open(path)
			xml = f.read()
			f.close()
			XmlList.append(xml)
	else:
		#xmlMainTables = config.getDirectEnv(sEnv, sTableName, sKey)
		oDbmd = config.Dbmd()
		MyDbm = oDbmd.connectByHost(config.DBM_HOSTNAME, sEnv)
		KeyNewList = []
		for sKey in KeyList:
			if type(sKey) == types.UnicodeType:
				KeyNewList.append(sKey.encode(UNICODE_CHARSET))
			else:
				KeyNewList.append(sKey)
		XmlList = MyDbm.getListDirect(sTableName, KeyNewList, sType=octopusdbm.client.TYPE_LIST, **ArgsDict)
	return XmlList

def getContextsList(ContextDataList):
	# Now -> Make N calls to dbmd. Future -> Use a single call for all environments and tables
	ResultList = []
	#EnvList = ContextDataDict.keys()
	for FieldList in ContextDataList:
		EnvTuple, DataList = FieldList
		sEnvName, sTableName = EnvTuple
		ContextList = []
		ContextDict = {}
		for Tuple in DataList:
			ContextList.append(Tuple[0])
			ContextDict[Tuple[0]] = Tuple[1]
		sContextId = ''
		XmlContentList = getXmlList(sEnvName, sTableName, ContextList)
		i = 0
		for xml in XmlContentList:
			PageXML = xml_lib.PageXML()
			PageXML.parse(xml)
			sContextId = ContextDict[ContextList[i]]
			Dict = PageXML.getContainerDict(sContextId)
			ResultList.append(Dict)
			i += 1
	return ResultList

def getQueryCache(sAccount, sKey):
	sEnv = 'query_cache'
	if DEVELOPMENT_ENVIRONMENT:
		Fields = sKey.split('&')
		sQuery = Fields[0]
		try:
			path = DEVELOPMENT_HOME + 'BuscaplusWeb/data/' + sEnv + '/' + sAccount + '/' + sQuery
			if os.path.isfile(path):
				f = open(path, 'rb')
				SDictC = f.read()
				f.close()
				if SDictC:
					SDict = zlib.decompress(SDictC)
					CacheDict = cPickle.loads(SDict)
					xml = CacheDict['xml']
				else:
					xml = None
			else:
				xml = None
		except UnicodeDecodeError:
			xml = None
	else:
		oDbmd = config.Dbmd()
		MyDbm = oDbmd.connectByHost(config.DBM_HOSTNAME, sEnv)
		SDictC = MyDbm.getDirect(sAccount + '.db', sKey, db.DB_BTREE, db.DB_CREATE)
		if SDictC:
			try:
				SDict = zlib.decompress(SDictC)
				CacheDict = cPickle.loads(SDict)
				xml = CacheDict['xml']
			except:
				xml = None
		else:
			xml = None
	return xml

def putQueryCache(sAccount, sKey, xml):
	sEnv = 'query_cache'
	if DEVELOPMENT_ENVIRONMENT:
		Fields = sKey.split('&')
		sQuery = Fields[0]
		Dict = {}
		Dict['xml'] = xml
		TimeTuple = time.localtime()
		timeStampStr = time.strftime('%Y-%m-%d', TimeTuple)
		Dict['date_create'] = timeStampStr
		Dict['date_update'] = ''
		SDict= cPickle.dumps(Dict, 1)
		SDictC = zlib.compress(SDict)
		try:
			path = DEVELOPMENT_HOME + 'BuscaplusWeb/data/' + sEnv + '/' + sAccount + '/' + sQuery
			f = open(path, 'wb')
			f.write(SDictC)
			f.close()
		except:
			pass
	else:
		oDbmd = config.Dbmd()
		MyDbm = oDbmd.connectByHost(config.DBM_HOSTNAME, sEnv)
		Dict = {}
		Dict['xml'] = xml
		TimeTuple = time.localtime()
		timeStampStr = time.strftime('%Y-%m-%d', TimeTuple)
		Dict['date_create'] = timeStampStr
		Dict['date_update'] = ''
		SDict= cPickle.dumps(Dict, 1)
		SDictC = zlib.compress(SDict)
		MyDbm.putDirect(sAccount + '.db', sKey, SDictC, db.DB_BTREE, db.DB_CREATE)

def resetQueryCache(sAccount):
	sEnv = 'query_cache'
	oDbmd = config.Dbmd()
	MyDbm = oDbmd.connectByHost(config.DBM_HOSTNAME, sEnv)
	MyDbm.open(sAccount + '.db', db.DB_BTREE, db.DB_CREATE)
	MyDbm.truncate()
	MyDbm.close()

def formatQ(sLang, sInteger):
	"""Format a quantity sInteger according to language rules. For english language include ',' and for others '.'."""
	orig = sInteger
	CommaDict = {'en': ''}
	PointDict = {'es': '', 'ca': '', 'eu': '', 'pt': ''}
	if CommaDict.has_key(sLang):
		new = re.sub("^(-?\d+)(\d{3})", '\g<1>,\g<2>', orig)
	elif PointDict.has_key(sLang):
		new = re.sub("^(-?\d+)(\d{3})", '\g<1>.\g<2>', orig)
	else:
		new = re.sub("^(-?\d+)(\d{3})", '\g<1>.\g<2>', orig)
	if orig == new:
		return new
	else:
		return formatQ(sLang, new)

def formatD(sLang, sDecimal):
	if sLang != 'en':
		sDecimal = sDecimal.replace('.',',')
	return sDecimal

def getNumberPages(iCounter, iMatchesPerPage):
	if iCounter%iMatchesPerPage == 0:
		iNumberPages = iCounter/iMatchesPerPage
	else:
		iNumberPages = (iCounter/iMatchesPerPage) + 1
	if iNumberPages == 0:
		iNumberPages = 1
	return iNumberPages

def groupAccountList(AccountList, iTmpCounter, iPage, iMatchesPerPage=8):
	iComp = iTmpCounter-(iPage)*iMatchesPerPage
	print 'iComp->', iComp
	if iComp > iMatchesPerPage:
		iCounter = iMatchesPerPage
	else:
		iCounter = len(AccountList)
	print 'iCounter->', iCounter
	if iCounter == 8:
		AccountList_1 = []
		AccountList_2 = []
		for i in range(4):
			AccountList_1.append((i+1, AccountList[i]))
		for i in range(4,8):
			AccountList_2.append((i+1, AccountList[i]))		
	else:
		if iCounter > 4:
			AccountList_1 = []
			for i in range(4):
				AccountList_1.append((i+1, AccountList[i]))
			AccountList_2 = []
			iCounterDiff = iCounter-4
			for i in range(4,4+iCounterDiff):
				AccountList_2.append((i+1, AccountList[i]))
			for i in range(4+iCounterDiff, 8):
				AccountList_2.append((i+1, ''))
		else:
			AccountList_1 = []
			for i in range(iCounter):
				AccountList_1.append((i+1, AccountList[i]))
			for i in range(iCounter, 4):
				AccountList_1.append((i+1, ''))
			AccountList_2 = [(5,''),(6,''),(7,''),(8,'')]
	return [AccountList_1, AccountList_2]

def includeBlankAccounts(AccountList, iCounter):
	#print AccountList, iCounter
	FinalAccountList = []
	if iCounter < 4:
		FinalAccountList = []
		for i in range(iCounter):
			FinalAccountList.append((i+1, AccountList[i]))
		for i in range(iCounter, 4):
			FinalAccountList.append((i+1, ''))
	else:
		FinalAccountList = []
		i = 0
		for Account in AccountList:
			FinalAccountList.append((i+1, Account))
			i += 1
	if len(FinalAccountList) != 4:
		iDiff = 4-len(FinalAccountList)
		for i in range(iDiff,4):
			FinalAccountList.append((i+1, ''))
	return FinalAccountList

def buildCombo(Dict, sSelected=None, bSortKeys=False):
	if not sSelected:
		if bSortKeys:
			List = Dict.keys()
			TupleList = []
			List.sort()
			for sKey in List:
				TupleList.append((sKey, Dict[sKey]))
		else:
			ValueList = Dict.values()
			ValueList.sort()
			TupleList = []
			List = Dict.keys()
			DictInv = {}
			ValueUniqueList = []
			for sKey in List:
				if DictInv.has_key(Dict[sKey]):
					DictInv[Dict[sKey]].append(sKey)
				else:
					DictInv[Dict[sKey]] = [sKey]
					ValueUniqueList.append(Dict[sKey])
			ValueUniqueList.sort()
			for sValue in ValueUniqueList:
				KeyList = DictInv[sValue]
				for sKey in KeyList:
					TupleList.append((sKey, sValue))
	else:
		if bSortKeys:
			List = Dict.keys()
			TupleList = []
			List.sort()
			for sKey in List:
				if sSelected == sKey:
					TupleList.append((sKey, Dict[sKey], True))
				else:
					TupleList.append((sKey, Dict[sKey], False))
		else:
			ValueList = Dict.values()
			ValueList.sort()
			TupleList = []
			List = Dict.keys()
			DictInv = {}
			ValueUniqueList = []
			for sKey in List:
				if DictInv.has_key(Dict[sKey]):
					DictInv[Dict[sKey]].append(sKey)
				else:
					DictInv[Dict[sKey]] = [sKey]
					ValueUniqueList.append(Dict[sKey])
			ValueUniqueList.sort()
			for sValue in ValueUniqueList:
				KeyList = DictInv[sValue]
				for sKey in KeyList:
					if sSelected == sKey:
						TupleList.append((sKey, sValue, True))
					else:
						TupleList.append((sKey, sValue, False))
	return TupleList

def getChoices(sTable, id):
	"""Gets valid choices for values in combos and other elements. We get values for spanish language since the values are the same for all languages. -> List ((value, string)...)."""
	sLang = 'es'
	xmlTables = getXml('xml_web', 'tables.db', sTable + '/' + sLang)
	TablesXML = xml_lib.PageXML()
	TablesXML.parse(xmlTables)
	Dict = TablesXML.getContainerDict(id)
	List = buildCombo(Dict)
	return List

def getAuthControlPanel(request, oUser):
	"""Get authorization to view pages in control panel. Admin and staff can view any user info. Normal users only view their own information."""
	bAuth = False
	sUser = oUser.username
	iAdmin = len(request.user.groups.filter(name="Admin"))
	if request.user.is_authenticated():
		if request.user.username == sUser:
			bAuth = True
		elif request.user.username != sUser and iAdmin != 0:
			bAuth = True
	return bAuth

def getAuthAdmin(request, oUser=None):
	if not oUser:
		oUser = request.user
	bAdmin = False
	if len(oUser.groups.filter(name="Admin")) != 0:
		bAdmin = True
	return bAdmin

def getLocalizedDate(sDate, MonthDict):
	"""sDate having form day/month/year."""
	List = sDate.split('/')
	sMonth = MonthDict[str(int(List[1]))]
	sNewDate = List[0] + ' ' + sMonth + ' ' + List[2]
	return sNewDate

def getId(sTxt):
	if sTxt:
		sId = sTxt.lower()
		sId = re.sub('[ ]', '_', sId)
		sId = re.sub('[.]', '_', sId)
		sId = re.sub('[/]', '__', sId)
		sId = re.sub(u'[á]', 'a', sId)
		sId = re.sub(u'[é]', 'e', sId)
		sId = re.sub(u'[í]', 'i', sId)
		sId = re.sub(u'[ó]', 'o', sId)
		sId = re.sub(u'[ú]', 'u', sId)
		sId = re.sub(u'[ñ]', 'n', sId)
		sId = re.sub(u'[ç]', 'c', sId)
		sId = re.sub('[^a-zA-Z0-9_-]', '___', sId)
	else:
		sId = ''
	return sId

def buildGroup(EnXMLContainer):
	"""Build the Group javascript data in hidden values Groups_enc, Groups, Queries_enc, Queries."""
	GroupDict = {}
	CollectionList = EnXMLContainer.getCollectionList()
	GroupEncList = []
	GroupList = []
	QueryEncList = []
	QueryList = [] 
	for Collection in CollectionList:
		sGroup = Collection.getAttr('group_txt')
		sGroupId = 'G_' + getId(sGroup)
		GroupEncList.append(sGroupId)
		GroupList.append(sGroup)
		EntryList = Collection.getEntryList()
		QueryFieldList = []
		QueryEncFieldList = []
		for Entry in EntryList:
			sTopic = Entry.getValue()
			sTopicId = 'I_' + getId(sTopic)
			QueryFieldList.append(sTopic)
			QueryEncFieldList.append(sTopicId)
		if len(EntryList) != 0:
			QueryList.append(sGroupId + '--:' + string.join(QueryFieldList, ':;:'))
			QueryEncList.append(sGroupId + '--:' + string.join(QueryEncFieldList, ','))
	GroupDict['Groups'] = string.join(GroupList, ':;:')
	GroupDict['Groups_enc'] = string.join(GroupEncList, ',')
	GroupDict['Queries'] = string.join(QueryList, ',.,')
	GroupDict['Queries_enc'] = string.join(QueryEncList, ',.,')
	return GroupDict

def getNumberQueriesInGroup(GroupDict):
	iNumberQueries = 0
	QueryEncList = []
	if GroupDict.has_key('Queries_enc'):
		if GroupDict['Queries_enc'] != '':
			QueryEncList = GroupDict['Queries_enc'].split(',.,')
		for sTarget in QueryEncList:
			Fields = sTarget.split('--:')
			List = Fields[1].split(',')
			iNumberQueries += len(List)
	else:
		iNumberQueries = 0
	return iNumberQueries

def buildGroupContainer(GroupDict, sContainerName, sContainerId, sCollectionName, sEntryName):
	"""Build XMLContainer from GroupDict. -> EnXMLContainer."""
	GroupList = GroupDict['Groups'].split(':;:')
	GroupEncList = GroupDict['Groups_enc'].split(',')
	QueryList = GroupDict['Queries'].split(',.,')
	QueryEncList = GroupDict['Queries_enc'].split(',.,')
	#Dict -> [sGroup] = []
	Dict = {}
	IdDict = {}
	i = 0
	for sGroup in GroupList:
		if sGroup != '':
			Dict[sGroup] = []
			sGroupId = GroupEncList[i]
			IdDict[sGroupId] = sGroup
		i += 1
	for sField in QueryList:
		if sField != '':
			Fields = sField.split('--:')
			sGroupId, QueryFields = Fields
			sGroup = IdDict[sGroupId]
			List = QueryFields.split(':;:')
			for sQuery in List:
				Dict[sGroup].append(sQuery)
	EnXMLContainer = xml_lib.EnXMLContainer(sContainerName, sContainerId, {})
	for sGroup in GroupList:
		if sGroup != '':
			AttrDict = {'group_txt': sGroup}
			sCollectionId = getId(sGroup)
			EnXMLCollection = xml_lib.EnXMLCollection(sCollectionName, sCollectionId, AttrDict)
			QueryList = Dict[sGroup]
			for sQuery in QueryList:
				EnXMLEntry = xml_lib.EnXMLEntry(sEntryName, sQuery)
				EnXMLCollection.addEntry(EnXMLEntry)
			EnXMLContainer.addCollection(EnXMLCollection)
	return EnXMLContainer

def buildAddList(EnXMLCollection):
	"""Build the AddList javascript data in hidden values ListFields_enc, ListFields."""
	AddDict = {}
	EntryList = EnXMLCollection.getEntryList()
	FieldEncList = []
	FieldList = []
	TupleList = []
	for Entry in EntryList:
		sValue = Entry.getValue()
		iValue = getId(sValue)
		TupleList.append((iValue, sValue))
		FieldEncList.append(iValue)
		FieldList.append(sValue)
	TupleList.sort()
	AddDict['ListFields_enc'] = string.join(FieldEncList, ',')
	AddDict['ListFields'] = string.join(FieldList, ':;:')
	Tuple = (AddDict, TupleList)
	return Tuple

def buildAddListPage(sName, TupleList):
	"""Doc."""
	Dict = {sName: '', sName + '_enc': '', sName + '_map': ''}
	FieldDict = {}
	MapList = []
	MapRevDict = {}
	for Tuple in TupleList:
		sFieldId, sField = Tuple
		sFieldIdGen = getId(sField)
		FieldDict[sFieldIdGen] = sField
		MapList.append(sFieldIdGen + ':' + sFieldId)
	Dict[sName] = string.join(FieldDict.values(), ':;:')
	Dict[sName + '_enc'] = string.join(FieldDict.keys(), ',')
	Dict[sName + '_map'] = string.join(MapList, ',') 
	return Dict

def buildAddListCollection(AddDict, sCollectionName, sCollectionId, sEntryName):
	"""Build XMLCollection from AddDict. -> EnXMLCollection."""
	FieldEncList = AddDict['ListFields_enc'].split(',')
	FieldList = AddDict['ListFields'].split(':;:')
	#print 'Data->', FieldEncList, FieldList
	EnXMLCollection = xml_lib.EnXMLCollection(sCollectionName, sCollectionId, {})
	for sField in FieldList:
		#print 'sField->', sField
		if sField != '':
			EnXMLEntry = xml_lib.EnXMLEntry(sEntryName, sField)
			EnXMLCollection.addEntry(EnXMLEntry)
	return EnXMLCollection

def stripVarUrl(sUrl):
	sUrl = sUrl[:sUrl.rfind('/')]
	return sUrl

def values_single_list(QuerySetList, sName):
	"""Gets List[Value1, Value2, etc...] from a QuerySetList for sName attribute, like Entity.objects.filter(). -> IdList. 
	Example: AccountList = values_single_list(SearchAccountList, 'Account') where SearchAccountList was obtained from a filter procedure."""
	ValueList = []
	DictList = QuerySetList.values()
	for Dict in DictList:
		value = Dict[sName]
		ValueList.append(value)
	return ValueList

def insertDefaultSystemSection(xmlConfig, sAccount, sServiceType, sEmail, sAutoPublish):
	oPageXML = xml_lib.PageXML()
	oPageXML.parse(xmlConfig)
	oPageXML.addContainer('PageXML/SystemSection[id="System"]', 'SystemPropertiesContainer', 'DICT_SYS_PROPS')
	xPath = 'PageXML/SystemSection[id="System"]/SystemPropertiesContainer[@id="DICT_SYS_PROPS"]'
	oPageXML.addKeySimple(xPath, 'Account', sAccount)
	oPageXML.addKeySimple(xPath, 'AccountNode', str(config.ACCOUNT_NODE_DICT[sServiceType]))
	oPageXML.addKeySimple(xPath, 'AccountType', 'USER')
	oPageXML.addKeySimple(xPath, 'AccountGroup', 'Main')
	oPageXML.addKeySimple(xPath, 'AccountSize', config.ACCOUNT_SIZE_DICT[sServiceType])
	oPageXML.addKeySimple(xPath, 'Service', config.ACCOUNT_SERVICE_DICT[sServiceType])
	oPageXML.addKeySimple(xPath, 'StatusCode', '1')
	oPageXML.addKeySimple(xPath, 'BuildCache', 'Y')
	oPageXML.addKeySimple(xPath, 'AccountLink', '')
	oPageXML.addCollection(xPath, 'IpCollection', 'LIST_SYS_IPS')
	oPageXML.addCollection(xPath, 'AccountCollection', 'LIST_META_SEARCH')
	oPageXML.addCollection(xPath, 'SiteCollection', 'LIST_SS_URLS')
	oPageXML.addKeySimple(xPath, 'EmailAddress', sEmail)
	oPageXML.addKeySimple(xPath, 'EmailSend', 'Y')
	oPageXML.addKeySimple(xPath, 'UseLatestConfigForProduction', sAutoPublish)
	oPageXML.addKeySimple(xPath, 'Language', 'es')
	xmlConfigNew = oPageXML.toXml(True)
	oXmlTools = xml_lib.XmlTools()
	xmlConfigNew = oXmlTools.timeStamp(xmlConfigNew)
	return xmlConfigNew

def getMonthList(MonthDict):
	MonthIdList = range(1,13)
	MonthList = []
	for iMonth in MonthIdList:
		sMonth = MonthDict[str(iMonth)]
		MonthList.append(sMonth)
	return MonthList

def getXmlTimestampLocalized(sTimestamp, MonthDict):
	Fields1 = sTimestamp.split('T')
	Fields2 = Fields1[1].split('-')
	DateFields = Fields1[0].split('-')
	TimeFields = Fields2[0].split(':')
	sDate = DateFields[2] + '/' + DateFields[1] + '/' + DateFields[0]
	sTimestamp = getLocalizedDate(sDate, MonthDict) + ' ' + TimeFields[0] + ':' + TimeFields[1]
	return sTimestamp

def getXmlTimestamp(sTimestamp):
	Fields1 = sTimestamp.split('T')
	Fields2 = Fields1[1].split('-')
	DateFields = Fields1[0].split('-')
	TimeFields = Fields2[0].split(':')
	sDate = DateFields[2] + '/' + DateFields[1] + '/' + DateFields[0]
	sTimestamp = sDate + ' ' + TimeFields[0] + ':' + TimeFields[1] + ':' + TimeFields[2]
	return sTimestamp

def getMonthInt(sMonth, MonthDict):
	MonthList = MonthDict.keys()
	MonthRevDict = {}
	for sMonthTarget in MonthList:
		MonthRevDict[MonthDict[sMonthTarget]] = int(sMonthTarget)
	iMonth = MonthRevDict[sMonth]
	return iMonth

def getContentRelaseDict(sTheme):
	Dict = config.CONTENT_REL_DICT
	ContentReleaseDict = {}
	for sKey in Dict.keys():
		if type(Dict[sKey]) != types.DictType:
			iRelease = Dict[sKey]
			if iRelease != -1:
				ContentReleaseDict[sKey] = '-' + str(iRelease).zfill(4)
			else:
				ContentReleaseDict[sKey] = ''
		else:
			for sName in Dict[sKey].keys():
				sOp = 'th_'
				iRelease = Dict[sKey][sName]
				if iRelease != -1:
					ContentReleaseDict[sOp + sName] = '-' + str(iRelease).zfill(4)
				else:
					ContentReleaseDict[sOp + sName] = ''
	iTheme = Dict['themes'][sTheme]
	ContentReleaseDict['lnk_th'] = ''
	if iTheme != -1:
		ContentReleaseDict['lnk_th'] = '-' + str(iTheme).zfill(4)
	return ContentReleaseDict

def isBackendServiceOK(sService):
	sService = sService.upper()
	bService = False
	PropertyList = app_Main.models.Properties.objects.all()
	Dict = {}
	for oProperty in PropertyList:
		Dict[oProperty.PropertyName] = oProperty.PropertyValue
	KeyList = Dict.keys()
	KeyList.sort()
	for sKey in KeyList:
		Fields = sKey.split('_')
		if Fields[0] == 'BACKEND':
			if Fields[2] == sService and sKey.find('_DOWN') != -1:
				sValue = Dict[sKey]
				sKeyConn = Fields[0] + '_' + Fields[1] + '_' + Fields[2] + '_' + Fields[3]
				if sValue != '1' and Dict[sKeyConn] == '1':
					bService = True
			elif Fields[2] == sService and sKey.find('_DOWN') == -1:
				sValue = Dict[sKey]
				if sValue == '1':
					bService = True
	return bService

def getSimpleContext(request, sLang, sKey, LinksDict):
	sTheme, sSearchTheme, sSession = http.doSession(request)
	# Xml Contexts
	XmlContentList = getXmlList('xml_content', 'main.db', ['Index/' + sLang, 'Messages/' + sLang, sKey])
	BaseXml = xml_lib.PageXML()
	BaseXml.parse(XmlContentList[0])
	BaseContextDict = BaseXml.getContainerDict('DICT_BASE_CONTEXT')
	MessagesXml = xml_lib.PageXML()
	MessagesXml.parse(XmlContentList[1])
	MessagesDict = MessagesXml.getContainerDict('DICT_MESSAGES')
	ContentXml = xml_lib.PageXML()
	ContentXml.parse(XmlContentList[2])
	TextDict = ContentXml.getContainerDict('DICT_TEXT')
	ParameterDict = {}
	ParameterDict['lnk_d'] = LinksDict
	ParameterDict['lnk_local_d'] = LinksDict[sLang]
	ParameterDict['theme'] = sTheme
	ParameterDict['lang'] = sLang
	ParameterDict['request'] = request
	ParameterDict['text_d'] = TextDict
	ParameterDict['base_d'] = BaseContextDict
	ParameterDict['messages_base_d'] = MessagesDict
	ParameterDict['rel_d'] = getContentRelaseDict(sTheme, sSearchTheme)
	ParameterDict['tmpl_base_path'] = 'base/base_general_jquery.html'
	return ParameterDict

def reverseDict(Dict):
	List = Dict.items()
	DictNew = {}
	for Tuple in List:
		DictNew[Tuple[1]] = Tuple[0]
	return DictNew

def getCategoryContainer(sLang):
	"""Get language category container Id->Category, like 001->Arts
	@param sLang: Language
	@return: CatLangContainer (XML Container)"""
	xmlCategories = getXml('xml_web', 'tables.db', 'Categories/' + sLang)
	oPageXMLCats = xml_lib.PageXML()
	oPageXMLCats.parse(xmlCategories)
	CatLangContainer = oPageXMLCats.getContainer('PageXML/Container[@id="DICT_CATEGORIES"]')
	return CatLangContainer

def getRevCategoryMap(sLang):
	"""Get reverse language category container Language Category->Id, like Arts->001
	@param sLang: Language
	@return: CatReverseLangMap (Dict)"""
	XMLContainer = getCategoryContainer(sLang)
	Map = XMLContainer.getKeyDict()
	List = Map.keys()
	RevDict = {}
	for sKey in List:
		EnXMLKey = Map[sKey]
		RevDict[EnXMLKey.getValue()] = sKey
	return RevDict

def getDowngradeDict():
	"""Get DowngradeDict, Unicode Char -> Char
	@return: DowngradeDict"""
	DowngradeDict = {}
	oDbmd = config.Dbmd()
	dbm = oDbmd.connectByHost(config.DBM_HOSTNAME, 'web')
	dbm.open('downgrade.db', db.DB_BTREE, db.DB_CREATE)
	List = dbm.items()
	dbm.close()
	for Tuple in List:
		sKey, sValue = Tuple
		charUni = unicode(sKey, "utf-8")
		DowngradeDict[charUni] = sValue
	return DowngradeDict

def downgradeQuery(sQuery):
	"""Downgrade query to get rid of accents and other chars
	@param sQuery: The Query string to parse
	@return: sQueryNew : Query parsed"""
	WordList = re.split('[-_ .]+', sQuery.lower())
	QueryNewList = []
	DowngradeDict = getDowngradeDict()
	DowngradePlusDict = {u'ñ': 'n', u'Ñ': 'n', u'ç': 'c', u'Ç': 'c'}
	for sWord in WordList:
		#print 'sWord->', sWord, type(sWord) 
		sWordNew = ''
		# Downgrade word
		for sCharUni in sWord:
			if DowngradeDict.has_key(sCharUni):
				#print 'Downgrade...'
				sChar = DowngradeDict[sCharUni]
			elif DowngradePlusDict.has_key(sCharUni):
				#print 'Downgrade Plus...'
				sChar = DowngradePlusDict[sCharUni]
			else:
				sChar = sCharUni.encode('utf-8')
			sWordNew += sChar
		if sWordNew != '':
			QueryNewList.append(sWordNew)
	sQueryNew = string.join(QueryNewList, ' ')
	return sQueryNew

def addToSearchAccIndex(QueryList, iAccountId, sType):
	"""Adds list of words in QueryList to account index. Used by search account signup for tags and vertical search boxes like account home page and web site searches.
	@param request: Request object
	@param QueryList: List of keywords separated by spaces
	@param iAccountId: Search account id
	@param sType: Type of entry: tag, topic, keyword
	@return: None"""
	# sWord -> Data (iAccountId, iOrder, sType)
	# iAccountId -> sWord
	oDbmd = config.Dbmd()
	DataList = []
	DataAltList = []	
	DowngradeDict = getDowngradeDict()
	DowngradePlusDict = {u'ñ': 'n', u'Ñ': 'n', u'ç': 'c', u'Ç': 'c'}
	"""print 'DowngradeDict->', DowngradeDict
	print 'DowngradePlusDict->', DowngradePlusDict"""
	for sQuery in QueryList:
		WordList = re.split('[-_ .]+', sQuery.lower())
		iOrder = 0
		for sWord in WordList:
			#print 'sWord->', sWord, type(sWord) 
			sWordNew = ''
			# Downgrade word
			for sCharUni in sWord:
				if DowngradeDict.has_key(sCharUni):
					#print 'Downgrade...'
					sChar = DowngradeDict[sCharUni]
				elif DowngradePlusDict.has_key(sCharUni):
					#print 'Downgrade Plus...'
					sChar = DowngradePlusDict[sCharUni]
				else:
					sChar = sCharUni.encode('utf-8')
				sWordNew += sChar
			#print 'sWordNew->', sWordNew
			DataList.append((sWordNew, str(iAccountId) + ',' + str(iOrder) + ',' + sType))
			# Type????? in Alt?????
			DataAltList.append((str(iAccountId), sWordNew))
			iOrder += 1
	#print 'DataList->', DataList
	#print 'DataAltList->', DataAltList
	DbmIdx = oDbmd.connectByHost(config.DBM_HOSTNAME, 'web')
	DbmIdx.set_flags(db.DB_DUP)
	DbmIdx.putListDirect('account_index.db', DataList, db.DB_BTREE, db.DB_CREATE)
	DbmIdxRev = oDbmd.connectByHost(config.DBM_HOSTNAME, 'web')
	DbmIdxRev.set_flags(db.DB_DUP)
	DbmIdxRev.putListDirect('account_index_rev.db', DataAltList, db.DB_BTREE, db.DB_CREATE)

def deleteFromSearchAccIndex(iAccountId, sType=None):
	"""Delete all data from account.
	@param request: Request:
	@param sType: Type of entry: tags, topic, keyword, etc... [Optional]  
	@param iAccountId: Account id"""
	# Get list of words
	oDbmd = config.Dbmd()
	DbmIdxRev = oDbmd.connectByHost(config.DBM_HOSTNAME, 'web')
	# sAccountId -> sWord
	DbmIdxRev.set_flags(db.DB_DUP)
	DbmIdxRev.open('account_index_rev.db', db.DB_BTREE, db.DB_CREATE, sMode='w')
	CursorRev = DbmIdxRev.cursor()
	TupleList = CursorRev.getDupList(str(iAccountId))
	WordList = []
	for Tuple in TupleList:
		WordList.append(Tuple[1])
	if DbmIdxRev.has_key(str(iAccountId)):
		DbmIdxRev.delete(str(iAccountId))
	CursorRev.close()
	DbmIdxRev.close()
	DbmIdx = oDbmd.connectByHost(config.DBM_HOSTNAME, 'web')
	DbmIdx.set_flags(db.DB_DUP)
	DbmIdx.open('account_index.db', db.DB_BTREE, db.DB_CREATE, sMode='w')
	# sWord -> sData
	Cursor = DbmIdx.cursor()
	for sWord in WordList:
		Tuple = Cursor.set(sWord)
		while Tuple:
			sWord, sData = Tuple
			Fields = sData.split(',')
			sAccountIdTg, sOrderTg, sTypeTg = Fields
			if sType:
				if sType == sTypeTg and sAccountIdTg == str(iAccountId):
					Cursor.delete()
			else:
				if sAccountIdTg == str(iAccountId):
					Cursor.delete()
			Tuple = Cursor.next_dup()
	Cursor.close()
	DbmIdx.close()

