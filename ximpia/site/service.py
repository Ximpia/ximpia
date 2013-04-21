# coding: utf-8

import random
import simplejson as json
import base64
import os
from datetime import date, timedelta

from django.contrib.auth.models import User
from ximpia.core.models import JsResultDict

from ximpia.core.service import EmailService, CommonService
from ximpia.core.service import view, action, validation, menu_action
from ximpia.core.models import Context as CoreContext
from ximpia.core.data import CoreParameterDAO
from ximpia.core.forms import DefaultForm

# Settings
from ximpia.core.util import get_class
settings = get_class(os.getenv("DJANGO_SETTINGS_MODULE"))

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
import messages as _m

class SiteService ( CommonService ):
	
	def __init__(self, ctx):
		super(SiteService, self).__init__(ctx)
	
	@validation()
	def _authen_user(self):
		if self._f()['authSource'] == K.FACEBOOK and self._f()['socialId'] != '':
			self._ctx.user = self._authenticate_user_soc_net(self._f()['socialId'], self._f()['socialToken'], self._f()['authSource'], 
														'facebook', _m.ERR_wrong_password)
		else:
			self._ctx.user = self._authenticate_user(self._f()['username'], self._f()['password'], 'password', _m.ERR_wrong_password)
		logger.debug('user: %s' % (self._ctx.user) )
	
	@validation()
	def _validate_user_not_signed_up(self):
		"""Validate user and email in system in case sign up with user/password. In case signup with social
		networks, only validate that username does not exist."""
		if self._f()['authSource'] == K.PASSWORD:
			self._validate_not_exists([
						[self._dbUser, {'username': self._f()['username']}, 'username', _m.ERR_ximpia_id],
						[self._dbUser, {'email': self._f()['email']}, 'email', _m.ERR_email]
						])
		else:
			self._validate_not_exists([
				[self._dbUser, {'username': self._f()['username']}, 'username', _m.ERR_ximpia_id],
				[self._dbUser, {'email': self._f()['email']}, 'email', _m.ERR_email],
				[self._dbSocialNetworkUser, {'socialId': self._f()['socialId']}, 'socialNet', _m.ERR_social_id_exists]
				])
	
	@validation()
	def _validate_invitation_pending(self, invitation_code):
		"""
		Validates that invitation is pending
		"""
		setting = self._get_setting(K.SET_SITE_SIGNUP_INVITATION)
		logger.debug('_validate_invitation_pending :: setting: %s value: %s' % (K.SET_SITE_SIGNUP_INVITATION, setting.isChecked()) )
		if setting.isChecked():
			self._validate_exists([
					[self._dbInvitation, {'invitationCode': invitation_code, 'status': K.PENDING}, 
							'invitationCode', _m.ERR_invitation_not_valid]
									])
	
	@validation()
	def _validate_invitation_not_used(self):
		"""
		Validates that invitation is valid: Checks that invitation has not been used in case invitations defined in settings
		"""
		setting = self._get_setting(K.SET_SITE_SIGNUP_INVITATION)
		logger.debug('_validateInvitationNotUsed :: setting: %s value: %s' % (K.SET_SITE_SIGNUP_INVITATION, setting.is_checked()) )
		if setting.is_checked():
			self._validate_not_exists([
					[self._dbInvitation, {'invitationCode': self._f()['invitationCode'], 'status': K.USED}, 
							'invitationCode', _m.ERR_invitation_not_valid]
									])
	
	def _create_user(self):
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
		statusActive = self._dbParam.get_user_status_active()
		address, created = self._dbAddress.get_create(city=self._f()['city'], country=self._f()['country'])
		addressTypePersonal = self._dbParam.get_address_type_personal()
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
	
	@validation()
	def _validate_user(self):
		"""Validate user: Check user password"""
		self._ctx.user = self._authenticate_user(self._ctx.user, self._f()['password'], 'password', _m.ERR_wrong_password)
	
	@validation()
	def _validate_reminder(self, username, reminderId):
		newDate = date.today()
		logger.debug( '_validateReminder :: New Password Data : username: %s newDate: %s reminderId: %s' % (username, newDate, reminderId) )
		# Show actual password, new password and confirm new password
		# 'resetPasswordDate__lte' : newDate}, 'noField', _m.ERR_changePassword],
		self._validate_exists([
					[self._dbUser, {'username': username}, 'username', _m.ERR_change_password],
					[self._dbUserMeta, {	'user__username': username,
											'meta__name': K.META_REMINDER_ID,
											'value': str(reminderId)}, 'noField', _m.ERR_change_password],
					])
		# Validate reset password date
		logger.debug('_validateReminder :: validate reset date...')
		reset_date_str = self._dbUserMeta.get(user__username=username, meta__name=K.META_RESET_PASSWORD_DATE).value
		if reset_date_str != '':
			reset_date_fields = reset_date_str.split('-')
			resetDate = date(year=int(reset_date_fields[0]), month=int(reset_date_fields[1]), day=int(reset_date_fields[2]))
			logger.debug('_validateReminder :: today: %s resetDate: %s' % (date.today(), resetDate) )
			if date.today() > resetDate:
				# show error
				self._addError('noField', _m.ERR_change_password)
		else:
			self._addError('noField', _m.ERR_change_password)
	
	@validation()
	def _validate_email_exist(self):
		self._validate_exists([
					[self._dbUser, {'email': self._f()['email']}, 'email', _m.ERR_email_does_not_exist]
				])
	
	def _do_db_instances_for_user(self):
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
	
	@view(forms.LoginForm)
	def view_login(self):
		"""Checks if user is logged in. If true, get login user information in the context
		@return: result"""
		# Check if login:
		logger.debug( 'login...' )
		self._add_attr('isSocialLogged', False)
		if not self._ctx.user.is_authenticated():
			logger.debug('viewLogin :: User not authenticated...')
			# no login: login form
			self._set_main_form(forms.LoginForm())
			# Popup - Password reminder
			self._add_form(forms.PasswordReminderForm())
		else:
			# We must redirect to homeLogin or other views
			if self._ctx.cookies.has_key(K.COOKIE_LOGIN_REDIRECT) and len(self._ctx.cookies[K.COOKIE_LOGIN_REDIRECT]) != 0:
				# We redirect to cookie value
				self._show_view(self._ctx.cookies[K.COOKIE_LOGIN_REDIRECT])
			else:
				self._show_view(K.Views.HOME_LOGIN)
	
	@view(DefaultForm)
	def view_logout(self):
		"""Show logout view"""
		pass
	
	@view(DefaultForm)
	def view_home_login(self):
		"""Show home after login"""
		pass
	
	@action(forms.LoginForm)
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
		
		logger.debug('login :: authSource: %s' % (self._f()['authSource']) )		
		
		self._authenUser()
		logger.debug( 'login :: user: %s' % (self._ctx.user) )
		self._login()
		
		# Checks if we have password
		# If password, normal login
		# If not password and socialId and token, authen with social id
		# Put parameters for login
				
		logger.debug( 'login :: Session: %s' % (self._ctx.session) )
		logger.debug( 'login :: user: %s' % (self._ctx.user) )
		logger.debug( 'login :: cookies: %s' % (self._ctx.cookies) )
		user_channel_name = self._get_user_channel_name()
		logger.debug( 'login :: userChannelName: %s' % (user_channel_name) )
		self._dbUserChannel = UserChannelDAO(self._ctx)
		self._ctx.userChannel = self._dbUserChannel.get(user=self._ctx.user, name=user_channel_name)
		self._ctx.session['userChannel'] = self._ctx.userChannel
		logger.debug( 'login :: userChannel: %s' % (self._ctx.userChannel) )
		
		# Redirect
		if self._ctx.cookies.has_key(K.COOKIE_LOGIN_REDIRECT) and len(self._ctx.cookies[K.COOKIE_LOGIN_REDIRECT]) != 0:
			self._show_view(self._ctx.cookies[K.COOKIE_LOGIN_REDIRECT])
			self._set_cookie(K.COOKIE_LOGIN_REDIRECT, '')
		else:
			self._show_view(K.Views.HOME_LOGIN)
	
	@action(forms.UserSignupInvitationForm)
	def signup(self):
		"""
		Signup user
		
		**Attributes**
		
		**Returns**
		"""
		# Instances
		self._do_db_instances_for_user()
		# Business Validation
		self._validate_user_not_signed_up()
		self._validate_invitation_not_used()
		if self._f()['authSource'] != K.PASSWORD:
			self._create_user()
			# set ok message
			self._set_ok_msg('OK_SOCIAL_SIGNUP')
		else:
			# user/password. Save in temp table user data
			activation_code = random.randrange(10, 100)
			logger.debug( 'doUser :: activation_code: %s' % (activation_code) )
			form_serialized = base64.encodestring(self._f().serialize_JSON())
			self._dbSignupData.delete_if_exists(user=self._f()['username'], is_real=True)
			self._dbSignupData.create(user=self._f()['username'], data=form_serialized, activationCode=activation_code)
			# Send email to user to validate email
			xml_message = self._dbSettings.get(name__name='Msg/Site/Signup/User/_en').value
			logger.debug( xml_message )
			logger.debug('path: %s' % (self._ctx.path) )
			EmailService.send(xml_message, {'scheme': settings.XIMPIA_SCHEME, 
							'host': settings.XIMPIA_BACKEND_HOST,
							'appSlug': K.Slugs.SITE,
							'activate': K.Slugs.ACTIVATE_USER,
							'firstName': self._f()['firstName'], 
							'user': self._f()['username'],
							'activationCode': activation_code}, settings.XIMPIA_WEBMASTER_EMAIL, [self._f()['email']])
			# set ok message
			self._set_ok_msg('OK_USER_SIGNUP')
	
	@view(forms.ActivateUserForm)
	def view_activation_user(self):
		"""Confirmation message for user activation"""
		pass
	
	@view(forms.ActivateUserForm)
	def activate_user(self, username, activation_code):
		"""Create user in system with validation link from email. Only used in case auth source is user/password."""
		# Instances
		self._do_db_instances_for_user()
		logger.debug('activate_user...')
		# Logic
		form_str_64 = self._dbSignupData.get(user=username).data
		form_dict = json.loads(base64.decodestring(form_str_64))
		form = forms.UserSignupInvitationForm(form_dict, ctx=self._ctx)
		self._setForm(form)
		# validate form again
		self._validate_user_not_signed_up()
		# Create user
		self._create_user() 
		self._dbSignupData.delete_if_exists(user=username, is_real=True)
		# show view
		self._show_view(K.Views.ACTIVATION_USER) 
	
	@view(forms.UserSignupInvitationForm)
	def view_signup(self, invitation_code=None):
		"""Show signup form. Get get invitation code."""
		self._dbInvitation = InvitationDAO(self._ctx)
		logger.debug('viewSignup :: invitationCode: %s' % (invitation_code) )
		self._add_attr('isSocialLogged', False)
		set_invitation = self._get_setting(K.SET_SITE_SIGNUP_INVITATION)
		self._validate_invitation_pending(invitation_code)
		if invitation_code != None and set_invitation.is_checked():
			# Add invitation code to form form_signup
			invitation = self._dbInvitation.get(invitationCode=invitation_code, status=K.PENDING)
			self._put_form_value('invitationCode', invitation_code)
			self._put_form_value('email', invitation.email)
			self._f().disable_fields(['invitationCode', 'email'])
	
	@menu_action('logout')
	def logout(self):
		"""Logout user
		"""
		self._logout()
		
	@view(forms.UserChangePasswordForm)
	def view_change_password(self):
		"""Change password form with current password and new password
		"""
		self._put_form_value('username', self._ctx.user.username)
	
	@action(forms.UserChangePasswordForm)
	def change_password(self):
		"""Change password from user area
		"""
		self._dbUser = UserDAO(self._ctx)
		self._validate_user()
		user = self._dbUser.get(username= self._ctx.user)
		user.set_password(self._f()['newPassword'])
		user.save()
	
	@view(forms.ChangePasswordForm)
	def view_reminder_new_password(self, username=None, reminder_id=None):
		"""Shows form to enter new password and confirm new password. Save button will call doNewPassword.
		@param username: username
		@param reminderId: reminderId"""
		self._dbUser = UserDAO(self._ctx)
		self._dbUserMeta = UserMetaDAO(self._ctx)
		self._validate_reminder(username, reminder_id)
		self._put_form_value('username', username)
		self._f().put_param_list(username=username)
	
	@action(forms.PasswordReminderForm)
	def request_reminder(self):
		"""Checks that email exists, then send email to user with reset link"""
		logger.debug('requestReminder...')
		self._dbUser = UserDAO(self._ctx)
		self._dbSetting = SettingDAO(self._ctx)
		self._dbUserMeta = UserMetaDAO(self._ctx)
		self._dbMetaKey = MetaKeyDAO(self._ctx)
		self._validate_email_exist()
		# Update User
		user = self._dbUser.get(email = self._f()['email'])
		days = self._get_setting(K.SET_REMINDER_DAYS).value
		new_date = date.today() + timedelta(days=int(days))
		# Write reminderId and resetPasswordDate
		reminder_id = str(random.randint(1, 999999))
		metas = self._dbMetaKey.metas([K.META_REMINDER_ID, K.META_RESET_PASSWORD_DATE])
		self._dbUserMeta.save_meta(user, metas, {	
										K.META_REMINDER_ID: reminder_id, 
										K.META_RESET_PASSWORD_DATE: str(new_date)})		
		# Send email with link to reset password. Link has time validation
		xml_message = self._dbSetting.get(name__name='Msg/Site/Login/PasswordReminder/_en').value
		EmailService.send(xml_message, {	'home': settings.XIMPIA_HOME, 
										'appSlug': K.Slugs.SITE,
										'viewSlug': K.Slugs.REMINDER_NEW_PASSWORD,
										'firstName': user.first_name, 
										'userAccount': user.username,
										'reminderId': reminder_id}, settings.XIMPIA_WEBMASTER_EMAIL, [self._f()['email']])
		logger.debug( 'requestReminder :: sent Email' )
		self._setOkMsg('OK_PASSWORD_REMINDER')
	
	@action(forms.ChangePasswordForm)
	def finalize_reminder(self):
		"""Saves new password, it does authenticate and login user."""
		self._dbUser = UserDAO(self._ctx)
		self._dbUserMeta = UserMetaDAO(self._ctx)
		user = self._dbUser.get(username= self._f().getParam('username'))
		user.set_password(self._f()['newPassword'])
		user.save()
		# Remove reminder data so that it is not used again
		self._dbUserMeta.search(meta__name__in=[K.META_REMINDER_ID, K.META_RESET_PASSWORD_DATE]).update(value='')

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
