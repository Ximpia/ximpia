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

class Flows:
	pass

#################### APPLICATION COMPONENTS : CLEAN AND MISC   ###################


class AppReg ( AppCompRegCommonBusiness ):
	def __init__(self):
		super(AppReg, self).__init__(__name__, doClean=True)
		self._reg.registerApp(name=self.app(), title='Ximpia Site', slug='site')


###################### SERVICE COMPONENT REGISTER ###########################

class SiteServiceReg ( AppCompRegCommonBusiness ):
	def __init__(self):
		super(SiteServiceReg, self).__init__()
	def views(self):
		# login
		self._reg.registerView(__name__, viewName=Views.LOGIN, myClass=SiteService, method=SiteService.viewLogin)
		self._reg.registerView(__name__, viewName=Views.LOGOUT, myClass=SiteService, method=SiteService.viewLogout)
		# Password reminder
		self._reg.registerView(__name__, viewName=Views.REMINDER_NEW_PASSWORD, myClass=SiteService, 
							method=SiteService.viewReminderNewPassword)
		# change password
		self._reg.registerView(__name__, viewName=Views.CHANGE_PASSWORD, myClass=SiteService, method=SiteService.viewChangePassword)
		# signup
		self._reg.registerView(__name__, viewName=Views.SIGNUP, myClass=SiteService, method=SiteService.viewSignup)
		self._reg.registerView(__name__, viewName=Views.ACTIVATION_USER, myClass=SiteService, method=SiteService.viewActivationUser)
		# homeLogin
		#self._reg.registerView(__name__, viewName='homeLogin', myClass=SiteService, method=SiteService.viewHomeLogin)
		# user
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
		#self._reg.registerTemplate(__name__, viewName='homeLogin', name='homeLogin')
		# Activate User
		self._reg.registerTemplate(__name__, viewName=Views.ACTIVATION_USER, name=Tmpls.ACTIVATION_USER)

	def actions(self):
		# login
		self._reg.registerAction(__name__, actionName=Actions.LOGIN, myClass=SiteService, method=SiteService.login)
		self._reg.registerAction(__name__, actionName=Actions.REQUEST_REMINDER, myClass=SiteService, method=SiteService.requestReminder)
		self._reg.registerAction(__name__, actionName=Actions.FINALIZE_REMINDER, myClass=SiteService, method=SiteService.finalizeReminder)
		self._reg.registerAction(__name__, actionName=Actions.LOGOUT, myClass=SiteService, method=SiteService.logout)
		# signup
		self._reg.registerAction(__name__, actionName=Actions.SIGNUP, myClass=SiteService, method=SiteService.signup)
		# user
		self._reg.registerAction(__name__, actionName=Actions.CHANGE_PASSWORD, myClass=SiteService, method=SiteService.changePassword)
		# activateUser
		self._reg.registerAction(__name__, actionName=Actions.ACTIVATE_USER, myClass=SiteService, method=SiteService.activateUser,
						hasUrl=True, hasAuth=False)

	def flows(self):
		pass

	def menus(self):
		# Ximpia Menu
		self._reg.registerMenu(__name__, name=Menus.SYS, titleShort='Ximpia', title='Ximpia', iconName='iconLogo')
		self._reg.registerMenu(__name__, name=Menus.SIGN_OUT, titleShort='Sign out', title='Sign out', iconName='iconLogout', 
					actionName='doLogout')
		self._reg.registerMenu(__name__, name=Menus.CHANGE_PASSWORD, titleShort='New Password', title='Change Password', iconName='', 
					viewName='changePassword')
		# Login Home Menu
		self._reg.registerMenu(__name__, name=Menus.HOME_LOGIN, titleShort='Home', title='Home', iconName='iconHome', 
							viewName='homeLogin')
		self._reg.registerMenu(__name__, name=Menus.HOME, titleShort='Home', title='Home', iconName='iconHome', viewName='home')

	def viewMenus(self):
		self._reg.registerViewMenu(__name__, viewName=Views.HOME_LOGIN, menus=[
						{_K.ZONE: _Ch.MENU_ZONE_SYS, _K.MENU_NAME: Menus.SYS},
						{_K.ZONE: _Ch.MENU_ZONE_SYS, _K.GROUP: Menus.SYS, _K.MENU_NAME: Menus.HOME_LOGIN},
						{_K.ZONE: _Ch.MENU_ZONE_SYS, _K.GROUP: Menus.SYS, _K.MENU_NAME: Menus.CHANGE_PASSWORD},
						{_K.ZONE: _Ch.MENU_ZONE_SYS, _K.GROUP: Menus.SYS, _K.MENU_NAME: Menus.SIGN_OUT},
						{_K.ZONE: _Ch.MENU_ZONE_MAIN, _K.MENU_NAME: Menus.HOME_LOGIN}
					])		

	def search(self):
		self._reg.registerSearch(text='Change Password', __name__, viewName=Views.CHANGE_PASSWORD)
