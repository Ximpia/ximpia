from django.forms.widgets import Widget
from django.forms import Field, ChoiceField, MultipleChoiceField, CharField
from django.forms.util import flatatt
from django.utils import formats
from django.utils.html import escape, conditional_escape
from itertools import chain
from django.utils.safestring import mark_safe
from django.utils.datastructures import MultiValueDict, MergeDict
from django.utils.encoding import force_unicode

from ximpia.settings_visual import SocialNetworkIconData as SocialNetwork

from validators import validateUserId, validateEmail, validateTxtField, validatePassword 

# =====================================================================================
# =================================== W I D G E T S ===================================
# =====================================================================================

class XpInputWidget(Widget):
	"""
	Base class for all <input> widgets (except type='checkbox' and
	type='radio', which are special).
	"""
	input_type = None # Subclasses must define this.
	show_info = False
	hasInfo = False
	def __init__(self, attrs={}, hasInfo = False):
		super(XpInputWidget, self).__init__(attrs)
		self.hasInfo = hasInfo
	def _format_value(self, value):
		if self.is_localized:
			return formats.localize_input(value)
		return value
	def render(self, name, value, attrs={}):
		if value is None:
			value = ''
		final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
		if value != '':
			# Only add the 'value' attribute if a value is non-empty.
			final_attrs['value'] = force_unicode(self._format_value(value))
		html = mark_safe(u'<input%s />' % flatatt(final_attrs))
		if self.hasInfo == True:
			html += mark_safe(u' <img id="id_img_' + name + '" src="/site_media/images/blank.png" class="ImgInfo" />')
		return html

class XpTextInputWidget(XpInputWidget):
	input_type = 'text'
	def __init__(self, attrs=None, hasInfo=False):
		super(XpTextInputWidget, self).__init__(attrs, hasInfo)

class XpHiddenWidget(XpInputWidget):
	input_type = 'hidden'
	is_hidden = True

class XpMultipleHiddenWidget(XpHiddenWidget):
	"""
	A widget that handles <input type="hidden"> for fields that have a list
	of values.
	"""
	def __init__(self, attrs=None, choices=()):
		super(XpMultipleHiddenWidget, self).__init__(attrs)
		# choices can be any iterable
		self.choices = choices
	def render(self, name, value, attrs=None, choices=()):
		if value is None: value = []
		final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
		id_ = final_attrs.get('id', None)
		inputs = []
		for i, v in enumerate(value):
			input_attrs = dict(value=force_unicode(v), **final_attrs)
			if id_:
				# An ID attribute was given. Add a numeric index as a suffix
				# so that the inputs don't all have the same ID attribute.
				input_attrs['id'] = '%s_%s' % (id_, i)
			inputs.append(u'<input%s />' % flatatt(input_attrs))
		return mark_safe(u'\n'.join(inputs))
	def value_from_datadict(self, data, files, name):
		if isinstance(data, (MultiValueDict, MergeDict)):
			return data.getlist(name)
		return data.get(name, None)

class XpPasswordWidget(XpInputWidget):
	input_type = 'password'
	def __init__(self, attrs=None, render_value=True, hasInfo=False):
		super(XpPasswordWidget, self).__init__(attrs, hasInfo)
		self.render_value = render_value
	def render(self, name, value, attrs=None):
		if not self.render_value: value=None
		return super(XpPasswordWidget, self).render(name, value, attrs)

class XpTextareaWidget(Widget):
	def __init__(self, attrs=None):
		# The 'rows' and 'cols' attributes are required for HTML correctness.
		super(XpTextareaWidget, self).__init__(attrs)
		default_attrs = {'cols': '40', 'rows': '10'}
		if attrs:
			default_attrs.update(attrs)
		#super(Textarea, self).__init__(default_attrs)
	def render(self, name, value, attrs=None):
		if value is None: value = ''
		final_attrs = self.build_attrs(attrs, name=name)
		return mark_safe(u'<textarea%s>%s</textarea>' % (flatatt(final_attrs),
			conditional_escape(force_unicode(value))))

