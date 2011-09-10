from django import template
import json

register = template.Library()

# TODO: Take this to utils !!!!
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

@register.inclusion_tag('social_network/tags/socialNetwork/signupButtonBar.html', takes_context=True)
def signupButtonBar(context, jsonObjStr=''):
	"""Default submit bar"""
	dict = {}
	dict['settings'] = context['settings']
	doJsonObj(dict, jsonObjStr, default={'idForm': 'id_Form1'})
	dict['idButton'] = dict['obj']['idForm'] + '_Submit'
	return dict

@register.inclusion_tag('social_network/tags/socialNetwork/field.html', takes_context=True)
def field(context, fieldName, fieldInstance, jsonObjStr=''):
	"""Field with Label and form object. Supports info tool tip from data model."""
	dict = {}
	#obj = {'info': 'False'}
	dict['settings'] = context['settings']
	doJsonObj(dict, jsonObjStr, default={'info': 'False'})
	dict['fieldInstance'] = fieldInstance
	dict['fieldName'] = fieldName
	return dict

@register.inclusion_tag('social_network/tags/socialNetwork/loadingSmall.html', takes_context=True)
def loadingSmall(context, idButton):
	"""Doc."""
	dict = {}
	dict['settings'] = context['settings']
	dict['idButton'] = idButton
	return dict

@register.inclusion_tag('social_network/tags/socialNetwork/loadingBig.html', takes_context=True)
def loadingBig(context):
	"""Doc."""
	dict = {}
	dict['settings'] = context['settings']
	return dict

@register.inclusion_tag('social_network/tags/socialNetwork/icon.html', takes_context=True)
def socialNetworkIcon(context, networkName, authDict):
	"""Tag function to process html code for social network icons"""
	dict = {}
	dict['settings'] = context['settings']
	dict['networkName'] = networkName
	dict['auth'] = authDict
	if authDict.has_key(networkName):
		dict['login'] = authDict[networkName]
	else:
		dict['login'] = False
	return dict

@register.inclusion_tag('social_network/tags/socialNetwork/captcha.html', takes_context=True)
def captcha(context):
	"""Doc."""
	dict = {}
	dict['settings'] = context['settings']
	dict['form'] = context['form']
	return dict
