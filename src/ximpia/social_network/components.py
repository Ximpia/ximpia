from ximpia.core.business import ComponentRegister
from constants import Constants as K
from ximpia.core.choices import Choices as CoreChoices

from business import LoginView, SignupView, HomeView
from business import LoginAction, SignupAction

###############
# Parameters
###############
ComponentRegister.registerParam(appCode=K.APP, name='myFirstParan', title='My favorite parameter', paramType=CoreChoices.BASIC_TYPE_STR)
ComponentRegister.registerParam(appCode=K.APP, name='ximpiaId', title='XimpiaId', paramType=CoreChoices.BASIC_TYPE_STR)


##########
# Views
##########
# login
ComponentRegister.registerView(appCode=K.APP, viewName='login', myClass=LoginView, method='showLogin')
ComponentRegister.registerView(appCode=K.APP, viewName='newPassword', myClass=LoginView, method='showNewPassword')
# signup
ComponentRegister.registerView(appCode=K.APP, viewName='signup', myClass=SignupView, method='showSignupUser')
# home
ComponentRegister.registerView(appCode=K.APP, viewName='home', myClass=HomeView, method='showStatus')


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
