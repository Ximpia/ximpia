from django.forms import Field, ChoiceField, MultipleChoiceField, CharField
import json

#from ximpia.settings_visual import SocialNetworkIconData as SocialNetwork
from ximpia.util.basic_types import DictUtil
from validators import validateUserId, validateEmail, validateTxtField, validatePassword

from form_widgets import XpHiddenWidget, XpMultipleWidget, XpPasswordWidget, XpSelectWidget, XpTextInputWidget, XpOptionWidget, XpCheckboxWidget 

from ximpia import settings

# Logging
import logging.config
logging.config.dictConfig(settings.LOGGING)
logger = logging.getLogger(__name__)

"""class XpSocialIconField( Field ):
	def __init__(self, network=None, version=None, *argsTuple, **argsDict):
		argsDict['widget'] = XpHiddenWidget()
		argsDict['required'] = False
		argsDict['initial'] = SocialNetwork(network, version).getS()
		super(XpSocialIconField, self).__init__(*argsTuple, **argsDict)"""

class XpBaseCharField( CharField ):
	instance = None
	initial = ''
	instanceName = ''
	instanceFieldName = ''
	def __init__(self, maxValue=None, required=True, init=None, **argsDict):
		if not argsDict.has_key('initial'):
			self.initial = ''
			argsDict['initial'] = ''
		initValue = init if init != None else ''
		if self.instance:
			argsDict['initial'] = eval('self.instance' + '.' + self.instanceFieldName) if self.instance != None else initValue
			self.initial = argsDict['initial']
		argsDict['required'] = required
		if self.instance:
			if not argsDict.has_key('label'):
				argsDict['label'] = self.instance._meta.get_field_by_name(self.instanceFieldName)[0].verbose_name.title()
			if not argsDict.has_key('help_text'):
				argsDict['help_text'] = self.instance._meta.get_field_by_name(self.instanceFieldName)[0].help_text.title()
		# val
		if argsDict.has_key('val'):
			for valField in argsDict['val']:
				argsDict['validators'].append(valField)
		# jsVal : data-xp-val
		if argsDict.has_key('jsVal'):
			for jsValidation in argsDict['jsVal']:
				if jsValidation.strip() != 'required':
					#argsDict['widget'].attrs['data-xp-val'] += ' ' + jsValidation
					self._updateAttrs(argsDict['widget'].attrs, 'data-xp-val', jsValidation)
		# jsReq
		if required == True and not argsDict.has_key('jsReq'):
			argsDict['jsReq'] = True
		if required == False and not argsDict.has_key('jsReq'):
			argsDict['jsReq'] = False
		if argsDict.has_key('jsReq'):
			if argsDict['jsReq'] == True:
				#argsDict['widget'].attrs['data-xp-val'] += ' required'
				self._updateAttrs(argsDict['widget'].attrs, 'data-xp-val', 'required')
		#logger.debug( 'attrs : ' + argsDict['label'] + ' ' + argsDict['widget'].attrs )
		# tabindex
		if argsDict.has_key('tabindex'):
			argsDict['widget'].attrs['tabindex'] = str(argsDict['tabindex'])
		if argsDict.has_key('val'):
			del argsDict['val']
		if argsDict.has_key('jsVal'):
			del argsDict['jsVal']
		if argsDict.has_key('jsReq'):
			del argsDict['jsReq']
		if argsDict.has_key('tabindex'):
			del argsDict['tabindex']
		if argsDict.has_key('attrs'):
			del argsDict['attrs']
		super(XpBaseCharField, self).__init__(**argsDict)
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
	def _doRequired(self, required, jsReq):
		"""Process required and javascript required"""
		# True | None => True		
		# False | None => False
		if jsReq == None:
			jsReq = required
		t = (required, jsReq)
		return t
	def _doAttrs(self, argsDict, attrDict):
		"""Process form attrs with field attribute dictionary for widget
		@param argsDict: 
		@param attrDict: 
		@return: dict"""
		d = {}
		if argsDict.has_key('attrs'):
			d = DictUtil.addDicts([argsDict['attrs'], attrDict])
		else:
			d = attrDict
		return d

