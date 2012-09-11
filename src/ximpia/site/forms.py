from django import forms
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User

from ximpia_core.util.js import Form as _jsf
from ximpia_core.core.form_fields import XpUserField, XpPasswordField, XpEmailField, XpCharField, XpChoiceField, XpHiddenField
from ximpia_core.core.form_fields import XpHiddenDataField
from ximpia_core.core.form_widgets import XpHiddenWidget
from ximpia_core.core.forms import XBaseForm

import messages as _m 
import constants as K
from choices import Choices
from models import Address, Invitation, UserChannel

# TODO: Remove settings_visual. We need this???? Other ways to do it????
from ximpia.settings_visual import SocialNetworkIconData as SocialNetwork

class HomeForm(XBaseForm):
	_XP_FORM_ID = 'home'
	errorMessages = forms.CharField(widget=XpHiddenWidget, initial=_jsf.buildMsgArray([_m, []]))
	okMessages = forms.CharField(widget=XpHiddenWidget, initial=_jsf.buildMsgArray([_m, []]))

class LoginForm(XBaseForm):
	_XP_FORM_ID = 'login' 
	_dbUser = User()
	ximpiaId = XpUserField(_dbUser, '_dbUser.username', label='XimpiaId', help_text=_('Your XimpiaId'))
	password = XpPasswordField(_dbUser, '_dbUser.password', minValue=6, help_text = _('Your Password'))
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
	newPassword = XpPasswordField(_dbUser, '_dbUser.password', minValue=6, label='New Password', help_text = _('Your New Password'))
	newPasswordConfirm = XpPasswordField(_dbUser, '_dbUser.password', minValue=6, label='Confirm Password', 
					help_text = _('Write again your password'))
	password = XpPasswordField(_dbUser, '_dbUser.password', minValue=6, label='Password', help_text = _('Current password'))
	errorMessages = forms.CharField(widget=XpHiddenWidget, initial=_jsf.buildMsgArray([_m, ['ERR_passwordValidate']]))
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
	ximpiaId = XpUserField(_dbUser, '_dbUser.username', label='XimpiaId')
	#password = XpPasswordField(_dbUser, '_dbUser.password', minValue=6, req=False, jsReq=True,  
	#	help_text = _('Must provide a good or strong password to signup. Allowed characters are letters, numbers and _ | . | $ | % | &'))
	#passwordVerify = XpPasswordField(_dbUser, '_dbUser.password', minValue=6, req=False, jsVal=["{equalTo: '#id_password'}"], jsReq=True,
	#				label= _('Password Verify'))
	email = XpEmailField(_dbInvitation, '_dbInvitation.email', label='Email', attrs={'readonly': 'readonly'})
	firstName = XpCharField(_dbUser, '_dbUser.first_name')
	lastName = XpCharField(_dbUser, '_dbUser.last_name', req=False)
	city = XpCharField(_dbAddress, '_dbAddress.city', req=False)
	country = XpChoiceField(_dbAddress, '_dbAddress.country', choicesId='country', req=False, initial='', choices=Choices.COUNTRY)
	#invitationCode = XpHiddenDataField(_dbInvitation, '_dbInvitation.invitationCode')
	facebookIcon_data = forms.CharField(widget=XpHiddenWidget, required=False, initial=SocialNetwork('facebook', 2).getS())
	# Navigation and Message Fields
	params = forms.CharField(widget=XpHiddenWidget, required=False, initial=_jsf.encodeDict({
									'profiles': '', 
									'userGroup': K.SIGNUP_USER_GROUP_ID,
									'affiliateId': -1}))
	choices = XpHiddenField(xpType='input.hidden', required=False, initial=_jsf.encodeDict({'country': Choices.COUNTRY}))
	errorMessages = forms.CharField(widget=XpHiddenWidget, initial=_jsf.buildMsgArray([_m,
		['ERR_invitationCode', 'ERR_ximpiaId', 'ERR_email', 'ERR_captcha','ERR_invitationUsed']]))
	okMessages = forms.CharField(widget=XpHiddenWidget, initial=_jsf.buildMsgArray([_m, ['OK_SN_SIGNUP']]))

	def buildInitial(self, invitation, snProfileDict, fbAccessToken, affiliateId):
		"""Build initial values for form"""
		#self.initial = {}
		#self.putParam('userGroups', [K.SIGNUP_USER_GROUP_ID])
		#self.initial['invitationCode'] = invitation.invitationCode
		self.fields['invitationCode'].initial = invitation.invitationCode
		# affiliateId
		self.putParam('affiliateId', affiliateId)
		if len(snProfileDict) != 0:
			self._dbUser.firstName = snProfileDict['first_name']
			self._dbUser.lastName = snProfileDict['last_name']
			#self.user.email = snProfileDict['email']
			#self._dbUser.username = (snProfileDict['first_name'] + '.' + snProfileDict['last_name']).strip().lower()
			locationName = snProfileDict['location']['name']
			locationFields = locationName.split(',')
			self._dbAddress.city = locationFields[0].strip()
			locale = snProfileDict['locale']
			self._dbAddress.country = locale.split('_')[1].lower()
			# TODO: Facebook integration
			#fbIcon = SocialNetwork('facebook', 2)
			#fbIcon.setToken(fbAccessToken)
			#self.initial['facebookIcon_data'] = fbIcon.getS()

	def clean(self):
		"""Clean form: validate same password and captcha when implemented"""
		self._validateCaptcha()
		self._xpClean()
		return self.cleaned_data
