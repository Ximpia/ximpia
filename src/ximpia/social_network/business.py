import random
import simplejson as json
import string
import base64
import cPickle
import datetime

from datetime import date, timedelta, datetime

from django.http import Http404
from django.db.models import Q

from django.core.mail import send_mail

from django.utils.translation import ugettext as _
from ximpia import util

import forms

from django.contrib.auth.models import User as UserSys, Group as GroupSys
from django.contrib.auth import login, authenticate, logout

from models import UserSocial, UserProfile, UserDetail, Invitation
from constants import Constants as K, KParam

from ximpia.util import ut_email

from ximpia.core.models import getResultOK, getResultERROR, XpMsgException, JsResultDict, Context as Ctx
from ximpia.core.business import CommonBusiness, ValidateFormBusiness, ShowSrvContent, EmailBusiness
from ximpia.core.data import CoreParameterDAO
from ximpia.core.constants import CoreConstants as CoreK, CoreKParam

from yacaptcha.models import Captcha
from ximpia import settings

from choices import Choices

from ximpia.util.js import Form as _jsf

from data import UserDAO, AccountDAO, OrganizationDAO, UserSysDAO, InvitationDAO, UserDetailDAO, GroupSysDAO, UserSocialDAO, ContactDAO
from data import GroupSocialDAO, ContactDetailDAO, SocialNetworkDAO, SocialNetworkUserSocialDAO, UserProfileDAO
from data import IndustryDAO, OrganizationGroupDAO, SocialNetworkOrganizationDAO, UserAccountContractDAO, TagUserTotalDAO, LinkUserTotalDAO
from data import SkillGroupDAO, SkillUserAccountDAO, VersionDAO, AddressContactDAO, CommunicationTypeContactDAO, FileVersionDAO
from data import TagTypeDAO, CalendarInviteDAO, AddressDAO, UserAccountDAO, XmlMessageDAO, SNParamDAO

import facebook

class ValidationBusiness(object):
	_objList = []
	_errorDict = {}
	_isBusinessOK = False
	def __init__(self, validateFuncDict):
		"""Validation decorator for business
		@param validateFuncDict: Dictionary with validation methods to use from validation object"""
		self._validateFuncDict = validateFuncDict
		self._errorDict = {}
		self._isBusinessOK = False
	def _doErrors(self, errorDict):
		"""Process object error container into validation error container"""
		for id in errorDict:
			self._errorDict[id] = errorDict[id]
	def _isBusinessOK(self):
		"""Checks that no errors have been generated in the validation methods
		@return: isOK : boolean"""
		if len(self._errorDict.keys()) == 0:
			self._isBusinessOK = True
		return self._isBusinessOK
	def __call__(self, f):
		"""Decorator call method"""		
		def wrapped_f(*argsTuple, **argsDict):
			print 'Fuction Dir : ', dir(f)
			print 'Class Arguments : ', dir(f.im_self)
			ctx = argsDict['ctx']
			form = ctx['form']
			bFormOK = form.is_valid()
			if bFormOK:
				keys = self._validateFuncDict.keys()
				for key in keys:
					oVal = eval(key)(ctx)
					for sFunc in self._validateFuncDict[key]:
						oVal.eval(sFunc)(*argsTuple, **argsDict)
					self._doErrors(oVal.getErrors())
			if self.isBusinessOK() and bFormOK:
				result = f(*argsTuple, **argsDict)
				# check errors
				return wrapped_f
			else:
				# Errors
				result = self._buildJSONResult(self._getErrorResultDict())
				return result
		return wrapped_f

class BaseValidationBusiness(object):
	_ctx = None
	_errorDict = {}
	def __init__(self, ctx):
		self._ctx = ctx
		self._errorDict = {}
	def addError(self, field):
		"""Add error
		@param idError: String : Id of error
		@param form: Form
		@param errorField: String : The field inside class form"""
		form = self.getForm()
		msgDict = _jsf.decodeArray(form.fields['errorMessages'].initial)		
		idError = 'id_' + field
		if not self._errorDict.has_key(idError):
			self._errorDict[idError] = {}
		self._errorDict[idError] = msgDict['ERR_' + field]
		print '_errorDict : ', self._errorDict
	def getErrors(self):
		"""Get error dict
		@return: errorDict : Dictionary"""
		return self._errorDict	
	def getForm(self):
		"""Get form from form container in context"""
		return self._ctx['form']
	def getPost(self):
		"""Get post dictionary"""
		return self._ctx['post']


