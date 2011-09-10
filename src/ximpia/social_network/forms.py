import re
import json
import types

from django import forms
from django.forms import ValidationError
from django.utils.translation import ugettext as _
from choices import Choices

from ximpia import settings
from form_objects import XpHiddenWidget, XpPasswordWidget, XpSelectWidget, XpTextareaWidget, XpTextInputWidget

import messages as _m
from messages import MsgSignup
from constants import KSignup

from ximpia.settings_visual import SocialNetworkIconData as SocialNetwork
from ximpia.settings_visual import SuggestBox, GenericComponent

#from yacaptcha.models import Captcha

from django.contrib.auth.models import User, Group
from models import UserSocial, Invitation, Address, ContactDetail, Organization, Tag, UserAccountContract

#from validators import *
from ximpia.social_network.form_objects import XpMultipleWidget, XpMultiField, XpCharField, XpEmailField, XpPasswordField, XpSocialIconField,\
	XpChoiceField
from ximpia.social_network.form_objects import XpUserField
from ximpia.util.js import Form as _jsf

from ximpia.social_network.validators import validateCaptcha

class XBaseForm(forms.Form):
	ERROR_INVALID = 'invalid'
	_request = None
	_ctx = None
	_db = {}
	entryFields = forms.CharField(widget=XpHiddenWidget, required=False, initial=_jsf.buildBlankArray([]))
	copyEntryFields = forms.CharField(widget=XpHiddenWidget, required=False, initial=json.dumps(False))
	params = forms.CharField(widget=XpHiddenWidget, required=False, initial=_jsf.buildBlankArray([]))
	pkFields = forms.CharField(widget=XpHiddenWidget, required=False, initial=_jsf.buildBlankArray([]))
	errorMessages = forms.CharField(widget=XpHiddenWidget, initial=_jsf.buildMsgArray([]))
	okMessages = forms.CharField(widget=XpHiddenWidget, initial=_jsf.buildMsgArray([]))
	errors = {}
	def __init__(self, *argsTuple, **argsDict): 
		"""Constructor for base form container"""
		if argsDict.has_key('ctx'):
			self._ctx = argsDict['ctx']
		self.errors = {}
		#self.errors['invalid'] = []
		if argsDict.has_key('instances'):
			dict = argsDict['instances']
			keys = dict.keys()
			# Set instances
			for key in keys:
				setattr(self, '_' + key, dict[key])
			fields = self.base_fields.keys()
			for sField in fields:
				field = self.base_fields[sField]
				try:
					instanceFieldName = field.instanceFieldName
					instanceName = field.instanceName
					if type(field.initial) == types.StringType and field.instance:
						field.initial = eval('self.' + instanceName + '.' + instanceFieldName)
						field.instance = eval('self.' + instanceName)
				except AttributeError:
					pass
			# Set instance too
		if argsDict.has_key('ctx'):
			del argsDict['ctx']
		if argsDict.has_key('dbDict'):
			del argsDict['dbDict']
		if argsDict.has_key('instances'):
			del argsDict['instances']
		self._db = {}
		super(XBaseForm, self).__init__(*argsTuple, **argsDict)	
	def putParam(self, name, value):
		"""Adds field to javascript array
		@param name: 
		@param value: """
		dict = json.loads(self.fields['params'].initial)
		dict[name] = value
		self.fields['params'].initial = json.dumps(dict)
	def getParam(self, name):
		"""Get param value.
		@param name: Param name
		@return: value"""
		dict = json.loads(self.fields['params'].initial)
		if dict.has_key(name):
			value = dict[name]
		else:
			raise ValueError
		return value
	def hasParam(self, name):
		"""Checks if has key name
		@param name: 
		@return: boolean"""
		dict = json.loads(self.fields['params'].initial)
		return dict.has_key(name)
	def _validateSameFields(self, tupleList):
		"""Validate same fields for list of tuples in form
		@param tupleList: Like ('password','passwordVerify')"""
		for tuple in tupleList:
			field1 = eval("self.fields['" + tuple[0] + "']")
			#field1Value = self.data[tuple[0]]
			field2 = eval("self.fields['" + tuple[1] + "']")
			#field1Value = self.data[tuple[1]]
			#field1Value = self.d(tuple[0])
			#field2Value = self.d(tuple[1])			
			field1Value = self.data[tuple[0]]
			field2Value = self.data[tuple[1]]
			
			if field1Value != field2Value:
				if not self.errors.has_key('id_' + tuple[0]):
					self.errors['id_' + tuple[0]] = []
				if not self._errors.has_key('id_' + tuple[0]):
					self._errors['id_' + tuple[0]] = []
				self.errors['id_' + tuple[0]].append(field1.label + _(' must be the same as ') + field2.label)
				self._errors['id_' + tuple[0]].append(field1.label + _(' must be the same as ') + field2.label)

	def _validateSignupCaptcha(self):
		"""Validate Signup captcha"""
		if self._ctx.captcha != self.cleaned_data['captcha'] and not settings.PRIVATE_BETA:
			self.errors['captcha'].append(_('Captcha code is not correct'))
	def _validateCaptcha(self):
		"""Validate captcha"""
		if self._ctx.captcha != self.cleaned_data['captcha']:
			self.errors['captcha'].append(_('Captcha code is not correct'))
	def addInvalidError(self, sError):
		"""Adds error to errors lists."""
		self.errors[self.ERROR_INVALID].append(sError)	
	def setErrorDict(self, errors):
		"""Sets error dictionary"""
		self.errors = errors	
	def getErrorDict(self):
		"""Get error dictionary"""
		return self.errors
	def hasInvalidErrors(self):
		"""Has the form invalid errors?"""
		bError = False
		if len(self.errors.keys()) != 0:
			bError = True
		return bError
	def d(self, name):
		"""Get cleaned data, after form has been validated"""
		value = ''
		if self.cleaned_data.has_key(name):
			value = self.cleaned_data[name]
		return value
	def is_valid(self):
		"""Checks if form is valid. Does a full clean of form."""
		super(XBaseForm, self).full_clean()
		bForm = super(XBaseForm, self).is_valid()
		print 'Call super'
		return bForm
	def _xpClean(self):
		"""Cleans form. Raises ValidationError in case errors found. Returns cleaned_data"""
		if self.hasInvalidErrors():
			raise ValidationError('Form Clean Validation Error')
		return self.cleaned_data

