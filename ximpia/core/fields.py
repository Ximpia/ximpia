import json
import os
import datetime
import copy
from decimal import Decimal, DecimalException

from django.forms import Field as DjField, ChoiceField, MultipleChoiceField

from django.forms.widgets import Widget, CheckboxInput, DateInput, DateTimeInput, TimeInput

from django.forms.util import from_current_timezone, to_current_timezone
from django.core.exceptions import ValidationError
from django.utils import formats
from django.utils.encoding import smart_str, force_unicode
from django.utils.ipv6 import clean_ipv6_address
from django.utils.translation import ugettext_lazy as _
import django.core.validators

from ximpia.util.basic_types import DictUtil
from validators import validationMap

from choices import Choices as Ch

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
	def __init__(self, maxLength=None, required=True, init=None, **args):
		if not args.has_key('initial'):
			self.initial = ''
			args['initial'] = ''
		initValue = init if init != None else ''
		if self.instance:
			args['initial'] = eval('self.instance' + '.' + self.instanceFieldName) if self.instance != None else initValue
			self.initial = args['initial']
		args['required'] = required
		if self.instance:
			if not args.has_key('label'):
				args['label'] = self.instance._meta.get_field_by_name(self.instanceFieldName)[0].verbose_name.title()
			if not args.has_key('help_text'):
				args['help_text'] = self.instance._meta.get_field_by_name(self.instanceFieldName)[0].help_text.title()
		# val
		if args.has_key('val'):
			for valField in args['val']:
				args['validators'].append(valField)
		# jsVal : data-xp-val
		if args.has_key('jsVal'):
			for jsValidation in args['jsVal']:
				if jsValidation.strip() != 'required':
					#args['widget'].attrs['data-xp-val'] += ' ' + jsValidation
					self._updateAttrs(args['widget'].attrs, 'data-xp-val', jsValidation)
		# jsRequired
		if required == True and not args.has_key('jsRequired'):
			args['jsRequired'] = True
		if required == False and not args.has_key('jsRequired'):
			args['jsRequired'] = False
		if args.has_key('jsRequired'):
			if args['jsRequired'] == True:
				#args['widget'].attrs['data-xp-val'] += ' required'
				self._updateAttrs(args['widget'].attrs, 'data-xp-val', 'required')
		#logger.debug( 'attrs : ' + args['label'] + ' ' + args['widget'].attrs )
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
		if args.has_key('attrs'):
			del args['attrs']
		super(Field, self).__init__(**args)
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
	def _getMaxLength(self):
		"""Get max length from model"""
		fieldMaxLength = self.instance._meta.get_field_by_name(self.instanceFieldName)[0].max_length if self.instance else 0
		return fieldMaxLength
	def _doRequired(self, required, jsRequired):
		"""Process required and javascript required"""
		# True | None => True		
		# False | None => False
		if jsRequired == None:
			jsRequired = required
		t = (required, jsRequired)
		return t
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

	def widget_attrs(self, widget):
		"""
		Given a Widget instance (*not* a Widget class), returns a dictionary of
		any HTML attributes that should be added to the Widget, based on this
		Field.
		"""
		return {}

	def __deepcopy__(self, memo):
		result = copy.copy(self)
		memo[id(self)] = result
		result.widget = copy.deepcopy(self.widget, memo)
		result.validators = self.validators[:]
		return result

class CharField( Field ):
	"""
	CharField
	
	** Required Attributes **
	
	* ``instance``:object : Model instance
	* ``insField``:String : Model field
	* ``fieldFormat``:String : Form field format, from Choices.FORM_CHAR_TYPE
	
	** Optional Attributes **
	
	* ``minLength``:Integer : Minimum length
	* ``maxLength``:Integer : Maximum length
	* ``required``:Boolean : Required field by back-end form valdiation
	* ``init``:String : Initial value
	* ``jsRequired``:String	: Required field by javascript validation
	
	Plus the attributes for Field form class
	
	"""
	def __init__(self, instance, insField, fieldFormat=Ch.FORMAT_TYPE_CHAR, minLength=None, maxLength=None, 
				required=True, init='', jsRequired=None, **args):
		self._doInstanceInit(instance, insField)
		fieldMaxLength = self._getMaxLength()
		args['validators'] = validationMap[fieldFormat]
		args['max_length'] = maxLength if maxLength != None else fieldMaxLength
		args['min_length'] = minLength if minLength != None else None
		args['required'], args['jsRequired'] = self._doRequired(required, jsRequired) 
		classStr = 'fieldMust' if required == True else 'field'
		if required == False and jsRequired == True:
			classStr = 'fieldMust'
		attrs = self._doAttrs(args, {	'class': classStr,
										'maxlength': str(args['max_length'])
									})
		args['widget'] = Widget(attrs=attrs)
		super(CharField, self).__init__(**args)

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
	widget = CheckboxInput

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

