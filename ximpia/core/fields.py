import json
import os
import datetime
import copy
from decimal import Decimal, DecimalException

from django.forms import ChoiceField, MultipleChoiceField

from django.forms.widgets import Widget

from django.forms.util import from_current_timezone, to_current_timezone
from django.core.exceptions import ValidationError
from django.utils import formats
from django.utils.encoding import smart_str, force_unicode, smart_unicode
from django.utils.ipv6 import clean_ipv6_address
from django.utils.translation import ugettext_lazy as _
import django.core.validators

from ximpia.util.basic_types import DictUtil
from validators import validateTxtField, validatePassword, validateUserId

# Settings
from ximpia.core.util import getClass
settings = getClass(os.getenv("DJANGO_SETTINGS_MODULE"))

# Logging
import logging.config
logging.config.dictConfig(settings.LOGGING)
logger = logging.getLogger(__name__)

class Field( object ):
	instance = None
	initial = ''
	instanceName = ''
	instanceFieldName = ''
	attrs = {}
	creationCounter = 0
	defaultValidators = []
	defaultErrorMessages = {}
	localize = False
	def __init__(self, instance, insField, required=True, jsRequired=None, label=None, initial=None, helpText=None, 
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
		classStr = 'fieldMust' if required == True else 'field'
		if required == False and jsRequired == True:
			classStr = 'fieldMust'
		# attrs
		self.attrs['class'] = classStr
		if label is not None:
			label = smart_unicode(label)
		self.required, self.label, self.initial = required, label, initial
		initValue = initial if initial != None else ''
		# helpText		
		if helpText is None:
			self.helpText = u''
		else:
			self.helpText = smart_unicode(helpText)
		if self.instance: 
			self.initial = eval('self.instance' + '.' + self.instanceFieldName) if self.instance != None and initial == None else initValue
		if self.instance:
			if not label:
				self.label = smart_unicode(self.instance._meta.get_field_by_name(self.instanceFieldName)[0].verbose_name.title())
			if not helpText:
				self.helpText = smart_unicode(self.instance._meta.get_field_by_name(self.instanceFieldName)[0].help_text.title())
		# jsRequired
		self.jsRequired = jsRequired
		if required == True and not self.jsRequired:
			self.jsRequired= True
		if required == False and not self.jsRequired:
			self.jsRequired = False
		if self.jsRequired:
			if self.jsRequired == True:
				self._updateAttrs(self.attrs, 'data-xp-val', 'required')
		logger.debug( 'attrs for %s: %s' % (self.label, str(self.attrs)) )
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
		
	def _doInstanceInit(self, instance, insField):
		"""Set instance and instanceName and instanceFieldName"""
		if insField.find('.') != -1:
			instanceName, instanceFieldName = insField.split('.')
			self.instanceName = instanceName
			self.instanceFieldName = instanceFieldName
			self.instance = instance
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
		if jsRequired == None:
			jsRequired = required
		t = (required, jsRequired)
		return t
	@DeprecationWarning
	def _doAttrs(self, args, attrDict):
		"""
		Process form attrs with field attribute dictionary for widget
		
		** Arguments **
		
		* ``args``
		* ``attrDict``
		
		** Returns **
		Dict, attribute dictionary
		"""
		d = {}
		if args.has_key('attrs'):
			d = DictUtil.addDicts([args['attrs'], attrDict])
		else:
			d = attrDict
		return d
	
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
	* ``instanceName``:str
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
	def __init__(self, instance, insField, minLength=None, maxLength=None, required=True, initial='', jsRequired=None, 
				label=None, helpText=None):
		self.minLength, self.maxLength = minLength, maxLength
		super(CharField, self).__init__(instance, insField, required=required, jsRequired=jsRequired, label=label, 
									initial=initial, helpText=helpText)
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

"""
Example: Months

option
======
form.month variable
model: jan
choices: ('jan','January')...
<label><input type="radio" name="month" value="jan" selected /> January</label> (Comes from choices table)
<label><input type="radio" name="month" value="feb"  /> February</label>
OptionChoiceField

checkbox
========
form.month variable
model: ['jan','feb'] 255 bytes, separated by comma. '' => [] .. 'jan' => ['jan'] .. 'jan,feb' => ['jan','feb']
<label><input type="checkbox" name="month" value="jan" checked /> January</label> (Comes from choices table)
<label><input type="checkbox" name="month" value="feb" /> February</label>
CheckboxChoiceField

checkbox no choices
===================
form.client variable
model: Many to many field
<label><input type="checkbox" name="client" value="$id" checked /> Client A</label> (comes from string representation of model)
<label><input type="checkbox" name="client" value="$id" checked /> Client B</label>
CheckboxField => (pk, str)...
"""

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
	* ``instanceName``:str
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
	* ``instanceName``:str
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
	* ``instanceName``:str
	* ``instanceFieldName``:str
	* ``required``:bool
	* ``initial``:str
	* ``jsRequired``:bool
	* ``label``:str
	* ``helpText``:str
	
	"""
	
	defaultErrorMessages = {}

	def __init__(self, instance, insField, minLength=None, maxLength=None, required=True, initial='', jsRequired=None, 
				label=None, helpText=None, protocol='both', unpackIpv4=False):
		self.unpack_ipv4 = unpackIpv4
		self.defaultValidators, invalidErrorMessage = django.core.validators.ip_address_validators(protocol, unpackIpv4)
		self.defaultErrorMessages['invalid'] = invalidErrorMessage
		self.required, self.jsRequired = self._doRequired(required, jsRequired)
		super(GenericIPAddressField, self).__init__(instance, insField, required=required, jsRequired=jsRequired, label=label, 
									initial=initial, helpText=helpText)
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
	* ``instanceName``:str
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
				maxValue=None, minValue=None, maxDigits=None, decimalPlaces=None):
		self.maxValue, self.minValue = maxValue, minValue
		self.maxDigits, self.decimalPlaces = maxDigits, decimalPlaces
		#Field.__init__(self, *args, **kwargs)
		super(DecimalField, self).__init__(instance, insField, required=required, jsRequired=jsRequired, label=label, 
									initial=initial, helpText=helpText)
		if maxValue is not None:
			self.validators.append(django.core.validators.MaxValueValidator(maxValue))
		if minValue is not None:
			self.validators.append(django.core.validators.MinValueValidator(minValue))

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
	* ``instanceName``:str
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
				maxValue=None, minValue=None):
		self.maxValue, self.minValue = maxValue, minValue
		super(IntegerField, self).__init__(instance, insField, required=required, jsRequired=jsRequired, label=label, 
									initial=initial, helpText=helpText)
		if maxValue is not None:
			self.validators.append(django.core.validators.MaxValueValidator(maxValue))
		if minValue is not None:
			self.validators.append(django.core.validators.MinValueValidator(minValue))

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
	* ``instanceName``:str
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
	* ``instanceName``:str
	* ``instanceFieldName``:str
	* ``required``:bool
	* ``initial``:str
	* ``jsRequired``:bool
	* ``label``:str
	* ``helpText``:str
	
	"""

	def __init__(self, instance, insField, required=True, initial='', jsRequired=None, label=None, helpText=None, inputFormats=None):
		super(_BaseTemporalField, self).__init__(instance, insField, required=required, jsRequired=jsRequired, label=label, 
									initial=initial, helpText=helpText)
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
	* ``instanceName``:str
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
	* ``instanceName``:str
	* ``instanceFieldName``:str
	* ``required``:bool
	* ``initial``:str
	* ``jsRequired``:bool
	* ``label``:str
	* ``helpText``:str
	
	"""

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
	* ``instanceName``:str
	* ``instanceFieldName``:str
	* ``required``:bool
	* ``initial``:str
	* ``jsRequired``:bool
	* ``label``:str
	* ``helpText``:str
	
	"""
	
	inputFormats = formats.get_format_lazy('TIME_INPUT_FORMATS')
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

class OptionChoiceField( Field ):
	"""Option Group Field. Labels and values comes from the choices list."""
	def __init__(self, instance, insField, xpType='option', choicesId='', **args):
		self._doInstanceInit(instance, insField)
		attrs = self._doAttrs(args, {	'choicesId': choicesId,	
							'xpType': xpType	})
		#if not args.has_key('widget'):
		#args['widget'] = OptionWidget(attrs=attrDict)
		args['widget'] = Widget(attrs=attrs)
		super(OptionChoiceField, self).__init__(**args)

class CheckboxChoiceField( Field ):
	"""Checkbox Group Field. Labels and values comes from the choices list.
	
	Checkbox group with values fetched from id_choices
	
	"""
	def __init__(self, instance, insField, xpType='checkbox', choicesId='', **args):
		self._doInstanceInit(instance, insField)
		attrs = self._doAttrs(args, {	'choicesId': choicesId,	
							'xpType': xpType	})
		#if not args.has_key('widget'):
		#args['widget'] = CheckboxWidget(attrs=attrDict)
		args['widget'] = Widget(attrs=attrs)
		super(CheckboxChoiceField, self).__init__(**args)

class HiddenField( Field ):
	"""
	Hidden Field, name and value.
	
	** Optional Arguments **
	
	* ``initial``:str : Initial value
	
	** Attributes **
	
	* ``initial``:str : Initial value
	"""
	def __init__(self, initial=None):
		super(HiddenField, self).__init__(initial=initial)

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
	* ``instanceName``:str
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
				label=None, helpText=None):
		super(UserField, self).__init__(instance, insField, required=required, jsRequired=jsRequired, label=label, 
									initial=initial, helpText=helpText)
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
	* ``instanceName``:str
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
				label=None, helpText=None):
		super(EmailField, self).__init__(instance, insField, required=required, jsRequired=jsRequired, label=label, 
									initial=initial, helpText=helpText)
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
	* ``instanceName``:str
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
				label=None, helpText=None):
		super(PasswordField, self).__init__(instance, insField, required=required, jsRequired=jsRequired, label=label, 
									initial=initial, helpText=helpText)
		self.attrs['data-xp-val'] = 'password'

