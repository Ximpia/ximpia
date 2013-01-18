import re

from django.utils.translation import ugettext as _
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

def validateStr(value):
	"""Validate any string value"""
	regexObj = re.compile('\w+', re.L)
	obj = RegexValidator(regexObj, _('Validation error. Text expected.'))
	obj.__call__(value)

def validateTxtField(value):
	"""Validate a text field"""
	#regexObj = re.compile("^(\w*)\s?(\s?\w+)*$", re.L)
	regexObj = re.compile('\w+', re.L)
	obj = RegexValidator(regexObj, _('Validation error. Text field expected.'))
	obj.__call__(value)

def validateDomain(value):
	"""Validate domain."""
	regexObj = re.compile("^([a-z0-9]([-a-z0-9]*[a-z0-9])?\\.)+((a[cdefgilmnoqrstuwxz]|aero|arpa)|(b[abdefghijmnorstvwyz]|biz)|(c[acdfghiklmnorsuvxyz]|cat|com|coop)|d[ejkmoz]|(e[ceghrstu]|edu)|f[ijkmor]|(g[abdefghilmnpqrstuwy]|gov)|h[kmnrtu]|(i[delmnoqrst]|info|int)|(j[emop]|jobs)|k[eghimnprwyz]|l[abcikrstuvy]|(m[acdghklmnopqrstuvwxyz]|mil|mobi|museum)|(n[acefgilopruz]|name|net)|(om|org)|(p[aefghklmnrstwy]|pro)|qa|r[eouw]|s[abcdeghijklmnortvyz]|(t[cdfghjklmnoprtvwz]|travel)|u[agkmsyz]|v[aceginu]|w[fs]|y[etu]|z[amw])$", re.L)
	obj = RegexValidator(regexObj, _('Validation error. Internet domain expected.'))
	obj.__call__(value)

def validateCurrency(value):
	"""Validate currency"""
	regexObj = re.compile('^[0-9]*\.?|\,?[0-9]{0,2}$')
	obj = RegexValidator(regexObj, _('Validation error. Currency expected.'))
	obj.__call__(value)

def validateId(value):
	"""Validate Id"""
	regexObj = re.compile('^[1-9]+[0-9]*$')
	obj = RegexValidator(regexObj, _('Validation error. Id expected.'))
	obj.__call__(value)

def validateUserId(value):
	"""Validate User Id"""
	#regexObj = re.compile('^[a-zA-Z0-9_.@-+]+')
	regexObj = re.compile('^[a-zA-Z0-9_]+')
	obj = RegexValidator(regexObj, _('Validation error. UserId expected.'))
	obj.__call__(value)

def validatePassword(value):
	"""Validate Password"""
	regexObj = re.compile('^[a-zA-Z0-9_.$%&]+')
	obj = RegexValidator(regexObj, _('Validation error. Password expected.'))
	obj.__call__(value)

def validateCaptcha(value):
	"""Validate Captcha"""
	regexObj = re.compile('^\w{6}$')
	obj = RegexValidator(regexObj, _('Validation error. Captcha text expected.'))
	obj.__call__(value)

def validateEmail(value):
	"""Validate Email"""
	regexObj = re.compile('^([\w.])+\@([a-z0-9]([-a-z0-9]*[a-z0-9])?\\.)+((a[cdefgilmnoqrstuwxz]|aero|arpa)|(b[abdefghijmnorstvwyz]|biz)|(c[acdfghiklmnorsuvxyz]|cat|com|coop)|d[ejkmoz]|(e[ceghrstu]|edu)|f[ijkmor]|(g[abdefghilmnpqrstuwy]|gov)|h[kmnrtu]|(i[delmnoqrst]|info|int)|(j[emop]|jobs)|k[eghimnprwyz]|l[abcikrstuvy]|(m[acdghklmnopqrstuvwxyz]|mil|mobi|museum)|(n[acefgilopruz]|name|net)|(om|org)|(p[aefghklmnrstwy]|pro)|qa|r[eouw]|s[abcdeghijklmnortvyz]|(t[cdfghjklmnoprtvwz]|travel)|u[agkmsyz]|v[aceginu]|w[fs]|y[etu]|z[amw])')
	obj = RegexValidator(regexObj, _('Validation error. Email expected.'))
	obj.__call__(value)