class UserSignupForm(XBaseForm):
	# Instances 
	_dbUser = User()
	_dbUserSocial = UserSocial()
	_dbContactDetail = ContactDetail()
	_dbAddress = Address()
	_dbInvitation = Invitation()
	# Fields
	ximpiaId = XpUserField(_dbUser, '_dbUser.username', tabindex=1, label='XimpiaId')
	password = XpPasswordField(_dbUser, '_dbUser.password', min=6, req=False, jsReq=True, tabindex=2, 
		help_text = _('Must provide a good or strong password to signup. Allowed characters are letters, numbers and _ | . | $ | % | &'))
	passwordVerify = XpPasswordField(_dbUser, '_dbUser.password', min=6, req=False, jsVal=["{equalTo: '#id_password'}"], jsReq=True,
					label= _('Password Verify'), tabindex=3)
	email = XpEmailField(_dbUser, '_dbUser.email', tabindex=6, label='Email')
	firstName = XpCharField(_dbUser, '_dbUser.first_name', tabindex=4)
	lastName = XpCharField(_dbUser, '_dbUser.last_name', req=False, tabindex=5)
	#industry = XpMultiField(None, '', choices = Choices.INDUSTRY, init=[], label=_('Industries'), help_text=_('Industries'))
	city = XpCharField(_dbAddress, '_dbAddress.city', req=False, tabindex=7)
	country = XpChoiceField(_dbAddress, '_dbAddress.country', choices=Choices.COUNTRY, req=False, initial='', tabindex=8)
	captcha = XpCharField(None, '', max=6, val=[validateCaptcha], req=False, initial='', label=_('Validation'))
	invitationCode = forms.CharField(widget=XpHiddenWidget)
	twitterIcon_data = XpSocialIconField(network='twitter', version=1)
	facebookIcon_data = XpSocialIconField(network='facebook', version=2)
	linkedinIcon_data = XpSocialIconField(network='linkedid', version=1)
	# Navigation and Message Fields
	params = forms.CharField(widget=XpHiddenWidget, required=False, initial=_jsf.encodeDict({
									'profiles': '', 
									'userGroups': [KSignup.USER_GROUP_ID],
									'affiliateId': -1}))
	errorMessages = forms.CharField(widget=XpHiddenWidget, initial=_jsf.buildMsgArray([_m,
		['ERR_invitationCode', 'ERR_ximpiaId', 'ERR_email', 'ERR_captcha']]))
	okMessages = forms.CharField(widget=XpHiddenWidget, initial=_jsf.buildMsgArray([_m, ['OK_SN_SIGNUP']]))
			
	def buildInitial(self, invitation, snProfileDict, fbAccessToken, affiliateId):
		"""Build initial values for form"""
		#self.initial = {}
		#self.putParam('userGroups', [KSignup.USER_GROUP_ID])
		self.initial['invitationCode'] = invitation.invitationCode
		# affiliateId
		self.putParam('affiliateId', affiliateId)
		if len(snProfileDict) != 0:
			self.user.firstName = snProfileDict['first_name']
			self.user.lastName = snProfileDict['last_name']
			self.user.email = snProfileDict['email']
			self.user.username = (snProfileDict['first_name'] + '.' + snProfileDict['last_name']).strip().lower()
			locationName = snProfileDict['location']['name']
			locationFields = locationName.split(',')
			self.address.city = locationFields[0].strip()
			locale = snProfileDict['locale']
			self.address.country = locale.split('_')[1].lower()
			fbIcon = SocialNetwork('facebook', 2)
			fbIcon.setToken(fbAccessToken)
			self.initial['facebookIcon_data'] = fbIcon.getS()

	def clean(self):
		"""Clean form: validate same password and captcha when implemented"""
		self._validateSameFields([('password','passwordVerify')])		
		#self._validateSignupCaptcha()
		return self._xpClean()


