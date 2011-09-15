import string
import fpformat
import time
import types

"""Copyright (c) 2010 Tecor Communications S.L.
All rights reserved."""

class DictType:
	Dict = {}
	ListSep = ', '
	Sep = ': '
	Encoding = 'utf-8'
	def __init__(self, Dict):
		self.Dict = Dict
	def __str__(self):
		List = self.Dict.keys()
		ResultList = []
		i = 0
		while i != len(List):
			key = List[i]
			if type(key) == types.UnicodeType:
				name = key.encode(self.Encoding)
			else:
				name = key
			field = string.capitalize(name) + self.Sep + string.capitalize(self.Dict[key])
			ResultList.append(field)
			i = i + 1
		resultStr = string.join(ResultList, self.ListSep)
		return resultStr
	

class ListType(object):
	def buildIdList(self, list):
		"""Builds a list of int values from a list of string values.
		@param list: List of strings
		@return: listFinal: List of ints : [1,2,3,4] """
		listFinal = []
		for value in list:
			iValue = int(value)
			listFinal.append(iValue)
		return listFinal
	def mixLists(self, list1, list2):
		"""Mixes two lists into one, ordered and intersection of both.
		@param list1: List
		@param list2: List: 
		@return: listFinal intersection list1 and list2."""
		dict = {}
		for value in list1:
			dict[value] = ''
		for value in list2:
			dict[value] = ''
		listFinal = dict.keys()
		listFinal.sort()
		return listFinal

class GroupList:
	def __init__(self, mpg):
		self.Mpg = mpg
	def get(self, List):
		GroupList = []
		matches_per_group = self.Mpg
		m_p_g = matches_per_group
		groups = len(List)/m_p_g
		last = len(List) - groups * m_p_g
		if groups:
			i = 0
			while i != groups:
				j = 0
				InputList = []
				InputDict = {}
				while j != m_p_g:
					element = List[j+i*m_p_g]
					InputList.append(element)
					j = j + 1
				GroupList.append(InputList)
				i = i + 1
		if last:
			i = 0
			InputList = []
			InputDict = {}
			while i != last:
				element = List[i+groups*m_p_g]
				InputList.append(element)
				i = i + 1
			GroupList.append(InputList)
		return GroupList


class UnicodeType:
	TextUni = u''
	def __init__(self, textUni=None):
		if textUni:
			self.TextUni = textUni
	def getStr(self):
		textStr = self.TextUni.encode("utf-8")
		return textStr
	def getUnicode(self):
		return self.TextUni
	def setUnicode(self, textUni):
		self.TextUni = textUni
	def setText(self, textStr):
		self.TextUni = unicode(textStr,"utf-8")
		

class DictUtil:
		
	@staticmethod
	def addDicts(dictList):
		"""Add dictionaries"""
		i = 0
		dict = {}
		while i != len(dictList):
			dictTemp = dictList[i]
			listTemp = dictTemp.keys()
			j = 0
			while j != len(listTemp):
				key = listTemp[j]
				value = dictTemp[key]
				dict[key] = value
				j = j + 1
			i = i + 1
		return dict

class DbDate:

	DateDocDb = None
	
	def __init__(self, dateDocSub, dateDoc):
		try:
			if dateDoc != '':
				timeTuple = time.strptime(dateDoc,'%m/%d/%Y')
				if time.mktime(timeTuple) < time.time():
					DateDocList = string.split(dateDoc, '/')
					dateDocDb = DateDocList[2] + '/' + DateDocList[0] + '/' + DateDocList[1]
				else:
					dateDocDb = time.strftime('%Y/%m/%d')
			elif dateDocSub != '':
				timeTuple = time.strptime(dateDocSub,'%m/%d/%Y')
				if time.mktime(timeTuple) < time.time():
					DateDocList = string.split(dateDocSub, '/')
					dateDocDb = DateDocList[2] + '/' + DateDocList[0] + '/' + DateDocList[1]
				else:
					dateDocDb = time.strftime('%Y/%m/%d')
			else:
				dateDocDb = time.strftime('%Y/%m/%d')
		except:
			dateDocDb = time.strftime('%Y/%m/%d')
		self.DateDocDb = dateDocDb

class WebDate:

	WebDate = None
	
	def __init__(self, DbDate):
		TimeTuple = time.strptime(DbDate, '%Y-%m-%d')
		self.WebDate = time.strftime('%d-%b-%Y', TimeTuple)
		

class TimeStamp:
	def getTimeStamp(self):
		TimeTuple = time.localtime()
		timeStampStr = time.strftime('%Y-%m-%d %H:%M:%S', TimeTuple)
		return timeStampStr

class TimeTuple:
	
	TimeTuple = None
	
	def __init__(self, DbTimeDate):
		TimeTuple = time.strptime(DbTimeDate, '%Y-%m-%d %H:%M:%S')
		self.TimeTuple = TimeTuple
		

class NumberStr:
	ThousandSep = ','
	CommaSep = '.'
	def __init__(self, thousand_sep='', comma_sep=''):
		if thousand_sep != '':
			self.ThousandSep = thousand_sep
		if comma_sep != '':
			self.CommaSep = comma_sep
	def __numberFormat(self, number_int):
		numberStr = str(number_int)
		if len(numberStr)%3 != 0:
			numberGroups = len(numberStr)/3+1
		else:
			numberGroups = len(numberStr)/3
		i = 0
		ChunkList = []
		while i != numberGroups:
			if i == numberGroups-1:
				index1 = 0
			else:
				index1 = len(numberStr) - 3*i - 3
			if i == 0:
				index2 = len(numberStr)
			else:
				index2 = index
			index = index1
			chunk = numberStr[index1:index2]
			ChunkList.append(chunk)
			i = i + 1
		ChunkList.reverse()
		numberStr = string.join(ChunkList, self.ThousandSep)
		return numberStr
	def getNumber(self, number, number_dec):
		numberInt = int(number)
		numberIntStr = self.__numberFormat(numberInt)
		numberFloat = float(number)
		numberFloatStr = fpformat.fix(numberFloat, number_dec)
		if string.find(numberFloatStr, '.') != -1:
			decStr = string.split(numberFloatStr, '.')[1]
			numberStr = numberIntStr + self.CommaSep + decStr
		else:
			numberStr = numberIntStr
		return numberStr
	def roundNumber(self, number, numberDec):
		if number > 10000000 and number < 100000000:
			# 34.234.234 => 34.200.000
			number = int(round(float(number)/100000))
			numberStr = str(number) + '00000'
		elif number > 1000000 and number < 10000000:
			# 2.345.876 => 2.350.000
			number = int(round(float(number)/10000))
			numberStr = str(number) + '0000'
		elif number > 10000 and number < 1000000:
			# 23897 => 24000
			number = int(round(float(number)/1000))
			numberStr = str(number) + '000'
		elif number > 1000 and number < 10000:
			# 1576 => 1600
			number = int(round(float(number)/100))
			numberStr = str(number) + '00'
		elif number > 100 and number < 1000:
			# 456 => 460
			number = int(round(float(number)/10))
			numberStr = str(number) + '0'
		else:
			numberStr = str(number)
		numberStr = self.getNumber(int(numberStr),0)
		return numberStr
