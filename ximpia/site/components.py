import os

from ximpia.core.choices import Choices as _Ch
import ximpia.core.constants as _K
from ximpia.core.business import AppCompRegCommonBusiness

#import business
from service import SiteService

# Settings
from ximpia.core.util import getClass
settings = getClass(os.getenv("DJANGO_SETTINGS_MODULE"))

# Logging
import logging.config
logging.config.dictConfig(settings.LOGGING)
logger = logging.getLogger(__name__)

class Services:
	USERS = 'Users'

class Slugs:
	LOGIN = 'login'
	LOGOUT = 'logout'
	REMINDER_NEW_PASSWORD = 'reminder-new-password'
	CHANGE_PASSWORD = 'change-password'
	SIGNUP = 'signup'
	ACTIVATION_USER = 'activation-user'
	HOME_LOGIN = 'home-login'
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

class Tmpls:
	LOGIN = 'login'
	PASSWORD_REMINDER = 'passwordReminder'
	LOGOUT = 'logout'
	CHANGE_PASSWORD = 'changePassword'
	SIGNUP = 'signup'
	REMINDER_NEW_PASSWORD = 'reminderNewPassword'
	ACTIVATION_USER = 'activationUser'
	HOME_LOGIN = 'homeLogin'

class Flows:
	pass

#################### APPLICATION COMPONENTS : CLEAN AND MISC   ###################


class AppReg ( AppCompRegCommonBusiness ):
	def __init__(self):
		super(AppReg, self).__init__(__name__, doClean=True)
		# Application
		self._reg.registerApp(__name__, title='Ximpia Site', slug=Slugs.SITE)
		# Services
		self._reg.registerService(__name__, serviceName=Services.USERS, className=SiteService)


###################### SERVICE COMPONENT REGISTER ###########################