class OrganizationSignupForm(XBaseForm):
	# Instances
	_dbUser = User()
	_dbAddress = Address()
	_dbOrganization = Organization()
	_dbGroup = Group()
	_dbTag = Tag()
	_dbUserAccountContract = UserAccountContract()
	# Fields
	ximpiaId = XpUserField(_dbUser, '_dbUser.username', label='XimpiaId')
	password = XpPasswordField(_dbUser, '_dbUser.password', min=6, req=False, jsReq=True, 
		help_text = _('Must provide a strong password to submit form. Allowed characters are letters, numbers and _ | . | $ | % | &'))
	passwordVerify = XpPasswordField(_dbUser, '_dbUser.password', min=6, req=False, jsVal=["{equalTo: '#id_password'}"], jsReq=True,
					label= _('Password Verify'))
	email = XpEmailField(_dbUser, '_dbUser.email', label='Email')
	firstName = XpCharField(_dbUser, '_dbUser.first_name')
	lastName = XpCharField(_dbUser, '_dbUser.last_name', req=False)
	organizationIndustry = XpMultiField(None, '', choices = Choices.INDUSTRY, init=[], label=_('Industries'), help_text=_('Industries'))
	city = XpCharField(_dbAddress, '_dbAddress.city', req=False)
	country = XpChoiceField(_dbAddress, '_dbAddress.country', choices=Choices.COUNTRY, req=False, initial='')
	organizationName = XpCharField(_dbOrganization, '_dbOrganization.name')
	organizationDomain = XpCharField(_dbOrganization, '_dbOrganization.domain')
	organizationCity = XpCharField(_dbAddress, '_dbAddress.city')
	organizationCountry = XpChoiceField(_dbAddress, '_dbAddress.country', choices=Choices.COUNTRY, initial='')
	account = XpCharField(_dbOrganization, '_dbOrganization.account')
	# TextArea
	description = XpCharField(_dbOrganization, '_dbOrganization.description')
	organizationGroup = XpCharField(_dbGroup, '_dbGroup.name', label=_('Organization Group'))
	organizationGroupTags = XpCharField(_dbTag, '_dbTag.name', label=_('Group Tags'))
	jobTitle = XpCharField(_dbUserAccountContract, '_dbUserAccountContract.jobTitle')
	captcha = XpCharField(None, '', max=6, val=[validateCaptcha], req=False, initial='', label=_('Validation'))
	
	orgGroupTags_data = forms.CharField(widget=XpHiddenWidget, required=False, initial='')
	orgGroup_data = forms.CharField(widget=XpHiddenWidget, required=False, initial='')
	jobTitle_data = forms.CharField(widget=XpHiddenWidget, required=False, initial=SuggestBox(Choices.JOB_TITLES))
	organizationGroup_data = forms.CharField(widget=XpHiddenWidget, required=False, initial=SuggestBox(Choices.ORG_GROUPS))
	groupTags_data = forms.CharField(widget=XpHiddenWidget, required=False, initial=GenericComponent())
	groupTagsAjax = forms.CharField(widget=XpHiddenWidget, required=False, initial='')
	
	# Navigation and Message Fields
	fields = forms.CharField(widget=XpHiddenWidget, required=False, initial=_jsf.encodeDict({
									'profiles': '', 
									'userGroups': [KSignup.USER_GROUP_ID],
									'affiliateId': -1,
									'invitationCode': '',
									'accountType': ''}))
	errorMessages = forms.CharField(widget=XpHiddenWidget, initial=_jsf.buildMsgArray([_m, []]))
	okMessages = forms.CharField(widget=XpHiddenWidget, initial=_jsf.buildMsgArray([_m, []]))
	
	def buildInitial(self):
		pass
	
	def clean(self):
		self._validateSameFields([('password','passwordVerify')])
		return self._xpClean()




