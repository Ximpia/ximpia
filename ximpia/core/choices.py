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
	LANG_SPANISH = 'es'
	LANG = (
			('en', _('English')),
			('es', _('Spanish')))
	# OPERATOR
	OP_EQ = 'eq'
	OP_LT = 'lt'
	OP_GT = 'gt'
	OP_NE = 'ne'
	OP = (
		('eq', _('Equal')),
		('lt', _('Less Than')),
		('gt', _('Greater Than')),
		('ne', _('Not Equal')))

	# BASIC_TYPES
	BASIC_TYPE_INT = 'int'
	BASIC_TYPE_STR = 'str'
	BASIC_TYPE_BOOL = 'bool'
	BASIC_TYPE_LONG = 'long'
	BASIC_TYPE_FLOAT = 'float'
	BASIC_TYPE_DATE = 'date'
	BASIC_TYPE_TIME = 'time'
	BASIC_TYPES = (
		('int', _('Integer')),
		('str', _('String')),
		('bool', _('Boolean')),
		('long', _('Long')),
		('float', _('Float')),
		('date', _('Date')),
		('time', _('Time')))
	# MENU_ZONE
	MENU_ZONE_SYS = 'sys'
	MENU_ZONE_MAIN = 'main'
	MENU_ZONE_VIEW = 'view'
	MENU_ZONES = (
		(MENU_ZONE_SYS, _('System')),
		(MENU_ZONE_MAIN, _('Main')),
		(MENU_ZONE_VIEW, _('View')))
	# WINDOW_TYPE
	WIN_TYPE_WINDOW = 'window'
	WIN_TYPE_POPUP = 'popup'
	WIN_TYPES = (
		(WIN_TYPE_WINDOW, _('Window')),
		(WIN_TYPE_POPUP, _('Popup')))
	# DEVICES
	DEVICE_PC = 'PC'
	DEVICE_TABLET = 'TABLET'
	DEVICE_PHONE = 'PHONE'
	DEVICES = (
		(DEVICE_PC, _('Personal Computer')),
		(DEVICE_TABLET, _('Tablet')),
		(DEVICE_PHONE, _('Phone')))
	# URL_TARGET
	URL_TARGET_SAME = 'same'
	URL_TARGET_NEW = 'new'
	URL_TARGET = (
		(URL_TARGET_SAME, _('Same Window')),
		(URL_TARGET_NEW, _('New Window')),
		)
