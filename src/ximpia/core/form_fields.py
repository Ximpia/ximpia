from django.forms.widgets import Widget
from django.forms import Field, ChoiceField, MultipleChoiceField, CharField
from django.forms.util import flatatt
from django.utils import formats
from django.utils.html import escape, conditional_escape
from itertools import chain
from django.utils.safestring import mark_safe
from django.utils.datastructures import MultiValueDict, MergeDict
from django.utils.encoding import force_unicode
import json

from ximpia.settings_visual import SocialNetworkIconData as SocialNetwork
from ximpia.util.basic_types import DictUtil
from validators import validateUserId, validateEmail, validateTxtField, validatePassword

from form_widgets import XpHiddenWidget, XpInputWidget, XpMultipleHiddenWidget, XpMultipleWidget, XpPasswordWidget, XpSelectWidget 
from form_widgets import XpTextareaWidget, XpTextInputWidget


class XpSocialIconField(Field):
	def __init__(self, network=None, version=None, *argsTuple, **argsDict):
		argsDict['widget'] = XpHiddenWidget()
		argsDict['required'] = False
		argsDict['initial'] = SocialNetwork(network, version).getS()
		super(XpSocialIconField, self).__init__(*argsTuple, **argsDict)

class XpBaseCharField(CharField):
	instance = None
	initial = ''
	instanceName = ''
	instanceFieldName = ''
	def __init__(self, max=None, req=True, init=None, **argsDict):		
		initValue = init if init != None else ''
		if self.instance:
			argsDict['initial'] = eval('self.instance' + '.' + self.instanceFieldName) if self.instance != None else initValue
			self.initial = argsDict['initial']
		argsDict['required'] = req
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
		if req == True and not argsDict.has_key('jsReq'):
			argsDict['jsReq'] = True
		if req == False and not argsDict.has_key('jsReq'):
			argsDict['jsReq'] = False
		if argsDict.has_key('jsReq'):
			if argsDict['jsReq'] == True:
				#argsDict['widget'].attrs['data-xp-val'] += ' required'
				self._updateAttrs(argsDict['widget'].attrs, 'data-xp-val', 'required')
		#print 'attrs : ', argsDict['label'], argsDict['widget'].attrs
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
	def _updateAttrs(self, dict, key, value):
		"""Update attrs dictionary"""
		if dict.has_key(key):
			dict[key] += ' ' + value
		else:
			dict[key] = value
	def _getMaxLength(self):
		"""Get max length from model"""
		fieldMaxLength = self.instance._meta.get_field_by_name(self.instanceFieldName)[0].max_length if self.instance else max
		return fieldMaxLength
	def _doRequired(self, req, jsReq):
		"""Process required and javascript required"""
		# True | None => True		
		# False | None => False
		if jsReq == None:
			jsReq = req
		tuple = (req, jsReq)
		return tuple
	def _doAttrs(self, argsDict, attrDict):
		"""Process form attrs with field attribute dictionary for widget
		@param argsDict: 
		@param attrDict: 
		@return: dict"""
		dict = {}
		if argsDict.has_key('attrs'):
			dict = DictUtil.addDicts([argsDict['attrs'], attrDict])
		else:
			dict = attrDict
		return dict

class XpCharField(XpBaseCharField):
	"""CharField"""
	def __init__(self, instance, insField, min=None, max=None, req=True, init=None, jsReq=None, xpType='basic.text', **argsDict):
		self._doInstanceInit(instance, insField)
		fieldMaxLength = self._getMaxLength()
		argsDict['validators'] = [validateTxtField]
		argsDict['max_length'] = max if max != None else fieldMaxLength
		argsDict['min_length'] = min if min != None else None
		argsDict['req'], argsDict['jsReq'] = self._doRequired(req, jsReq) 
		classStr = 'fieldMust' if req == True else 'field'
		attrDict = self._doAttrs(argsDict, {	'class': classStr,
							'maxlength': str(argsDict['max_length']),
							'xpType': xpType})
		
		if not argsDict.has_key('widget'):
			argsDict['widget'] = XpTextInputWidget(attrs=attrDict)
		super(XpCharField, self).__init__(**argsDict)

