import re
import string
import simplejson as json

from django.http import HttpResponse
from django.core.mail import send_mail
from django.utils.translation import ugettext as _

from django.contrib.auth import login, authenticate, logout

from models import getResultOK, getResultERROR, XpMsgException
from ximpia.util import ut_email
from ximpia.util.js import Form as _jsf
from ximpia.core.models import JsResultDict, Context as Ctx

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
		#print 'Dumping...'
		sResult = json.dumps(resultDict)
		#print 'sResult : ', sResult
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
	
	def getErrorResultDict(self, errorDict, pageError=False):
		"""Get sorted error list to show in pop-up window
		@return: self._resultDict : ResultDict"""		
		#dict = self._errorDict
		keyList = errorDict.keys()
		keyList.sort()
		myList = []
		for key in keyList:
			message = errorDict[key]
			index = key.find('id_')
			if pageError == False:
				if index == -1:
					myList.append(('id_' + key, message, False))
				else:
					myList.append((key, message, False))
			else:
				if index == -1:
					myList.append(('id_' + key, message, True))
				else:
					myList.append((key, message, True))
		self._resultDict = getResultERROR(myList)
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
		#print 'form: ', self._f
		#return self._ctx['form']
		return self._f
	
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
		#print 'form: ', form
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
			exists = dbObj.check(**qArgs)
			print 'exists: ', exists
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
			exists = dbObj.check(**qArgs)
			print 'exists : ', exists
			if exists:
				self.addError(field=errName)
		
	def validateContext(self, ctxDataList):
		"""Validates context variable. [[name, value, errName],...]"""
		for ctxData in ctxDataList:
			name, value, errName = ctxData
			if self._ctx[name] != value:
				self.addError(errName)
		
	def authenticateUser(self, **dd):
		"""Authenticates user and password
		dd: {'userName': $userName, 'password': $password, 'errorName': $errorName}"""
		qArgs = {'username': dd['userName'], 'password': dd['password']}
		user = authenticate(**qArgs)
		if user:
			pass
		else:
			self.addError(dd['errorName'])
		return user
	
	def isValid(self):
		"""Checks if no errors have been written to error container.
		If not, raises XpMsgException """
		self._errorDict = self.getErrors()
		print 'errorDict : ', self._errorDict
		if not self.isBusinessOK():
			# Here throw the BusinessException
			raise XpMsgException(None, _('Error in validating business layer'))
	def setOkMsg(self, idOK):
		"""Sets the ok message id to shoe"""
		msgDict = _jsf.decodeArray(self._f.fields['okMessages'].initial)
		self._f.fields['msg_ok'].initial = msgDict[idOK]
	

class EmailBusiness(object):
	#python -m smtpd -n -c DebuggingServer localhost:1025
	@staticmethod
	def send(xmlMessage, subsDict, recipientList):
		"""Send email
		@param keyName: keyName for datastore
		@subsDict : Dictionary with substitution values for template
		@param recipientList: List of emails to send message"""
		subject, message = ut_email.getMessage(xmlMessage)
		message = string.Template(message).substitute(**subsDict)
		send_mail(subject, message, settings.WEBMASTER_EMAIL, recipientList)

class ShowSrvContent(object):
	"""Doc."""
	def __init__(self, *argsTuple, **argsDict):
		"""Doc."""
		self._form = argsTuple[0]
	def __call__(self, f):
		"""Doc."""
		def wrapped_f(*argsTuple, **argsDict):
			obj = argsTuple[0]
			obj._ctx[Ctx.FORM] = self._form()
			obj._f = self._form()
			try:
				f(*argsTuple, **argsDict)
				jsData = JsResultDict()
				obj._ctx[Ctx.FORM].buildJsData(jsData)
				obj._ctx[Ctx.CTX] = json.dumps(jsData)
			except XpMsgException as e:
				if settings.DEBUG == True:
					print e
					print e.myException
				errorDict = obj.getErrors()
				resultDict = obj.getErrorResultDict(errorDict, pageError=True)
				obj._ctx[Ctx.CTX] = json.dumps(resultDict)
			except Exception as e:
				raise
				if settings.DEBUG == True:
					print e
				errorDict = {'': _('I cannot process your request due to an unexpected error. Sorry for the inconvenience, please retry later. Thanks')}
				resultDict = obj.getErrorResultDict(errorDict, pageError=True)
				obj._ctx[Ctx.CTX] = json.dumps(resultDict)
		return wrapped_f

class ValidateFormBusiness(object):
	"""Checks that form is valid, builds result, builds errors"""
	_form = None
	_pageError = False
	def __init__(self, *argsTuple, **argsDict):
		# Sent by decorator
		self._form = argsTuple[0]
		if argsDict.has_key('pageError'):
			self._pageError = argsDict['pageError']
		else:
			self._pageError = False
	def __call__(self, f):
		"""Decorator call method"""
		def wrapped_f(*argsTuple, **argsDict):
			"""Doc."""
			object = argsTuple[0]
			object._ctx[Ctx.JS_DATA] = JsResultDict()
			object._f = self._form(object._ctx[Ctx.POST])
			bForm = object._f.is_valid()
			object._ctx[Ctx.FORM] = object._f
			if bForm == True:
				try:
					f(*argsTuple, **argsDict)
					object._f.buildJsData(object._ctx[Ctx.JS_DATA])
					result = object.buildJSONResult(object._ctx[Ctx.JS_DATA])
					#print result
					return result
				except XpMsgException as e:
					errorDict = object.getErrors()
					if settings.DEBUG == True:
						print errorDict
						print e
						print e.myException
					if len(errorDict) != 0:
						result = object.buildJSONResult(object.getErrorResultDict(errorDict, pageError=self._pageError))
					else:
						raise
					return result
				except Exception as e:
					if settings.DEBUG == True:
						print e
						print e.myException
			else:
				if settings.DEBUG == True:
					print 'Validation error!!!!!'
					#print object._f
					print object._f.errors
				errorDict = {'': 'Error validating your data. Check it out and send again'}
				result = object.buildJSONResult(object.getErrorResultDict(errorDict, pageError=True))
				return result
		return wrapped_f
