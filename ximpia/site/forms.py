# coding: utf-8

import os

from django.utils.translation import ugettext as _
from django.contrib.auth.models import User

from ximpia.util.js import Form as _jsf
from ximpia.core.fields import UserField, PasswordField, EmailField, CharField, HiddenField, OneListField, ManyListField
from ximpia.core.forms import XBaseForm

# Settings
from ximpia.core.util import getClass
settings = getClass(os.getenv("DJANGO_SETTINGS_MODULE"))

# Logging
import logging.config
logging.config.dictConfig(settings.LOGGING)
logger = logging.getLogger(__name__)

import messages as _m 
import constants as K
from choices import Choices
from models import Address, Invitation, UserChannel

from ximpia.core.models import View, XpTemplate, Application

class HomeForm(XBaseForm):
	_XP_FORM_ID = 'home'
	errorMessages = HiddenField(initial=_jsf.buildMsgArray([_m, []]))
	okMessages = HiddenField(initial=_jsf.buildMsgArray([_m, []]))

class ContactUsForm(XBaseForm):
	_XP_FORM_ID = 'contactUs'
	name = CharField(None, '', label="Name", maxLength=30)
	email = EmailField(None, '', label='Email', maxLength=100)
	errorMessages = HiddenField(initial=_jsf.buildMsgArray([_m, []]))
	okMessages = HiddenField(initial=_jsf.buildMsgArray([_m, []]))

class JoinUsForm(XBaseForm):
	_XP_FORM_ID = 'joinUs'
	name = CharField(None, '', label="Name", maxLength=30)
	email = EmailField(None, '', label='Email', maxLength=100)
	linkedInProfile = CharField(None, '', label="LinkedIn Profile", maxLength=100, required=False)
	githubProfile = CharField(None, '', label="GitHub Profile", maxLength=100, required=False)
	errorMessages = HiddenField(initial=_jsf.buildMsgArray([_m, []]))
	okMessages = HiddenField(initial=_jsf.buildMsgArray([_m, []]))

class LoginForm(XBaseForm):
	_XP_FORM_ID = 'login' 
	_dbUser = User()
	username = UserField(_dbUser, 'username', label='Username', required=False, jsRequired=True, initial='')
	password = PasswordField(_dbUser, 'password', minLength=6, required=False, jsRequired=True, initial='')
	socialId = HiddenField()
	socialToken = HiddenField()
	authSource = HiddenField(initial=K.PASSWORD)
	choices = HiddenField(initial=_jsf.encodeDict({'authSources': Choices.SOCIAL_NETS}))
	errorMessages = HiddenField(initial=_jsf.buildMsgArray([_m, ['ERR_wrong_password']]))
	okMessages = HiddenField(initial=_jsf.buildMsgArray([_m, []]))
	def clean(self):
		"""Clean form"""
		self._xpClean()
		return self.cleaned_data

class HeaderForm(XBaseForm):
	_XP_FORM_ID = 'header' 
	errorMessages = HiddenField(initial=_jsf.buildMsgArray([_m, []]))
	okMessages = HiddenField(initial=_jsf.buildMsgArray([_m, []]))
	def clean(self):
		"""Clean form"""
		self._xpClean()
		return self.cleaned_data

class PasswordReminderForm(XBaseForm):
	_XP_FORM_ID = 'passwordReminder'
	_dbUser = User()
	email = EmailField(_dbUser, 'email', label='Email', helpText= _('Email address you signed up with'))
	errorMessages = HiddenField(initial=_jsf.buildMsgArray([_m, ['ERR_wrong_password','ERR_email_does_not_exist']]))
	okMessages = HiddenField(initial=_jsf.buildMsgArray([_m, ['OK_PASSWORD_REMINDER']]))
	def clean(self):
		"""Clean form"""
		self._xpClean()
		return self.cleaned_data

class ChangePasswordForm(XBaseForm):
	_XP_FORM_ID = 'changePassword'
	_dbUser = User()
	username = UserField(_dbUser, 'username', label='Username')
	newPassword = PasswordField(_dbUser, 'password', minLength=6, label='Password', helpText = _('Your New Password'))
	newPasswordConfirm = PasswordField(_dbUser, 'password', minLength=6, label='Confirm Password', 
					helpText = _('Write again your password to make sure there are no errors'))
	errorMessages = HiddenField(initial=_jsf.buildMsgArray([_m, ['ERR_change_password']]))
	okMessages = HiddenField(initial=_jsf.buildMsgArray([_m, ['OK_PASSWORD_CHANGE']]))
	def clean(self):
		"""Clean form"""
		self._validateSameFields([('newPassword','newPasswordConfirm')])
		self._xpClean()
		return self.cleaned_data

