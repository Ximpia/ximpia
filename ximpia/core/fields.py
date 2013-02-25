# coding: utf-8

import json
import os
import datetime
import copy
from decimal import Decimal, DecimalException

from django.forms.widgets import Widget
from django.forms import Field as DjField
from django.forms.util import from_current_timezone, to_current_timezone
from django.core.exceptions import ValidationError
from django.utils import formats
from django.utils.encoding import smart_str, force_unicode, smart_unicode
from django.utils.ipv6 import clean_ipv6_address
from django.utils.translation import ugettext_lazy as _
import django.core.validators

from models import XpMsgException
from validators import validateTxtField, validatePassword, validateUserId

# Settings
from ximpia.core.util import getClass
settings = getClass(os.getenv("DJANGO_SETTINGS_MODULE"))

# Logging
import logging.config
logging.config.dictConfig(settings.LOGGING)
logger = logging.getLogger(__name__)

class Field( DjField ):
	instance = None
	initial = ''
	instanceName = ''
	instanceFieldName = ''
	attrs = {}
	creationCounter = 0
	defaultValidators = []
	defaultErrorMessages = {}
	localize = False
	def __init__(self, instance, insField, required=None, jsRequired=None, jsVal=None, label=None, initial=None, helpText=None, 
				errorMessages=None, validators=[]):
		"""
		Common field form class
		
		** Required Arguments **
		
		* ``instance``
		* ``insField``
		
		** Optional Arguments **
		
		* ``required``:bool [True] : Field is required by back-end
		* ``label``:str [None] : Field label
		* ``initial``:str [None] : Field initial value
		* ``helpText``:str [None] : Field tooltip
		* ``errorMessages``:dict [None] : Error messages in dict format
		* ``validators``:list [[]] : List of validators		
		
		"""
		self.attrs = {}
		self._doInstanceInit(instance, insField)
		self.required, self.jsRequired = self._doRequired(required, jsRequired)
		classStr = 'fieldMust' if self.required == True else 'field'
		if self.required == False and self.jsRequired == True:
			classStr = 'fieldMust'
		# attrs
		self.attrs['class'] = classStr
		if label is not None:
			label = smart_unicode(label)
		self.label, self.initial = label, initial
		initValue = initial if initial != None else ''
		# helpText		
		if helpText is None:
			self.helpText = u''
		else:
			self.helpText = smart_unicode(helpText)
		# Perform instance operations for basic fields, FK, and many to many relationships
		self._doInstance(initial, initValue)
		if self.instance:
			if not label:
				self.label = smart_unicode(self.instance._meta.get_field_by_name(self.instanceFieldName)[0].verbose_name.title())
			if not helpText:
				self.helpText = smart_unicode(self.instance._meta.get_field_by_name(self.instanceFieldName)[0].help_text.title())
		# jsRequired
		#self.jsRequired = jsRequired
		if self.required == True and not self.jsRequired:
			self.jsRequired= True
		if self.required == False and not self.jsRequired:
			self.jsRequired = False
		if self.jsRequired:
			if self.jsRequired == True:
				self._updateAttrs(self.attrs, 'data-xp-val', 'required')
		# jsval
		self.jsVal = jsVal or []
		if len(self.jsVal) != 0:
			for item in jsVal:
				self._updateAttrs(self.attrs, 'data-xp-val', item)
		#logger.debug( 'attrs for %s: %s' % (self.label, str(self.attrs)) )
		# Increase the creation counter, and save our local copy.
		self.creationCounter = Field.creationCounter
		Field.creationCounter += 1
		messages = {}
		for c in reversed(self.__class__.__mro__):
			messages.update(getattr(c, 'defaultErrorMessages', {}))
		messages.update(errorMessages or {})
		self.error_messages = messages
		self.validators = self.defaultValidators + validators
		# maxLength from model
		self.maxLength = self.instance._meta.get_field_by_name(self.instanceFieldName)[0].max_length if self.instance else None
		self.localize = False
		self.attrs['label'] = label or self.label
		self.attrs['helpText'] = self.helpText
		self.attrs['required'] = self.required 
		self.attrs['jsRequired'] = self.jsRequired
		super(Field, self).__init__(required=required, widget=None, label=label, initial=initial,
                 help_text=helpText, error_messages=None, show_hidden_initial=False, validators=[], localize=False)
		
	def _doInstanceInit(self, instance, insField):
		"""
		Set instance and instanceName and instanceFieldName
		"""
		if insField != '' or insField is not None:
			self.instanceFieldName = insField
			self.instance = instance
	def _getModelField(self):
		"""
		Get field from model instance
		"""
		modelField = eval("self.instance.__class__._meta.get_field_by_name('" + self.instanceFieldName + "')[0]")
		return modelField
	def _getModelFieldType(self):
		"""
		Get field model type
		"""
		modelField = self._getModelField()
		fieldTypeFields = str(type(modelField)).split('.')
		return fieldTypeFields[len(fieldTypeFields)-1].split("'")[0]
	def _getLimitChoicesTo(self, instance, instanceFieldName):
		"""
		Get limit_choices_to from model for field name. Searches for through table.
		
		** Attributes **
		
		* ``instance``
		* ``instanceFieldName``
		
		** Returns**
		
		limitChoices:dict
		"""
		limitChoicesTo = {}
		rel = instance.__class__._meta.get_field_by_name(instanceFieldName)[0].rel
		if rel:
			try:
				through = rel.through
			except AttributeError:
				through = None
			if through:
				# Many through another table
				mainTo = rel.to
				# Resolve fieldName for link from through table to main table
				fieldList = through._meta.fields
				fieldName = ''
				for field in fieldList:
					if field.rel:
						relTo = field.rel.to
						if relTo and relTo == mainTo:
							# This is the field
							fieldName = field.name
				if fieldName != '':
					limitChoicesTo = through._meta.get_field_by_name(fieldName)[0].rel.limit_choices_to
			else:
				# No through table
				limitChoicesTo = rel.limit_choices_to
		return limitChoicesTo
	def _doInstance(self, initial, initValue):
		"""
		Perform instance logic with basic fields, foreign key fields and many to many fields
		"""
		if self.instance:
			if self._isForeignKey() == True:
				# ForeignKey
				try:
					self.initial = eval('str(self.instance' + '.' + self.instanceFieldName + '.pk)')\
							 if self.instance != None and not initial else initValue
				except:
					self.initial = initValue
			elif self._isManyToMany() == True:
				# ManyToMany
				try:
					initialList = []
					values1 = eval('self.instance' + '.' + self.instanceFieldName + '.all()')
					if len(values1) != 0:
						values = values1.values('pk')
						for value in values:
							initialList.append(str(value['pk']))
						self.initial = '[' + ','.join(initialList) + ']' if self.instance != None and not initial else initValue
					else:
						self.initial = '[]' if self.instance != None and not initial else initValue
				except:
					self.initial = initValue
			else:
				# Any field...
				self.initial = eval('self.instance' + '.' + self.instanceFieldName)\
						 if self.instance != None and initial == None else initValue
	def _updateAttrs(self, d, key, value):
		"""Update attrs dictionary"""
		if d.has_key(key):
			d[key] += ' ' + value
		else:
			d[key] = value
	def _doRequired(self, required, jsRequired):
		"""Process required and javascript required"""
		# True | None => True		
		# False | None => False
		if required == None and self.instance != None:
			required = not self.instance.__class__._meta.get_field_by_name(self.instanceFieldName)[0].null
			logger.debug('Field._doRequired :: field: %s model field null: %s required: %s' % 
						(self.instanceFieldName, self.instance.__class__._meta.get_field_by_name(self.instanceFieldName)[0].null, required) )
		if jsRequired == None:
			jsRequired = required
		t = (required, jsRequired)
		return t
	def _getFieldName(self, insField):
		"""
		get model field name from instance field like '_dbAddress.country'
		
		** Attributes **
		
		* ``insfield``:str
		
		** Returns **
		
		Will return the field name, 'country' in the above example."""
		return insField.split('.')[1]
	def _isForeignKey(self):
		"""
		Checks if field is related to a model ForeignKey
		
		** Returns**
		
		``isFK``:bool
		"""
		isFK = False
		if eval('self.instance.__class__.__dict__.has_key(\'' + self.instanceFieldName + '\')') and\
				 str(type(eval('self.instance.__class__.' + self.instanceFieldName))) == "<class 'django.db.models.fields.related.ReverseSingleRelatedObjectDescriptor'>":
			isFK = True
		return isFK
	def _isManyToMany(self):
		"""
		Checks if form field is related to a ManyToMany relationship
		
		** Returns **
		
		``isManyToMany``:bool		
		"""
		isManyToMany = False
		if eval('self.instance.__class__.__dict__.has_key(\'' + self.instanceFieldName + '\')') and\
				 str(type(eval('self.instance.__class__.' + self.instanceFieldName))) == "<class 'django.db.models.fields.related.ReverseManyRelatedObjectsDescriptor'>":
			isManyToMany = True
		return isManyToMany
	
	def prepare_value(self, value):
		return value

	def to_python(self, value):
		return value

	def validate(self, value):
		if value in django.core.validators.EMPTY_VALUES and self.required:
			raise ValidationError(self.error_messages['required'])

	def run_validators(self, value):
		if value in django.core.validators.EMPTY_VALUES:
			return
		errors = []
		for v in self.validators:
			try:
				v(value)
			except ValidationError, e:
				if hasattr(e, 'code') and e.code in self.error_messages:
					message = self.error_messages[e.code]
					if e.params:
						message = message % e.params
					errors.append(message)
				else:
					errors.extend(e.messages)
		if errors:
			raise ValidationError(errors)

	def clean(self, value):
		"""
		Validates the given value and returns its "cleaned" value as an
		appropriate Python object.

		Raises ValidationError for any errors.
		"""
		value = self.to_python(value)
		self.validate(value)
		self.run_validators(value)
		return value

	def bound_data(self, data, initial):
		"""
		Return the value that should be shown for this field on render of a
		bound form, given the submitted POST data for the field and the initial
		data, if any.

		For most fields, this will simply be data; FileFields need to handle it
		a bit differently.
		"""
		return data

	def __deepcopy__(self, memo):
		result = copy.copy(self)
		memo[id(self)] = result
		#result.widget = copy.deepcopy(self.widget, memo)
		result.validators = self.validators[:]
		return result

