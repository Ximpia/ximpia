from django.utils.translation import ugettext as _

class Choices(object):
	# COUNTRY
	COUNTRY = (
		('fr', _('France')),
		('es', _('Spain')),
		('us', _('United States')),
		('ag', _('Antigua and Barbuda')),
		('ai', _('Angilla')),
		('al', _('Albania')),
		('am', _('Armenia')),
		('an', _('Netherlands Antilles')),
		('ao', _('Angola')),
		('aq', _('Antartica')),
		('ar', _('Argentina')),
		('as', _('American Samoa')),
		('at', _('Australia')),
		('aw', _('Aruba')),
		('ax', _('Aland Islands')),
		('az', _('Azerbaijan')),
		('ba', _('Bosnia and Herzegovina')),
		('bb', _('Barbados')),
		('bd', _('Bangladesh')),
		('be', _('Belgium')),
		('bf', _('Burkina Faso')),		
		)
	# SEX
	SEX_MAN = 'male'
	SEX_WOMAN = 'female'
	SEX = (
		(SEX_MAN, _('Male')),
		(SEX_WOMAN, _('Female'))
		)
	# RELATIONSHIP
	SINGLE = 'single'
	IN_RELATIONSHIP = 'in_relationship'
	MARRIED = 'married'
	RELATIONSHIP = (
			(SINGLE, _('Single')),
			(IN_RELATIONSHIP, _('In a Relationship')),
			(MARRIED, _('Married')))
	# CUSTOM_TYPE
	CUSTOM_TYPE_INPUT = 'input'
	CUSTOM_TYPE_COMBO = 'combo'
	CUSTOM_TYPE = (
		(CUSTOM_TYPE_INPUT, 'Input'),
		(CUSTOM_TYPE_COMBO, 'Combo'),
		)
	# LANG
	LANG_ENGLISH = 'en'
	LANG = (
			('en', _('English')),
			('es', _('Spanish')))
