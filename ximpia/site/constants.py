# coding: utf-8

class Services:
	USERS = 'Users'

class Slugs:
	LOGIN = 'login'
	LOGOUT = 'logout'
	REMINDER_NEW_PASSWORD = 'reminder-new-password'
	CHANGE_PASSWORD = 'change-password'
	SIGNUP = 'signup'
	ACTIVATION_USER = 'activation-user'
	HOME_LOGIN = 'in'
	SITE = 'site'
	REQUEST_REMINDER = 'request-reminder'
	FINALIZE_REMINDER = 'finalize-reminder'
	ACTIVATE_USER = 'activate-user'

class Views:
	LOGIN = 'login'
	LOGOUT = 'logout'
	REMINDER_NEW_PASSWORD = 'reminderNewPassword'
	CHANGE_PASSWORD = 'changePassword'
	SIGNUP = 'signup'
	ACTIVATION_USER = 'activationUser'
	HOME_LOGIN = 'homeLogin'

class Actions:
	LOGIN = 'login'
	REQUEST_REMINDER = 'requestReminder'
	FINALIZE_REMINDER = 'finalizeReminder'
	LOGOUT = 'logout'
	SIGNUP = 'signup'
	CHANGE_PASSWORD = 'changePassword'
	ACTIVATE_USER = 'activateUser'	

class Menus:
	SYS = 'sys'
	SIGN_OUT = 'signOut'
	CHANGE_PASSWORD = 'changePassword'
	HOME_LOGIN = 'homeLogin'
	HOME = 'home'
	LOGIN = 'login'

class Tmpls:
	LOGIN = 'login'
	PASSWORD_REMINDER = 'password_reminder'
	LOGOUT = 'logout'
	CHANGE_PASSWORD = 'change_password'
	SIGNUP = 'signup'
	REMINDER_NEW_PASSWORD = 'reminder_new_password'
	ACTIVATION_USER = 'activation_user'
	HOME_LOGIN = 'home_login'

class Flows:
	pass


#APP = 'site'
XIMPIA = 'ximpia'
TWITTER = 'twitter'
FACEBOOK = 'facebook'
XING = 'xing'
LINKEDIN = 'linkedin'
GOOGLE = 'google'
EMAIL = 'email'
PASSWORD = 'password'
SMS = 'sms'
FILE_QUOTA_DEFAULT = 2000
FILE_QUOTA_ORG = 5000
MSG_MODE_REC = 'received'
MSG_MODE_SENT = 'sent'
USER_SETTINGS = 'user_settings'
SETTINGS_ALLOW_PRIVATE_GRP_SUBS = 'ALLOW_PRIVATE_GRP_SUBS'
NUMBER_MATCHES = 10
OK = 'ok'
BLOCKED = 'blocked'
UNBLOCKED = 'unblocked'
ERROR = 'error'
ARCHIVE = 'archive'
UNARCHIVE = 'unarchive'
PROFESSIONAL = 'professional'
USER = 'user'
ORGANIZATION = 'organization'
SETTINGS_DEFAULT = ''
IMPORT = 'import'
GMAIL = 'gmail'
YAHOO = 'yahoo'
MSN = 'msn'
HOME = 'home'
WORK = 'work'
MOBILE = 'mobile'
WORK_MOBILE = 'work_mobile'
FAX = 'fax'
NETWORK = 'network'
SITE = 'site'
BLOG = 'blog'
FACEBOOK_PAGE = 'facebook_page'
IM = 'im'
RESERVED_GROUP_NAME_LIST = ['ximpia']
PENDING = 'pending'
USED = 'used'
NUMBER_INVITATIONS_USER = 15
NUMBER_INVITATIONS_STAFF = 500
SOCIAL_NETWORK = 'social_network'

# Signup constants
SIGNUP_USER_GROUP_ID = '1'

# Parameters
PARAM_LOGIN = 'LOGIN'
PARAM_REMINDER_DAYS = 'REMINDER_DAYS'
PARAM_USER_STATUS = 'USER_STATUS'
PARAM_USER_STATUS_PENDING = 'PENDING'
PARAM_USER_STATUS_ACTIVE = 'ACTIVE'
PARAM_ADDRESS_TYPE = 'ADDRESS_TYPE'
PARAM_ADDRESS_TYPE_PERSONAL = 'PERSONAL'
PARAM_CATEGORY_TYPE = 'CATEGORY_TYPE'

KEY_HAS_VALIDATED_EMAIL = 'HAS_VALIDATED_EMAIL'

# Cookies
COOKIE_LOGIN_REDIRECT = 'XP_LR'

# Meta Keys
META_REMINDER_ID = 'REMINDER_ID'
META_RESET_PASSWORD_DATE = 'RESET_PASSWORD_DATE'

# Settings
SET_SITE_SIGNUP_INVITATION = 'SITE_SIGNUP_INVITATION'
SET_SIGNUP_SOCIAL_NETWORK = 'SIGNUP_SOCIAL_NETWORK'
SET_SIGNUP_USER_PASSWORD = 'SIGNUP_USER_PASSWORD'
SET_REMINDER_DAYS = 'REMINDER_DAYS'
SET_NUMBER_RESULTS_LIST = 'NUMBER_RESULTS_LIST'