class UserChangePasswordForm( XBaseForm ):
	_XP_FORM_ID = 'userChangePassword'
	_dbUser = User()
	username = UserField(_dbUser, 'username', label='Username')
	newPassword = PasswordField(_dbUser, 'password', minLength=6, label='New Password', helpText = _('Your New Password'))
	newPasswordConfirm = PasswordField(_dbUser, 'password', minLength=6, label='Confirm Password', 
					helpText = _('Write again your password'))
	password = PasswordField(_dbUser, 'password', minLength=6, label='Password', helpText = _('Current password'))
	errorMessages = HiddenField(initial=_jsf.buildMsgArray([_m, ['ERR_wrong_password']]))
	okMessages = HiddenField(initial=_jsf.buildMsgArray([_m, []]))
	def clean(self):
		"""Clean form"""
		self._validateSameFields([('newPassword','newPasswordConfirm')])
		self._xpClean()
		return self.cleaned_data

class UserSignupInvitationForm ( XBaseForm ):
	_XP_FORM_ID = 'signup'
	# Instances 
	_dbUser = User()
	_dbUserChannel = UserChannel()
	_dbAddress = Address()
	_dbInvitation = Invitation()
	# Fields
	username = UserField(_dbUser, 'username', label='Username')
	password = PasswordField(_dbUser, 'password', minLength=6, required=False, jsRequired=False,  
		helpText = _('Must provide a good or strong password to signup. Allowed characters are letters, numbers and _ | . | $ | % | &'))
	passwordVerify = PasswordField(_dbUser, 'password', minLength=6, required=False, jsVal=["{equalTo: '#id_password'}"], 
								jsRequired=False, label= _('Password Verify'))
	email = EmailField(_dbInvitation, 'email', label='Email')
	firstName = CharField(_dbUser, 'first_name')
	lastName = CharField(_dbUser, 'last_name', required=False)
	city = CharField(_dbAddress, 'city', required=False)
	country = OneListField(_dbAddress, 'country', choicesId='country', required=False, choices=Choices.COUNTRY)
	invitationCode = CharField(_dbInvitation, 'invitationCode', required=False, jsRequired=True)
	authSource = HiddenField(initial=K.PASSWORD)
	socialId = HiddenField()
	socialToken = HiddenField()
	# Navigation and Message Fields 
	params = HiddenField(initial=_jsf.encodeDict({
									'profiles': '', 
									'userGroup': K.SIGNUP_USER_GROUP_ID,
									'affiliateId': -1}))
	#choices = HiddenField(initial=_jsf.encodeDict( {'country': Choices.COUNTRY } ) )
	errorMessages = HiddenField(initial=_jsf.buildMsgArray([_m,
										['ERR_ximpia_id', 'ERR_email', 'ERR_social_id_exists']]))
	okMessages = HiddenField(initial=_jsf.buildMsgArray([_m, ['OK_USER_SIGNUP','OK_SOCIAL_SIGNUP']]))

	def clean(self):
		"""Clean form: validate same password and captcha when implemented"""
		logger.debug( 'UserSignupInvitationForm :: authSource: %s' % (self._getFieldValue('authSource')) )
		if self._getFieldValue('authSource') == K.PASSWORD:
			self._validateSameFields([('password','passwordVerify')])
		self._xpClean()
		return self.cleaned_data

class ActivateUserForm ( XBaseForm ):
	_XP_FORM_ID = 'activateUser'
	errorMessages = HiddenField(initial=_jsf.buildMsgArray([_m, []]))
	okMessages = HiddenField(initial=_jsf.buildMsgArray([_m, []]))

class FieldTestForm ( XBaseForm ):
	_XP_FORM_ID = 'fieldTest'
	_dbView = View()
	application = OneListField(_dbView, 'application', choicesId='application', values=('slug',))
	templates = ManyListField(_dbView, 'templates', choicesId='templates')
	errorMessages = HiddenField(initial=_jsf.buildMsgArray([_m, []]))
	okMessages = HiddenField(initial=_jsf.buildMsgArray([_m, []]))