class AppRegex(object):
	"""Doc.
	@deprecated: """
	# Any text
	string = re.compile('\w+', re.L)
	# text field, like 
	textField = re.compile("^(\w*)\s?(\s?\w+)*$", re.L)
	# Domain
	domain = re.compile("^([a-z0-9]([-a-z0-9]*[a-z0-9])?\\.)+((a[cdefgilmnoqrstuwxz]|aero|arpa)|(b[abdefghijmnorstvwyz]|biz)|(c[acdfghiklmnorsuvxyz]|cat|com|coop)|d[ejkmoz]|(e[ceghrstu]|edu)|f[ijkmor]|(g[abdefghilmnpqrstuwy]|gov)|h[kmnrtu]|(i[delmnoqrst]|info|int)|(j[emop]|jobs)|k[eghimnprwyz]|l[abcikrstuvy]|(m[acdghklmnopqrstuvwxyz]|mil|mobi|museum)|(n[acefgilopruz]|name|net)|(om|org)|(p[aefghklmnrstwy]|pro)|qa|r[eouw]|s[abcdeghijklmnortvyz]|(t[cdfghjklmnoprtvwz]|travel)|u[agkmsyz]|v[aceginu]|w[fs]|y[etu]|z[amw])$", re.L)
	# currency, like 23.23, 34.5
	currency = re.compile('^[0-9]*\.?|\,?[0-9]{0,2}$')
	# id, like 87262562
	id = re.compile('^[1-9]+[0-9]*$')
	# user id
	userId = re.compile('^[a-zA-Z0-9_.]+')
	# password
	password = re.compile('^\w+')
	# captcha
	captcha = re.compile('^\w{6}$')
	# Email
	email = re.compile('^([\w.])+\@([a-z0-9]([-a-z0-9]*[a-z0-9])?\\.)+((a[cdefgilmnoqrstuwxz]|aero|arpa)|(b[abdefghijmnorstvwyz]|biz)|(c[acdfghiklmnorsuvxyz]|cat|com|coop)|d[ejkmoz]|(e[ceghrstu]|edu)|f[ijkmor]|(g[abdefghilmnpqrstuwy]|gov)|h[kmnrtu]|(i[delmnoqrst]|info|int)|(j[emop]|jobs)|k[eghimnprwyz]|l[abcikrstuvy]|(m[acdghklmnopqrstuvwxyz]|mil|mobi|museum)|(n[acefgilopruz]|name|net)|(om|org)|(p[aefghklmnrstwy]|pro)|qa|r[eouw]|s[abcdeghijklmnortvyz]|(t[cdfghjklmnoprtvwz]|travel)|u[agkmsyz]|v[aceginu]|w[fs]|y[etu]|z[amw])')

class FrmCommon(forms.Form):
	"""Doc.
	@deprecated: """
	def __init__(self, *args, **kwargs): 
		"""Doc."""
		super(FrmCommon, self).__init__(*args, **kwargs)
	def validateSameFields(self, fieldName1, fieldName2):
		"""Doc."""
		if self.fields.has_key('fieldName1'):
			fieldLabel1 = self.fields[fieldName1].label
			fieldLabel2 = self.fields[fieldName2].label
			fieldData1 = self.data[fieldName1]
			fieldData2 = self.data[fieldName2]		
			checkSame = False
			if fieldData1 == fieldData2:
				checkSame = True
			checkBasic = self.is_valid()
			check = False
			if checkBasic== True and checkSame == True:
				check = True
			else:
				if checkSame == False:
					self.errors['invalid'] = ' password. ' + fieldLabel1 + ' must be the same as ' + fieldLabel2
		else:
			check = self.is_valid()
		return check
	def cleaned_data(self, data):
		value = super(FrmCommon, self).cleaned_data(data)
		return value