class CharField( Field ):
	"""
	Char field.
	
	Example:
	
	firstName = CharField(_dbUser, '_dbUser.first_name')
	
	where _dbUser is a form class attribute with the model instance, ``_dbUser = User()``
	
	** Required Arguments **
	
	* ``instance``:object : Model instance
	* ``insField``:str : Model field
	
	** Optional Arguments **
	
	* ``minLength``:int : Field minimum length
	* ``maxLength``:int : Field maximum length
	* ``required``:bool : Required field by back-end form valdiation
	* ``initial``:str : Initial value
	* ``jsRequired``:str	: Required field by javascript validation
	* ``label``:str : Field label
	* ``helpText``:str : Field tooptip
	
	** Attributes **
	
	* ``instance``:object
	* ``instanceFieldName``:str
	* ``minLength``:str
	* ``maxLength``:str
	* ``required``:bool
	* ``initial``:str
	* ``jsRequired``:bool
	* ``label``:str
	* ``helpText``:str
	
	"""
	maxLength = None
	minLength = None
	def __init__(self, instance, insField, minLength=None, maxLength=None, required=None, initial='', jsRequired=None, 
				label=None, helpText=None, jsVal=None):
		super(CharField, self).__init__(instance, insField, required=required, jsRequired=jsRequired, label=label, 
									initial=initial, helpText=helpText, jsVal=jsVal)
		if maxLength != None:
			self.maxLength = maxLength
		if minLength != None:
			self.minLength = minLength
		if len(self.defaultValidators) == 0:
			self.defaultValidators = [validateTxtField]
		if self.minLength is not None:
			self.validators.append(django.core.validators.MinLengthValidator(self.minLength))
		if self.maxLength is not None:
			self.validators.append(django.core.validators.MaxLengthValidator(self.maxLength))
		if self.maxLength != None:
			self.attrs['maxlength'] = str(self.maxLength)
		if self.minLength != None:
			self.attrs['minlength'] = str(self.minLength)

class BooleanField ( Field ):	
	"""
	Boolean field. This field can be rendered into any visual component: checkbox, selection box, etc... The most common use is to
	render into a checkbox.
	
	Example:
	
	isOrdered = BooleanField(_dbUserOrder, '_dbUserOrder.isOrdered')
	
	where _dbUserOrder is a form class attribute with the model instance, ``_dbUserOrder = UserOrder()``
	
	** Required Arguments **

	* ``instance``:object : Model instance
	* ``insField``:str : Model field
	
	** Optional Arguments **
	
	* ``required``:bool : Required field by back-end form valdiation
	* ``initial``:str : Initial value
	* ``jsRequired``:str	: Required field by javascript validation
	* ``label``:str : Field label
	* ``helpText``:str : Field tooptip
	
	** Attributes **
	
	* ``instance``:object
	* ``instanceFieldName``:str
	* ``required``:bool
	* ``initial``:str
	* ``jsRequired``:bool
	* ``label``:str
	* ``helpText``:str
	
	"""

	def to_python(self, value):
		"""Returns a Python boolean object."""
		# Explicitly check for the string 'False', which is what a hidden field
		# will submit for False. Also check for '0', since this is what
		# RadioSelect will provide. Because bool("True") == bool('1') == True,
		# we don't need to handle that explicitly.
		if isinstance(value, basestring) and value.lower() in ('false', '0'):
			value = False
		else:
			value = bool(value)
		value = super(BooleanField, self).to_python(value)
		if not value and self.required:
			raise ValidationError(self.error_messages['required'])
		return value

