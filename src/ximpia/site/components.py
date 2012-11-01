from ximpia.core.business import ComponentRegister
from ximpia.core.choices import Choices as _Ch
import ximpia.core.constants as _K
import constants as K
import business
from ximpia.core.business import DefaultBusiness

#################################################
# Parameters used in Menu, Views and Workflow
#################################################

##########
# Application
##########
ComponentRegister.registerApp(code=K.APP, name='Site')

##########
# Views
##########
ComponentRegister.cleanViews(appCode=K.APP)
# login
ComponentRegister.registerView(appCode=K.APP, viewName='login', myClass=business.LoginBusiness, method='showLogin')
ComponentRegister.registerView(appCode=K.APP, viewName='newPassword', myClass=business.LoginBusiness, method='showNewPassword')
ComponentRegister.registerView(appCode=K.APP, viewName='logout', myClass=business.LoginBusiness, method='showLogout')
# signup
ComponentRegister.registerView(appCode=K.APP, viewName='signup', myClass=business.SignupBusiness, method='showSignupUserInvitation')
# homeLogin
ComponentRegister.registerView(appCode=K.APP, viewName='homeLogin', myClass=business.HomeBusiness, method='showLoginHome')
# user
ComponentRegister.registerView(appCode=K.APP, viewName='changePassword', myClass=business.UserBusiness, method='showChangePassword', 
			winType=_Ch.WIN_TYPE_POPUP)
# showHome
# TODO: Integrate into videos application
ComponentRegister.registerView(appCode=K.APP, viewName='home', myClass=business.VideoBusiness, method='showHome')
# activateUser
ComponentRegister.registerView(appCode=K.APP, viewName='activateUser', myClass=business.SignupBusiness, method='showActivateUser')
# Contact Us
ComponentRegister.registerView(appCode=K.APP, viewName='contactUs', myClass=business.HomeBusiness, method='showContactUs')
# Join Us
ComponentRegister.registerView(appCode=K.APP, viewName='joinUs', myClass=business.HomeBusiness, method='showJoinUs')
# Code
ComponentRegister.registerView(appCode=K.APP, viewName='code', myClass=DefaultBusiness, method='show')
# Wiki
#ComponentRegister.registerView(appCode=K.APP, viewName='wiki', myClass=DefaultBusiness, method='show')


#############
# Templates
#############
ComponentRegister.cleanTemplates(appCode=K.APP)
ComponentRegister.registerTemplate(appCode=K.APP, viewName='home', name='home')
ComponentRegister.registerTemplate(appCode=K.APP, viewName='login', name='login')
ComponentRegister.registerTemplate(appCode=K.APP, viewName='login', name='passwordReminder', winType=_Ch.WIN_TYPE_POPUP, 
				alias='passwordReminder')
ComponentRegister.registerTemplate(appCode=K.APP, viewName='logout', name='logout')
# user
ComponentRegister.registerTemplate(appCode=K.APP, viewName='changePassword', name='changePassword', winType=_Ch.WIN_TYPE_POPUP)
# Signup
ComponentRegister.registerTemplate(appCode=K.APP, viewName='signup', name='signup')
ComponentRegister.registerTemplate(appCode=K.APP, viewName='newPassword', name='newPassword')
# Home login
ComponentRegister.registerTemplate(appCode=K.APP, viewName='homeLogin', name='homeLogin')
# Activate User
ComponentRegister.registerTemplate(appCode=K.APP, viewName='activateUser', name='activateUser')
# Contact Us
ComponentRegister.registerTemplate(appCode=K.APP, viewName='contactUs', name='contactUs')
# Join Us
ComponentRegister.registerTemplate(appCode=K.APP, viewName='joinUs', name='joinUs')
# Code
ComponentRegister.registerTemplate(appCode=K.APP, viewName='code', name='code')
# Wiki
#ComponentRegister.registerTemplate(appCode=K.APP, viewName='wiki', name='wiki')


##########
# Actions
##########
ComponentRegister.cleanActions(appCode=K.APP)
# login
ComponentRegister.registerAction(appCode=K.APP, actionName='doLogin', myClass=business.LoginBusiness, method='doLogin')
ComponentRegister.registerAction(appCode=K.APP, actionName='doNewPassword', myClass=business.LoginBusiness, method='doNewPassword')
ComponentRegister.registerAction(appCode=K.APP, actionName='doPasswordReminder', myClass=business.LoginBusiness, method='doPasswordReminder')
ComponentRegister.registerAction(appCode=K.APP, actionName='doLogout', myClass=business.LoginBusiness, method='doLogout')
# signup
ComponentRegister.registerAction(appCode=K.APP, actionName='doSignupUser', myClass=business.SignupBusiness, method='doUser')
# user
ComponentRegister.registerAction(appCode=K.APP, actionName='doChangePassword', myClass=business.UserBusiness, method='doChangePassword')
# activateUser
ComponentRegister.registerAction(appCode=K.APP, actionName='activateUser', myClass=business.SignupBusiness, method='activateUser',
				hasUrl=True, hasAuth=False)
