import random
import simplejson as json
import string
import base64
import cPickle

from django.http import HttpResponse
from django.db.models import Q

from django.core.mail import send_mail

from django.utils.translation import ugettext as _
from ximpia import util

import forms

from django.contrib.auth.models import User as UserSys, Group as GroupSys

from models import UserSocial, XmlMessage, UserProfile, UserDetail, Constants, Invitation

from ximpia.util import ut_email

from ximpia.core.models import getResultOK, getResultERROR

from yacaptcha.models import Captcha
from ximpia import settings

from ximpia.util.js import Form as _jsf

from data import UserDAO, AccountDAO, OrganizationDAO

import facebook

class Common(object):
	
	_ctx = None
	_request = None
	_errorDict = {}
	_resultDict = {}
	_form = None
	_postDict = {}
	_isBusinessOK = False
	_isFormOK = None
	
	def __init__(self, ctx):
		self._ctx = ctx
		self._resultDict = getResultERROR([])
		self._postDict = ctx['post']
		self._errorDict = {}
		self._resultDict = {}
		self._isFormOK = None
	
	def buildJSONResult(self, resultDict):
		"""Builds json result
		@param resultDict: dict : Dictionary with json data
		@return: result : HttpResponse"""
		result = HttpResponse(json.dumps(resultDict))
		return result
	
	def _addError(self, idError, form, errorField):
		"""Add error
		@param idError: String : Id of error
		@param form: Form
		@param errorField: String : The field inside class form"""
		if not self._errorDict.has_key(idError):
			self._errorDict[idError] = {}
		self._errorDict[idError] = form.fields[errorField].initial
	
	def getErrorResultDict(self, errorDict):
		"""Get sorted error list to show in pop-up window
		@return: self._resultDict : ResultDict"""		
		#dict = self._errorDict
		keyList = errorDict.keys()
		keyList.sort()
		list = []
		for key in keyList:
			message = errorDict[key]
			index = key.find('id_')
			if index == -1:
				list.append(('id_' + key, message))
			else:
				list.append((key, message))
		self._resultDict = getResultERROR(list)
		return self._resultDict

	def _doValidations(self, validationDict):
		"""Do all validations defined in validation dictionary"""
		bFormOK = self._ctx['form'].is_valid()
		if bFormOK:
			keys = self.validationDict.keys()
			for key in keys:
				oVal = eval(key)(self._ctx)
				for sFunc in self.validationDict[key]:
					oVal.eval(sFunc)()
				self._doErrors(oVal.getErrors())
		"""if self.isBusinessOK() and bFormOK:
			result = f(*argsTuple, **argsDict)
			# check errors
			return wrapped_f
		else:
			# Errors
			result = self._buildJSONResult(self._getErrorResultDict())
			return result"""
	
	def getForm(self):
		"""Get form"""
		return self._ctx['form']
	
	def setForm(self, form):
		"""Sets the form"""
		self._ctx['form'] = form
	
	def getPostDict(self):
		"""Get post dictionary. This will hold data even if form is not validated. If not validated cleaned_value will have no values"""
		return self._postDict
	
	def isBusinessOK(self):
		"""Checks that no errors have been generated in the validation methods
		@return: isOK : boolean"""
		if len(self._errorDict.keys()) == 0:
			self._isBusinessOK = True
		return self._isBusinessOK
	
	def _isFormValid(self):
		"""Is form valid?"""
		if self._isFormOK == None:
			self._isFormOK = self._ctx['form'].is_valid()
		return self._isFormOK

	def _isFormBsOK(self):
		"""Is form valid and business validations passed?"""
		bDo = False
		if len(self._errorDict.keys()) == 0:
			self._isBusinessOK = True
		if self._isFormOK == True and self._isBusinessOK == True:
			bDo = True
		return bDo

class EmailBusiness(object):
	#python -m smtpd -n -c DebuggingServer localhost:1025
	@staticmethod
	def send(keyName, subsDict, recipientList, lang):
		"""Send email
		@param keyName: keyName for datastore
		@subsDict : Dictionary with substitution values for template
		@param recipientList: List of emails to send message"""
		xmlMessage = XmlMessage.objects.get(name=keyName, lang=lang).body
		subject, message = ut_email.getMessage(xmlMessage)
		message = string.Template(message).substitute(**subsDict)
		send_mail(subject, message, settings.WEBMASTER_EMAIL, recipientList)

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

class SignupBusiness(Common):	
	_ctx = None
	_request = None
	_TMPL_SIGNUP_PROFESSIONAL = 'social_network/signupProfessional.html'
	_TMPL_SIGNUP_ORGANIZATION = 'social_network/signupOrganization.html'
	_TMPL_SIGNUP_OK = 'social_network/signupOK.msg.html'
	def __init__(self, ctx):
		super(SignupBusiness, self).__init__(ctx)
		self._dbUser = UserDAO(ctx)
		self._dbAccount = AccountDAO(ctx)
		self._dbOrganization = OrganizationDAO(ctx)
		self._valSignup = SignupValidationBusiness(ctx)
	def doProfessional(self, bFacebookLogin):
		"""Signup professional user"""
		# Validation
		invitation = self._valSignup.getInvitation(self._dbUser)
		self._valSignup.validateSameUser()
		self._valSignup.validateSameEmail(self._dbUser)
		self._errorDict = self._valSignup.getErrors()
		# Business
		if self.isBusinessOK():
			form = self._ctx['form']
			# Signup
			form = self._getNetworkProfile(form, bFacebookLogin)		
			self._dbAccount.doSignup(form)
			invitation = self._dbUser.changeInvitationUsed(invitation)
			resultDict = getResultOK([], status='OK.create')			
			# login and show control panel if login from facebook
			# Redirect
			result = self.buildJSONResult(resultDict)
			print result
		else:
			# Errors
			result = self.buildJSONResult(self.getErrorResultDict(self._errorDict))
		return result
	def activateAccount(self, user, activationCode):
		"""Activate account
		@param user: User
		@param activationCode: Activation Code
		@return: resultDict"""
		signupData = self._dbUser.getSignupData(user)
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
		return resultDict
	def _getNetworkProfile(self, form, bFacebookLogin):
		"""Doc."""
		# Get facebook profile
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
		# Build in case only Facebook, Only LinkedIn or both		
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
		return form
	def doOrganization(self, form, captcha, bFacebookLogin, *argsTuple, **argsDict):
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
		return result