class IPAddressField(Field):
	"""
	Ip Address field, IPv4, like 255.255.255.0
	
	Example:
	
	isOrdered = IPAddressField(_dbModel, '_dbModel.ip')
	
	where _dbModel is a form class attribute with the model instance.
	
	** Required Arguments **

	* ``instance``:object : Model instance
	* ``insField``:str : Model field
	
	** Optional Arguments **
	
	* ``required``:bool : Required field by back-end form valdiation
	* ``initial``:str : Initial value
	* ``jsRequired``:str	: Required field by javascript validation
	* ``label``:str : Field label
	* ``helpText``:str : Field tooptip
	
	** Attributes **
	
	* ``instance``:object
	* ``instanceFieldName``:str
	* ``required``:bool
	* ``initial``:str
	* ``jsRequired``:bool
	* ``label``:str
	* ``helpText``:str
	
	"""
	
	defaultErrorMessages = {
		'invalid': _(u'Enter a valid IPv4 address.'),
	}
	defaultValidators = [django.core.validators.validate_ipv4_address]


class GenericIPAddressField(CharField):
	
	"""
	Generic IP Address field, IPv4 and IPv6
	
	Example:
	
	isOrdered = IPGenericAddressField(_dbModel, '_dbModel.ip')
	
	where _dbModel is a form class attribute with the model instance.
	
	** Required Arguments **

	* ``instance``:object : Model instance
	* ``insField``:str : Model field
	
	** Optional Arguments **
	
	* ``protocol``:str ['both'] : Protocol, possible values: both|ipv4|ipv6
	* ``unpackIpv4``:bool [False]
	* ``required``:bool : Required field by back-end form valdiation
	* ``initial``:str : Initial value
	* ``jsRequired``:str	: Required field by javascript validation
	* ``label``:str : Field label
	* ``helpText``:str : Field tooptip
	
	** Attributes **
	
	* ``instance``:object
	* ``instanceFieldName``:str
	* ``required``:bool
	* ``initial``:str
	* ``jsRequired``:bool
	* ``label``:str
	* ``helpText``:str
	
	"""
	
	defaultErrorMessages = {}

	def __init__(self, instance, insField, minLength=None, maxLength=None, required=True, initial='', jsRequired=None, 
				label=None, helpText=None, protocol='both', unpackIpv4=False, jsVal=None):
		self.unpack_ipv4 = unpackIpv4
		self.defaultValidators, invalidErrorMessage = django.core.validators.ip_address_validators(protocol, unpackIpv4)
		self.defaultErrorMessages['invalid'] = invalidErrorMessage
		self.required, self.jsRequired = self._doRequired(required, jsRequired)
		super(GenericIPAddressField, self).__init__(instance, insField, required=required, jsRequired=jsRequired, label=label, 
									initial=initial, helpText=helpText, jsVal=jsVal)
		classStr = 'fieldMust' if required == True else 'field'
		if required == False and jsRequired == True:
			classStr = 'fieldMust'
		# attrs
		self.attrs['class'] = classStr

	def to_python(self, value):
		if value in django.core.validators.EMPTY_VALUES:
			return u''
		if value and ':' in value:
				return clean_ipv6_address(value,
					self.unpack_ipv4, self.error_messages['invalid'])
		return value

class DecimalField ( Field ):
	
	"""
	Decimal field with support for maxValue, minValue, maxDigits and decimalPlaces
	
	Example:
	
	amount = DecimalField(_dbModel, '_dbModel.field', maxValue=9800, minValue=100, maxDigits=4, decimalPlaces=2)
	
	where _dbModel is a form class attribute with the model instance.
	
	** Required Arguments **

	* ``instance``:object : Model instance
	* ``insField``:str : Model field
	
	** Optional Arguments **
	
	* ``maxValue``:decimal.Decimal : Maximum value
	* ``minValue``:decimal.Decimal : Minimum value
	* ``maxDigits``:int : Maximum number of digits (before decimal point plus after decimal point)
	* ``decimalPlaces``:int : Number of decimal places
	* ``required``:bool : Required field by back-end form valdiation
	* ``initial``:str : Initial value
	* ``jsRequired``:str	: Required field by javascript validation
	* ``label``:str : Field label
	* ``helpText``:str : Field tooptip
	
	** Attributes **
	
	* ``instance``:object
	* ``instanceFieldName``:str
	* ``required``:bool
	* ``initial``:str
	* ``jsRequired``:bool
	* ``label``:str
	* ``helpText``:str
	
	"""
	
	defaultErrorMessages = {
		'invalid': _(u'Enter a number.'),
		'max_value': _(u'Ensure this value is less than or equal to %(limit_value)s.'),
		'min_value': _(u'Ensure this value is greater than or equal to %(limit_value)s.'),
		'max_digits': _('Ensure that there are no more than %s digits in total.'),
		'max_decimal_places': _('Ensure that there are no more than %s decimal places.'),
		'max_whole_digits': _('Ensure that there are no more than %s digits before the decimal point.')
	}

	def __init__(self, instance, insField, required=True, initial='', jsRequired=None, label=None, helpText=None, 
				maxValue=None, minValue=None, maxDigits=None, decimalPlaces=None, jsVal=None):
		self.maxValue, self.minValue = maxValue, minValue
		self.maxDigits, self.decimalPlaces = maxDigits, decimalPlaces
		#Field.__init__(self, *args, **kwargs)
		super(DecimalField, self).__init__(instance, insField, required=required, jsRequired=jsRequired, label=label, 
									initial=initial, helpText=helpText, jsVal=jsVal)
		if maxValue is not None:
			self.validators.append(django.core.validators.MaxValueValidator(maxValue))
		if minValue is not None:
			self.validators.append(django.core.validators.MinValueValidator(minValue))
		if maxValue is not None:
			self.attrs['maxValue'] = maxValue
			self.maxValue = maxValue
		if minValue is not None:
			self.attrs['minValue'] = minValue
			self.minValue = minValue
		if maxDigits is not None:
			self.attrs['maxDigits'] = maxDigits
			self.maxDigits = maxDigits
		if decimalPlaces is not None:
			self.attrs['decimalPlaces'] = decimalPlaces
			self.decimalPlaces = decimalPlaces
		
		# Get max digits and decimal places from model field in case no values defined in the form field
		modelFieldType = self._getModelFieldType()
		modelField = self._getModelField()
		if modelFieldType == 'DecimalField' and maxDigits is None and decimalPlaces is None:
			self.attrs['maxDigits'] = modelField.max_digits
			self.attrs['decimalPlaces'] = modelField.decimal_places
			self.decimalPlaces = modelField.decimal_places
			self.maxDigits = modelField.max_digits
		
		# For fields PossitiveIntegerField and PossitiveSmallIntegerField if no minValue defined, set minValue to 0
		if (modelFieldType == 'PositiveIntegerField' or modelFieldType == 'PositiveSmallIntegerField') and minValue is None:
			self.attrs['minValue'] = 0
			self.minValue = 0
			self.validators.append(django.core.validators.MinValueValidator(0))

	def to_python(self, value):
		"""
		Validates that the input is a decimal number. Returns a Decimal
		instance. Returns None for empty values. Ensures that there are no more
		than max_digits in the number, and no more than decimal_places digits
		after the decimal point.
		"""
		if value in django.core.validators.EMPTY_VALUES:
			return None
		if self.localize:
			value = formats.sanitize_separators(value)
		value = smart_str(value).strip()
		try:
			value = Decimal(value)
		except DecimalException:
			raise ValidationError(self.error_messages['invalid'])
		return value

	def validate(self, value):
		super(DecimalField, self).validate(value)
		if value in django.core.validators.EMPTY_VALUES:
			return
		# Check for NaN, Inf and -Inf values. We can't compare directly for NaN,
		# since it is never equal to itself. However, NaN is the only value that
		# isn't equal to itself, so we can use this to identify NaN
		if value != value or value == Decimal("Inf") or value == Decimal("-Inf"):
			raise ValidationError(self.error_messages['invalid'])
		sign, digittuple, exponent = value.as_tuple()	#@UnusedVariable
		decimals = abs(exponent)
		# digittuple doesn't include any leading zeros.
		digits = len(digittuple)
		if decimals > digits:
			# We have leading zeros up to or past the decimal point.  Count
			# everything past the decimal point as a digit.  We do not count
			# 0 before the decimal point as a digit since that would mean
			# we would not allow max_digits = decimal_places.
			digits = decimals
		wholeDigits = digits - decimals

		if self.maxDigits is not None and digits > self.maxDigits:
			raise ValidationError(self.error_messages['max_digits'] % self.maxDigits)
		if self.decimalPlaces is not None and decimals > self.decimalPlaces:
			raise ValidationError(self.error_messages['max_decimal_places'] % self.decimalPlaces)
		if self.maxDigits is not None and self.decimalPlaces is not None and wholeDigits > (self.maxDigits - self.decimalPlaces):
			raise ValidationError(self.error_messages['max_whole_digits'] % (self.maxDigits - self.decimalPlaces))
		return value

