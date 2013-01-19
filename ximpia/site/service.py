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
from ximpia.core.data import CoreParameterDAO
from ximpia.core.forms import DefaultForm

# Settings
from ximpia.core.util import getClass
settings = getClass(os.getenv("DJANGO_SETTINGS_MODULE"))

# Logging
import logging.config
logging.config.dictConfig(settings.LOGGING)
logger = logging.getLogger(__name__)

# Constants
import ximpia.core.constants as CoreK
import constants as K

import forms
from data import ParamDAO, UserChannelDAO, UserDAO, GroupDAO, SettingDAO, SignupDataDAO, SocialNetworkUserDAO, UserMetaDAO, UserProfileDAO
from data import UserChannelGroupDAO, UserAddressDAO, AddressDAO, GroupSysDAO, MetaKeyDAO, InvitationDAO
from forms import UserSignupInvitationForm, UserSignupForm #@UnusedImport
import messages as _m

class SiteService ( CommonService ):
	
	def __init__(self, ctx):
		super(SiteService, self).__init__(ctx)
	
	@ValidationDecorator()
	def _authenUser(self):
		"""if self._f()['authSource'] == K.FACEBOOK:
			ximpiaId = 'fb_'+ self._f()['facebookId']"""
		self._ctx.user = self._authenticateUser(self._f()['username'], self._f()['password'], 'password', _m.ERR_wrongPassword)
		logger.debug('user: %s' % (self._ctx.user) )
		"""self._ctx.user = self._authenticateUser(	ximpiaId = ximpiaId, 
						token = self._f()['facebookToken'], 
						errorTuple = _m.ERR_wrongPassword	)"""
	
	@ValidationDecorator()
	def _validateUserNotSignedUp(self):
		"""Validate user and email in system in case sign up with user/password. In case signup with social
		networks, only validate that username does not exist."""
		if self._f()['authSource'] == K.PASSWORD:
			self._validateNotExists([
						[self._dbUser, {'username': self._f()['username']}, 'username', _m.ERR_ximpiaId],
						[self._dbUser, {'email': self._f()['email']}, 'email', _m.ERR_email]
						])
		else:
			self._validateNotExists([
				[self._dbUser, {'username': self._f()['username']}, 'username', _m.ERR_ximpiaId],
				[self._dbSocialNetworkUser, {'socialId': self._f()['socialId']}, 'socialNet', _m.ERR_socialIdExists]
				])
	
	@ValidationDecorator()
	def _validateInvitationPending(self, invitationCode):
		"""
		Validates that invitation is pending
		"""
		setting = self._getSetting(K.SET_SITE_SIGNUP_INVITATION)
		logger.debug('_validateInvitationPending :: setting: %s value: %s' % (K.SET_SITE_SIGNUP_INVITATION, setting.isChecked()) )
		if setting.isChecked():
			self._validateExists([
					[self._dbInvitation, {'invitationCode': invitationCode, 'status': K.PENDING}, 
							'invitationCode', _m.ERR_invitationNotValid]
									])
	
	@ValidationDecorator()
	def _validateInvitationNotUsed(self):
		"""
		Validates that invitation is valid: Checks that invitation has not been used in case invitations defined in settings
		"""
		setting = self._getSetting(K.SET_SITE_SIGNUP_INVITATION)
		logger.debug('_validateInvitationNotUsed :: setting: %s value: %s' % (K.SET_SITE_SIGNUP_INVITATION, setting.isChecked()) )
		if setting.isChecked():
			self._validateNotExists([
					[self._dbInvitation, {'invitationCode': self._f()['invitationCode'], 'status': K.USED}, 
							'invitationCode', _m.ERR_invitationNotValid]
									])
	
	def _createUser(self):
		"""
		Create user
		
		Will create user and related information
		
		1. Creates django user
		2. Sets password
		3. Creates UserChannel
		4. Obtains params statusActive, addressTypePersonal
		5. Gets or create address with city and country
		6. Creates UserProfile with user and status active
		7. Creates UserAddress with userProfile, address and addressTypePersonal
		8. Creates user meta variable HAS_VALIDATED_EMAIL to 'True'
		9. In case social network signup, links socialId, socialToken
		10. Associates django groups and ximpia groups to user
		
		** Returns**
		None
		"""
		# System User
		user = self._dbUser.create(username=self._f()['username'], email=self._f()['email'], 
						first_name=self._f()['firstName'], last_name=self._f()['lastName'])
		if self._f()['authSource'] == 'password':
			user.set_password(self._f()['password'])
		user.save()
		# Ximpia User
		userChannel = self._dbUserChannel.create(user=user, name=K.USER, title=self._f()['firstName'], userCreateId=user.id)
		# Profile (Address, UserProfile, UserAddress)
		statusActive = self._dbParam.getUserStatusActive()
		address, created = self._dbAddress.getCreate(city=self._f()['city'], country=self._f()['country'])
		addressTypePersonal = self._dbParam.getAddressTypePersonal()
		userProfile = self._dbUserProfile.create(user=user, status=statusActive)
		userAddress = self._dbUserAddress.create(userProfile=userProfile, address=address, type=addressTypePersonal)
		# User Meta
		keyEmail = self._dbMetaKey.get(name=K.KEY_HAS_VALIDATED_EMAIL)
		self._dbUserMeta.create(user=user, meta=keyEmail, value='True')
		# Social networks
		if self._f()['authSource'] != 'password':
			socialNetwork = self._dbCoreParam.get(mode=CoreK.NET, name=self._f()['authSource'])
			self._dbSocialNetworkUser.create(user=user, socialNetwork=socialNetwork, 
							socialId=self._f()['socialId'], token=self._f()['socialToken'])			
		# Groups
		userGroupId = json.loads(self._f()['params'])['userGroup']
		groupSys = self._dbGroupSys.get(id=userGroupId)
		user.groups.add(groupSys)
		group = self._dbGroup.get(group__group=groupSys)
		self._dbUserChannelGroup.create(userChannel=userChannel, group=group)
		# Invitation
		setInvitation = self._getSetting(K.SET_SITE_SIGNUP_INVITATION)
		if setInvitation.isChecked() and self._f()['invitationCode'] != '':
			invitation = self._dbInvitation.get(invitationCode=self._f()['invitationCode'])
			invitation.status = K.USED
			invitation.save()
	
	@ValidationDecorator()
	def _validateUser(self):
		"""Validate user: Check user password"""
		self._ctx.user = self._authenticateUser(self._ctx.user, self._f()['password'], 'password', _m.ERR_wrongPassword)
	
	@ValidationDecorator()
	def _validateReminder(self, username, reminderId):
		days = self._dbParam.get(mode=K.PARAM_LOGIN, name=K.PARAM_REMINDER_DAYS).valueId
		newDate = date.today() + timedelta(days=days)
		logger.debug( 'New Password Data : username: %s newDate: %s reminderId: %s' % (username, newDate, reminderId) )
		# Show actual password, new password and confirm new password
		self._validateExists([
					[self._dbUserSys, {'username': username}, 'username', _m.ERR_changePassword],
					[self._dbUserDetail, {	'user__username': username, 
											'reminderId': reminderId, 
											'resetPasswordDate__lte' : newDate}, 'noField', _m.ERR_changePassword],
					])
	
	@ValidationDecorator()
	def _validateEmailExist(self):
		self._validateExists([
					[self._dbUserSys, {'email': self._f()['email']}, 'email', _m.ERR_emailDoesNotExist]
				])
	
	def _doDbInstancesForUser(self):
		"""
		Instances for user creation
		"""
		self._dbSettings = SettingDAO(self._ctx)
		self._dbSignupData = SignupDataDAO(self._ctx)
		self._dbUser = UserDAO(self._ctx)
		self._dbSocialNetworkUser = SocialNetworkUserDAO(self._ctx)
		self._dbUserProfile = UserProfileDAO(self._ctx)
		self._dbUserChannel = UserChannelDAO(self._ctx)
		self._dbUserChannelGroup = UserChannelGroupDAO(self._ctx)
		self._dbAddress = AddressDAO(self._ctx)
		self._dbUserAddress = UserAddressDAO(self._ctx)
		self._dbMetaKey= MetaKeyDAO(self._ctx)
		self._dbUserMeta = UserMetaDAO(self._ctx)
		self._dbGroup = GroupDAO(self._ctx)
		self._dbGroupSys = GroupSysDAO(self._ctx)
		self._dbParam = ParamDAO(self._ctx)
		self._dbCoreParam = CoreParameterDAO(self._ctx)
		self._dbInvitation = InvitationDAO(self._ctx)
	
	@WorkflowViewDecorator('login', form=forms.LoginForm)
	def viewLogin(self):
		"""Checks if user is logged in. If true, get login user information in the context
		@param ctx: Context
		@return: result"""
		# Check if login:
		logger.debug( 'login...' )
		if not self._ctx.user.is_authenticated():
			# no login: login form
			self._setMainForm(forms.LoginForm())
			# Popup - Password reminder
			self._addForm(forms.PasswordReminderForm())
	
	@ViewDecorator(DefaultForm)
	def viewLogout(self):
		"""Show logout view"""
		pass
	
	@ViewDecorator(DefaultForm)
	def viewHomeLogin(self):
		"""Show home after login"""
		pass
	
	@WorkflowActionDecorator('login', forms.LoginForm)
	def login(self):
		"""
		Performs the login action. Puts workflow parameter username, write context variables userChannel and session.
		
		** Decorator **
		
		* ``@WorkflowActionDecorator('login', forms.LoginForm)`` : Flow code ``login``and form LoginForm.
		
		** Attributes **
		
		** Returns **
		
		None
		"""
		logger.debug( '***************************************************' )
		logger.debug( 'login...' )
		logger.debug( '***************************************************' )
		#logger.debug( 'form: %s' % (self._ctx.form) )
		self._authenUser()
		logger.debug( 'login :: user: %s' % (self._ctx.user) )
		self._login()
		
		# Checks if we have password
		# If password, normal login
		# If not password and socialId and token, authen with social id
		# Put parameters for login
		
		#self._putFlowParams(username=self._ctx.user.username.encode(settings.DEFAULT_CHARSET))		
		logger.debug( 'login :: Session: %s' % (self._ctx.session) )
		logger.debug( 'login :: user: %s' % (self._ctx.user) )
		logger.debug( 'login :: cookies: %s' % (self._ctx.cookies) )
		userChannelName = self._getUserChannelName()
		logger.debug( 'login :: userChannelName: %s' % (userChannelName) )
		self._dbUserChannel = UserChannelDAO(self._ctx)
		self._ctx.userChannel = self._dbUserChannel.get(user=self._ctx.user, name=userChannelName)
		self._ctx.session['userChannel'] = self._ctx.userChannel
		logger.debug( 'login :: userChannel: %s' % (self._ctx.userChannel) )
	
	@ActionDecorator(forms.UserSignupInvitationForm)
	def signup(self):
		"""
		Signup user
		
		**Attributes**
		
		**Returns**
		"""
		# Instances
		self._doDbInstancesForUser()
		# Business Validation
		self._validateUserNotSignedUp()
		self._validateInvitationNotUsed()
		if self._f()['authSource'] != K.PASSWORD:
			self._createUser()
			# set ok message
			self._setOkMsg('OK_SOCIAL_SIGNUP')
		else:
			# user/password. Save in temp table user data
			activationCode = random.randrange(10, 100)
			logger.debug( 'doUser :: activationCode: %s' % (activationCode) )
			formSerialized = base64.encodestring(self._f().serializeJSON())
			self._dbSignupData.deleteIfExists(user=self._f()['username'], real=True)
			self._dbSignupData.create(user=self._f()['username'], data=formSerialized, activationCode=activationCode)
			# Send email to user to validate email
			xmlMessage = self._dbSettings.get(name__name='Msg/Site/Signup/User/_en').value
			logger.debug( xmlMessage )
			logger.debug('path: %s' % (self._ctx.path) )
			EmailService.send(xmlMessage, {'scheme': settings.XIMPIA_SCHEME, 
							'host': settings.XIMPIA_BACKEND_HOST,
							'appSlug': K.Slugs.SITE,
							'activate': K.Slugs.ACTIVATE_USER,
							'firstName': self._f()['firstName'], 
							'user': self._f()['username'],
							'activationCode': activationCode}, settings.XIMPIA_WEBMASTER_EMAIL, [self._f()['email']])
			logger.debug( 'doUser :: sent Email' )
			# set ok message
			self._setOkMsg('OK_USER_SIGNUP')
	
	@ViewDecorator(forms.ActivateUserForm)
	def viewActivationUser(self):
		"""Confirmation message for user activation"""
		pass
	
	@ViewDecorator(forms.ActivateUserForm)
	def activateUser(self, username, activationCode):
		"""Create user in system with validation link from email. Only used in case auth source is user/password."""
		# Instances
		self._doDbInstancesForUser()
		logger.debug('activateUser...')
		# Logic
		formStr64 = self._dbSignupData.get(user=username).data
		formDict = json.loads(base64.decodestring(formStr64))
		form = forms.UserSignupInvitationForm(formDict, ctx=self._ctx)
		self._setForm(form)
		# validate form again
		self._validateUserNotSignedUp()
		# Create user
		self._createUser() 
		self._dbSignupData.deleteIfExists(user=username, real=True)
		# show view
		self._showView(K.Views.ACTIVATION_USER) 
	
	@ViewDecorator(forms.UserSignupInvitationForm)
	def viewSignup(self, invitationCode=None):
		"""Show signup form. Get get invitation code."""
		self._dbInvitation = InvitationDAO(self._ctx)
		logger.debug('viewSignup :: invitationCode: %s' % (invitationCode) )
		self._addAttr('isSocialLogged', False)
		setInvitation = self._getSetting(K.SET_SITE_SIGNUP_INVITATION)
		self._validateInvitationPending(invitationCode)
		if invitationCode != None and setInvitation.isChecked():
			# Add invitation code to form form_signup
			invitation = self._dbInvitation.get(invitationCode=invitationCode, status=K.PENDING)
			self._addFormValue('invitationCode', invitationCode)
			self._addFormValue('email', invitation.email)
			self._f().disableFields(['invitationCode', 'email'])
	
	@MenuActionDecorator('logout')
	def logout(self):
		"""Logout user"""
		logger.debug( 'doLogout...' )
		self._logout()
		logger.debug( 'doLogout :: WF Data: %s' % (self._getWFUser()) )
		self._wf.removeData(self._getWFUser(), 'login')
		logger.debug( 'doLogout :: did logout...' )
		
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
	def viewReminderNewPassword(self, username=None, reminderId=None):
		"""Shows form to enter new password and confirm new password. Save button will call doNewPassword.
		@param username: username
		@param reminderId: reminderId"""
		self._validateReminder(username, reminderId)
		self._f().putParamList(username=username)
	
	@ActionDecorator(forms.PasswordReminderForm)
	def requestReminder(self):
		"""Checks that email exists, then send email to user with reset link"""
		self._validateEmailExist()
		# Update User
		user = self._dbUserSys.get(email = self._f()['email'])
		userDetail = self._dbUserDetail.get(user=user) 
		days = self._dbParam.get(mode=K.PARAM_LOGIN, name=K.PARAM_REMINDER_DAYS).valueId
		newDate = date.today() + timedelta(days=days)
		#logger.debug( 'newDate: %s %s' % (newDate, type(newDate)) )
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
		user = self._dbUserSys.get(username= self._f().getParam('username'))
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
