from ximpia.core.business import ComponentRegister
from ximpia.core.choices import Choices as _Ch
from ximpia.core.constants import CoreConstants as _K

from constants import Constants as K
import business

#################################################
# Parameters used in Menu, Views and Workflow
#################################################
ComponentRegister.registerParam(appCode=K.APP, name='myFirstParan', title='My favorite parameter', paramType=_Ch.BASIC_TYPE_STR)
ComponentRegister.registerParam(appCode=K.APP, name='ximpiaId', title='XimpiaId', paramType=_Ch.BASIC_TYPE_STR)


##########
# Views
##########
# login
ComponentRegister.registerView(appCode=K.APP, viewName='login', myClass=business.LoginBusiness, method='showLogin')
ComponentRegister.registerView(appCode=K.APP, viewName='newPassword', myClass=business.LoginBusiness, method='showNewPassword')
ComponentRegister.registerView(appCode=K.APP, viewName='logout', myClass=business.LoginBusiness, method='showLogout')
# signup
ComponentRegister.registerView(appCode=K.APP, viewName='signup', myClass=business.SignupBusiness, method='showSignupUser')
# home
ComponentRegister.registerView(appCode=K.APP, viewName='home', myClass=business.HomeBusiness, method='showStatus')
# user
ComponentRegister.registerView(appCode=K.APP, viewName='changePassword', myClass=business.UserBusiness, method='showChangePassword', 
			winType=_Ch.WIN_TYPE_POPUP)

##########
# Actions
##########
# login
ComponentRegister.registerAction(appCode=K.APP, actionName='doLogin', myClass=business.LoginBusiness, method='doLogin')
ComponentRegister.registerAction(appCode=K.APP, actionName='doNewPassword', myClass=business.LoginBusiness, method='doNewPassword')
ComponentRegister.registerAction(appCode=K.APP, actionName='doPasswordReminder', myClass=business.LoginBusiness, method='doPasswordReminder')
ComponentRegister.registerAction(appCode=K.APP, actionName='doLogout', myClass=business.LoginBusiness, method='doLogout')
# signup
ComponentRegister.registerAction(appCode=K.APP, actionName='doSignupUser', myClass=business.SignupBusiness, method='doUser')
# user
ComponentRegister.registerAction(appCode=K.APP, actionName='doChangePassword', myClass=business.UserBusiness, method='doChangePassword')


###############
# Menu
###############
# Ximpia Menu
ComponentRegister.cleanMenu(K.APP)
ComponentRegister.registerMenu(appCode=K.APP, name='sys', titleShort='Ximpia', title='Ximpia', iconName='iconLogo')
ComponentRegister.registerMenu(appCode=K.APP, name='signout', titleShort='Sign out', title='Sign out', iconName='iconLogout', 
			actionName='doLogout')
ComponentRegister.registerMenu(appCode=K.APP, name='changePassword', titleShort='New Password', title='Change Password', iconName='', 
			viewName='changePassword')
# Home Menu
ComponentRegister.registerMenu(appCode=K.APP, name='home', titleShort='Home', title='Home', iconName='iconHome', viewName='home')


###############
# View Menus
###############
ComponentRegister.registerViewMenu(appCode=K.APP, viewName='home', menus=[
				{_K.ZONE: 'sys', _K.MENU_NAME: 'sys'},
				{_K.ZONE: 'sys', _K.GROUP: 'sys', _K.MENU_NAME: 'home'},
				{_K.ZONE: 'sys', _K.GROUP: 'sys', _K.MENU_NAME: 'changePassword'},
				{_K.ZONE: 'sys', _K.GROUP: 'sys', _K.MENU_NAME: 'signout'},
				{_K.ZONE: 'main', _K.MENU_NAME: 'home'}
			])

#############
# Templates
#############
ComponentRegister.registerTemplate(appCode=K.APP, viewName='home', name='home', winType=_Ch.WIN_TYPE_WINDOW)
ComponentRegister.registerTemplate(appCode=K.APP, viewName='login', name='login', winType=_Ch.WIN_TYPE_WINDOW)
ComponentRegister.registerTemplate(appCode=K.APP, viewName='login', name='passwordReminder', winType=_Ch.WIN_TYPE_POPUP, 
				alias='passwordReminder')
ComponentRegister.registerTemplate(appCode=K.APP, viewName='logout', name='logout', winType=_Ch.WIN_TYPE_WINDOW)
# user
ComponentRegister.registerTemplate(appCode=K.APP, viewName='changePassword', name='changePassword', winType=_Ch.WIN_TYPE_POPUP)


##########
# Flows
##########
# login
ComponentRegister.registerFlow(appCode=K.APP, flowCode='login')
ComponentRegister.registerFlowView(appCode=K.APP, flowCode='login', viewNameSource='login', viewNameTarget='home', 
				actionName='doLogin', order=10)

##########
# Search
##########
ComponentRegister.cleanSearch(K.APP)
ComponentRegister.registerSearch(text='Change Password', appCode=K.APP, viewName='changePassword')
