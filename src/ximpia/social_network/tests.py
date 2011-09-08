from django.test import TestCase

import forms
import simplejson as json

from django.http import HttpRequest
from django.utils import translation

from django.contrib.auth.models import User as UserSys, Group as GroupSys

from models import UserX, GroupX, UserDetail, Professional, Organization, Profile, Context, Constants, Choices

from ximpia import settings

from ximpia.settings_visual import SocialNetworkIconData as SND
from ximpia.settings_visual import SuggestBox as SB
from ximpia.settings_visual import GenericComponent as GC

#from ximpia.human_resources.models import Professional, Profile
#from models import BsAccount

from business import Signup
from data import UserDAO, AccountDAO
from ximpia.social_network.data import GroupDAO

def buildRequest(myUserName='user1'):
	request = HttpRequest()	
	user = UserSys(username=myUserName, email='jorge.alegre@tecor.com', first_name='Jorge', last_name='Alegre')
	user.set_password('123456')
	user.save()
	request.user = user
	return request

def buildContext(request): 
	lang = translation.get_language()
	contextDict = {
			'request': request,
			'lang': lang,
			'settings': settings,
			}
	ctx = Context(request.user, lang, contextDict, {}, request.COOKIES, request.META)
	return ctx

class AccountDAOTest(TestCase):
	def setUp(self):
		self.request = buildRequest()
		self.ctx = buildContext(self.request)
		self.dbAccount = AccountDAO(self.ctx)
		self.dbUser = UserDAO(self.ctx)
	def testSignup(self):
		invitation = self.dbUser.invite(self.ctx.user, 'jorge.alegre@tecor.com', '', '', Constants.EMAIL, '', Choices.INVITATION_TYPE_ORDINARY)
		FormDict = {
			'ximpiaId': 'jalegre_test', 
			'email': 'jorge.alegre@zoho.com',
			'firstName': "Jorge",
			'lastName': 'Alegre',
			'password': '123456',
			'passwordVerify': '123456',
			'industry': ['102','103','104'],
			'city': 'Madrid',
			'country': 'es',
			'userGroups': ['1'],
			'invitationCode': invitation.invitationCode,
			'invitationByUser': invitation.fromUser.id,
			'twitterIcon_data': SND('twitter', 1).getS(),
			'facebookIcon_data': SND('facebook', 2).getS(),
			'linkedinIcon_data': SND('linkedin', 1).getS()
			}
		form = forms.FrmUserSignup(FormDict)
		check = form.isValid()
		self.assert_(check == True)
		# doSignup
		self.dbAccount.doSignup(form)
		# Test get
		user = UserSys.objects.get(username='jalegre_test')
		userDetail = UserDetail.objects.get(user=user)
		userX = UserX.objects.get(user=user, socialChannel=Constants.PROFESSIONAL)
		professional = Professional.objects.get(user=userDetail)
		profile = Profile.objects.get(professional=professional)
		self.assert_(user != None)
		self.assert_(userX != None)
		self.assert_(professional != None)
		self.assert_(profile != None)				
		self.assert_(userX.groups.filter(group__name='Users').exists() == True)
		self.assert_(Professional.objects.filter(user=userX).exists() == True)
		self.assert_(Profile.objects.filter(professional=professional).exists() == True)
		self.assert_(user.email == 'jorge.alegre@zoho.com')
		self.assert_(userDetail.hasValidatedEmail == False)
		self.assert_(user.check_password('123456') == True)
		self.assert_(professional.invitedByUser.id == invitation.fromUser.id)
	def testOrgSignup(self):
		invitation = self.dbUser.invite(self.ctx.user, 'jorge.alegre@tecor.com', '', '', Constants.EMAIL, '', Choices.INVITATION_TYPE_ORDINARY)
		FormDict = {
			'ximpiaId': 'jalegre_test', 
			'email': 'jorge.alegre@zoho.com',
			'firstName': "Jorge",
			'lastName': 'Alegre',
			'password': '123456',
			'passwordVerify': '123456',
			'organizationIndustry': ['102','103','104'],
			'city': 'Madrid',
			'country': 'es',
			'organizationName' : 'Tecor',
			'organizationDomain': 'tecor.com',
			'organizationCity': 'Madrid',
			'organizationCountry': 'es',
			'account': 'tecor',
			'accountType': invitation.type,
			'description': 'Descripcion de Tecor',
			'organizationGroup': 'Sales',
			'organizationGroupTags': '',
			'jobTitle': 'Project Manager',
			'userGroups': json.dumps(['1']),
			'invitationCode': invitation.invitationCode,
			'invitationByUser': invitation.fromUser.id,
			'twitterOrgIcon_data' : SND('twitter', 1).getS(),
			'twitterIcon_data': SND('twitter', 1).getS(),
			'facebookIcon_data': SND('facebook', 2).getS(),
			'linkedinIcon_data': SND('linkedin', 1).getS(),
			'linkedInProfile' : '',
			'orgGroupTags_data' : json.dumps([]),
			'orgGroup_data' : '',
			'jobTitle_data': SB(Choices.JOB_TITLES),
			'organizationGroup_data' : SB(Choices.ORG_GROUPS)
			}
		form = forms.FrmOrganizationSignup(FormDict)
		check = form.isValid()
		self.assert_(check == True)
		self.dbAccount.doOrganizationSignup(form)
		user = UserSys.objects.get(username='jalegre_test')
		userDetail = UserDetail.objects.get(user=user)
		userX = UserX.objects.get(user=user, socialChannel='tecor')
		organization = Organization.objects.get(account='tecor')
		professional = Professional.objects.get(user=userDetail)
		self.assert_(professional.invitedByUser.id == invitation.fromUser.id)
		self.assert_(organization.invitedByUser.id == invitation.fromUser.id)
		self.assert_(Organization.objects.filter(account='tecor').count() == 1)
		self.assert_(UserX.objects.filter(user=user).count() == 2)
		self.assert_(professional.professionalRelations.all()[0].organization.id == organization.id)

