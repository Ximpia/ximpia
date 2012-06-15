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

from models import UserProfile, UserDetail, Invitation
from constants import Constants as K, KParam

from ximpia.util import ut_email

from ximpia.core.models import getResultOK, getResultERROR, XpMsgException, JsResultDict, Context as Ctx, UserSocial,\
	Workflow
from ximpia.core.business import CommonBusiness, EmailBusiness, WorkFlowBusiness
from ximpia.core.business import ValidateFormDecorator, WFActionDecorator, DoBusinessDecorator, WFViewDecorator, MenuActionDecorator,\
	ValidationDecorator
from ximpia.core.data import CoreParameterDAO, UserSocialDAO
from ximpia.core.constants import CoreConstants as CoreK, CoreKParam

from yacaptcha.models import Captcha
from ximpia import settings

from choices import Choices

from ximpia.util.js import Form as _jsf

from data import UserDAO, AccountDAO, OrganizationDAO, UserSysDAO, InvitationDAO, UserDetailDAO, GroupSysDAO, ContactDAO
from data import GroupSocialDAO, ContactDetailDAO, SocialNetworkDAO, SocialNetworkUserSocialDAO, UserProfileDAO
from data import IndustryDAO, OrganizationGroupDAO, SocialNetworkOrganizationDAO, UserAccountContractDAO, TagUserTotalDAO, LinkUserTotalDAO
from data import SkillGroupDAO, SkillUserAccountDAO, VersionDAO, AddressContactDAO, CommunicationTypeContactDAO, FileVersionDAO
from data import TagTypeDAO, CalendarInviteDAO, AddressDAO, UserAccountDAO, XmlMessageDAO, SNParamDAO

