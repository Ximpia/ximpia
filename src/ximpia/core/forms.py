import re
import json
import types

from django.core import serializers as _s
from django import forms
from django.forms import ValidationError
from django.utils.translation import ugettext as _

from ximpia.util.js import Form as _jsf
from ximpia import settings

from form_fields import XpHiddenField

class XBaseForm(forms.Form):
	ERROR_INVALID = 'invalid'
	_request = None
	_ctx = None
	_db = {}
	#cleaned_data = None
	entryFields = XpHiddenField(xpType='input.hidden', required=False, initial=_jsf.buildBlankArray([]))
	copyEntryFields = XpHiddenField(xpType='input.hidden', required=False, initial=json.dumps(False))
	params = XpHiddenField(xpType='input.hidden', required=False, initial=_jsf.buildBlankArray([]))
	choices = XpHiddenField(xpType='input.hidden', required=False, initial=_jsf.buildBlankArray([]))
	pkFields = XpHiddenField(xpType='input.hidden', required=False, initial=_jsf.buildBlankArray([]))
	errorMessages = XpHiddenField(xpType='input.hidden', initial=_jsf.buildMsgArray([]))
	okMessages = XpHiddenField(xpType='input.hidden', initial=_jsf.buildMsgArray([]))
	ERR_GEN_VALIDATION = XpHiddenField(xpType='input.hidden', initial= _('Error validating your data. Check errors marked in red'))
	siteMedia = XpHiddenField(xpType='input.hidden', initial= settings.MEDIA_URL)
	buttonConstants = XpHiddenField(xpType='input.hidden', initial= "[['close','" + _('Close') + "']]")
	facebookAppId = XpHiddenField(xpType='input.hidden', initial= settings.FACEBOOK_APP_ID)
	objects = XpHiddenField(xpType='input.hidden', initial='')
	#errors = {}
	_argsDict = {}
	def __init__(self, *argsTuple, **argsDict): 
		"""Constructor for base form container"""
		self._argsDict = argsDict
		if argsDict.has_key('ctx'):
			self._ctx = argsDict['ctx']
		#self.errors = {}
		#self.errors['invalid'] = []
		print 'argsDict : ', argsDict
		if argsDict.has_key('instances'):
			dict = argsDict['instances']
			keys = dict.keys()
			# Set instances
			for key in keys:
				setattr(self, '_' + key, dict[key])
			fields = self.base_fields.keys()
			for sField in fields:
				field = self.base_fields[sField]
				try:
					instanceFieldName = field.instanceFieldName
					instanceName = field.instanceName
					if type(field.initial) == types.StringType and field.instance:
						field.initial = eval('self.' + instanceName + '.' + instanceFieldName)
						field.instance = eval('self.' + instanceName)
				except AttributeError:
					pass
			# Set instance too
		self._buildObjects()
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
			dict = {}
			for key in self._argsDict['instances']:
				# Get json object, parse, serialize fields object
				jsonObj = _s.serialize("json", [self._argsDict['instances'][key]])
				obj = json.loads(jsonObj)[0]
				dict[key] = obj['fields']
				self.base_fields['objects'].initial = json.dumps(dict)
	def putParam(self, name, value):
		"""Adds field to javascript array
		@param name: 
		@param value: """
		dict = json.loads(self.fields['params'].initial)
		dict[name] = value
		self.fields['params'].initial = json.dumps(dict)
	def getParam(self, name):
		"""Get param value.
		@param name: Param name
		@return: value"""
		dict = json.loads(self.fields['params'].initial)
		if dict.has_key(name):
			value = dict[name]
		else:
			raise ValueError
		return value
	def hasParam(self, name):
		"""Checks if has key name
		@param name: 
		@return: boolean"""
		dict = json.loads(self.fields['params'].initial)
		return dict.has_key(name)
	def _validateSameFields(self, tupleList):
		"""Validate same fields for list of tuples in form
		@param tupleList: Like ('password','passwordVerify')"""
		for tuple in tupleList:
			field1 = eval("self.fields['" + tuple[0] + "']")
			field2 = eval("self.fields['" + tuple[1] + "']")
			field1Value = self.data[tuple[0]]
			field2Value = self.data[tuple[1]]
			if field1Value != field2Value:
				if not self.errors.has_key('id_' + tuple[0]):
					self.errors['id_' + tuple[0]] = []
				if not self._errors.has_key('id_' + tuple[0]):
					self._errors['id_' + tuple[0]] = []
				self.errors['id_' + tuple[0]].append(field1.label + _(' must be the same as ') + field2.label)
				self._errors['id_' + tuple[0]].append(field1.label + _(' must be the same as ') + field2.label)

	def _validateSignupCaptcha(self):
		"""Validate Signup captcha"""
		if self._ctx.captcha != self.cleaned_data['captcha'] and not settings.PRIVATE_BETA:
			self.errors['captcha'].append(_('Captcha code is not correct'))
	def _validateCaptcha(self):
		"""Validate captcha"""
		if self._ctx.captcha != self.cleaned_data['captcha']:
			self.errors['captcha'].append(_('Captcha code is not correct'))
	def addInvalidError(self, sError):
		"""Adds error to errors lists."""
		self.errors[self.ERROR_INVALID].append(sError)	
	def setErrorDict(self, errors):
		"""Sets error dictionary"""
		self.errors = errors	
	def getErrorDict(self):
		"""Get error dictionary"""
		return self.errors
	def hasInvalidErrors(self):
		"""Has the form invalid errors?"""
		bError = False
		if len(self.errors.keys()) != 0:
			bError = True
		return bError
	def d(self, name):
		"""Get cleaned data, after form has been validated"""
		value = ''
		if self.cleaned_data.has_key(name):
			value = self.cleaned_data[name]
		return value	
	def _xpClean(self):
		"""Cleans form. Raises ValidationError in case errors found. Returns cleaned_data"""
		if self.hasInvalidErrors():
			raise ValidationError('Form Clean Validation Error')
		"""print 'self.cleaned_data : ', self.cleaned_data
		return self.cleaned_data"""
	def buildJsData(self, jsData):
		"""Get javascript json data for this form"""
		jsData['response']['form_' + self._XP_FORM_ID] = {}
		#print 'self.initial : ', self.initial
		fieldsDict = self.fields
		for field in fieldsDict:
			oField = fieldsDict[field]
			attrs = oField.widget.attrs
			try:
				attrs['type'] = oField.widget.input_type
			except AttributeError:
				pass
			attrs['element'] = oField.widget._element
			if attrs['element'] == 'select':
				attrs['choices'] = oField.choices
			attrs['name'] = field
			attrs['label'] = oField.label
			attrs['help_text'] = oField.help_text
			attrs['value'] = oField.initial
			"""if attrs.has_key('xpType'):
				xpType = attrs['xpType']
				if not jsData['response']['form_' + self._XP_FORM_ID].has_key(xpType):
					jsData['response']['form_' + self._XP_FORM_ID][xpType] = {}
				jsData['response']['form_' + self._XP_FORM_ID][xpType][field] = attrs
			else:
				jsData['response']['form_' + self._XP_FORM_ID][field] = attrs"""
			jsData['response']['form_' + self._XP_FORM_ID][field] = attrs

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
