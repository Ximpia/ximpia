import simplejson as json
from django.core import serializers as _s

class Form(object):

	@staticmethod
	def buildMsgArray(list=[]):
		"""Encode a message list into array for javascript."""
		dict = {}
		if len(list) != 0:
			insMessage, keyList = list
			for key in keyList:
				message = eval('insMessage.' + key)
				dict[key] = message
		dictStr = Form.encodeDict(dict)
		return dictStr

	@staticmethod
	def buildBlankArray(keyList):
		"""Build blank array for initial values"""
		dict = {}
		for key in keyList:
			dict[key] = ''
		dictStr = Form.encodeDict(dict)
		return dictStr
	
	@staticmethod
	def encodeDict(dict):
		"""Doc."""
		dictStr = json.dumps(dict)
		return dictStr
	
	@staticmethod
	def encodeObjDict(dict):
		"""Encode db instance dictionary into json"""
		dictNew = {}
		for key in dict:
			# Get json object, parse, serialize fields object
			dictNew[key] = _s.serialize("json", [dict[key]])
		return dictNew
	
	@staticmethod
	def decodeArray(array):
		"""Decode a javascript array into a python object, either list or dictionary"""
		obj = json.loads(array)
		return obj
	
	@staticmethod
	def addVarDict(jsArray, name, value):
		"""Add variable to dict"""
		dict = json.loads(jsArray)
		dict[name] = value
		jsArrayNew = json.dumps(dict)
		return jsArrayNew