class XpSelectWidget(Widget):
	show_info = False
	def __init__(self, attrs=None, choices=(), hasInfo=False):
		super(XpSelectWidget, self).__init__(attrs)
		# choices can be any iterable, but we may need to render this widget
		# multiple times. Thus, collapse it into a list so it can be consumed
		# more than once.
		self.choices = list(choices)
		self.hasInfo = hasInfo
	def render(self, name, value, attrs=None, choices=()):
		if value is None: value = ''
		final_attrs = self.build_attrs(attrs, name=name)
		output = [u'<select%s>' % flatatt(final_attrs)]
		options = self.render_options(choices, [value])
		if options:
			output.append(options)
		output.append(u'</select>')
		if self.hasInfo == True: 
			output.append(' <img id="id_img_' + name + '" src="/site_media/images/blank.png" class="ImgInfo" />')
		return mark_safe(u'\n'.join(output))
	def render_options(self, choices, selected_choices):
		def render_option(option_value, option_label):
			option_value = force_unicode(option_value)
			selected_html = (option_value in selected_choices) and u' selected="selected"' or ''
			return u'<option value="%s"%s>%s</option>' % (
				escape(option_value), selected_html,
				conditional_escape(force_unicode(option_label)))
		# Normalize to strings.
		selected_choices = set([force_unicode(v) for v in selected_choices])
		output = []
		for option_value, option_label in chain(self.choices, choices):
			if isinstance(option_label, (list, tuple)):
				output.append(u'<optgroup label="%s">' % escape(force_unicode(option_value)))
				for option in option_label:
					output.append(render_option(*option))
				output.append(u'</optgroup>')
			else:
				output.append(render_option(option_value, option_label))
		return u'\n'.join(output)

class XpMultipleWidget(XpSelectWidget):
	show_info = False
	def render(self, name, value, attrs=None, choices=()):
		if value is None: value = []
		final_attrs = self.build_attrs(attrs, name=name)
		output = [u'<select multiple="multiple"%s>' % flatatt(final_attrs)]
		options = self.render_options(choices, value)
		if options:
			output.append(options)
		output.append('</select>')
		if self.hasInfo == True: 
			output.append(' <img id="id_img_' + name + '" src="/site_media/images/blank.png" class="ImgInfo" />')
		return mark_safe(u'\n'.join(output))
	def value_from_datadict(self, data, files, name):
		if isinstance(data, (MultiValueDict, MergeDict)):
			return data.getlist(name)
		return data.get(name, None)
	def _has_changed(self, initial, data):
		if initial is None:
			initial = []
		if data is None:
			data = []
		if len(initial) != len(data):
			return True
		for value1, value2 in zip(initial, data):
			if force_unicode(value1) != force_unicode(value2):
				return True
		return False


# ===================================================================================
# =================================== F I E L D S ===================================
# ===================================================================================


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
		print 'attrs : ', argsDict['label'], argsDict['widget'].attrs
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

class XpCharField(XpBaseCharField):
	"""CharField"""
	def __init__(self, instance, insField, min=None, max=None, req=True, init=None, jsReq=None, **argsDict):
		self._doInstanceInit(instance, insField)
		fieldMaxLength = self._getMaxLength()
		argsDict['validators'] = [validateTxtField]
		argsDict['max_length'] = max if max != None else fieldMaxLength
		argsDict['min_length'] = min if min != None else None
		argsDict['req'], argsDict['jsReq'] = self._doRequired(req, jsReq) 
		classStr = 'SmallMust' if req == True else 'Small' 
		if not argsDict.has_key('widget'):
			argsDict['widget'] = XpTextInputWidget(attrs={	'class': classStr,
									'maxlength': str(argsDict['max_length'])})
		super(XpCharField, self).__init__(**argsDict)

