import string
import types
import os
import time
import random
import re
import urllib
import xml.parsers.expat

"""Copyright (c) 2010 Tecor Communications S.L.
All rights reserved."""

class ClassNodeDict(dict):
	__KeyList = []
	__dict__ = {}
	def __init__(self):
		self.__KeyList = []
		self.__ValueList = []
		self.__dict__ = {}
	def __setitem__(self, key, value):
		if not self.__dict__.has_key(key):
			self.__KeyList.append(key)
			self.__ValueList.append(value)
			self.__dict__[key] = value
		else:
			self.__dict__[key] = value
	def __repr__(self):
		return str(self.__dict__)
	def __getitem__(self, key):
		value = self.__dict__[key]
		return value
	def __delitem__(self, key):
		del self.__dict__[key]
		KeyListTmp = []
		for keyTarget in self.__KeyList:
			if key != keyTarget:
				KeyListTmp.append(keyTarget)
		self.__KeyList = KeyListTmp
	def has_key(self, key):
		if self.__dict__.has_key(key):
			check = True
		else:
			check = False
		return check
	def keys(self):
		return self.__KeyList
	def values(self):
		ValueList = []
		KeyList = self.__KeyList
		i = 0
		while i != len(KeyList):
			ValueList.append(self.__dict__[KeyList[i]])
			i = i + 1
		return ValueList


class SchemaException:
	Code = 0
	Name = ''
	def __init__(self, code, name=''):
		self.Code = code
		if name != '':
			self.Name = str(name)
	def __str__(self):
		if self.Code == 100:
			errMsg = 'Error validating schema'
		else:
			errMsg = 'Schema Error'
		return str(errMsg)

class PageXMLException:
	Code = 0
	Name = ''
	ErrDict = {}
	def __init__(self, code, name=''):
		self.Code = code
		if name != '':
			self.Name = str(name)
	def __str__(self):
		if self.Code == 100:
			errMsg = 'Id ' + self.Name + 'is not a container.'
		elif self.Code == 200:
			#errMsg = 'Container ' + self.Name + ' does not exist.'
			errMsg = 'Error in getting container'
		elif self.Code == 201:
			errMsg = self.Name + ' is not a container.'
		elif self.Code == 202:
			errMsg = self.Name + ' already exists.'
		elif self.Code == 203:
			errMsg = 'Error in format fot xPath.'
		elif self.Code == 204:
			errMsg = 'Key must be added only to a container. XPath: ' + self.Name
		elif self.Code == 205:
			errMsg = 'Entry must be added only to a collection. XPath: ' + self.Name
		elif self.Code == 206:
			errMsg = 'I cannot add node to a Key or Entry'
		elif self.Code == 207:
			errMsg = 'Node with xPath ' + self.Name + ' is not a container'
		elif self.Code == 208:
			errMsg = 'Node with xPath ' + self.Name + ' is not a collection'
		elif self.Code == 209:
			errMsg = 'Node with xPath ' + self.Name + ' is not a collection complex'
		elif self.Code == 210:
			errMsg = 'Node with xPath ' + self.Name + ' is not a key'
		elif self.Code == 211:
			errMsg = 'Node with xPath ' + self.Name + ' is not a section'
		elif self.Code == 212:
			errMsg = 'Error in ' + self.Name
		elif self.Code == 213:
			errMsg = 'Error in ' + self.Name
		elif self.Code == 214:
			errMsg = 'Error'
		elif self.Code == 215:
                        errMsg = 'You cant add container more than 6 levels.'
		elif self.Code == 300:
			errMsg = "Collection "  + self.Name + " does not exist."
		elif self.Code == 400:
			errMsg = "EntryDict must be a container of String objects."""
		else:
			errMsg = 'Error Parsing XML'
		return str(errMsg)

class EnXMLKey:
	__AttrDict = {}
	__Name = ''
	__Value = ''
	__NodeName = ''
	__Type = 'Key'
	def __init__(self, keyNodeName, keyName, keyValue, AttrDict={}):
		self.__Name = keyName
		self.__Value = keyValue
		self.__NodeName = keyNodeName
		if len(AttrDict) != 0:
			self.__AttrDict = AttrDict
		self.oXmlTools = XmlTools()
	def getAttrDict(self):
		""""Get AttrDict."""
		return self.__AttrDict
	def getName(self):
		"""Get Name."""
		return self.__Name
	def getType(self):
		"""Get type of element."""
		return self.__Type
	def getNodeName(self):
		"""Get Node Name (XML)."""
		return self.__NodeName
	def getValue(self):
		"""Get Value."""
		value = self.__Value
		return value
	def setAttrDict(self, AttrDict):
		"""Set AttrDict."""
		self.__AttrDict = AttrDict
	def setValue(self, keyValue):
		"""Set Value."""
		self.__Value = keyValue
	def setType(self, nodeType):
		"""Set node type."""
		self.__Type = nodeType
	def addAttr(self, attrName, attrValue):
		"""Add attribute to AttrDict."""
		check = self.hasAttr(attrName)
		if not check:
			self.AttrDict[attrName] = attrValue
	def delAttr(self, attrName):
		"""Delete attribute to AttrDict."""
		check = self.hasAttr(attrName)
		if check:
			del self.__AttrDict[attrName]
	def updateAttr(self, attrName, attrValue):
		"""Updates attribute value to AttrDict."""
		check = self.hasAttr(attrName)
		if check:
			self.__AttrDict[attrName] = attrValue
	def getAttr(self, attrName):
		"""Get attribute from AttrDict."""
		check = self.hasAttr(attrName)
		if check:
			attrValue = self.getAttr(attrName)
		else:
			attrValue = ''
		return attrValue
	def hasAttr(self, attrName):
		"""Checks that has attribute (AttrDict). Returns True or False."""
		if self.__AttrDict.has_key(attrName):
			check = True
		else:
			check = False
		return check
	def toXml(self, tabFlag=0, nodeLevel=1, encoding="utf-8"):
		"""Convert to Xml string."""
		if tabFlag:
			tab = '\t'*nodeLevel
		else:
			tab = ''
		nodeName = self.getNodeName()
		keyName = self.getName()
		keyValue = self.getValue()
		AttrDict = self.getAttrDict()
		nodeType = self.getType()
		attrStr = self.oXmlTools.buildAttrStr(AttrDict, 'Key')
		if nodeType == 'KeySimple':
			xmlStr = tab + '<' + nodeName + attrStr + '>' + self.oXmlTools.scapeAmp(keyValue) + '</' + nodeName + '>' + '\015\012'
		else:
			xmlStr = tab + '<' + nodeName + ' name="' + keyName + '"' + attrStr + '>' + self.oXmlTools.scapeAmp(keyValue) + '</' + nodeName + '>' + '\015\012'
		if string.find(xmlStr, '\x00') != -1:
			xmlStr = string.replace(xmlStr, '\x00','')
		if type(xmlStr) == types.UnicodeType:
			xmlStr = xmlStr.encode(encoding)
		return xmlStr

class EnXMLCollection:
	__Id = ''
	__NodeName = ''
	__Count = '0'
	__Type = 'Collection'
	__AttrDict = {}
	def __init__(self, nodeName, id, AttrDict):
		self.__Id = id
		self.__NodeName = nodeName
		self.__Dict = ClassNodeDict()
		self.__AttrDict = AttrDict
		self.oXmlTools = XmlTools()
	def __getElementDict(self, ElementTypeList):
                TypeDict = {}
                i = 0
                while i != len(ElementTypeList):
                        TypeDict[ElementTypeList[i]]=''
                        i = i + 1
		List = self.__Dict.keys()
		i = 0
		ElementDict = ClassNodeDict()
		while i != len(List):
			EnXML = self.__Dict[List[i]]
			type = EnXML.getType()
			if TypeDict.has_key(type):
				ElementDict[List[i]] = EnXML
			i = i + 1
		return ElementDict
	def getEntryList(self):
		"""Get list of entries."""
		EntryDict = self.__getElementDict(['Entry'])
		EntryList = EntryDict.values()
		return EntryList
	def getCounter(self):
		"""Get size of entries and containers."""
		return self.__Count
	def getId(self):
		"""Get Id."""
		return self.__Id
	def getNodeName(self):
		"""Get Node Name (XML)."""
		return self.__NodeName
	def getType(self):
		"""Get type of element."""
		return self.__Type
	def addEntry(self, EnXMLEntry):
		"""Add entry."""
		count = self.__Count
		self.__Dict[count] = EnXMLEntry
		count = int(count) + 1
		self.__Count = str(count)
	def searchEntry(self, attrName, attrValue):
		"""Search entries inside a collection. Returns EnXMLEntry."""
		EntryList = self.getEntryList()
		i = 0
		EnXMLEntry = None
		while i != len(EntryList):
			EnXMLEntry = EntryList[i]
			AttrDict = EnXMLEntry.getAttrDict()
			if AttrDict.has_key(attrName):
				if AttrDict[attrName] == attrValue:
					break
			i = i + 1
		return EnXMLEntry
	def getAttrDict(self):
		"""Doc."""
		return self.__AttrDict
	def getAttr(self, sName):
		sValue = self.__AttrDict[sName]
		return sValue
	def setAttrDict(self, AttrDict):
		"""Doc."""
		self.__AttrDict = AttrDict
	def toXml(self, tabFlag=0, nodeLevel=1, encoding="utf-8"):
		"""Convert to Xml string."""
		if tabFlag:
			tab = '\t'*nodeLevel
		else:
			tab = ''
		nodeName = self.getNodeName()
		collectionId = self.getId()
		counter = self.getCounter()
		AttrDict = self.getAttrDict()
		attrStr = self.oXmlTools.buildAttrStr(AttrDict, 'Collection')
		xmlStr = ''
		sNodeName = nodeName.encode(encoding)
		if collectionId != '':
			xmlStr = xmlStr + tab + '<' + sNodeName + ' id="' + str(collectionId) + '" count="' + str(counter) + '"' + attrStr + '>' + '\015\012'
		else:
			xmlStr = xmlStr + tab + '<' + sNodeName + ' count="' + str(counter) + '"' + attrStr + '>' + '\015\012'
		List = self.__Dict.keys()
		i = 0
		while i != len(List):
			key = List[i]
			oEnXML = self.__Dict[key]
			nodeType = oEnXML.getType()
			"""try:
				xmlPieceStr = oEnXML.toXml(tabFlag, nodeLevel+1, encoding)
				#xmlStr = xmlStr + unicode(xml, encoding)
				xmlStr = xmlStr + xmlPieceStr
			except UnicodeDecodeError:
				pass"""
			xml = oEnXML.toXml(tabFlag, nodeLevel+1, encoding)
			xmlStr = xmlStr + xml
			"""try:
				print 'a', encoding, type(xmlStr)
				xmlStr = xmlStr + unicode(xml, encoding)
				print 'b'
			except UnicodeDecodeError:
				xmlStr = xmlStr + unicode(xml, 'latin1')"""
			i = i + 1
		xmlStr = xmlStr + tab + '</' + sNodeName + '>' + '\015\012'
		if string.find(xmlStr, '\x00') != -1:
			xmlStr = string.replace(xmlStr, '\x00','')
		if type(xmlStr) == types.UnicodeType:
			xmlStr = xmlStr.encode(encoding)
		return xmlStr

class EnXMLCollectionComplex:
	__NodeName = ''
	__AttrDict = {}
	__Count = 0
	__Id = ''
	__Type = 'CollectionComplex'
	def __init__(self, nodeName, id, AttrDict):
		self.__NodeName = nodeName
		self.__Id = id
		self.__Dict = ClassNodeDict()
		self.__AttrDict = AttrDict
		self.__Count = 0
		self.oXmlTools = XmlTools()
	def __getElementDict(self, ElementTypeList):
                TypeDict = {}
                i = 0
                while i != len(ElementTypeList):
                        TypeDict[ElementTypeList[i]]=''
                        i = i + 1
		List = self.__Dict.keys()
		i = 0
		ElementDict = ClassNodeDict()
		while i != len(List):
			EnXML = self.__Dict[List[i]]
			type = EnXML.getType()
			if TypeDict.has_key(type):
				ElementDict[List[i]] = EnXML
			i = i + 1
		return ElementDict
	def getType(self):
		"""Get type."""
		return self.__Type
	def getId(self):
		"""Get id."""
		return self.__Id
	def getNodeName(self):
		"""Get Node Name (XML)."""
		return self.__NodeName
	def getContainerList(self):
		"""Get list of containers."""
		ContainerList = self.__Dict.values()
		return ContainerList
	def getContainer(self, containerId):
		"""Get container "containerId"."""
		EnXMLContainer = self.__Dict[containerId]
		return EnXMLContainer
	def getCounter(self):
		"""Get size of entries and containers."""
		return self.__Count
	def addContainer(self, EnXMLContainer):
		"""Add container."""
		count = self.__Count
		containerId = EnXMLContainer.getId()
		self.__Dict[containerId] = EnXMLContainer
		count = int(count) + 1
		self.__Count = str(count)
	def getAttrDict(self):
		"""Get AttrDict."""
		return self.__AttrDict
	def setAttrDict(self, AttrDict):
		"""Set AttrDict."""
		self.__AttrDict = AttrDict
	def searchContainer(self, containerName, keyName):
		"""Search containers inside a collection. Returns EnXMLKey."""
		ContainerList = self.getContainerList()
		i = 0
		EnXMLKey = None
		while i != len(ContainerList):
			EnXMLContainer = ContainerList[i]
			containerNameTarget = EnXMLContainer.getName()
			if containerName == containerNameTarget:
				Dict = EnXMLContainer.getKeyDict()
				List = Dict.keys()
				j = 0
				while j != len(List):
					keyNameTarget = List[j]
					if keyNameTarget == keyName:
						EnXMLKey = Dict[keyName]
					j = j + 1
			i = i + 1
		return EnXMLKey
	def toXml(self, tabFlag, nodeLevel=1, encoding="utf-8"):
		"""Convert to Xml string."""
		if tabFlag:
			tab = '\t'*nodeLevel
		else:
			tab = ''
		nodeName = self.getNodeName()
		collectionId = self.getId()
		counter = self.getCounter()
		AttrDict = self.getAttrDict()
		attrStr = self.oXmlTools.buildAttrStr(AttrDict, 'CollectionComplex')
		xmlStr = ''
		if collectionId != '':
			xmlStr = xmlStr + tab + '<' + nodeName + ' id="' + str(collectionId) + '" count="' + str(counter) + '"' + attrStr + '>' + '\015\012'
		else:
			xmlStr = xmlStr + tab + '<' + nodeName + ' count="' + str(counter) + '"' + attrStr + '>' + '\015\012'
		List = self.__Dict.keys()
		i = 0
		while i != len(List):
			key = List[i]
			oEnXML = self.__Dict[key]
			nodeType = oEnXML.getType()
			"""try:
				xmlPieceStr = oEnXML.toXml(tabFlag, nodeLevel+1, encoding)
				#xmlStr = xmlStr + unicode(xml, encoding)
				xmlStr = xmlStr + xmlPieceStr
			except UnicodeDecodeError:
				pass"""
			xml = oEnXML.toXml(tabFlag, nodeLevel+1, encoding)
			try:
				xmlStr = xmlStr + unicode(xml, encoding)
			except UnicodeDecodeError:
				xmlStr = xmlStr + unicode(xml, 'latin1')
			i = i + 1
		xmlStr = xmlStr + tab + '</' + nodeName + '>' + '\015\012'
		if string.find(xmlStr, '\x00') != -1:
			xmlStr = string.replace(xmlStr, '\x00','')
		if type(xmlStr) == types.UnicodeType:
			xmlStr = xmlStr.encode(encoding)
		return xmlStr

class EnXMLEntry:
	__AttrDict = {}
	__Value = ''
	__NodeName = ''
	__Type = 'Entry'
	def __init__(self, nodeName, value, AttrDict={}):
		self.__NodeName = nodeName
		self.__Value = value
		if len(AttrDict) != 0:
			self.__AttrDict = AttrDict
		self.oXmlTools = XmlTools()
	def getAttrDict(self):
		"""Get AttrDict."""
		return self.__AttrDict
	def getNodeName(self):
		"""Get Node Name (XML)."""
		return self.__NodeName
	def getType(self):
		"""Get element type."""
		return self.__Type
	def getValue(self):
		"""Get Value."""
		return self.__Value
	def setAttrDict(self, AttrDict):
		"""Set AttrDict."""
		self.__AttrDict = AttrDict
	def setValue(self, keyValue):
		"""Set Value."""
		self.__Value = keyValue
	def addAttr(self, attrName, attrValue):
		"""Adds attribute to AttrDict."""
		check = self.hasAttr(attrName)
		if not check:
			self.AttrDict[attrName] = attrValue
	def delAttr(self, attrName):
		"""Delete attribute from AttrDict."""
		check = self.hasAttr(attrName)
		if check:
			del self.__AttrDict[attrName]
	def updateAttr(self, attrName, attrValue):
		"""Updates AttrDict."""
		check = self.hasAttr(attrName)
		if check:
			self.__AttrDict[attrName] = attrValue
	def getAttr(self, attrName):
		"""Get attribute value from AttrDict."""
		check = self.hasAttr(attrName)
		if check:
			attrValue = self.getAttr(attrName)
		else:
			attrValue = ''
		return attrValue
	def hasAttr(self, attrName):
		"""Checks that AttrDict has attribute. Returns True or False."""
		if self.__AttrDict.has_key(attrName):
			check = True
		else:
			check = False
		return check
	def toXml(self, tabFlag=0, nodeLevel=1, encoding="utf-8"):
		"""Convert to Xml string."""
		if tabFlag:
			tab = '\t'*nodeLevel
		else:
			tab = ''
		nodeName = self.getNodeName()
		entryValue = self.getValue()
		AttrDict = self.getAttrDict()
		attrStr = self.oXmlTools.buildAttrStr(AttrDict, 'Entry')
		if entryValue != '':
			xmlStr = tab + '<' + nodeName + ' ' + attrStr + '>' + self.oXmlTools.scapeAmp(entryValue) + '</' + nodeName + '>' + '\015\012'
		else:
			xmlStr = tab + '<' + nodeName + ' ' + attrStr + '/>' + '\015\012'
		if string.find(xmlStr, '\x00') != -1:
			xmlStr = string.replace(xmlStr, '\x00','')
		if type(xmlStr) == types.UnicodeType:
			xmlStr = xmlStr.encode(encoding)
		return xmlStr