class ChoiceTextField( Field ):
	"""Choice field with autocompletion. Behaves like a select, with name and value
	
	Autocompletion
	
	Preferred Visual Type: list.select
	
	We could use CharField with minCharacters
	
	"""
	def __init__(self, instance, insField, minLength=None, maxLength=None, required=True, init=None, jsRequired=None, maxHeight=200, 
				minCharacters=3, choices=(), dbClass='', params={}, xpType='list.select', **args):
		self._doInstanceInit(instance, insField)
		fieldMaxLength = self._getMaxLength()
		args['validators'] = []
		args['max_length'] = maxLength if maxLength != None else fieldMaxLength
		args['min_length'] = minLength if minLength != None else None
		args['required'], args['jsRequired'] = self._doRequired(required, jsRequired)
		classStr = 'fieldMust' if required == True else 'field'
		attrs = self._doAttrs(args, {	'class': classStr,
							'maxlength': str(args['max_length']),
							'xpType': xpType})
		#data, maxHeight, minCharacters, url
		#$('#id_jobTitle').jsonSuggest({data: $('#id_jobTitle_data').attr('value'), maxHeight: 200, minCharacters:3});
		#d = {'id': tupleData[0], 'text': tupleData[1]}
		"""suggestList = []
		for tuple in choices:
			suggestList.append({'id': tuple[0], 'text': tuple[1]})"""
		attrs['data-xp'] = {	'maxHeight': maxHeight,
								'minCharacters' : minCharacters
					}
		"""if len(choices) != 0:
			attrDict['data-xp']['data'] = suggestList"""
		"""if dbClass != '' and len(params) != 0:
			attrDict['data-xp']['url'] = '/jxSuggestList?dbClass=' + dbClass + ';params=' + json.dumps(params)""" 
		"""if not args.has_key('widget'):
			args['widget'] = TextInputWidget(attrs=attrDict)"""
		args['widget'] = Widget(attrs=attrs)
		super(ChoiceTextField, self).__init__(**args)