class XpCharField( XpBaseCharField ):
	"""CharField"""
	def __init__(self, instance, insField, minValue=None, maxValue=None, required=True, init='', jsReq=None, xpType='basic.text', **argsDict):
		self._doInstanceInit(instance, insField)
		fieldMaxLength = self._getMaxLength()
		argsDict['validators'] = [validateTxtField]
		argsDict['max_length'] = maxValue if maxValue != None else fieldMaxLength
		argsDict['min_length'] = minValue if minValue != None else None
		argsDict['required'], argsDict['jsReq'] = self._doRequired(required, jsReq) 
		classStr = 'fieldMust' if required == True else 'field'
		attrDict = self._doAttrs(argsDict, {	'class': classStr,
							'maxlength': str(argsDict['max_length']),
							'xpType': xpType})
		if not argsDict.has_key('widget'):
			argsDict['widget'] = XpTextInputWidget(attrs=attrDict) 
		super(XpCharField, self).__init__(**argsDict)

"""
Example: Months

option
======
form.month variable
model: jan
choices: ('jan','January')...
<label><input type="radio" name="month" value="jan" selected /> January</label> (Comes from choices table)
<label><input type="radio" name="month" value="feb"  /> February</label>
XpOptionChoiceField

checkbox
========
form.month variable
model: ['jan','feb'] 255 bytes, separated by comma. '' => [] .. 'jan' => ['jan'] .. 'jan,feb' => ['jan','feb']
<label><input type="checkbox" name="month" value="jan" checked /> January</label> (Comes from choices table)
<label><input type="checkbox" name="month" value="feb" /> February</label>
XpCheckboxChoiceField

checkbox no choices
===================
form.client variable
model: Many to many field
<label><input type="checkbox" name="client" value="$id" checked /> Client A</label> (comes from string representation of model)
<label><input type="checkbox" name="client" value="$id" checked /> Client B</label>
XpCheckboxField => (pk, str)...
"""

class XpOptionChoiceField( XpBaseCharField ):
	"""Option Group Field. Labels and values comes from the choices list."""
	def __init__(self, instance, insField, xpType='input.option', choicesId='', **argsDict):
		self._doInstanceInit(instance, insField)
		attrDict = self._doAttrs(argsDict, {	'choicesId': choicesId,	
							'xpType': xpType	})
		#if not argsDict.has_key('widget'):
		argsDict['widget'] = XpOptionWidget(attrs=attrDict)
		super(XpOptionChoiceField, self).__init__(**argsDict)

class XpCheckboxChoiceField( XpBaseCharField ):
	"""Checkbox Group Field. Labels and values comes from the choices list."""
	def __init__(self, instance, insField, xpType='input.checkbox', choicesId='', **argsDict):
		self._doInstanceInit(instance, insField)
		attrDict = self._doAttrs(argsDict, {	'choicesId': choicesId,	
							'xpType': xpType	})
		#if not argsDict.has_key('widget'):
		argsDict['widget'] = XpCheckboxWidget(attrs=attrDict)
		super(XpCheckboxChoiceField, self).__init__(**argsDict)

class XpHiddenDataField( XpBaseCharField ):
	"""Hidden Field"""
	def __init__(self, instance, insField, required=True, init=None, jsReq=None, xpType='', **argsDict):
		self._doInstanceInit(instance, insField)
		argsDict['validators'] = []
		argsDict['required'], argsDict['jsReq'] = self._doRequired(required, jsReq)
		attrDict = self._doAttrs(argsDict, {	'xpType': xpType	})
		if not argsDict.has_key('widget'):
			argsDict['widget'] = XpHiddenWidget(attrs=attrDict)
		super(XpHiddenDataField, self).__init__(**argsDict)

