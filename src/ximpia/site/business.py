import random
import forms
import simplejson as json
import data
from datetime import date, timedelta

from ximpia.core.models import ContextDecorator as Ctx
from ximpia.core.business import CommonBusiness, EmailBusiness
from ximpia.core.business import ValidateFormDecorator, WFActionDecorator, DoBusinessDecorator, WFViewDecorator, MenuActionDecorator,\
	ValidationDecorator
from ximpia import settings

from data import GroupChannelDAO, InvitationDAO, OrganizationDAO, ParamDAO, UserChannelDAO, XmlMessageDAO, UserDAO, GroupDAO, UserDetailDAO
from forms import UserSignupInvitationForm #@UnusedImport
import constants as K

class VideoBusiness ( CommonBusiness ):
	
	def __init__(self, ctx):
		super(VideoBusiness, self).__init__(ctx)
		self._dbVideo = data.VideoDAO(ctx)
	
	@DoBusinessDecorator(form = forms.HomeForm, pageError=True, isServerTmpl=True)
	def showHome(self):
		"""Show videos in the home view"""
		self._addList('featuredVideos', self._dbVideo.searchFields( 	['embedCode', 'name', 'title', 'description', 'isFeatured'], 
										isFeatured=True  ) )
		self._addList('videos', self._dbVideo.searchFields( 	['embedCode', 'name', 'title', 'description', 'isFeatured'], 
									isFeatured=False  ) )

#######################################################################################

class LoginBusiness ( CommonBusiness ):
	
	def __init__(self, ctx):
		super(LoginBusiness, self).__init__(ctx)
		#self._dbUserAccount = UserAccountDAO(ctx)
		self._dbUserSys = UserDAO(ctx)
		self._dbXmlMessage = XmlMessageDAO(ctx)
		#self._dbUserDetail = UserDetailDAO(ctx)
		#self._dbUserSocial = UserSocialDAO(ctx)
		self._dbParam = ParamDAO(ctx)	
	
	@WFViewDecorator('login')
	@DoBusinessDecorator(pageError=True)
	def showLogin(self):
		"""Checks if user is logged in. If true, get login user information in the context
		@param ctx: Context
		@return: result"""
		# Check if login:
		print 'login...'
		if not self._ctx['user'].is_authenticated():
			# no login: login form
			self._setMainForm(forms.LoginForm())
			self._ctx[Ctx.JS_DATA].addAttr('isLogin', False)
			# Popup - Password reminder
			self._addForm(forms.PasswordReminderForm())

	@DoBusinessDecorator(pageError=True)
	def showLogout(self):
		"""Show logout view"""
		self._ctx[Ctx.JS_DATA].addAttr('isLogin', False)
	
	@ValidationDecorator()
	def _validateReminder(self, ximpiaId, reminderId):
		days = self._dbParam.get(mode=K.PARAM_LOGIN, name=K.PARAM_REMINDER_DAYS).valueId
		newDate = date.today() + timedelta(days=days)
		print 'New Password Data : ', ximpiaId, newDate, reminderId
		# Show actual password, new password and confirm new password
		self._validateExists([
					[self._dbUserSys, {'username': ximpiaId}, 'changePassword'],
					[self._dbUserDetail, {	'user__username': ximpiaId, 
								'reminderId': reminderId, 
								'resetPasswordDate__lte' : newDate}, 'changePassword'],
					])

	@DoBusinessDecorator(form = forms.ChangePasswordForm, isServerTmpl=True)
	def showNewPassword(self, ximpiaId=None, reminderId=None):
		"""Shows form to enter new password and confirm new password. Save button will call doNewPassword.
		@param ximpiaId: ximpiaId
		@param reminderId: reminderId"""
		self._validateReminder(ximpiaId, reminderId)
		self._f().putParamList(ximpiaId=ximpiaId)
	
	@ValidationDecorator()
	def _authenUser(self):
		self._ctx[Ctx.USER] = self._authenticateUser(	userName = self._f()['ximpiaId'], 
						password = self._f()['password'], 
						errorName = 'wrongPassword'	)
	
	@ValidateFormDecorator(forms.LoginForm)
	@WFActionDecorator()
	def doLogin(self):
		"""Performs the login action
		@param ctx: Context
		@return: result"""
		print 'doLogin...'
		print 'form: ', self._ctx[Ctx.FORM], self._f()['ximpiaId']
		self._authenUser()
		print 'user: ', self._ctx[Ctx.USER]
		self._login()
		self._putFlowParams(ximpiaId=self._ctx[Ctx.USER].username.encode(settings.DEFAULT_CHARSET))		
		print 'Session: ', self._ctx[Ctx.SESSION]
		print 'user: ', self._ctx[Ctx.USER]
		print 'cookies: ', self._ctx[Ctx.COOKIES]
		userChannelName = self._getUserChannelName()
		print 'userChannelName: ', userChannelName
		self._ctx[Ctx.USER_CHANNEL] = self._dbUserSocial.get(user=self._ctx[Ctx.USER], name=userChannelName)
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
		
	@ValidationDecorator()
	def _validateEmailExist(self):
		self._validateExists([
					[self._dbUserSys, {'email': self._f()['email']}, 'emailDoesNotExist']
				])
	
	@ValidateFormDecorator(forms.PasswordReminderForm)
	@DoBusinessDecorator(pageError=True)
	def doPasswordReminder(self):
		"""Checks that email exists, then send email to user with reset link"""
		self._validateEmailExist()
		# Update User
		user = self._dbUserSys.get(email = self._f()['email'])
		userDetail = self._dbUserDetail.get(user=user) 
		days = self._dbParam.get(mode=K.PARAM_LOGIN, name=K.PARAM_REMINDER_DAYS).valueId
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