class TextChoiceField( Field  ):
	"""Text Choice Field. Field with autocompletion
	
	This field is ximple CharField with autocompletion support. Autocompletion values fetched from id_choices or ajax jxSuggestList
	
	"""
	def __init__(self, instance, insField, minLength=None, maxLength=None, required=True, init=None, jsRequired=None, maxHeight=200, minCharacters=3, 
			choicesId='', dbClass='', params={}, xpType='field', **args):
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

class ListOneField( Field ):
	"""
	Select field. Will render to combobox, option lists, autocomplete, etc... when form instance is rendered, values are
	fetched from database to fill ``id_choices``hidden field with data for field values.
	
	** Required Arguments **
	
	* ``instance``:object : Model instance
	* ``insField``:str : Model field, like '_myModel.fieldName'
	* ``choicesId``:str: Choice id to save into id_choices hidden field, like {myChoiceId: [(name1,value1),(name2,value2),...] ... }
	
	** Optional Arguments **
	
	* ``limitTo``:dict : Dictionary with attributes sent to model filter method
	* ``listName``:str : Model field to use for name in (name, value) pairs. By default, pk is used.
	* ``listValue``:str : Model field to be used for value in (name, value) pairs. By default, string notation of model used.
	
	**args accept other arguments to be passed to the django Field parent class
	
	** Methods **
	
	* ``build()`` : ???? on hold so far...
	
	"""
	def __init__(self, instance, insField, choicesId=None, limitTo={}, listName=None, listValue=None, required=True, init='', **args):
		if insField.find('.') != -1:
			instanceName, instanceFieldName = insField.split('.')
			self.instanceName = instanceName
			self.instanceFieldName = instanceFieldName
			self.instance = instance
		classStr = 'fieldMust' if required == True else 'field'
		xpVal = 'required' if required == True else ''
		args['required'] = required
		if instance != None:
			if not args.has_key('label'):
				args['label'] = instance._meta.get_field_by_name(self.instanceFieldName)[0].verbose_name if instance else args['label']
			if not args.has_key('help_text'):
				args['help_text'] = instance._meta.get_field_by_name(self.instanceFieldName)[0].help_text if instance else args['help_text']
			args['initial'] = init if init != '' else eval('instance' + '.' + self.instanceFieldName)
		attrs = self._doAttrs(args, {	'class': classStr,
							'data-xp-val': xpVal,
							'choicesId': choicesId})
		args['widget'] = Widget(attrs=attrs)
		# tabindex
		if args.has_key('tabindex'):
			args['widget'].attrs['tabindex'] = str(args['tabindex'])
		if args.has_key('val'):
			del args['val']
		if args.has_key('jsVal'):
			del args['jsVal']
		if args.has_key('jsRequired'):
			del args['jsRequired']
		if args.has_key('tabindex'):
			del args['tabindex']
		super(ListOneField, self).__init__(**args)