class XpUserField(XpBaseCharField):
	"""UserField""" 
	def __init__(self, instance, insField, min=None, max=None, req=True, init=None, jsReq=None, **argsDict):
		self._doInstanceInit(instance, insField)
		fieldMaxLength = self._getMaxLength()
		argsDict['validators'] = [validateUserId]
		argsDict['max_length'] = max if max != None else fieldMaxLength
		argsDict['min_length'] = min if min != None else None
		argsDict['req'], argsDict['jsReq'] = self._doRequired(req, jsReq)
		classStr = 'SmallMust' if req == True else 'Small'
		if not argsDict.has_key('widget'):
			argsDict['widget'] = XpTextInputWidget(attrs={	'class': classStr,
									'data-xp-val': 'ximpiaId',
									'maxlength': str(argsDict['max_length'])})
		super(XpUserField, self).__init__(**argsDict)

class XpEmailField(XpBaseCharField):
	"""EmailField"""
	def __init__(self, instance, insField, min=None, max=None, req=True, init=None, jsReq=None, **argsDict):
		self._doInstanceInit(instance, insField)
		fieldMaxLength = self._getMaxLength()
		argsDict['validators'] = [validateEmail]
		argsDict['max_length'] = max if max != None else fieldMaxLength
		argsDict['min_length'] = min if min != None else None
		argsDict['req'], argsDict['jsReq'] = self._doRequired(req, jsReq)
		classStr = 'SmallMust' if req == True else 'Small'
		if not argsDict.has_key('widget'):
			argsDict['widget'] = XpTextInputWidget(attrs={	'class': classStr,
									'data-xp-val': 'email',
									'maxlength': str(argsDict['max_length'])})
		super(XpEmailField, self).__init__(**argsDict)

class XpPasswordField(XpBaseCharField):
	"""PasswordField"""
	def __init__(self, instance, insField, min=None, max=None, req=True, init=None, jsReq=None, **argsDict):
		self._doInstanceInit(instance, insField)
		fieldMaxLength = self._getMaxLength()
		argsDict['validators'] = [validatePassword]
		argsDict['max_length'] = max if max != None else fieldMaxLength
		argsDict['min_length'] = min if min != None else None
		argsDict['req'], argsDict['jsReq'] = self._doRequired(req, jsReq)
		classStr = 'SmallMust' if req == True else 'Small'
		if not argsDict.has_key('widget'):
			argsDict['widget'] = XpPasswordWidget(attrs={	'class': classStr,
									'data-xp-val': 'password',
									'maxlength': str(argsDict['max_length'])})
		super(XpPasswordField, self).__init__(**argsDict)

class XpChoiceField(ChoiceField):
	"""ChoiceField"""
	def __init__(self, instance, insField, req=True, init='', choices=None, **argsDict):
		if insField.find('.') != -1:
			instanceName, instanceFieldName = insField.split('.')
			self.instanceName = instanceName
			self.instanceFieldName = instanceFieldName
			self.instance = instance
		classStr = 'SmallMust' if req == True else 'Small'
		xpVal = 'required' if req == True else ''
		argsDict['required'] = req
		if instance != None:
			if not argsDict.has_key('label'):
				argsDict['label'] = instance._meta.get_field_by_name(self.instanceFieldName)[0].verbose_name if instance else argsDict['label']
			if not argsDict.has_key('help_text'):
				argsDict['help_text'] = instance._meta.get_field_by_name(self.instanceFieldName)[0].help_text if instance else argsDict['help_text']
			argsDict['initial'] = init if init != '' else eval('instance' + '.' + self.instanceFieldName)
		argsDict['choices'] = choices if choices != None else None		
		if not argsDict.has_key('widget'):
			argsDict['widget'] = XpSelectWidget(attrs={	'class': classStr,
									'data-xp-val': xpVal})
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
	def __init__(self, instance, insField, req=True, init=[], choices=None, **argsDict):
		if insField.find('.') != -1:
			instanceName, instanceFieldName = insField.split('.')
			self.instanceName = instanceName
			self.instanceFieldName = instanceFieldName
			self.instance = instance
		classStr = 'SmallMust' if req == True else 'Small'
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
		if not argsDict.has_key('widget'):
			argsDict['widget'] = XpMultipleWidget(attrs={'class': classStr, 'data-xp-val': xpVal, 'size': '10', 
							'style': 'vertical-align:top; margin-top: 10px'})
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
