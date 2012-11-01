from django.forms.widgets import Widget, RadioSelect
from django.forms.util import flatatt
from django.utils import formats
from django.utils.html import escape, conditional_escape
from itertools import chain
from django.utils.safestring import mark_safe
from django.utils.datastructures import MultiValueDict, MergeDict
from django.utils.encoding import force_unicode

class XpCheckboxWidget ( Widget ):
	"""Widget for checkbox"""
	def render(self, name, value, attrs=None):
		final_attrs = self.build_attrs(attrs, type='checkbox', name=name)
		try:
			result = self.check_test(value)
		except: # Silently catch exceptions
			result = False
		if result:
			final_attrs['checked'] = 'checked'
		if value not in ('', True, False, None):
			# Only add the 'value' attribute if a value is non-empty.
			final_attrs['value'] = force_unicode(value)
		return mark_safe(u'<input%s />' % flatatt(final_attrs))

class XpOptionWidget( Widget ):
	"""Widget for radio buttons (option visual component)"""
	_element = 'input'
	input_type = 'radio'
	def __init__(self, attrs=None, hasInfo=False):
		super(XpOptionWidget, self).__init__(attrs)
		self.hasInfo = hasInfo

class XpInputWidget( Widget ):
	"""
	Base class for all <input> widgets (except type='checkbox' and
	type='radio', which are special).
	"""
	input_type = None # Subclasses must define this.
	show_info = False
	hasInfo = False
	_element = 'input'
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

class XpTextInputWidget( XpInputWidget ):
	_element = 'input'
	input_type = 'text'
	def __init__(self, attrs=None, hasInfo=False):
		super(XpTextInputWidget, self).__init__(attrs, hasInfo)

class XpHiddenWidget( XpInputWidget ):
	input_type = 'hidden'
	_element = 'input'
	is_hidden = True

class XpMultipleHiddenWidget( XpHiddenWidget ):
	"""
	A widget that handles <input type="hidden"> for fields that have a list
	of values.
	"""
	_element = 'input'
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

class XpPasswordWidget( XpInputWidget ):
	_element = 'input'
	input_type = 'password'
	def __init__(self, attrs=None, render_value=True, hasInfo=False):
		super(XpPasswordWidget, self).__init__(attrs, hasInfo)
		self.render_value = render_value
	def render(self, name, value, attrs=None):
		if not self.render_value: value=None
		return super(XpPasswordWidget, self).render(name, value, attrs)

class XpTextareaWidget( Widget ):
	_element = 'textarea'
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

class XpSelectWidget( Widget ):
	_element = 'select'
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

class XpMultipleWidget( XpSelectWidget ):
	_element = 'select'
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