class ChoiceField( ChoiceField ):
	"""ChoiceField"""
	def _doAttrs(self, args, attrDict):
		"""Process form attrs with field attribute dictionary for widget
		@param args: 
		@param attrDict: 
		@return: dict"""
		d = {}
		if args.has_key('attrs'):
			d = DictUtil.addDicts([args['attrs'], attrDict])
		else:
			d = attrDict
		return d
	def __init__(self, instance, insField, required=True, init='', choicesId='', xpType='list.select', **args):
		if insField.find('.') != -1:
			instanceName, instanceFieldName = insField.split('.')
			self.instanceName = instanceName
			self.instanceFieldName = instanceFieldName
			self.instance = instance
		classStr = 'fieldMust' if required == True else 'field'
		xpVal = 'required' if required == True else ''
		args['required'] = required
		if instance != None:
			if not args.has_key('label'):
				args['label'] = instance._meta.get_field_by_name(self.instanceFieldName)[0].verbose_name if instance else args['label']
			if not args.has_key('help_text'):
				args['help_text'] = instance._meta.get_field_by_name(self.instanceFieldName)[0].help_text if instance else args['help_text']
			args['initial'] = init if init != '' else eval('instance' + '.' + self.instanceFieldName)
		#args['choices'] = choices if choices != None else None
		#args['choicesId'] = choicesId if choicesId != '' else ''
		#logger.debug( 'choicesId : ' + choicesId )
		attrDict = self._doAttrs(args, {	'class': classStr,
											'data-xp-val': xpVal,
											'choicesId': choicesId,
											'xpType': xpType})
		"""if not args.has_key('widget'):
			args['widget'] = SelectWidget(attrs=attrDict)"""
		args['widget'] = Widget(attrs=attrDict)
		# tabindex
		if args.has_key('tabindex'):
			args['widget'].attrs['tabindex'] = str(args['tabindex'])
		if args.has_key('val'):
			del args['val']
		if args.has_key('jsVal'):
			del args['jsVal']
		if args.has_key('jsRequired'):
			del args['jsRequired']
		if args.has_key('tabindex'):
			del args['tabindex']
		super(ChoiceField, self).__init__(**args)

