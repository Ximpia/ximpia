import re
import json
import types
import os

from django.core import serializers as _s
from django import forms
from django.forms import ValidationError
from django.utils.translation import ugettext as _

from fields import HiddenField
import messages as _m
from ximpia.core.models import ContextDecorator as Ctx
from ximpia.util.js import Form as _jsf

# Settings
from ximpia.core.util import getClass
settings = getClass(os.getenv("DJANGO_SETTINGS_MODULE"))

import constants as K

from recaptcha.client import captcha

# Logging
import logging.config
logging.config.dictConfig(settings.LOGGING)
logger = logging.getLogger(__name__)

class XBaseForm( forms.Form ):
	ERROR_INVALID = 'invalid'
	_request = None
	_ctx = None
	_db = {}
	#cleaned_data = None
	entryFields = HiddenField(initial=_jsf.buildBlankArray([]))
	params = HiddenField(initial=_jsf.encodeDict({'viewMode': [K.UPDATE,K.DELETE]}))
	choices = HiddenField(initial=_jsf.buildBlankArray([]))
	pkFields = HiddenField(initial=_jsf.buildBlankArray([]))
	errorMessages = HiddenField(initial=_jsf.buildMsgArray([]))
	okMessages = HiddenField(initial=_jsf.buildMsgArray([]))
	ERR_GEN_VALIDATION = HiddenField(initial= _('Error validating your data. Check errors marked in red'))
	msg_ok = HiddenField(initial= _(' '))
	siteMedia = HiddenField(initial= settings.MEDIA_URL)
	buttonConstants = HiddenField(initial= "[['close','" + _('Close') + "']]")
	facebookAppId = HiddenField(initial= settings.FACEBOOK_APP_ID)
	action = HiddenField(initial='')
	app = HiddenField(initial='')
	viewNameSource = HiddenField(initial='')
	viewNameTarget = HiddenField(initial=' ')
	result = HiddenField(initial=' ')
	objects = HiddenField(initial='{}')
	#errors = {}
	_argsDict = {}
	def __init__(self, *argsTuple, **argsDict): 
		"""Constructor for base form container"""
		self._argsDict = argsDict
		self._errors = {}
		#logger.debug ( 'XBaseForm :: argsDict: ' + argsDict )
		if argsDict.has_key('ctx'):
			self._ctx = argsDict['ctx']
		#self.errors = {}
		#self.errors['invalid'] = []
		#logger.debug( 'argsDict : ' + argsDict )
		if argsDict.has_key('instances'):
			d = argsDict['instances']
			keys = d.keys()
			# Set instances
			for key in keys:
				setattr(self, '_' + key, d[key])
			fields = self.base_fields.keys()
			for sField in fields:
				field = self.base_fields[sField]
				try:
					instanceFieldName = field.instanceFieldName
					instanceName = field.instanceName
					if type(field.initial) == types.StringType and field.instance:
						field.initial = eval('self.' + instanceName + '.' + instanceFieldName)
						field.instance = eval('self.' + instanceName)
						#logger.debug( instanceFieldName + ' => ' + field.initial )
				except AttributeError:
					pass
			# Set instance too
		self._buildObjects()
		#self.app = argsDict['app'] if argsDict.has_key('app') else ''
		if argsDict.has_key('ctx'):
			del argsDict['ctx']
		if argsDict.has_key('dbDict'):
			del argsDict['dbDict']
		if argsDict.has_key('instances'):
			del argsDict['instances']
		self._db = {}
		super(XBaseForm, self).__init__(*argsTuple, **argsDict)
	def _buildObjects(self):
		"""Build db instance json objects"""
		if self._argsDict.has_key('instances'):
			d = {}
			for key in self._argsDict['instances']:
				# Get json object, parse, serialize fields object
				jsonObj = _s.serialize("json", [self._argsDict['instances'][key]])
				obj = json.loads(jsonObj)[0]
				#logger.debug( key + ' ' + obj )
				d[key] = obj['fields']
				self.base_fields['objects'].initial = json.dumps(d)
	def setViewMode(self, viewList):
		"""Set view mode from ['update,'delete','read']. As CRUD. Save button will be create and update."""
		paramDict = json.loads(self.fields['params'].initial)
		paramDict['viewMode'] = viewList
		self.fields['params'].initial = json.dumps(paramDict)
	def setViewModeRead(self):
		"""Read only mode"""
		paramDict = json.loads(self.fields['params'].initial)
		paramDict['viewMode'] = ['read']
		self.fields['params'].initial = json.dumps(paramDict)
	def putParam(self, name, value):
		"""Adds field to javascript array
		@param name: 
		@param value: """
		paramDict = json.loads(self.fields['params'].initial)
		paramDict[name] = value
		self.fields['params'].initial = json.dumps(paramDict)
	def putParamList(self, **argsDict):
		"""Put list of parameters. attribute set, like putParamList(myKey='', myOtherKey='')"""
		paramDict = json.loads(self.fields['params'].initial)
		for key in argsDict:
			paramDict[key] = argsDict[key]
		self.fields['params'].initial = json.dumps(paramDict)
	def getParam(self, name):
		"""Get param value.
		@param name: Param name
		@return: value"""
		paramDict = json.loads(self.d('params'))
		if paramDict.has_key(name):
			value = paramDict[name]
		else:
			raise ValueError
		return value
	def getParamDict(self, paramList):
		"""Get dictionary of parameters for the list of parameters given"""
		paramDict = json.loads(self.fields['params'].initial)
		d = {}
		for field in paramList: 
			d[field] = paramDict[field]
		return d
	def getParamList(self, paramList):
		"""Get list of values from list of names given.
		@param paramList: List of fields (names)
		@return: list of values"""
		paramDict = json.loads(self.fields['params'].initial)
		l = []
		for field in paramList:
			l.append(paramDict[field])
		return l
	def hasParam(self, name):
		"""Checks if has key name
		@param name: 
		@return: boolean"""
		d = json.loads(self.fields['params'].initial)
		return d.has_key(name)
	def _getFieldValue(self, fieldName):
		"""Get field value to be used in forms"""
		#field = eval("self.fields['" + fieldName + "']")
		value = self.data[fieldName]
		return value
	def _validateSameFields(self, tupleList):
		"""Validate same fields for list of tuples in form
		@param tupleList: Like ('password','passwordVerify')"""
		for myTuple in tupleList:
			field1 = eval("self.fields['" + myTuple[0] + "']")
			field2 = eval("self.fields['" + myTuple[1] + "']")
			field1Value = self.data[myTuple[0]]
			field2Value = self.data[myTuple[1]]
			if field1Value != field2Value:
				if not self.errors.has_key('id_' + myTuple[0]):
					self.errors['id_' + myTuple[0]] = []
				if not self._errors.has_key('id_' + myTuple[0]):
					self._errors['id_' + myTuple[0]] = []
				self.errors['id_' + myTuple[0]].append(field1.label + _(' must be the same as ') + field2.label)
				self._errors['id_' + myTuple[0]].append(field1.label + _(' must be the same as ') + field2.label)

	def _validateCaptcha(self):
		"""Validate captcha"""
		if self._ctx.request.has_key('recaptcha_challenge_field'):
			logger.debug( 'XBaseForm :: _validateCapctha() ...' )
			captchaResponse = captcha.submit(self._ctx.request['recaptcha_challenge_field'],
							self._ctx.request['recaptcha_response_field'], 
							settings.RECAPTCHA_PRIVATE_KEY, 
							self._ctx.meta['REMOTE_ADDR'])			
			if captchaResponse.is_valid == False:
				self.addInvalidError(_('Words introduced in Captcha do not correspond to image. You can reload for another image.'))
	def addInvalidError(self, sError):
		"""Adds error to errors lists."""
		if not self.errors.has_key(self.ERROR_INVALID):
			self.errors[self.ERROR_INVALID] = []
		if not self._errors.has_key(self.ERROR_INVALID):
			self._errors[self.ERROR_INVALID] = []
		self.errors[self.ERROR_INVALID].append(sError)	
		self._errors[self.ERROR_INVALID].append(sError)
	def serializeJSON(self):
		"""Serialize the form into json. The form must be validated first."""
		return json.dumps(self.cleaned_data)
	def setErrorDict(self, errors):
		"""Sets error dictionary"""
		self.errors = errors	
	def getErrorDict(self):
		"""Get error dictionary"""
		return self.errors
	def hasInvalidErrors(self):
		"""Has the form invalid errors?"""
		bError = False
		#logger.debug( 'XBaseForm :: hasIvalidErrors :: errors: ' + self.errors.keys() )
		if len(self.errors.keys()) != 0:
			bError = True
		return bError
	def __getitem__(self, name):
		"""Get item from object, like a dictionary. Can do form[fieldName]"""
		return self.d(name)
	def d(self, name):
		"""Get cleaned data, after form has been validated"""
		value = ''
		if self.cleaned_data.has_key(name):
			value = self.cleaned_data[name]
		return value
	def clean(self):
		"""Common clean data."""
		self._xpClean()
		return self.cleaned_data
	def _xpClean(self):
		"""Cleans form. Raises ValidationError in case errors found. Returns cleaned_data"""
		#logger.debug( 'XBaseForm :: hasInvalidErrors(): ' + self.hasInvalidErrors() )
		self._validateCaptcha()
		if self.hasInvalidErrors():
			raise ValidationError('Form Clean Validation Error')
		"""logger.debug( 'self.cleaned_data : ' + self.cleaned_data )
		return self.cleaned_data"""
	def getFormId(self):
		"""Get form id"""
		return self._XP_FORM_ID
	def setApp(self, app):
		"""Set application code to form."""
		self.base_fields['app'].initial = app
	def __buildForeignKey(self, jsData):
		"""
		Build foreign key choices
		
		** Attributes **
		
		* ``jsData`` : form data
		
		** Returns **
		
		None
		"""
		# append choices into id_choices		
		choicesStr = jsData['response']['form_' + self._XP_FORM_ID]['choices']['value']
		choices = _jsf.decodeArray(choicesStr)
		# Get fields from this form		
		for fieldName in self.fields:
			field = self.fields[fieldName]
			if str(type(field)) == "<class 'ximpia.core.fields.OneListField'>":
				#logger.debug('__buildForeignKey :: field: %s' % (fieldName) ) 
				choices[field.choicesId] = field.buildList()
		# Update new choices
		jsData['response']['form_' + self._XP_FORM_ID]['choices']['value'] = _jsf.encodeDict(choices)
	def __buildManyToMany(self, jsData):
		"""
		Build many to many choices
		
		** Attributes **
		
		* ``jsData`` : form data
		
		** Returns **
		
		None
		"""
		# append choices into id_choices		
		choicesStr = jsData['response']['form_' + self._XP_FORM_ID]['choices']['value']
		choices = _jsf.decodeArray(choicesStr)
		# Get fields from this form		
		for fieldName in self.fields:
			field = self.fields[fieldName]
			if str(type(field)) == "<class 'ximpia.core.fields.ManyListField'>":
				#logger.debug('__buildForeignKey :: field: %s' % (fieldName) ) 
				choices[field.choicesId] = field.buildList()
		# Update new choices
		jsData['response']['form_' + self._XP_FORM_ID]['choices']['value'] = _jsf.encodeDict(choices)
	def buildJsData(self, app, jsData):
		"""Get javascript json data for this form"""
		jsData['response']['form_' + self._XP_FORM_ID] = {}
		#logger.debug( 'self.initial : ' + self.initial )
		fieldsDict = self.fields
		#logger.debug( 'base_fields: ' + self.base_fields )
		for fieldName in fieldsDict:
			oField = fieldsDict[fieldName]
			attrs = oField.attrs
			fieldTypeFields = str(type(oField)).split('.')
			attrs['fieldType'] = fieldTypeFields[len(fieldTypeFields)-1].split("'")[0]
			"""try:
				attrs['type'] = oField.widget.input_type
			except AttributeError:
				pass"""
			#attrs['element'] = oField.widget._element
			try:
				attrs['choices'] = oField.choices
			except AttributeError:
				pass
			attrs['name'] = fieldName
			attrs['value'] = oField.initial or ''
			#logger.debug( 'field: %s' % (fieldName) )
			#logger.debug( attrs )
			jsData['response']['form_' + self._XP_FORM_ID][fieldName] = attrs
		# populate choices with foreign key fields: XpSelectField
		self.__buildForeignKey(jsData)
		self.__buildManyToMany(jsData)
		jsData['response']['form_' + self._XP_FORM_ID]['app']['value'] = app
	
	def disableFields(self, fields):
		"""
		Diable fields
		
		** Attributes **
		
		* ``fields``:List : fields to diable
		
		** Returns **
		
		None
		"""
		for field in fields:
			self.fields[field].widget.attrs['readonly'] = 'readonly'