class SignupValidationBusiness(BaseValidationBusiness):	
	def __init__(self, ctx):
		super(SignupValidationBusiness, self).__init__(ctx)
	def validateCaptcha(self):
		"""Validate Captcha"""
		if not settings.PRIVATE_BETA:
			if self._ctx['captcha'] != self._ctx['post']['captcha']:
				self.addError('captcha')
	def validateSameUser(self):
		"""Validate if same user is already in system"""
		try:
			# Get organization user
			form = self._ctx['form']
			user = UserSys.objects.get(username=form.d('ximpiaId'))
			self.addError(field='ximpiaId')			
		except UserSys.DoesNotExist:
			pass	
	def validateSameEmail(self, dbUser):
		"""Validates same email"""
		form = self._ctx['form']
		if dbUser.checkSameEmail(form.d('email')):
			self.addError(field='email')
	def validateSameAccount(self, dbOrganization):
		"""Validates same account"""
		try:
			form = self._ctx['form']
			organization = dbOrganization.getByAccount(form.d('account'))
			self.addError(field='account')
		except:
			pass
	def getInvitation(self, dbUser):
		"""Get invitation. Processes in case of adding error when not found invitation.
		@return: invitation : Invitation"""
		postDict = self._ctx['post']
		invitationCode = postDict['invitationCode']
		try:
			invitation = dbUser.getInvitation(invitationCode)
		except Invitation.DoesNotExist:
			if settings.PRIVATE_BETA == True:
				self.addError('invitationCode')
		return invitation
	def validateProfessional(self):
		pass


