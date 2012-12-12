import os

from ximpia.core.choices import Choices as _Ch
import ximpia.core.constants as _K
from ximpia.core.business import AppCompRegCommonBusiness
from ximpia.site import constants as K

#import business
import service

# Settings
from ximpia.core.util import getClass
settings = getClass(os.getenv("DJANGO_SETTINGS_MODULE"))

from ximpia.core.service import DefaultService

# Logging
import logging.config
logging.config.dictConfig(settings.LOGGING)
logger = logging.getLogger(__name__)

def app():
	print __name__

class CompReg ( AppCompRegCommonBusiness ):
	def __init__(self):
		super(CompReg, self).__init__()
	def app(self):
		return '.'.join(__name__.split('.')[:2])
	def main(self):
		logger.debug( 'I am running the main' )
		self._reg.registerApp(name=self.app(), title='Ximpia Site', slug='site')
	def views(self):
		logger.debug( 'I am running the views' )
		# showHome
		# TODO: Integrate into videos application
		"""self._reg.cleanViews(appCode=K.APP)
		# login
		self._reg.registerView(appCode=K.APP, viewName='login', myClass=business.LoginBusiness, method='showLogin')
		self._reg.registerView(appCode=K.APP, viewName='newPassword', myClass=business.LoginBusiness, method='showNewPassword')
		self._reg.registerView(appCode=K.APP, viewName='logout', myClass=business.LoginBusiness, method='showLogout')
		# signup
		self._reg.registerView(appCode=K.APP, viewName='signup', myClass=business.SignupBusiness, method='showSignupUserInvitation')
		# homeLogin
		self._reg.registerView(appCode=K.APP, viewName='homeLogin', myClass=business.HomeBusiness, method='showLoginHome')
		# user
		self._reg.registerView(appCode=K.APP, viewName='changePassword', myClass=business.UserBusiness, method='showChangePassword', 
					winType=_Ch.WIN_TYPE_POPUP)
		# showHome
		# TODO: Integrate into videos application
		self._reg.registerView(appCode=K.APP, viewName='home', myClass=business.VideoBusiness, method='showHome')
		# activateUser
		self._reg.registerView(appCode=K.APP, viewName='activateUser', myClass=business.SignupBusiness, method='showActivateUser')"""
		"""self._reg.registerView(appName=self.app(), viewName='home', myClass=service.SiteService, method='home')
		# Contact Us
		self._reg.registerView(appName=self.app(), viewName='contactUs', myClass=service.SiteService, method='contactUs')
		# Join Us
		self._reg.registerView(appName=self.app(), viewName='joinUs', myClass=service.SiteService, method='joinUs')
		# Code
		self._reg.registerView(appName=self.app(), viewName='code', myClass=DefaultService, method='show')"""
	def templates(self):
		logger.debug( 'I am running the templates' )
		self._reg.registerTemplate(appName=self.app(), viewName='home', name='home')
		self._reg.registerTemplate(appName=self.app(), viewName='login', name='login')
		self._reg.registerTemplate(appName=self.app(), viewName='login', name='passwordReminder', winType=_Ch.WIN_TYPE_POPUP, 
						alias='passwordReminder')
		self._reg.registerTemplate(appName=self.app(), viewName='logout', name='logout')
		# user
		self._reg.registerTemplate(appName=self.app(), viewName='changePassword', name='changePassword', winType=_Ch.WIN_TYPE_POPUP)
		# Signup
		self._reg.registerTemplate(appName=self.app(), viewName='signup', name='signup')
		self._reg.registerTemplate(appName=self.app(), viewName='newPassword', name='newPassword')
		# Home login
		self._reg.registerTemplate(appName=self.app(), viewName='homeLogin', name='homeLogin')
		# Activate User
		self._reg.registerTemplate(appName=self.app(), viewName='activateUser', name='activateUser')
		# Contact Us
		self._reg.registerTemplate(appName=self.app(), viewName='contactUs', name='contactUs')
		# Join Us
		self._reg.registerTemplate(appName=self.app(), viewName='joinUs', name='joinUs')
		# Code
		self._reg.registerTemplate(appName=self.app(), viewName='code', name='code')
		# Wiki
		#self._reg.registerTemplate(appName=self.app(), viewName='wiki', name='wiki')

	def actions(self):
		logger.debug( 'I am running the actions' )
		"""self._reg.cleanActions(appCode=K.APP)
		# login
		self._reg.registerAction(appCode=K.APP, actionName='doLogin', myClass=business.LoginBusiness, method='doLogin')
		self._reg.registerAction(appCode=K.APP, actionName='doNewPassword', myClass=business.LoginBusiness, method='doNewPassword')
		self._reg.registerAction(appCode=K.APP, actionName='doPasswordReminder', myClass=business.LoginBusiness, method='doPasswordReminder')
		self._reg.registerAction(appCode=K.APP, actionName='doLogout', myClass=business.LoginBusiness, method='doLogout')
		# signup
		self._reg.registerAction(appCode=K.APP, actionName='doSignupUser', myClass=business.SignupBusiness, method='doUser')
		# user
		self._reg.registerAction(appCode=K.APP, actionName='doChangePassword', myClass=business.UserBusiness, method='doChangePassword')
		# activateUser
		self._reg.registerAction(appCode=K.APP, actionName='activateUser', myClass=business.SignupBusiness, method='activateUser',
						hasUrl=True, hasAuth=False)"""
		"""# contactUs
		self._reg.registerAction(appName=self.app(), actionName='contactUs', myClass=business.HomeBusiness, method='contactUs')
		# joinUs
		self._reg.registerAction(appName=self.app(), actionName='joinUs', myClass=business.HomeBusiness, method='joinUs')"""

	def flows(self):
		logger.debug( 'I am running the flows' )

	def menus(self):
		logger.debug( 'I am running the menus' )
		# Ximpia Menu
		self._reg.registerMenu(appName=self.app(), name='sys', titleShort='Ximpia', title='Ximpia', iconName='iconLogo')
		self._reg.registerMenu(appName=self.app(), name='signout', titleShort='Sign out', title='Sign out', iconName='iconLogout', 
					actionName='doLogout')
		self._reg.registerMenu(appName=self.app(), name='changePassword', titleShort='New Password', title='Change Password', iconName='', 
					viewName='changePassword')
		# Login Home Menu
		self._reg.registerMenu(appName=self.app(), name='homeLogin', titleShort='Home', title='Home', iconName='iconHome', viewName='homeLogin')
		self._reg.registerMenu(appName=self.app(), name='home', titleShort='Home', title='Home', iconName='iconHome', viewName='home')
		# Site Pages
		self._reg.registerMenu(appName=self.app(), name='contactUs', titleShort='Contact Us', title='Contact Us', iconName='iconContactUs', 
					viewName='contactUs')
		self._reg.registerMenu(appName=self.app(), name='joinUs', titleShort='Join Us', title='Join Our Developer Community', 
					iconName='iconUsers', viewName='joinUs')
		self._reg.registerMenu(appName=self.app(), name='code', titleShort='Code', title='Get the Code', iconName='iconEngine', viewName='code')
		#self._reg.registerMenu(appName=self.app(), name='wiki', titleShort='Wiki', title='Info on Developing Apps', iconName='iconWiki', viewName='wiki')

	def viewMenus(self):
		logger.debug( 'I am running the viewMenus' )
		self._reg.registerViewMenu(appName=self.app(), viewName='homeLogin', menus=[
						{_K.ZONE: _Ch.MENU_ZONE_SYS, _K.MENU_NAME: 'sys'},
						{_K.ZONE: _Ch.MENU_ZONE_SYS, _K.GROUP: 'sys', _K.MENU_NAME: 'homeLogin'},
						{_K.ZONE: _Ch.MENU_ZONE_SYS, _K.GROUP: 'sys', _K.MENU_NAME: 'changePassword'},
						{_K.ZONE: _Ch.MENU_ZONE_SYS, _K.GROUP: 'sys', _K.MENU_NAME: 'signout'},
						{_K.ZONE: _Ch.MENU_ZONE_MAIN, _K.MENU_NAME: 'homeLogin'}
					])
		
		"""self._reg.registerViewMenu(appName='testScrap', viewName='homeLogin', menus=[
						{_K.ZONE: _Ch.MENU_ZONE_VIEW, _K.MENU_NAME: 'scrap'}
					])"""
		
		self._reg.registerViewMenu(appName=self.app(), viewName='home', menus=[
						#{_K.ZONE: _Ch.MENU_ZONE_MAIN, _K.MENU_NAME: 'home'},
						{_K.ZONE: _Ch.MENU_ZONE_VIEW, _K.MENU_NAME: 'code'},
						#{_K.ZONE: _Ch.MENU_ZONE_VIEW, _K.MENU_NAME: 'wiki'},
						{_K.ZONE: _Ch.MENU_ZONE_VIEW, _K.MENU_NAME: 'joinUs'},
						{_K.ZONE: _Ch.MENU_ZONE_VIEW, _K.MENU_NAME: 'contactUs'}
					])
		# contactUs
		self._reg.registerViewMenu(appName=self.app(), viewName='contactUs', menus=[
					])
		# joinUs
		self._reg.registerViewMenu(appName=self.app(), viewName='joinUs', menus=[
						{_K.ZONE: _Ch.MENU_ZONE_VIEW, _K.MENU_NAME: 'code'}
					])
		# code
		self._reg.registerViewMenu(appName=self.app(), viewName='code', menus=[
						{_K.ZONE: _Ch.MENU_ZONE_VIEW, _K.MENU_NAME: 'joinUs'}
					])
		# wiki

	def search(self):
		logger.debug( 'I am running the search' )
		self._reg.registerSearch(text='Change Password', appName=self.app(), viewName='changePassword')