class EnXMLContainer:
	__AttrDict = {}
	__Id = ''
	__NodeName = ''
	__Type = 'Container'
	def __init__(self, nodeName, id, AttrDict):
		self.__NodeName = nodeName
		self.__Id = id
		self.__Dict = ClassNodeDict()
		self.__AttrDict = AttrDict
		self.oXmlTools = XmlTools()
	def __getElementDict(self, ElementTypeList):
                TypeDict = {}
                i = 0
                while i != len(ElementTypeList):
                        TypeDict[ElementTypeList[i]]=''
                        i = i + 1
		List = self.__Dict.keys()
		i = 0
		ElementDict = ClassNodeDict()
		while i != len(List):
			EnXML = self.__Dict[List[i]]
			type = EnXML.getType()
			if TypeDict.has_key(type):
				ElementDict[List[i]] = EnXML
			i = i + 1
		return ElementDict
	def getId(self):
		"""Get Id."""
		return self.__Id
	def getType(self):
		"""Get element type."""
		return self.__Type
	def getNodeName(self):
		"""Get Node Name (XML)."""
		return self.__NodeName
	def addKey(self, oEnXMLKey):
		"""Adds key to KeyDict."""
		keyName = oEnXMLKey.getName()
		check = self.hasKey(keyName)
		if not check:
			self.__Dict[keyName] = oEnXMLKey
	def getKey(self, keyName):
		"""Get key from KeyDict."""
		EnXMLKey = self.__Dict[keyName]
		return EnXMLKey
	def getKeyDict(self):
		"""Get KeyDict."""
		KeyDict = self.__getElementDict(['Key','KeySimple'])
		return KeyDict
	def getKeyList(self):
		"""Get list of EnXMLKey."""
		Dict = self.getKeyDict()
		List = Dict.values()
		return List
	def deletekey(self, keyName):
		"""Deletes key from KeyDict."""
		check = self.hasKey(keyName)
		if check:
			del self.__Dict[keyName]
	def updateKey(self, keyName, EnXMLKey):
		"""Updates key in KeyDict."""
		check = self.hasKey(keyName)
		if check:
			self.__Dict[keyName] = EnXMLKey
	def hasKey(self, keyName):
		"""Checks that KeyDict has keyName. Returns True or False."""
		if self.__Dict.has_key(keyName):
			elementType = self.__Dict[keyName].getType()
			if elementType == 'Key':
				check = True
			else:
				check = False
		else:
			check = False
		return check
	def getAttrDict(self):
		"""Doc."""
		return self.__AttrDict
	def getAttr(self, sName):
		sValue = self.__AttrDict[sName]
		return sValue
	def setAttrDict(self, AttrDict):
		"""Doc."""
		self.__AttrDict = AttrDict
	def addCollection(self, EnXMLCollection):
		"""Adds a collection."""
		collectionId = EnXMLCollection.getId()
		self.__Dict[collectionId] = EnXMLCollection
	def getCollectionList(self):
		"""Get list of EnXMLCollection."""
		CollectionDict = self.__getElementDict(['Collection'])
		List = CollectionDict.values()
		return List
	def getCollectionDict(self):
		"""Get CollectionDict, collectionId => EnXMLCollection."""
		CollectionDict = self.__getElementDict(['Collection'])
		return CollectionDict
	def getCollection(self, collectionId):
		"""Get collection by collectionId. Returns EnXMLCollection"""
		EnXMLCollection = self.__Dict[collectionId]
		return EnXMLCollection
	def hasCollection(self, collectionId):
		"""Checks if has collection by "id". Returns True or False."""
		if self.__Dict.has_key[collectionId]:
			if self.__Dict[collectionId].getType() == 'Collection':
				check = True
			else:
				check = False
		else:
			check = False
		return check
	def setCollectionDict(self, EnCollectionDict):
		"""Set CollectionDict."""
		List = EnCollectionDict.keys()
		i = 0
		while i != len(List):
			self.__Dict[List[i]] = EnCollectionDict[List[i]]
			i = i + 1
	def addContainer(self, EnXMLContainer):
		"""Add container."""
		containerId = EnXMLContainer.getId()
		self.__Dict[containerId] = EnXMLContainer
	def getContainerList(self):
		"""Get list of EnXMLContainer"""
		ContainerDict = self.__getElementDict(['Container'])
		List = ContainerDict.values()
		return List
	def getContainerDict(self):
		"""Get Dict of EnXMLContainer, id=> EnXMLContainer."""
		ContainerDict = self.__getElementDict(['Container'])
		return ContainerDict
	def getContainer(self, containerId):
		"""Get EnXMLContainer by "id"."""
		EnXMLContainer = self.__Dict[containerId]
		return EnXMLContainer
	def hasContainer(self, containerId):
		"""Checks if has container by "id". Returns True or False."""
		if self.__Dict.has_key(containerId):
			if self.__Dict[containerId].getType() == 'Container':
				check = True
			else:
				check = False
		else:
			check = False
		return check
	def addCollectionComplex(self, EnXMLCollectionComplex):
		"""Add CollectionComplex"""
		collectionComplexId = EnXMLCollectionComplex.getId()
		self.__Dict[collectionComplexId] = EnXMLCollectionComplex
	def getCollectionComplexList(self):
		"""Get list of EnXMLCollectionComplex."""
		EnXMLCollectionComplexDict = self.__getElementDict(['CollectionComplex'])
		List = EnXMLCollectionComplexDict.values()
		return List
	def getCollectionComplexDict(self):
		"""Get Dict of EnXMLCollectionComplex, id=> EnXMLCollectionComplex"""
		EnXMLCollectionComplexDict = self.__getElementDict(['CollectionComplex'])
		return EnXMLCollectionComplexDict
	def getCollectionComplex(self, collectionComplexId):
		"""Get EnXMLCollectionComplex by "id"."""
		EnXMLCollectionComplex = self.__Dict[collectionComplexId]
		return EnXMLCollectionComplex
	def hasCollectionComplex(self, collectionComplexId):
		"""Checks that has CollectionComplex by "id". Returns True or False."""
		if self.__Dict.has_key(collectionComplexId):
			if self.__Dict[collectionComplexId].getType() == 'CollectionComplex':
				check = True
			else:
				check = False
		else:
			check = False
		return check
	def toXml(self, tabFlag=0, nodeLevel=1, encoding="utf-8"):
		"""Convert to Xml string."""
		if tabFlag:
			tab = '\t'*nodeLevel
		else:
			tab = ''
		nodeName = self.getNodeName()
		containerId = self.getId()
		AttrDict = self.getAttrDict()
		attrStr = self.oXmlTools.buildAttrStr(AttrDict, 'Container')
		xmlStr = tab + '<' + str(nodeName) + ' id="' + str(containerId) + '"' + attrStr + '>' + '\015\012'
		List = self.__Dict.keys()
		i = 0
		while i != len(List):
			key = List[i]
			oEnXML = self.__Dict[key]
			nodeType = oEnXML.getType()
			"""try:
				xmlPieceStr = oEnXML.toXml(tabFlag, nodeLevel+1, encoding)
				#xmlStr = xmlStr + unicode(xml, encoding)
				xmlStr = xmlStr + xmlPieceStr
			except UnicodeDecodeError:
				pass"""
			xml = oEnXML.toXml(tabFlag, nodeLevel+1, encoding)
			xmlStr = xmlStr + xml
			"""try:
				xmlStr = xmlStr + unicode(xml, encoding)
			except UnicodeDecodeError:
				xmlStr = xmlStr + unicode(xml, 'latin1')"""
			i = i + 1
		xmlStr = xmlStr + tab + '</' + str(nodeName) + '>' + '\015\012'
		if string.find(xmlStr, '\x00') != -1:
			xmlStr = string.replace(xmlStr, '\x00','')
		if type(xmlStr) == types.UnicodeType:
			xmlStr = xmlStr.encode(encoding)
		return xmlStr

class EnXMLSection:
	__Id = ''
	__NodeName = ''
	__Type = 'Section'
	def __init__(self, nodeName, id):
		self.__NodeName = nodeName
		self.__Id = id
		self.__Dict = ClassNodeDict()
		self.oXmlTools = XmlTools()
	def __getElementDict(self, ElementTypeList):
                TypeDict = {}
                i = 0
                while i != len(ElementTypeList):
                        TypeDict[ElementTypeList[i]]=''
                        i = i + 1
		List = self.__Dict.keys()
		i = 0
		ElementDict = ClassNodeDict()
		while i != len(List):
			EnXML = self.__Dict[List[i]]
			type = EnXML.getType()
			if TypeDict.has_key(type):
				ElementDict[List[i]] = EnXML
			i = i + 1
		return ElementDict
	def getId(self):
		"""Get Id."""
		return self.__Id
	def getNodeName(self):
		"""Get Node Name (XML)."""
		return self.__NodeName
	def getType(self):
		"""Get element type."""
		return self.__Type
	def addKey(self, EnXMLKey):
		"""Adds key to KeyDict."""
		keyName = EnXMLKey.getName()
		self.__Dict[keyName] = EnXMLKey
	def addCollection(self, EnXMLCollection):
		"""Adds collection to CollectionList."""
		collectionId = EnXMLCollection.getId()
		self.__Dict[collectionId] = EnXMLCollection
	def addContainer(self, EnXMLContainer):
		"""Adds container to ContainerList."""
		containerId = EnXMLContainer.getId()
		self.__Dict[containerId] = EnXMLContainer
	def getKeyDict(self):
		"""Get container KeyDict."""
		KeyDict = self.__getElementDict(["Key","KeySimple"])
		return KeyDict
	def getKeyList(self):
		"""Get list of EnXMLKey."""
		Dict = self.getKeyDict()
		List = Dict.values()
		return List
	def getCollectionDict(self):
		"""Get container of EnXMLCollection, collectionId => EnXMLCollection."""
		CollectionDict = self.__getElementDict(["Collection"])
		return CollectionDict
	def getCollectionList(self):
		"""Get list of EnXMLCollection."""
		Dict = self.getCollectionDict()
		List = Dict.values()
		return List
	def getContainerDict(self):
		"""Get list of EnXMLContainer."""
		ContainerDict = self.__getElementDict(["Container"])
		return ContainerDict
	def getContainerList(self):
		"""Get list of EnXMLContainer."""
		Dict = self.getContainerDict()
		List = Dict.values()
		return List
	def getContainer(self, containerId):
		"""Get container "containerId" from ContainerDict. Returns
		EnXMLContainer."""
		EnXMLContainer = self.__Dict[containerId]
		return EnXMLContainer
	def getCollection(self, collectionId):
		"""Get collection "collectioId" from CollectionDict. Returns
		EnXMLCollection."""
		EnXMLCollection = self.__Dict[collectionId]
		return EnXMLCollection
	def hasContainer(self, containerId):
		"""Checks that ContainerDict has containerId. Returns True or
		False."""
		if self.__Dict.has_key(containerId):
			if self.__Dict[containerId].getType() == 'Container':
				check = True
			else:
				check = False
		else:
			check = False
		return check
	def hasCollection(self, collectionId):
		"""Checks that CollectionDict has collectionId. Returns True or
		False."""
		if self.__Dict.has_key(collectionId):
			if self.__Dict[collectionId].getType() == 'Collection':
				check = True
			else:
				check = False
		else:
			check = False
		return check
	def getKey(self, keyName):
		"""Get key from KeyDict."""
		EnXMLKey = self.__Dict[keyName]
		return EnXMLKey
	def hasKey(self, keyName):
		"""Checks that KeyDict has keyName. Returns True or False."""
		if self.__Dict.has_key(keyName):
			if self.__Dict[keyName].getType() == 'Key':
				check = True
			else:
				check = False
		else:
			check = False
		return check
	def addCollectionComplex(self, EnXMLCollectionComplex):
		"""Add CollectionComplex."""
		collectionComplexId = EnXMLCollectionComplex.getId()
		self.__Dict[collectionComplexId] = EnXMLCollectionComplex
	def getCollectionComplexDict(self):
		"""Get Dict of CollectionComplex, id=>EnXMLCollectionComplex."""
		CollectionComplexDict = self.__getElementDict(["CollectionComplex"])
		return CollectionComplexDict
	def getCollectionComplexList(self):
		"""Get list of EnXMLCollectionComplex."""
		Dict = self.getCollectionComplexDict()
		EnXMLCollectionComplexList = Dict.values()
		return EnXMLCollectionComplexList
	def getCollectionComplex(self, collectionComplexId):
		"""Get CollectionComplex by id. Returns EnXMLCollectionComplex."""
		EnXMLCollectionComplex = self.__Dict[collectionComplexId]
		return EnXMLCollectionComplex
	def hasCollectionComplex(self, collectionComplexId):
		"""Checks if has CollectionComplex, by "id"."""
		if self.__Dict.has_key(collectionComplexId):
			if self.__Dict[collectionComplexId].getType() == 'CollectionComplex':
				check = True
			else:
				check = False
		else:
			check = False
		return check
	def toXml(self, tabFlag=0, nodeLevel=1, encoding="utf-8"):
		"""Convert to Xml string."""
		if tabFlag:
			tab = '\t'*nodeLevel
		else:
			tab = ''
		nodeName = self.getNodeName()
		sectionId = self.getId()
		
		List = self.__Dict.keys()
		if len(List) == 0:
			xmlStr = tab + '<' + str(nodeName) + ' id="' + str(sectionId) + '"/>' + '\015\012'
		else:
			xmlStr = tab + '<' + str(nodeName) + ' id="' + str(sectionId) + '">' + '\015\012'
			i = 0
			while i != len(List):
				key = List[i]
				oEnXML = self.__Dict[key]
				nodeType = oEnXML.getType()
				xml = oEnXML.toXml(tabFlag, nodeLevel+1, encoding)
				xmlStr = xmlStr + xml
				i = i + 1
			xmlStr = xmlStr + tab + '</' + str(nodeName) + '>' + '\015\012'
			if string.find(xmlStr, '\x00') != -1:
				xmlStr = string.replace(xmlStr, '\x00','')
			if type(xmlStr) == types.UnicodeType:
				xmlStr = xmlStr.encode(encoding)
		return xmlStr
class EnXMLPage:
	__AttrDict = {}
	__Id = ''
	__Type = 'Page'
	def __init__(self, id=''):
		self.setId(id)
		self.__AttrDict = {}
		self.__Dict = ClassNodeDict()
		self.oXmlTools = XmlTools()
	def __getElementDict(self, ElementTypeList):
                TypeDict = {}
                i = 0
                while i != len(ElementTypeList):
                        TypeDict[ElementTypeList[i]]=''
                        i = i + 1
		List = self.__Dict.keys()
		i = 0
		ElementDict = ClassNodeDict()
		while i != len(List):
			EnXML = self.__Dict[List[i]]
			type = EnXML.getType()
			if TypeDict.has_key(type):
				ElementDict[List[i]] = EnXML
			i = i + 1
		return ElementDict
	def getId(self):
		"""Get document root."""
		return self.__Id
	def setId(self, id):
		"""Set document root."""
		self.__Id = id
	def getType(self):
		"""Get element type."""
		return self.__Type
	def getAttrDict(self):
		"""Get AttrDict."""
		return self.__AttrDict
	def setAttrDict(self, AttrDict):
		"""Set AttrDict."""
		self.__AttrDict = AttrDict
	def addSection(self, EnXMLSection):
		"""Adds section to SectionDict."""
		sectionId = EnXMLSection.getId()
		self.__Dict[sectionId] = EnXMLSection
	def addKey(self, EnXMLKey):
		"""Adds key to KeyDict."""
		keyName = EnXMLKey.getName()
		self.__Dict[keyName] = EnXMLKey
	def getSectionList(self):
		"""Get list of EnXMLSection."""
		SectionDict = self.__getElementDict(["Section"])
		List = SectionDict.values()
		return List
	def getSection(self, sectionId):
		"""Get section by sectionId from SectionDict. Returns EnXMLSection."""
		SectionDict = self.__getElementDict(["Section"])
		EnXMLSection = SectionDict[sectionId]
		return EnXMLSection
	def hasSection(self, sectionId):
		"""Checks that SectionDict has sectionId. Returns True or False."""
		if self.__Dict.has_key(sectionId):
			if self.__Dict[sectionId].getType == 'Section':
				check = True
			else:
				check = False
		else:
			check = False
		return check
	def getKey(self, keyName):
		"""Get key from KeyDict."""
		EnXMLKey = self.__Dict[keyName]
		return EnXMLKey
	def hasKey(self, keyName):
		"""Checks that KeyDict has keyName."""
		if self.__Dict.has_key(keyName):
			if self.__Dict[keyName].getType() == 'Key':
				check = True
			else:
				check = False
		else:
			check = False
		return check
	def getKeyDict(self):
		"""Get KeyDict."""
		KeyDict = self.__getElementDict(["Key","KeySimple"])
		return KeyDict
	def getKeyList(self):
		"""Get list of EnXMLKey."""
		Dict = self.getKeyDict()
		List = Dict.values()
		return List
	def setKey(self, oEnXMLKey):
		"""Set Key."""
		keyName = oEnXMLKey.getName()
		self.__Dict[keyName] = oEnXMLKey
	def addCollection(self, EnXMLCollection):
		"""Add collection EnXMLCollection."""
		collectionId = EnXMLCollection.getId()
		self.__Dict[collectionId] = EnXMLCollection
	def getCollectionDict(self):
		"""Get CollectionDict, id=>EnXMLCollection."""
		CollectionDict = self.__getElementDict(["Collection"])
		return CollectionDict
	def getCollectionList(self):
		"""Get list of EnXMLCollection."""
		CollectionDict = self.getCollectionDict()
		List = CollectionDict.values()
		return List
	def getCollection(self, collectionId):
		"""Get collection EnXMLCollection with id."""
		CollectionDict = self.getCollectionDict()
		EnXMLCollection = CollectionDict[collectionId]
		return EnXMLCollection
	def hasCollection(self, collectionId):
		"""Checks if has collection "collectionId"."""
		CollectionDict = self.getCollectionDict()
		if CollectionDict.has_key(collectionId):
			check = True
		else:
			check = False
		return check
	def addContainer(self, EnXMLContainer):
		"""Add container EnXMLContainer."""
		containerId = EnXMLContainer.getId()
		self.__Dict[containerId] = EnXMLContainer
	def getContainerDict(self):
		"""Get ContainerDict."""
		ContainerDict = self.__getElementDict(["Container"])
		return ContainerDict
	def getContainerList(self):
		"""Get list of containers, EnXMLContainer."""
		ContainerDict = self.getContainerDict()
		List = ContainerDict.values()
		return List
	def getContainer(self, containerId):
		"""Get Container EnXMLContainer with "containerId"."""
		ContainerDict = self.getContainerDict()
		EnXMLContainer = ContainerDict[containerId]
		return EnXMLContainer
	def hasContainer(self, containerId):
		"""Checks if has container "containerId"."""
		ContainerDict = self.getContainerDict()
		if ContainerDict.has_key(containerId):
			check = True
		else:
			check = False
		return check
	def addCollectionComplex(self, EnXMLCollectionComplex):
		"""Add CollectionComplex."""
		collectionComplexId = EnXMLCollectionComplex.getId()
		self.__Dict[collectionComplexId] = EnXMLCollectionComplex
	def getCollectionComplexDict(self):
		"""Get Dict of CollectionComplex, id=>EnXMLCollectionComplex."""
		CollectionComplexDict = self.__getElementDict(["CollectionComplex"])
		return CollectionComplexDict
	def getCollectionComplexList(self):
		"""Get list of EnXMLCollectionComplex."""
		Dict = self.getCollectionComplexDict()
		EnXMLCollectionComplexList = Dict.values()
		return EnXMLCollectionComplexList
	def getCollectionComplex(self, collectionComplexId):
		"""Get CollectionComplex by id. Returns EnXMLCollectionComplex."""
		EnXMLCollectionComplex = self.__Dict[collectionComplexId]
		return EnXMLCollectionComplex
	def hasCollectionComplex(self, collectionComplexId):
		"""Checks if has CollectionComplex, by "id"."""
		if self.__Dict.has_key(collectionComplexId):
			if self.__Dict[collectionComplexId].getType() == 'CollectionComplex':
				check = True
			else:
				check = False
		else:
			check = False
		return check
	def toXml(self, tabFlag, encoding="utf-8", dtdPath=None):
		"""Convert to Xml String."""
		if tabFlag:
			tab = '\t'
		else:
			tab = ''
		xmlStr = '<?xml version="1.0" encoding="' + encoding + '"?>' + '\015\012'
		if dtdPath:
			xmlStr = xmlStr + dtdPath + '\015\012'
		AttrDict = self.getAttrDict()
		Id = self.getId()
		if len(AttrDict) == 0:
			xmlStr = xmlStr + """<""" + Id + """>""" + '\015\012'
		else:
			xmlStr = xmlStr + """<""" + Id
			i = 0
			List = AttrDict.keys()
			while i != len(List):
				xmlStr = xmlStr + ' ' + str(List[i]) + '="' + str(self.__AttrDict[List[i]]) + '"'
				i = i + 1
			xmlStr = xmlStr + '>' + '\015\012'
		List = self.__Dict.keys()
		i = 0
		while i != len(List):
			key = List[i]
			oEnXML = self.__Dict[key]
			nodeType = oEnXML.getType()
			"""try:
				xmlPieceStr = oEnXML.toXml(tabFlag, 1, encoding)
				#xmlStr = xmlStr + unicode(xml, encoding)
				xmlStr = xmlStr + xmlPieceStr
			except UnicodeDecodeError:
				pass"""
			xml = oEnXML.toXml(tabFlag, 1, encoding)
			xmlStr = xmlStr + xml
			"""try:
				xmlStr = xmlStr + unicode(xml, encoding)
			except UnicodeDecodeError:
				xmlStr = xmlStr + unicode(xml, 'latin1')"""
			i = i + 1
		xmlStr = xmlStr + """</""" + Id + """>""" + '\015\012'
		if string.find(xmlStr, '\x00') != -1:
			xmlStr = string.replace(xmlStr, '\x00','')
		if type(xmlStr) == types.UnicodeType:
			xmlStr = xmlStr.encode(encoding)
		return xmlStr