class IntegerField ( Field ):
	
	"""
	Integer field with maxValue and minValue
	
	Example:
	
	number = IntegerField(_dbModel, '_dbModel.field', maxValue=9800, minValue=100)
	
	where _dbModel is a form class attribute with the model instance.
	
	** Required Arguments **

	* ``instance``:object : Model instance
	* ``insField``:str : Model field
	
	** Optional Arguments **
	
	* ``maxValue``:decimal.Decimal : Maximum value
	* ``minValue``:decimal.Decimal : Minimum value
	* ``required``:bool : Required field by back-end form valdiation
	* ``initial``:str : Initial value
	* ``jsRequired``:str	: Required field by javascript validation
	* ``label``:str : Field label
	* ``helpText``:str : Field tooptip
	
	** Attributes **
	
	* ``instance``:object
	* ``instanceFieldName``:str
	* ``required``:bool
	* ``initial``:str
	* ``jsRequired``:bool
	* ``label``:str
	* ``helpText``:str
	
	"""
	
	defaultErrorMessages = {
		'invalid': _(u'Enter a whole number.'),
		'max_value': _(u'Ensure this value is less than or equal to %(limit_value)s.'),
		'min_value': _(u'Ensure this value is greater than or equal to %(limit_value)s.'),
	}

	def __init__(self, instance, insField, required=True, initial='', jsRequired=None, label=None, helpText=None, 
				maxValue=None, minValue=None, jsVal=None):
		self.maxValue, self.minValue = maxValue, minValue
		super(IntegerField, self).__init__(instance, insField, required=required, jsRequired=jsRequired, label=label, 
									initial=initial, helpText=helpText, jsVal=jsVal)
		if maxValue is not None:
			self.validators.append(django.core.validators.MaxValueValidator(maxValue))
		if minValue is not None:
			self.validators.append(django.core.validators.MinValueValidator(minValue))
		if maxValue is not None:
			self.attrs['maxValue'] = maxValue
		if minValue is not None:
			self.attrs['minValue'] = minValue
		
		# For fields PossitiveIntegerField and PossitiveSmallIntegerField if no minValue defined, set minValue to 0
		modelFieldType = self._getModelFieldType()
		if (modelFieldType == 'PositiveIntegerField' or modelFieldType == 'PositiveSmallIntegerField') and minValue is None:
			self.attrs['minValue'] = 0
			self.minValue = 0
			self.validators.append(django.core.validators.MinValueValidator(0))

	def to_python(self, value):
		"""
		Validates that int() can be called on the input. Returns the result
		of int(). Returns None for empty values.
		"""
		value = super(IntegerField, self).to_python(value)
		if value in django.core.validators.EMPTY_VALUES:
			return None
		if self.localize:
			value = formats.sanitize_separators(value)
		try:
			value = int(str(value))
		except (ValueError, TypeError):
			raise ValidationError(self.error_messages['invalid'])
		return value

class FloatField ( IntegerField ):
	
	"""
	Integer field with maxValue and minValue
	
	Example:
	
	number = FloatField(_dbModel, '_dbModel.field', maxValue=9800, minValue=100)
	
	where _dbModel is a form class attribute with the model instance.
	
	** Required Arguments **

	* ``instance``:object : Model instance
	* ``insField``:str : Model field
	
	** Optional Arguments **
	
	* ``maxValue``:decimal.Decimal : Maximum value
	* ``minValue``:decimal.Decimal : Minimum value
	* ``required``:bool : Required field by back-end form valdiation
	* ``initial``:str : Initial value
	* ``jsRequired``:str	: Required field by javascript validation
	* ``label``:str : Field label
	* ``helpText``:str : Field tooptip
	
	** Attributes **
	
	* ``instance``:object
	* ``instanceFieldName``:str
	* ``required``:bool
	* ``initial``:str
	* ``jsRequired``:bool
	* ``label``:str
	* ``helpText``:str
	
	"""
	
	defaultErrorMessages = {
		'invalid': _(u'Enter a number.'),
	}

	def to_python(self, value):
		"""
		Validates that float() can be called on the input. Returns the result
		of float(). Returns None for empty values.
		"""
		value = super(IntegerField, self).to_python(value)
		if value in django.core.validators.EMPTY_VALUES:
			return None
		if self.localize:
			value = formats.sanitize_separators(value)
		try:
			value = float(value)
		except (ValueError, TypeError):
			raise ValidationError(self.error_messages['invalid'])
		return value

