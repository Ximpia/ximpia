import os

from django import forms
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User

from ximpia.util.js import Form as _jsf
from ximpia.core.form_fields import XpUserField, XpPasswordField, XpEmailField, XpCharField, XpChoiceField, XpHiddenField
from ximpia.core.form_widgets import XpHiddenWidget
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

class HomeForm(XBaseForm):
	_XP_FORM_ID = 'home'
	errorMessages = forms.CharField(widget=XpHiddenWidget, initial=_jsf.buildMsgArray([_m, []]))
	okMessages = forms.CharField(widget=XpHiddenWidget, initial=_jsf.buildMsgArray([_m, []]))

class ContactUsForm(XBaseForm):
	_XP_FORM_ID = 'contactUs'
	name = XpCharField(None, '', label="Name", maxValue=30)
	email = XpEmailField(None, '', label='Email', maxValue=100)
	errorMessages = forms.CharField(widget=XpHiddenWidget, initial=_jsf.buildMsgArray([_m, []]))
	okMessages = forms.CharField(widget=XpHiddenWidget, initial=_jsf.buildMsgArray([_m, []]))

class JoinUsForm(XBaseForm):
	_XP_FORM_ID = 'joinUs'
	name = XpCharField(None, '', label="Name", maxValue=30)
	email = XpEmailField(None, '', label='Email', maxValue=100)
	linkedInProfile = XpCharField(None, '', label="LinkedIn Profile", maxValue=100, required=False)
	githubProfile = XpCharField(None, '', label="GitHub Profile", maxValue=100, required=False)
	errorMessages = forms.CharField(widget=XpHiddenWidget, initial=_jsf.buildMsgArray([_m, []]))
	okMessages = forms.CharField(widget=XpHiddenWidget, initial=_jsf.buildMsgArray([_m, []]))

class LoginForm(XBaseForm):
	_XP_FORM_ID = 'login' 
	_dbUser = User()
	username = XpUserField(_dbUser, '_dbUser.username', label='Username', required=False, jsReq=True, initial='')
	password = XpPasswordField(_dbUser, '_dbUser.password', minValue=6, required=False, jsReq=True, initial='')
	socialId = forms.CharField(widget=XpHiddenWidget, required=False, initial='')
	socialToken = forms.CharField(widget=XpHiddenWidget, required=False, initial='')
	authSource = forms.CharField(widget=XpHiddenWidget, initial=K.PASSWORD)
	choices = XpHiddenField(xpType='input.hidden', required=False, initial=_jsf.encodeDict({'authSources': Choices.SOCIAL_NETS}))
	errorMessages = forms.CharField(widget=XpHiddenWidget, initial=_jsf.buildMsgArray([_m, ['ERR_wrongPassword']]))
	okMessages = forms.CharField(widget=XpHiddenWidget, initial=_jsf.buildMsgArray([_m, []]))
	def clean(self):
		"""Clean form"""
		self._xpClean()
		return self.cleaned_data

class HeaderForm(XBaseForm):
	_XP_FORM_ID = 'header' 
	errorMessages = forms.CharField(widget=XpHiddenWidget, initial=_jsf.buildMsgArray([_m, []]))
	okMessages = forms.CharField(widget=XpHiddenWidget, initial=_jsf.buildMsgArray([_m, []]))
	def clean(self):
		"""Clean form"""
		self._xpClean()
		return self.cleaned_data

class PasswordReminderForm(XBaseForm):
	_XP_FORM_ID = 'passwordReminder'
	_dbUser = User()
	email = XpEmailField(_dbUser, '_dbUser.email', label='Email', help_text= _('Email address you signed up with'))
	errorMessages = forms.CharField(widget=XpHiddenWidget, initial=_jsf.buildMsgArray([_m, ['ERR_wrongPassword','ERR_emailDoesNotExist']]))
	okMessages = forms.CharField(widget=XpHiddenWidget, initial=_jsf.buildMsgArray([_m, ['OK_PASSWORD_REMINDER']]))
	def clean(self):
		"""Clean form"""
		self._xpClean()
		return self.cleaned_data

class ChangePasswordForm(XBaseForm):
	_XP_FORM_ID = 'changePassword'
	_dbUser = User()
	username = XpUserField(_dbUser, '_dbUser.username', label='Username')
	newPassword = XpPasswordField(_dbUser, '_dbUser.password', minValue=6, label='Password', help_text = _('Your New Password'))
	newPasswordConfirm = XpPasswordField(_dbUser, '_dbUser.password', minValue=6, label='Confirm Password', 
					help_text = _('Write again your password to make sure there are no errors'))
	errorMessages = forms.CharField(widget=XpHiddenWidget, initial=_jsf.buildMsgArray([_m, ['ERR_changePassword']]))
	okMessages = forms.CharField(widget=XpHiddenWidget, initial=_jsf.buildMsgArray([_m, ['OK_PASSWORD_CHANGE']]))
	def clean(self):
		"""Clean form"""
		self._validateSameFields([('newPassword','newPasswordConfirm')])
		self._xpClean()
		return self.cleaned_data