class HomeBusiness ( CommonBusiness ):
	
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
		self._dbUserSys = UserDAO(ctx)
	
	@ValidationDecorator()
	def _validateUser(self):
		"""Validate user: Check user password"""
		self._ctx[Ctx.USER] = self._authenticateUser(	userName = self._ctx[Ctx.USER], 
								password = self._f()['password'], 
								errorName = 'passwordValidate'	)
	
	@DoBusinessDecorator(form = forms.UserChangePasswordForm, pageError=True)
	def showChangePassword(self):
		"""Change password form with current password and new password"""
		pass
	
	@ValidateFormDecorator(forms.UserChangePasswordForm)
	@DoBusinessDecorator(pageError=True)
	def doChangePassword(self):
		"""Change password from user area"""
		self._validateUser()
		user = self._dbUserSys.get(username= self._ctx[Ctx.USER])
		user.set_password(self._f()['newPassword'])
		user.save()

class SignupBusiness ( CommonBusiness ):

	def __init__(self, ctx):
		super(SignupBusiness, self).__init__(ctx)
		self._dbInvitation = InvitationDAO(ctx)
		self._dbUser = UserDAO(ctx)
		self._dbUserDetail = UserDetailDAO(ctx)
		self._dbOrganization = OrganizationDAO(ctx)
		self._dbInvitation = InvitationDAO(ctx)
		self._dbGroup = GroupDAO(ctx)
		self._dbUserChannel = UserChannelDAO(ctx)
		self._dbGroupChannel = GroupChannelDAO(ctx)
		self._dbUser = UserDAO(ctx)
	
	@ValidationDecorator()
	def _validateInvUserSignup(self):
		self._validateNotExists([
				[self._dbUser, {'username': self._f()['ximpiaId']}, 'ximpiaId'],
				[self._dbUser, {'email': self._f()['email']}, 'email']
				])
		self._validateExists([
				[self._dbInvitation, {'invitationCode': self._f()['invitationCode']}, 'invitationCode']
				])
	
	@ValidationDecorator()
	def _validateInvitation(self, invitationCode):
		self._validateNotExists([
				[self._dbInvitation, {'invitationCode': invitationCode, 'status': K.USED}, 'invitationUsed']
				])
	
	@DoBusinessDecorator(pageError=True, form=forms.UserSignupInvitationForm, isServerTmpl=True)
	def showSignupUserInvitation(self, invitationCode=None, affiliateId=None):
		"""Show signup form. Get get invitation code."""
		print 'invitationCode: ', invitationCode
		print 'affiliateId: ', affiliateId
		# Business Validation 
		self._validateInvitation(invitationCode)
		# Business
		invitation = self._dbUser.getInvitation(invitationCode, status=K.PENDING)
		self._ctx['affiliateid'] = json.dumps(affiliateId)
		self._setMainForm(forms.UserSignupInvitationForm(instances = {'dbInvitation': invitation}))
	
	@ValidateFormDecorator(forms.UserSignupInvitationForm)
	@DoBusinessDecorator()
	def doUser(self):
		"""Signup professional user
		@param ctx: Context"""
		# Business Validation
		self._validateInvUserSignup()
		# Invitation
		invitation = self._dbInvitation.get(invitationCode=self._f()['invitationCode'])
		# System User
		user = self._dbUser.create(username=self._f()['ximpiaId'], email=self._f()['email'], 
						first_name=self._f()['firstName'], last_name=self._f()['lastName'])
		user.set_password(self._f()['password'])
		user.save()
		# Ximpia User
		userChannel = self._dbUserChannel.create(user=user, name=K.USER, title=self._f()['firstName'], userCreateId=user.id)
		userDetail = self._dbUserDetail.create(user=user, name=self._f()['firstName'] + ' ' + self._f()['lastName'], #@UnusedVariable
						hasValidatedEmail=True)
		# Groups
		userGroupId = json.loads(self._f()['params'])['userGroup']
		group = self._dbGroup.get(id=userGroupId)
		user.groups.add(group)
		userChannel.groups.add(group)
		# Modify Invitation
		invitation.status = K.USED
		invitation.save()