class UserDAOTest(TestCase):
	_SOCIAL_CHANNEL_PRO = 'professional'
	_USER_1 = 'user_test_1'
	_USER_2 = 'user_test_2'
	_USER_3 = 'user_test_3'
	_USER_MINE = 'user_1'

	def setUp(self):
		self.request = buildRequest()
		self.ctx = buildContext(self.request)
		self.dbUser = UserDAO(self.ctx)

	def _createXimpiaUser(self, userName, groupIdList=[1], bUser=True):
		if bUser == True:
			user = self.dbUser.createUser(userName, 'Jorge', 'Alegre', 'jorge.alegre@tecor.com', '123456', groupIdList)
		else:
			user = self.ctx.user
		userX = self.dbUser.createUserChannel(user, self._SOCIAL_CHANNEL_PRO, groupIdList)
		return userX

	def _deleteXimpiaUser(self, userX):
		userXDel = self.dbUser.deleteById(userX.id)
		userDel = self.dbUser.deleteUserById(userX.user.id)
		return userXDel

	def testCreateUser(self):
		user = self.dbUser.createUser('user_test_1', 'Jorge', 'Alegre', 'jorge.alegre@tecor.com', '123456', [1])
		self.assert_(user != None)
		self.assert_(user.first_name == 'Jorge')
		userDel = self.dbUser.deleteUserById(user.id)
		self.assert_(user.first_name == userDel.first_name)

	def testCreateUserX(self):
		userX = self._createXimpiaUser(self._USER_1, [1])
		self.assert_(userX != None)
		self.assert_(userX.socialChannel == self._SOCIAL_CHANNEL_PRO)
		userXDel = self._deleteXimpiaUser(userX)
		self.assert_(userXDel.id == userX.id)

	def testCheckSameMail(self):
		userX = self._createXimpiaUser(self._USER_1, [1]) 
		bTest = self.dbUser.checkSameEmail(userX.user.email)
		self.assert_(bTest == True)
		userXDel = self._deleteXimpiaUser(userX)
		self.assert_(userXDel.id == userX.id)

	def testGet(self):
		userX = self._createXimpiaUser(self._USER_1, [1])
		# Get by user object
		userX = self.dbUser.get(userX.user)
		self.assert_(userX != None and userX.user != None and userX.user.first_name == 'Jorge' and userX.groups.count() == 1)
		# Get by username
		userX = self.dbUser.get(None, userName=self._USER_1)
		self.assert_(userX != None and userX.user != None and userX.user.first_name == 'Jorge' and userX.groups.count() == 1)
		userXDel = self._deleteXimpiaUser(userX)
		self.assert_(userXDel.id == userX.id)

	def testGetByUserChannel(self):
		userX = self._createXimpiaUser(self._USER_1, [1])
		# Get by django user id
		userX = self.dbUser.getByUserId(userX.user.id, self._SOCIAL_CHANNEL_PRO)
		self.assert_(userX != None and userX.user != None and userX.user.first_name == 'Jorge' and userX.groups.count() == 1)
		userXDel = self._deleteXimpiaUser(userX)
		self.assert_(userXDel.id == userX.id)

	"""def testGetDetails(self):
		userX = self._createXimpiaUser(self._USER_1, [1])
		user = userX.user
		userDetail = self.dbUser.getDetails(user)
		self.assert_(userDetail != None and userDetail.user != None)
		userXDel = self._deleteXimpiaUser(userX)
		self.assert_(userXDel.id == userX.id)"""

	def testGetChannels(self):
		userX = self._createXimpiaUser(self._USER_1, [1])
		user = userX.user
		userList = self.dbUser.getChannels(user)
		self.assert_(len(userList) != 0)
		userXDel = self._deleteXimpiaUser(userX)
		self.assert_(userXDel.id == userX.id)

	def testGetChannelsByGroupList(self):
		userX = self._createXimpiaUser(self._USER_1, [1])
		user = userX.user
		userList = self.dbUser.getChannelsByGroupList(user.id, [1])
		self.assert_(len(userList) == 1)
		userXDel = self._deleteXimpiaUser(userX)
		self.assert_(userXDel.id == userX.id)

	def testGetMyGroupsByChannel(self):
		userX = self._createXimpiaUser(self._USER_1, [101])
		user = userX.user
		groupList = self.dbUser.getMyGroupsByChannel(user, self._SOCIAL_CHANNEL_PRO)
		self.assert_(len(groupList) == 1, groupList[0].id == 101)
		userXDel = self._deleteXimpiaUser(userX)
		self.assert_(userXDel.id == userX.id)

	"""def testGetGroupsByChannel(self):
		groupList = self.dbUser.getGroupsByChannel(user, socialChannel)"""

	"""def testGetOrgByChannel(self):
		organization = self.dbUser.getOrgByChannel(user, socialChannel)"""

	def testGetGroupsAllChannels(self):
		userX = self._createXimpiaUser(self._USER_1, [101])
		user = userX.user
		groupList = self.dbUser.getGroupsAllChannels(user)
		self.assert_(len(groupList) == 1)
		userXDel = self._deleteXimpiaUser(userX)
		self.assert_(userXDel.id == userX.id)

	"""def testSearch(self):
		userList = self.dbUser.search('Jorge')
		self.assert_(len(userList) != 0)"""

	def testCreateChannel(self):
		user = self.dbUser.createUser(self._USER_1, 'Jorge', 'Alegre', 'jorge.alegre@tecor.com', '123456', [101])
		userX = self.dbUser.createUserChannel(user, self._SOCIAL_CHANNEL_PRO, [101])
		self.assert_(userX != None and userX.user != None and userX.user.first_name == 'Jorge' and userX.groups.count() == 1)
		userXDel = self._deleteXimpiaUser(userX)
		self.assert_(userXDel.id == userX.id)

	def testGetNumberInvitationsLeft(self):
		userX = self._createXimpiaUser(self._USER_1, [101])
		user = userX.user
		invitations = self.dbUser.getNumberInvitationsLeft(user)
		self.assert_(invitations > 1)
		userXDel = self._deleteXimpiaUser(userX)
		self.assert_(userXDel.id == userX.id)

	def testInvite(self):
		userX = self._createXimpiaUser(self._USER_1, [101])
		user = userX.user
		invitationAdd = self.dbUser.invite(user, 'jorge.alegre@zoho.com', '', '', 'Email', '')
		self.assert_(invitationAdd != None and invitationAdd.status == Constants.PENDING)
		invitation = self.dbUser.getInvitation(invitationAdd.invitationCode)
		self.assert_(invitation != None and invitation.status == Constants.PENDING)
		invitation.status = Constants.USED
		invitation = self.dbUser.changeInvitationUsed(invitation)
		self.assert_(invitation != None and invitation.status == Constants.USED)
		userXDel = self._deleteXimpiaUser(userX)
		self.assert_(userXDel.id == userX.id)
	
	def testInvitePromotion(self):
		userX = self._createXimpiaUser(self._USER_1, [101])
		user = userX.user
		invitationAdd = self.dbUser.invite(user, 'jorge.alegre@zoho.com', '', '', 'Email', '', type = Choices.INVITATION_TYPE_PROMOTION)
		self.assert_(invitationAdd != None and invitationAdd.status == Constants.PENDING)
		self.assert_(invitationAdd != None and invitationAdd.type == Choices.INVITATION_TYPE_PROMOTION)
		userXDel = self._deleteXimpiaUser(userX)
		self.assert_(userXDel.id == userX.id)
	
	def testSignupData(self):
		userX = self._createXimpiaUser(self._USER_1, [101])
		user = userX.user
		postDict = {}
		invitation = self.dbUser.invite(user, 'jorge.alegre@zoho.com', '', '', 'Email', '', type = Choices.INVITATION_TYPE_PROMOTION)
		activationCode = 12345
		signupData = self.dbUser.writeSignupData(self._USER_1, activationCode, invitation, postDict)
		self.assert_(signupData != '')
		signupData = self.dbUser.getSignupData(self._USER_1)
		self.assert_(signupData != '')
		userXDel = self._deleteXimpiaUser(userX)
		self.assert_(userXDel.id == userX.id)

	def testGetMap(self):
		userX_1 = self._createXimpiaUser(self._USER_1, [101])
		userX_2 = self._createXimpiaUser(self._USER_2, [101])
		userX_3 = self._createXimpiaUser(self._USER_3, [101])
		idList = [1,2,3]
		# get map simple
		dict = self.dbUser.getMap(idList)
		self.assert_(dict.has_key(1) and dict[1].user.first_name == 'Jorge')
		# get map will all links
		dict = self.dbUser.getMap(idList, bFull=True)
		userXDel_1 = self._deleteXimpiaUser(userX_1)
		userXDel_2 = self._deleteXimpiaUser(userX_2)
		userXDel_3 = self._deleteXimpiaUser(userX_3)
		self.assert_(userXDel_1.id == userX_1.id)
		self.assert_(userXDel_2.id == userX_2.id)
		self.assert_(userXDel_3.id == userX_3.id)

	def testGetById(self):
		userXAdd = self._createXimpiaUser(self._USER_1, [101])
		userX = self.dbUser.getById(userXAdd.id)
		self.assert_(userX != None and userX.id == userXAdd.id)
		userX = self.dbUser.getById(userXAdd.id, bFull=True)
		self.assert_(userX != None and userX.id == userXAdd.id)
		userXDel = self._deleteXimpiaUser(userXAdd)
		self.assert_(userXDel.id == userXAdd.id)

	def testDeleteById(self):
		userXAdd = self._createXimpiaUser(self._USER_1, [101])
		userXDel = self.dbUser.deleteById(userXAdd.id)
		self.assert_(userXDel.id == userXAdd.id)

	def testFilter(self):
		userX = self._createXimpiaUser(self._USER_1, [101])
		list = self.dbUser.filter(socialChannel='professional')
		self.assert_(len(list) != 0)
		list = self.dbUser.filter(socialChannel='professional', bFull=True)
		self.assert_(len(list) != 0)
		userXDel = self._deleteXimpiaUser(userX)
		self.assert_(userXDel.id == userX.id)

	def testGetAll(self):
		userX = self._createXimpiaUser(self._USER_1, [101])
		list = self.dbUser.getAll()
		self.assert_(len(list) != 0)
		list = self.dbUser.getAll(bFull=True)
		self.assert_(len(list) != 0)
		userXDel = self._deleteXimpiaUser(userX)
		self.assert_(userXDel.id == userX.id)

class GroupDAOTest(TestCase):
	_SOCIAL_CHANNEL_PRO = 'professional'
	_USER_1 = 'user_test_1'
	_USER_2 = 'user_test_2'
	_USER_3 = 'user_test_3'
	_USER_MINE = 'user_1'

	def setUp(self):
		self.request = buildRequest()
		self.ctx = buildContext(self.request)
		self.dbGroup = GroupDAO(self.ctx)
	
	def _getForm(self):
		form = None
		return form
