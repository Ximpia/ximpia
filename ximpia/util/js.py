import base64
import types
import simplejson as json
from django.core import serializers as _s

class Form(object):

	@staticmethod
	def buildMsgArray(data=[]):
		"""Encode a message list into array for javascript."""
		dd = {}
		if len(data) != 0:
			insMessage, keyList = data
			for key in keyList:
				message = eval('insMessage.' + key)
				dd[key] = message
		dictStr = Form.encodeDict(dd)
		return dictStr

	@staticmethod
	def buildBlankArray(keyList):
		"""Build blank array for initial values"""
		dd = {}
		for key in keyList:
			dd[key] = ''
		dictStr = Form.encodeDict(dd)
		return dictStr
	
	@staticmethod
	def encodeDict(dd):
		"""Encode dictionary into json"""
		dictStr = json.dumps(dd)
		return dictStr
	
	@staticmethod
	def encode64Dict(dd):
		"""Encode dictionary into json and then to base64"""
		data = base64.encodestring(json.dumps(dd))
		return data
	
	@staticmethod
	def decode64dict(ddS):
		"""Decodes serialized json in base64 into a dictionary."""
		dd = json.loads(base64.decodestring(ddS))
		return dd
	
	@staticmethod
	def encodeObjDict(dd):
		"""Encode db instance dictionary into json"""
		dictNew = {}
		keyList = dd.keys()
		for key in keyList:
			# Get json object, parse, serialize fields object
			if type(dd[key]) == types.ListType:
				data = dd[key]
			else:
				data = [dd[key]]
			dictNew[key] = _s.serialize("json", data)
		return dictNew
	
	@staticmethod
	def encodeObj(dataInstance):
		"""Encode data instance"""
		if type(dataInstance) == types.ListType:
			data = dataInstance
		else:
			data = [dataInstance]
		encodedData = _s.serialize("json", data)
		return encodedData
	
	@staticmethod
	def decodeArray(array):
		"""Decode a javascript array into a python object, either list or dictionary"""
		obj = json.loads(array)
		return obj
	
	@staticmethod
	def addVarDict(jsArray, name, value):
		"""Add variable to dict"""
		dd = json.loads(jsArray)
		dd[name] = value
		jsArrayNew = json.dumps(dd)
		return jsArrayNew