class DefaultForm(XBaseForm):
	_XP_FORM_ID = 'default'
	errorMessages = HiddenField(initial=_jsf.buildMsgArray([_m, []]))
	okMessages = HiddenField(initial=_jsf.buildMsgArray([_m, []]))

class AppRegex(object):
	"""Doc.
	@deprecated: """
	# Any text
	string = re.compile('\w+', re.L)
	# text field, like 
	textField = re.compile("^(\w*)\s?(\s?\w+)*$", re.L)
	# Domain
	domain = re.compile("^([a-z0-9]([-a-z0-9]*[a-z0-9])?\\.)+((a[cdefgilmnoqrstuwxz]|aero|arpa)|(b[abdefghijmnorstvwyz]|biz)|(c[acdfghiklmnorsuvxyz]|cat|com|coop)|d[ejkmoz]|(e[ceghrstu]|edu)|f[ijkmor]|(g[abdefghilmnpqrstuwy]|gov)|h[kmnrtu]|(i[delmnoqrst]|info|int)|(j[emop]|jobs)|k[eghimnprwyz]|l[abcikrstuvy]|(m[acdghklmnopqrstuvwxyz]|mil|mobi|museum)|(n[acefgilopruz]|name|net)|(om|org)|(p[aefghklmnrstwy]|pro)|qa|r[eouw]|s[abcdeghijklmnortvyz]|(t[cdfghjklmnoprtvwz]|travel)|u[agkmsyz]|v[aceginu]|w[fs]|y[etu]|z[amw])$", re.L)
	# currency, like 23.23, 34.5
	currency = re.compile('^[0-9]*\.?|\,?[0-9]{0,2}$')
	# id, like 87262562
	id = re.compile('^[1-9]+[0-9]*$')
	# user id
	userId = re.compile('^[a-zA-Z0-9_.]+')
	# password
	password = re.compile('^\w+')
	# captcha
	captcha = re.compile('^\w{6}$')
	# Email
	email = re.compile('^([\w.])+\@([a-z0-9]([-a-z0-9]*[a-z0-9])?\\.)+((a[cdefgilmnoqrstuwxz]|aero|arpa)|(b[abdefghijmnorstvwyz]|biz)|(c[acdfghiklmnorsuvxyz]|cat|com|coop)|d[ejkmoz]|(e[ceghrstu]|edu)|f[ijkmor]|(g[abdefghilmnpqrstuwy]|gov)|h[kmnrtu]|(i[delmnoqrst]|info|int)|(j[emop]|jobs)|k[eghimnprwyz]|l[abcikrstuvy]|(m[acdghklmnopqrstuvwxyz]|mil|mobi|museum)|(n[acefgilopruz]|name|net)|(om|org)|(p[aefghklmnrstwy]|pro)|qa|r[eouw]|s[abcdeghijklmnortvyz]|(t[cdfghjklmnoprtvwz]|travel)|u[agkmsyz]|v[aceginu]|w[fs]|y[etu]|z[amw])')
