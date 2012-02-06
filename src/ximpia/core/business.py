import re
import string
import simplejson as json

from django.http import HttpResponse
from django.core.mail import send_mail
from django.utils.translation import ugettext as _

from models import getResultOK, getResultERROR, XmlMessage, XpMsgException
from ximpia.util import ut_email
from ximpia.util.js import Form as _jsf

from ximpia import settings

class CommonBusiness(object):
	
	_ctx = None
	_request = None
	_errorDict = {}
	_resultDict = {}
	_form = None
	_postDict = {}
	_isBusinessOK = False
	_isFormOK = None
	
	def __init__(self, ctx):
		self._ctx = ctx
		self._resultDict = getResultERROR([])
		self._postDict = ctx['post']
		self._errorDict = {}
		self._resultDict = {}
		self._isFormOK = None
	
	def buildJSONResult(self, resultDict):
		"""Builds json result
		@param resultDict: dict : Dictionary with json data
		@return: result : HttpResponse"""
		print 'Dumping...'
		sResult = json.dumps(resultDict)
		print 'sResult : ', sResult
		result = HttpResponse(sResult)
		return result
	
	def _addError(self, idError, form, errorField):
		"""Add error
		@param idError: String : Id of error
		@param form: Form
		@param errorField: String : The field inside class form"""
		if not self._errorDict.has_key(idError):
			self._errorDict[idError] = {}
		self._errorDict[idError] = form.fields[errorField].initial
	
	def getErrorResultDict(self, errorDict):
		"""Get sorted error list to show in pop-up window
		@return: self._resultDict : ResultDict"""		
		#dict = self._errorDict
		keyList = errorDict.keys()
		keyList.sort()
		list = []
		for key in keyList:
			message = errorDict[key]
			index = key.find('id_')
			if index == -1:
				list.append(('id_' + key, message))
			else:
				list.append((key, message))
		self._resultDict = getResultERROR(list)
		return self._resultDict

	def _doValidations(self, validationDict):
		"""Do all validations defined in validation dictionary"""
		bFormOK = self._ctx['form'].is_valid()
		if bFormOK:
			keys = self.validationDict.keys()
			for key in keys:
				oVal = eval(key)(self._ctx)
				for sFunc in self.validationDict[key]:
					oVal.eval(sFunc)()
				self._doErrors(oVal.getErrors())
		"""if self.isBusinessOK() and bFormOK:
			result = f(*argsTuple, **argsDict)
			# check errors
			return wrapped_f
		else:
			# Errors
			result = self._buildJSONResult(self._getErrorResultDict())
			return result"""
	
	def getForm(self):
		"""Get form"""
		return self._ctx['form']
	
	def setForm(self, form):
		"""Sets the form"""
		self._ctx['form'] = form
	
	def getPostDict(self):
		"""Get post dictionary. This will hold data even if form is not validated. If not validated cleaned_value will have no values"""
		return self._postDict
	
	def isBusinessOK(self):
		"""Checks that no errors have been generated in the validation methods
		@return: isOK : boolean"""
		if len(self._errorDict.keys()) == 0:
			self._isBusinessOK = True
		return self._isBusinessOK
	
	def _isFormValid(self):
		"""Is form valid?"""
		if self._isFormOK == None:
			self._isFormOK = self._ctx['form'].is_valid()
		return self._isFormOK

	def _isFormBsOK(self):
		"""Is form valid and business validations passed?"""
		bDo = False
		if len(self._errorDict.keys()) == 0:
			self._isBusinessOK = True
		if self._isFormOK == True and self._isBusinessOK == True:
			bDo = True
		return bDo
	
	def addError(self, field):
		"""Add error
		@param idError: String : Id of error
		@param form: Form
		@param errorField: String : The field inside class form"""
		form = self.getForm()
		msgDict = _jsf.decodeArray(form.fields['errorMessages'].initial)		
		idError = 'id_' + field
		if not self._errorDict.has_key(idError):
			self._errorDict[idError] = {}
		self._errorDict[idError] = msgDict['ERR_' + field]
		print '_errorDict : ', self._errorDict
	def getErrors(self):
		"""Get error dict
		@return: errorDict : Dictionary"""
		return self._errorDict	
	def getPost(self):
		"""Get post dictionary"""
		return self._ctx['post']
	
	def validateExists(self, dbDataList):
		"""Validates that db data provided exists. Error is shown in case does not exist.
		Db data contains data instance, query arguments in a dictionary
		and errorName for error message display at the front
		@param dbDataList: [dbObj, queryArgs, errorName]"""
		print 'validateExists...'
		print 'dbDataList : ', dbDataList
		for dbData in dbDataList:
			dbObj, qArgs, errName = dbData
			exists = dbObj.check(qArgs)
			if not exists:
				self.addError(field=errName)
	
	def validateNotExists(self, dbDataList):
		"""Validates that db data provided does not exist. Error is shown in case exists.
		Db data contains data instance, query arguments in a dictionary
		and errorName for error message display at the front
		@param dbDataList: [dbObj, queryArgs, errorName]"""
		print 'validateNotExists...'
		print 'dbDataList : ', dbDataList
		for dbData in dbDataList:
			dbObj, qArgs, errName = dbData
			exists = dbObj.check(qArgs)
			print 'qArgs : ', exists
			if exists:
				self.addError(field=errName)
		
	def validateContext(self, ctxDataList):
		"""Validates context variable. [[name, value, errName],...]"""
		for ctxData in ctxDataList:
			name, value, errName = ctxData
			if self._ctx[name] != value:
				self.addError(errName)
	
	def isValid(self):
		"""Checks if no errors have been written to error container.
		If not, raises XpMsgException """
		self._errorDict = self.getErrors()
		print 'errorDict : ', self._errorDict
		if not self.isBusinessOK():
			# Here throw the BusinessException
			raise XpMsgException(None, _('Error in validating business layer'))
	

class EmailBusiness(object):
	#python -m smtpd -n -c DebuggingServer localhost:1025
	@staticmethod
	def send(keyName, subsDict, recipientList, lang):
		"""Send email
		@param keyName: keyName for datastore
		@subsDict : Dictionary with substitution values for template
		@param recipientList: List of emails to send message"""
		xmlMessage = XmlMessage.objects.get(name=keyName, lang=lang).body
		subject, message = ut_email.getMessage(xmlMessage)
		message = string.Template(message).substitute(**subsDict)
		send_mail(subject, message, settings.WEBMASTER_EMAIL, recipientList)