class _BaseTemporalField ( Field ):
	
	"""
	
	
	Example:	
	
	
	where _dbModel is a form class attribute with the model instance.
	
	** Input Formats **
	
	A list of formats used to attempt to convert a string to a valid datetime.date object.
	
	** Required Arguments **

	* ``instance``:object : Model instance
	* ``insField``:str : Model field
	
	** Optional Arguments **
	
	* ``inputFormats``:list : Input formats
	* ``required``:bool : Required field by back-end form valdiation
	* ``initial``:str : Initial value
	* ``jsRequired``:str	: Required field by javascript validation
	* ``label``:str : Field label
	* ``helpText``:str : Field tooptip
	
	** Attributes **
	
	* ``instance``:object
	* ``instanceFieldName``:str
	* ``required``:bool
	* ``initial``:str
	* ``jsRequired``:bool
	* ``label``:str
	* ``helpText``:str
	
	"""

	def __init__(self, instance, insField, required=True, initial='', jsRequired=None, label=None, helpText=None, inputFormats=None,
				jsVal=None):
		super(_BaseTemporalField, self).__init__(instance, insField, required=required, jsRequired=jsRequired, label=label, 
									initial=initial, helpText=helpText, jsVal=jsVal)
		if inputFormats is not None:
			self.inputFormats = inputFormats

	def to_python(self, value):
		# Try to coerce the value to unicode.
		unicode_value = force_unicode(value, strings_only=True)
		if isinstance(unicode_value, unicode):
			value = unicode_value.strip()
		# If unicode, try to strptime against each input format.
		if isinstance(value, unicode):
			for timeFormat in self.inputFormats:
				try:
					return self.strptime(value, timeFormat)
				except ValueError:
					if timeFormat.endswith('.%f'):
						# Compatibility with datetime in pythons < 2.6.
						# See: http://docs.python.org/library/datetime.html#strftime-and-strptime-behavior
						if value.count('.') != timeFormat.count('.'):
							continue
						try:
							datetime_str, usecs_str = value.rsplit('.', 1)
							usecs = int(usecs_str[:6].ljust(6, '0'))
							dt = datetime.datetime.strptime(datetime_str, timeFormat[:-3])
							return dt.replace(microsecond=usecs)
						except ValueError:
							continue
		raise ValidationError(self.error_messages['invalid'])

	def strptime(self, value, timeFormat):
		raise NotImplementedError('Subclasses must define this method.')

class DateField ( _BaseTemporalField ):
	
	"""
	Example:		
	
	where _dbModel is a form class attribute with the model instance.
	
	** Input Formats **
	
	A list of formats used to attempt to convert a string to a valid datetime.date object.

	If no input_formats argument is provided, the default input formats are:

	'%Y-%m-%d',       # '2006-10-25'
	'%m/%d/%Y',       # '10/25/2006'
	'%m/%d/%y',       # '10/25/06'
	
	Additionally, if you specify USE_L10N=False in your settings, the following will also be included in the default input formats:

	'%b %d %Y',       # 'Oct 25 2006'
	'%b %d, %Y',      # 'Oct 25, 2006'
	'%d %b %Y',       # '25 Oct 2006'
	'%d %b, %Y',      # '25 Oct, 2006'
	'%B %d %Y',       # 'October 25 2006'
	'%B %d, %Y',      # 'October 25, 2006'
	'%d %B %Y',       # '25 October 2006'
	'%d %B, %Y',      # '25 October, 2006'
	
	** Required Arguments **

	* ``instance``:object : Model instance
	* ``insField``:str : Model field
	
	** Optional Arguments **
	
	* ``inputFormats``:list : Input formats
	* ``required``:bool : Required field by back-end form valdiation
	* ``initial``:str : Initial value
	* ``jsRequired``:str	: Required field by javascript validation
	* ``label``:str : Field label
	* ``helpText``:str : Field tooptip
	
	** Attributes **
	
	* ``instance``:object
	* ``instanceFieldName``:str
	* ``required``:bool
	* ``initial``:str
	* ``jsRequired``:bool
	* ``label``:str
	* ``helpText``:str
	
	"""

	inputFormats = formats.get_format_lazy('DATE_INPUT_FORMATS')
	defaultErrorMessages = {
		'invalid': _(u'Enter a valid date.'),
	}

	def to_python(self, value):
		"""
		Validates that the input can be converted to a date. Returns a Python
		datetime.date object.
		"""
		if value in django.core.validators.EMPTY_VALUES:
			return None
		if isinstance(value, datetime.datetime):
			return value.date()
		if isinstance(value, datetime.date):
			return value
		return super(DateField, self).to_python(value)

	def strptime(self, value, timeFormat):
		return datetime.datetime.strptime(value, timeFormat).date()

class DateTimeField ( _BaseTemporalField ):
	
	"""
	Example:	
	
	where _dbModel is a form class attribute with the model instance.
	
	** Input Formats **
	
	A list of formats used to attempt to convert a string to a valid datetime.date object.

	If no input_formats argument is provided, the default input formats are:

	'%Y-%m-%d %H:%M:%S',     # '2006-10-25 14:30:59'
	'%Y-%m-%d %H:%M',        # '2006-10-25 14:30'
	'%Y-%m-%d',              # '2006-10-25'
	'%m/%d/%Y %H:%M:%S',     # '10/25/2006 14:30:59'
	'%m/%d/%Y %H:%M',        # '10/25/2006 14:30'
	'%m/%d/%Y',              # '10/25/2006'
	'%m/%d/%y %H:%M:%S',     # '10/25/06 14:30:59'
	'%m/%d/%y %H:%M',        # '10/25/06 14:30'
	'%m/%d/%y',              # '10/25/06'
		
	** Required Arguments **

	* ``instance``:object : Model instance
	* ``insField``:str : Model field
	
	** Optional Arguments **
	
	* ``inputFormats``:list : Input formats
	* ``required``:bool : Required field by back-end form valdiation
	* ``initial``:str : Initial value
	* ``jsRequired``:str	: Required field by javascript validation
	* ``label``:str : Field label
	* ``helpText``:str : Field tooptip
	
	** Attributes **
	
	* ``instance``:object
	* ``instanceFieldName``:str
	* ``required``:bool
	* ``initial``:str
	* ``jsRequired``:bool
	* ``label``:str
	* ``helpText``:str
	
	"""

	fieldType = 'DateTimeField'
	inputFormats = formats.get_format_lazy('DATETIME_INPUT_FORMATS')
	defaultErrorMessages = {
		'invalid': _(u'Enter a valid date/time.'),
	}

	def prepare_value(self, value):
		if isinstance(value, datetime.datetime):
			value = to_current_timezone(value)
		return value

	def to_python(self, value):
		"""
		Validates that the input can be converted to a datetime. Returns a
		Python datetime.datetime object.
		"""
		if value in django.core.validators.EMPTY_VALUES:
			return None
		if isinstance(value, datetime.datetime):
			return from_current_timezone(value)
		if isinstance(value, datetime.date):
			result = datetime.datetime(value.year, value.month, value.day)
			return from_current_timezone(result)
		if isinstance(value, list):
			# Input comes from a SplitDateTimeWidget, for example. So, it's two
			# components: date and time.
			if len(value) != 2:
				raise ValidationError(self.error_messages['invalid'])
			if value[0] in django.core.validators.EMPTY_VALUES and value[1] in django.core.validators.EMPTY_VALUES:
				return None
			value = '%s %s' % tuple(value)
		result = super(DateTimeField, self).to_python(value)
		return from_current_timezone(result)

	def strptime(self, value, timeFormat):
		return datetime.datetime.strptime(value, timeFormat)

