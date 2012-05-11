from ximpia.core.business import ComponentRegister
from constants import Constants as K
from ximpia.core.choices import Choices as _Ch
from ximpia.core.constants import CoreConstants as _K

from business import LoginView, SignupView, HomeView
from business import LoginAction, SignupAction

# TODO: Is commit safe????

###############
# Parameters
###############
ComponentRegister.registerParam(appCode=K.APP, name='myFirstParan', title='My favorite parameter', paramType=_Ch.BASIC_TYPE_STR)
ComponentRegister.registerParam(appCode=K.APP, name='ximpiaId', title='XimpiaId', paramType=_Ch.BASIC_TYPE_STR)


###############
# Menu
###############
# Ximpia Menu
ComponentRegister.cleanMenu(K.APP)
ComponentRegister.registerMenu(appCode=K.APP, name='sys', titleShort='Ximpia', title='Ximpia', iconName='iconLogo')
ComponentRegister.registerMenu(appCode=K.APP, name='signout', titleShort='Sign out', title='Sign out', iconName='iconLogout')
# Home Menu
ComponentRegister.registerMenu(appCode=K.APP, name='home', titleShort='Home', title='Home', iconName='iconHome', viewName='home')


##########
# Views
##########
# login
ComponentRegister.registerView(appCode=K.APP, viewName='login', myClass=LoginView, method='showLogin')
ComponentRegister.registerView(appCode=K.APP, viewName='newPassword', myClass=LoginView, method='showNewPassword')
# signup
ComponentRegister.registerView(appCode=K.APP, viewName='signup', myClass=SignupView, method='showSignupUser')
# home
ComponentRegister.registerView(appCode=K.APP, viewName='home', myClass=HomeView, method='showStatus',
			menus=[
				{_K.ZONE: 'sys', _K.MENU_NAME: 'sys'},
				{_K.ZONE: 'sys', _K.GROUP: 'sys', _K.MENU_NAME: 'signout'},
				{_K.ZONE: 'main', _K.MENU_NAME: 'home'}
			])


#############
# Templates
#############
ComponentRegister.registerTemplate(appCode=K.APP, viewName='home', name='home', winType=_Ch.WIN_TYPE_WINDOW)
ComponentRegister.registerTemplate(appCode=K.APP, viewName='login', name='login', winType=_Ch.WIN_TYPE_WINDOW)
ComponentRegister.registerTemplate(appCode=K.APP, viewName='login', name='passwordReminder', winType=_Ch.WIN_TYPE_POPUP)

##########
# Actions
##########
# login
ComponentRegister.registerAction(appCode=K.APP, actionName='doLogin', myClass=LoginAction, method='doLogin')
ComponentRegister.registerAction(appCode=K.APP, actionName='doNewPassword', myClass=LoginAction, method='doNewPassword')
ComponentRegister.registerAction(appCode=K.APP, actionName='doPasswordReminder', myClass=LoginAction, method='doPasswordReminder')
# signup
ComponentRegister.registerAction(appCode=K.APP, actionName='doSignupUser', myClass=SignupAction, method='doUser')


##########
# Flows
##########
ComponentRegister.registerFlow(appCode=K.APP, flowCode='login', viewNameSource='login', viewNameTarget='home', actionName='doLogin')

##########
# Search
##########
ComponentRegister.cleanSearch(K.APP)
ComponentRegister.registerSearch(text='This is a simple sample of text', appCode=K.APP, viewName='home')