class PageXML:
	"""This class wraps the methods neccessary to construct the container
	PageDict and the XML to be used by XSLT.
	
	Attribute "Id" has the name for the page tag. Its value is "PageXML" for default.	
	"""
	Id = ''
	MAX_NODES = 6
	PageDict = {}
	AttrDict = {}
	TAB = 0
	NodeDict = {}
	NodeTypeDict = {}
	ElementType = ''
	ElementTypeDict = {}
	ElementList = []
	PathList = []
	DictList = []
	ObjDict = {}
	IdDict = {}
	__DataStr = ''
	__Encoding = 'utf-8'
	def __init__(self, AttrDict={}):
		self.AttrDict = AttrDict
		self.Id = 'PageXML'
		self.PageDict = {}
		self.PageDict[self.Id] = ClassNodeDict()
		self.HtmlDict = {'&Ecirc;': u'\xca', '&raquo;': u'\xbb', '&eth;': u'\xf0', '&divide;': u'\xf7',
			 '&atilde;': u'\xe3', '&sup1;': u'\xb9', '&THORN;': u'\xde', '&ETH;': u'\xd0',
			 '&frac34;': u'\xbe', '&nbsp;': u'\xa0', '&Auml;': u'\xc4', '&Ouml;': u'\xd6',
			 '&Egrave;': u'\xc8', '&acute;': u'\xb4', '&Icirc;': u'\xce', '&deg;': u'\xb0',
			 '&middot;': u'\xb7', '&ocirc;': u'\xf4', '&Ugrave;': u'\xd9', '&gt;': u'>',
			 '&ordf;': u'\xaa', '&uml;': u'\xa8', '&aring;': u'\xe5', '&frac12;': u'\xbd',
			 '&iexcl;': u'\xa1', '&frac14;': u'\xbc', '&Aacute;': u'\xc1', '&szlig;': u'\xdf',
			 '&igrave;': u'\xec', '&aelig;': u'\xe6', '&yen;': u'\xa5', '&times;': u'\xd7',
			 '&egrave;': u'\xe8', '&Atilde;': u'\xc3', '&Igrave;': u'\xcc', '&ucirc;': u'\xfb',
			 '&brvbar;': u'\xa6', '&micro;': u'\xb5', '&agrave;': u'\xe0', '&thorn;': u'\xfe',
			 '&Ucirc;': u'\xdb', '&amp;': u'&', '&uuml;': u'\xfc', '&ecirc;': u'\xea',
			 '&laquo;': u'\xab', '&not;': u'\xac', '&Ograve;': u'\xd2', '&oslash;': u'\xf8',
			 '&Uuml;': u'\xdc', '&cedil;': u'\xb8', '&plusmn;': u'\xb1', '&AElig;': u'\xc6',
			 '&shy;': u'\xad', '&auml;': u'\xe4', '&ouml;': u'\xf6', '&Ccedil;': u'\xc7',
			 '&icirc;': u'\xee', '&euml;': u'\xeb', '&lt;': u'<', '&iquest;': u'\xbf',
			 '&eacute;': u'\xe9', '&ntilde;': u'\xf1', '&pound;': u'\xa3', '&Iuml;': u'\xcf',
			 '&Eacute;': u'\xc9', '&Ntilde;': u'\xd1', '&sup2;': u'\xb2', '&Acirc;': u'\xc2',
			 '&ccedil;': u'\xe7', '&Iacute;': u'\xcd', '&quot;': u'"', '&Aring;': u'\xc5',
			 '&macr;': u'\xaf', '&ordm;': u'\xba', '&Oslash;': u'\xd8', '&Yacute;': u'\xdd',
			 '&Uacute;': u'\xda', '&reg;': u'\xae', '&Otilde;': u'\xd5', '&iuml;': u'\xef',
			 '&ugrave;': u'\xf9', '&sup3;': u'\xb3', '&curren;': u'\xa4', '&copy;': u'\xa9',
			 '&oacute;': u'\xf3', '&para;': u'\xb6', '&Euml;': u'\xcb', '&uacute;': u'\xfa',
			 '&ograve;': u'\xf2', '&acirc;': u'\xe2', '&aacute;': u'\xe1', '&Agrave;': u'\xc0',
			 '&Oacute;': u'\xd3', '&sect;': u'\xa7', '&yacute;': u'\xfd', '&iacute;': u'\xed',
			 '&cent;': u'\xa2', '&Ocirc;': u'\xd4', '&otilde;': u'\xf5'}
		self.PathList = []
		self.DictList = []
	def __validateXpath(self, xPath):
		"""xPathOld = xPath
		xPath = re.sub('\[.*\]','',xPath)"""
		FieldList = string.split(xPath, '/')
		if len(FieldList) > self.MAX_NODES+2:
			check = False
		elif xPath[0] == '/':
			check = False
		else:
			check = True
		"""if check:
			i = 1
			while i != len(FieldList):
				checkId = string.find(FieldList[i],'id')
				checkName = string.find(FieldList[i],'name')
				if checkId == -1 and checkName == -1:
					check = False
				i = i + 1"""
		return check
	def __getIdFromNode(self, nodeStr):
		if string.find(nodeStr, 'id="') != -1:
			index1 = string.find(nodeStr, 'id="')
			index2 = string.find(nodeStr, '"]', index1+len('id="')+1)
			nodeId = nodeStr[index1+len('id="'):index2]
		elif string.find(nodeStr, 'name="') != -1:
			index1 = string.find(nodeStr, 'name="')
			index2 = string.find(nodeStr, '"]', index1+len('name="')+1)
			nodeId = nodeStr[index1+len('name="'):index2]
			nodeId = self.__decodeXPathName(nodeId)
		else:
			nodeId = nodeStr
		return nodeId
	def __getNodeDict(self, xPath):
		checkFormat = self.__validateXpath(xPath)
		if checkFormat:
			PathList = string.split(xPath,'/')
			pageId = PathList[0]
			PageDict = self.PageDict[pageId] 
			if type(PageDict) == ClassNodeDict:
				if len(PathList) == 2:
					mainNodeStr = PathList[1]
					mainNodeId = self.__getIdFromNode(mainNodeStr)
					try:
						NodeDict = self.PageDict[pageId][mainNodeId]
					except KeyError:
						raise PageXMLException(200)
				elif len(PathList) == 3:
					mainNodeStr = PathList[1]
					mainNodeId = self.__getIdFromNode(mainNodeStr)
					node1 = PathList[2]
					nodeId_1 = self.__getIdFromNode(node1)
					try:
						Node_a = self.PageDict[pageId][mainNodeId]['_value']
						NodeDict = self.__processNodeTypeGet(Node_a, nodeId_1)
					except KeyError:
						raise PageXMLException(200)
				elif len(PathList) == 4:
					mainNodeStr = PathList[1]
					mainNodeId = self.__getIdFromNode(mainNodeStr)
					node1 = PathList[2]
					nodeId_1 = self.__getIdFromNode(node1)
					node2 = PathList[3]
					nodeId_2 = self.__getIdFromNode(node2)
					try:
						Node_a = self.PageDict[pageId][mainNodeId]['_value']
						if type(Node_a) == types.ListType:
							entryValue = self.__getEntryValue(Node_a, nodeId_1)
							Node_b = Node_a[entryValue]['_value']
							NodeDict = self.__processNodeTypeGet(Node_b, nodeId_2)
						else:
							Node_b = Node_a[nodeId_1]['_value']
							NodeDict = self.__processNodeTypeGet(Node_b, nodeId_2)
					except KeyError:
						raise PageXMLException(200)
				elif len(PathList) == 5:
					mainNodeStr = PathList[1]
					mainNodeId = self.__getIdFromNode(mainNodeStr)
					node1 = PathList[2]
					nodeId_1 = self.__getIdFromNode(node1)
					node2 = PathList[3]
					nodeId_2 = self.__getIdFromNode(node2)
					node3 = PathList[4]
					nodeId_3 = self.__getIdFromNode(node3)
					try:
						Node_a = self.PageDict[pageId][mainNodeId]['_value']
						if type(Node_a) == types.ListType:
							entryValue = self.__getEntryValue(Node_a, nodeId_1)
							Node_b = Node_a[entryValue]['_value']
							if type(Node_b) == types.ListType:
								entryValue = self.__getEntryValue(Node_b, nodeId_2)
								Node_c = Node_b[entryValue]['_value']
								NodeDict = self.__processNodeTypeGet(Node_c, nodeId_3)
							else:
								Node_c = Node_b[nodeId_2]['_value']
								NodeDict = self.__processNodeTypeGet(Node_c, nodeId_3)
						else:
							Node_b = Node_a[nodeId_1]['_value']
							if type(Node_b) == types.ListType:
								entryValue = self.__getEntryValue(Node_b, nodeId_2)
								Node_c = Node_b[entryValue]['_value']
								NodeDict = self.__processNodeTypeGet(Node_c, nodeId_3)
							else:
								Node_c = Node_b[nodeId_2]['_value']
								NodeDict = self.__processNodeTypeGet(Node_c, nodeId_3)
					except KeyError:
						raise PageXMLException(200)
				elif len(PathList) == 6:
					mainNodeStr = PathList[1]
					mainNodeId = self.__getIdFromNode(mainNodeStr)
					node1 = PathList[2]
					nodeId_1 = self.__getIdFromNode(node1)
					node2 = PathList[3]
					nodeId_2 = self.__getIdFromNode(node2)
					node3 = PathList[4]
					nodeId_3 = self.__getIdFromNode(node3)
					node4 = PathList[5]
					nodeId_4 = self.__getIdFromNode(node4)
					try:
						Node_a = self.PageDict[pageId][mainNodeId]['_value']
						if type(Node_a) == types.ListType:
							entryValue = self.__getEntryValue(Node_a, nodeId_1)
							Node_b = Node_a[entryValue]['_value']
							if type(Node_b) == types.ListType:
								entryValue = self.__getEntryValue(Node_b, nodeId_2)
								Node_c = Node_b[entryValue]['_value']
								if type(Node_c) == types.ListType:
									entryValue = self.__getEntryValue(Node_c, nodeId_3)
									Node_d = Node_c[entryValue]['_value']
									NodeDict = self.__processNodeTypeGet(Node_d, nodeId_4)
								else:
									Node_d = Node_c[nodeId_3]['_value']
									NodeDict = self.__processNodeTypeGet(Node_d, nodeId_4)
							else:
								Node_c = Node_b[nodeId_2]['_value']
								if type(Node_c) == types.ListType:
									entryValue = self.__getEntryValue(Node_c, nodeId_3)
									Node_d = Node_c[entryValue]['_value']
									NodeDict = self.__processNodeTypeGet(Node_d, nodeId_4)
								else:
									Node_d = Node_c[nodeId_3]['_value']
									NodeDict = self.__processNodeTypeGet(Node_d, nodeId_4)
						else:
							Node_b = Node_a[nodeId_1]['_value']
							if type(Node_b) == types.ListType:
								entryValue = self.__getEntryValue(Node_b, nodeId_2)
								Node_c = Node_b[entryValue]['_value']
								if type(Node_c) == types.ListType:
									entryValue = self.__getEntryValue(Node_c, nodeId_3)
									Node_d = Node_c[entryValue]['_value']
									NodeDict = self.__processNodeTypeGet(Node_d, nodeId_4)
								else:
									Node_d = Node_c[nodeId_3]['_value']
									NodeDict = self.__processNodeTypeGet(Node_d, nodeId_4)
							else:
								Node_c = Node_b[nodeId_2]['_value']
								if type(Node_c) == types.ListType:
									entryValue = self.__getEntryValue(Node_c, nodeId_3)
									Node_d = Node_c[entryValue]['_value']
									NodeDict = self.__processNodeTypeGet(Node_d, nodeId_4)
								else:
									Node_d = Node_c[nodeId_3]['_value']
									NodeDict = self.__processNodeTypeGet(Node_d, nodeId_4)
					except KeyError:
						raise PageXMLException(200)
				elif len(PathList) == 7:
					mainNodeStr = PathList[1]
					mainNodeId = self.__getIdFromNode(mainNodeStr)
					node1 = PathList[2]
					nodeId_1 = self.__getIdFromNode(node1)
					node2 = PathList[3]
					nodeId_2 = self.__getIdFromNode(node2)
					node3 = PathList[4]
					nodeId_3 = self.__getIdFromNode(node3)
					node4 = PathList[5]
					nodeId_4 = self.__getIdFromNode(node4)
					node5 = PathList[6]
					nodeId_5 = self.__getIdFromNode(node5)
					try:
						Node_a = self.PageDict[pageId][mainNodeId]['_value']
						if type(Node_a) == types.ListType:
							entryValue = self.__getEntryValue(Node_a, nodeId_1)
							Node_b = Node_a[entryValue]['_value']
							if type(Node_b) == types.ListType:
								entryValue = self.__getEntryValue(Node_b, nodeId_2)
								Node_c = Node_b[entryValue]['_value']
								if type(Node_c) == types.ListType:
									entryValue = self.__getEntryValue(Node_c, nodeId_3)
									Node_d = Node_c[entryValue]['_value']
									if type(Node_d) == types.ListType:
										entryValue = self.__getEntryValue(Node_d, nodeId_4)
										Node_e = Node_d[entryValue]['_value']
										NodeDict = self.__processNodeTypeGet(Node_e, nodeId_5)
									else:
										Node_e = Node_d[nodeId_4]['_value']
										NodeDict = self.__processNodeTypeGet(Node_e, nodeId_5)
								else:
									Node_d = Node_c[nodeId_3]['_value']
									if type(Node_d) == types.ListType:
										entryValue = self.__getEntryValue(Node_d, nodeId_4)
										Node_e = Node_d[entryValue]['_value']
										NodeDict = self.__processNodeTypeGet(Node_e, nodeId_5)
									else:
										Node_e = Node_d[nodeId_4]['_value']
										NodeDict = self.__processNodeTypeGet(Node_e, nodeId_5)
							else:
								Node_c = Node_b[nodeId_2]['_value']
								if type(Node_c) == types.ListType:
									entryValue = self.__getEntryValue(Node_c, nodeId_3)
									Node_d = Node_c[entryValue]['_value']
									if type(Node_d) == types.ListType:
										entryValue = self.__getEntryValue(Node_d, nodeId_4)
										Node_e = Node_d[entryValue]['_value']
										NodeDict = self.__processNodeTypeGet(Node_e, nodeId_5)
									else:
										Node_e = Node_d[nodeId_4]['_value']
										NodeDict = self.__processNodeTypeGet(Node_e, nodeId_5)
								else:
									Node_d = Node_c[nodeId_3]['_value']
									if type(Node_d) == types.ListType:
										entryValue = self.__getEntryValue(Node_d, nodeId_4)
										Node_e = Node_d[entryValue]['_value']
										NodeDict = self.__processNodeTypeGet(Node_e, nodeId_5)
									else:
										Node_e = Node_d[nodeId_4]['_value']
										NodeDict = self.__processNodeTypeGet(Node_e, nodeId_5)
						else:
							Node_b = Node_a[nodeId_1]['_value']
							if type(Node_b) == types.ListType:
								entryValue = self.__getEntryValue(Node_b, nodeId_2)
								Node_c = Node_b[entryValue]['_value']
								if type(Node_c) == types.ListType:
									entryValue = self.__getEntryValue(Node_c, nodeId_3)
									Node_d = Node_c[entryValue]['_value']
									if type(Node_d) == types.ListType:
										entryValue = self.__getEntryValue(Node_d, nodeId_4)
										Node_e = Node_d[entryValue]['_value']
										NodeDict = self.__processNodeTypeGet(Node_e, nodeId_5)
									else:
										Node_e = Node_d[nodeId_4]['_value']
										NodeDict = self.__processNodeTypeGet(Node_e, nodeId_5)
								else:
									Node_d = Node_c[nodeId_3]['_value']
									if type(Node_d) == types.ListType:
										entryValue = self.__getEntryValue(Node_d, nodeId_4)
										Node_e = Node_d[entryValue]['_value']
										NodeDict = self.__processNodeTypeGet(Node_e, nodeId_5)
									else:
										Node_e = Node_d[nodeId_4]['_value']
										NodeDict = self.__processNodeTypeGet(Node_e, nodeId_5)
							else:
								Node_c = Node_b[nodeId_2]['_value']
								if type(Node_c) == types.ListType:
									entryValue = self.__getEntryValue(Node_c, nodeId_3)
									Node_d = Node_c[entryValue]['_value']
									if type(Node_d) == types.ListType:
										entryValue = self.__getEntryValue(Node_d, nodeId_4)
										Node_e = Node_d[entryValue]['_value']
										NodeDict = self.__processNodeTypeGet(Node_e, nodeId_5)
									else:
										Node_e = Node_d[nodeId_4]['_value']
										NodeDict = self.__processNodeTypeGet(Node_e, nodeId_5)
								else:
									Node_d = Node_c[nodeId_3]['_value']
									if type(Node_d) == types.ListType:
										entryValue = self.__getEntryValue(Node_d, nodeId_4)
										Node_e = Node_d[entryValue]['_value']
										NodeDict = self.__processNodeTypeGet(Node_e, nodeId_5)
									else:
										Node_e = Node_d[nodeId_4]['_value']
										NodeDict = self.__processNodeTypeGet(Node_e, nodeId_5)
					except KeyError:
						raise PageXMLException(200)
				else:
					NodeDict = self.PageDict[pageId]
			else:
				raise PageXMLException(100, pageId)
		else:
			raise PageXMLException(203)
		return NodeDict
	def __getEntryValue(self, Node, nodeId):
		List = Node
		i = 0
		entryValue = 0
		while i != len(List):
			Dict = List[i]
			nodeIdTarget = Dict['_id']
			if nodeIdTarget == nodeId:
				entryValue = i
			i = i + 1
		return entryValue
	def __processNodeType(self, Node, nodeId):
		if type(Node) == types.ListType:
			entryValue = self.__getEntryValue(Node, nodeId)
			NodeParent = Node[entryValue]['_value']
			parentType = Node[entryValue]['_type']
		else:
			NodeParent = Node[nodeId]['_value']
			parentType = Node[nodeId]['_type']
		if parentType == 'Key' or parentType == 'Entry':
			raise PageXMLException(206)
		Tuple = (NodeParent, parentType)
		return Tuple
	def __processNodeTypeGet(self, Node, nodeId):
		if type(Node) == types.ListType:
			entryValue = self.__getEntryValue(Node, nodeId)
			nodeI = entryValue
		else:
			nodeI = nodeId
		NodeDict = Node[nodeI]
		return NodeDict
	def __getNodeParent(self, xPath, nodeType):
		checkFormat = self.__validateXpath(xPath)
		if checkFormat:
			PathList = string.split(xPath,'/')
			pageId = PathList[0]
			PageDict = self.PageDict[pageId]
			if type(PageDict) == ClassNodeDict:
				if len(PathList) == 2:
					mainNodeStr = PathList[1]
					mainNodeId = self.__getIdFromNode(mainNodeStr)
					try:
						NodeParent = self.PageDict[pageId][mainNodeId]['_value']
						parentType = self.PageDict[pageId][mainNodeId]['_type']
						parentParentType = 'Page'
					except KeyError:
						raise PageXMLException(200)
				elif len(PathList) == 3:
					mainNodeStr = PathList[1]
					mainNodeId = self.__getIdFromNode(mainNodeStr)
					node1 = PathList[2]
					nodeId_1 = self.__getIdFromNode(node1)
					try:
						Node_a = self.PageDict[pageId][mainNodeId]['_value']
						(NodeParent, parentType) = self.__processNodeType(Node_a, nodeId_1)
						parentParentType = self.PageDict[pageId][mainNodeId]['_type']
					except KeyError:
						raise PageXMLException(200)
				elif len(PathList) == 4:
					mainNodeStr = PathList[1]
					mainNodeId = self.__getIdFromNode(mainNodeStr)
					node1 = PathList[2]
					nodeId_1 = self.__getIdFromNode(node1)
					node2 = PathList[3]
					nodeId_2 = self.__getIdFromNode(node2)
					#print pageId, mainNodeId, nodeId_1, nodeId_2
					try:
						Node_a = self.PageDict[pageId][mainNodeId]['_value']
						if type(Node_a) == types.ListType:
							entryValue = self.__getEntryValue(Node_a, nodeId_1)
							Node_b = Node_a[entryValue]['_value']
							(NodeParent, parentType) = self.__processNodeType(Node_b, nodeId_2)
							parentParentType = Node_a[entryValue]['_type']
						else:
							Node_b = Node_a[nodeId_1]['_value']
							(NodeParent, parentType) = self.__processNodeType(Node_b, nodeId_2)
							parentParentType = Node_a[nodeId_1]['_type']
					except KeyError:
						raise PageXMLException(200)
				elif len(PathList) == 5:
					mainNodeStr = PathList[1]
					mainNodeId = self.__getIdFromNode(mainNodeStr)
					node1 = PathList[2]
					nodeId_1 = self.__getIdFromNode(node1)
					node2 = PathList[3]
					nodeId_2 = self.__getIdFromNode(node2)
					node3 = PathList[4]
					nodeId_3 = self.__getIdFromNode(node3)
					try:
						Node_a = self.PageDict[pageId][mainNodeId]['_value']
						if type(Node_a) == types.ListType:
							entryValue = self.__getEntryValue(Node_a, nodeId_1)
							Node_b = Node_a[entryValue]['_value']
							if type(Node_b) == types.ListType:
								entryValue = self.__getEntryValue(Node_b, nodeId_2)
								Node_c = Node_b[entryValue]['_value']
								(NodeParent, parentType) = self.__processNodeType(Node_c, nodeId_3)
								parentParentType = Node_b[entryValue]['_type']
							else:
								Node_c = Node_b[nodeId_2]['_value']
								(NodeParent, parentType) = self.__processNodeType(Node_c, nodeId_3)
								parentParentType = Node_b[nodeId_2]['_type']
						else:
							Node_b = Node_a[nodeId_1]['_value']
							if type(Node_b) == types.ListType:
								entryValue = self.__getEntryValue(Node_b, nodeId_2)
								Node_c = Node_b[entryValue]['_value']
								(NodeParent, parentType) = self.__processNodeType(Node_c, nodeId_3)
								parentParentType = Node_b[entryValue]['_type']
							else:
								Node_c = Node_b[nodeId_2]['_value']
								(NodeParent, parentType) = self.__processNodeType(Node_c, nodeId_3)
								parentParentType = Node_b[nodeId_2]['_type']
					except KeyError:
						raise PageXMLException(200)
				elif len(PathList) == 6:
					mainNodeStr = PathList[1]
					mainNodeId = self.__getIdFromNode(mainNodeStr)
					node1 = PathList[2]
					nodeId_1 = self.__getIdFromNode(node1)
					node2 = PathList[3]
					nodeId_2 = self.__getIdFromNode(node2)
					node3 = PathList[4]
					nodeId_3 = self.__getIdFromNode(node3)
					node4 = PathList[5]
					nodeId_4 = self.__getIdFromNode(node4)
					try:
						Node_a = self.PageDict[pageId][mainNodeId]['_value']
						if type(Node_a) == types.ListType:
							entryValue = self.__getEntryValue(Node_a, nodeId_1)
							Node_b = Node_a[entryValue]['_value']
							if type(Node_b) == types.ListType:
								entryValue = self.__getEntryValue(Node_b, nodeId_2)
								Node_c = Node_b[entryValue]['_value']
								if type(Node_c) == types.ListType:
									entryValue = self.__getEntryValue(Node_c, nodeId_3)
									Node_d = Node_c[entryValue]['_value']
									(NodeParent, parentType) = self.__processNodeType(Node_d, nodeId_4)
									parentParentType = Node_c[entryValue]['_type']
								else:
									Node_d = Node_c[nodeId_3]['_value']
									(NodeParent, parentType) = self.__processNodeType(Node_d, nodeId_4)
									parentParentType = Node_c[nodeId_3]['_type']
							else:
								Node_c = Node_b[nodeId_2]['_value']
								if type(Node_c) == types.ListType:
									entryValue = self.__getEntryValue(Node_c, nodeId_3)
									Node_d = Node_c[entryValue]['_value']
									(NodeParent, parentType) = self.__processNodeType(Node_d, nodeId_4)
									parentParentType = Node_c[entryValue]['_type']
								else:
									Node_d = Node_c[nodeId_3]['_value']
									(NodeParent, parentType) = self.__processNodeType(Node_d, nodeId_4)
									parentParentType = Node_c[nodeId_3]['_type']
						else:
							Node_b = Node_a[nodeId_1]['_value']
							if type(Node_b) == types.ListType:
								entryValue = self.__getEntryValue(Node_b, nodeId_2)
								Node_c = Node_b[entryValue]['_value']
								if type(Node_c) == types.ListType:
									entryValue = self.__getEntryValue(Node_c, nodeId_3)
									Node_d = Node_c[entryValue]['_value']
									(NodeParent, parentType) = self.__processNodeType(Node_d, nodeId_4)
									parentParentType = Node_c[entryValue]['_type']
								else:
									Node_d = Node_c[nodeId_3]['_value']
									(NodeParent, parentType) = self.__processNodeType(Node_d, nodeId_4)
									parentParentType = Node_c[nodeId_3]['_type']
							else:
								Node_c = Node_b[nodeId_2]['_value']
								if type(Node_c) == types.ListType:
									entryValue = self.__getEntryValue(Node_c, nodeId_3)
									Node_d = Node_c[entryValue]['_value']
									(NodeParent, parentType) = self.__processNodeType(Node_d, nodeId_4)
									parentParentType = Node_c[entryValue]['_type']
								else:
									Node_d = Node_c[nodeId_3]['_value']
									(NodeParent, parentType) = self.__processNodeType(Node_d, nodeId_4)
									parentParentType = Node_c[nodeId_3]['_type']
					except KeyError:
						raise PageXMLException(200)
				elif len(PathList) == 7:
					mainNodeStr = PathList[1]
					mainNodeId = self.__getIdFromNode(mainNodeStr)
					node1 = PathList[2]
					nodeId_1 = self.__getIdFromNode(node1)
					node2 = PathList[3]
					nodeId_2 = self.__getIdFromNode(node2)
					node3 = PathList[4]
					nodeId_3 = self.__getIdFromNode(node3)
					node4 = PathList[5]
					nodeId_4 = self.__getIdFromNode(node4)
					node5 = PathList[6]
					nodeId_5 = self.__getIdFromNode(node5)
					try:
						Node_a = self.PageDict[pageId][mainNodeId]['_value']
						if type(Node_a) == types.ListType:
							entryValue = self.__getEntryValue(Node_a, nodeId_1)
							Node_b = Node_a[entryValue]['_value']
							if type(Node_b) == types.ListType:
								entryValue = self.__getEntryValue(Node_b, nodeId_2)
								Node_c = Node_b[entryValue]['_value']
								if type(Node_c) == types.ListType:
									entryValue = self.__getEntryValue(Node_c, nodeId_3)
									Node_d = Node_c[entryValue]['_value']
									if type(Node_d) == types.ListType:
										entryValue = self.__getEntryValue(Node_d, nodeId_4)
										Node_e = Node_d[entryValue]['_value']
										(NodeParent, parentType) = self.__processNodeType(Node_e, nodeId_5)
										parentParentType = Node_d[entryValue]['_type']
									else:
										Node_e = Node_d[nodeId_4]['_value']
										(NodeParent, parentType) = self.__processNodeType(Node_e, nodeId_5)
										parentParentType = Node_d[nodeId_4]['_type']
								else:
									Node_d = Node_c[nodeId_3]['_value']
									if type(Node_d) == types.ListType:
										entryValue = self.__getEntryValue(Node_d, nodeId_4)
										Node_e = Node_d[entryValue]['_value']
										(NodeParent, parentType) = self.__processNodeType(Node_e, nodeId_5)
										parentParentType = Node_d[entryValue]['_type']
									else:
										Node_e = Node_d[nodeId_4]['_value']
										(NodeParent, parentType) = self.__processNodeType(Node_e, nodeId_5)
										parentParentType = Node_d[nodeId_4]['_type']
							else:
								Node_c = Node_b[nodeId_2]['_value']
								if type(Node_c) == types.ListType:
									entryValue = self.__getEntryValue(Node_c, nodeId_3)
									Node_d = Node_c[entryValue]['_value']
									if type(Node_d) == types.ListType:
										entryValue = self.__getEntryValue(Node_d, nodeId_4)
										Node_e = Node_d[entryValue]['_value']
										(NodeParent, parentType) = self.__processNodeType(Node_e, nodeId_5)
										parentParentType = Node_d[entryValue]['_type']
									else:
										Node_e = Node_d[nodeId_4]['_value']
										(NodeParent, parentType) = self.__processNodeType(Node_e, nodeId_5)
										parentParentType = Node_d[nodeId_4]['_type']
								else:
									Node_d = Node_c[nodeId_3]['_value']
									if type(Node_d) == types.ListType:
										entryValue = self.__getEntryValue(Node_d, nodeId_4)
										Node_e = Node_d[entryValue]['_value']
										(NodeParent, parentType) = self.__processNodeType(Node_e, nodeId_5)
										parentParentType = Node_d[entryValue]['_type']
									else:
										Node_e = Node_d[nodeId_4]['_value']
										(NodeParent, parentType) = self.__processNodeType(Node_e, nodeId_5)
										parentParentType = Node_d[nodeId_4]['_type']
						else:
							Node_b = Node_a[nodeId_1]['_value']
							if type(Node_b) == types.ListType:
								entryValue = self.__getEntryValue(Node_b, nodeId_2)
								Node_c = Node_b[entryValue]['_value']
								if type(Node_c) == types.ListType:
									entryValue = self.__getEntryValue(Node_c, nodeId_3)
									Node_d = Node_c[entryValue]['_value']
									if type(Node_d) == types.ListType:
										entryValue = self.__getEntryValue(Node_d, nodeId_4)
										Node_e = Node_d[entryValue]['_value']
										(NodeParent, parentType) = self.__processNodeType(Node_e, nodeId_5)
										parentParentType = Node_d[entryValue]['_type']
									else:
										Node_e = Node_d[nodeId_4]['_value']
										(NodeParent, parentType) = self.__processNodeType(Node_e, nodeId_5)
										parentParentType = Node_d[nodeId_4]['_type']
								else:
									Node_d = Node_c[nodeId_3]['_value']
									if type(Node_d) == types.ListType:
										entryValue = self.__getEntryValue(Node_d, nodeId_4)
										Node_e = Node_d[entryValue]['_value']
										(NodeParent, parentType) = self.__processNodeType(Node_e, nodeId_5)
										parentParentType = Node_d[entryValue]['_type']
									else:
										Node_e = Node_d[nodeId_4]['_value']
										(NodeParent, parentType) = self.__processNodeType(Node_e, nodeId_5)
										parentParentType = Node_d[nodeId_4]['_type']
							else:
								Node_c = Node_b[nodeId_2]['_value']
								if type(Node_c) == types.ListType:
									entryValue = self.__getEntryValue(Node_c, nodeId_3)
									Node_d = Node_c[entryValue]['_value']
									if type(Node_d) == types.ListType:
										entryValue = self.__getEntryValue(Node_d, nodeId_4)
										Node_e = Node_d[entryValue]['_value']
										(NodeParent, parentType) = self.__processNodeType(Node_e, nodeId_5)
										parentParentType = Node_d[entryValue]['_type']
									else:
										Node_e = Node_d[nodeId_4]['_value']
										(NodeParent, parentType) = self.__processNodeType(Node_e, nodeId_5)
										parentParentType = Node_d[nodeId_4]['_type']
								else:
									Node_d = Node_c[nodeId_3]['_value']
									if type(Node_d) == types.ListType:
										entryValue = self.__getEntryValue(Node_d, nodeId_4)
										Node_e = Node_d[entryValue]['_value']
										(NodeParent, parentType) = self.__processNodeType(Node_e, nodeId_5)
										parentParentType = Node_d[entryValue]['_type']
									else:
										Node_e = Node_d[nodeId_4]['_value']
										(NodeParent, parentType) = self.__processNodeType(Node_e, nodeId_5)
										parentParentType = Node_d[nodeId_4]['_type']
					except KeyError:
						raise PageXMLException(200)
				else:
					NodeParent = self.PageDict[pageId]
					parentType = 'Page'
					parentParentType = ''
			else:
				raise PageXMLException(100, pageId)
		else:
			# Invalid format for xPath
			raise PageXMLException(203)
		if len(PathList) == 7 and parentType == 'Container' and nodeType == 'Container':
                        raise PageXMLException(215)
		if parentType == 'Container' or parentType == 'Section' or parentType == 'Page':
			checkKey = True
		else:
			checkKey = False
		if parentParentType == 'CollectionComplex' and parentType == 'Container' and nodeType != 'Key':
			raise PageXMLException(214)
		if nodeType == 'Key' and not checkKey:
			raise PageXMLException(204, xPath)
		elif parentType == 'Collection' and nodeType != 'Entry':
			raise PageXMLException(212, xPath)
		elif parentType == 'Container' and nodeType == 'Entry':
			raise PageXMLException(213, xPath)
		elif nodeType == 'Entry' and parentType != 'Collection':
			raise PageXMLException(205, xPath)
		return NodeParent
	def __getParentParentType(self, NodeDict):
		List = NodeDict.keys()
		parentParentType = ''
		return parentParentType
	def __getNodeType(self, nodeName):
		nodeNameLower = string.lower(nodeName)
		if string.find(nodeNameLower, 'entry') != -1:
			if (nodeNameLower.find('entry')+len('entry') == len(nodeNameLower)):
				nodeType = 'Entry'
			else:
				nodeType = 'KeySimple'
		elif string.find(nodeNameLower, 'container') != -1:
			if (nodeNameLower.find('container')+len('container') == len(nodeNameLower)):
				nodeType = 'Container'
			else:
				nodeType = 'KeySimple'
		elif string.find(nodeNameLower, 'collectioncomplex') != -1:
			if (nodeNameLower.find('collectioncomplex')+len('collectioncomplex') == len(nodeNameLower)):
				nodeType = 'CollectionComplex'
			else:
				nodeType = 'KeySimple'
		elif string.find(nodeNameLower, 'collection') != -1:
			if (nodeNameLower.find('collection')+len('collection') == len(nodeNameLower)):
				nodeType = 'Collection'
			else:
				nodeType = 'KeySimple'
		elif string.find(nodeNameLower, 'section') != -1:
			if (nodeNameLower.find('section')+len('section') == len(nodeNameLower)):
				nodeType = 'Section'
			else:
				nodeType = 'KeySimple'
		elif string.find(nodeNameLower, 'pagexml') != -1:
			if (nodeNameLower.find('pagexml')+len('pagexml') == len(nodeNameLower)):
				nodeType = 'PageXML'
			else:
				nodeType = 'KeySimple'
		elif string.find(nodeNameLower, 'key') != -1:
			if (nodeNameLower.find('key')+len('key') == len(nodeNameLower)):
				nodeType = 'Key'
			else:
				nodeType = 'KeySimple'
		else:
			nodeType = 'KeySimple'
		return nodeType
	def __doKey(self, KeyDict, cDataFlag):
		keyNodeName = KeyDict['_node_name']
		keyName = KeyDict['_name']
		keyValueTmp = KeyDict['_value']
		AttrDict = KeyDict['_attr']
		nodeType = KeyDict['_type']
		if keyValueTmp.find('<![CDATA[') != -1 and not cDataFlag:
			index1 = keyValueTmp.find('<![CDATA[')
			index2 = keyValueTmp.find(']]>', index1+1)
			keyValue = keyValueTmp[index1+len('<![CDATA['):index2]
		else:
			keyValue = keyValueTmp
		oEnXMLKey = EnXMLKey(keyNodeName, keyName, keyValue, AttrDict)
		if nodeType == 'KeySimple':
			oEnXMLKey.setType('KeySimple')
		return oEnXMLKey
	def __doKeyUpdate(self, oEnXMLKey):
		KeyDict = {}
		KeyDict['_name'] = oEnXMLKey.getName()
		KeyDict['_value'] = oEnXMLKey.getValue()
		KeyDict['_type'] = oEnXMLKey.getType()
		KeyDict['_node_name'] = oEnXMLKey.getNodeName()
		KeyDict['_attr'] = oEnXMLKey.getAttrDict()
		return KeyDict
	def __doContainer(self, Node):
		containerNodeName = Node['_node_name']
		containerId = Node['_id']
		AttrDict = Node['_attr']
		oEnXMLContainer = EnXMLContainer(containerNodeName, containerId, AttrDict)
		return oEnXMLContainer
	def __doContainerUpdate(self, oEnXMLContainer, ContainerDict):
		containerId = oEnXMLContainer.getId()
		ContainerDict[containerId] = {}
		ContainerDict[containerId]['_type'] = oEnXMLContainer.getType()
		ContainerDict[containerId]['_node_name'] = oEnXMLContainer.getNodeName()
		ContainerDict[containerId]['_id'] = oEnXMLContainer.getId()
		ContainerDict[containerId]['_value'] = {}
		return ContainerDict
	def __doCollection(self, Node):
		collectionNodeName = Node['_node_name']
		collectionId = Node['_id']
		AttrDict = Node['_attr']
		oEnXMLCollection = EnXMLCollection(collectionNodeName, collectionId, AttrDict)
		EntryList = Node['_value']
		i = 0
		while i != len(EntryList):
			EntryDict = Node['_value'][i]
			entryNodeName = EntryDict['_node_name']
			entryValue = EntryDict['_value']
			AttrDict = EntryDict['_attr']
			oEnXMLEntry = EnXMLEntry(entryNodeName, entryValue, AttrDict)
			oEnXMLCollection.addEntry(oEnXMLEntry)
			i = i + 1
		return oEnXMLCollection
	def __doCollectionUpdate(self, EnXMLCollection, ContainerDict):
		collectionId = EnXMLCollection.getId()
		List = []
		for EnXMLEntry in EnXMLCollection.getEntryList():
			ElementDict = {}
			ElementDict['_value'] = EnXMLEntry.getValue()
			ElementDict['_attr'] = EnXMLEntry.getAttrDict()
			ElementDict['_type'] = 'Entry'
			ElementDict['_node_name'] = EnXMLEntry.getNodeName()
			List.append(ElementDict)
		KeyDict = {}
		KeyDict['_node_name'] = EnXMLCollection.getNodeName()
		KeyDict['_id'] = EnXMLCollection.getId()
		KeyDict['_type'] = EnXMLCollection.getType()
		KeyDict['_attr'] = EnXMLCollection.getAttrDict()
		KeyDict['_value'] = List		
		ContainerDict[collectionId] = KeyDict
		return ContainerDict
	def __doCollectionComplex(self, NodeDict):
		collectionComplexNodeName = NodeDict['_node_name']
		collectionComplexId = NodeDict['_id']
		AttrDict = NodeDict['_attr']
		NodeList = NodeDict['_value']
		i = 0
		oEnXMLCollectionComplex = EnXMLCollectionComplex(collectionComplexNodeName, collectionComplexId, AttrDict)
		while i != len(NodeList):
			ContainerDict = NodeDict['_value'][i]
			containerNodeName = ContainerDict['_node_name']
			containerId = ContainerDict['_id']
			AttrDict = ContainerDict['_attr']
			oEnXMLContainer = EnXMLContainer(containerNodeName, containerId, AttrDict)
			KeyList = ContainerDict['_value'].keys()
			j = 0
			while j != len(KeyList):
				KeyDict = ContainerDict[KeyList[j]]
				keyNodeName = KeyDict['_node_name']
				keyName = KeyDict['_name']
				keyValue = KeyDict['_value']
				AttrDict = KeyDict['_attr']
				oEnXMLKey = EnXMLKey(keyNodeName, keyName, keyValue, AttrDict)
				oEnXMLContainer.addKey(oEnXMLKey)
				j = j + 1
			oEnXMLCollectionComplex.addContainer(oEnXMLContainer)
			i = i + 1
		return oEnXMLCollectionComplex
	def __doCollectionComplexUpdate(self, EnXMLCollectionComplex, ContainerDict):
		collectionComplexId = EnXMLCollectionComplex.getId()
		KeyDict = {}
		KeyDict['_node_name'] = EnXMLCollectionComplex.getNodeName()
		KeyDict['_id'] = EnXMLCollectionComplex.getId()
		KeyDict['_type'] = EnXMLCollectionComplex.getType()
		KeyDict['_attr'] = EnXMLCollectionComplex.getAttrDict()
		KeyDict['_value'] = []
		ContainerDict[collectionComplexId] = KeyDict
		return ContainerDict
	def __encodeXPath(self, xPath):
		targetStr = '@name="'
		index1 = xPath.find(targetStr)
		if index1 != -1:
			while index1 != -1:
				index2 = xPath.find('"', index1+len(targetStr)+1)
				piece = xPath[index1+len(targetStr):index2].encode(self.__Encoding)
				xPath = xPath[:index1+len(targetStr)] + urllib.quote_plus(piece) + xPath[index2:]
				index1 = xPath.find(targetStr, index2+1)
			xPathCoded = xPath
		else:
			xPathCoded = xPath
		return xPathCoded
	def __decodeXPathName(self, nameCodedStr):
		nameStr = unicode(urllib.unquote_plus(nameCodedStr.encode(self.__Encoding)), self.__Encoding)
		return nameStr
	def __encodeXPathName(self, nameStr):
		nameCodedStr = urllib.quote_plus(nameStr)
		return nameCodedStr
	def __unicodeWords(self, textStr, encode='utf-8'):
		List = textStr.split()
		i = 0
		ListUni = []
		while i != len(List):
			wordStr = List[i]
			try:
				wordUni = unicode(wordStr, encode)
			except UnicodeDecodeError:
				wordUni = u''
			ListUni.append(wordUni)
			i = i + 1
		textUni = string.join(ListUni)
		return textUni
	def enableTabs(self):
		"""Enable tab spaces indents when generating the XML."""
		self.TAB = 1
	def disableTabs(self):
		"""Disable tab spaces indents when generating the XML."""
		self.TAB = 0
	def setRootNode(self, idStr):
		self.Id = idStr
	def getAttrDict(self):
		return self.AttrDict
	def setAttrDict(self, AttrDict):
		self.AttrDict = AttrDict
	def setEncoding(self, encoding):
		self.__Encoding = encoding
	def addSection(self, xPath, sectionNodeName, sectionId):
		"""Adds a section to Page."""
		idStr = xPath
		NodeDict = self.PageDict[idStr]
		if type(NodeDict) == ClassNodeDict:
			ElementDict = {}
			ElementDict['_type'] = 'Section'
			ElementDict['_id'] = sectionId
			ElementDict['_value'] = ClassNodeDict()
			ElementDict['_node_name'] = sectionNodeName
			"""NodeDict[sectionId] = {}
			NodeDict[sectionId]['_type'] = 'Section'
			NodeDict[sectionId]['_id'] = sectionId
			NodeDict[sectionId]['_value'] = NodeDict()
			NodeDict[sectionId]['_node_name'] = sectionNodeName"""
			NodeDict[sectionId] = ElementDict
			self.IdDict[sectionId] = ElementDict
		else:
			raise PageXMLException(100, self.Id)
	def addContainer(self, xPath, containerNodeName, containerId, AttrDict={}):
		"""Add container at node with xPath."""
		xPathCoded = self.__encodeXPath(xPath)
		NodeParent = self.__getNodeParent(xPathCoded, 'Container')
		ElementDict = {}
		ElementDict['_node_name'] = containerNodeName
		ElementDict['_value'] = ClassNodeDict()
		ElementDict['_id'] = containerId
		ElementDict['_type'] = 'Container'
		ElementDict['_attr'] = AttrDict
		if type(NodeParent) == ClassNodeDict:
			NodeParent[containerId] = ElementDict
		elif type(NodeParent) == types.ListType:
			NodeParent.append(ElementDict)
		self.IdDict[containerId] = ElementDict
	def addCollection(self, xPath, collectionNodeName, collectionId, AttrDict={}):
		"""Adds a collection "collectionName" to container "sectionId"."""
		xPathCoded = self.__encodeXPath(xPath)
		NodeParent = self.__getNodeParent(xPathCoded, 'Collection')
		ElementDict = {}
		ElementDict['_type'] = 'Collection'
		ElementDict['_value'] = []
		ElementDict['_id'] = collectionId
		ElementDict['_node_name'] = collectionNodeName
		ElementDict['_attr'] = AttrDict
		if type(NodeParent) == ClassNodeDict:
			NodeParent[collectionId] = ElementDict
		elif type(NodeParent) == types.ListType:
			NodeParent.append(ElementDict)
		self.IdDict[collectionId] = ElementDict
	def addCollectionComplex(self, xPath, collectionNodeName, collectionId, AttrDict={}):
		"""Adds a collection container, "collectionName" to container in "sectionId". This
		collection container will have containers instead of entries."""
		xPathCoded = self.__encodeXPath(xPath)
		NodeParent = self.__getNodeParent(xPathCoded, 'CollectionComplex')
		ElementDict = {}
		ElementDict['_type'] = 'CollectionComplex'
		ElementDict['_value'] = []
		ElementDict['_id'] = collectionId
		ElementDict['_node_name'] = collectionNodeName
		ElementDict['_attr'] = AttrDict
		if type(NodeParent) == ClassNodeDict:
			NodeParent[collectionId] = ElementDict
		elif type(NodeParent) == types.ListType:
			NodeParent.append(ElementDict)
		self.IdDict[collectionId] = ElementDict
	def addKey(self, xPath, keyNodeName, keyName, keyValue, AttrDict={}):
		"""Add Key to xPath."""
		xPathCoded = self.__encodeXPath(xPath)
		NodeParent = self.__getNodeParent(xPathCoded, 'Key')
		ElementDict = {}
		ElementDict['_attr'] = AttrDict
		ElementDict['_node_name'] = keyNodeName
		ElementDict['_value'] = keyValue
		ElementDict['_type'] = 'Key'
		ElementDict['_name'] = keyName
		NodeParent[keyName] = ElementDict
	def addKeySimple(self, xPath, keyNodeName, keyValue, AttrDict={}):
		"""Add simple Key to xPath."""
		xPathCoded = self.__encodeXPath(xPath)
		NodeParent = self.__getNodeParent(xPathCoded, 'Key')
		ElementDict = {}
		ElementDict['_attr'] = AttrDict
		ElementDict['_node_name'] = keyNodeName
		ElementDict['_value'] = keyValue
		ElementDict['_type'] = 'KeySimple'
		ElementDict['_name'] = keyNodeName
		NodeParent[keyNodeName] = ElementDict
	def addEntry(self, xPath, entryNodeName, entryValue, AttrDict={}):
		"""Adds a collection entry line, with value and attributes."""
		xPathCoded = self.__encodeXPath(xPath)
		NodeParent = self.__getNodeParent(xPathCoded, 'Entry')
		ElementDict = {}
		ElementDict['_value'] = entryValue
		ElementDict['_attr'] = AttrDict
		ElementDict['_type'] = 'Entry'
		ElementDict['_node_name'] = entryNodeName
		NodeParent.append(ElementDict)
	def getContainer(self, xPath, cDataFlag=False):
		"""Get container EnXMLContainer at "xPath"."""
		xPathCoded = self.__encodeXPath(xPath)
		NodeDict = self.__getNodeDict(xPathCoded)
		if NodeDict['_type'] == 'Container':
			checkContainer = True
		else:
			checkContainer = False
		if checkContainer:
			Node_1 = NodeDict
			containerNodeName = Node_1['_node_name']
			containerId = Node_1['_id']
			AttrDict = Node_1['_attr']
			List_2 = Node_1['_value'].keys()
			i = 0
			oEnXMLContainer = EnXMLContainer(containerNodeName, containerId, AttrDict)
			while i != len(List_2):
				nodeId = List_2[i]
				Node_2  = Node_1['_value'][nodeId]
				nodeType = Node_2['_type']
				if nodeType == 'Key' or nodeType == 'KeySimple':
					oEnXMLKey_2 = self.__doKey(Node_2, cDataFlag)
					oEnXMLContainer.addKey(oEnXMLKey_2)
				elif nodeType == 'Container':
					oEnXMLContainer_2 = self.__doContainer(Node_2)
					List_3 = Node_2['_value'].keys()
					j = 0
					while j != len(List_3):
						Node_3 = Node_2['_value'][List_3[j]]
						nodeType = Node_3['_type']
						if nodeType == 'Key' or nodeType == 'KeySimple':
							oEnXMLKey_3 = self.__doKey(Node_3, cDataFlag)
							oEnXMLContainer_2.addKey(oEnXMLKey_3)
						elif nodeType == 'Container':
							oEnXMLContainer_3 = self.__doContainer(Node_3)
							List_4 = Node_3['_value'].keys()
							k = 0
							while k != len(List_4):
								Node_4 = Node_3['_value'][List_4[k]]
								nodeType = Node_4['_type']
								if nodeType == 'Key' or nodeType == 'KeySimple':
									oEnXMLKey_4 = self.__doKey(Node_4, cDataFlag)
									oEnXMLContainer_3.addKey(oEnXMLKey_4)
								elif nodeType == 'Container':
									oEnXMLContainer_4 = self.__doContainer(Node_4)
									List_5 = Node_4['_value'].keys()
									l = 0
									while l != len(List_5):
										Node_5 = Node_4['_value'][List_5[l]]
										nodeType = Node_5['_type']
										if nodeType == 'Key' or nodeType == 'KeySimple':
											oEnXMLKey_5 = self.__doKey(Node_5, cDataFlag)
											oEnXMLContainer_4.addKey(oEnXMLKey_5)
										elif nodeType == 'Container':
											oEnXMLContainer_5 = self.__doContainer(Node_5)
											List_6 = Node_5['_value'].keys()
											m = 0
											while m != len(List_6):
												Node_6 = Node_5['_value'][List_6[m]]
												nodeType = Node_6['_type']
												if nodeType == 'Key' or nodeType == 'KeySimple':
													oEnXMLKey_6 = self.__doKey(Node_6, cDataFlag)
													oEnXMLContainer_5.addKey(oEnXMLKey_6)
												elif nodeType == 'Container':
													oEnXMLContainer_6 = self.__doContainer(Node_6)
													List_7 = Node_6['_value'].keys()
													n = 0
													while n != len(List_7):
														Node_7 = Node_6['_value'][List_7[n]]
														nodeType = Node_7['_type']
														if nodeType == 'Key' or nodeType == 'KeySimple':
															oEnXMLKey_7 = self.__doKey(Node_7, cDataFlag)
															oEnXMLContainer_6.addKey(oEnXMLKey_7)
														n = n + 1
													oEnXMLContainer_5.addContainer(oEnXMLContainer_6)
												elif nodeType == 'Collection':
													oEnXMLCollection_6 = self.__doCollection(Node_6)
													oEnXMLContainer_5.addCollection(oEnXMLCollection_6)
												elif nodeType == 'CollectionComplex':
													oEnXMLCollectionComplex_6 = self.__doCollectionComplex(Node_6)
													oEnXMLContainer_5.addCollectionComplex(oEnXMLCollectionComplex_6)
												m = m + 1
											oEnXMLContainer_4.addContainer(oEnXMLContainer_5)
										elif nodeType == 'Collection':
											oEnXMLCollection_5 = self.__doCollection(Node_5)
											oEnXMLContainer_4.addCollection(oEnXMLCollection_5)
										elif nodeType == 'CollectionComplex':
											oEnXMLCollectionComplex_5 = self.__doCollectionComplex(Node_5)
											oEnXMLContainer_4.addCollectionComplex(oEnXMLCollectionComplex_5)
										l = l + 1
									oEnXMLContainer_3.addContainer(oEnXMLContainer_4)
								elif nodeType == 'Collection':
									oEnXMLCollection_4 = self.__doCollection(Node_4)
									oEnXMLContainer_3.addCollection(oEnXMLCollection_4)
								elif nodeType == 'CollectionComplex':
									oEnXMLCollectionComplex_4 = self.__doCollectionComplex(Node_4)
									oEnXMLContainer_3.addCollectionComplex(oEnXMLCollectionComplex_4)
								k = k + 1
							oEnXMLContainer_2.addContainer(oEnXMLContainer_3)
						elif nodeType == 'Collection':
							oEnXMLCollection_3 = self.__doCollection(Node_3)
							oEnXMLContainer_2.addCollection(oEnXMLCollection_3)
						elif nodeType == 'CollectionComplex':
							oEnXMLCollectionComplex_3 = self.__doCollectionComplex(Node_3)
							oEnXMLContainer_2.addCollectionComplex(oEnXMLCollectionComplex_3)
						j = j + 1
					oEnXMLContainer.addContainer(oEnXMLContainer_2)
				elif nodeType == 'Collection':
					oEnXMLCollection_2 = self.__doCollection(Node_2)
					oEnXMLContainer.addCollection(oEnXMLCollection_2)
				elif nodeType == 'CollectionComplex':
					oEnXMLCollectionComplex_2 = self.__doCollectionComplex(Node_2)
					oEnXMLContainer.addCollectionComplex(oEnXMLCollectionComplex_2)
				i = i + 1
		else:
			raise PageXMLException(207, xPath)
		return oEnXMLContainer
	def getContainerDict(self, iContainerId):
		ElementDict = self.IdDict[iContainerId]
		ContainerDict = {}
		List = ElementDict['_value'].keys()
		i = 0
		while i != len(List):
			ElementDict2 = ElementDict['_value'][List[i]]
			type = ElementDict2['_type']
			if type == 'Key' or type == 'KeySimple':
				#ContainerDict[ElementDict2['_name'].encode(self.__Encoding)] = ElementDict2['_value'].encode(self.__Encoding)
				ContainerDict[ElementDict2['_name'].encode(self.__Encoding)] = ElementDict2['_value']
			i = i + 1
		return ContainerDict
	def getContainerDictFull(self, iContainerId):
		"""Get full information for container: container info and key information. -> Tuple (AttrDict, ContainerDict)."""
		ElementDict = self.IdDict[iContainerId]
		ContainerDict = {}
		List = ElementDict['_value'].keys()
		i = 0
		while i != len(List):
			ElementDict2 = ElementDict['_value'][List[i]]
			type = ElementDict2['_type']
			if type == 'Key' or type == 'KeySimple':
				#ContainerDict[ElementDict2['_name'].encode(self.__Encoding)] = ElementDict2['_value'].encode(self.__Encoding)
				ContainerDict[ElementDict2['_name'].encode(self.__Encoding)] = ElementDict2['_value']
			i = i + 1
		Tuple = (ElementDict['_attr'], ContainerDict)
		return Tuple
	def getKeyValue(self, iContainerId, sName):
		ContainerDict = self.getContainerDict(iContainerId)
		if ContainerDict.has_key(sName):
			sValue = ContainerDict[sName]
		else:
			sValue = None
		return sValue
	def getCollection(self, xPath, cDataFlag=False):
		"""Get collection EnXMLCollection at "xPath"."""
		xPathCoded = self.__encodeXPath(xPath)
		NodeDict = self.__getNodeDict(xPathCoded)
		if NodeDict['_type'] == 'Collection':
			checkCollection = True
		else:
			checkCollection = False
		if checkCollection:
			collectionNodeName = NodeDict['_node_name']
			collectionId = NodeDict['_id']
			AttrDict = NodeDict['_attr']
			oEnXMLCollection = EnXMLCollection(collectionNodeName, collectionId, AttrDict)
			EntryList = NodeDict['_value']
			i = 0
			while i != len(EntryList):			
				EntryDict = NodeDict['_value'][i]
				entryNodeName = EntryDict['_node_name']
				entryValueTmp = EntryDict['_value']
				if entryValueTmp.find('<![CDATA[') != -1 and not cDataFlag:
					index1 = entryValueTmp.find('<![CDATA[')
					index2 = entryValueTmp.find(']]>', index1+1)
					entryValue = entryValueTmp[index1+len('<![CDATA['):index2]
				else:
					entryValue = entryValueTmp
				AttrDictTmp = EntryDict['_attr']
				List = AttrDictTmp.keys()
				j = 0
				AttrDict = {}
				while j != len(List):
					valueTmp = AttrDictTmp[List[j]]
					if valueTmp.find('<![CDATA[') != -1 and not cDataFlag:
						index1 = valueTmp.find('<![CDATA[')
						index2 = valueTmp.find(']]>', index1+1)
						attrValue = valueTmp[index1+len('<![CDATA['):index2]
					else:
						attrValue = valueTmp
					AttrDict[List[j]] = attrValue
					j = j  + 1
				oEnXMLEntry = EnXMLEntry(entryNodeName, entryValue, AttrDict)
				oEnXMLCollection.addEntry(oEnXMLEntry)
				i = i + 1
		else:
			raise PageXMLException(208, xPath)
		return oEnXMLCollection
	def getCollectionList(self, iCollectionId):
		"""Get collection entries. CollectionList is a list of dictionaries having the key "value" the entry value. ->  CollectionList."""
		ElementDict = self.IdDict[iCollectionId]
		CollectionList = []
		List = ElementDict['_value']
		i = 0
		while i != len(List):
			ElementDict2 = ElementDict['_value'][i]
			type = ElementDict2['_type']
			if type == 'Entry':
				AttrDict = ElementDict2['_attr']
				List2 = AttrDict.keys()
				j = 0
				AttrNewDict = {}
				while j != len(List2):
					sAttrName = List2[j].encode(self.__Encoding)
					#sAttrValue = AttrDict[sAttrName].encode(self.__Encoding)
					sAttrValue = AttrDict[sAttrName]
					AttrNewDict[sAttrName] = sAttrValue
					j = j + 1
				AttrNewDict['value'] = ElementDict2['_value']
				CollectionList.append(AttrNewDict)
			i = i + 1
		return CollectionList
	def getCollectionListFull(self, iCollectionId):
		"""Get complete information for collection: collection attribute information and entries. CollectionList is a list of dictionaries having the key "value" the entry value. -> Tuple(AttrDict, CollectionList)."""
		ElementDict = self.IdDict[iCollectionId]
		CollectionList = []
		List = ElementDict['_value']
		i = 0
		while i != len(List):
			ElementDict2 = ElementDict['_value'][i]
			type = ElementDict2['_type']
			if type == 'Entry':
				AttrDict = ElementDict2['_attr']
				List2 = AttrDict.keys()
				j = 0
				AttrNewDict = {}
				while j != len(List2):
					sAttrName = List2[j].encode(self.__Encoding)
					#sAttrValue = AttrDict[sAttrName].encode(self.__Encoding)
					sAttrValue = AttrDict[sAttrName]
					AttrNewDict[sAttrName] = sAttrValue
					j = j + 1
				AttrNewDict['value'] = ElementDict2['_value']
				CollectionList.append(AttrNewDict)
			i = i + 1
		Tuple = (ElementDict['_attr'], CollectionList)
		return Tuple
	def getCollectionComplex(self, xPath, cDataFlag=False):
		"""Get CollectionComplex EnXMLCollectionComplex at "xPath"."""
		xPathCoded = self.__encodeXPath(xPath)
		NodeDict = self.__getNodeDict(xPathCoded)
		if NodeDict['_type'] == 'CollectionComplex':
			checkCollectionComplex = True
		else:
			checkCollectionComplex = False
		if checkCollectionComplex:
			collectionComplexNodeName = NodeDict['_node_name']
			collectionComplexId = NodeDict['_id']
			AttrDict = NodeDict['_attr']
			NodeList = NodeDict['_value']
			i = 0
			oEnXMLCollectionComplex = EnXMLCollectionComplex(collectionComplexNodeName, collectionComplexId, AttrDict)
			while i != len(NodeList):
				ContainerDict = NodeDict['_value'][i]
				containerNodeName = ContainerDict['_node_name']
				containerId = ContainerDict['_id']
				xPathContainer = xPath + '/' + containerNodeName + '[@id="' + containerId + '"]'
				oEnXMLContainer = self.getContainer(xPathContainer, cDataFlag)
				oEnXMLCollectionComplex.addContainer(oEnXMLContainer)
				i = i + 1
		else:
			raise PageXMLException(209, xPath)
		return oEnXMLCollectionComplex
	def getCollectionComplexList(self, sCollectionComplexId):
		ElementDict = self.IdDict[sCollectionComplexId]
		CollectionComplexList = []
		List = ElementDict['_value']
		i = 0
		while i != len(List):
			ElementDict2 = ElementDict['_value'][i]
			type = ElementDict2['_type']
			if type == 'Container':
				ContainerDict = {}
				List = ElementDict2['_value'].keys()
				j = 0
				while j != len(List):
					ElementDict3 = ElementDict2['_value'][List[j]]
					type = ElementDict3['_type']
					if type == 'Key' or type == 'KeySimple':
						ContainerDict[ElementDict3['_name'].encode(self.__Encoding)] = ElementDict3['_value'].encode(self.__Encoding)
					j = j + 1
				CollectionComplexList.append(ContainerDict)
			i = i + 1
		return CollectionComplexList
	def getKey(self, xPath, cDataFlag=False):
		"""Get key EnXMLKey at "xPath"."""
		xPathCoded = self.__encodeXPath(xPath)
		NodeDict = self.__getNodeDict(xPathCoded)
		if NodeDict['_type'] == 'Key':
			checkKey = True
		else:
			checkKey = False
		if checkKey:
			oEnXMLKey = self.__doKey(NodeDict, cDataFlag)
		else:
			raise PageXMLException(210, xPath)
		return oEnXMLKey
	def getKeySimple(self, xPath, cDataFlag=False):
		"""Get key EnXMLKey at "xPath"."""
		xPathCoded = self.__encodeXPath(xPath)
		XPathList = string.split(xPathCoded, '/')
		keyNodeName = XPathList[len(XPathList)-1]
		xPath = xPath + '[@name="' + keyNodeName + '"]'
		NodeDict = self.__getNodeDict(xPath)
		if NodeDict['_type'] == 'KeySimple':
			checkKey = True
		else:
			checkKey = False
		if checkKey:
			oEnXMLKey = self.__doKey(NodeDict, cDataFlag)
		else:
			raise PageXMLException(210, xPath)
		return oEnXMLKey
	def getSection(self, xPath, cDataFlag=False):
		"""Get section EnXMLSection at "xPath"."""
		xPathCoded = self.__encodeXPath(xPath)
		NodeDict = self.__getNodeDict(xPathCoded)
		if NodeDict['_type'] == 'Section':
			checkSection = True
		else:
			checkSection = False
		if checkSection:
			sectionNodeName = NodeDict['_node_name']
			sectionId = NodeDict['_id']
			oEnXMLSection = EnXMLSection(sectionNodeName, sectionId)
			i = 0
			NodeList = NodeDict['_value'].keys()
			while i != len(NodeList):
				nodeId = NodeList[i]
				nodeType = NodeDict['_value'][nodeId]['_type']
				if nodeType == 'Key':
					oEnXMLKey = self.__doKey(NodeDict['_value'][nodeId], cDataFlag)
					oEnXMLSection.addKey(oEnXMLKey)
				elif nodeType == 'KeySimple':
					oEnXMLKey = self.__doKey(NodeDict['_value'][nodeId], cDataFlag)
					oEnXMLSection.addKey(oEnXMLKey)
				elif nodeType == 'Container':
					ContainerSecDict = NodeDict['_value'][nodeId]
					containerSecNodeName = ContainerSecDict['_node_name']
					containerSecId = ContainerSecDict['_id']
					xPathContainer = xPath + '/' + containerSecNodeName + '[@id="' + containerSecId + '"]'
					oEnXMLContainerSec = self.getContainer(xPathContainer, cDataFlag)
					oEnXMLSection.addContainer(oEnXMLContainerSec)
				elif nodeType == 'Collection':
					CollectionSecDict = NodeDict['_value'][nodeId]
					collectionSecNodeName = CollectionSecDict['_node_name']
					collectionSecId = CollectionSecDict['_id']
					xPathCollection = xPath + '/' + collectionSecNodeName + '[@id="' + collectionSecId + '"]'
					oEnXMLCollectionSec = self.getCollection(xPathCollection, cDataFlag)
					oEnXMLSection.addCollection(oEnXMLCollectionSec)
				elif nodeType == 'CollectionComplex':
					CollectionComplexDict = NodeDict['_value'][nodeId]
					collectionComplexNodeName = CollectionComplexDict['_node_name']
					collectionComplexId = CollectionComplexDict['_id']
					xPathCollectionComplex = xPath + '/' + collectionComplexNodeName + '[@id="' + collectionComplexId + '"]'
					oEnXMLCollectionComplex = self.getCollectionComplex(xPathCollectionComplex, cDataFlag)
					oEnXMLSection.addCollectionComplex(oEnXMLCollectionComplex)
				i = i + 1
		else:
			raise PageXMLException(211, xPath)
		return oEnXMLSection
	def getSectionDict(self, sSectionId):
		ElementDict = self.IdDict[sSectionId]
		SectionDict = {}
		List = ElementDict['_value'].keys()
		i = 0
		while i != len(List):
			ElementDict2 = ElementDict['_value'][List[i]]
			type = ElementDict2['_type']
			if type == 'Key' or type == 'KeySimple':
				SectionDict[ElementDict2['_name'].encode(self.__Encoding)] = ElementDict2['_value'].encode(self.__Encoding)
			i = i + 1
		return SectionDict
	def getSectionValue(self, sSectionId, sName):
		SectionDict = self.getSectionDict(sSectionId)
		if SectionDict.has_key(sName):
			sValue = SectionDict['sName']
		else:
			sValue = None
		return sValue
	def getPage(self, cDataFlag=False):
		"""Get page EnXMLPage at "xPath"."""
		Dict = self.PageDict[self.Id]
		AttrDict = self.getAttrDict()
		oEnXMLPage = EnXMLPage(self.Id)
		oEnXMLPage.setAttrDict(AttrDict)
		List = Dict.keys()
		i = 0
		while i != len(List):
			key = List[i]
			KeyDict = Dict[key]['_value']
			elementType = Dict[key]['_type']
			if elementType == 'Key':
				keyName = key
				keyNodeName = Dict[key]['_node_name']
				xPath = self.Id + '/' + keyNodeName + '[@name="' + keyName + '"]'
				oEnXMLKey = self.getKey(xPath, cDataFlag)
				oEnXMLPage.addKey(oEnXMLKey)
			elif elementType == 'KeySimple':
				keyName = key
				keyNodeName = Dict[key]['_node_name']
				xPath = self.Id + '/' + keyNodeName
				oEnXMLKey = self.getKeySimple(xPath, cDataFlag)
				oEnXMLPage.addKey(oEnXMLKey)
			elif elementType == 'Section':
				sectionId = key
				sectionNodeName = Dict[key]['_node_name']
				xPath = self.Id + '/' + sectionNodeName + '[@id="' + sectionId + '"]'
				oEnXMLSection = self.getSection(xPath, cDataFlag)
				oEnXMLPage.addSection(oEnXMLSection)
			elif elementType == 'Container':
				containerNodeName = Dict[key]['_node_name']
				containerId = Dict[key]['_id']
				xPathContainer = self.Id + '/' + containerNodeName + '[@id="' + containerId + '"]'
				oEnXMLContainer = self.getContainer(xPathContainer, cDataFlag)
				oEnXMLPage.addContainer(oEnXMLContainer)
			elif elementType == 'Collection':
				collectionNodeName = Dict[key]['_node_name']
				collectionId = Dict[key]['_id']
				xPathCollection = self.Id + '/' + collectionNodeName + '[@id="' + collectionId + '"]'
				oEnXMLCollection = self.getCollection(xPathCollection, cDataFlag)
				oEnXMLPage.addCollection(oEnXMLCollection)
			elif elementType == 'CollectionComplex':
				collectionComplexNodeName = Dict[key]['_node_name']
				collectionComplexId = Dict[key]['_id']
				xPathCollectionComplex = self.Id + '/' + collectionComplexNodeName + '[@id="' + collectionComplexId + '"]'
				oEnXMLCollectionComplex = self.getCollectionComplex(xPathCollectionComplex, cDataFlag)
				oEnXMLPage.addCollectionComplex(oEnXMLCollectionComplex)
			i = i + 1
		return oEnXMLPage
	def updateContainer(self, xPath, oEnXMLContainer):
		"""Updates container with EnXMLContainer."""
		xPathCoded = self.__encodeXPath(xPath)
		NodeDict = self.__getNodeDict(xPathCoded)
		if NodeDict['_type'] == 'Container':
			checkContainer = True
		else:
			checkContainer = False
		if checkContainer:
			ContainerDict = {}
			KeyList = oEnXMLContainer.getKeyList()
			i = 0
			while i != len(KeyList):
				KeyDict = self.__doKeyUpdate(KeyList[i])
				ContainerDict[KeyDict['_name']] = KeyDict
				i = i + 1
			ContainerList_1 = oEnXMLContainer.getContainerList()
			i = 0
			while i != len(ContainerList_1):
				oEnXMLContainer_1 = ContainerList_1[i]
				containerId_1 = oEnXMLContainer_1.getId()
				ContainerDict = self.__doContainerUpdate(oEnXMLContainer_1, ContainerDict)
				KeyList_1 = oEnXMLContainer_1.getKeyList()
				j = 0
				while j != len(KeyList_1):
					KeyDict_1 = self.__doKeyUpdate(KeyList_1[j])
					ContainerDict[containerId_1]['_value'][KeyDict_1['_name']] = KeyDict_1
					j = j + 1
				ContainerList_2 = oEnXMLContainer_1.getContainerList()
				j = 0
				while j != len(ContainerList_2):
					oEnXMLContainer_2 = ContainerList_2[j]
					containerId_2 = oEnXMLContainer_2.getId()
					ContainerDict = self.__doContainerUpdate(oEnXMLContainer_2, ContainerDict)
					KeyList_2 = oEnXMLContainer_2.getKeyList()
					ContainerList_3 = oEnXMLContainer_2.getContainerList()
					k = 0
					while k != len(KeyList_2):
						KeyDict_2 = self.__doKeyUpdate(KeyList_2[k])
						ContainerDict[containerId_1]['_value'][containerId_2]['_value'][KeyDict_2['_name']] = KeyDict_2
						k = k + 1
					k = 0
					while k != len(ContainerList_3):
						oEnXMLContainer_3 = ContainerList_3[k]
						containerId_3 = oEnXMLContainer_3.getId()
						ContainerDict = self.__doContainerUpdate(oEnXMLContainer_3, ContainerDict)
						KeyList_3 = oEnXMLContainer_3.getKeyList()
						ContainerList_4 = oEnXMLContainer_3.getContainerList()
						l = 0
						while l != len(KeyList_3):
							KeyDict_3 = self.__doKeyUpdate(KeyList_3[l])
							ContainerDict[containerId_1]['_value'][containerId_2]['_value'][containerId_3]['_value'][KeyDict_3['_name']] = KeyDict_3
							l = l + 1
						l = 0
						while l != len(ContainerList_4):
							oEnXMLContainer_4 = ContainerList_4[l]
							containerId_4 = oEnXMLContainer_4.getId()
							ContainerDict = self.__doContainerUpdate(oEnXMLContainer_4, ContainerDict)
							KeyList_4 = oEnXMLContainer_4.getKeyList()
							ContainerList_5 = oEnXMLContainer_4.getContainerList()
							m = 0
							while m != len(KeyList_4):
								KeyDict_4 = self.__doKeyUpdate(KeyList_4[m])
								ContainerDict[containerId_1]['_value'][containerId_2]['_value'][containerId_3]['_value'][containerId_4]['_value'][KeyDict_4['_name']] = KeyDict_4
								m = m + 1
							m = 0
							while m != len(ContainerList_5):
								oEnXMLContainer_5 = ContainerList_4[l]
								containerId_5 = oEnXMLContainer_5.getId()
								ContainerDict = self.__doContainerUpdate(oEnXMLContainer_5, ContainerDict)
								KeyList_5 = oEnXMLContainer_5.getKeyList()
								n = 0
								while n != len(KeyList_5):
									KeyDict_5 = self.__doKeyUpdate(KeyList_5[n])
									ContainerDict[containerId_1]['_value'][containerId_2]['_value'][containerId_3]['_value'][containerId_4]['_value'][containerId_5]['_value'][KeyDict_5['_name']] = KeyDict_5
									n = n + 1
								m = m + 1
							CollectionList_4 = oEnXMLContainer_4.getCollectionList()
							m = 0
							while m != len(CollectionList_4):
								EnXMLCollection_4 = CollectionList_4[m]
								ContainerDict = self.__doCollectionUpdate(EnXMLCollection_4, ContainerDict)
								m = m + 1
							CollectionComplexList_4 = oEnXMLContainer_4.getCollectionComplexList()
							m = 0
							while m != len(CollectionComplexList_4):
								EnXMLCollectionComplex_4 = CollectionComplexList_4[m]
								ContainerDict = self.__doCollectionComplexUpdate(EnXMLCollectionComplex_4, ContainerDict)
								m = m + 1
							l = l + 1
						CollectionList_3 = oEnXMLContainer_3.getCollectionList()
						l = 0
						while l != len(CollectionList_3):
							EnXMLCollection_3 = CollectionList_3[l]
							ContainerDict = self.__doCollectionUpdate(EnXMLCollection_3, ContainerDict)
							l = l + 1
						CollectionComplexList_3 = oEnXMLContainer_3.getCollectionComplexList()
						l = 0
						while l != len(CollectionComplexList_3):
							EnXMLCollectionComplex_3 = CollectionComplexList_3[l]
							ContainerDict = self.__doCollectionComplexUpdate(EnXMLCollectionComplex_3, ContainerDict)
							l = l + 1
						k = k + 1
					CollectionList_2 = oEnXMLContainer_2.getCollectionList()
					k = 0
					while k != len(CollectionList_2):
						EnXMLCollection_2 = CollectionList_2[k]
						ContainerDict = self.__doCollectionUpdate(EnXMLCollection_2, ContainerDict)
						k = k + 1
					CollectionComplexList_2 = oEnXMLContainer_2.getCollectionComplexList()
					k = 0
					while k != len(CollectionComplexList_2):
						EnXMLCollectionComplex_2 = CollectionComplexList_2[k]
						ContainerDict = self.__doCollectionComplexUpdate(EnXMLCollectionComplex_2, ContainerDict)
						k = k + 1
					j = j + 1
				CollectionList_1 = oEnXMLContainer_1.getCollectionList()
				j = 0
				while j != len(CollectionList_1):
					EnXMLCollection_1 = CollectionList_1[j]
					ContainerDict = self.__doCollectionUpdate(EnXMLCollection_1, ContainerDict)
					j = j + 1
				CollectionComplexList_1 = oEnXMLContainer_1.getCollectionComplexList()
				j = 0
				while j != len(CollectionComplexList_1):
					EnXMLCollectionComplex_1 = CollectionComplexList_1[j]
					ContainerDict = self.__doCollectionComplexUpdate(EnXMLCollectionComplex_1, ContainerDict)
					j = j + 1
				i = i + 1
			CollectionList = oEnXMLContainer.getCollectionList()
			i = 0
			while i != len(CollectionList):
				EnXMLCollection = CollectionList[i]
				ContainerDict = self.__doCollectionUpdate(EnXMLCollection, ContainerDict)
				i = i + 1
			CollectionComplexList = oEnXMLContainer.getCollectionComplexList()
			i = 0
			while i != len(CollectionComplexList):
				EnXMLCollectionComplex = CollectionComplexList[i]
				ContainerDict = self.__doCollectionComplexUpdate(EnXMLCollectionComplex, ContainerDict)
				i = i + 1
			NodeDict['_value'] = ContainerDict
		else:
			raise PageXMLException(207, xPath)
	def updateCollection(self, xPath, oEnXMLCollection):
		"""Updates collection with oEnXMLCollection."""
		xPathCoded = self.__encodeXPath(xPath)
		NodeDict = self.__getNodeDict(xPathCoded)
		if NodeDict['_type'] == 'Collection':
			checkCollection = True
		else:
			checkCollection = False
		if checkCollection:
			List = oEnXMLCollection.getEntryList()
			EntryList = []
			i = 0
			while i != len(List):
				oEnXMLEntry = List[i]
				entryNodeName = oEnXMLEntry.getNodeName()
				entryValue = oEnXMLEntry.getValue()
				AttrDict = oEnXMLEntry.getAttrDict()
				EntryDict = {}
				EntryDict['_node_name'] = entryNodeName
				EntryDict['_value'] = entryValue
				EntryDict['_attr'] = AttrDict
				EntryList.append(EntryDict)
				i = i + 1
			NodeDict['_value'] = EntryList
		else:
			raise PageXMLException(208, xPath)
	def updateCollectionComplex(self, xPath, oEnXMLCollectionComplex):
		"""Doc."""
		xPathCoded = self.__encodeXPath(xPath)
		NodeDict = self.__getNodeDict(xPathCoded)
		if NodeDict['_type'] == 'CollectionComplex':
			checkCollectionComplex = True
		else:
			checkCollectionComplex = False
		if checkCollectionComplex:
			List = oEnXMLCollectionComplex.getContainerList()
			i = 0
			ContainerList = []
			while i != len(List):
				oEnXMLContainer = List[i]
				ContainerDict = {}
				ContainerDict['_id'] = oEnXMLContainer.getId()
				ContainerDict['_node_name'] = oEnXMLContainer.getNodeName()
				ContainerDict['_type'] = oEnXMLContainer.getType()
				ContainerDict['_value'] = {}
				KeyList = oEnXMLContainer.getKeyList()
				j = 0
				while j != len(KeyList):
					oEnXMLKey = KeyList[j]
					keyName = oEnXMLKey.getName()
					keyValue = oEnXMLKey.getValue()
					AttrDict = oEnXMLKey.getAttrDict()
					keyNodeName = oEnXMLKey.getNodeName()
					keyType = oEnXMLKey.getType()
					KeyDict = {}
					KeyDict['_name'] = keyName
					KeyDict['_type'] = keyType
					KeyDict['_value'] = keyValue
					KeyDict['_attr'] = AttrDict
					KeyDict['_node_name'] = keyNodeName
					ContainerDict['_value'][keyName] = KeyDict
					j = j + 1
				ContainerList.append(ContainerDict)
				i = i + 1
			NodeDict['_value'] = ContainerList
		else:
			raise PageXMLException(209, xPath)
	def updateKey(self, xPath, oEnXMLKey):
		"""Updates key."""
		xPathCoded = self.__encodeXPath(xPath)
		NodeDict = self.__getNodeDict(xPathCoded)
		if NodeDict['_type'] == 'Key':
			checkKey = True
		else:
			checkKey = False
		if checkKey:
			keyValue = oEnXMLKey.getValue()
			AttrDict = oEnXMLKey.getAttrDict()
			NodeDict['_attr'] = AttrDict
			NodeDict['_value'] = keyValue
		else:
			raise PageXMLException(210, xPath)
	def updateKeySimple(self, xPath, oEnXMLKey):
		"""Updates key."""
		xPathCoded = self.__encodeXPath(xPath)
		XPathList = string.split(xPathCoded, '/')
		keyNodeName = XPathList[len(XPathList)-1]
		xPathKey = xPath + '[@name="' + keyNodeName + '"]'
		NodeDict = self.__getNodeDict(xPathKey)
		if NodeDict['_type'] == 'KeySimple':
			checkKey = True
		else:
			checkKey = False
		if checkKey:
			keyValue = oEnXMLKey.getValue()
			AttrDict = oEnXMLKey.getAttrDict()
			NodeDict['_attr'] = AttrDict
			NodeDict['_value'] = keyValue
		else:
			raise PageXMLException(210, xPath)
	
	def deleteSection(self, xPath):
		"""Deletes section."""
		xPathCoded = self.__encodeXPath(xPath)
		NodeDict = self.__getNodeDict(xPathCoded)
		sId = NodeDict['_id']
		Dict = self.PageDict['PageXML'][sId]
		del self.PageDict['PageXML'][sId]
	
	def resetSection(self, xPath):
		xPathCoded = self.__encodeXPath(xPath)
		NodeDict = self.__getNodeDict(xPathCoded)
		sId = NodeDict['_id']
		Dict = self.PageDict['PageXML'][sId]
		Dict['_value'] = {}
	
	def updateSection(self, xPath, oEnXMLSection):
		"""Updates section with EnXMLSection."""
		xPathCoded = self.__encodeXPath(xPath)
		NodeDict = self.__getNodeDict(xPathCoded)
		if NodeDict['_type'] == 'Section':
			checkSection = True
		else:
			checkSection = False
		if checkSection:
			KeyList = oEnXMLSection.getKeyList()
			i = 0
			while i != len(KeyList):
				oEnXMLKey = KeyList[i]
				keyNodeName = oEnXMLKey.getNodeName()
				keyName = oEnXMLKey.getName()
				if keyName == '':
					xPathKey = xPath + '/' + keyNodeName + '[@name="' + keyNodeName + '"]'
				else:
					xPathKey = xPath + '/' + keyNodeName + '[@name="' + keyName + '"]'
				self.updateKey(xPathKey, oEnXMLKey)
				i = i + 1
			ContainerList = oEnXMLSection.getContainerList()
			i = 0
			while i != len(ContainerList):
				oEnXMLContainer = ContainerList[i]
				containerNodeName = oEnXMLContainer.getNodeName()
				containerId = oEnXMLContainer.getId()
				xPathContainer = xPath + '/' + containerNodeName + '[@id="]' + containerId + '"]'
				self.updateContainer(xPathContainer, oEnXMLContainer)
				i = i + 1
			CollectionList = oEnXMLSection.getCollectionList()
			i = 0
			while i != len(CollectionList):
				oEnXMLCollection = CollectionList[i]
				collectionNodeName = oEnXMLCollection.getNodeName()
				collectionId = oEnXMLCollection.getId()
				xPathCollection = xPath + '/' + collectionNodeName + '[@id="' + collectionId + '"]'
				self.updateCollection(xPathCollection, oEnXMLCollection)
				i = i + 1
			CollectionComplexList = oEnXMLSection.getCollectionComplexList()
			i = 0
			while i != len(CollectionComplexList):
				oEnXMLCollectionComplex = CollectionComplexList[i]
				collectionComplexNodeName = oEnXMLCollectionComplex.getNodeName()
				collectionComplexId = oEnXMLCollectionComplex.getId()
				xPathCollectionComplex = xPath + '/' + collectionComplexNodeName + '[@id="' + collectionComplexId + '"]'
				self.updateCollectionComplex(xPathCollectionComplex, oEnXMLCollectionComplex)
				i = i + 1
		else:
			raise PageXMLException(211, xPath)
	def updatePage(self, oEnXMLPage):
		"""Updates page with EnXMLPage."""
		KeyList = oEnXMLPage.getKeyList()
		xPath = 'PageXML'
		i = 0
		while i != len(KeyList):
			oEnXMLKey = KeyList[i]
			keyNodeName = oEnXMLKey.getNodeName()
			keyName = oEnXMLKey.getName()
			keyType = oEnXMLKey.getType() 
			if keyType == 'KeySimple':
				xPathKey = xPath + '/' + keyNodeName
				self.updateKeySimple(xPathKey, oEnXMLKey)
			else:
				xPathKey = xPath + '/' + keyNodeName + '[@name="' + keyName + '"]'
				self.updateKey(xPathKey, oEnXMLKey)
			i = i + 1
		ContainerList = oEnXMLPage.getContainerList()
		i = 0
		while i != len(ContainerList):
			oEnXMLContainer = ContainerList[i]
			containerNodeName = oEnXMLContainer.getNodeName()
			containerId = oEnXMLContainer.getId()
			xPathContainer = xPath + '/' + containerNodeName + '[@id="' + containerId + '"]'
			self.updateContainer(xPathContainer, oEnXMLContainer)
			i = i + 1
		CollectionList = oEnXMLPage.getCollectionList()
		i = 0
		while i != len(CollectionList):
			oEnXMLCollection = CollectionList[i]
			collectionNodeName = oEnXMLCollection.getNodeName()
			collectionId = oEnXMLCollection.getId()
			xPathCollection = xPath + '/' + collectionNodeName + '[@id="' + collectionId + '"]'
			self.updateCollection(xPathCollection, oEnXMLCollection)
			i = i + 1
		CollectionComplexList = oEnXMLPage.getCollectionComplexList()
		i = 0
		while i != len(CollectionComplexList):
			oEnXMLCollectionComplex = CollectionComplexList[i]
			collectionComplexNodeName = oEnXMLCollectionComplex.getNodeName()
			collectionComplexId = oEnXMLCollectionComplex.getId()
			xPathCollectionComplex = xPath + '/' + collectionComplexNodeName + '[@id="' + collectionComplexId + '"]'
			self.updateCollectionComplex(xPathCollectionComplex, oEnXMLCollectionComplex)
			i = i + 1
	def __buildAttrStr(self, AttrDict):
		i = 0
		List = AttrDict.keys()
		ListAttr = []
		attrStr = ''
		while i != len(List):
			attrName = List[i]
			if attrName != 'name':
				ListAttr.append(List[i] + '="' + AttrDict[List[i]] + '"')
			i = i + 1
		if len(ListAttr) != 0:
			attrStr = ' ' + string.join(ListAttr, ' ')
		else:
			attrStr = ''
		return attrStr
	def __scapeAmp(self, text):
		"""Convert the html special characters, like &oacute; or &#126; to unicode
		chars using HtmlDict. Then, replace the "&" char to "&amp;"."""
		WordList = string.split(text)
		w = 0
		html_dict = self.HtmlDict
		WordListNew = []
		while w != len(WordList):
			word = WordList[w]
			if string.find(word, '&') != -1:
				if  not re.search('&\w+;',word) and not re.search('&#\w+;',word):
					word = string.replace(word, '&', '&amp;')
			WordListNew.append(word)
			w = w + 1
		textNew = string.join(WordListNew, ' ')
		return textNew
	def toXml(self, tabFlag=0, encoding="utf-8", dtdPath=None):
		self.__Encoding = encoding
		oEnXMLPage = self.getPage(True)
		xml = oEnXMLPage.toXml(tabFlag, encoding, dtdPath)
		return xml
	def parse(self, xmlStr):
		if len(xmlStr) != 0:
			List = xmlStr.split()
			encodingStr = xmlStr.split()[2]
			index1 = encodingStr.find('"')
			index2 = encodingStr.find('"', index1+1)
			self.__Encoding = encodingStr[index1+1:index2].lower()
			self.oParser = xml.parsers.expat.ParserCreate()
			self.oParser.StartElementHandler = self.__startElement
			self.oParser.EndElementHandler = self.__endElement
			self.oParser.CharacterDataHandler = self.__charData
			check = self.oParser.Parse(xmlStr, 1)
	def getEncoding(self):
		return self.__Encoding
	def __startElement(self, name, AttrDict):
		nodeType = self.__getNodeType(name)
		if nodeType == 'PageXML':
			self.AttrDict = AttrDict
			xPathPage = 'PageXML'
			self.PathList.append(xPathPage)
		elif nodeType == 'Key':
			Dict = {}
			Dict['_type'] = nodeType
			Dict['_value'] = ''
			Dict['_node_name'] = name
			if AttrDict.has_key('name'):
				Dict['_name'] = AttrDict['name']
			else:
				Dict['_name'] = ''
			Dict['_attr'] = AttrDict
			xPath = self.PathList[len(self.PathList)-1]
			self.addKey(xPath, name, Dict['_name'], '', AttrDict)
			self.PathList.append(xPath)
			self.DictList.append(Dict)
		elif nodeType == 'KeySimple':
			Dict = {}
			Dict['_type'] = nodeType
			Dict['_value'] = ''
			Dict['_node_name'] = name
			Dict['_name'] = name
			Dict['_attr'] = AttrDict
			xPath = self.PathList[len(self.PathList)-1]
			self.addKeySimple(xPath, name, '', AttrDict)
			self.PathList.append(xPath)
			self.DictList.append(Dict)
		elif nodeType == 'Container':
			containerNodeName = name
			containerId = AttrDict['id']
			Dict = {}
			Dict['_node_name'] = containerNodeName
			Dict['_id'] = containerId
			Dict['_type'] = nodeType
			Dict['_attr'] = AttrDict
			Dict['_value'] = {}
			xPath = self.PathList[len(self.PathList)-1]
			self.addContainer(xPath, containerNodeName, containerId, AttrDict)
			xPathNew = xPath + '/' + containerNodeName + '[@id="' + containerId + '"]'
			self.PathList.append(xPathNew)
			self.DictList.append(Dict)
		elif nodeType == 'Collection':
			collectionNodeName = name
			#print 'collectionNodeName->', collectionNodeName
			collectionId = AttrDict['id']
			Dict = {}
			Dict['_node_name'] = collectionNodeName
			Dict['_id'] = collectionId
			Dict['_type'] = nodeType
			Dict['_attr'] = AttrDict
			Dict['_value'] = []
			xPath = self.PathList[len(self.PathList)-1]
			self.addCollection(xPath, collectionNodeName, collectionId, AttrDict)
			xPathNew = xPath + '/' + collectionNodeName + '[@id="' + collectionId + '"]'
			self.PathList.append(xPathNew)
			self.DictList.append(Dict)
		elif nodeType == 'Entry':
			Dict = {}
			Dict['_type'] = nodeType
			Dict['_value'] = ''
			Dict['_node_name'] = name
			Dict['_attr'] = AttrDict
			xPath = self.PathList[len(self.PathList)-1]
			self.PathList.append(xPath)
			self.DictList.append(Dict)			
		elif nodeType == 'CollectionComplex':
			collectionComplexNodeName = name
			collectionComplexId = AttrDict['id']
			Dict = {}
			Dict['_node_name'] = collectionComplexNodeName
			Dict['_id'] = collectionComplexId
			Dict['_type'] = nodeType
			Dict['_attr'] = AttrDict
			Dict['_value'] = []
			xPath = self.PathList[len(self.PathList)-1]
			self.addCollectionComplex(xPath, collectionComplexNodeName, collectionComplexId, AttrDict)
			xPathNew = xPath + '/' + collectionComplexNodeName + '[@id="' + collectionComplexId + '"]'
			self.PathList.append(xPathNew)
			self.DictList.append(Dict)
		elif nodeType == 'Section':
			sectionNodeName = name
			sectionId = AttrDict['id']
			Dict = {}
			Dict['_id'] = sectionId
			Dict['_node_name'] = sectionNodeName
			Dict['_type'] = nodeType
			Dict['_value'] = {}
			xPath = self.PathList[len(self.PathList)-1]
			self.addSection(xPath, sectionNodeName, sectionId)
			xPathNew = xPath + '/' + sectionNodeName + '[@id="' + sectionId + '"]'
			self.PathList.append(xPathNew)
			self.DictList.append(Dict)
	def __charData(self, data):
		self.__DataStr = self.__DataStr + data
	def __endElement(self, name):
		if len(self.DictList) != 0:
			Dict = self.DictList[len(self.DictList)-1]
			nodeType = Dict['_type']
		else:
			nodeType = None
		if len(self.PathList) != 0:
			xPath = self.PathList[len(self.PathList)-1]
		if nodeType == 'Key':
			keyNodeName = Dict['_node_name']
			keyName = Dict['_name']
			value = self.__DataStr
			keyValue = value.replace('\t','').lstrip()
			AttrDict = Dict['_attr']
			oEnXMLKey = EnXMLKey(keyNodeName, keyName, keyValue, AttrDict)
			xPath = xPath + '/' + keyNodeName + '[@name="' + keyName + '"]'
			self.updateKey(xPath, oEnXMLKey)
		elif nodeType == 'KeySimple':
			keyNodeName = Dict['_node_name']
			value = self.__DataStr
			keyValue = value.replace('\t','').lstrip()
			AttrDict = Dict['_attr']
			oEnXMLKey = EnXMLKey(keyNodeName, keyNodeName, keyValue, AttrDict)
			xPath = xPath + '/' + keyNodeName
			self.updateKeySimple(xPath, oEnXMLKey)
		elif nodeType == 'Entry':
			entryNodeName = Dict['_node_name']
			value = self.__DataStr
			entryValue = value.replace('\t','').lstrip()
			AttrDict = Dict['_attr']
			self.addEntry(xPath, entryNodeName, entryValue, AttrDict)
		if len(self.PathList) != 0:
			del self.PathList[len(self.PathList)-1]
		if len(self.DictList) != 0:
			del self.DictList[len(self.DictList)-1]
		self.__DataStr = ''