class XpHiddenField(XpBaseCharField):
	"""Hidden Field"""
	def __init__(self, req=True, init=None, jsReq=None, xpType='', **argsDict):
		argsDict['validators'] = []
		argsDict['req'], argsDict['jsReq'] = self._doRequired(req, jsReq) 
		attrDict = self._doAttrs(argsDict, {'xpType': xpType})
		if not argsDict.has_key('widget'):
			argsDict['widget'] = XpHiddenWidget(attrs=attrDict)
		super(XpHiddenField, self).__init__(**argsDict)

class XpUserField(XpBaseCharField):
	"""UserField""" 
	def __init__(self, instance, insField, min=None, max=None, req=True, init=None, jsReq=None, xpType='basic.text', **argsDict):
		self._doInstanceInit(instance, insField)
		fieldMaxLength = self._getMaxLength()
		argsDict['validators'] = [validateUserId]
		argsDict['max_length'] = max if max != None else fieldMaxLength
		argsDict['min_length'] = min if min != None else None
		argsDict['req'], argsDict['jsReq'] = self._doRequired(req, jsReq)
		classStr = 'fieldMust' if req == True else 'field'
		attrDict = self._doAttrs(argsDict, {	'class': classStr,
							'data-xp-val': 'ximpiaId',
							'maxlength': str(argsDict['max_length']),
							'xpType': xpType})
		if not argsDict.has_key('widget'):
			argsDict['widget'] = XpTextInputWidget(attrs=attrDict)
		super(XpUserField, self).__init__(**argsDict)

class XpEmailField(XpBaseCharField):
	"""EmailField"""
	def __init__(self, instance, insField, min=None, max=None, req=True, init=None, jsReq=None, xpType='basic.text', **argsDict):
		self._doInstanceInit(instance, insField)
		fieldMaxLength = self._getMaxLength()
		argsDict['validators'] = [validateEmail]
		argsDict['max_length'] = max if max != None else fieldMaxLength
		argsDict['min_length'] = min if min != None else None
		argsDict['req'], argsDict['jsReq'] = self._doRequired(req, jsReq)
		classStr = 'fieldMust' if req == True else 'field'
		attrDict = self._doAttrs(argsDict, {	'class': classStr,
							'data-xp-val': 'email',
							'maxlength': str(argsDict['max_length']),
							'xpType': xpType})
		if not argsDict.has_key('widget'):
			argsDict['widget'] = XpTextInputWidget(attrs=attrDict)
		super(XpEmailField, self).__init__(**argsDict)

class XpChoiceTextField(XpBaseCharField):
	"""Choice field with autocompletion. Behaves like a select, with name and value"""
	def __init__(self, instance, insField, min=None, max=None, req=True, init=None, jsReq=None, maxHeight=200, minCharacters=3, 
			choices=(), dbClass='', params={}, xpType='list.select', **argsDict):
		self._doInstanceInit(instance, insField)
		fieldMaxLength = self._getMaxLength()
		argsDict['validators'] = []
		argsDict['max_length'] = max if max != None else fieldMaxLength
		argsDict['min_length'] = min if min != None else None
		argsDict['req'], argsDict['jsReq'] = self._doRequired(req, jsReq)
		classStr = 'fieldMust' if req == True else 'field'
		attrDict = self._doAttrs(argsDict, {	'class': classStr,
							'maxlength': str(argsDict['max_length']),
							'xpType': xpType})
		#data, maxHeight, minCharacters, url
		#$('#id_jobTitle').jsonSuggest({data: $('#id_jobTitle_data').attr('value'), maxHeight: 200, minCharacters:3});
		#dict = {'id': tupleData[0], 'text': tupleData[1]}
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

class XpTextChoiceField(XpBaseCharField):
	"""Text Choice Field. Field with autocompletion"""
	def __init__(self, instance, insField, min=None, max=None, req=True, init=None, jsReq=None, maxHeight=200, minCharacters=3, 
			choicesId='', dbClass='', params={}, xpType='basic.text', **argsDict):
		self._doInstanceInit(instance, insField)
		fieldMaxLength = self._getMaxLength()
		argsDict['validators'] = []
		argsDict['max_length'] = max if max != None else fieldMaxLength
		argsDict['min_length'] = min if min != None else None
		argsDict['req'], argsDict['jsReq'] = self._doRequired(req, jsReq)
		classStr = 'fieldMust' if req == True else 'field'
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