class MultiField( MultipleChoiceField ):
	"""
	Ximpia Multiple Choice Field
	
	Used with "select" multiple fields. This field is doubt to be deprecated
	
	Deprecated???
	"""
	def _doAttrs(self, args, attrDict):
		"""Process form attrs with field attribute dictionary for widget
		@param args: 
		@param attrDict: 
		@return: dict"""
		d = {}
		if args.has_key('attrs'):
			d = DictUtil.addDicts([args['attrs'], attrDict])
		else:
			d = attrDict
		return d
	def __init__(self, instance, insField, required=True, init=[], choices=None, multiple=False, **args):
		if insField.find('.') != -1:
			instanceName, instanceFieldName = insField.split('.')
			self.instanceName = instanceName
			self.instanceFieldName = instanceFieldName
			self.instance = instance
		classStr = 'fieldMust' if required == True else 'field'
		xpVal = 'required' if required == True else ''
		#classStr = 'SmallMust' if required == True else 'Small'
		args['required'] = required
		if instance:
			if not args.has_key('label'):
				args['label'] = instance._meta.get_field_by_name(self.instanceFieldName)[0].verbose_name
			if not args.has_key('help_text'):
				args['help_text'] = instance._meta.get_field_by_name(self.instanceFieldName)[0].help_text		
		if len(init) == 0 and instance:
			listRaw = eval('instance' + '.' + self.instanceFieldName + '.all()')
			l = []
			for obj in listRaw:
				l.append(obj.pk)
			args['initial'] = l
		else:
			args['initial'] = init
		args['choices'] = choices if choices != None else None
		attrDict = self._doAttrs(args, {'class': classStr, 'data-xp-val': xpVal})
		if multiple == True:
			attrDict['multiple'] = 'multiple'
		"""if not args.has_key('widget'):
			logger.debug( 'attrDict : ' + attrDict )
			args['widget'] = MultipleWidget(attrs=attrDict)"""
		args['widget'] = Widget(attrs=attrDict)
		# jsVal
		if args.has_key('jsVal'):
			for jsValidation in args['jsVal']:
				args['widget'].attrs['data-xp-val'] += ' ' + jsValidation
		# tabindex
		if args.has_key('tabindex'):
			args['widget'].attrs['tabindex'] = str(args['tabindex'])
		if args.has_key('val'):
			del args['val']
		if args.has_key('jsVal'):
			del args['jsVal']
		super(MultiField, self).__init__(**args)