class RdfXML(PageXML):
	Id = 'rdf:RDF'
	TAB = 0
	def __init__(self, AttrDict={}):
		self.AttrDict = AttrDict
		self.Id = 'rdf:RDF'
		self.PageDict[self.Id] = {}
		self.HtmlDict = {'&Ecirc;': u'\xca', '&raquo;': u'\xbb', '&eth;': u'\xf0', '&divide;': u'\xf7',
			 '&atilde;': u'\xe3', '&sup1;': u'\xb9', '&THORN;': u'\xde', '&ETH;': u'\xd0',
			 '&frac34;': u'\xbe', '&nbsp;': u'\xa0', '&Auml;': u'\xc4', '&Ouml;': u'\xd6',
			 '&Egrave;': u'\xc8', '&acute;': u'\xb4', '&Icirc;': u'\xce', '&deg;': u'\xb0',
			 '&middot;': u'\xb7', '&ocirc;': u'\xf4', '&Ugrave;': u'\xd9', '&gt;': u'>',
			 '&ordf;': u'\xaa', '&uml;': u'\xa8', '&aring;': u'\xe5', '&frac12;': u'\xbd',
			 '&iexcl;': u'\xa1', '&frac14;': u'\xbc', '&Aacute;': u'\xc1', '&szlig;': u'\xdf',
			 '&igrave;': u'\xec', '&aelig;': u'\xe6', '&yen;': u'\xa5', '&times;': u'\xd7',
			 '&egrave;': u'\xe8', '&Atilde;': u'\xc3', '&Igrave;': u'\xcc', '&ucirc;': u'\xfb',
			 '&brvbar;': u'\xa6', '&micro;': u'\xb5', '&agrave;': u'\xe0', '&thorn;': u'\xfe',
			 '&Ucirc;': u'\xdb', '&amp;': u'&', '&uuml;': u'\xfc', '&ecirc;': u'\xea',
			 '&laquo;': u'\xab', '&not;': u'\xac', '&Ograve;': u'\xd2', '&oslash;': u'\xf8',
			 '&Uuml;': u'\xdc', '&cedil;': u'\xb8', '&plusmn;': u'\xb1', '&AElig;': u'\xc6',
			 '&shy;': u'\xad', '&auml;': u'\xe4', '&ouml;': u'\xf6', '&Ccedil;': u'\xc7',
			 '&icirc;': u'\xee', '&euml;': u'\xeb', '&lt;': u'<', '&iquest;': u'\xbf',
			 '&eacute;': u'\xe9', '&ntilde;': u'\xf1', '&pound;': u'\xa3', '&Iuml;': u'\xcf',
			 '&Eacute;': u'\xc9', '&Ntilde;': u'\xd1', '&sup2;': u'\xb2', '&Acirc;': u'\xc2',
			 '&ccedil;': u'\xe7', '&Iacute;': u'\xcd', '&quot;': u'"', '&Aring;': u'\xc5',
			 '&macr;': u'\xaf', '&ordm;': u'\xba', '&Oslash;': u'\xd8', '&Yacute;': u'\xdd',
			 '&Uacute;': u'\xda', '&reg;': u'\xae', '&Otilde;': u'\xd5', '&iuml;': u'\xef',
			 '&ugrave;': u'\xf9', '&sup3;': u'\xb3', '&curren;': u'\xa4', '&copy;': u'\xa9',
			 '&oacute;': u'\xf3', '&para;': u'\xb6', '&Euml;': u'\xcb', '&uacute;': u'\xfa',
			 '&ograve;': u'\xf2', '&acirc;': u'\xe2', '&aacute;': u'\xe1', '&Agrave;': u'\xc0',
			 '&Oacute;': u'\xd3', '&sect;': u'\xa7', '&yacute;': u'\xfd', '&iacute;': u'\xed',
			 '&cent;': u'\xa2', '&Ocirc;': u'\xd4', '&otilde;': u'\xf5'}
		self.oParser = xml.parsers.expat.ParserCreate()
		self.oParser.StartElementHandler = self.__startElement
		self.oParser.EndElementHandler = self.__endElement
		self.oParser.CharacterDataHandler = self.__charData


