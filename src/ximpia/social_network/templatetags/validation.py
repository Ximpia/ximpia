from django import template

register = template.Library()

@register.inclusion_tag('social_network/tags/validation/captcha.html', takes_context=True)
def captcha(context):
    """Doc."""
    dict = {}
    dict['settings'] = context['settings']
    dict['form'] = context['form']
    return dict