class LoginBusiness(CommonBusiness):
	def __init__(self, ctx):
		super(LoginBusiness, self).__init__(ctx)
		self._dbUserAccount = UserAccountDAO(ctx)
		self._dbUserSys = UserSysDAO(ctx)
		self._dbXmlMessage = XmlMessageDAO(ctx)
		self._dbUserDetail = UserDetailDAO(ctx)
		self._dbParam = SNParamDAO(ctx)
		self._f = ctx[Ctx.FORM]
	
	@ValidateFormBusiness(forms.LoginForm, pageError=True)
	def doLogin(self, **dd):
		"""Performs the login action
		@param ctx: Context
		@return: result"""
		user = self.authenticateUser(	userName = self._f.d('ximpiaId'), 
						password = self._f.d('password'), 
						errorName = 'wrongPassword')
		self.isValid()
		login(self._ctx[Ctx.RAW_REQUEST], user)
	
	@ValidateFormBusiness(forms.PasswordReminderForm, pageError=True)
	def doPasswordReminder(self):
		"""Checks that email exists, then send email to user with reset link"""
		# Checks that email sent is in system
		self.validateExists([
					[self._dbUserSys, {'email': self._f.d('email')}, 'emailDoesNotExist']
				])
		self.isValid()
		# Update User
		user = self._dbUserSys.get(email = self._f.d('email'))
		userDetail = self._dbUserDetail.get(user=user) 
		days = self._dbParam.get(mode=KParam.LOGIN, name=KParam.REMINDER_DAYS).valueId
		newDate = date.today() + timedelta(days=days)
		userDetail.resetPasswordDate = datetime.date(newDate)
		# Set reminderId
		userDetail.reminderId = str(random.randint(1, 999999))
		userDetail.save()
		# Send email with link to reset password. Link has time validation
		xmlMessage = self._dbXmlMessage.get(name='Msg/SocialNetwork/Login/PasswordReminder/', lang='en').body
		EmailBusiness.send(xmlMessage, {'firstName': user.first_name, 'userAccount': user.username,
						'reminderId': userDetail.reminderId}, [self._f.d('email')])
		self.setOkMsg('OK_PASSWORD_REMINDER')
	
	@ValidateFormBusiness(forms.ChangePasswordForm, pageError=True)
	def doNewPassword(self):
		"""Saves new password, it does authenticate and login user."""
		user = self._dbUserSys.get(username= self._f.getParam('ximpiaId'))
		user.set_password(self._f.d('newPassword'))
		user.save()
		userDetail = self._dbUserDetail.get(user=user)
		userDetail.reminderId = None
		userDetail.resetPasswordDate = None
		userDetail.save()
		#login(self._ctx[Ctx.RAW_REQUEST], user)
	
	@ShowSrvContent(forms.ChangePasswordForm)
	def showNewPassword(self, ximpiaId, reminderId):
		"""Shows form to enter new password and confirm new password. Save button will call doNewPassword."""
		days = self._dbParam.get(mode=KParam.LOGIN, name=KParam.REMINDER_DAYS).valueId
		newDate = date.today() + timedelta(days=days)
		# Show actual password, new password and confirm new password
		self.validateExists([
					[self._dbUserSys, {'username': ximpiaId}, 'changePassword'],
					[self._dbUserDetail, {	'user__username': ximpiaId, 
								'reminderId': reminderId, 
								'resetPasswordDate__lt' : newDate}, 'changePassword'],
					])		
		# validate
		self.isValid()
		self._f.putParamList(ximpiaId=ximpiaId)
	
	def login(self):
		"""Checks if user is logged in. If true, get login user information in the context
		@param ctx: Context
		@return: result"""
		# Check if login:
		print 'login...'
		if self._ctx['user'].is_authenticated():
			# login: context variable isLogin = True
			jsData = JsResultDict()
			jsData.addAttr('isLogin', True)
			jsData.addAttr('userid', self._ctx['user'].pk)
		else:
			# no login: login form
			jsData = JsResultDict()
			self._ctx[Ctx.FORM] = forms.LoginForm()
			self._ctx[Ctx.FORM].buildJsData(jsData)
			#print invitation.invitationCode, jsData['response']['form_signup']['invitationCode']
			jsData.addAttr('isLogin', False)			
		# Popup - Password reminder
		self._ctx[Ctx.FORM] = forms.PasswordReminderForm()
		self._ctx[Ctx.FORM].buildJsData(jsData)
		result = self.buildJSONResult(jsData)
		print 'result: ', result
		return result

class ContactBusiness(CommonBusiness):
	def __init__(self, ctx):
		super(ContactBusiness, self).__init__(ctx)
		self._dbContactDetail = ContactDetailDAO(ctx)
		self._dbAddress = AddressDAO(ctx)
		self._dbAddressContact = AddressContactDAO(ctx)
		self._dbCoreParam = CoreParameterDAO(ctx)
		self._dbCommunicationTypeContact = CommunicationTypeContactDAO(ctx)
		self._dbContact = ContactDAO(ctx)
		self._f = ctx[Ctx.FORM]
	
	def createDirectoryUser(self, user, userSocial):
		"""Create user in directory"""
		try:
			# ContactDetail
			contactDetail = self._dbContactDetail.create(user=user, firstName=self._f.d('firstName'), 
					lastName=self._f.d('lastName'), name=self._f.d('firstName') + ' ' + self._f.d('lastName'))
			groupList = userSocial.groups.all()
			for group in groupList:
				if group.isIndustry:
					contactDetail.industries.add(group)
				else:
					contactDetail.groups.add(group)
			# City and Country
			address, bCreate = self._dbAddress.getCreate(city=self._f.d('city'), country=self._f.d('country'))
			self._dbAddressContact.create(addressType=Choices.ADDRESS_TYPE_HOME, contact=contactDetail, address=address)
			# Email
			communicationTypeEmail = self._dbCoreParam.get(mode=CoreKParam.COMMTYPE, name=CoreK.EMAIL)
			comContact = self._dbCommunicationTypeContact.create(communicationType=communicationTypeEmail,
						contact=contactDetail, value=self._f.d('email'))
			# Contact
			contact, bCreate = self._dbContact.getCreate(user=userSocial, detail=contactDetail)
			return contactDetail
		except Exception as e:
			print e
			raise XpMsgException(e, _('Error creating user in directory'))


