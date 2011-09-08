from django import template
import json

register = template.Library()

@register.inclusion_tag('social_network/tags/form/default.html', takes_context=True)
def submitDefault(context, formId):
	"""Default submit bar"""
	# id_" + form.id + '_Submit
	dict = {}
	dict['settings'] = context['settings']
	dict['idButton'] = formId + '_Submit'
	dict['idLoadIcon'] = formId + '_Submit'
	return dict

@register.inclusion_tag('social_network/tags/form/field.html', takes_context=True)
def field(context, fieldName, fieldInstance, jsonObjStr=''):
	"""Field with Label and form object. Supports info tool tip from data model."""
	dict = {}
	obj = {'info': 'False'}
	dict['settings'] = context['settings']
	if jsonObjStr != '':
		try:
			jsonObj = json.loads(jsonObjStr)
			dict['obj'] = {}
			if jsonObj.has_key('info'):
				dict['obj']['info'] = str(jsonObj['info'])
			else:
				dict['obj'] = obj
		except ValueError:
			dict['obj'] = obj
	else:
		dict['obj'] = obj
	dict['fieldInstance'] = fieldInstance
	dict['fieldName'] = fieldName
	return dict