class TimeField ( _BaseTemporalField ):
	
	"""
	Example:
	
	where _dbModel is a form class attribute with the model instance.
	
	** Input Formats **
	
	A list of formats used to attempt to convert a string to a valid datetime.date object.
	
	If no input_formats argument is provided, the default input formats are:

	'%H:%M:%S',     # '14:30:59'
	'%H:%M',        # '14:30'
	
	** Required Arguments **

	* ``instance``:object : Model instance
	* ``insField``:str : Model field
	
	** Optional Arguments **
	
	* ``inputFormats``:list : Input formats
	* ``required``:bool : Required field by back-end form valdiation
	* ``initial``:str : Initial value
	* ``jsRequired``:str	: Required field by javascript validation
	* ``label``:str : Field label
	* ``helpText``:str : Field tooptip
	
	** Attributes **
	
	* ``instance``:object
	* ``instanceFieldName``:str
	* ``required``:bool
	* ``initial``:str
	* ``jsRequired``:bool
	* ``label``:str
	* ``helpText``:str
	
	"""
	
	inputFormats = formats.get_format_lazy('TIME_INPUT_FORMATS')
	dateTimeFormat = 'time'
	defaultErrorMessages = {
		'invalid': _(u'Enter a valid time.')
	}

	def to_python(self, value):
		"""
		Validates that the input can be converted to a time. Returns a Python
		datetime.time object.
		"""
		if value in django.core.validators.EMPTY_VALUES:
			return None
		if isinstance(value, datetime.time):
			return value
		return super(TimeField, self).to_python(value)

	def strptime(self, value, timeFormat):
		return datetime.datetime.strptime(value, timeFormat).time()

class HiddenField( Field ):
	"""
	Hidden Field, name and value.
	
	** Optional Arguments **
	
	* ``initial``:str : Initial value
	
	** Attributes **
	
	* ``initial``:str : Initial value
	"""
	
	def __init__(self, initial=None):
		initial = initial or ''
		super(HiddenField, self).__init__(None, '', initial=initial)
		self.attrs['data-xp-type'] = 'input.hidden'
		self.attrs['type'] = 'hidden'

class UserField( Field ):
	"""
	User id field
	
	** Required Arguments **
	
	* ``instance``:object : Model instance
	* ``insField``:str : Model field
	
	** Optional Arguments **
	
	* ``minLength``:int : Field minimum length
	* ``maxLength``:int : Field maximum length
	* ``required``:bool : Required field by back-end form valdiation
	* ``initial``:str : Initial value
	* ``jsRequired``:str	: Required field by javascript validation
	* ``label``:str : Field label
	* ``helpText``:str : Field tooptip
	
	** Attributes **
	
	* ``instance``:object
	* ``instanceFieldName``:str
	* ``minLength``:str
	* ``maxLength``:str
	* ``required``:bool
	* ``initial``:str
	* ``jsRequired``:bool
	* ``label``:str
	* ``helpText``:str	
	
	"""
	
	defaultErrorMessages = {
		'invalid': _(u'Enter a valid user id.'),
							}
	defaultValidators = [validateUserId]
	
	def __init__(self, instance, insField, minLength=None, maxLength=None, required=True, initial='', jsRequired=None, 
				label=None, helpText=None, jsVal=None):
		super(UserField, self).__init__(instance, insField, required=required, jsRequired=jsRequired, label=label, 
									initial=initial, helpText=helpText, jsVal=jsVal)
		self.attrs['data-xp-val'] = 'userid'

class EmailField( CharField ):
	"""
	Email field. Validates email address	
	
	** Required Arguments **
	
	* ``instance``:object : Model instance
	* ``insField``:str : Model field
	
	** Optional Arguments **
	
	* ``minLength``:int : Field minimum length
	* ``maxLength``:int : Field maximum length
	* ``required``:bool : Required field by back-end form valdiation
	* ``initial``:str : Initial value
	* ``jsRequired``:str	: Required field by javascript validation
	* ``label``:str : Field label
	* ``helpText``:str : Field tooptip
	
	** Attributes **
	
	* ``instance``:object
	* ``instanceFieldName``:str
	* ``minLength``:str
	* ``maxLength``:str
	* ``required``:bool
	* ``initial``:str
	* ``jsRequired``:bool
	* ``label``:str
	* ``helpText``:str
	
	"""
	
	defaultErrorMessages = {
		'invalid': _(u'Enter a valid e-mail address.'),
	}
	defaultValidators = [django.core.validators.validate_email]
	
	def __init__(self, instance, insField, minLength=None, maxLength=None, required=True, initial='', jsRequired=None, 
				label=None, helpText=None, jsVal=None):
		super(EmailField, self).__init__(instance, insField, required=required, jsRequired=jsRequired, label=label, 
									initial=initial, helpText=helpText, jsVal=jsVal)
		self._updateAttrs(self.attrs, 'data-xp-val', 'email')

	def clean(self, value):
		value = self.to_python(value).strip()
		return super(EmailField, self).clean(value)	

class PasswordField( CharField ):
	"""
	Password field. Checks valid password
	
	** Required Arguments **
	
	* ``instance``:object : Model instance
	* ``insField``:str : Model field
	
	** Optional Arguments **
	
	* ``minLength``:int : Field minimum length
	* ``maxLength``:int : Field maximum length
	* ``required``:bool : Required field by back-end form valdiation
	* ``initial``:str : Initial value
	* ``jsRequired``:str	: Required field by javascript validation
	* ``label``:str : Field label
	* ``helpText``:str : Field tooptip
	
	** Attributes **
	
	* ``instance``:object
	* ``instanceFieldName``:str
	* ``minLength``:str
	* ``maxLength``:str
	* ``required``:bool
	* ``initial``:str
	* ``jsRequired``:bool
	* ``label``:str
	* ``helpText``:str
	
	"""
	
	defaultErrorMessages = {
		'invalid': _(u'Enter a valid password'),
	}
	defaultValidators = [validatePassword]
	
	def __init__(self, instance, insField, minLength=None, maxLength=None, required=True, initial='', jsRequired=None, 
				label=None, helpText=None, jsVal=None):
		super(PasswordField, self).__init__(instance, insField, required=required, jsRequired=jsRequired, label=label, 
									initial=initial, helpText=helpText, jsVal=jsVal)
		self.attrs['data-xp-val'] = 'password'