# contactUs
ComponentRegister.registerAction(appCode=K.APP, actionName='contactUs', myClass=business.HomeBusiness, method='contactUs')
# joinUs
ComponentRegister.registerAction(appCode=K.APP, actionName='joinUs', myClass=business.HomeBusiness, method='joinUs')


##########
# Flows
##########
ComponentRegister.cleanFlows(appCode=K.APP)
# login
ComponentRegister.registerFlow(appCode=K.APP, flowCode='login')
ComponentRegister.registerFlowView(appCode=K.APP, flowCode='login', viewNameSource='login', viewNameTarget='homeLogin', 
				actionName='doLogin', order=10)

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
# Login Home Menu
ComponentRegister.registerMenu(appCode=K.APP, name='homeLogin', titleShort='Home', title='Home', iconName='iconHome', viewName='homeLogin')
ComponentRegister.registerMenu(appCode=K.APP, name='home', titleShort='Home', title='Home', iconName='iconHome', viewName='home')
# Site Pages
ComponentRegister.registerMenu(appCode=K.APP, name='contactUs', titleShort='Contact Us', title='Contact Us', iconName='iconContactUs', 
			viewName='contactUs')
ComponentRegister.registerMenu(appCode=K.APP, name='joinUs', titleShort='Join Us', title='Join Our Developer Community', 
			iconName='iconUsers', viewName='joinUs')
ComponentRegister.registerMenu(appCode=K.APP, name='code', titleShort='Code', title='Get the Code', iconName='iconEngine', viewName='code')
#ComponentRegister.registerMenu(appCode=K.APP, name='wiki', titleShort='Wiki', title='Info on Developing Apps', iconName='iconWiki', viewName='wiki')

###############
# View Menus
###############
ComponentRegister.registerViewMenu(appCode=K.APP, viewName='homeLogin', menus=[
				{_K.ZONE: _Ch.MENU_ZONE_SYS, _K.MENU_NAME: 'sys'},
				{_K.ZONE: _Ch.MENU_ZONE_SYS, _K.GROUP: 'sys', _K.MENU_NAME: 'homeLogin'},
				{_K.ZONE: _Ch.MENU_ZONE_SYS, _K.GROUP: 'sys', _K.MENU_NAME: 'changePassword'},
				{_K.ZONE: _Ch.MENU_ZONE_SYS, _K.GROUP: 'sys', _K.MENU_NAME: 'signout'},
				{_K.ZONE: _Ch.MENU_ZONE_MAIN, _K.MENU_NAME: 'homeLogin'}
			])

"""ComponentRegister.registerViewMenu(appCode='testScrap', viewName='homeLogin', menus=[
				{_K.ZONE: _Ch.MENU_ZONE_VIEW, _K.MENU_NAME: 'scrap'}
			])"""

ComponentRegister.registerViewMenu(appCode=K.APP, viewName='home', menus=[
				#{_K.ZONE: _Ch.MENU_ZONE_MAIN, _K.MENU_NAME: 'home'},
				{_K.ZONE: _Ch.MENU_ZONE_VIEW, _K.MENU_NAME: 'code'},
				#{_K.ZONE: _Ch.MENU_ZONE_VIEW, _K.MENU_NAME: 'wiki'},
				{_K.ZONE: _Ch.MENU_ZONE_VIEW, _K.MENU_NAME: 'joinUs'},
				{_K.ZONE: _Ch.MENU_ZONE_VIEW, _K.MENU_NAME: 'contactUs'}
			])
# contactUs
ComponentRegister.registerViewMenu(appCode=K.APP, viewName='contactUs', menus=[
			])
# joinUs
ComponentRegister.registerViewMenu(appCode=K.APP, viewName='joinUs', menus=[
				{_K.ZONE: _Ch.MENU_ZONE_VIEW, _K.MENU_NAME: 'code'}
			])
# code
ComponentRegister.registerViewMenu(appCode=K.APP, viewName='code', menus=[
				{_K.ZONE: _Ch.MENU_ZONE_VIEW, _K.MENU_NAME: 'joinUs'}
			])
# wiki

##########
# Search
##########
ComponentRegister.cleanSearch(K.APP)
ComponentRegister.registerSearch(text='Change Password', appCode=K.APP, viewName='changePassword')