class XpHiddenField( XpBaseCharField ):
	"""Hidden Field"""
	def __init__(self, required=True, init=None, jsReq=None, xpType='', **argsDict):
		argsDict['validators'] = []
		argsDict['required'], argsDict['jsReq'] = self._doRequired(required, jsReq) 
		attrDict = self._doAttrs(argsDict, {'xpType': xpType})
		if not argsDict.has_key('widget'):
			argsDict['widget'] = XpHiddenWidget(attrs=attrDict)
		super(XpHiddenField, self).__init__(**argsDict)

class XpUserField( XpBaseCharField ):
	"""UserField""" 
	def __init__(self, instance, insField, minValue=None, maxValue=None, required=True, init=None, jsReq=None, xpType='basic.text', **argsDict):
		self._doInstanceInit(instance, insField)
		fieldMaxLength = self._getMaxLength()
		argsDict['validators'] = [validateUserId]
		argsDict['max_length'] = maxValue if maxValue != None else fieldMaxLength
		argsDict['min_length'] = minValue if minValue != None else None
		argsDict['required'], argsDict['jsReq'] = self._doRequired(required, jsReq)
		classStr = 'fieldMust' if required == True else 'field'
		attrDict = self._doAttrs(argsDict, {	'class': classStr,
							'data-xp-val': 'ximpiaId',
							'maxlength': str(argsDict['max_length']),
							'xpType': xpType})
		if not argsDict.has_key('widget'):
			argsDict['widget'] = XpTextInputWidget(attrs=attrDict)
		super(XpUserField, self).__init__(**argsDict)

class XpEmailField( XpBaseCharField ):
	"""EmailField"""
	def __init__(self, instance, insField, minValue=None, maxValue=None, required=True, init=None, jsReq=None, xpType='basic.text', **argsDict):
		self._doInstanceInit(instance, insField)
		fieldMaxLength = self._getMaxLength()
		argsDict['validators'] = [validateEmail]
		argsDict['max_length'] = maxValue if maxValue != None else fieldMaxLength
		argsDict['min_length'] = minValue if minValue != None else None
		argsDict['required'], argsDict['jsReq'] = self._doRequired(required, jsReq)
		classStr = 'fieldMust' if required == True else 'field'
		attrDict = self._doAttrs(argsDict, {	'class': classStr,
							'data-xp-val': 'email',
							'maxlength': str(argsDict['max_length']),
							'xpType': xpType})
		if not argsDict.has_key('widget'):
			argsDict['widget'] = XpTextInputWidget(attrs=attrDict)
		super(XpEmailField, self).__init__(**argsDict)

class XpChoiceTextField( XpBaseCharField ):
	"""Choice field with autocompletion. Behaves like a select, with name and value"""
	def __init__(self, instance, insField, minValue=None, maxValue=None, required=True, init=None, jsReq=None, maxHeight=200, minCharacters=3, 
			choices=(), dbClass='', params={}, xpType='list.select', **argsDict):
		self._doInstanceInit(instance, insField)
		fieldMaxLength = self._getMaxLength()
		argsDict['validators'] = []
		argsDict['max_length'] = maxValue if maxValue != None else fieldMaxLength
		argsDict['min_length'] = minValue if minValue != None else None
		argsDict['required'], argsDict['jsReq'] = self._doRequired(required, jsReq)
		classStr = 'fieldMust' if required == True else 'field'
		attrDict = self._doAttrs(argsDict, {	'class': classStr,
							'maxlength': str(argsDict['max_length']),
							'xpType': xpType})
		#data, maxHeight, minCharacters, url
		#$('#id_jobTitle').jsonSuggest({data: $('#id_jobTitle_data').attr('value'), maxHeight: 200, minCharacters:3});
		#d = {'id': tupleData[0], 'text': tupleData[1]}
		"""suggestList = []
		for tuple in choices:
			suggestList.append({'id': tuple[0], 'text': tuple[1]})"""
		attrDict['data-xp'] = {	'maxHeight': maxHeight,
					'minCharacters' : minCharacters
					}
		"""if len(choices) != 0:
			attrDict['data-xp']['data'] = suggestList"""
		"""if dbClass != '' and len(params) != 0:
			attrDict['data-xp']['url'] = '/jxSuggestList?dbClass=' + dbClass + ';params=' + json.dumps(params)""" 
		if not argsDict.has_key('widget'):
			argsDict['widget'] = XpTextInputWidget(attrs=attrDict)
		super(XpChoiceTextField, self).__init__(**argsDict)