class XMLMixEngine:
	Html = ''
	def __init__(self, xsl_path, xml_path):
		sablotPath = '/usr/local/bin/sabcmd'
		webRootPath = '/www/'
		id = str(int(time.time())) + '_' + str(random.randint(0,999999))
		sablotOutPath = '/www/sablot_out/' + id + '.html'
		cmdPath = sablotPath + ' ' + webRootPath + xsl_path + ' ' + webRootPath + xml_path + ' ' + sablotOutPath
		os.system(cmdPath)
		f = open(sablotOutPath)
		html = f.read()
		f.close()
		os.remove(sablotOutPath)
		self.Html = html
	def getHtml(self):
		return self.Html

class XmlTools:    
	ENCODING = "UTF-8"
	def __init__(self):
		self.HtmlDict = {'&Ecirc;': u'\xca', '&raquo;': u'\xbb', '&eth;': u'\xf0', '&divide;': u'\xf7',
			 '&atilde;': u'\xe3', '&sup1;': u'\xb9', '&THORN;': u'\xde', '&ETH;': u'\xd0',
			 '&frac34;': u'\xbe', '&nbsp;': u'\xa0', '&Auml;': u'\xc4', '&Ouml;': u'\xd6',
			 '&Egrave;': u'\xc8', '&acute;': u'\xb4', '&Icirc;': u'\xce', '&deg;': u'\xb0',
			 '&middot;': u'\xb7', '&ocirc;': u'\xf4', '&Ugrave;': u'\xd9', '&gt;': u'>',
			 '&ordf;': u'\xaa', '&uml;': u'\xa8', '&aring;': u'\xe5', '&frac12;': u'\xbd',
			 '&iexcl;': u'\xa1', '&frac14;': u'\xbc', '&Aacute;': u'\xc1', '&szlig;': u'\xdf',
			 '&igrave;': u'\xec', '&aelig;': u'\xe6', '&yen;': u'\xa5', '&times;': u'\xd7',
			 '&egrave;': u'\xe8', '&Atilde;': u'\xc3', '&Igrave;': u'\xcc', '&ucirc;': u'\xfb',
			 '&brvbar;': u'\xa6', '&micro;': u'\xb5', '&agrave;': u'\xe0', '&thorn;': u'\xfe',
			 '&Ucirc;': u'\xdb', '&amp;': u'&', '&uuml;': u'\xfc', '&ecirc;': u'\xea',
			 '&laquo;': u'\xab', '&not;': u'\xac', '&Ograve;': u'\xd2', '&oslash;': u'\xf8',
			 '&Uuml;': u'\xdc', '&cedil;': u'\xb8', '&plusmn;': u'\xb1', '&AElig;': u'\xc6',
			 '&shy;': u'\xad', '&auml;': u'\xe4', '&ouml;': u'\xf6', '&Ccedil;': u'\xc7',
			 '&icirc;': u'\xee', '&euml;': u'\xeb', '&lt;': u'<', '&iquest;': u'\xbf',
			 '&eacute;': u'\xe9', '&ntilde;': u'\xf1', '&pound;': u'\xa3', '&Iuml;': u'\xcf',
			 '&Eacute;': u'\xc9', '&Ntilde;': u'\xd1', '&sup2;': u'\xb2', '&Acirc;': u'\xc2',
			 '&ccedil;': u'\xe7', '&Iacute;': u'\xcd', '&quot;': u'"', '&Aring;': u'\xc5',
			 '&macr;': u'\xaf', '&ordm;': u'\xba', '&Oslash;': u'\xd8', '&Yacute;': u'\xdd',
			 '&Uacute;': u'\xda', '&reg;': u'\xae', '&Otilde;': u'\xd5', '&iuml;': u'\xef',
			 '&ugrave;': u'\xf9', '&sup3;': u'\xb3', '&curren;': u'\xa4', '&copy;': u'\xa9',
			 '&oacute;': u'\xf3', '&para;': u'\xb6', '&Euml;': u'\xcb', '&uacute;': u'\xfa',
			 '&ograve;': u'\xf2', '&acirc;': u'\xe2', '&aacute;': u'\xe1', '&Agrave;': u'\xc0',
			 '&Oacute;': u'\xd3', '&sect;': u'\xa7', '&yacute;': u'\xfd', '&iacute;': u'\xed',
			 '&cent;': u'\xa2', '&Ocirc;': u'\xd4', '&otilde;': u'\xf5'}
	def join(self, XmlList, lang):
		"""Joins a list of Xml files having <Secton id=""> elements and keys, and create the
		final Xml containing all the elements."""
		XmlFields = []
		i = 0
		while i != len(XmlList):
			xml = XmlList[i]
			index1 = string.find(xml, '<PageXML')
			index2 = string.find(xml, '>', index1+1)
			index3 = string.find(xml, '</PageXML')
			sectionXML = xml[index2+1:index3]
			XmlFields.append(sectionXML + '\015\012')
			i = i + 1
		xml = '<?xml version="1.0" encoding="' + self.ENCODING + '"?>' + '\015\012'
		xml = xml + '<PageXML xml:lang="' + lang + '">' + '\015\012'
		xml = xml + string.join(XmlFields, "\015\012")
		xml = xml + """</PageXML>""" + '\015\012'
		return xml
	def timeStamp(self, xmlPage):
		"""Insert timestamp as a KeySimple at end. -> xml."""
		timeZone = time.timezone
		timeZoneStr = str(timeZone)
		timeZoneSign = timeZoneStr[0]
		timeZoneHr = int(timeZoneStr[1:])/3600
		timeZoneMin = int((float(timeZoneStr[1:])/3600-timeZoneHr)*60)
		timeZoneNew = timeZoneSign + str(timeZoneHr).zfill(2) + ':' + str(timeZoneMin).zfill(2)
		timeStamp = time.strftime("%Y-%m-%dT%H:%M:%S" + str(timeZoneNew), time.localtime())
		oPageXML = PageXML()
		oPageXML.parse(xmlPage)
		try:
			xPath = 'PageXML/TimeStamp'
			oEnXMLKey = oPageXML.getKey(xPath)
			oEnXMLKey.setValue(str(timeStamp))
			oPageXML.updateKeySimple(xPath, oEnXMLKey)
		except PageXMLException:
                        xPath = 'PageXML'
                        oPageXML.addKeySimple(xPath, 'TimeStamp', str(timeStamp), {})
		xmlPage = oPageXML.toXml(1)
		return xmlPage
	def buildAttrStr(self, AttrDict, nodeType):
		i = 0
		List = AttrDict.keys()
		List.sort()
		ListAttr = []
		attrStr = ''
		while i != len(List):
			attrName = List[i]
			if attrName == 'name' and nodeType == 'Key':
				check = False
			elif attrName == 'id':
				check = False
			elif attrName == 'count' and nodeType == 'Collection':
				check = False
			elif attrName == 'count' and nodeType == 'CollectionComplex':
				check = False
			else:
				check = True
			if check:
				name = List[i]
				valueTmp = AttrDict[List[i]]
				cDataIndex = valueTmp.find('<![CDATA')
				if cDataIndex == -1:
					j = 0
					WordList = string.split(valueTmp)
					ValueList = []
					while j != len(WordList):
						word = WordList[j]
						if string.find(word, '&') != -1:
							if  not re.search('&\w+;',word) and not re.search('&#\w+;',word):
								word = string.replace(word, '&', '&amp;')
						ValueList.append(word)
						j = j + 1
					value = string.join(ValueList, ' ')
					if type(value) == types.UnicodeType:
						value = value.encode(self.ENCODING)
						name = name.encode(self.ENCODING)
					if string.find(value, '<') != -1:
						value = value.replace('<', '&lt;')
					if string.find(value, '>') != -1:
						value = value.replace('>', '&gt;')
					if string.find(value, '"') != -1:
						value = value.replace('"', '&quot;')
					if string.find(value, '"') != -1:
						value = value.replace("'", '&apos;')
					#value = string.replace(value, '&', '&amp;')					
					ListAttr.append(name + '="' + value + '"')
				else:
					ListAttr.append(name + '="' + valueTmp + '"')
			i = i + 1
		if len(ListAttr) != 0:
			attrStr = ' ' + string.join(ListAttr, ' ')
		else:
			attrStr = ''
		return attrStr
	def scapeAmp(self, text):
		"""Convert the html special characters, like &oacute; or &#126; to unicode
		chars using HtmlDict. Then, replace the "&" char to "&amp;"."""
		cDataIndex = text.find('<![CDATA')
		if cDataIndex == -1:
			WordList = string.split(text)
			w = 0
			WordListNew = []
			while w != len(WordList):
				word = WordList[w]
				if string.find(word, '&') != -1:
					if  not re.search('&\w+;',word) and not re.search('&#\w+;',word):
						word = string.replace(word, '&', '&amp;')
				if string.find(word, '<') != -1:
					word = word.replace('<', '&lt;')
				if string.find(word, '>') != -1:
					word = word.replace('>', '&gt;')
				if string.find(word, '"') != -1:
					word = word.replace('"', '&quot;')
				if string.find(word, '"') != -1:
					word = word.replace("'", '&apos;')				
				try:
					#wordUni = unicode(word, self.ENCODING)
					#wordUni = word.decode(self.ENCODING)
					WordListNew.append(word)
				except UnicodeDecodeError:
					wordUni = u''
				#WordListNew.append(word)
				w = w + 1
			textNew = string.join(WordListNew, ' ')
		else:
			textNew = text
		return textNew
	def validateXML(self, xmlPath, schemaPath):
		"""Validates an XML using an Schema. Returns True or False."""
		check = True
		# *********** FINISH AND LINK TO XSV
		if not check:
			raise SchemaException(100)