class IPAddressField(CharField):
	default_error_messages = {
		'invalid': _(u'Enter a valid IPv4 address.'),
	}
	default_validators = [django.core.validators.validate_ipv4_address]


class GenericIPAddressField(CharField):
	default_error_messages = {}

	def __init__(self, protocol='both', unpackIpv4=False, *args, **kwargs):
		self.unpack_ipv4 = unpackIpv4
		self.default_validators, invalid_error_message = \
			django.core.validators.ip_address_validators(protocol, unpackIpv4)
		self.default_error_messages['invalid'] = invalid_error_message
		super(GenericIPAddressField, self).__init__(*args, **kwargs)

	def to_python(self, value):
		if value in django.core.validators.EMPTY_VALUES:
			return u''
		if value and ':' in value:
				return clean_ipv6_address(value,
					self.unpack_ipv4, self.error_messages['invalid'])
		return value

class DecimalField ( Field ):
	default_error_messages = {
		'invalid': _(u'Enter a number.'),
		'max_value': _(u'Ensure this value is less than or equal to %(limit_value)s.'),
		'min_value': _(u'Ensure this value is greater than or equal to %(limit_value)s.'),
		'max_digits': _('Ensure that there are no more than %s digits in total.'),
		'max_decimal_places': _('Ensure that there are no more than %s decimal places.'),
		'max_whole_digits': _('Ensure that there are no more than %s digits before the decimal point.')
	}

	def __init__(self, maxValue=None, minValue=None, maxDigits=None, decimalPlaces=None, *args, **kwargs):
		self.max_value, self.min_value = maxValue, minValue
		self.max_digits, self.decimal_places = maxDigits, decimalPlaces
		Field.__init__(self, *args, **kwargs)

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
		whole_digits = digits - decimals

		if self.max_digits is not None and digits > self.max_digits:
			raise ValidationError(self.error_messages['max_digits'] % self.max_digits)
		if self.decimal_places is not None and decimals > self.decimal_places:
			raise ValidationError(self.error_messages['max_decimal_places'] % self.decimal_places)
		if self.max_digits is not None and self.decimal_places is not None and whole_digits > (self.max_digits - self.decimal_places):
			raise ValidationError(self.error_messages['max_whole_digits'] % (self.max_digits - self.decimal_places))
		return value