class UserChangePasswordForm( XBaseForm ):
	_XP_FORM_ID = 'userChangePassword'
	_dbUser = User()
	username = XpUserField(_dbUser, '_dbUser.username', label='Username')
	newPassword = XpPasswordField(_dbUser, '_dbUser.password', minValue=6, label='New Password', help_text = _('Your New Password'))
	newPasswordConfirm = XpPasswordField(_dbUser, '_dbUser.password', minValue=6, label='Confirm Password', 
					help_text = _('Write again your password'))
	password = XpPasswordField(_dbUser, '_dbUser.password', minValue=6, label='Password', help_text = _('Current password'))
	errorMessages = forms.CharField(widget=XpHiddenWidget, initial=_jsf.buildMsgArray([_m, ['ERR_wrongPassword']]))
	okMessages = forms.CharField(widget=XpHiddenWidget, initial=_jsf.buildMsgArray([_m, []]))
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
	username = XpUserField(_dbUser, '_dbUser.username', label='Username')
	password = XpPasswordField(_dbUser, '_dbUser.password', minValue=6, required=False, jsReq=False,  
		help_text = _('Must provide a good or strong password to signup. Allowed characters are letters, numbers and _ | . | $ | % | &'))
	passwordVerify = XpPasswordField(_dbUser, '_dbUser.password', minValue=6, required=False, jsVal=["{equalTo: '#id_password'}"], jsReq=False,
					label= _('Password Verify'))
	email = XpEmailField(_dbInvitation, '_dbInvitation.email', label='Email')
	firstName = XpCharField(_dbUser, '_dbUser.first_name')
	lastName = XpCharField(_dbUser, '_dbUser.last_name', required=False)
	city = XpCharField(_dbAddress, '_dbAddress.city', required=False)
	country = XpChoiceField(_dbAddress, '_dbAddress.country', choicesId='country', required=False, initial='', choices=Choices.COUNTRY)
	invitationCode = XpCharField(_dbInvitation, '_dbInvitation.invitationCode', required=False, jsReq=True)
	authSource = forms.CharField(widget=XpHiddenWidget, initial=K.PASSWORD)
	socialId = forms.CharField(widget=XpHiddenWidget, required=False, initial='')
	socialToken = forms.CharField(widget=XpHiddenWidget, required=False, initial='')
	# Navigation and Message Fields
	params = forms.CharField(widget=XpHiddenWidget, required=False, initial=_jsf.encodeDict({
									'profiles': '', 
									'userGroup': K.SIGNUP_USER_GROUP_ID,
									'affiliateId': -1}))
	choices = XpHiddenField(xpType='input.hidden', required=False, initial=_jsf.encodeDict({'country': Choices.COUNTRY}))
	errorMessages = forms.CharField(widget=XpHiddenWidget, initial=_jsf.buildMsgArray([_m,
										['ERR_ximpiaId', 'ERR_email', 'ERR_socialIdExists']]))
	okMessages = forms.CharField(widget=XpHiddenWidget, initial=_jsf.buildMsgArray([_m, ['OK_USER_SIGNUP','OK_SOCIAL_SIGNUP']]))

	"""def buildInitial(self, invitation, snProfileDict, fbAccessToken, affiliateId):
		Build initial values for form
		self.fields['invitationCode'].initial = invitation.invitationCode
		self.putParam('affiliateId', affiliateId)
		if len(snProfileDict) != 0:
			self._dbUser.firstName = snProfileDict['first_name']
			self._dbUser.lastName = snProfileDict['last_name']
			locationName = snProfileDict['location']['name']
			locationFields = locationName.split(',')
			self._dbAddress.city = locationFields[0].strip()
			locale = snProfileDict['locale']
			self._dbAddress.country = locale.split('_')[1].lower()"""

	def clean(self):
		"""Clean form: validate same password and captcha when implemented"""
		logger.debug( 'UserSignupInvitationForm :: authSource: %s' % (self._getFieldValue('authSource')) )
		if self._getFieldValue('authSource') == K.PASSWORD:
			self._validateSameFields([('password','passwordVerify')])
		self._xpClean()
		return self.cleaned_data

class ActivateUserForm ( XBaseForm ):
	_XP_FORM_ID = 'activateUser'
	errorMessages = forms.CharField(widget=XpHiddenWidget, initial=_jsf.buildMsgArray([_m, []]))
	okMessages = forms.CharField(widget=XpHiddenWidget, initial=_jsf.buildMsgArray([_m, []]))