@DeprecationWarning
class TextChoiceField( Field  ):
	"""Text Choice Field. Field with autocompletion
	
	This field is ximple CharField with autocompletion support. Autocompletion values fetched from id_choices or ajax jxSuggestList
	
	in autocomplete we have visual component attributes:
	
	- maxHeight:int
	- mincharacters:int
	- maxFields:int
	- hasSearchMore:bool
	
	In case not defined, we get them from js settings. Fields with autocomplete field.*
	
	- arguments:
	
	- * dbClass (url) : completeDb
	- * params (url) . completeParams 
	
	django settings??? model settings ???	
	
	"""
	def __init__(self, instance, insField, minLength=None, maxLength=None, required=True, init=None, jsRequired=None, maxHeight=200, 
				minCharacters=3, choicesId='', dbClass='', params={}, xpType='field', **args):
		self._doInstanceInit(instance, insField)
		fieldMaxLength = self._getMaxLength()
		args['validators'] = []
		args['max_length'] = maxLength if maxLength != None else fieldMaxLength
		args['min_length'] = minLength if minLength != None else None
		args['required'], args['jsRequired'] = self._doRequired(required, jsRequired)
		classStr = 'fieldMust' if required == True else 'field'
		attrs = self._doAttrs(args, {	'class': classStr,
							'maxlength': str(args['max_length']),
							'choicesId': choicesId,
							'xpType': xpType})
		attrs['data-xp'] = {	'maxHeight': maxHeight,
								'minCharacters' : minCharacters
								}
		if dbClass != '' and len(params) != 0:
			attrs['data-xp']['url'] = '/jxSuggestList?dbClass=' + dbClass + ';params=' + json.dumps(params) 
		"""if not args.has_key('widget'):
			args['widget'] = TextInputWidget(attrs=attrDict)"""
		args['widget'] = Widget(attrs=attrs)
		super(TextChoiceField, self).__init__(**args)

class FileBrowseField ( CharField ):
	"""
	File browser form field.
	
	We keep additional attributes for visual component into ``data-xp`` html attribute:
	
	* ``site`` : Site to search for files.
	* ``directory`` : Directory to search for files.
	* ``extensions`` : File extensions to search for files.
	* ``fieldFormats : File formats to search for.
	
	These attributes are used to search for files when search icon in file browser field is clicked.
	
	In case these attributes are None, files will be searched in default media home with all extensions and file formats.
	
	** Required Arguments **

	* ``instance``:object : Model instance
	* ``insField``:str : Model field	

	
	** Optional Arguments **
	
	* ``site``:str : Site that keeps media files
	* ``directory``:str : Directory that keeps media files
	* ``extensions``:list : Extensions
	* ``fieldFormat``:list : Field formats
	
	** Attributes **
	
	* ``instance``:object
	* ``instanceFieldName``:str
	* ``minLength``:str
	* ``maxLength``:str
	* ``required``:bool
	* ``initial``:str
	* ``jsRequired``:bool
	* ``label``:str
	* ``helpText``:str
	* ``site``:str : Site that keeps media files
	* ``directory``:str : Directory that keeps media files
	* ``extensions``:list : Extensions
	* ``fieldFormat``:list : Field formats
	
	"""
	
	defaultErrorMessages = {
        'extension': _(u'Extension %(ext)s is not allowed. Only %(allowed)s is allowed.'),
    }
	
	def __init__(self, instance, insField, minLength=None, maxLength=None, required=True, initial='', jsRequired=None, 
				label=None, helpText=None, site=None, directory=None, extensions=None, fieldFormats=None, jsVal=None):
		self.site = site
		self.directory = directory
		self.extensions = extensions
		if fieldFormats:
			self.fieldFormat = fieldFormats or ''
			if settings.FILEBROWSER_EXTENSIONS:
				self.extensions = settings.EXTENSIONS.get(fieldFormats)
		super(FileBrowseField, self).__init__(instance, insField, required=required, jsRequired=jsRequired, label=label, 
									initial=initial, helpText=helpText, jsVal=jsVal)
		self.attrs['data-xp'] = "{	site:'" + self.site + "', directory: '" + self.directory +\
									 "', extensions: '" + self.extensions +\
									  "', fieldFormats: '" + self.fieldFormats + "'}"		

class OneListField( Field ):
	"""
	Select field. Will render to combobox, option lists, autocomplete, etc... when form instance is rendered, values are
	fetched from database to fill ``id_choices``hidden field with data for field values.
	
	In case choices is not null, we attempt to skip foreign key search for values and get values from choices object.
	
	From choices...
	country = OneListField(_dbAddress, '_dbAddress.country', choicesId='country', required=False, choices=Choices.COUNTRY)
	
	From fk...
	country = OneListField(_dbAddress, '_dbAddress.country', choicesId='country', required=False)
	
	** From Choices **
	
	You need to include arguments ``choicesId``, ``choices``.
	
	** From Foreign Key **
	
	You need to include arguments: ``choicesId``. Optional ``limitTo``, ``orderBy`` and ``listValue``. In case these
	optional attributes not defined, will search without filter and name will be FK and value string representation of model instance.
	
	** Required Arguments **
	
	* ``instance``:object : Model instance
	* ``insField``:str : Model field, like '_myModel.fieldName'
	* ``choicesId``:str: Choice id to save into id_choices hidden field, like {myChoiceId: [(name1,value1),(name2,value2),...] ... }
	
	** Optional Arguments **
	
	* ``limitTo``:dict : Dictionary with attributes sent to model filter method
	* ``repr``:str : Model field to be used for value in (name, value) pairs. By default, string notation of model used.
	* ``values``:list : List of values to append to 'id_choices'
	* ``orderBy``:tuple : Order by tuples, like ('field', '-field2'). field ascending and field2 descending.
	* ``choices``:list
	
	** Attributes **
	
	* ``instance``:object
	* ``instanceFieldName``:str
	* ``required``:bool
	* ``initial``:str
	* ``jsRequired``:bool
	* ``label``:str
	* ``helpText``:str
	* ``choicesId``:str
	* ``limitTo``:dict
	* ``orderBy``:tuple
	* ``listValue``:str
	* ``values``:tuple
	
	** Visual Component Attributes **
	
	Attributes in attrs field attribute:
	
	* ``choicesId``
	* ``data-xp-val``
	* ``help_text``
	* ``class``
	* ``label``
	
	** Methods **
	
	* ``buildList()``:list<(name:str, value:str, data:dict)> : Build list of tuples (name, value) and data associated to values argument
	
	"""
	def __init__(self, instance, insField, choicesId=None, limitTo=None, listValue=None, values=None, choices=None, orderBy=None,
				required=True, initial='', jsRequired=None, label=None, helpText=None):
		if choicesId == None:
			raise XpMsgException(AttributeError, _('choicesId is required'))
		#instanceFieldName = self._getFieldName(insField)
		#logger.debug('OneListField :: instance: %s' % (instance) )
		#logger.debug('OneListField :: instanceFieldName: %s' % (instanceFieldName) )
		self.listValue = listValue or ''
		self.values = values or ()
		self.limitTo = limitTo or {}
		self.choicesId = choicesId or ''
		self.choices = choices or ()
		self.orderBy = orderBy or ()
		super(OneListField, self).__init__(instance, insField, required=required, jsRequired=jsRequired, label=label, 
									initial=initial, helpText=helpText)
		if choices == None and self._isForeignKey() == False:
			raise XpMsgException(AttributeError, _('Either choices must be declared or field be a Foreign key'))
		self.attrs['choicesId'] = self.choicesId
		
	def buildList(self):
		"""
		Build list of possible values for field. Depending on type of rendering, will be shown in a option element, 
		select or checkbox, as well as any additional visual component with selection of one item from a list.
		
		** Returns **
		
		``valueList``:list<(name, value)>
		
		"""		
		
		if len(self.choices) != 0:
			# choices
			valueList = self.choices
		else:
			model = self.instance.__class__  #@UnusedVariableWarning
			field = eval('model.' + self.instanceFieldName)
			if self._isForeignKey() == False:
				raise XpMsgException(AttributeError, _('Field must be ForeignKey if choices attribute  is not declared.'))
			# foreign key
			valueList = []			
			limitChoicesTo = self._getLimitChoicesTo(self.instance, self.instanceFieldName)
			if len(limitChoicesTo) != 0 and len(self.limitTo) == 0:
				self.limitTo = limitChoicesTo			
			# in case we have limitTo, place filter query. Otherwise, run all() on queryset related to foreign key
			if len(self.limitTo) == 0:
				if len(self.orderBy) == 0:
					rows = field.get_query_set().all()
				else:
					rows = field.get_query_set().all().order_by(self.orderBy)
			else:
				if len(self.orderBy) == 0:
					rows = field.get_query_set().filter(**self.limitTo)
				else:
					rows = field.get_query_set().filter(**self.limitTo).order_by(self.orderBy)
			# Get name and value, and add to valueList
			for row in rows:
				name = str(row.pk)
				value = str(row)
				if self.listValue != '':
					value = eval('row.' + self.listValue)
				# Additional data to name, value
				valuesDict = {}				
				for field in self.values:
					try:
						valuesDict[field] = eval('row.' + field)
					except AttributeError:
						# value from model not found
						pass
				valueList.append((name, value, valuesDict))
		return valueList		