class SiteServiceReg ( AppCompRegCommonBusiness ):
	def __init__(self):
		super(SiteServiceReg, self).__init__(__name__)
	def views(self):
		# login
		self._reg.registerView(__name__, serviceName=Services.USERS, viewName=Views.LOGIN, slug=Slugs.LOGIN, 
							className=SiteService, method='viewLogin')
		self._reg.registerView(__name__, serviceName=Services.USERS, viewName=Views.LOGOUT, slug=Slugs.LOGOUT, 
							className=SiteService, method='viewLogout')
		# Password reminder
		self._reg.registerView(__name__, serviceName=Services.USERS, viewName=Views.REMINDER_NEW_PASSWORD, slug=Slugs.REMINDER_NEW_PASSWORD, 
							className=SiteService, method='viewReminderNewPassword')
		# change password
		self._reg.registerView(__name__, serviceName=Services.USERS, viewName=Views.CHANGE_PASSWORD, slug=Slugs.CHANGE_PASSWORD, 
							className=SiteService, method='viewChangePassword')
		# signup
		self._reg.registerView(__name__, serviceName=Services.USERS, viewName=Views.SIGNUP, slug=Slugs.SIGNUP, 
							className=SiteService, method='viewSignup')
		self._reg.registerView(__name__, serviceName=Services.USERS, viewName=Views.ACTIVATION_USER, slug=Slugs.ACTIVATION_USER, 
							className=SiteService, method='viewActivationUser')
		# homeLogin
		self._reg.registerView(__name__, serviceName=Services.USERS, viewName=Views.HOME_LOGIN, slug=Slugs.HOME_LOGIN, 
							className=SiteService, method='viewHomeLogin')
	def templates(self):
		self._reg.registerTemplate(__name__, viewName=Views.LOGIN, name=Tmpls.LOGIN)
		self._reg.registerTemplate(__name__, viewName=Views.LOGIN, name=Tmpls.PASSWORD_REMINDER, winType=_Ch.WIN_TYPE_POPUP, 
						alias='passwordReminder')
		self._reg.registerTemplate(__name__, viewName=Views.LOGOUT, name=Tmpls.LOGOUT)
		# user
		self._reg.registerTemplate(__name__, viewName=Views.CHANGE_PASSWORD, name=Tmpls.CHANGE_PASSWORD, winType=_Ch.WIN_TYPE_POPUP)
		# Signup
		self._reg.registerTemplate(__name__, viewName=Views.SIGNUP, name=Tmpls.SIGNUP)
		self._reg.registerTemplate(__name__, viewName=Views.REMINDER_NEW_PASSWORD, name=Tmpls.REMINDER_NEW_PASSWORD)
		# Home login
		self._reg.registerTemplate(__name__, viewName=Views.HOME_LOGIN, name=Tmpls.HOME_LOGIN)
		# Activate User
		self._reg.registerTemplate(__name__, viewName=Views.ACTIVATION_USER, name=Tmpls.ACTIVATION_USER)

	def actions(self):
		# login
		self._reg.registerAction(__name__, serviceName=Services.USERS, actionName=Actions.LOGIN, slug=Slugs.LOGIN, 
								className=SiteService, method='login')
		self._reg.registerAction(__name__, serviceName=Services.USERS, actionName=Actions.REQUEST_REMINDER, slug=Slugs.REQUEST_REMINDER,
								className=SiteService, method='requestReminder')
		self._reg.registerAction(__name__, serviceName=Services.USERS, actionName=Actions.FINALIZE_REMINDER, slug=Slugs.FINALIZE_REMINDER,
								className=SiteService, method='finalizeReminder')
		self._reg.registerAction(__name__, serviceName=Services.USERS, actionName=Actions.LOGOUT, slug=Slugs.LOGOUT,
								className=SiteService, method='logout',
								hasAuth=True)
		# signup
		self._reg.registerAction(__name__, serviceName=Services.USERS, actionName=Actions.SIGNUP, slug=Slugs.SIGNUP,
								className=SiteService, method='signup')
		# user
		self._reg.registerAction(__name__, serviceName=Services.USERS, actionName=Actions.CHANGE_PASSWORD, slug=Slugs.CHANGE_PASSWORD,
								className=SiteService, method='changePassword',
								hasAuth=True)
		# activateUser
		self._reg.registerAction(__name__, serviceName=Services.USERS, actionName=Actions.ACTIVATE_USER, slug=Slugs.ACTIVATE_USER,
								className=SiteService, method='activateUser')

	def flows(self):
		pass

	def menus(self):		
		# Ximpia Menu
		self._reg.registerMenu(__name__, name=Menus.SYS, title='Ximpia', description='Ximpia', iconName='iconLogo', viewName=Views.HOME_LOGIN)
		self._reg.registerMenu(__name__, name=Menus.SIGN_OUT, title='Sign out', description='Sign out', iconName='iconLogout', 
					actionName=Actions.LOGOUT)
		self._reg.registerMenu(__name__, name=Menus.CHANGE_PASSWORD, title='New Password', description='Change Password', iconName='', 
					viewName=Views.CHANGE_PASSWORD)
		# Login Home Menu
		self._reg.registerMenu(__name__, name=Menus.HOME_LOGIN, title='', description='Home', iconName='iconHome', 
							viewName=Views.HOME_LOGIN)
		#self._reg.registerMenu(__name__, name=Menus.HOME, title='Home', description='Home', iconName='iconHome', viewName=Views.HOME_LOGIN)

	def viewMenus(self):
		self._reg.registerViewMenu(__name__, viewName=Views.HOME_LOGIN, menus=[
						{_K.ZONE: _Ch.MENU_ZONE_SYS, _K.MENU_NAME: Menus.SYS},
						{_K.ZONE: _Ch.MENU_ZONE_SYS, _K.GROUP: Menus.SYS, _K.MENU_NAME: Menus.HOME_LOGIN},
						{_K.ZONE: _Ch.MENU_ZONE_SYS, _K.GROUP: Menus.SYS, _K.MENU_NAME: Menus.CHANGE_PASSWORD},
						{_K.ZONE: _Ch.MENU_ZONE_SYS, _K.GROUP: Menus.SYS, _K.MENU_NAME: Menus.SIGN_OUT},
						{_K.ZONE: _Ch.MENU_ZONE_MAIN, _K.MENU_NAME: Menus.HOME_LOGIN}
					])
	
	def search(self):
		self._reg.registerSearch(__name__, text='Change Password', viewName=Views.CHANGE_PASSWORD)
