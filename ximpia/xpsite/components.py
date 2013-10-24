# coding: utf-8

import os

from ximpia.xpcore.choices import Choices as _Ch
import ximpia.xpcore.constants as _K
from ximpia.xpcore.business import AppCompRegCommonBusiness

#import business
from service import SiteService
from constants import Services, Slugs, Views, Actions, Menus, Tmpls

# Settings
from ximpia.xpcore.util import get_class
settings = get_class(os.getenv("DJANGO_SETTINGS_MODULE"))

# Logging
import logging.config
logging.config.dictConfig(settings.LOGGING)
logger = logging.getLogger(__name__)

#################### APPLICATION COMPONENTS : CLEAN AND MISC   ###################


class AppReg ( AppCompRegCommonBusiness ):
	def __init__(self):
		super(AppReg, self).__init__(__name__)
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
							className=SiteService, method='view_login')
		self._reg.registerView(__name__, serviceName=Services.USERS, viewName=Views.LOGOUT, slug=Slugs.LOGOUT, 
							className=SiteService, method='view_logout')
		# Password reminder
		self._reg.registerView(__name__, serviceName=Services.USERS, viewName=Views.REMINDER_NEW_PASSWORD, slug=Slugs.REMINDER_NEW_PASSWORD, 
							className=SiteService, method='view_reminder_new_password')
		# change password
		self._reg.registerView(__name__, serviceName=Services.USERS, viewName=Views.CHANGE_PASSWORD, slug=Slugs.CHANGE_PASSWORD, 
							className=SiteService, method='view_change_password', hasAuth=True, winType=_Ch.WIN_TYPE_POPUP)
		# signup
		self._reg.registerView(__name__, serviceName=Services.USERS, viewName=Views.SIGNUP, slug=Slugs.SIGNUP, 
							className=SiteService, method='view_signup')
		self._reg.registerView(__name__, serviceName=Services.USERS, viewName=Views.ACTIVATION_USER, slug=Slugs.ACTIVATION_USER, 
							className=SiteService, method='view_activation_user')
		# homeLogin
		self._reg.registerView(__name__, serviceName=Services.USERS, viewName=Views.HOME_LOGIN, slug=Slugs.HOME_LOGIN, 
							className=SiteService, method='view_home_login', hasAuth=True)
	def templates(self):
		self._reg.registerTemplate(__name__, viewName=Views.LOGIN, name=Tmpls.LOGIN)
		self._reg.registerTemplate(__name__, viewName=Views.LOGIN, name=Tmpls.PASSWORD_REMINDER, winType=_Ch.WIN_TYPE_POPUP, 
						alias='password_reminder')
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
								className=SiteService, method='request_reminder')
		self._reg.registerAction(__name__, serviceName=Services.USERS, actionName=Actions.FINALIZE_REMINDER, slug=Slugs.FINALIZE_REMINDER,
								className=SiteService, method='finalize_reminder')
		self._reg.registerAction(__name__, serviceName=Services.USERS, actionName=Actions.LOGOUT, slug=Slugs.LOGOUT,
								className=SiteService, method='logout',
								hasAuth=True)
		# signup
		self._reg.registerAction(__name__, serviceName=Services.USERS, actionName=Actions.SIGNUP, slug=Slugs.SIGNUP,
								className=SiteService, method='signup')
		# user
		self._reg.registerAction(__name__, serviceName=Services.USERS, actionName=Actions.CHANGE_PASSWORD, slug=Slugs.CHANGE_PASSWORD,
								className=SiteService, method='change_password',
								hasAuth=True)
		# activateUser
		self._reg.registerAction(__name__, serviceName=Services.USERS, actionName=Actions.ACTIVATE_USER, slug=Slugs.ACTIVATE_USER,
								className=SiteService, method='activate_user')

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
		self._reg.registerMenu(__name__, name=Menus.HOME_LOGIN, title='', description='Home', iconName='iconUser', 
							viewName=Views.HOME_LOGIN)
		self._reg.registerMenu(__name__, name=Menus.SIGNUP, title='Signup', description='Signup', iconName='iconSignup', 
							viewName=Views.SIGNUP)
		self._reg.registerMenu(__name__, name=Menus.LOGIN, title='Login', description='Login', iconName='iconUnlock',
							viewName=Views.LOGIN)

	def viewMenus(self):
		# conditions
		self._reg.registerCondition(__name__, 'notLogin', 'isLogin == false')
		self._reg.registerCondition(__name__, 'login', 'isLogin == true')
		self._reg.registerViewMenu(__name__, viewName=Views.HOME_LOGIN, menus=[
						{_K.ZONE: _Ch.MENU_ZONE_SYS, _K.MENU_NAME: Menus.SYS},
						{_K.ZONE: _Ch.MENU_ZONE_SYS, _K.GROUP: Menus.SYS, _K.MENU_NAME: Menus.CHANGE_PASSWORD},
						{_K.ZONE: _Ch.MENU_ZONE_SYS, _K.GROUP: Menus.SYS, _K.MENU_NAME: Menus.SIGN_OUT},
						{_K.ZONE: _Ch.MENU_ZONE_MAIN, _K.MENU_NAME: Menus.HOME_LOGIN}
					])
		self._reg.registerViewMenu(__name__, viewName=Views.ACTIVATION_USER, menus=[
						{_K.ZONE: _Ch.MENU_ZONE_VIEW, _K.MENU_NAME: Menus.HOME},
						{_K.ZONE: _Ch.MENU_ZONE_VIEW, _K.MENU_NAME: Menus.LOGIN}
					])
		self._reg.registerViewMenu(__name__, viewName=Views.SIGNUP, menus=[
						{_K.ZONE: _Ch.MENU_ZONE_VIEW, _K.MENU_NAME: Menus.HOME},
						{_K.ZONE: _Ch.MENU_ZONE_VIEW, _K.MENU_NAME: Menus.LOGIN}
					])
		self._reg.registerServMenu(__name__, serviceName=Services.USERS, menus=[
						{_K.ZONE: _Ch.MENU_ZONE_MAIN, _K.MENU_NAME: Menus.LOGIN, _K.CONDITIONS: 'notLogin:render:True'},
						{_K.ZONE: _Ch.MENU_ZONE_MAIN, _K.MENU_NAME: Menus.SIGNUP, _K.CONDITIONS: 'notLogin:render:True'},
						{_K.ZONE: _Ch.MENU_ZONE_MAIN, _K.MENU_NAME: Menus.HOME_LOGIN, _K.CONDITIONS: 'login:render:True'}
					])

	def search(self):
		self._reg.registerSearch(__name__, text='Change Password', viewName=Views.CHANGE_PASSWORD)
