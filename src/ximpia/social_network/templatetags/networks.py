from django import template

register = template.Library()

@register.inclusion_tag('social_network/tags/networks/icon.html', takes_context=True)
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