import facebook
from ximpia.social_network.forms import UserSignupForm

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
			user = UserSys.objects.get(username=form['ximpiaId'])
			self.addError(field='ximpiaId')			
		except UserSys.DoesNotExist:
			pass	
	def validateSameEmail(self, dbUser):
		"""Validates same email"""
		form = self._ctx['form']
		if dbUser.checkSameEmail(form['email']):
			self.addError(field='email')
	def validateSameAccount(self, dbOrganization):
		"""Validates same account"""
		try:
			form = self._ctx['form']
			organization = dbOrganization.getByAccount(form['account'])
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
		self._dbUserSocial = UserSocialDAO(ctx)
		self._dbParam = SNParamDAO(ctx)
	
	@WFViewDecorator('login')
	@DoBusinessDecorator(pageError=True)
	def showLogin(self):
		"""Checks if user is logged in. If true, get login user information in the context
		@param ctx: Context
		@return: result"""
		# Check if login:
		print 'login...'
		"""if self._ctx['user'].is_authenticated():
			# login: context variable isLogin = True
			self._ctx[Ctx.JS_DATA].addAttr('isLogin', True)
			self._ctx[Ctx.JS_DATA].addAttr('userid', self._ctx['user'].pk)
			# Include user_info, a dictionary with user environment data
			viewName = 'home'
			self._setMainForm(forms.LoginForm())
			self._ctx[Ctx.VIEW_NAME_TARGET] = viewName
			print 'ximpiaId: ', self._ctx[Ctx.USER].username.encode(settings.DEFAULT_CHARSET)
			self._putParams(ximpiaId=self._ctx[Ctx.USER].username.encode(settings.DEFAULT_CHARSET))
			# Get implementation for view
			home = HomeView(self._ctx)
			home.showStatus()
			pass"""
		if not self._ctx['user'].is_authenticated():
			# no login: login form
			self._setMainForm(forms.LoginForm())
			#self._ctx[Ctx.FORM].buildJsData(self._ctx[Ctx.JS_DATA])
			#print invitation.invitationCode, jsData['response']['form_signup']['invitationCode']
			self._ctx[Ctx.JS_DATA].addAttr('isLogin', False)
			# Popup - Password reminder
			self._addForm(forms.PasswordReminderForm())

	@DoBusinessDecorator(pageError=True)
	def showLogout(self):
		"""Show logout view"""
		self._ctx[Ctx.JS_DATA].addAttr('isLogin', False)

	@DoBusinessDecorator(form = forms.ChangePasswordForm, isServerTmpl=True)
	def showNewPassword(self, ximpiaId=None, reminderId=None):
		"""Shows form to enter new password and confirm new password. Save button will call doNewPassword.
		@param ximpiaId: ximpiaId
		@param reminderId: reminderId"""
		# validate that ximpiaId and reminderId are informed
		days = self._dbParam.get(mode=KParam.LOGIN, name=KParam.REMINDER_DAYS).valueId
		newDate = date.today() + timedelta(days=days)
		print 'New Password Data : ', ximpiaId, newDate, reminderId
		# Show actual password, new password and confirm new password
		self._validateExists([
					[self._dbUserSys, {'username': ximpiaId}, 'changePassword'],
					[self._dbUserDetail, {	'user__username': ximpiaId, 
								'reminderId': reminderId, 
								'resetPasswordDate__lte' : newDate}, 'changePassword'],
					])		
		# validate
		self._isValid()
		self._f().putParamList(ximpiaId=ximpiaId)
	
	@ValidateFormDecorator(forms.LoginForm)
	@WFActionDecorator()
	def doLogin(self):
		"""Performs the login action
		@param ctx: Context
		@return: result"""
		print 'doLogin...'
		#self._f()['ximpiaId']
		print 'form: ', self._ctx[Ctx.FORM], self._f()['ximpiaId']
		self._ctx[Ctx.USER] = self._authenticateUser(	userName = self._f()['ximpiaId'], 
						password = self._f()['password'], 
						errorName = 'wrongPassword'	)
		self._isValid()
		print 'user: ', self._ctx[Ctx.USER]
		self._login()
		# Include login info
		# Include user_info, a dictionary with user environment data		
		# Context => viewNameSource, actionName, flowCode (inserted in context by WorkflowView)
		#self._wf = WorkFlowBusiness(self._ctx)
		#print 'Will insert into workflow : ximpiaId: ', user.username, self._ctx[Ctx.FLOW_CODE]
		self._putFlowParams(ximpiaId=self._ctx[Ctx.USER].username.encode(settings.DEFAULT_CHARSET))		
		#print self._wf.getFlowDataDict(self._ctx[], self._ctx[], self._ctx[Ctx.FLOW_CODE])
		# How we get? viewNameSource, actionName to resolve view??? => Context		
		# Workflow will take control, check that view home must be shown
		print 'Session: ', self._ctx[Ctx.SESSION]
		print 'user: ', self._ctx[Ctx.USER]
		print 'cookies: ', self._ctx[Ctx.COOKIES]
		userSocialName = self._getUserSocialName()
		print 'userSocialName: ', userSocialName
		self._ctx[Ctx.USER_SOCIAL] = self._dbUserSocial.get(user=self._ctx[Ctx.USER], name=userSocialName)
		self._ctx[Ctx.SESSION]['userSocial'] = self._ctx['userSocial']
		print 'userSocial: ', self._ctx['userSocial']

	@MenuActionDecorator('logout')
	def doLogout(self):
		"""Logout user"""
		print 'doLogout...'
		self._logout()
		print 'doLogout :: WF Data: ', self._getWFUser()
		self._wf.removeData(self._getWFUser(), 'login')
		print 'did logout...'
	
	@ValidateFormDecorator(forms.PasswordReminderForm)
	@DoBusinessDecorator(pageError=True)
	def doPasswordReminder(self):
		"""Checks that email exists, then send email to user with reset link"""
		# Checks that email sent is in system
		self._validateExists([
					[self._dbUserSys, {'email': self._f()['email']}, 'emailDoesNotExist']
				])
		self._isValid()
		# Update User
		user = self._dbUserSys.get(email = self._f()['email'])
		userDetail = self._dbUserDetail.get(user=user) 
		days = self._dbParam.get(mode=KParam.LOGIN, name=KParam.REMINDER_DAYS).valueId
		newDate = date.today() + timedelta(days=days)
		#print 'newDate: ', newDate, type(newDate)
		#userDetail.resetPasswordDate = datetime.date(newDate)
		userDetail.resetPasswordDate = newDate
		# Set reminderId
		userDetail.reminderId = str(random.randint(1, 999999))
		userDetail.save()
		# Send email with link to reset password. Link has time validation
		xmlMessage = self._dbXmlMessage.get(name='Msg/SocialNetwork/Login/PasswordReminder/', lang='en').body
		EmailBusiness.send(xmlMessage, {'firstName': user.first_name, 'userAccount': user.username,
						'reminderId': userDetail.reminderId}, [self._f()['email']])
		self.setOkMsg('OK_PASSWORD_REMINDER')
	
	@ValidateFormDecorator(forms.ChangePasswordForm)
	@DoBusinessDecorator(pageError=True)
	def doNewPassword(self):
		"""Saves new password, it does authenticate and login user."""
		user = self._dbUserSys.get(username= self._f().getParam('ximpiaId'))
		user.set_password(self._f()['newPassword'])
		user.save()
		userDetail = self._dbUserDetail.get(user=user)
		userDetail.reminderId = None
		userDetail.resetPasswordDate = None
		userDetail.save()
		#login(self._ctx[Ctx.RAW_REQUEST], user)


class HomeBusiness(CommonBusiness):
	
	def __init__(self, ctx):
		super(HomeBusiness, self).__init__(ctx)
	
	@WFViewDecorator('login')
	@DoBusinessDecorator(form = forms.HomeForm)
	def showStatus(self):
		"""Status home view"""
		print 'showStatus...'
		print 'I do the status and home view...'
		dd = self._getFlowParams('ximpiaId')
		print 'showStatus :: param values: ', dd

