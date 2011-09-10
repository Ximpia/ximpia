from django import template
import json

register = template.Library()

def doJsonObj(dict, jsonObjStr, default={}):
	"""Doc."""
	if jsonObjStr != '':
		try:
			jsonObj = json.loads(jsonObjStr)
			dict['obj'] = {}
			list = jsonObj.keys()
			for key in list:
				if jsonObj.has_key(key):
					dict['obj'][key] = str(jsonObj[key])
				else:
					dict['obj'] = default
		except ValueError:
			dict['obj'] = default
	else:
		dict['obj'] = default

@register.inclusion_tag('social_network/tags/form/default.html', takes_context=True)
def submitDefault(context, jsonObjStr=''):
	"""Default submit bar"""
	# id_" + form.id + '_Submit
	print 'jsonObjStr : ', jsonObjStr
	dict = {}
	dict['settings'] = context['settings']
	doJsonObj(dict, jsonObjStr, default={'idForm': 'id_Form1'})
	print 'dict : ', dict
	return dict

@register.inclusion_tag('social_network/tags/form/field.html', takes_context=True)
def field(context, fieldName, fieldInstance, jsonObjStr=''):
	"""Field with Label and form object. Supports info tool tip from data model."""
	dict = {}
	#obj = {'info': 'False'}
	dict['settings'] = context['settings']
	doJsonObj(dict, jsonObjStr, default={'info': 'False'})
	dict['fieldInstance'] = fieldInstance
	dict['fieldName'] = fieldName
	print 'dict : ', dict
	return dict