class FrmUserSignup(FrmCommon):
	ximpiaId = forms.RegexField(max_length=20, regex=AppRegex.userId, widget=XpTextInputWidget(attrs={'class':"SmallMust ximpiaid required",'maxlength': '20'}, hasInfo=True))
	email = forms.EmailField(max_length=50, widget=XpTextInputWidget(attrs={'class':'SmallMust required email','maxlength': '50'}))
	firstName = forms.RegexField(max_length=30, regex=AppRegex.textField, widget=XpTextInputWidget(attrs={'class':'SmallMust required','maxlength': '30'}))
	lastName = forms.RegexField(max_length=30, regex=AppRegex.textField, widget=XpTextInputWidget(attrs={'class':'Small','maxlength': '30'}), required=False)
	password = forms.RegexField(max_length=10, min_length=6, regex=AppRegex.password, widget=XpPasswordWidget(render_value=False, 
							attrs={'class':'Small password required','maxlength': '10'}), required=False)
	passwordVerify = forms.RegexField(max_length=10, min_length=6, regex=AppRegex.password, 
							widget=XpPasswordWidget(render_value=False, attrs={'class':"Small password required {equalTo: '#id_password'}",'maxlength': '10'}, hasInfo=True), 
							required=False)
	industry = forms.MultipleChoiceField(choices=Choices.INDUSTRY, widget=XpMultipleWidget(attrs={'class': 'SmallMust required', 'size': '10', 
															'style': 'vertical-align:top; margin-top: 10px'}, hasInfo=True))
	city = forms.RegexField(max_length=20, regex=AppRegex.textField, widget=XpTextInputWidget(attrs={'class':'Small','maxlength': '20'}), required=False)
	country = forms.ChoiceField(choices=Choices.COUNTRY, widget=XpSelectWidget(attrs={'class': 'Small'}), required=False)	
	
	twitterIcon_data = forms.CharField(widget=XpHiddenWidget, required=False, initial=SocialNetwork('twitter', 1).getS())
	facebookIcon_data = forms.CharField(widget=XpHiddenWidget, required=False, initial=SocialNetwork('facebook', 2).getS())
	linkedinIcon_data = forms.CharField(widget=XpHiddenWidget, required=False, initial=SocialNetwork('linkedin', 1).getS())
	profiles = forms.CharField(widget=XpHiddenWidget, required=False, initial='')
	userGroups = forms.CharField(widget=XpHiddenWidget)
	invitationCode = forms.CharField(max_length=10, widget=XpTextInputWidget(attrs={'class':"SmallMust required {minlength: 10, maxlength: 10}"}, hasInfo=True), required=False)
	affiliateId = forms.RegexField(max_length=6, regex=AppRegex.id, widget=XpHiddenWidget, required=False)
	captcha = forms.RegexField(max_length=6, regex=AppRegex.captcha, widget=XpTextInputWidget(attrs={'class':'Small required'}, hasInfo=True), required=False)
	invitationType = forms.CharField(widget=XpHiddenWidget, required=False)
	invitationByUser = forms.CharField(widget=XpHiddenWidget, required=False)
	invitationByOrg = forms.CharField(widget=XpHiddenWidget, required=False)
	
	msgError_invitationCode = forms.CharField(widget=XpHiddenWidget, required=False, initial=_("""Error in validating invitation code. Ximpia is invitation-only, you must have a valid invitation code from another user"""))
	msgError_VALIDATION = forms.CharField(widget=XpHiddenWidget, required=False, initial=_('Errors validating your signup data. Please check data entered and try again.'))
	msgError_ximpiaId = forms.CharField(widget=XpHiddenWidget, required=False, initial=_('An user with same ximpiaId already exists. Please choose another id for your ximpia account'))
	msgError_email = forms.CharField(widget=XpHiddenWidget, required=False, initial=_('An user with same email address already exists. Please select another email'))
	msgError_captcha = forms.CharField(widget=XpHiddenWidget, required=False, initial=_('Error in validation image. You can reload image to display another image.'))
	msg_ximpiaId = forms.CharField(widget=XpHiddenWidget, required=False, initial = MsgSignup.XIMPIA_ID)
	msg_invitationCode = forms.CharField(widget=XpHiddenWidget, required=False, initial = MsgSignup.INVITATION_CODE)
	msg_captcha = forms.CharField(widget=XpHiddenWidget, required=False, initial = MsgSignup.CAPTCHA)
	msg_passwordVerify = forms.CharField(widget=XpHiddenWidget, required=False, initial = MsgSignup.PASSWORD_VERIFY)
	msg_industry = forms.CharField(widget=XpHiddenWidget, required=False, initial = MsgSignup.INDUSTRY)
	msg_ok = forms.CharField(widget=XpHiddenWidget, required=False, initial = _('Your signup has been received, check your email'))
	msgSubmit_Form1 = forms.CharField(widget=XpHiddenWidget, required=False, initial = "['" + _("We received your signup. Check your mail") + "','" + _("We have received correctly your account signup. :p:We have sent an email to validate your email address. Just click on link on Email message to activate your account.::p:::p:Thanks!::p::'") + ",'popMessageOk']")

	def isValid(self, captcha=None):
		bForm = self.validateSameFields('password','passwordVerify')
		if bForm == True and captcha != None and captcha != self.cleaned_data['captcha'] and not settings.PRIVATE_BETA:
			bForm = False
		return bForm

	def buildInitialShow(self, invitationCode, invitation, profileDict, fbAccessToken):
		"""Build initial page data from invitation data and facebook profile data"""
		self.initial = {}
		self.initial['userGroups'] = json.dumps(['1'])
		if invitation:
			self.initial['invitationCode'] = invitationCode
			self.initial['invitationType'] = invitation.type
			self.initial['invitationByUser'] = invitation.fromUser.id
			self.initial['invitationByOrg'] = invitation.fromAccount
		if len(profileDict) != 0:
				self.initial['firstName'] = profileDict['first_name']
				self.initial['lastName'] = profileDict['last_name']
				self.initial['email'] = profileDict['email']
				self.initial['ximpiaId'] = (profileDict['first_name'] + '.' + profileDict['last_name']).strip().lower()
				locationName = profileDict['location']['name']
				locationFields = locationName.split(',')
				self.initial['city'] = locationFields[0].strip()
				locale = profileDict['locale']
				self.initial['country'] = locale.split('_')[1].lower()
				fbIcon = SocialNetwork('facebook', 2)
				fbIcon.setToken(fbAccessToken)
				self.initial['facebookIcon_data'] = fbIcon.getS()