class XpTextChoiceField( XpBaseCharField  ):
	"""Text Choice Field. Field with autocompletion"""
	def __init__(self, instance, insField, minValue=None, maxValue=None, required=True, init=None, jsReq=None, maxHeight=200, minCharacters=3, 
			choicesId='', dbClass='', params={}, xpType='basic.text', **argsDict):
		self._doInstanceInit(instance, insField)
		fieldMaxLength = self._getMaxLength()
		argsDict['validators'] = []
		argsDict['max_length'] = maxValue if maxValue != None else fieldMaxLength
		argsDict['min_length'] = minValue if minValue != None else None
		argsDict['required'], argsDict['jsReq'] = self._doRequired(required, jsReq)
		classStr = 'fieldMust' if required == True else 'field'
		attrDict = self._doAttrs(argsDict, {	'class': classStr,
							'maxlength': str(argsDict['max_length']),
							'choicesId': choicesId,
							'xpType': xpType})
		attrDict['data-xp'] = {	'maxHeight': maxHeight,
					'minCharacters' : minCharacters
					}
		if dbClass != '' and len(params) != 0:
			attrDict['data-xp']['url'] = '/jxSuggestList?dbClass=' + dbClass + ';params=' + json.dumps(params) 
		if not argsDict.has_key('widget'):
			argsDict['widget'] = XpTextInputWidget(attrs=attrDict)
		super(XpTextChoiceField, self).__init__(**argsDict)


class XpPasswordField( XpBaseCharField ):
	"""PasswordField"""
	def __init__(self, instance, insField, minValue=None, maxValue=None, required=True, init=None, jsReq=None, xpType='basic.text', **argsDict):
		self._doInstanceInit(instance, insField)
		fieldMaxLength = self._getMaxLength()
		argsDict['validators'] = [validatePassword]
		argsDict['max_length'] = maxValue if maxValue != None else fieldMaxLength
		argsDict['min_length'] = minValue if minValue != None else None
		argsDict['required'], argsDict['jsReq'] = self._doRequired(required, jsReq)
		classStr = 'fieldMust' if required == True else 'field'
		attrDict = self._doAttrs(argsDict, {	'class': classStr,
							'autocomplete': 'no',
							'data-xp-val': 'password',
							'maxlength': str(argsDict['max_length']),
							'xpType': xpType})
		if not argsDict.has_key('widget'):
			argsDict['widget'] = XpPasswordWidget(attrs=attrDict)
		super(XpPasswordField, self).__init__(**argsDict)