class ManyListField( Field ):
	"""
	Selection with many possible values. Will render: select with multiple attribute, list of items with checkbox, other
	visual components with multiple values from a list.
	
	In case choices is not null, we attempt to skip many search for values and get values from choices object.
	
	From choices...
	country = ManyListField(_dbAddress, '_dbAddress.country', choicesId='country', required=False, choices=Choices.COUNTRY)
	
	From many relationship...
	country = ManyListField(_dbAddress, '_dbAddress.country', choicesId='country', required=False)
	
	** From Choices **
	
	You need to include arguments ``choicesId``, ``choices``.
	
	** From Many to Many relationship **
	
	You need to include arguments: ``choicesId``. Optional ``limitTo``, ``listName``and ``listValue``. In case these
	optional attributes not defined, will search without filter and name will be FK and value string representation of model instance.
	
	** Required Arguments **
	
	* ``instance``:object : Model instance
	* ``insField``:str : Model field, like '_myModel.fieldName'
	* ``choicesId``:str: Choice id to save into id_choices hidden field, like {myChoiceId: [(name1,value1),(name2,value2),...] ... }
	
	** Optional Arguments **
	
	* ``limitTo``:dict : Dictionary with attributes sent to model filter method
	* ``listValue``:str : Model field to be used for value in (name, value) pairs. By default, string notation of model used.
	* ``values``:tuple
	* ``orderBy``:tuple : Order by tuples, like ('field', '-field2'). field ascending and field2 descending.
	* ``choices``:list
	
	** Attributes **
	
	* ``instance``:object
	* ``instanceFieldName``:str
	* ``required``:bool
	* ``initial``:str
	* ``jsRequired``:bool
	* ``label``:str
	* ``helpText``:str
	* ``choicesId``:str
	* ``limitTo``:dict
	* ``orderBy``:tuple
	* ``values``:tuple
	* ``listValue``:str
	
	** Visual Component Attributes **
	
	Attributes inside attrs field attribute:
	
	* ``choicesId``
	* ``data-xp-val``
	* ``help_text``
	* ``class``
	* ``label``
		
	** Methods **
	
	* ``buildList()``:list<(name:str, value:str, data:dict)> : Build list of tuples (name, value) and data associated to values argument	
	
	"""
	def __init__(self, instance, insField, choicesId=None, limitTo=None, listValue=None, values=None, choices=None, orderBy=None,
				required=True, initial='', jsRequired=None, label=None, helpText=None):
		if choicesId == None:
			raise XpMsgException(AttributeError, _('choicesId is required'))
		#instanceFieldName = self._getFieldName(insField)
		#logger.debug('ManyListField :: instance: %s' % (instance) )
		#logger.debug('ManyListField :: instanceFieldName: %s' % (instanceFieldName) )
		self.listValue = listValue or ''
		self.values = values or ()
		self.limitTo = limitTo or {}
		self.choicesId = choicesId or ''
		self.choices = choices or ()
		self.orderBy = orderBy or ()
		super(ManyListField, self).__init__(instance, insField, required=required, jsRequired=jsRequired, label=label, 
									initial=initial, helpText=helpText)
		if choices == None and self._isManyToMany() == False:
			raise XpMsgException(AttributeError, _('Either choices must be declared or field be a ManyToMany relationship'))
		self.attrs['choicesId'] = self.choicesId
		if initial == '':
			self.initial = '[]'
		
	def buildList(self):
		"""
		Build list of possible values for field. Depending on type of rendering, will be shown in checkbox, multiple
		select, and any other components that more than one item can be checked / selected.
		
		** Returns **
		
		``valueList``:list<(name, value)>
		
		"""
		
		if len(self.choices) != 0:
			# choices
			valueList = self.choices
		else:
			model = self.instance.__class__  #@UnusedVariableWarning

			if self._isManyToMany() == False:
				raise XpMsgException(AttributeError, _('Field must be ManyToMany if choices attribute is not declared.'))
			# many to many			
			valueList = []
			
			limitChoicesTo = self._getLimitChoicesTo(self.instance, self.instanceFieldName)
			if len(limitChoicesTo) != 0 and len(self.limitTo) == 0:
				self.limitTo = limitChoicesTo
			# in case we have limitTo, place filter query. Otherwise, run all() on related parent model related to foreign key
			if len(self.limitTo) == 0:
				if len(self.orderBy) == 0:
					# Default query without limitTo or orderBy
					rows = model._meta.get_field_by_name(self.instanceFieldName)[0].related.parent_model.\
						objects.all()
				else:
					rows = model._meta.get_field_by_name(self.instanceFieldName)[0].related.parent_model\
						.objects.all().order_by(self.orderBy)
			else:
				if len(self.orderBy) == 0:
					rows = model._meta.get_field_by_name(self.instanceFieldName)[0].related.parent_model\
						.objects.filter(**self.limitTo)
				else:
					rows = model._meta.get_field_by_name(self.instanceFieldName)[0].related.parent_model\
						.objects.filter(**self.limitTo).order_by(self.orderBy)
			# Get name and value, and add to valueList
			for row in rows:
				name = str(row.pk)
				value = str(row)
				if self.listValue != '':
					value = eval('row.' + self.listValue)
				# Additional data to name, value
				valuesDict = {}				
				for field in self.values:
					try:
						valuesDict[field] = eval('row.' + field)
					except AttributeError:
						# value from model not found
						pass
				valueList.append((name, value, valuesDict))
		return valueList
