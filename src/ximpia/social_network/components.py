from ximpia.core.business import ComponentRegister
from constants import Constants as K

from business import LoginView, SignupView
from business import LoginAction, SignupAction

##########
# Views
##########
# login
ComponentRegister.registerView('login', K.APP, LoginView, 'showLogin')
ComponentRegister.registerView('newPassword', K.APP, LoginView, 'showNewPassword')
# signup
ComponentRegister.registerView('signup', K.APP, SignupView, 'showSignupUser')

##########
# Actions
##########
# login
ComponentRegister.registerAction('doLogin', K.APP, LoginAction, 'doLogin')
ComponentRegister.registerAction('doNewPassword', K.APP, LoginAction, 'doNewPassword')
ComponentRegister.registerAction('doPasswordReminder', K.APP, LoginAction, 'doPasswordReminder')
# signup
ComponentRegister.registerAction('doSignupUser', K.APP, SignupAction, 'doUser')
