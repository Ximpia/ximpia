from django import template

register = template.Library()

@register.inclusion_tag('social_network/tags/loading/small.html', takes_context=True)
def loadingSmall(context, loadId):
    """Doc."""
    dict = {}
    dict['settings'] = context['settings']
    dict['id'] = loadId
    return dict

@register.inclusion_tag('social_network/tags/loading/big.html', takes_context=True)
def loadingBig(context):
    """Doc."""
    dict = {}
    dict['settings'] = context['settings']
    return dict