class XpPasswordField(XpBaseCharField):
	"""PasswordField"""
	def __init__(self, instance, insField, min=None, max=None, req=True, init=None, jsReq=None, xpType='basic.text', **argsDict):
		self._doInstanceInit(instance, insField)
		fieldMaxLength = self._getMaxLength()
		argsDict['validators'] = [validatePassword]
		argsDict['max_length'] = max if max != None else fieldMaxLength
		argsDict['min_length'] = min if min != None else None
		argsDict['req'], argsDict['jsReq'] = self._doRequired(req, jsReq)
		classStr = 'fieldMust' if req == True else 'field'
		attrDict = self._doAttrs(argsDict, {	'class': classStr,
							'autocomplete': 'no',
							'data-xp-val': 'password',
							'maxlength': str(argsDict['max_length']),
							'xpType': xpType})
		if not argsDict.has_key('widget'):
			argsDict['widget'] = XpPasswordWidget(attrs=attrDict)
		super(XpPasswordField, self).__init__(**argsDict)

class XpChoiceField(ChoiceField):
	"""ChoiceField"""
	def _doAttrs(self, argsDict, attrDict):
		"""Process form attrs with field attribute dictionary for widget
		@param argsDict: 
		@param attrDict: 
		@return: dict"""
		dict = {}
		if argsDict.has_key('attrs'):
			dict = DictUtil.addDicts([argsDict['attrs'], attrDict])
		else:
			dict = attrDict
		return dict
	def __init__(self, instance, insField, req=True, init='', choicesId='', xpType='list.select', **argsDict):
		if insField.find('.') != -1:
			instanceName, instanceFieldName = insField.split('.')
			self.instanceName = instanceName
			self.instanceFieldName = instanceFieldName
			self.instance = instance
		classStr = 'fieldMust' if req == True else 'field'
		xpVal = 'required' if req == True else ''
		argsDict['required'] = req
		if instance != None:
			if not argsDict.has_key('label'):
				argsDict['label'] = instance._meta.get_field_by_name(self.instanceFieldName)[0].verbose_name if instance else argsDict['label']
			if not argsDict.has_key('help_text'):
				argsDict['help_text'] = instance._meta.get_field_by_name(self.instanceFieldName)[0].help_text if instance else argsDict['help_text']
			argsDict['initial'] = init if init != '' else eval('instance' + '.' + self.instanceFieldName)
		#argsDict['choices'] = choices if choices != None else None		
		#argsDict['choicesId'] = choicesId if choicesId != '' else ''
		#print 'choicesId : ', choicesId
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

class XpMultiField(MultipleChoiceField):
	"""Cimpia Multiple Choice Field"""
	def _doAttrs(self, argsDict, attrDict):
		"""Process form attrs with field attribute dictionary for widget
		@param argsDict: 
		@param attrDict: 
		@return: dict"""
		dict = {}
		if argsDict.has_key('attrs'):
			dict = DictUtil.addDicts([argsDict['attrs'], attrDict])
		else:
			dict = attrDict
		return dict
	def __init__(self, instance, insField, req=True, init=[], choices=None, multiple=False, **argsDict):
		if insField.find('.') != -1:
			instanceName, instanceFieldName = insField.split('.')
			self.instanceName = instanceName
			self.instanceFieldName = instanceFieldName
			self.instance = instance
		classStr = 'fieldMust' if req == True else 'field'
		xpVal = 'required' if req == True else ''
		#classStr = 'SmallMust' if req == True else 'Small'
		argsDict['required'] = req
		if instance:
			if not argsDict.has_key('label'):
				argsDict['label'] = instance._meta.get_field_by_name(self.instanceFieldName)[0].verbose_name
			if not argsDict.has_key('help_text'):
				argsDict['help_text'] = instance._meta.get_field_by_name(self.instanceFieldName)[0].help_text		
		if len(init) == 0 and instance:
			listRaw = eval('instance' + '.' + self.instanceFieldName + '.all()')
			list = []
			for obj in listRaw:
				list.append(obj.pk)
			argsDict['initial'] = list
		else:
			argsDict['initial'] = init
		argsDict['choices'] = choices if choices != None else None
		attrDict = self._doAttrs(argsDict, {'class': classStr, 'data-xp-val': xpVal})
		if multiple == True:
			attrDict['multiple'] = 'multiple'
		if not argsDict.has_key('widget'):
			print 'attrDict : ', attrDict
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