class IntegerField ( Field ):
	default_error_messages = {
		'invalid': _(u'Enter a whole number.'),
		'max_value': _(u'Ensure this value is less than or equal to %(limit_value)s.'),
		'min_value': _(u'Ensure this value is greater than or equal to %(limit_value)s.'),
	}

	def __init__(self, maxValue=None, minValue=None, *args, **kwargs):
		self.max_value, self.min_value = maxValue, minValue
		super(IntegerField, self).__init__(*args, **kwargs)
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
	default_error_messages = {
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

	def __init__(self, input_formats=None, *args, **kwargs):
		super(_BaseTemporalField, self).__init__(*args, **kwargs)
		if input_formats is not None:
			self.input_formats = input_formats

	def to_python(self, value):
		# Try to coerce the value to unicode.
		unicode_value = force_unicode(value, strings_only=True)
		if isinstance(unicode_value, unicode):
			value = unicode_value.strip()
		# If unicode, try to strptime against each input format.
		if isinstance(value, unicode):
			for timeFormat in self.input_formats:
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
	widget = DateInput
	input_formats = formats.get_format_lazy('DATE_INPUT_FORMATS')
	default_error_messages = {
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
	widget = DateTimeInput
	input_formats = formats.get_format_lazy('DATETIME_INPUT_FORMATS')
	default_error_messages = {
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
	widget = TimeInput
	input_formats = formats.get_format_lazy('TIME_INPUT_FORMATS')
	default_error_messages = {
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

class HiddenDataField( Field ):
	"""Hidden Data Field
	
	Deprecated????
	
	"""
	def __init__(self, instance, insField, required=True, init=None, jsRequired=None, xpType='', **args):
		self._doInstanceInit(instance, insField)
		args['validators'] = []
		args['required'], args['jsRequired'] = self._doRequired(required, jsRequired)
		attrs = self._doAttrs(args, {	'xpType': xpType	})
		"""if not args.has_key('widget'):
			args['widget'] = HiddenWidget(attrs=attrDict)"""		
		args['widget'] = Widget(attrs=attrs)
		super(HiddenDataField, self).__init__(**args)

class HiddenField( Field ):
	"""
	Hidden Field, name and value, no xpType. 
	
	Analyze the way we include hidden fields to determine if we need this field.
	"""
	def __init__(self, required=True, init=None, jsRequired=None, xpType='', **args):
		args['validators'] = []
		args['required'], args['jsRequired'] = self._doRequired(required, jsRequired) 
		attrs = self._doAttrs(args, {'xpType': xpType})
		"""if not args.has_key('widget'):
			args['widget'] = HiddenWidget(attrs=attrDict)"""
		args['widget'] = Widget(attrs=attrs)
		super(HiddenField, self).__init__(**args)

@DeprecationWarning
class UserField( Field ):
	"""UserField""" 
	def __init__(self, instance, insField, minLength=None, maxLength=None, required=True, init=None, jsRequired=None, xpType='field', **args):
		self._doInstanceInit(instance, insField)
		fieldMaxLength = self._getMaxLength()
		#args['validators'] = [validateUserId]
		args['max_length'] = maxLength if maxLength != None else fieldMaxLength
		args['min_length'] = minLength if minLength != None else None
		args['required'], args['jsRequired'] = self._doRequired(required, jsRequired)
		classStr = 'fieldMust' if required == True else 'field'
		attrDict = self._doAttrs(args, {	'class': classStr,
							'data-xp-val': 'ximpiaId',
							'maxlength': str(args['max_length']),
							'xpType': xpType})
		"""if not args.has_key('widget'):
			args['widget'] = TextInputWidget(attrs=attrDict)"""
		args['widget'] = Widget(attrs=attrDict)
		super(UserField, self).__init__(**args)

@DeprecationWarning
class EmailField( Field ):
	"""EmailField"""
	def __init__(self, instance, insField, minLength=None, maxLength=None, required=True, init=None, jsRequired=None, xpType='field', **args):
		self._doInstanceInit(instance, insField)
		fieldMaxLength = self._getMaxLength()
		#args['validators'] = [validateEmail]
		args['max_length'] = maxLength if maxLength != None else fieldMaxLength
		args['min_length'] = minLength if minLength != None else None
		args['required'], args['jsRequired'] = self._doRequired(required, jsRequired)
		classStr = 'fieldMust' if required == True else 'field'
		attrDict = self._doAttrs(args, {	'class': classStr,
							'data-xp-val': 'email',
							'maxlength': str(args['max_length']),
							'xpType': xpType})
		"""if not args.has_key('widget'):
			args['widget'] = TextInputWidget(attrs=attrDict)"""
		args['widget'] = Widget(attrs=attrDict)
		super(EmailField, self).__init__(**args)

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


@DeprecationWarning
class PasswordField( Field ):
	"""PasswordField"""
	def __init__(self, instance, insField, minLength=None, maxLength=None, required=True, init=None, jsRequired=None, xpType='field', **args):
		self._doInstanceInit(instance, insField)
		fieldMaxLength = self._getMaxLength()
		#args['validators'] = [validatePassword]
		args['max_length'] = maxLength if maxLength != None else fieldMaxLength
		args['min_length'] = minLength if minLength != None else None
		args['required'], args['jsRequired'] = self._doRequired(required, jsRequired)
		classStr = 'fieldMust' if required == True else 'field'
		attrDict = self._doAttrs(args, {	'class': classStr,
							'autocomplete': 'no',
							'data-xp-val': 'password',
							'maxlength': str(args['max_length']),
							'xpType': xpType})
		"""if not args.has_key('widget'):
			args['widget'] = PasswordWidget(attrs=attrDict)"""
		args['widget'] = Widget(attrs=attrDict)
		super(PasswordField, self).__init__(**args)

class ListField( Field ):
	"""
	Select field. Will render to combobox, option lists, autocomplete, etc... when form instance is rendered, values are
	fetched from database to fill ``id_choices``hidden field with data for field values.
	
	** Required Attributes **
	
	* ``instance``:Object : Model instance
	* ``insField``:String : Model field, like '_myModel.fieldName'
	* ``choicesId``:String: Choice id to save into id_choices hidden field, like {myChoiceId: [(name1,value1),(name2,value2),...] ... }
	
	** Optional Attributes **
	
	* ``limitTo``:Dict : Dictionary with attributes sent to model filter method
	* ``listName``:String : Model field to use for name in (name, value) pairs. By default, pk is used.
	* ``listValue``:String : Model field to be used for value in (name, value) pairs. By default, string notation of model used.
	
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
		super(ListField, self).__init__(**args)

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