class SignupBusiness(CommonBusiness):

	def __init__(self, ctx):
		super(SignupBusiness, self).__init__(ctx)
		self._dbUserSys = UserSysDAO(ctx)
		self._dbAccount = AccountDAO(ctx)
		self._dbOrganization = OrganizationDAO(ctx)
		self._dbInvitation = InvitationDAO(ctx)
		self._dbUserDetail = UserDetailDAO(ctx)
		self._dbGroupSys = GroupSysDAO(ctx)
		self._dbUserSocial = UserSocialDAO(ctx)
		self._dbGroupSocial = GroupSocialDAO(ctx)
		self._dbUserAccount = UserAccountDAO(ctx)
		self._dbUser = UserDAO(ctx)
		self._contact = ContactBusiness(ctx)
		self._f = ctx[Ctx.FORM]
	
	@ShowSrvContent(forms.UserSignupForm)
	def showSignupUser(self, invitationCode, affiliateId):
		"""Show signup form. Get get invitation code."""
		self.validateNotExists([
				[self._dbInvitation, {'invitationCode': invitationCode, 'status': K.USED}, 'invitationUsed']
				])
		self.isValid()
		invitation = self._dbUser.getInvitation(invitationCode, status=K.PENDING)
		self._ctx['affiliateid'] = json.dumps(affiliateId)
		self._f = forms.UserSignupForm(instances = {'dbInvitation': invitation})
	
	@ValidateFormBusiness(forms.UserSignupForm)
	def doUser(self):
		"""Signup professional user
		@param ctx: Context"""
		# Validation
		self.validateNotExists([
				[self._dbUserSys, {'username': self._f.d('ximpiaId')}, 'ximpiaId'],
				[self._dbUserSys, {'email': self._f.d('email')}, 'email']
				])
		self.validateExists([
				[self._dbInvitation, {'invitationCode': self._f.d('invitationCode')}, 'invitationCode']
				])
		self.isValid()
		# Business
		# Invitation
		invitation = self._dbInvitation.get(invitationCode=self._f.d('invitationCode'))
		# System User
		user = self._dbUserSys.create(username=self._f.d('ximpiaId'), email=self._f.d('email'), 
						first_name=self._f.d('firstName'), last_name=self._f.d('lastName'))
		user.set_password(self._f.d('password'))
		user.save()
		# Ximpia User
		userSocial = self._dbUserSocial.create(user=user, socialChannel=K.PROFESSIONAL, userCreateId=user.id)
		userDetail = self._dbUserDetail.create(user=user, name=self._f.d('firstName') + ' ' + self._f.d('lastName'), hasValidatedEmail=True)
		# Groups
		userGroupId = json.loads(self._f.d('params'))['userGroup']
		group = self._dbGroupSys.get(id=userGroupId)
		groupSocial = self._dbGroupSocial.get(group__id=group.id)
		user.groups.add(group)
		userSocial.groups.add(groupSocial)
		# Directory		
		contactDetail = self._contact.createDirectoryUser(user, userSocial)
		# InvitedBy
		invitedByUser = None
		invitedByOrg = None
		if invitation.fromUser.pk != None:
			invitedByUser = self._dbUserSys.get(pk=invitation.fromUser.pk)
		if invitation.fromAccount != None:
			invitedByOrg = self._dbOrganization.get(account=invitation.fromAccount)
		# UserAccount
		userAccount = self._dbUserAccount.create(user=userDetail, invitedByUser=invitedByUser, invitedByOrg=invitedByOrg,
							contact=contactDetail, userCreateId=user.pk)
		# Modify Invitation
		invitation.status = K.USED
		invitation.save() 
	
	#def activateAccount(self, user, activationCode):
		"""Activate account
		@param user: User
		@param activationCode: Activation Code
		@return: resultDict"""
		"""signupData = self._dbUser.getSignupData(user)
		sData = signupData.data.encode('utf-8')
		formDict = cPickle.loads(base64.decodestring(sData))
		activationCode = int(activationCode)
		if signupData.activationCode == activationCode:
			# Activation code is the same, we process request
			if not formDict.has_key('account'):
				# user account
				self._ctx['form'] = forms.UserSignupForm(formDict)
				self._dbAccount.doSignup(self._ctx)
				resultDict = getResultOK([])
			else:
				# organization account
				form = forms.FrmOrganizationSignup(formDict)
				self._dbAccount.doOrganizationSignup(form)
				# Email Administrator to validate account
				xmlMessage = XmlMessage.objects.get(name='Msg/SocialNetwork/Signup/AdminNotify/', lang='en').body
				subject, message = ut_email.getMessage(xmlMessage)
				message = string.Template(message).substitute()
				# send mail
				send_mail(subject, message, settings.WEBMASTER_EMAIL, [settings.WEBMASTER_EMAIL])
				#staticContent(request, 'login', message=_('Your account has been activated'))
				# login user
				# Should redirect to /in/$account
				#return HttpResponse('OK, user account created')
				resultDict = getResultOK([])
			# ValidatedEmail
			userDetail = UserDetail.objects.get(user__username=user)
			userDetail.isValidatedEmail = True
			userDetail.save()
			# Invitation => Change Status
			invitationCode = formDict['invitationCode']
			try:
				invitation = self._dbUser.getInvitation(invitationCode)
				invitation = self._dbUser.changeInvitationUsed(invitation)
			except:
				invitation = None
		else:
			# Activation code is not same => We show original form with message
			resultDict = getResultERROR([])
		print 'resultDict : ', resultDict
		return resultDict"""
	
	#def _getNetworkProfile(self, form, bFacebookLogin):
		"""Doc."""
		"""# Get facebook profile
		profilesDict = {}
		facebookIcon_data = form.cleaned_data['facebookIcon_data']
		fbIconTuple = json.loads(facebookIcon_data)
		dataDict = fbIconTuple[1]
		fbToken = dataDict['token']
		if fbToken != '' or bFacebookLogin:
			graph = facebook.GraphAPI(fbToken)
			try:
				fbProfileDict = graph.get_object("me");
				profilesDict['facebook'] = fbProfileDict
				form.cleaned_data['profiles'] = json.dumps(profilesDict)
			except facebook.GraphAPIError:
				pass
		# Get LinkedIn profile
		linkedInIcon_data = form.cleaned_data['linkedinIcon_data']
		profilesDict['linkedin'] = False
		# TODO: do linkedin profile...		
		# Build in case only Facebook, Only LinkedIn or both"""		
		"""if profilesDict['facebook'] == True and profilesDict['linkedin'] == False:
			pass
		elif profilesDict['facebook'] == False and profilesDict['linkedin'] == True:
			pass"""		
		# 1.0 => Only Facebook
		"""if profilesDict['facebook'] == True:
			if fbProfileDict.has_key('bio'): profile.bio = fbProfileDict['bio']
			if fbProfileDict.has_key('hometown'): profile.homeTown = fbProfileDict['hometown']['name']
			if fbProfileDict.has_key('quotes'): profile.favQuotes = fbProfileDict['quotes']
			if fbProfileDict.has_key('gender'): profile.sex = fbProfileDict['gender']"""
		
		"""
	politicalViews = models.CharField(max_length=50, null=True, blank=True)
	religiousViews = models.CharField(max_length=50, null=True, blank=True)
	relationship = models.CharField(max_length=20, choices=Choices.RELATIONSHIP, null=True, blank=True)
	activities = models.CharField(max_length=500, null=True, blank=True)
	interests = models.CharField(max_length=500, null=True, blank=True)
	music = models.CharField(max_length=500, null=True, blank=True)
	books = models.CharField(max_length=500, null=True, blank=True)
	movies = models.CharField(max_length=500, null=True, blank=True)
	television = models.CharField(max_length=500, null=True, blank=True)
		"""		
		"""
{u'bio': u'Passionate about life, love my home city, Madrid, enjoy tapas, walking around the city, terrazas and cafes. 
Like hang around in VIPS restaurant, love night life and cute and interesting people\r\n\r\nI graduated from University of 
Kansas in Aerospace Engineering. Living in the US was a great experience and taught me many things. I also loved the american 
music, like Blues, Cajun Music, Rock.\r\n\r\nCame back to Madrid, Spain, where I live now. It is a great city, where you can do 
so many things, but what I love more is the night life.\r\n\r\nI am a normal guy that enjoys life and ordinary things, like a nice 
food, enjoying a sunset, nature, etc...', u'first_name': u'Jorge', u'last_name': u'Alegre', u'verified': True, u'name': u'Jorge Alegre', 
u'locale': u'en_US', u'hometown': {u'id': u'106504859386230', u'name': u'Madrid, Spain'}, u'work': [{u'position': 
{u'id': u'110785958946092', u'name': u'CEO'}, u'start_date': u'1995-01', u'location': {u'id': u'106504859386230', 
u'name': u'Madrid, Spain'}, u'employer': {u'id': u'104996346207771', u'name': u'Tecor'}}], u'email': u'jorge_alegre@yahoo.es', 
u'quotes': u'"Never ever ever give up" "\xa1\xa1\xa1Adelante!!!"', u'birthday': u'11/25/1968', 
u'link': u'http://www.facebook.com/jorge.alegre', u'location': {u'id': u'106504859386230', u'name': u'Madrid, Spain'}, 
u'gender': u'male', u'timezone': 1, u'updated_time': u'2011-01-02T18:54:59+0000', u'id': u'602227728'}

		"""
		"""return form"""
	"""def doOrganization(self, form, captcha, bFacebookLogin, *argsTuple, **argsDict):
		self.setForm(form) 
		self.setFormOK(form.isValid(captcha=captcha))
		if self._isFormOK: 
			invitation = self._getInvitation()
			self._validateCaptcha()
			self._validateSameUser()
			self._validateSameEmail()
			self._validateSameAccount()
		if self.isBusinessOK() and self._isFormOK:
			activationCode = random.randint(1,9999)
			sUser = form.cleaned_data['ximpiaId']
			print 'bFacebookLogin: ', bFacebookLogin
			if not bFacebookLogin:
				# User/Password, we need to validate email address
				xmlMessage = XmlMessage.objects.get(name='Msg/SocialNetwork/Signup/Organization/', lang=self._ctx.lang).body
				subject, message = ut_email.getMessage(xmlMessage)
				message = string.Template(message).substitute(	host = settings.MAIL_HOST,
										name = form.cleaned_data['firstName'],
										user = str(sUser),
										lang = self._ctx.lang, 
										activationCode = str(activationCode),
										account = str(form.cleaned_data['account']))
				# send mail
				send_mail(subject, message, settings.WEBMASTER_EMAIL, [form.cleaned_data['email']])
		
			form = self._getNetworkProfile(form, bFacebookLogin)
		
			# Show Result
			if bFacebookLogin == False:
				# User / Password
				resultDict = getResultOK([])
				# Write Signup Data to DB
				signupData = self._dbUser.writeSignupData(sUser, activationCode, invitation, form.cleaned_data)
			else:
				# Facebook Login
				# In case facebook, no need to activate account. Create account directly
				print 'Will create account'
				self._dbAccount.doOrganizationSignup(form)
				# Change status of invitation to used
				invitation = self._dbUser.changeInvitationUsed(invitation)
				print 'Invitation Status: ', invitation.status
				resultDict = getResultOK([], status='OK.create')			
			print 'resultDict', resultDict, type(resultDict)
			# login and show control panel if login from facebook
			# Redirect
			result = self._buildJSONResult(resultDict)
		else:
			# Errors
			result = self._buildJSONResult(self._getErrorResultDict())
		return result"""