class UserBusiness ( CommonBusiness ):
	
	def __init__(self, ctx):
		super(UserBusiness, self).__init__(ctx)
		self._dbUserSys = UserSysDAO(ctx)
	
	@DoBusinessDecorator(form = forms.UserChangePasswordForm, pageError=True)
	def showChangePassword(self):
		"""Change password form with current password and new password"""
		pass
	
	@ValidationDecorator()
	def _validateUser(self):
		"""Validate user: Check user password"""
		self._ctx[Ctx.USER] = self._authenticateUser(	userName = self._ctx[Ctx.USER], 
								password = self._f()['password'], 
								errorName = 'passwordValidate'	)
	
	@ValidateFormDecorator(forms.UserChangePasswordForm)
	@DoBusinessDecorator(pageError=True)
	def doChangePassword(self):
		"""Change password from user area"""
		self._validateUser()
		user = self._dbUserSys.get(username= self._ctx[Ctx.USER])
		user.set_password(self._f()['newPassword'])
		user.save()
	
class ContactBusiness( CommonBusiness ):

	def __init__(self, ctx):
		super(ContactBusiness, self).__init__(ctx)
		self._dbContactDetail = ContactDetailDAO(ctx)
		self._dbAddress = AddressDAO(ctx)
		self._dbAddressContact = AddressContactDAO(ctx)
		self._dbCoreParam = CoreParameterDAO(ctx)
		self._dbCommunicationTypeContact = CommunicationTypeContactDAO(ctx)
		self._dbContact = ContactDAO(ctx)
		self._dbGroupSocial = GroupSocialDAO(ctx)
	
	def createDirectoryUser(self, user, userSocial):
		"""Create user in directory"""
		# ContactDetail
		form = self._ctx[Ctx.FORM]
		contactDetail = self._dbContactDetail.create(user=user, firstName=form['firstName'], 
				lastName=form['lastName'], name=form['firstName'] + ' ' + form['lastName'])
		groupList = userSocial.groups.all()
		for group in groupList:
			groupSocial = self._dbGroupSocial.get(group=group)
			if groupSocial.isIndustry:
				contactDetail.industries.add(groupSocial)
			else:
				contactDetail.groups.add(groupSocial)
		# City and Country
		address, bCreate = self._dbAddress.getCreate(city=form['city'], country=form['country'])
		self._dbAddressContact.create(addressType=Choices.ADDRESS_TYPE_HOME, contact=contactDetail, address=address)
		# Email
		communicationTypeEmail = self._dbCoreParam.get(mode=CoreKParam.COMMTYPE, name=CoreK.EMAIL)
		comContact = self._dbCommunicationTypeContact.create(communicationType=communicationTypeEmail,
					contact=contactDetail, value=form['email'])
		# Contact
		contact, bCreate = self._dbContact.getCreate(user=userSocial, detail=contactDetail)
		return contactDetail


class SignupBusiness(CommonBusiness):

	def __init__(self, ctx):
		super(SignupBusiness, self).__init__(ctx)
		self._dbInvitation = InvitationDAO(ctx)
		self._dbUser = UserDAO(ctx)
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
		self._contact = ContactBusiness(self._ctx)		
	
	@DoBusinessDecorator(pageError=True, form=forms.UserSignupForm, isServerTmpl=True)
	def showSignupUser(self, invitationCode=None, affiliateId=None):
		"""Show signup form. Get get invitation code.""" 
		self._validateNotExists([
				[self._dbInvitation, {'invitationCode': invitationCode, 'status': K.USED}, 'invitationUsed']
				])
		self._isValid() 
		invitation = self._dbUser.getInvitation(invitationCode, status=K.PENDING)
		self._ctx['affiliateid'] = json.dumps(affiliateId)
		self._setMainForm(forms.UserSignupForm(instances = {'dbInvitation': invitation}))
	
	@ValidateFormDecorator(forms.UserSignupForm)
	@DoBusinessDecorator()
	def doUser(self):
		"""Signup professional user
		@param ctx: Context"""
		# Validation
		self._validateNotExists([
				[self._dbUserSys, {'username': self._f()['ximpiaId']}, 'ximpiaId'],
				[self._dbUserSys, {'email': self._f()['email']}, 'email']
				])
		self._validateExists([
				[self._dbInvitation, {'invitationCode': self._f()['invitationCode']}, 'invitationCode']
				])
		self._isValid()
		# Business
		# Invitation
		invitation = self._dbInvitation.get(invitationCode=self._f()['invitationCode'])
		# System User
		user = self._dbUserSys.create(username=self._f()['ximpiaId'], email=self._f()['email'], 
						first_name=self._f()['firstName'], last_name=self._f()['lastName'])
		user.set_password(self._f()['password'])
		user.save()
		# Ximpia User
		userSocial = self._dbUserSocial.create(user=user, name=K.USER, title=self._f()['firstName'], userCreateId=user.id)
		userDetail = self._dbUserDetail.create(user=user, name=self._f()['firstName'] + ' ' + self._f()['lastName'], hasValidatedEmail=True)
		# Groups
		userGroupId = json.loads(self._f()['params'])['userGroup']
		group = self._dbGroupSys.get(id=userGroupId)
		groupSocial = self._dbGroupSocial.get(group__id=group.id)
		user.groups.add(group)
		userSocial.groups.add(group)
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
		self._dbUserAccount.create(user=userDetail, invitedByUser=invitedByUser, invitedByOrg=invitedByOrg,
							contact=contactDetail, userCreateId=user.pk)
		# Modify Invitation
		invitation.status = K.USED
		invitation.save()
