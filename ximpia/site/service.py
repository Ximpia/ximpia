import random
import simplejson as json
import base64
import os
from datetime import date, timedelta

from django.contrib.auth.models import User
from ximpia.core.models import JsResultDict

from ximpia.core.service import EmailService, CommonService
from ximpia.core.service import ViewDecorator, ActionDecorator, ValidationDecorator, MenuActionDecorator, WorkflowViewDecorator,\
		WorkflowActionDecorator
from ximpia.core.models import Context as CoreContext
from ximpia.core.forms import DefaultForm

# Settings
from ximpia.core.util import getClass
settings = getClass(os.getenv("DJANGO_SETTINGS_MODULE"))

# Logging
import logging.config
logging.config.dictConfig(settings.LOGGING)
logger = logging.getLogger(__name__)

import forms
from data import ParamDAO, UserChannelDAO, UserDAO, GroupDAO, SettingsDAO, SignupDataDAO, SocialNetworkUserDAO
from forms import UserSignupInvitationForm #@UnusedImport
import messages as _m
import constants as K

# TODO: Resolve pageError=True attribute for decorators

class SiteService ( CommonService ):
	
	def __init__(self, ctx):
		super(SiteService, self).__init__(ctx)
	
	@ValidationDecorator()
	def _authenUser(self):
		# TODO: Integrate signup mode from settings
		if self._f()['authSource'] == K.FACEBOOK:
			ximpiaId = 'fb_'+ self._f()['facebookId']
		self._ctx.user = self._authenticateUser(	ximpiaId = ximpiaId, 
						token = self._f()['facebookToken'], 
						errorTuple = _m.ERR_wrongPassword	)
	
	@ValidationDecorator()
	def _validateUserNotSignedUp(self):
		"""Validate user and email in system in case sign up with user/password. In case signup with social
		networks, only validate that ximpiaId does not exist."""
		# TODO: Integrate signup mode from settings
		if self._f()['authSource'] == K.PASSWORD:
			self._validateNotExists([
						[self._dbUser, {'username': self._f()['ximpiaId']}, 'ximpiaId', _m.ERR_ximpiaId],
						[self._dbUser, {'email': self._f()['email']}, 'email', _m.ERR_email]
						])
		else:
			self._validateNotExists([
				[self._dbUser, {'username': self._f()['ximpiaId']}, 'ximpiaId', _m.ERR_ximpiaId],
				[self._dbSocialNetworkUser, {'socialId': self._f()['socialId']}, 'socialNet', _m.ERR_socialIdExists]
				])
	
	def _createUser(self):
		"""Create user """
		# System User
		user = self._dbUser.create(username=self._f()['ximpiaId'], email=self._f()['email'], 
						first_name=self._f()['firstName'], last_name=self._f()['lastName'])
		if self._f()['authSource'] == 'password':
			user.set_password(self._f()['password'])
		user.save()
		# Ximpia User
		userChannel = self._dbUserChannel.create(user=user, name=K.USER, title=self._f()['firstName'], userCreateId=user.id)
		userDetail = self._dbUserDetail.create(user=user, name=self._f()['firstName'] + ' ' + self._f()['lastName'], #@UnusedVariable
						hasValidatedEmail=True)
		# Social networks
		if self._f()['authSource'] != 'password':
			self._dbSocialNetworkUser.create(user=userDetail, socialNetwork=self._f()['authSource'], 
							socialId=self._f()['socialId'], token=self._f()['socialToken'])			
		# Groups
		userGroupId = json.loads(self._f()['params'])['userGroup']
		group = self._dbGroup.get(id=userGroupId)
		user.groups.add(group)
		userChannel.groups.add(group)
	
	@ValidationDecorator()
	def _validateUser(self):
		"""Validate user: Check user password"""
		self._ctx.user = self._authenticateUser(self._ctx.user, self._f()['password'], 'password', _m.ERR_wrongPassword)
	
	@ValidationDecorator()
	def _validateReminder(self, ximpiaId, reminderId):
		days = self._dbParam.get(mode=K.PARAM_LOGIN, name=K.PARAM_REMINDER_DAYS).valueId
		newDate = date.today() + timedelta(days=days)
		logger.debug( 'New Password Data : ', ximpiaId, newDate, reminderId )
		# Show actual password, new password and confirm new password
		self._validateExists([
					[self._dbUserSys, {'username': ximpiaId}, 'ximpiaId', _m.ERR_changePassword],
					[self._dbUserDetail, {	'user__username': ximpiaId, 
								'reminderId': reminderId, 
								'resetPasswordDate__lte' : newDate}, 'noField', _m.ERR_changePassword],
					])
	
	@ValidationDecorator()
	def _validateEmailExist(self):
		self._validateExists([
					[self._dbUserSys, {'email': self._f()['email']}, 'email', _m.ERR_emailDoesNotExist]
				])
	
	@WorkflowViewDecorator('login', form=forms.HomeForm)
	def viewLogin(self):
		"""Checks if user is logged in. If true, get login user information in the context
		@param ctx: Context
		@return: result"""
		# Check if login:
		logger.debug( 'login...' )
		if not self._ctx['user'].is_authenticated():
			# no login: login form
			self._setMainForm(forms.LoginForm())
			self._ctx.jsData.addAttr('isLogin', False)
			# Popup - Password reminder
			self._addForm(forms.PasswordReminderForm())
	
	@ViewDecorator(DefaultForm)
	def viewLogout(self):
		"""Show logout view"""
		self._ctx.jsData.addAttr('isLogin', False)
	
	@WorkflowActionDecorator('login', forms.LoginForm)
	def login(self):
		"""Performs the login action
		@param ctx: Context
		@return: result"""
		logger.debug( '***************************************************' )
		logger.debug( 'doLogin...' )
		logger.debug( '***************************************************' )
		"""logger.debug( 'form: ', self._ctx[Ctx.FORM] )
		self._authenUser()
		logger.debug( 'user: ', self._ctx[Ctx.USER] )
		self._login()
		self._putFlowParams(ximpiaId=self._ctx[Ctx.USER].username.encode(settings.DEFAULT_CHARSET))		
		logger.debug( 'Session: ', self._ctx[Ctx.SESSION] )
		logger.debug( 'user: ', self._ctx[Ctx.USER] )
		logger.debug( 'cookies: ', self._ctx[Ctx.COOKIES] )
		userChannelName = self._getUserChannelName()
		logger.debug( 'userChannelName: ', userChannelName )
		self._ctx[Ctx.USER_CHANNEL] = self._dbUserChannel.get(user=self._ctx[Ctx.USER], name=userChannelName)
		self._ctx[Ctx.SESSION]['userChannel'] = self._ctx['userChannel']
		logger.debug( 'userChannel: ', self._ctx['userChannel'] ) """
	
	@ActionDecorator(forms.UserSignupInvitationForm)
	def signup(self):
		"""Signup user
		@param ctx: Context"""
		# Business Validation
		self._validateInvUserSignup()
		if self._f()['authSource'] != K.PASSWORD:
			self._createUser()
		else:
			# user/password. Save in temp table user data
			activationCode = random.randrange(10, 100)
			logger.debug( 'doUser :: activationCode: ', activationCode )
			formSerialized = base64.encodestring(self._f().serializeJSON())
			self._dbSignupData.deleteIfExists(user=self._f()['ximpiaId'])
			self._dbSignupData.create(user=self._f()['ximpiaId'], data=formSerialized, activationCode=activationCode)
			# Send email to user to validate email
			xmlMessage = self._dbXmlMessage.get(name='Msg/Site/Signup/User/', lang='en').body
			logger.debug( xmlMessage )
			EmailService.send(xmlMessage, {'scheme': settings.XIMPIA_SCHEME, 
							'host': settings.XIMPIA_BACKEND_HOST,
							'app': self._ctx.app,
							'firstName': self._f()['firstName'], 
							'user': self._f()['ximpiaId'],
							'activationCode': activationCode}, [self._f()['email']])
			logger.debug( 'doUser :: sent Email' )
	
	@ViewDecorator(forms.ActivateUserForm)
	def viewActivationUser(self):
		"""Confirmation message for user activation"""
		pass
	
	@ActionDecorator(forms.ActivateUserForm)
	def activateUser(self, ximpiaId, activationCode):
		"""Create user in system with validation link from email. Only used in case auth source is user/password."""
		formStr64 = self._dbSignupData.get(user=ximpiaId).data
		formDict = json.loads(base64.decodestring(formStr64))
		form = forms.UserSignupInvitationForm(formDict, ctx=self._ctx)
		self._setForm(form)
		# validate form again
		self._validateInvUserSignup()
		# Create user
		self._createUser() 
		self._dbSignupData.deleteIfExists(user=ximpiaId)
		# show view
		self._showView('activateUser')
	
	@ViewDecorator(forms.UserSignupInvitationForm)
	def viewSignup(self):
		"""Show signup form. Get get invitation code."""
		pass
	
	@MenuActionDecorator('logout')
	def logout(self):
		"""Logout user"""
		logger.debug( 'doLogout...' )
		self._logout()
		logger.debug( 'doLogout :: WF Data: ', self._getWFUser() )
		self._wf.removeData(self._getWFUser(), 'login')
		logger.debug( 'did logout...' )
		
	@ViewDecorator(forms.UserChangePasswordForm)
	def viewChangePassword(self):
		"""Change password form with current password and new password"""
		pass
	
	@ActionDecorator(forms.UserChangePasswordForm)
	def changePassword(self):
		"""Change password from user area"""
		self._validateUser()
		user = self._dbUserSys.get(username= self._ctx.user)
		user.set_password(self._f()['newPassword'])
		user.save()
	
	@ViewDecorator(forms.ChangePasswordForm)
	def viewReminderNewPassword(self, ximpiaId=None, reminderId=None):
		"""Shows form to enter new password and confirm new password. Save button will call doNewPassword.
		@param ximpiaId: ximpiaId
		@param reminderId: reminderId"""
		self._validateReminder(ximpiaId, reminderId)
		self._f().putParamList(ximpiaId=ximpiaId)
	
	@ActionDecorator(forms.PasswordReminderForm)
	def requestReminder(self):
		"""Checks that email exists, then send email to user with reset link"""
		self._validateEmailExist()
		# Update User
		user = self._dbUserSys.get(email = self._f()['email'])
		userDetail = self._dbUserDetail.get(user=user) 
		days = self._dbParam.get(mode=K.PARAM_LOGIN, name=K.PARAM_REMINDER_DAYS).valueId
		newDate = date.today() + timedelta(days=days)
		#logger.debug( 'newDate: ', newDate, type(newDate) )
		#userDetail.resetPasswordDate = datetime.date(newDate)
		userDetail.resetPasswordDate = newDate
		# Set reminderId
		userDetail.reminderId = str(random.randint(1, 999999))
		userDetail.save()
		# Send email with link to reset password. Link has time validation
		xmlMessage = self._dbXmlMessage.get(name='Msg/SocialNetwork/Login/PasswordReminder/', lang='en').body
		EmailService.send(xmlMessage, {'scheme': settings.XIMPIA_SCHEME, 
						'host': settings.XIMPIA_BACKEND_HOST,
						'firstName': user.first_name, 
						'userAccount': user.username,
						'reminderId': userDetail.reminderId}, [self._f()['email']])
		self._setOkMsg('OK_PASSWORD_REMINDER')
	
	@ActionDecorator(forms.ChangePasswordForm)
	def finalizeReminder(self):
		"""Saves new password, it does authenticate and login user."""
		user = self._dbUserSys.get(username= self._f().getParam('ximpiaId'))
		user.set_password(self._f()['newPassword'])
		user.save()
		userDetail = self._dbUserDetail.get(user=user)
		userDetail.reminderId = None
		userDetail.resetPasswordDate = None
		userDetail.save()
		#login(self._ctx[Ctx.RAW_REQUEST], user)

class Context ( CoreContext ):
	
	def __init__(self):
		super(Context, self).__init__()



































# =========================================
# Eclipse Dumb Classes for code completion
# =========================================

class ContextDumbClass (object):
	def __init__(self):
		if False: self._ctx = Context()
		if False: self._ctx.user = User()
		if False: self._ctx.jsData = JsResultDict()