class XpChoiceField( ChoiceField ):
	"""ChoiceField"""
	def _doAttrs(self, argsDict, attrDict):
		"""Process form attrs with field attribute dictionary for widget
		@param argsDict: 
		@param attrDict: 
		@return: dict"""
		d = {}
		if argsDict.has_key('attrs'):
			d = DictUtil.addDicts([argsDict['attrs'], attrDict])
		else:
			d = attrDict
		return d
	def __init__(self, instance, insField, required=True, init='', choicesId='', xpType='list.select', **argsDict):
		if insField.find('.') != -1:
			instanceName, instanceFieldName = insField.split('.')
			self.instanceName = instanceName
			self.instanceFieldName = instanceFieldName
			self.instance = instance
		classStr = 'fieldMust' if required == True else 'field'
		xpVal = 'required' if required == True else ''
		argsDict['required'] = required
		if instance != None:
			if not argsDict.has_key('label'):
				argsDict['label'] = instance._meta.get_field_by_name(self.instanceFieldName)[0].verbose_name if instance else argsDict['label']
			if not argsDict.has_key('help_text'):
				argsDict['help_text'] = instance._meta.get_field_by_name(self.instanceFieldName)[0].help_text if instance else argsDict['help_text']
			argsDict['initial'] = init if init != '' else eval('instance' + '.' + self.instanceFieldName)
		#argsDict['choices'] = choices if choices != None else None
		#argsDict['choicesId'] = choicesId if choicesId != '' else ''
		#logger.debug( 'choicesId : ' + choicesId )
		attrDict = self._doAttrs(argsDict, {	'class': classStr,
							'data-xp-val': xpVal,
							'choicesId': choicesId,
							'xpType': xpType})
		if not argsDict.has_key('widget'):
			argsDict['widget'] = XpSelectWidget(attrs=attrDict)
		# tabindex
		if argsDict.has_key('tabindex'):
			argsDict['widget'].attrs['tabindex'] = str(argsDict['tabindex'])
		if argsDict.has_key('val'):
			del argsDict['val']
		if argsDict.has_key('jsVal'):
			del argsDict['jsVal']
		if argsDict.has_key('jsReq'):
			del argsDict['jsReq']
		if argsDict.has_key('tabindex'):
			del argsDict['tabindex']
		super(XpChoiceField, self).__init__(**argsDict)

class XpMultiField( MultipleChoiceField ):
	"""Cimpia Multiple Choice Field"""
	def _doAttrs(self, argsDict, attrDict):
		"""Process form attrs with field attribute dictionary for widget
		@param argsDict: 
		@param attrDict: 
		@return: dict"""
		d = {}
		if argsDict.has_key('attrs'):
			d = DictUtil.addDicts([argsDict['attrs'], attrDict])
		else:
			d = attrDict
		return d
	def __init__(self, instance, insField, required=True, init=[], choices=None, multiple=False, **argsDict):
		if insField.find('.') != -1:
			instanceName, instanceFieldName = insField.split('.')
			self.instanceName = instanceName
			self.instanceFieldName = instanceFieldName
			self.instance = instance
		classStr = 'fieldMust' if required == True else 'field'
		xpVal = 'required' if required == True else ''
		#classStr = 'SmallMust' if required == True else 'Small'
		argsDict['required'] = required
		if instance:
			if not argsDict.has_key('label'):
				argsDict['label'] = instance._meta.get_field_by_name(self.instanceFieldName)[0].verbose_name
			if not argsDict.has_key('help_text'):
				argsDict['help_text'] = instance._meta.get_field_by_name(self.instanceFieldName)[0].help_text		
		if len(init) == 0 and instance:
			listRaw = eval('instance' + '.' + self.instanceFieldName + '.all()')
			l = []
			for obj in listRaw:
				l.append(obj.pk)
			argsDict['initial'] = l
		else:
			argsDict['initial'] = init
		argsDict['choices'] = choices if choices != None else None
		attrDict = self._doAttrs(argsDict, {'class': classStr, 'data-xp-val': xpVal})
		if multiple == True:
			attrDict['multiple'] = 'multiple'
		if not argsDict.has_key('widget'):
			logger.debug( 'attrDict : ' + attrDict )
			argsDict['widget'] = XpMultipleWidget(attrs=attrDict)
		# jsVal
		if argsDict.has_key('jsVal'):
			for jsValidation in argsDict['jsVal']:
				argsDict['widget'].attrs['data-xp-val'] += ' ' + jsValidation
		# tabindex
		if argsDict.has_key('tabindex'):
			argsDict['widget'].attrs['tabindex'] = str(argsDict['tabindex'])
		if argsDict.has_key('val'):
			del argsDict['val']
		if argsDict.has_key('jsVal'):
			del argsDict['jsVal']
		super(XpMultiField, self).__init__(**argsDict)