class FrmOrganizationSignup(FrmCommon):
	ximpiaId = forms.RegexField(max_length=20, regex=AppRegex.userId, widget=XpTextInputWidget(attrs={'class':"SmallMust ximpiaid required",'maxlength': '20'}, hasInfo=True))
	email = forms.EmailField(max_length=50, widget=XpTextInputWidget(attrs={'class':'SmallMust required email','maxlength': '50'}))
	firstName = forms.RegexField(max_length=30, regex=AppRegex.textField, widget=XpTextInputWidget(attrs={'class':'SmallMust required','maxlength': '30'}))
	lastName = forms.RegexField(max_length=30, regex=AppRegex.textField, widget=XpTextInputWidget(attrs={'class':'SmallMust required','maxlength': '30'}))
	password = forms.RegexField(max_length=10, min_length=6, regex=AppRegex.password, 
							widget=XpPasswordWidget(render_value=False, attrs={'class':'SmallMust password required','maxlength': '10'}), required=False)
	passwordVerify = forms.RegexField(max_length=10, min_length=6, regex=AppRegex.password, 
							widget=XpPasswordWidget(render_value=False, attrs={'class':"SmallMust password required {equalTo: '#id_password'}",'maxlength': '10'}, hasInfo=True), 
							required=False)
	organizationIndustry = forms.MultipleChoiceField(choices=Choices.INDUSTRY, widget=XpMultipleWidget(attrs={'class': 'SmallMust required', 
															'size': '10', 'style': 'vertical-align:top; margin-top: 10px'}, hasInfo=True))
	city = forms.RegexField(max_length=20, regex=AppRegex.textField, widget=XpTextInputWidget(attrs={'class':'SmallMust required','maxlength': '20'}))
	country = forms.ChoiceField(choices=Choices.COUNTRY, widget=XpSelectWidget(attrs={'class': 'SmallMust required'}))
	organizationName = forms.RegexField(max_length=30, regex=AppRegex.textField, widget=XpTextInputWidget(attrs={'class':'SmallMust required','maxlength': '30'}))
	organizationDomain = forms.RegexField(max_length=50, regex=AppRegex.domain, widget=XpTextInputWidget(attrs={'class':'SmallMust required','maxlength': '50'}))
	organizationCity = forms.RegexField(max_length=20, regex=AppRegex.textField, widget=XpTextInputWidget(attrs={'class':'SmallMust required','maxlength': '20'}))
	organizationCountry = forms.ChoiceField(choices=Choices.COUNTRY, widget=XpSelectWidget(attrs={'class': 'SmallMust required'}))
	account = forms.RegexField(max_length=20, regex=AppRegex.textField, widget=XpTextInputWidget(attrs={'class':'SmallMust required','maxlength': '20'}, hasInfo=True))	
	description = forms.RegexField(max_length=144, regex=AppRegex.string, widget=XpTextareaWidget(attrs={'class' : 'TextArea Small',
															'style': 'vertical-align:top; width: 330px; height: 14px; padding: 5px; resize:none; overflow: none'}), required=False)
	organizationGroup = forms.RegexField(max_length=20, regex=AppRegex.textField, widget=XpTextInputWidget(attrs={'class':'SmallMust required','maxlength': '20','style': 'width: 250px'}, hasInfo=True))
	organizationGroupTags = forms.CharField(max_length=15, widget=XpTextInputWidget(attrs={'class':'Small','maxlength': '30', 'style': 'width: 130px'}), required=False)
	jobTitle = forms.RegexField(max_length=50, regex=AppRegex.textField, widget=XpTextInputWidget(attrs={'class':'SmallMust required','maxlength': '50'}))
	
	orgGroupTags_data = forms.CharField(widget=XpHiddenWidget, required=False, initial='')
	orgGroup_data = forms.CharField(widget=XpHiddenWidget, required=False, initial='')
	twitterOrgIcon_data = forms.CharField(widget=XpHiddenWidget, required=False, initial=SocialNetwork('twitter', 1))
	twitterIcon_data = forms.CharField(widget=XpHiddenWidget, required=False, initial=SocialNetwork('twitter', 1))
	facebookIcon_data = forms.CharField(widget=XpHiddenWidget, required=False, initial=SocialNetwork('facebook', 2))
	linkedinIcon_data = forms.CharField(widget=XpHiddenWidget, required=False, initial=SocialNetwork('linkedin', 1))
	jobTitle_data = forms.CharField(widget=XpHiddenWidget, required=False, initial=SuggestBox(Choices.JOB_TITLES))
	organizationGroup_data = forms.CharField(widget=XpHiddenWidget, required=False, initial=SuggestBox(Choices.ORG_GROUPS))
	profiles = forms.CharField(widget=XpHiddenWidget, required=False, initial='')
	linkedInProfile = forms.URLField(max_length=255, verify_exists=True, widget=XpTextInputWidget(attrs={'class':'Small required','style':'width:300px'}, hasInfo=True), required=False)
	userGroups = forms.CharField(widget=XpHiddenWidget)
	invitationCode = forms.CharField(max_length=10, widget=XpTextInputWidget(attrs={'class':"SmallMust required {minlength: 10, maxlength: 10}"}, 
																	hasInfo=True), required=False)
	accountType = forms.CharField(max_length=20, widget=XpHiddenWidget)
	affiliateId = forms.RegexField(max_length=6, regex=AppRegex.id, widget=XpHiddenWidget, required=False)
	captcha = forms.RegexField(max_length=6, regex=AppRegex.captcha, widget=XpTextInputWidget(attrs={'class':'Small required'}, hasInfo=True), required=False)
	invitationType = forms.CharField(widget=XpHiddenWidget, required=False)
	invitationByUser = forms.CharField(widget=XpHiddenWidget, required=False)
	invitationByOrg = forms.CharField(widget=XpHiddenWidget, required=False)
	groupTags_data = forms.CharField(widget=XpHiddenWidget, required=False, initial=GenericComponent())
	groupTagsAjax = forms.CharField(widget=XpHiddenWidget, required=False, initial='')
	
	msgError_invitationCode = forms.CharField(widget=XpHiddenWidget, required=False,  initial=_("""Error in validating invitation code. Ximpia is invitation-only, you must have a valid invitation code from another user"""))
	msgError_VALIDATION = forms.CharField(widget=XpHiddenWidget, required=False, initial=_('Errors validating your signup data. Please check data entered and try again.'))
	msgError_ximpiaId = forms.CharField(widget=XpHiddenWidget, required=False, initial=_('An user with same ximpiaId already exists. Please choose another id for your ximpia account'))
	msgError_email = forms.CharField(widget=XpHiddenWidget, required=False, initial=_('An user with same email address already exists. Please select another email'))
	msgError_captcha = forms.CharField(widget=XpHiddenWidget, required=False, initial=_('Error in validation image. You can reload image to display another image.'))
	msgError_account = forms.CharField(widget=XpHiddenWidget, required=False, initial=_('Account name already exists. Please select another account name'))
	msg_ximpiaId = forms.CharField(widget=XpHiddenWidget, required=False, initial = MsgSignup.XIMPIA_ID)
	msg_invitationCode = forms.CharField(widget=XpHiddenWidget, required=False, initial = MsgSignup.INVITATION_CODE)
	msg_captcha = forms.CharField(widget=XpHiddenWidget, required=False, initial = MsgSignup.CAPTCHA)
	msg_organizationGroup = forms.CharField(widget=XpHiddenWidget, required=False, initial = MsgSignup.ORGANIZATION_GROUP)
	msg_organizationGroupTags = forms.CharField(widget=XpHiddenWidget, required=False, initial = MsgSignup.ORGANIZATION_GROUP_TAGS)
	msg_linkedInProfile = forms.CharField(widget=XpHiddenWidget, required=False, initial = MsgSignup.LINKEDIN_PROFILE)
	msg_passwordVerify = forms.CharField(widget=XpHiddenWidget, required=False, initial = MsgSignup.PASSWORD_VERIFY)
	msg_organizationIndustry = forms.CharField(widget=XpHiddenWidget, required=False, initial = MsgSignup.ORGANIZATION_INDUSTRY)
	msg_account = forms.CharField(widget=XpHiddenWidget, required=False,  initial = MsgSignup.ACCOUNT)
	msg_ok = forms.CharField(widget=XpHiddenWidget, required=False, initial = _('Your signup has been received, check your email'))
	msgSubmit_Form1 = forms.CharField(widget=XpHiddenWidget, required=False, initial = "['" + _("We received your signup. Check your mail") + "','" + _("We have received correctly your account signup. :p:We have sent an email to validate your email address. Just click on link on Email message to activate your account.::p:::p:Thanks!::p::'") + ",'popMessageOk']")

	def isValid(self, captcha=None):
		bForm = self.validateSameFields('password','passwordVerify')
		if bForm == True and captcha != None and captcha != self.cleaned_data['captcha'] and not settings.PRIVATE_BETA:
			bForm = False
		return bForm

	def buildInitialShow(self, invitationCode, invitation, profileDict, fbAccessToken):
		"""Build initial page data from invitation data and facebook profile data"""
		self.initial = {}
		self.initial['userGroups'] = json.dumps(['1'])
		if invitation:
			self.initial['invitationCode'] = invitationCode
			self.initial['invitationType'] = invitation.type
			self.initial['invitationByUser'] = invitation.fromUser.id
			self.initial['invitationByOrg'] = invitation.fromAccount
			self.initial['accountType'] = invitation.type
		if len(profileDict) != 0:
				self.initial['firstName'] = profileDict['first_name']
				self.initial['lastName'] = profileDict['last_name']
				self.initial['email'] = profileDict['email']
				self.initial['ximpiaId'] = (profileDict['first_name'] + '.' + profileDict['last_name']).strip().lower()
				locationName = profileDict['location']['name']
				locationFields = locationName.split(',')
				self.initial['city'] = locationFields[0].strip()
				locale = profileDict['locale']
				self.initial['country'] = locale.split('_')[1].lower()
				fbIcon = SocialNetwork('facebook', 2)
				fbIcon.setToken(fbAccessToken)
				self.initial['facebookIcon_data'] = fbIcon.getS()

