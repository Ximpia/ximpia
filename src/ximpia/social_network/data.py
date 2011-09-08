import random
import simplejson as json
import base64
import cPickle
import traceback

from django.db.models import Q
from django.contrib.auth.models import User as UserSys, Group as GroupSys

from django.utils.translation import ugettext as _
from ximpia import util

from models import Constants, getFormDataValue, getPagingStartEnd, getDataDict, XpMsgException, parseLinks, parseText, Choices
from models import UserSocial, SocialNetwork, UserParam, SocialNetworkUserSocial, GroupSocial, UserDetail, UserProfile, Industry, UserAccount
from models import Organization, OrganizationGroup, AddressOrganization, Tag, SocialNetworkOrganization, UserAccountContract
from models import UserAccountRelation, Application, Subscription, Invitation, SignupData, GroupFollow, GroupStream, StatusMessage
from models import Comment, TagUserTotal, LinkUserTotal, Link, Like, Notification, Skill, SkillGroup, SkillUserAccount, Affiliate, Version
from models import AddressContact, CommunicationTypeContact, ContactDetail, Contact, File, FileVersion, TagType
from models import Calendar, CalendarInvite, MasterValue, XpMsgException, Address
import sys

from ximpia.settings_visual import SocialNetworkIconData as SND
from ximpia.settings_visual import GenericComponent

from constants import DbType

class CommonDAO(object):	

	NUMBER_MATCHES = 100
	_ctx = None
	_model = None
	_argsTuple = ()
	_argsDict = {}

	def __init__(self, ctx, *ArgsTuple, **ArgsDict):
		self._ctx = ctx
		self._argsTuple = ArgsTuple
		self._argsDict = ArgsDict
		
	def _cleanDict(self, dict):
		"""Clean dict removing xpXXX fields.
		@param dict: Dictionary
		@return: dictNew : New dictionary without xpXXX fields"""
		list = dict.keys()
		dictNew = {}
		for sKey in list:
			if sKey.find('xp') == 0:
				pass
			else:
				dictNew[sKey] = dict[sKey]
		return dictNew
	
	def _getPagingStartEnd(self, page, numberMatches):
		"""Get tuple (iStart, iEnd)"""
		iStart = (page-1)*numberMatches
		iEnd = iStart+numberMatches
		tuple = (iStart, iEnd)
		return tuple
	
	def getMap(self, idList, bFull=False, useModel=None):
		"""Get object map for a list of ids 
		@param idList: 
		@param bFull: boolean : Follows all foreign keys
		@return: Dict[id]: object"""
		dict = {}
		if len(idList) != 0:
			if useModel != None:
				dbObj = self.useModel.objects
			else:
				dbObj = self._model.objects
			if bFull == True:
				dbObj = dbObj.select_related()
			list = dbObj.filter(id__in=idList)
			for object in list:
				dict[object.id] = object
		return dict
	
	def getById(self, id, bFull=False):
		"""Get model object by id
		@param id: Object id
		@param bFull: boolean : Follows all foreign keys
		@return: Model object"""
		try:
			dbObj = self._model.objects
			if bFull == True:
				dbObj = self._model.objects.select_related()
			object = dbObj.get(id=id)
		except Exception as e:
			raise XpMsgException(e, _('Error in get object by id ') + str(id) + _(' in model ') + str(self._model))
		return object	
	
	def deleteById(self, id):
		"""Delete model object by id
		@param id: Object id
		@return: Model object"""
		try:
			list = self._model.objects.filter(id=id)
			object = list[0]
			list.delete()
		except Exception as e:
			raise XpMsgException(e, _('Error delete object by id ') + str(id))
		return object
	
	def filter(self, bFull=False, **ArgsDict):
		"""Search a model table with ordering support and paging
		@param bFull: boolean : Follows all foreign keys
		@return: list : List of model objects"""
		try:
			iNumberMatches = self.NUMBER_MATCHES
			if ArgsDict.has_key('xpNumberMatches'):
				iNumberMatches = ArgsDict['xpNumberMatches']
			page = 1
			if ArgsDict.has_key('xpPage'):
				page = int(ArgsDict['xpPage'])
			iStart, iEnd = self._getPagingStartEnd(page, iNumberMatches)
			orderByTuple = ()
			if ArgsDict.has_key('xpOrderBy'):
				orderByTuple = ArgsDict['xpOrderBy']
			ArgsDict = self._cleanDict(ArgsDict)
			dbObj = self._model.objects
			if bFull == True:
				dbObj = self._model.objects.select_related()
			if len(orderByTuple) != 0:
				dbObj = self._model.objects.order_by(*orderByTuple)
			list = dbObj.filter(**ArgsDict)[iStart:iEnd]			
		except Exception as e:
			raise XpMsgException(e, _('Error in search table model ') + str(self._model))
		return list	
		
	def getAll(self, bFull=False):
		"""Get all rows from table
		@param bFull: boolean : Follows all foreign keys
		@return: list"""
		try:
			dbObj = self._model.objects
			if bFull == True:
				dbObj = self._model.objects.select_related()
			list = dbObj.all()
		except Exception as e:
			raise XpMsgException(e, _('Error in getting all fields from ') + str(self._model))
		return list
	
	def _getCtx(self):
		"""Get context"""
		return self._ctx

	def _doManyById(self, model, idList, field):
		"""Does request for map for list of ids (one query). Then processes map and adds to object obtained objects.
		@param idList: List
		@param object: Model"""
		dict = self.getMap(idList, userModel=model)
		for idTarget in dict.keys():
			addModel = dict[idTarget]
			field.add(addModel)
	
	def _doManyByName(self, model, nameList, field):
		"""Does request for map for list of ids (one query). Then processes map and adds to object obtained objects.
		@param idList: List
		@param object: Model"""
		for value in nameList:
			nameModel, bCreate = model.objects.get_or_create(name=value)
			field.add(nameModel)

	ctx = property(_getCtx, None)

class AccountDAO(CommonDAO):
	
	_ctx = None
	
	def __init__(self, ctx, *ArgsTuple, **ArgsDict):
		super(AccountDAO, self).__init__(ctx, *ArgsTuple, **ArgsDict)
	
	def linkUserSocialNetworks(self, userDetail, twitterDict, facebookDict, linkedinDict):
		"""Doc."""
		user = userDetail.user
		typeTwitter = UserParam.objects.get(mode='net', name=Constants.TWITTER)
		typeFacebook = UserParam.objects.get(mode='net', name=Constants.FACEBOOK)
		typeLinkedIn = UserParam.objects.get(mode='net', name=Constants.LINKEDIN)
		netTwitter = SocialNetwork.objects.get(type=typeTwitter)
		netFacebook = SocialNetwork.objects.get(type=typeFacebook)
		netLinkedIn = SocialNetwork.objects.get(type=typeLinkedIn)
		tupleSocialNets = (netTwitter, netFacebook, netLinkedIn)
		for socialNet in tupleSocialNets:
			if socialNet.getName() == Constants.TWITTER and twitterDict['token'] != '':
				userDetail.TwitterAuth = True
				netUser = SocialNetworkUserSocial(user=userDetail, socialNetwork=socialNet)
				netUser.token = twitterDict['token']
				netUser.tokenSecret = twitterDict['tokenSecret']
				netUser.userCreateId = user.pk
				netUser.save()
			elif socialNet.getName() == Constants.FACEBOOK and facebookDict['token'] != '':
				userDetail.FacebookAuth = True
				netUser = SocialNetworkUserSocial(user=userDetail, socialNetwork=socialNet)
				netUser.token = facebookDict['token']
				netUser.tokenSecret = facebookDict['tokenSecret']
				netUser.userCreateId = user.pk
				netUser.save()
			elif socialNet.getName() == Constants.LINKEDIN and linkedinDict['token'] != '':
				userDetail.LinkedInAuth = True
				netUser = SocialNetworkUserSocial(user=userDetail, socialNetwork=socialNet)
				netUser.token = linkedinDict['token']
				netUser.tokenSecret = linkedinDict['tokenSecret']
				netUser.userCreateId = user.pk
				netUser.save()
		userDetail.save()
		
	def addGroupsToUser(self, form, groupIdList):
		"""Doc."""
		ximpiaId = getDataDict(form)['ximpiaId']
		user = UserSys.objects.get(username=ximpiaId)
		userList = UserSocial.objects.filter(user=user)
		for groupId in groupIdList:
			group = GroupSys.objects.get(id=groupId)
			user.groups.add(group)
			groupSocial = GroupSocial.objects.get(group__id=groupId)
			for userSocial in userList:
				userSocial.groups.add(groupSocial)

	def _createUser(self, ximpiaId, email, firstName, lastName, password):
		"""Creates Django user, sets first name, last name, email and password"""
		try:
			user = UserSys.objects.get(username=ximpiaId)
		except UserSys.DoesNotExist:
			user = UserSys(username=ximpiaId, email=email, first_name=firstName, last_name=lastName)
			user.set_password(password)
			user.save()
		return user

	def _createXimpiaUser(self, user, firstName, lastName, auth, profiles):
		"""Doc."""
		try:
			userX = UserDAO(self._ctx).get(user, socialChannel=Constants.PROFESSIONAL)
			userDetail = UserDetail.objects.get(user=user)
		except UserSocial.DoesNotExist:
			name = firstName + ' ' + lastName
			userX = UserDAO(self._ctx).createUserChannel(user, Constants.PROFESSIONAL)
			userDetail = UserDetail.objects.create(user=user, name=name, auth=auth, netProfiles=profiles)
		tuple = (userX, userDetail)
		return tuple

	def _createAuthProfiles(self, profiles, facebookIcon_data, twitterIcon_data, linkedinIcon_data):
		"""Creates the dictionaries for auth and profiles for all social networks.
		@param profiles: json string with profiles for facebook and linkedin
		@param facebookIcon_data: json data for facebook
		@param twitterIcon_data: json data for twitter: 
		@param linkedinIcon_data: json data for Linkedin
		@return: (authDict, profileDict)"""
		# Processing auth and profiles...
		profileDict = {Constants.FACEBOOK: {}, Constants.LINKEDIN: {}}
		if profiles != '':
			profileDict = json.loads(profiles)		
		# Processing icon data
		twitterDataDict = SND(jsonData=twitterIcon_data).getData()
		facebookDataDict = SND(jsonData=facebookIcon_data).getData()
		linkedinDataDict = SND(jsonData=linkedinIcon_data).getData()
		auth = {Constants.FACEBOOK: facebookDataDict, Constants.TWITTER: twitterDataDict, Constants.LINKEDIN: linkedinDataDict}		
		tuple = (auth, profileDict, facebookDataDict, twitterDataDict, linkedinDataDict)
		return tuple

	def doSignup(self, invitedByUser=None, invitedByOrg=None):
		"""Doc."""
		# Get data from form
		f = self._ctx['form']
		ximpiaId = getDataDict(f)['ximpiaId']
		email = getDataDict(f)['email']
		firstName = getDataDict(f)['firstName']
		lastName = getDataDict(f)['lastName']
		password = getDataDict(f)['password']
		#industryList = getDataDict(f)['industry']
		city = getDataDict(f)['city']
		country = getDataDict(f)['country']		
		twitterIcon_data = getDataDict(f)['twitterIcon_data']
		facebookIcon_data = getDataDict(f)['facebookIcon_data']
		linkedinIcon_data = getDataDict(f)['linkedinIcon_data']
		# fields data
		fields = json.loads(getDataDict(f)['fields'])		
		userGroupList = fields['userGroups']
		profiles = fields['profiles']
		affiliateId = fields['affiliateId']
		invitationCode = getDataDict(f)['invitationCode']
		
		# Invitation Data
		invitation = Invitation.objects.get(invitationCode=invitationCode)
		invitedByUserId = invitation.fromUser.pk
		invitedByOrgAcc = invitation.fromAccount  
		
		# Get profile dict and auth dict for all social networks
		
		socialNetworkTuple = self._createAuthProfiles(profiles, facebookIcon_data, twitterIcon_data, linkedinIcon_data)
		authDict, profileDict, facebookDataDict, twitterDataDict, linkedinDataDict = socialNetworkTuple
		sAuth = json.dumps(authDict)
		profiles = json.dumps(profileDict)
		# Build Id Lists
		listTools = util.basic_types.ListType()
		#industryIdList = listTools.buildIdList(industryList)
		#groupTmpList = listTools.mixLists(industryList, userGroupList)
		#groupList = listTools.buildIdList(groupTmpList)
		groupList = listTools.buildIdList(userGroupList)
		# Django User
		user = self._createUser(ximpiaId, email, firstName, lastName, password)
		# Ximpia User, tokens and profiles
		userSocial, userDetail = self._createXimpiaUser(user, firstName, lastName, sAuth, profiles)
		# Add groups to user
		self.addGroupsToUser(f, groupList)
		# Social Networks Linked
		if twitterDataDict['token'] != '' or facebookDataDict['token'] != '' or linkedinDataDict['token'] != '':
			self.linkUserSocialNetworks(userDetail, twitterDataDict, facebookDataDict, linkedinDataDict)
		# Affiliate
		affiliate = None
		if affiliateId != -1:
			affiliate = AffiliateDAO(self._ctx).get(affiliateId)
		# User Directory
		contactDetail = ContactDAO(self._ctx).createDirectoryUser(user, firstName, lastName, email, city, country, 
									userSocial, None, Constants.PROFESSIONAL)
		# InvitedBy
		invitedByUser = None
		invitedByOrg = None
		if invitedByUserId:
			invitedByUser = UserSys.objects.get(pk=invitedByUserId)
		if invitedByOrgAcc:
			invitedByOrg = OrganizationDAO(self._ctx).getByAccount(invitedByOrgAcc)
		# UserAccount
		userAccount = UserAccount.objects.create(	user=userDetail,
								invitedByUser = invitedByUser,
								invitedByOrg = invitedByOrg,
								affiliate = affiliate,
								contact = contactDetail, 
								userCreateId = user.pk)
		# Profile		
		ProfileDAO(self._ctx).writeFromNetworks(userAccount.id, profileDict)

	def getSocialNetwork(self, socialNet):
		"""Doc."""
		typeNet = UserParam.objects.get(mode='net', name=socialNet)
		socialNet = SocialNetwork.objects.get(type=typeNet)
		return socialNet

	def doOrganizationSignup(self, form):
		"""Doc."""
		# Get data from form
		d = getDataDict(form)
		dbGroup = GroupDAO(self._ctx)
		organizationGroupTagList = GenericComponent(obj=d['groupTags_data']).filter('text')
		userGroupList = json.loads(d['userGroups'])
		# Build Id Lists
		industryList = d['organizationIndustry']
		listTools = util.basic_types.ListType()
		industryIdList = listTools.buildIdList(industryList)
		groupTmpList = listTools.mixLists(industryList, userGroupList)
		groupList = listTools.buildIdList(groupTmpList)
		industryList = []
		if len(industryIdList) != 0:
			industryList = Industry.objects.in_bulk(industryIdList)
		# Social		
		socialNetworkTuple = self._createAuthProfiles(d['profiles'], d['facebookIcon_data'], d['twitterIcon_data'], d['linkedinIcon_data'])
		authDict, profileDict, facebookDataDict, twitterDataDict, linkedinDataDict = socialNetworkTuple
		twitterOrgDataDict = SND(jsonData=d['twitterOrgIcon_data']).getData()
		sAuth = json.dumps(authDict)
		profiles = json.dumps(profileDict)
		# Django User
		user = self._createUser(d['ximpiaId'], d['email'], d['firstName'], d['lastName'], d['password'])
		# Ximpia User
		professionalUserSocial, userDetail = self._createXimpiaUser(user, d['firstName'], d['lastName'], sAuth, profiles)
		userX = UserDAO(self._ctx).createUserChannel(user, d['account'])
		self.addGroupsToUser(form, groupList)
		# Social Networks Linked
		if twitterDataDict['token'] != '' or facebookDataDict['token'] != '' or linkedinDataDict['token'] != '':
			self.linkUserSocialNetworks(userDetail, twitterDataDict, facebookDataDict, linkedinDataDict)
		# Affiliate
		affiliate = None
		if d['affiliateId'] != '':
			affiliate = AffiliateDAO(self._ctx).get(int(d['affiliateId']))
		# InvitedBy
		invitedByUser = None
		invitedByOrg = None
		if len(d['invitationByUser']) > 0:
			invitedByUser = UserSys.objects.get(id=int(d['invitationByUser']))
		if len(d['invitationByOrg']) > 0:
			invitedByOrg = OrganizationDAO(self._ctx).getByAccount(d['invitationByOrg'])
		# Organization
		organization = Organization.objects.create(
							account=d['account'],
							accountType = d['accountType'], 
							name=d['organizationName'], 
							domain=d['organizationDomain'], 
							description=d['description'], 
							filesQuota = Constants.FILE_QUOTA_DEFAULT, 
							invitedByUser = invitedByUser,
							invitedByOrg = invitedByOrg,
							affiliate = affiliate)
		# Organization Industries
		for industry in industryList:
			organization.industries.add(industry)
		# OrganizationGroup & Groups
		organizationGroup = d['account'] + '-' + d['organizationGroup']
		orgGroup, bGroupCreate = GroupSys.objects.get_or_create(name=organizationGroup)
		orgGroupSocial, bGroupSocialCreate = GroupSocial.objects.get_or_create(group=orgGroup, isPublic=False, isOrgGroup=True)
		organizationGroup = OrganizationGroup.objects.create(group=orgGroupSocial, organization=organization)
		# OrganizationGroup Tags
		tagType, isCreated = TagType.objects.get_or_create(type='default')
		for organizationGroupTag in organizationGroupTagList:
			tag, isCreated = Tag.objects.get_or_create(name=organizationGroupTag, type=tagType)
			orgGroupSocial.tags.add(tag)
		# Industries
		for industry in industryList:
			organization.industries.add(industry)
		# Address
		addressOrg = AddressOrganization.objects.create(
							addressType=Choices.ADDRESS_TYPE_BILL, 
							organization=organization, 
							city=d['organizationCity'], 
							country=d['organizationCountry'])
		# Social Networks
		netTwitter = self.getSocialNetwork(Constants.TWITTER)
		if twitterOrgDataDict['token'] != '':
			socialNetworkOrganization = SocialNetworkOrganization.objects.create(
							organization=organization, 
							socialNetwork=netTwitter, 
							token=twitterOrgDataDict['token'], 
							tokenSecret=twitterOrgDataDict['tokenSecret'])
			organization.socialNetworks.add(socialNetworkOrganization)
		# User Directory
		contactDetail = ContactDAO(self._ctx).createDirectoryUser(user, d['firstName'], d['lastName'], d['email'], d['city'], 
										d['country'], professionalUserSocial, userX, d['account'], bOrg=True)
		# UserAccount
		try:
			professional = UserAccount.objects.get(user=userDetail)
		except UserAccount.DoesNotExist:
			professional = UserAccount.objects.create(
							user=userDetail, 
							userCreateId = user.id,
							invitedByUser = invitedByUser,
							invitedByOrg = invitedByOrg,
							contact = contactDetail,
							affiliate = affiliate,
							linkedInProfile = d['linkedInProfile'])
			for industry in industryList:
				professional.Industries.add(industry)		
		# Relation User to Organization
		contract, bCreate = UserAccountContract.objects.get_or_create(
										status=Choices.STATUS_EMPLOYEE, 
										schedule=Choices.SCHEDULE_FULL, 
										contractType=Choices.CONTRACT_TYPE_REGULAR, 
										jobTitle=d['jobTitle'])
		professionalRelation = UserAccountRelation.objects.create(
									organization=organization, 
									organizationGroup=organizationGroup, 
									contract=contract)
		professional.professionalRelations.add(professionalRelation)		
		# User Profile
		ProfileDAO(self._ctx).writeFromNetworks(professional.id, profileDict)

	def doOrganizationUserSignup(self, form):
		"""Doc."""
		ximpiaId = getDataDict(form)['ximpiaId']
		email = getDataDict(form)['email']
		firstName = getDataDict(form)['firstName']
		lastName = getDataDict(form)['lastName']
		password = getDataDict(form)['password']
		city = getDataDict(form)['city']
		country = getDataDict(form)['country']
		twitter = getDataDict(form)['twitter']
		twitterPass = getDataDict(form)['twitterPass']
		facebook = getDataDict(form)['facebook']
		facebookPass = getDataDict(form)['facebookPass']
		linkedIn = getDataDict(form)['linkedIn']
		linkedInPass = getDataDict(form)['linkedInPass']
		userGroupList = eval(getDataDict(form)['userGroups'])
		jobTitle = getDataDict(form)['jobTitle']
		account = getDataDict(form)['account']
		jobStatus = getDataDict(form)['jobStatus']
		jobContractType = getDataDict(form)['jobContractType']
		jobSchedule = getDataDict(form)['jobSchedule']
		organizationDescription = getDataDict(form)['organizationDescription']
		organizationGroup = getDataDict(form)['organizationGroup']
		organizationName = getDataDict(form)['organizationName']
		organizationDomain = getDataDict(form)['organizationDomain']
		# Build Id Lists
		listTools = util.basic_types.ListType()
		groupList = listTools.buildIdList(userGroupList)
		#professionalRelationList
		# Django User
		user = UserSys(username=ximpiaId, email=email, first_name=firstName, last_name=lastName)
		user.set_password(password)
		user.save()
		# Ximpia User
		userX = UserSocial.objects.create(user=user, city=city, country=country, userCreateId = user.pk)
		# Organization user should be allowed to follow industries streams by default????
		self.addGroupsToUser(form, groupList)
		# Social Networks Linked
		if twitter != '' or facebook != '' or linkedIn != '':
			self.linkUserSocialNetworks(form, userX)
		# UserAccount
		professional = UserAccount.objects.create(user=userX, userCreateId = user.pk)
		# Relation User to Organization
		# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
		
		# Organization
		organization = Organization.objects.create(
							account=account, 
							name=organizationName, 
							domain=organizationDomain, 
							description=organizationDescription, 
							filesQuota = Constants.FILE_QUOTA_DEFAULT)
		# OrganizationGroup & Groups
		orgGroup, bCreate = GroupSys.objects.get_or_create(name=organizationGroup)
		orgGroupSocial, bCreate = GroupSocial.objects.get_or_create(group=orgGroup, public=False, orgGroup=True)
		organizationGroup = OrganizationGroup.objects.create(group=orgGroupSocial, organization=organization)
		
		professionalRelationList = []
		for professionalRelationTuple in professionalRelationList:
			jobStatus, jobSchedule, jobContractType, subcontractOrgName = professionalRelationTuple
			contract, bCreate = UserAccountContract.objects.get_or_create(
										status=jobStatus, 
										schedule=jobSchedule, 
										contractType=jobContractType, 
										jobTitle=jobTitle)
			if subcontractOrgName != '':				
				try:
					subcontractOrg = Organization.objects.get(name=subcontractOrgName)
				except Organization.DoesNotExist:
					subcontractOrg = None
				except Organization.MultipleObjectsReturned:
					subcontractOrg = None
			professionalRelation = UserAccountRelation.objects.create(
									organization=organization, 
									organizationGroup=organizationGroup, 
									professionalContract=contract,
									subcontractOrganization=subcontractOrg)
			professional.UserAccountRelations.add(professionalRelation)
		# User Profile
		profile = UserProfile.objects.create(professional=professional, userCreateId = user.pk)

	def subscriptionOrganization(self, form):
		"""Sign up subscription for organization and all users signed up"""
		# Change status to valid organization
		organization = OrganizationDAO(self._ctx).getByAccount(getDataDict(form)['account'])
		organization.subscriptionStatus = Choices.SUBSCRIPTION_VALID
		organization.save()
		# Change subscription to valid for all users
		application = Application.objects.get(name=Constants.SOCIAL_NETWORK)
		list = Subscription.objects.filter(organization=organization, app=application)
		for subscription in list:
			subscription.subscriptionStatus = Choices.SUBSCRIPTION_VALID
			subscription.save()
		# ERP :: Write billing information for new client, generate billing documents, send by email

	def getNumberSubscriptions(self, account):
		"""Get number of subscriptions
		@param request: 
		@param account: 
		@return: numberSubscriptions"""
		try:
			numberSubscriptions = Subscription.objects.filter(organization__account=account, app__name=Constants.SOCIAL_NETWORK).count()
		except Exception as e:
			raise XpMsgException(e, _('Error in getting number of subscriptions'))
		return numberSubscriptions

class UserDAO(CommonDAO):
	
	def __init__(self, ctx, *ArgsTuple, **ArgsDict):
		super(UserDAO, self).__init__(ctx, *ArgsTuple, **ArgsDict)
		self._model = UserAccount
	
	def get(self, user, userName=None, socialChannel=Constants.PROFESSIONAL):
		"""Get UserSocial
		@param userName: 
		@param socialChannel:  
		@return: userX"""
		try:
			if userName == None:
				userX = UserSocial.objects.get(user=user, socialChannel=socialChannel)
			else:
				userX = UserSocial.objects.get(user__username = userName, socialChannel = socialChannel)
		except UserSocial.DoesNotExist:
			raise UserSocial.DoesNotExist
		return userX
	
	def getUser(self, userName):
		"""Get Django User
		@param username: 
		@return: user : User"""
		try:
			user = UserSys.objects.get(username=userName)
		except Exception as e:
			raise XpMsgException(e, _('Error when getting django user ') + str(userName))
		return user
	
	def deleteUserById(self, userId):
		"""Delete django user by id"""
		try:
			user = UserSys.objects.get(id=userId)
			user.delete()
		except Exception as e:
			raise XpMsgException(e, _('Error when deleting django user ') + str(userId))
		return user

	def getByUserId(self, userId, socialChannel=Constants.PROFESSIONAL):
		"""Get UserSocial for given django user id and social channel
		@param userId: 
		@param socialChannel:
		@return: userX"""
		try:
			user = UserSys.objects.get(id=userId)
			userX = UserSocial.objects.get(user=user, socialChannel=socialChannel)
		except UserSocial.DoesNotExist:
			raise UserSocial.DoesNotExist
		return userX

	def getDetails(self, user):
		"""Get UserSocial 
		@return: userDetail"""
		try:
			userDetail = UserDetail.objects.get(user=user)
		except UserSocial.DoesNotExist:
			raise UserSocial.DoesNotExist
		except UserDetail.DoesNotExist:
			raise UserDetail.DoesNotExist
		return userDetail

	def getChannels(self, user):
		"""Get social channels for user
		@return: userList"""
		userList = UserSocial.objects.filter(user=user)
		return userList

	def getChannelsByGroupList(self, userId, groupList):
		"""Get channels for user and list of groups. Used when user has in common two groups or more with user. Generally this will return a list of one element
		@param userId: 
		@param groupList: 
		@return: userList"""
		userList = UserSocial.objects.filter(user__id=userId, groups__in=groupList)
		return userList

	def getMyGroupsByChannel(self, user, socialChannel):
		"""Get the groups (either OrgGroup or Industry) I belong to, given the social channel 
		@param socialChannel: 
		@return: groupList"""
		userX = self.get(user, socialChannel=socialChannel)		
		groupList = userX.groups.filter(Q(isOrgGroup=True) | Q(industry=True))
		return groupList

	def getGroupsByChannel(self, user, socialChannel):
		"""Get all the groups I follow, either those I belong (org or industry) and groups follow with social channel
		@param socialProfile: 
		@return: groupList"""
		userX = self.getByChannel(user, socialChannel)
		groupList = userX.groups.all()
		return groupList

	def getOrgByChannel(self, user, socialChannel):
		"""Get organization for social channel"""
		organization = OrganizationDAO(self._ctx).getByAccount(user, socialChannel)
		return organization

	def getGroupsAllChannels(self, user):
		"""Get all the groups I follow, those I belong and groups follow with all social channels"""
		userListX = self.getChannels(user)
		groupList = []
		for userX in userListX:
			groupListTmp = userX.groups.all()
			for groupX in groupListTmp:
				groupList.append(groupX)
		return groupList

	def search(self, name):
		"""Search users by name
		@param name: 
		@return: userList"""
		userList = UserDetail.objects.filter(name__icontains=name)
		return userList
	
	def createUser(self, username, firstName, lastName, email, password, groupIdList):
		"""Create user and link to groups. Groups must already exist.
		@param username: 
		@param firstName: 
		@param lastName: 
		@param email: 
		@param password: 
		@param groupIdList: 
		@return: user : User"""
		# Create user
		user, bCreate = UserSys.objects.get_or_create(username=username, email=email, first_name=firstName, last_name=lastName)
		if bCreate == False:
			raise XpMsgException(self, _('Could not create user ') + str(user.username) + _('. User already exists'))		
		user.set_password(password)
		user.save()
		# Link groups
		for groupId in groupIdList:
			group = GroupSys.objects.get(pk=groupId)
			user.groups.add(group)
		return user

	def createUserChannel(self, user, socialChannel, groupIdList=[]):
		"""Create social profile and link to groups. Groups must already exist
		@param user: UserSys
		@param socialChannel: Either 'professional' or organization account name
		@param groupIdList: List of group (django) ids to link channel user to
		@return: userX : UserSocial"""
		# Create userX
		userX, bCreate = UserSocial.objects.get_or_create(user=user, socialChannel=socialChannel, userCreateId=user.id)
		if bCreate == False:
			raise XpMsgException(self, _('Could not create user ') + str(user.username) + _('. User already exists'))
		# Link groups
		for groupId in groupIdList:
			groupX = GroupSocial.objects.get(group__id=groupId)
			userX.groups.add(groupX)
		return userX

	def getNumberInvitationsLeft(self, user):
		"""Get number of invitations left for user 
		@return: numberInvitationsLeft"""
		numberInvitationsUsed = Invitation.objects.filter(fromUser=user).count()
		if user.is_staff:
			numberMaxInvitations = Constants.NUMBER_INVITATIONS_STAFF
		else:
			numberMaxInvitations = Constants.NUMBER_INVITATIONS_USER
		numberInvitationsLeft = numberMaxInvitations-numberInvitationsUsed
		return numberInvitationsLeft

	def invite(self, user, email, mobile, contactId, contactMethod, account, type=Choices.INVITATION_TYPE_ORDINARY):
		"""Invite other user to ximpia
		@return: invitation : Invitation"""
		fromAccount = None
		contact = None
		affiliate = None
		invitationCode = ''
		try:
			numberInvitationsLeft = self.getNumberInvitationsLeft(user)
			if numberInvitationsLeft == 0:
				raise XpMsgException(Exception, _('No invitations left. You used all your invitations'))
			for i in range(8):
				invitationCode += random.choice('0123456789ABCDEFG')
			try:
				invitation = Invitation.objects.get(invitationCode=invitationCode)
			except Invitation.DoesNotExist:
				invitation = None
			while invitation:
				invitationCode = ''
				for i in range(8):
					invitationCode += random.choice('0123456789ABCDEFG')
				try:
					invitation = Invitation.objects.get(invitationCode=invitationCode)
				except Invitation.DoesNotExist:
					invitation = None
			# FromAccount
			if account != '':
				fromAccount = Organization.objects.get(account=account)
			# Contact
			if contactId != '':
				contact = ContactDAO(self._ctx).get(contactId)
			# Should get affiliate from UserAccount or Organization
			if account != '':
				# Get affiliate from organization if any
				affiliate = fromAccount.affiliate
			else:
				# Get affiliate from professional if any
				try:
					affiliate = UserAccountDAO(self._ctx).get(user, Constants.PROFESSIONAL).affiliate
				except:
					affiliate = None
			# Number
			if user.is_staff:
				numberMaxInvitations = Constants.NUMBER_INVITATIONS_STAFF
			else:
				numberMaxInvitations = Constants.NUMBER_INVITATIONS_USER
			numberInvitationsUsed = numberMaxInvitations - numberInvitationsLeft
			number = numberInvitationsUsed + 1;
			invitation = Invitation.objects.create(
							fromUser=user, 
							invitationCode=invitationCode, 
							email=email, 
							mobile=mobile, 
							fromAccount=fromAccount,
							contact=contact,
							contactMethod=contactMethod,
							affiliate=affiliate,
							number=number,
							type = type)
		except Exception as e:
			raise XpMsgException(e, _('An error occurred when processing the invitation. Please retry later. Thanks '))
		return invitation

	def getInvitation(self, invitationCode, status=None):
		"""Get invitation for invitationCode 
		@param invitationCode: 
		@return: Invitation"""
		try:
			if status:
				invitation = Invitation.objects.get(invitationCode=invitationCode, status=status)
			else:
				invitation = Invitation.objects.get(invitationCode=invitationCode)
		except Exception as e:
			raise e
			#raise XpMsgException(e, _('Error in checking invitation code'))
		return invitation

	def changeInvitationUsed(self, invitation):
		"""Change status of invitation
		@param invitation: Invitation
		@return: invitation"""
		try:
			invitation.status = Constants.USED
			invitation.save()
		except Exception as e:
			raise XpMsgException(e, _('Error in chnaging status of invitation'))
		return invitation

	def writeSignupData(self, sUser, activationCode, invitation, postDict):
		"""Write signup data"""
		try:
			signupData = SignupData.objects.get(user=sUser)
			signupData.data = base64.encodestring(cPickle.dumps(postDict))
			signupData.activationCode = activationCode
			signupData.invitationType = invitation.type
			signupData.invitationByUser = invitation.fromUser
			signupData.invitationByOrg = invitation.fromAccount
			signupData.save()
		except SignupData.DoesNotExist:
			signupData = SignupData.objects.create(
													user=sUser,
													activationCode =  activationCode,
													invitationType = invitation.type,
													invitationByUser = invitation.fromUser,
													invitationByOrg = invitation.fromAccount,
													data= base64.encodestring(cPickle.dumps(postDict))
													)
		return signupData

	def getSignupData(self, sUser):
		"""Get signup data for user.
		@param sUser: User
		@return: postDict : Dictionary with sign up data"""
		signupData = SignupData.objects.get(user=sUser)
		return signupData

	def checkSameEmail(self, email):
		"""Checks that an user has same email
		@param email: 
		@return: boolean"""
		try:
			bEmailExists = UserSys.objects.filter(email=email).exists()
		except Exception as e:
			raise XpMsgException(e, _('Error in checking email'))
		return bEmailExists


class GroupDAO(CommonDAO):
	
	def __init__(self, ctx, *ArgsTuple, **ArgsDict):
		super(GroupDAO, self).__init__(ctx, *ArgsTuple, **ArgsDict)
		self._model = GroupSocial

	def validateGroupName(self, groupName, socialGroup):
		"""Validates the group name is ok with no reserved words. So far, checks that ximpia is not beginning of group name for social groups
		@param groupName: 
		@param socialGroup:  
		@return: boolean"""
		check = True
		for reservedWord in Constants.RESERVED_GROUP_NAME_LIST:
			indexXimpia = groupName.lower().find(reservedWord)
			if indexXimpia == 0 and socialGroup == True:
				check = False
		return check

	def save(self, form):
		"""Creates a Ximpia Group. Can be: XimpiaGroup, Industry, SocialGroup, Organization Group (Department), Public or Private.
		@param form: Form
		@return: groupX : GroupSocial
		@raise UserSocial.DoesNotExist: """
		user = self._ctx.user
		userX = self._ctx.userX
		d = getDataDict(form)
		adminUserIdList = json.loads(d['adminUserIdList'])
		accessGroupIdList = json.loads(d['accessGroupIdList'])
		tagList = json.loads(d['tagList'])
		bValidateGroup = self.validateGroupName(d['groupName'], d['socialGroup'])
		if not bValidateGroup:
			# TODO: Include Ximpia exception, validation exceptions, etc... Design exceptions
			raise XpMsgException(Exception, _('Error validating group'))
		try:
			bModify = False
			if d.has_key('groupId'):
				bModify = True
			if bModify:
				groupX = GroupSocial.objects.get(id=d['groupId'])
				groupX.ximpiaGroup = d['ximpiaGroup']
				groupX.industry = d['industry']
				groupX.isSocialGroup = d['socialGroup']
				groupX.isOrgGroup = d['orgGroup']
				groupX.isPublic = d['public']
				groupX.userModifyId = user.id
				groupX.account = d['account']
				groupX.save()
			else:
				group = GroupSys.objects.create(name=d['groupName'])
				groupX = GroupSocial.objects.create(group=group, groupNameId=d['groupNameId'], owner=userX, ximpiaGroup = d['ximpiaGroup'], 
						industry = d['industry'], isSocialGroup = d['socialGroup'], isOrgGroup = d['orgGroup'], isPublic = d['public'], 
						userCreateId = user.id)
			user.groups.add(group)
			# Admins
			if bModify == True:
				groupX.admins.all().delete()
			if bModify == True:
				self._doManyById(UserSocial, adminUserIdList, groupX.admins)				
			else:
				groupX.admins.add(userX)			
			# AccessGroups : in case group is private
			if bModify == True:
				groupX.accessGroups.all().delete()
			self._doManyById(GroupSocial, accessGroupIdList, groupX.accessGroups)
			# userX
			if bModify == False:
				userX.groups.add(groupX)
			# Tags
			if bModify == True:
				groupX.tags.all().delete()
			self._doManyByName(Tag, tagList, groupX.tags)			
		except UserSocial.DoesNotExist:
			raise UserSocial.DoesNotExist
		return groupX

	def getGroupsByIdList(self, groupIdList):
		"""Get list of groups by list of Ids 
		@param groupIdList: 
		@return: groupList"""
		list = GroupSocial.objects.filter(id__in=groupIdList)
		return list

	def edit(self, form):
		"""Doc."""
		user = self._ctx.user
		userX = self._ctx.userX
		d = getDataDict(form)
		# getFormParameter(form, '') => Checks to obtain value from data or cleaned_data
		#groupName = getDataDict(form)['groupName']
		ximpiaGroup = getDataDict(form)['ximpiaGroup']
		socialChannel = getDataDict(form)['socialChannel']
		industry = getDataDict(form)['industry']
		isSocialGroup = getDataDict(form)['isSocialGroup']
		isOrgGroup = getDataDict(form)['isOrgGroup']
		account = getDataDict(form)['account']
		isPublic = getDataDict(form)['isPublic']
		accessGroupIdList = json.loads(getDataDict(form)['accessGroupIdList'])
		groupId = getDataDict(form)['groupId']
		adminUserIdList = json.loads(getDataDict(form)['adminUserIdList'])
		#ownerUserId = getDataDict(form)['ownerUserId']
		tagList = json.loads(getDataDict(form)['tagList'])
		try:
			#userX = UserDAO(self._ctx).getByChannel(request, socialChannel)
			groupX = GroupSocial.objects.get(id=groupId)
			if ximpiaGroup != None:
				groupX.ximpiaGroup = ximpiaGroup
			if industry != None:
				groupX.industry = industry
			if isSocialGroup != None:
				groupX.isSocialGroup = isSocialGroup
			if isOrgGroup != None:
				groupX.isOrgGroup = isOrgGroup
			if isPublic != None:
				groupX.isPublic = isPublic
			groupX.userModifyId = user.id
			groupX.account = account
			groupX.save()
			# Admins
			groupX.admins.all().delete()
			for adminUserId in adminUserIdList:
				adminUserSocial = UserDAO(self._ctx).getById(adminUserId)
				groupX.admins.add(adminUserSocial)
			# AccessGroups
			groupX.accessGroups.all().delete()
			for accessGroupId in accessGroupIdList:
				accessGroup = GroupSocial.objects.get(id=accessGroupId)
				groupX.accessGroups.add(accessGroup)
			# Tags
			groupX.tags.all().delete()
			for sTag in tagList:
				tag, bCreate = Tag.objects.get_or_create(name=sTag)
				groupX.Tags.add(tag)
		except UserSocial.DoesNotExist:
			raise UserSocial.DoesNotExist
		except GroupSocial.DoesNotExist:
			raise GroupSocial.DoesNotExist
		except:
			raise Exception

	def getByName(self, groupName):
		"""Get group by name. Appends all data attached."""
		try:
			groupX = GroupSocial.objects.select_related().get(group__name = groupName)
			return groupX
		except GroupSocial.DoesNotExist:
			raise GroupSocial.DoesNotExist

	def getIdByName(self, groupName):
		"""Get group id giving group name"""
		try:
			groupId = GroupSocial.objects.get(group__name = groupName).id
			return groupId
		except GroupSocial.DoesNotExist:
			raise GroupSocial.DoesNotExist

	def delete(self, form):
		"""Deletes a group"""
		try:
			groupId = getDataDict(form)['groupId']
			groupX = GroupSocial.objects.get(id=groupId)
			group = GroupSys.objects.get(id=groupX.group.id)
			group.delete()
			# Unlink from all UserSocial
			#UserSocial.Groups.filter(id=groupId).delete()
			#UserSocial.Groups.through.objects.filter(id=groupId).delete()
			groupX.delete()
		except GroupSocial.DoesNotExist:
			raise GroupSocial.DoesNotExist
		except GroupSys.DoesNotExist:
			raise GroupSys.DoesNotExist
		return groupX

	def exists(self, form):
		"""Checks if group exists.
		@return: Boolean"""
		groupId = getDataDict(form)['groupId']
		check = GroupSocial.objects.get(id=groupId).exists()
		return check

	def listGroups(self, user, form, sessionAllowPrivateGrpSubs):
		"""List groups to join, either public or private with access from groups I belong"""
		try:
			query = getDataDict(form)['query']
			page = getDataDict(form)['page']
			numberMatches = getDataDict(form)['numberMatches']
			if not numberMatches:
				numberMatches = Constants.NUMBER_MATCHES
			if not page:
				page = 1
			iStart, iEnd = getPagingStartEnd(page, numberMatches)
			wordList = query.split()
			userX = UserSocial.objects.get(user=user)
			# Private group :: We assume that private groups will be granted access to other private groups
			myGroupsPrivate = userX.Groups.filter(public=False)
			groupListNamePrivate = GroupSocial.objects.filter(accessGroups__in=myGroupsPrivate)
			groupListTagPrivate = GroupSocial.objects.filter(accessGroups__in=myGroupsPrivate)
			# Public groups
			groupListName = GroupSocial.objects.filter(public=True)
			groupListTag = GroupSocial.objects.filter(public=True)
			# Should merge and order by alpha
			sortDict = {}
			sortList = []
			try:
				# ????????????????????
				if sessionAllowPrivateGrpSubs == True:			
				#if request.session[Constants.USER_SETTINGS][Constants.SETTINGS_ALLOW_PRIVATE_GRP_SUBS] == True:
					for groupX in groupListNamePrivate:
						sortList.append(groupX.group.name, groupX)
					for groupX in groupListTagPrivate:
						sortList.append(groupX.group.name, groupX)
			except KeyError:
				pass
			for groupX in groupListName:
				sortList.append(groupX.group.name, groupX)
			for groupX in groupListTag:
				sortList.append(groupX.group.name, groupX)
			sortList.sort()
			groupList = []
			i = 1
			for tuple in sortList:
				if i>= iStart and i<iEnd:
					groupList.append(tuple[1])
				if i> iEnd:
					break
		except UserSocial.DoesNotExist:
			raise UserSocial.DoesNotExist
		return groupList

	def searchMyGroupsByNameTags(self, user, form):
		"""Search my groups, either public or private"""
		try:
			query = getDataDict(form)['query']
			page = getDataDict(form)['page']
			numberMatches = getDataDict(form)['numberMatches']
			if not numberMatches:
				numberMatches = Constants.NUMBER_MATCHES
			if not page:
				page = 1
			iStart, iEnd = getPagingStartEnd(page, numberMatches)
			wordList = query.split()
			userX = UserSocial.objects.get(user=user)
			# Search for Name and Tag
			groupListName = userX.Groups.filter(group__name__istartswith=query)
			groupListTag = []
			for word in wordList:
				groupListTagTmp = userX.Groups.filter(group__name__istartswith=query)
				for field in groupListTagTmp:
					groupListTag.append(field)
			sortDict = {}
			sortList = []
			for groupX in groupListName:
				sortList.append(groupX.group.name, groupX)
			for groupX in groupListTag:
				sortList.append(groupX.group.name, groupX)
			sortList.sort()
			groupList = []
			i = 1
			for tuple in sortList:
				if i>= iStart and i<iEnd:
					groupList.append(tuple[1])
				if i> iEnd:
					break
		except UserSocial.DoesNotExist:
			raise UserSocial.DoesNotExist
		return groupList

	def searchGroupsByNameTags(self, user, form, sessionAllowPrivateGrpSubs):
		"""Search groups I have access in name and tags, sorted alphabetically. Called when users start typing group name in tooltip #abcd...
		@return: groupList : [GroupSocial,...]"""
		try:
			query = getDataDict(form)['query']
			page = getDataDict(form)['page']
			numberMatches = getDataDict(form)['numberMatches']
			if not numberMatches:
				numberMatches = Constants.NUMBER_MATCHES
			if not page:
				page = 1
			iStart, iEnd = getPagingStartEnd(page, numberMatches)
			wordList = query.split()
			userX = UserSocial.objects.get(user=user)
			# Private group :: We assume that private groups will be granted access to other private groups
			myGroupsPrivate = userX.Groups.filter(public=False)
			groupListNamePrivate = GroupSocial.objects.filter(group__name__istartswith=query, accessGroups__in=myGroupsPrivate)
			groupListTagPrivate = []
			for word in wordList:
				groupListTagPrivateTmp = GroupSocial.objects.filter(tags__name__icontains=word, accessGroups__in=myGroupsPrivate)
				for field in groupListTagPrivateTmp:
					groupListTagPrivate.append(field)
			# Public groups
			groupListName = GroupSocial.objects.filter(group__name__istartswith=query, public=True)
			groupListTag = []
			for word in wordList:
				groupListTagTmp = GroupSocial.objects.filter(tags__name__icontains=query, public=True)
				for field in groupListTagTmp:
					groupListTag.append(field)
			# Should merge and order by alpha
			sortDict = {}
			sortList = []
			try:
				# ???????????????????????
				if sessionAllowPrivateGrpSubs:			
				#if request.session[Constants.USER_SETTINGS][Constants.SETTINGS_ALLOW_PRIVATE_GRP_SUBS] == True:
					for groupX in groupListNamePrivate:
						sortList.append(groupX.group.name, groupX)
					for groupX in groupListTagPrivate:
						sortList.append(groupX.group.name, groupX)
			except KeyError:
				pass
			for groupX in groupListName:
				sortList.append(groupX.group.name, groupX)
			for groupX in groupListTag:
				sortList.append(groupX.group.name, groupX)
			sortList.sort()
			groupList = []
			i = 1
			for tuple in sortList:
				if i>= iStart and i<iEnd:
					groupList.append(tuple[1])
				if i> iEnd:
					break
		except UserSocial.DoesNotExist:
			raise UserSocial.DoesNotExist
		return groupList

	def hasAccess(self, form, userX, groupX):
		"""Checks in case group is private that my user belongs to a group that has access to the group"""
		accessGroupList = groupX.accessGroups.all()
		accessGroupIdList = []
		for accessGroup in accessGroupList:
			accessGroupIdList.append(accessGroup.id)
		list = userX.groups.in_bulk(accessGroupIdList)
		check = False
		if len(list) != 0:
			check = True
		return check

	def join(self, user, form):
		"""Join group"""
		try:
			groupId = getDataDict(form)['groupId']
			socialChannel = getDataDict(form)['socialChannel']
			groupX = GroupSocial.objects.get(id=groupId)
			userX = UserDAO(self._ctx).getByChannel(user, socialChannel)
			if groupX.Public == False:
				hasAccess = self.hasAccess(form, userX, groupX)
				if hasAccess:
					group = groupX.group
					user.groups.add(group)
					userX.groups.add(groupX)
			else:
				group = groupX.group
				user.groups.add(group)
				userX.groups.add(groupX)
			# I follow group stream like this??????
		except GroupSocial.DoesNotExist:
			raise GroupSocial.DoesNotExist
		except UserSocial.DoesNotExist:
			raise UserSocial.DoesNotExist

	def leave(self, user, form):
		"""Leave group"""
		try:
			groupId = getDataDict(form)['groupId']
			socialChannel = getDataDict(form)['socialChannel']
			groupX = GroupSocial.objects.get(id=groupId)
			# Delete django link from user to group
			user.groups.get(id=groupX.group.id).delete()
			userX = UserDAO(self._ctx).getByChannel(user, socialChannel)
			# Delete Ximpia link from userX to groupX
			userX.Groups.get(id=groupX.id).delete()
		except GroupSocial.DoesNotExist:
			raise GroupSocial.DoesNotExist
		except UserSocial.DoesNotExist:
			raise UserSocial.DoesNotExist

	def getOrganizations(self, groupList):
		"""Get organization list related to list of groups"""
		organizationList = []
		for groupX in groupList:
			account = groupX.account
			if account != '':
				organization = Organization.objects.get(account=account)
				organizationList.append(organization)
		return organizationList

class SocialDAO(CommonDAO):
	
	def __init__(self, ctx, *ArgsTuple, **ArgsDict):
		super(SocialDAO, self).__init__(ctx, *ArgsTuple, **ArgsDict)
		self._model = GroupFollow
	
	def followGroup(self, groupIdSource, groupIdTarget):
		"""Follow group, I will get all status from the group with '@GroupNameId' => 'x@GroupNameId'.
		@param groupIdSource: 
		@param groupIdTarget: """
		try:
			groupTarget = GroupSocial.objects.get(id=groupIdTarget)
			groupSource = GroupSocial.objects.get(id=groupIdSource)
			if groupTarget.Public == False:
				doFollow = groupTarget.accessGroups.exists(group=groupSource)
			else:
				doFollow = True
			if doFollow:
				groupFollow = GroupFollow.objects.create(groupSource=groupSource, groupTarget=groupTarget)
			else:
				# Raise exception XimpiaException with message
				pass
		except GroupSocial.DoesNotExist:
			raise GroupSocial.DoesNotExist

	def unfollowGroup(self, groupIdSource, groupIdTarget):
		"""Unfollow group target from source group, we delete the table GroupFollow for that criteria"""
		try:
			groupTarget = GroupSocial.objects.get(id=groupIdTarget)
			groupSource = GroupSocial.objects.get(id=groupIdSource)
			GroupFollow.objects.get(groupSource=groupSource, groupTarget=groupTarget).delete()
		except GroupSocial.DoesNotExist:
			raise GroupSocial.DoesNotExist
		except GroupFollow.DoesNotExist:
			raise GroupFollow.DoesNotExist

	def blockGroup(self, groupIdSource, groupIdTarget):
		"""Change status of link from groupSource to groupTarget"""
		try:
			groupTarget = GroupSocial.objects.get(id=groupIdTarget)
			groupSource = GroupSocial.objects.get(id=groupIdSource)
			groupFollow = GroupFollow.objects.get(groupSource=groupSource, groupTarget=groupTarget)
			groupFollow.status = Constants.BLOCKED
			groupFollow.save()
		except GroupSocial.DoesNotExist:
			raise GroupSocial.DoesNotExist
		except GroupFollow.DoesNotExist:
			raise GroupFollow.DoesNotExist

	def unblockGroup(self, groupIdSource, groupIdTarget):
		"""Change status of link from groupSource to groupTarget"""
		try:
			groupTarget = GroupSocial.objects.get(id=groupIdTarget)
			groupSource = GroupSocial.objects.get(id=groupIdSource)
			groupFollow = GroupFollow.objects.get(groupSource=groupSource, groupTarget=groupTarget)
			groupFollow.status = Constants.OK
			groupFollow.save()
		except GroupSocial.DoesNotExist:
			raise GroupSocial.DoesNotExist
		except GroupFollow.DoesNotExist:
			raise GroupFollow.DoesNotExist

	def listFollowing(self, groupIdSource, page, numberMatches=Constants.NUMBER_MATCHES):
		"""List of groups that we follow
		@param groupIdSource: 
		@param page: 1-XX
		@param numberMatches: Constants.NUMBER_MATCHES [optional]
		@return: list : List of Groups"""
		try:
			iStart, iEnd = getPagingStartEnd(page, numberMatches)
			groupSource = GroupSocial.objects.get(id=groupIdSource)
			list = GroupFollow.objects.filter(groupSource=groupSource)[iStart:iEnd]
		except GroupSocial.DoesNotExist:
			raise GroupSocial.DoesNotExist
		return list

	def listFollowed(self, groupIdTarget, page, numberMatches=Constants.NUMBER_MATCHES):
		"""List of groups that follow us
		@param groupIdTarget: 
		@param page: 1-XX
		@param numberMatches: Constants.NUMBER_MATCHES [optional]
		@return: list : List of Groups"""
		try:
			iStart, iEnd = getPagingStartEnd(page, numberMatches)
			groupTarget = GroupSocial.objects.get(id=groupIdTarget)
			list = GroupFollow.objects.filter(groupTarget=groupTarget)[iStart:iEnd]
		except GroupSocial.DoesNotExist:
			raise GroupSocial.DoesNotExist
		return list

	def listFollowedByList(self, myGroupList):
		"""List group that follow list of group provided, myGroupList
		@param myGroupList: 
		@return: groupFollowerList"""
		groupFollowerList = GroupFollow.objects.filter(groupTarget__in=myGroupList)
		return groupFollowerList

class StatusDAO(CommonDAO):
	
	def __init__(self, ctx, *ArgsTuple, **ArgsDict):
		super(StatusDAO, self).__init__(ctx, *ArgsTuple, **ArgsDict)
		self._model = GroupStream
	
	def update(self, user, status, socialChannel, source=None, fileIdList=[], tagIdList=[], linkIdList=[], groupIdList=[]):
		"""Update status
		@param status: Status message. In case of ximpia status, the html code. In case of other sources, json obtained.
		@param source: Used for twitter, facebook, etc... statuses [optional]
		@param fileIdList: [optional] 
		@param tagIdList: [optional]
		@param linkIdList: [optional]
		@param groupIdList: [optional]"""
		try:
			# Message
			statusTxt = parseText(status)
			linkStatusList = parseLinks(status)
			statusMessage = StatusMessage.objects.create(message=status, messageTxt=statusTxt)
			postId = statusMessage.id
			# Files
			fileDict = FileDAO(self._ctx).getMap(fileIdList)
			for fileId in fileIdList:
				file = fileDict[fileId]
				statusMessage.files.add(file)
			# Tags
			tagDict = TagDAO(self._ctx).getMap(tagIdList)
			for tagId in tagIdList:
				statusMessage.files.add(tagDict[tagId])
			# Links
			linkDict = LinkDAO(self._ctx).getMap(linkIdList)
			for linkId in linkIdList:
				statusMessage.links.add(linkDict[linkId])
			# Stream
			streamGroupList = []
			userX = UserDAO(self._ctx).getByChannel(user, socialChannel)
			myGroupList = UserDAO(self._ctx).getMyGroupsByChannel(user, socialChannel)
			groupFollowerList = SocialDAO(self._ctx).listFollowedByList(myGroupList)
			# Groups mentioned with tag @GroupNameId ???? Should be included in groupIdList with JS when clicking on '@'
			"""if len(groupIdList) != 0: 
				groupList = GroupSocial.objects.filter(pk__in=groupIdList)
				for groupX in groupList:
					groupFollowerList.append(groupX)"""
			# Links mentioned in status
			if len(linkStatusList) != 0:
				linkDict = LinkDAO(self._ctx).getIdList(linkStatusList)
				linkIdList = linkDict.keys()
				for linkId in linkIdList:
					statusMessage.links.add(linkDict[linkId])
			# GroupStream
			if source == None:
				for group in groupFollowerList:
					if group.isOrgGroup == True:
						streamGroupList.append((group, group.account, group.isPublic, Constants.XIMPIA))
					else:
						streamGroupList.append((group, '', group.isPublic, Constants.XIMPIA))
			else:
				for group in groupFollowerList:
					streamGroupList.append((group, '', True, source))
			for tuple in streamGroupList:
				group, account, public, source = tuple 
				groupStream = GroupStream(
							user=userX,  
							group=group,  
							message=statusMessage, 
							postId=postId, 
							public=public, 
							source=source)
				if account != '':
					groupStream.account = account
				groupStream.save()
		except UserSocial.DoesNotExist:
			raise UserSocial.DoesNotExist

	def getList(self, user, socialChannel=None, numberMatches=50):
		"""Get status for all groups I belong and groups I belong follow
		@param socialChannel: [optional]
		@param numberMatches: [optional]
		@return: statusList"""
		try:
			if socialChannel == None:
				myGroupList = UserDAO(self._ctx).getGroupsAllChannels(user)
			else:
				myGroupList = UserDAO(self._ctx).getGroupsByChannel(user, socialChannel)
			groupFollowList = SocialDAO(self._ctx).listFollowedByList(myGroupList)
			statusList = GroupStream.objects.select_related().filter(group__in=groupFollowList)[:numberMatches]
		except UserSocial.DoesNotExist:
			raise UserSocial.DoesNotExist
		return statusList

	def getListByUser(self, userId, numberMatches=50, public=None):
		"""Get list of statuses for user in all their channels
		@param request: 
		@param userId: 
		@param numberMatches: [optional=50]
		@param public: [optional=True]
		@return: statusList"""
		try:
			user = UserSys.objects.get(pk=userId)
			if public != None:
				statusList = GroupStream.objects.select_related().filter(user__user=user, public=public)[:numberMatches]
			else:
				statusList = GroupStream.objects.select_related().filter(user__user=user)[:numberMatches]
		except Exception as e:
			raise XpMsgException(e, _('Error getting status for user'))
		return statusList

	def getListByOrg(self, account, numberMatches=50, public=None):
		"""Get statuses for organization.
		@param request: 
		@param account: organization account
		@param numberMatches: [optional=50]
		@param public: [optional=None]
		@return: statusList"""
		try:
			if public != None:
				statusList = GroupStream.objects.select_related().filter(user__socialChannel=account, public=public)[:numberMatches]
			else:
				statusList = GroupStream.objects.select_related().filter(user__socialChannel=account)[:numberMatches]
		except Exception as e:
			raise XpMsgException(e, _('Error getting status for organization'))
		return statusList

	def getListByGroup(self, account, groupId, numberMatches=50, public=None):
		"""Get statuses for organization group
		@param request: 
		@param account: 
		@param groupId: 
		@param numberMatches: [optional=50]
		@param public: [optional=None]
		@return: statusList"""
		try:
			group = GroupSys.objects.get(pk=groupId)
			if public != None:
				statusList = GroupStream.objects.select_related().filter(
																		user__groups__in=[group], 
																		user__socialChannel=account, 
																		public=public)[:numberMatches]
			else:
				statusList = GroupStream.objects.select_related().filter(user__groups__in=[group], 
																		user__socialChannel=account)[:numberMatches]
		except Exception as e:
			raise XpMsgException(e, _('Error getting status for group'))
		return statusList

	def like(self, user, postId, socialChannel):
		"""Like the status
		@param postId: 
		@param socialChannel: """
		try:
			groupStream = GroupStream.objects.get(postId=postId)
			like = LikeDAO(self._ctx).get(user, socialChannel)
			groupStream.like.add(like)
		except GroupStream.DoesNotExist:
			raise GroupStream.DoesNotExist
		except UserSocial.DoesNotExist:
			raise UserSocial.DoesNotExist

	def comment(self, user, postId, socialChannel, content, public=True, fileIdList=[]):
		"""Comment status
		@param request: 
		@param postId: 
		@param socialProfile: 
		@param content: 
		@param public: [optional, default True]
		@param fileIdList: [optional]"""
		try:
			groupStream = GroupStream.objects.get(postId=postId)
			comment = self._dbComment.add(user, content, socialChannel, public, fileIdList)
			groupStream.comments.add(comment)
		except GroupStream.DoesNotExist:
			raise GroupStream.DoesNotExist
		except UserSocial.DoesNotExist:
			raise UserSocial.DoesNotExist
		except Comment.DoesNotExist:
			raise Comment.DoesNotExist

	def share(self):
		# TODO: Finish status share
		pass
	
	def makePublic(self):
		# TODO: Finish status make public
		pass

class TagDAO(CommonDAO):
	
	def __init__(self, ctx, *ArgsTuple, **ArgsDict):
		super(TagDAO, self).__init__(ctx, *ArgsTuple, **ArgsDict)
		self._model = Tag
	
	def getCreate(self, user, socialChannel, tagId=None, tag='', public=False, systemTag=False):
		"""Get or create a tag. If given tagId, we get tag. If we have more data we get or create
		@param tagId: [optional]
		@param tag: [optional]
		@param public: False [optional]
		@param systemFlag: [optional]
		@return: tag"""
		try:
			#socialChannel = request.session['socialChannel']
			# UserSocial
			userX = UserDAO(self._ctx).getByChannel(user, socialChannel)
			if tagId:
				tag = Tag.objects.get(id=tagId)
				tag.popularity += 1
				tag.save()
			else:
				tag, bCreateTag = Tag.objects.get_or_create(tag=tag, public=public, systemTag=systemTag)
			# TagUserTotal
			tagTotal, bCreate = TagUserTotal.objects.get_or_create(user=user, userX=userX, tag=tag)
			if bCreate != True:
				tagTotal.number += 1
				tagTotal.save()
		except (Tag.DoesNotExist, TagUserTotal.DoesNotExist) as e:
			raise XpMsgException(e, _('Error in processing the tag associated with your action'))
		return tag

	def listTagsForUser(self, user, socialChannel=None, public=None, userId=None, numberMatches=25):
		"""Tags for user in all socialChannels or filtered by socialChannel
		@param request: 
		@param socialChannel: [optional=None]
		@param public: [optional=True]
		@param userId: [optional=None]
		@return: tagList"""
		try:
			if public != None:
				if socialChannel != '' and userId == None:
					userX = UserDAO(self._ctx).getByChannel(user, socialChannel)
					tagList = TagUserTotal.objects.filter(userX=userX, tag__public = public)[:numberMatches]
				elif socialChannel == '' and userId == None:
					tagList = TagUserTotal.objects.filter(user=user, tag__public = public)[:numberMatches]
				elif socialChannel != '' and userId != None:
					userX = UserDAO(self._ctx).getByChannel(user, socialChannel, userId=userId)
					tagList = TagUserTotal.objects.filter(userX=userX, tag__public = public)[:numberMatches]
				elif socialChannel == '' and userId != None:
					tagList = TagUserTotal.objects.filter(user__id=userId, tag__public = public)[:numberMatches]
			else:
				if socialChannel != '' and userId == None:
					userX = UserDAO(self._ctx).getByChannel(user, socialChannel)
					tagList = TagUserTotal.objects.filter(userX=userX)[:numberMatches]
				elif socialChannel == '' and userId == None:
					tagList = TagUserTotal.objects.filter(user=user)[:numberMatches]
				elif socialChannel != '' and userId != None:
					userX = UserDAO(self._ctx).getByChannel(user, socialChannel, userId=userId)
					tagList = TagUserTotal.objects.filter(userX=userX)[:numberMatches]
				elif socialChannel == '' and userId != None:
					tagList = TagUserTotal.objects.filter(user__id=userId)[:numberMatches]
		except Exception as e:
			raise XpMsgException(e, _('Error in getting tags for user'))
		return tagList

	def listTagsForOrg(self, account, public=None, numberMatches=25):
		"""Get all links for organization shared by users
		@param request: 
		@param account:  
		@param public: [optional=None]
		@param numberMatches: [optional=25]
		@return: tagList"""
		try:
			if public != None:
				tagList = LinkUserTotal.objects.filter(userX__socialChannel=account, tag__public=public)[:numberMatches]
			else:
				tagList = LinkUserTotal.objects.filter(userX__socialChannel=account)[:numberMatches]
		except Exception as e:
			raise XpMsgException(e, _('Error in getting tags for organization'))
		return tagList

	def listTagsForGroup(self, account, groupId, public=None, numberMatches=25):
		"""Get all links for group and organization.
		@param request: 
		@param account: 
		@param groupId: 
		@param public: [optional=None]
		@param numberMatches: [optional=25]
		@return: linkList"""
		try:
			group = GroupDAO(self._ctx).getById(groupId)
			if public != None:
				tagList = TagUserTotal.objects.filter(
												userX__socialChannel=account,
												userX__groups__in=[group],
												tag__public=public)[:numberMatches]
			else:
				tagList = TagUserTotal.objects.filter(
												userX__socialChannel=account,
												userX__groups__in=[group])[:numberMatches]
		except Exception as e:
			raise XpMsgException(e, _('Error in getting tags for group organization'))
		return tagList

	def searchPublicTags(self, searchText):
		"""Doc."""
		try:
			tagList = Tag.objects.filter(name__icontains=searchText, isPublic=True)
		except Exception as e:
			raise XpMsgException(e, _('Error in getting tags for group organization'))
		return tagList

class CommentDAO(CommonDAO):
	
	def __init__(self, ctx, *ArgsTuple, **ArgsDict):
		super(GroupDAO, self).__init__(ctx, *ArgsTuple, **ArgsDict)
		self._model = Comment
	
	def add(self, user, content, socialChannel, public=False, fileIdList=[], tagIdList=[]):
		"""Create comment for user
		@param content: Comment text
		@param socialChannel: 
		@param public: If comment private for organization domain or public [optional]
		@param fileIdList: File attached to comment [optional]
		@return: comment"""
		try:
			contentLinkList = parseLinks(content)
			userX = UserDAO(self._ctx).getByChannel(user, socialChannel)
			comment = Comment.objects.create(user=userX, message=content, public=public)
			# Files
			if len(fileIdList) != 0:
				fileDict = FileDAO(self._ctx).getMap(fileIdList)
				for fileId in fileIdList:
					file = fileDict[fileId]
					comment.files.add(file)
			# Links (in content)
			if len(contentLinkList) != 0:
				#for contentLink in contentLinkList:
				linkDict = LinkDAO(self._ctx).getIdList(contentLinkList)
				linkIdList = linkDict.keys()
				for linkId in linkIdList:
					comment.links.add(linkDict[linkId])
			# Tags
			if len(tagIdList) != 0:
				tagDict = TagDAO(self._ctx).getMap(tagIdList)
				tagIdList = tagDict.keys()
				for tagId in tagIdList:
					tag = tagDict[tagId]
					comment.tags.add(tag)
		except UserSocial.DoesNotExist:
			raise UserSocial.DoesNotExist
		return comment

	def like(self, user, commentId, socialChannel):
		"""Likes a comment
		@param commentId: """
		try:
			like = LikeDAO(self._ctx).get(user, socialChannel)
			comment = Comment.objects.get(id=commentId)
			comment.like.add(like)
		except Comment.DoesNotExist:
			raise Comment.DoesNotExist

	def share(self):
		"""Share a comment"""
		# TODO: finish comment share
		pass

class LikeDAO(CommonDAO):
	
	def __init__(self, ctx, *ArgsTuple, **ArgsDict):
		super(LikeDAO, self).__init__(ctx, *ArgsTuple, **ArgsDict)
		self._model = Like
	
	def get(self, user, socialChannel):
		"""Get like object for signed on user. It uses get_or_create()"""
		userX = UserDAO(self._ctx).getByChannel(user, socialChannel)
		# Like
		like, bCreated = Like.objects.get_or_create(user=userX)
		like.number += 1
		like.save()
		return like

class LinkDAO(CommonDAO):
	
	def __init__(self, ctx, *ArgsTuple, **ArgsDict):
		super(LinkDAO, self).__init__(ctx, *ArgsTuple, **ArgsDict)
		self._model = Link
	
	def getCreate(self, user, socialChannel, linkId=None, url='', urlShort='', tagIdList=[], title='', summary='', description=''):
		"""Get or create a link. If given linkId, we get link. If we have more data we get or create link
		@param linkId: [optional]
		@param url: [optional]
		@return: link"""
		try:
			#socialChannel = request.session['socialChannel']
			# UserSocial
			userX = UserDAO(self._ctx).getByChannel(user, socialChannel)
			if linkId:
				link = Link.objects.get(id=linkId)
				link.numberShared += 1
				link.save()
			else:
				oUrl = util.resources.Url()
				domain = oUrl.getDomainName(url)
				try:
					link = Link.objects.get(Q(url=url) | Q(urlShort=urlShort))
					link.numberShared += 1
					link.save()
				except Link.DoesNotExist:
					link = Link.objects.create(url=url, urlShort=urlShort, domain=domain, urlTitle=title, summary=summary)
			# LinkUserTotal
			linkTotal, bCreate = LinkUserTotal.objects.get_or_create(user=user, userX=userX, link=link)
			if bCreate != True:
				linkTotal.number += 1
				linkTotal.save()
			# Tags
			if len(tagIdList) != 0:
				tagDict = TagDAO(self._ctx).getMap(tagIdList)
				tagIdList = tagDict.keys()
				for tagId in tagIdList:
					tag = tagDict[tagId]
					link.tags.add(tag)
		except Link.DoesNotExist:
			raise Link.DoesNotExist
		return link

	def listLinksForUser(self, user, socialChannel=None, public=None, userId=None, numberMatches=25):
		"""Get links for user in a social channel or all social channels
		@param request: 
		@param socialChannel: [optional=None]
		@param public: [optional=None]
		@param userId: [optional=None]
		@param numberMatches: [optional=25] 
		@return: linkList"""
		try:
			if public != None:
				if socialChannel != '' and userId == None:
					userX = UserDAO(self._ctx).getByChannel(user, socialChannel)
					linkList = LinkUserTotal.objects.filter(userX=userX, link__public=public)[:numberMatches]
				elif socialChannel == '' and userId == None:
					linkList = LinkUserTotal.objects.filter(user=user, link__public=public)[:numberMatches]
				elif socialChannel != '' and userId != None:
					userX = UserDAO(self._ctx).getByChannel(user, socialChannel, userId=userId)
					linkList = LinkUserTotal.objects.filter(userX=userX, link__public=public)[:numberMatches]
				elif socialChannel == '' and userId != None:
					linkList = LinkUserTotal.objects.filter(user__id=userId, link__public=public)[:numberMatches]
			else:
				if socialChannel != '' and userId == None:
					userX = UserDAO(self._ctx).getByChannel(user, socialChannel)
					linkList = LinkUserTotal.objects.filter(userX=userX)[:numberMatches]
				elif socialChannel == '' and userId == None:
					linkList = LinkUserTotal.objects.filter(user=user)[:numberMatches]
				elif socialChannel != '' and userId != None:
					userX = UserDAO(self._ctx).getByChannel(user, socialChannel, userId=userId)
					linkList = LinkUserTotal.objects.filter(userX=userX)[:numberMatches]
				elif socialChannel == '' and userId != None:
					linkList = LinkUserTotal.objects.filter(user__id=userId)[:numberMatches]
		except Exception as e:
			raise XpMsgException(e, _('Error in getting links for user'))
		return linkList

	def listLinksForOrg(self, account, public=None, numberMatches=25):
		"""Get all links for organization shared by users
		@param request: 
		@param account:  
		@param public: [optional=None]
		@param numberMatches: [optional=25]
		@return: linkList"""
		try:
			if public != None:
				linkList = LinkUserTotal.objects.filter(userX__socialChannel=account, link__public=public)[:numberMatches]
			else:
				linkList = LinkUserTotal.objects.filter(userX__socialChannel=account)[:numberMatches]
		except Exception as e:
			raise XpMsgException(e, _('Error in getting links for organization'))
		return linkList

	def listLinksForGroup(self, account, groupId, public=None, numberMatches=25):
		"""Get all links for group and organization.
		@param request: 
		@param account: 
		@param groupId: 
		@param public: [optional=None]
		@param numberMatches: [optional=25]
		@return: linkList"""
		try:
			group = GroupDAO(self._ctx).getById(groupId)
			if public != None:
				linkList = LinkUserTotal.objects.filter(
												userX__socialChannel=account,
												userX__groups__in=[group],
												link__public=public)[:numberMatches]
			else:
				linkList = LinkUserTotal.objects.filter(
												userX__socialChannel=account,
												userX__groups__in=[group])[:numberMatches]
		except Exception as e:
			raise XpMsgException(e, _('Error in getting links for group organization'))
		return linkList

class IndustryDAO(CommonDAO):
	
	def __init__(self, ctx, *ArgsTuple, **ArgsDict):
		super(GroupDAO, self).__init__(ctx, *ArgsTuple, **ArgsDict)
		self._model = Industry	

class UserAccountDAO(CommonDAO):
	
	def __init__(self, ctx, *ArgsTuple, **ArgsDict):
		super(UserAccountDAO, self).__init__(ctx, *ArgsTuple, **ArgsDict)
		self._model = UserAccount
	
	def get(self, user, socialChannel):
		"""Get professional by social channel"""
		try: 
			userDetail = UserDAO(self._ctx).getDetails(user)
			professional = UserAccount.objects.get(user=userDetail)
		except UserAccount.DoesNotExist:
			raise UserAccount.DoesNotExist
		return professional

	def getListByIdList(self, professionalIdList):
		"""Get list of professionals by list of ids"""
		list = UserAccount.objects.filter(id__in=professionalIdList)
		return list


class OrganizationDAO(CommonDAO):
	
	def __init__(self, ctx, *ArgsTuple, **ArgsDict):
		super(OrganizationDAO, self).__init__(ctx, *ArgsTuple, **ArgsDict)
		self._model = Organization
	
	def getByAccount(self, account):
		"""Doc."""
		organization = Organization.objects.get(account=account)
		return organization

	def getMapByAccounts(self, idList):
		"""Doc."""
		dict = {}
		if len(idList) != 0:
			list = Organization.objects.filter(account__in=idList)
			for organization in list:
				dict[organization.account] = organization
		return dict

	def getTeam(self, account):
		"""Get team of users for organization
		@param request: 
		@param account: 
		@return: userList (UserSocial)"""
		try:
			userList = UserSocial.objects.filter(socialChannel=account)
		except Exception as e:
			raise XpMsgException(e, _('Error in getting organization team'))
		return userList

class NotificationDAO(CommonDAO):
	
	def __init__(self, ctx, *ArgsTuple, **ArgsDict):
		super(NotificationDAO, self).__init__(ctx, *ArgsTuple, **ArgsDict)
		self._model = Notification
	
	def add(self, user, socialChannel, content):
		"""Adds notification for user and socialChannel
		@param request: 
		@param socialChannel: 
		@param content: Notification content with wikiText chars
		@return: Notification"""
		try:
			userX = UserDAO(self._ctx).getByChannel(user, socialChannel)
			notification = Notification.objects.create(owner=userX, content=content)
		except Exception as e:
			raise XpMsgException(e, _('Error in adding notification'))
		return notification

	def getList(self, user, numberRows=50):
		"""Get N first list of notifications for user
		@param request: 
		@param numberRows: 50
		@return: List"""
		try:
			list = Notification.objects.filter(owner__user=user)[:numberRows]
		except Exception as e:
			raise XpMsgException(e, _('Error in get notification list'))
		return list

class SkillDAO(CommonDAO):
	
	def __init__(self, ctx, *ArgsTuple, **ArgsDict):
		super(SkillDAO, self).__init__(ctx, *ArgsTuple, **ArgsDict)
		self._model = Skill
	
	def getList(self, skillCatCode=''):
		"""Get list of skill. Optional catCode can filter out results
		@param request: 
		@param skillCatCode: [optional]
		@return: skillList"""
		try:
			if skillCatCode == '':
				list = Skill.objects.all()
			else:
				skillList = UserParam.objects.filter(mode='skill_cat')
				list = Skill.objects.filter(catCode__in=skillList)
		except Exception as e:
			raise XpMsgException(e, _('Error in get notification list'))
		return list

	def add(self, skillName, skillCatCode):
		"""Add skill
		@param request: 
		@param skillName: 
		@param skillCatCode: """
		try:
			catCode = UserParam.objects.filter(mode='skill_cat', name=skillCatCode)
			tuple = Skill.objects.get_or_create(catCode=catCode, skillName=skillName)
			skill = tuple[0]
		except Exception as e:
			raise XpMsgException(e, _('Error in get notification list'))
		return skill

	def linkToUserAccount(self, user, socialChannel, professionalId, numberMonths, skillId, public=True):
		"""Link skill to professional
		@param request: 
		@param socialChannel: 
		@param professionalId: 
		@param numberMonths: 
		@param skillId: 
		@return: skillUserAccount"""
		try:
			professional = UserAccountDAO(self._ctx).getById(professionalId)
			skill = self.get(skillId)
			skillUserAccount, bCreate = SkillUserAccount.objects.get_or_create(
																skill=skill, 
																professional=professional, 
																numberMonths=numberMonths,
																public=public)
			groupList = UserDAO(self._ctx).getGroupsByChannel(user, socialChannel).filter(isOrgGroup=True)
			for groupX in groupList:
				organizationGroup = OrganizationGroup.objects.get(group=groupX)
				skillGroup, bCreate = SkillGroup.objects.get_or_create(skill=skill, group=organizationGroup)
		except Exception as e:
			raise XpMsgException(e, _('Error in link skill to professional'))
		return skillUserAccount

	def setSkillAccess(self, skillUserAccountId, public=False):
		"""Set skill access, either public or private
		@param request: 
		@param skillUserAccountId: 
		@param public: [optional]
		@return: skillUserAccount"""
		try:
			skillUserAccount = SkillUserAccount.objects.get(pk=skillUserAccountId)
			skillUserAccount.public = public
			skillUserAccount.save()
		except Exception as e:
			raise XpMsgException(e, _('Error in setting access rights to skill'))
		return skillUserAccount

	def getUserAccountSkills(self, professionalId, public=None):
		"""Get list of skills for user professional
		@param request: 
		@param professionalId: 
		@return: skillList"""
		try:
			if public != None:
				skillList = UserAccount.objects.get(pk=professionalId).skills.filter(public=public)
			else:
				skillList = UserAccount.objects.get(pk=professionalId).skills.all()
		except Exception as e:
			raise XpMsgException(e, _('Error in get professional skills'))
		return skillList

	def getGroupSkills(self, groupId, public=None):
		"""Get skills for group
		@param request: 
		@param groupId: 
		@param public: [optional=None]
		@return: skillList"""
		try:
			groupX = GroupDAO(self._ctx).getById(groupId)
			group = OrganizationGroup.objects.get(group=groupX)
			if public != None:
				skillList = group.Skills.filter(public=public)
			else:
				skillList = group.Skills.all()
		except Exception as e:
			raise XpMsgException(e, _('Error in get group skills'))
		return skillList

	def getOrgSkills(self, account, public=None):
		"""Get organization skills
		@param request: 
		@param account: 
		@param groupId: 
		@param public: [optional=None]
		@return: skillList"""
		try:
			organization = OrganizationDAO(self._ctx).getByAccount(account)
			groupList = organization.Groups.filter(group__isOrgGroup=True)
			skillTotalList = []
			if public != None:
				for group in groupList:
					skillList = group.Skills.filter(public=public)
					for skill in skillList:
						if skill not in skillTotalList:
							skillTotalList.append(skill)
			else:
				for group in groupList:
					skillList = group.skills.all()
					for skill in skillList:
						if skill not in skillTotalList:
							skillTotalList.append(skill)
		except Exception as e:
			raise XpMsgException(e, _('Error in get organization skills'))
		return skillTotalList

	def vote(self, professionalId, skillId, rating):
		"""Vote professional skill
		@param request: 
		@param professionalId: 
		@param skillId: 
		@param rating: [from 1 to 100]
		@return: skillUserAccount"""
		try:
			skillUserAccount = SkillUserAccount.objects.get(skill__id=skillId, professional__id=professionalId)
			skillUserAccount.rating += rating
			skillUserAccount.votes += 1
			skillUserAccount.save()
			# OrganizationGroup
			professional = UserAccountDAO(self._ctx).getById(professionalId)
			groupX = professional.group
			if groupX.isOrgGroup == True:
				skillGroup = SkillGroup.objects.get(skill__id=skillId, group__group__id=groupX)
				skillGroup.rating += rating
				skillGroup.votes += 1
				skillGroup.save()			
		except Exception as e:
			raise XpMsgException(e, _('Error in voting a professional skill'))
		return skillUserAccount

class AffiliateDAO(CommonDAO):
	
	def __init__(self, ctx, *ArgsTuple, **ArgsDict):
		super(AffiliateDAO, self).__init__(ctx, *ArgsTuple, **ArgsDict)
		self._model = Affiliate
	

class ProfileDAO(CommonDAO):
	
	def __init__(self, ctx, *ArgsTuple, **ArgsDict):
		super(ProfileDAO, self).__init__(ctx, *ArgsTuple, **ArgsDict)
		self._model = UserProfile
	
	def getUserPublicSite(self, user, professionalId, statusNumberMatches=100):
		"""Get entities for user public page
		@param request: 
		@param professionalId: 
		@param statusNumberMatches: [optional=100]
		@return: dictionary :: statusList,linkList,tagList,skillList,proRelList"""
		dict = {}
		# status
		statusList = StatusDAO(self._ctx).getListByUser(user.id, statusNumberMatches, public=True)
		dict['statusList'] = statusList
		# links
		linkList = LinkDAO(self._ctx).listLinksForUser(user, public=True)
		dict['linkList'] = linkList
		# tags
		tagList = TagDAO(self._ctx).listTagsForUser(user, public=True)
		dict['tagList'] = tagList
		# skills
		skillList = SkillDAO(self._ctx).getUserAccountSkills(professionalId, public=True)
		dict['skillList'] = skillList
		# organization groups
		professional = UserAccountDAO(self._ctx).getById(professionalId)
		professionalRelationList = professional.professionalRelations.filter(public=True)
		dict['proRelList'] = professionalRelationList
		return dict

	def getUser(self, user, professionalId, statusNumberMatches=100):
		"""Get entities for user profile
		@param request: 
		@param professionalId: 
		@param statusNumberMatches: [optional=100]
		@return: dictionary :: statusList,linkList,tagList,skillList,proRelList,professional, profile"""
		# Get social network profile with tabs, professional info, etc...
		dict = {}
		# status
		statusList = StatusDAO(self._ctx).getListByUser(user.id, statusNumberMatches)
		dict['statusList'] = statusList
		# links
		linkList = LinkDAO(self._ctx).listLinksForUser(user)
		dict['linkList'] = linkList
		# tags
		tagList = TagDAO(self._ctx).listTagsForUser(user)
		dict['tagList'] = tagList
		# skills
		skillList = SkillDAO(self._ctx).getUserAccountSkills(professionalId)
		dict['skillList'] = skillList
		# organization groups
		professional = UserAccountDAO(self._ctx).getById(professionalId)
		professionalRelationList = professional.professionalRelations.all()
		dict['proRelList'] = professionalRelationList
		dict['professional'] = professional
		# net profile
		profile = ProfileDAO(self._ctx).get(professionalId)
		dict['profile'] = profile
		return dict

	def getOrganizationPublicSite(self, account, statusNumberMatches=100):
		"""Get organization public profile
		@param request: 
		@param account: 
		@param statusNumberMatches: [optional=100]
		@return: dictionary :: statusList,linkList,tagList,skillList,userList,organization,groups"""
		dict = {}
		# status
		statusList = StatusDAO(self._ctx).getListByOrg(account, statusNumberMatches, public=True)
		dict['statusList'] = statusList
		# links
		linkList = LinkDAO(self._ctx).listLinksForOrg(account, public=True, numberMatches=statusNumberMatches)
		dict['linkList'] = linkList
		# tags
		tagList = TagDAO(self._ctx).listTagsForOrg(account, public=True, numberMatches=statusNumberMatches)
		dict['tagList'] = tagList
		# skills
		skillList = SkillDAO(self._ctx).getOrgSkills(account, public=True)
		dict['skillList'] = skillList
		# team
		userList = OrganizationDAO(self._ctx).getTeam(account)
		dict['userList'] = userList
		# organization
		organization = OrganizationDAO(self._ctx).getByAccount(account)
		dict['organization'] = organization
		# groups
		groups = organization.Groups.filter(group__public=True)
		dict['groups'] = groups
		return dict

	def getOrganizationGroupPublicSite(self, account, groupId, statusNumberMatches=100):
		"""Get organization group public profile entities
		@param request: 
		@param account: 
		@param groupId: 
		@param statusNumberMatches: [optional=100]
		@return: dictionary :: statusList,linkList,tagList,skillList,userList,organization,group"""
		dict = {}
		# status
		statusList = StatusDAO(self._ctx).getListByGroup(account, groupId, statusNumberMatches, public=True)
		dict['statusList'] = statusList
		# links
		linkList = LinkDAO(self._ctx).listLinksForGroup(account, groupId, public=True, numberMatches=statusNumberMatches)
		dict['linkList'] = linkList
		# tags
		tagList = TagDAO(self._ctx).listTagsForGroup(account, groupId, public=True, numberMatches=statusNumberMatches)
		dict['tagList'] = tagList
		# skills
		skillList = SkillDAO(self._ctx).getGroupSkills(groupId, public=True)
		dict['skillList'] = skillList
		# team
		userList = OrganizationDAO(self._ctx).getTeam(account)
		dict['userList'] = userList
		# organization
		organization = OrganizationDAO(self._ctx).getByAccount(account)
		dict['organization'] = organization
		# group
		group = GroupDAO(self._ctx).getById(groupId)
		dict['group'] = group
		return dict

	def getOrganization(self, account, statusNumberMatches=100):
		"""Get organization profile
		@param request: 
		@param account: 
		@param statusNumberMatches: [optional=100]
		@return: dictionary :: statusList,linkList,tagList,skillList,userList,organization,groups"""
		# Get organization information, team, groups
		dict = {}
		# status
		statusList = StatusDAO(self._ctx).getListByOrg(account, statusNumberMatches)
		dict['statusList'] = statusList
		# links
		linkList = LinkDAO(self._ctx).listLinksForOrg(account, numberMatches=statusNumberMatches)
		dict['linkList'] = linkList
		# tags
		tagList = TagDAO(self._ctx).listTagsForOrg(account, numberMatches=statusNumberMatches)
		dict['tagList'] = tagList
		# skills
		skillList = SkillDAO(self._ctx).getOrgSkills(account)
		dict['skillList'] = skillList
		# team
		userList = OrganizationDAO(self._ctx).getTeam(account)
		dict['userList'] = userList
		# organization
		organization = OrganizationDAO(self._ctx).getByAccount(account)
		dict['organization'] = organization
		# groups
		groups = organization.groups.all()
		dict['groups'] = groups
		return dict

	def getOrganizationGroup(self, account, groupId, statusNumberMatches=100):
		"""Get organization group profile entities
		@param request: 
		@param account: 
		@param groupId: 
		@param statusNumberMatches: [optional=100]
		@return: dictionary :: statusList,linkList,tagList,skillList,userList,organization,group"""
		# team, group information
		# status
		statusList = StatusDAO(self._ctx).getListByGroup(account, groupId, statusNumberMatches)
		dict['statusList'] = statusList
		# links
		linkList = LinkDAO(self._ctx).listLinksForGroup(account, groupId, numberMatches=statusNumberMatches)
		dict['linkList'] = linkList
		# tags
		tagList = TagDAO(self._ctx).listTagsForGroup(account, groupId, numberMatches=statusNumberMatches)
		dict['tagList'] = tagList
		# skills
		skillList = SkillDAO(self._ctx).getGroupSkills(groupId)
		dict['skillList'] = skillList
		# team
		userList = OrganizationDAO(self._ctx).getTeam(account)
		dict['userList'] = userList
		# organization
		organization = OrganizationDAO(self._ctx).getByAccount(account)
		dict['organization'] = organization
		# group
		group = GroupDAO(self._ctx).getById(groupId)
		dict['group'] = group
		return dict

	def writeFromNetworks(self, userAccountId, profileNetworkDict):
		"""Write the profile from profile"""
		userAccount = UserAccountDAO(self._ctx).getById(userAccountId)
		profile = UserProfile(userAccount=userAccount)		
		# Do logic for facebook and linkedin
		fbProfileDict = profileNetworkDict['facebook']
		if len(fbProfileDict) != 0:
			if fbProfileDict.has_key('bio'): profile.bio = fbProfileDict['bio']
			if fbProfileDict.has_key('hometown'): profile.homeTown = fbProfileDict['hometown']['name']
			if fbProfileDict.has_key('quotes'): profile.favQuotes = fbProfileDict['quotes']
			if fbProfileDict.has_key('gender'): profile.sex = fbProfileDict['gender']
			# TODO: Add more as we add final scopes from Facebook
		profile.save()		
		return profile

class ContactDAO(CommonDAO):
	
	def __init__(self, ctx, *ArgsTuple, **ArgsDict):
		super(ContactDAO, self).__init__(ctx, *ArgsTuple, **ArgsDict)
		self._model = Contact
	
	def put(self, form, bUpdateNets=True):
		"""Add contact"""
		# Directory
		userId = getFormDataValue(form, 'userId')
		orgList = json.loads(getFormDataValue(form, 'account'))
		groupList = json.loads(getFormDataValue(form, 'groupId'))
		# Data
		firstName = getFormDataValue(form, 'firstName')
		lastName = getFormDataValue(form, 'lastName')
		nickName = getFormDataValue(form, 'nickName')
		socialInfo = getFormDataValue(form, 'socialInfo')
		birthday = getFormDataValue(form, 'birthday')
		anniversary = getFormDataValue(form, 'anniversary')
		socialInfoDict = json.loads(socialInfo)
		industryIdList = json.loads(getFormDataValue(form, 'industryIdList'))
		assistantIdList = json.loads(getFormDataValue(form, 'assistantIdList'))
		reportToIdList = json.loads(getFormDataValue(form, 'reportToIdList'))
		tagIdList = json.loads(getFormDataValue(form, 'tagIdList'))
		relatedContactIdList = json.loads(getFormDataValue(form, 'relatedContactIdList'))
		addressDict = json.loads(getFormDataValue(form, 'adressDict'))
		commTypesDict = json.loads(getFormDataValue(form, 'comTypes'))
		socialChannel = getFormDataValue(form, 'socialChannel')
		bUpdate = False
		try:
			# Agenda, Directory or Social Network contact
			if getFormDataValue(form, 'ownerId') != '' or getFormDataValue(form, 'ownerGroupId') != '' \
				or getFormDataValue(form, 'ownerOrgId') != '':
				# Agenda
				bUpdate = True
				if getFormDataValue(form, 'ownerId') != '':
					professional = UserAccountDAO(self._ctx).getById(getFormDataValue(form, 'ownerId'))
					contactDetail, bCreate = ContactDetail.objects.get_or_create(firstName=firstName, lastName=lastName, 
																				nickName=nickName, owner=professional)
				elif getFormDataValue(form, 'ownerGroupId') != '':
					group = GroupDAO(self._ctx).getById(getFormDataValue(form, 'groupId'))
					contactDetail, bCreate = ContactDetail.objects.get_or_create(firstName=firstName, lastName=lastName, 
																				nickName=nickName, ownerGroup=group)
				elif getFormDataValue(form, 'ownerOrgId') != '':
					ownerOrg = OrganizationDAO(self._ctx).getByAccount(getFormDataValue(form, 'ownerOrg'))
					contactDetail, bCreate = ContactDetail.objects.get_or_create(firstName=firstName, lastName=lastName, 
																				nickName=nickName, ownerOrg=ownerOrg)
			else:
				if userId != '':
					# Directory
					bUpdate = True
					user = UserSys.objects.get(id=userId)
					contactDetail, bExists = ContactDetail.objects.get_or_create(user=user)
					contactDetail.firstName = firstName
					contactDetail.lastName = lastName
					contactDetail.nickName = nickName
				else:
					# Social Network
					if bUpdateNets == True:
						bUpdate = True
					list = ContactDetail.objects.filter(firstName=firstName, lastName=lastName, socialInfo__isnull = False)
					if len(list) == 1:
						contactDetail = list[0]
					elif len(list) > 1:
						# TODO: Include the processing of social info
						pass
			# Other attributes...
			if bUpdate == True:
				contactDetail.name = getFormDataValue(form, 'name')
				contactDetail.socialInfo = socialInfo
				contactDetail.salutation = getFormDataValue(form, 'salutation')
				contactDetail.birthDay = birthday
				contactDetail.anniversary = anniversary
				contactDetail.comBy = getFormDataValue(form, 'comBy')
				contactDetail.preferredSocialNet = getFormDataValue(form, 'preferredSocialNet')
				contactDetail.organization = getFormDataValue(form, 'organization')
				contactDetail.jobTitle = getFormDataValue(form, 'jobTitle')
				contactDetail.department = getFormDataValue(form, 'department')
				contactDetail.office = getFormDataValue(form, 'office')
				contactDetail.profession = getFormDataValue(form, 'profession')
				contactDetail.source = getFormDataValue(form, 'source')
				contactDetail.public = getFormDataValue(form, 'public')
				contactDetail.sserCreateId = user.pk
				contactDetail.save()
				# Communications
				list = commTypesDict.keys()
				for comm in list:
					tuple = commTypesDict[comm]
					name, value = tuple
					# CommunicationType
					communicationType = MasterValue.objects.get(name=comm, type=DbType.COMMTYPE)
					# CommunicationTypeContact
					communicationTypeContact = CommunicationTypeContact.objects.create(	contactDetail=contactDetail,
														communicationType = communicationType,
														name = name,
														value = value,
														userCreateId = user.pk)
				# Industries
				industryDict = IndustryDAO(self._ctx).getMap(industryIdList)
				for industryId in industryIdList:
					contactDetail.industries.add(industryDict[industryId])
				# Groups
				groupDict = GroupDAO(self._ctx).getMap(groupList)
				for groupId in groupList:
					contactDetail.groups.add(groupDict[groupId])
				# Organizations
				orgDict = OrganizationDAO(self._ctx).getMapByAccounts(orgList)
				for account in orgList:
					contactDetail.organizations.add(orgDict[account])
				# Assistants
				assistantDict = self.getDetailMap(assistantIdList)
				for contactId in assistantIdList:
					contactDetail.assistants.add(assistantDict[contactId])
				# Reports To
				reportToDict = self.getDetailMap(reportToIdList)
				for contactId in reportToIdList:
					contactDetail.reportsTo.add(reportToDict[contactId])
				# Tags
				tagDict = TagDAO(self._ctx).getMap(tagIdList)
				for tagId in tagDict:
					contactDetail.tags.add(tagDict[tagId])
				# Related Contacts
				relatedDict = self.getDetailMap(relatedContactIdList)
				for contactId in relatedContactIdList:
					contactDetail.relatedContacts.add(relatedDict[contactId])
				# Addresses
				for addrType in addressDict:
					addrDict = addressDict[addrType]
					address = Address.objects.get_or_create(	street=addrDict['street'], 
											city=addrDict['city'], 
											region=addrDict['region'], 
											zipCode=addrDict['zipCode'], 
											country=addrDict['country'])
					# AddressContact
					addressContact = AddressContact.objects.create(	addressType = addrType,
											contact = contactDetail,
											address = address)
			# Contact
			userX = None
			if getFormDataValue(form, 'ownerId') != '':
				userX = UserDAO(self._ctx).getByChannel(user, socialChannel)
				if socialChannel == Constants.PROFESSIONAL:
					ranking = Contact._RANKING_USER_ACCOUNT
				else:
					ranking = Contact._RANKING_USER
				contact, bExists = Contact.objects.get_or_create(user=userX, detail=contactDetail, ranking=ranking)
			elif getFormDataValue(form, 'ownerGroupId') != '':
				group = GroupDAO(self._ctx).getById(getFormDataValue(form, 'groupId'))
				contact, bExists = Contact.objects.get_or_create(group=group, detail=contactDetail, ranking=Contact._RANKING_GROUP)
			elif getFormDataValue(form, 'ownerOrgId') != '':
				ownerOrg = OrganizationDAO(self._ctx).getByAccount(getFormDataValue(form, 'ownerOrg'))
				contact, bExists = Contact.objects.get_or_create(organization=ownerOrg, detail=contactDetail, ranking = Contact._RANKING_ORG)
			else:
				userX = UserDAO(self._ctx).getByChannel(user, socialChannel)
				if socialChannel == Constants.PROFESSIONAL:
					ranking = Contact._RANKING_USER_ACCOUNT
				else:
					ranking = Contact._RANKING_USER
				contact, bExists = Contact.objects.get_or_create(user=userX, detail=contactDetail, ranking=ranking)
			if bCreate == True or contact.Notes != getFormDataValue(form, 'notes'):
				contact.notes = getFormDataValue(form, 'notes')
				contact.save()
			
			# Calendar for Birthday			
			if birthday != '' and userX != None:
				# Make dateStart TimeDate for day
				# TODO: Convert date to timeDate 09:00
				dateStart = ''
				calendarName = _('Birthday ') + name
				CalendarDAO(self._ctx).attachContactDate(user, userX, contact.id, Choices.CALENDAR_TYPE_BIRTHDAY, dateStart, name=calendarName)
			
			# Calendar for Anniversary
			if anniversary != '' and userX != None:
				# TODO: Convert date to timeDate 09:00
				dateStart = ''
				calendarName = _('Anniversary ') + name
				CalendarDAO(self._ctx).attachContactDate(user, userX, contact.id, Choices.CALENDAR_TYPE_ANNIVERSARY, dateStart, name=calendarName)
			
			tuple = (contact, contactDetail)
		except Exception as e:
			raise XpMsgException(e, _('Error in adding or updating contact information'))
		return tuple

	def createDirectoryUser(self, user, firstName, lastName, email, city, country, userXPro, userX, socialChannel, bOrg=False):
		"""Create user in directory"""
		try:
			#print 'createDirectoryUser()...', user, firstName, lastName, email, city, country, userXPro, userX, socialChannel
			# ContactDetail
			user = UserSys.objects.get(id=user.pk)
			contactDetail, bCreate = ContactDetail.objects.get_or_create(user=user)
			contactDetail.firstName = firstName
			contactDetail.lastName = lastName
			contactDetail.name = firstName + ' ' + lastName
			# Get groups from user
			groupList = userXPro.groups.all()
			for group in groupList:
				if group.isIndustry:
					contactDetail.industries.add(group)
				else:
					contactDetail.groups.add(group)
			"""if bCreate:
				contactDetail.userCreateId = user.pk
			else:
				contactDetail.userModifyId = user.pk"""
			contactDetail.save()
			# City and Country
			address, bCreate = Address.objects.get_or_create(city=city, country=country)
			addressTypeHome = Choices.ADDRESS_TYPE_HOME
			AddressContact.objects.create(addressType=addressTypeHome, contact=contactDetail, address=address)
			# Email
			communicationTypeEmail = MasterValue.objects.get(name='SN.COMMTYPE-EMAIL', type='SN.COMMTYPE')
			comContact = CommunicationTypeContact.objects.create(
										communicationType=communicationTypeEmail, 
										contact=contactDetail, 
										value=email)
			# Contact
			if bOrg == False:
				# UserAccount
				contact, bCreate = Contact.objects.get_or_create(user=userXPro, detail=contactDetail)
			else:
				# Organization
				contact, bCreate = Contact.objects.get_or_create(user=userXPro, detail=contactDetail)
				contact, bCreate = Contact.objects.get_or_create(user=userX, detail=contactDetail)
			return contactDetail
		except Exception as e:
			print e
			raise XpMsgException(e, _('Error creating user in directory'))
		
	def getDetail(self, contactDetailId):
		"""Get a contact"""
		try:
			# Get contactDetail
			contactDetail = ContactDetail.objects.get(id=contactDetailId)
		except Exception as e:
			raise XpMsgException(e, _('Error in fetching contact information'))
		return contactDetail

	def get(self, contactId):
		"""Get a contact"""
		try:
			# Get contactDetail
			contact = Contact.objects.get(id=contactId)
		except Exception as e:
			raise XpMsgException(e, _('Error in fetching contact information'))
		return contact

	def list(self, user, form):
		"""Get list of contacts, ordered by the Ranking attribute in Contact class"""
		page = getFormDataValue(form, 'page')
		numberMatches = getFormDataValue(form, 'numberMatches')
		socialChannel = getFormDataValue(form, 'socialChannel')
		if not numberMatches:
			numberMatches = Constants.NUMBER_MATCHES
		if not page:
			page = 1
		try:
			iStart, iEnd =  getPagingStartEnd(page, numberMatches)
			userX = UserDAO(self._ctx).getByChannel(user, socialChannel)
			groupList = UserDAO(self._ctx).getGroupsByChannel(user, socialChannel)
			orgList = UserDAO(self._ctx).getOrgByChannel(user, socialChannel)
			list = Contact.objects.select_related().distinct().filter(
														Q(user=userX) | 
														Q(group__in=groupList) | 
														Q(organization__in=orgList))[iStart:iEnd]
		except Exception as e:
			raise XpMsgException(e, _('Error in fetching contact information'))
		return list

	def search(self, user, form):
		"""Search for contacts"""
		page = getFormDataValue(form, 'page')
		numberMatches = getFormDataValue(form, 'numberMatches')
		#query = getFormDataValue(form, 'query')
		name = getFormDataValue(form, 'name')
		socialChannel = getFormDataValue(form, 'socialChannel')
		if not numberMatches:
			numberMatches = Constants.NUMBER_MATCHES
		if not page:
			page = 1
		try:
			# Name, Tags
			iStart, iEnd =  getPagingStartEnd(page, numberMatches)
			userX = UserDAO(self._ctx).getByChannel(user, socialChannel)
			groupList = UserDAO(self._ctx).getGroupsByChannel(user, socialChannel)
			orgList = UserDAO(self._ctx).getOrgByChannel(user, socialChannel)
			list = Contact.objects.select_related().distinct().filter(
														Q(user=userX) | 
														Q(group__in=groupList) | 
														Q(organization__in=orgList) | 
														Q(detail__name__icontains = name))[iStart:iEnd] 
		except Exception as e:
			raise XpMsgException(e, _('Error in fetching contact information'))
		return list

	def deleteFromSystem(self, contactDetailId, socialChannel):
		"""Deletes contact information from system."""
		try:
			# Delete Contact
			ContactDetail.objects.get(id=contactDetailId).delete()
		except Exception as e:
			raise XpMsgException(e, _('Error in fetching contact information'))

	def sendInvite(self, contactId, socialChannel):
		"""Send invitation to contact. So far, method email??????"""
		try:
			pass
		except Exception as e:
			raise XpMsgException(e, _('Error in fetching contact information'))

	def getDetailMap(self, contactIdList):
		"""Get contact map for a list if contactId"""
		dict = {}
		if len(contactIdList) != 0:
			list = ContactDetail.objects.filter(id__in=contactIdList)
			for contactDetail in list:
				dict[contactDetail.id] = contactDetail
		return dict

class CalendarDAO(CommonDAO):
	
	def __init__(self, ctx, *ArgsTuple, **ArgsDict):
		super(CalendarDAO, self).__init__(ctx, *ArgsTuple, **ArgsDict)
		self._model = Calendar
	
	def add(self, user, form):
		"""Add calendar activity"""
		socialChannel = getFormDataValue(form, 'socialChannel')
		name = getFormDataValue(form, 'name')
		location = getFormDataValue(form, 'location')
		notes = getFormDataValue(form, 'notes')
		dateStart = getFormDataValue(form, 'dateStart')
		dateEnd = getFormDataValue(form, 'dateEnd')
		type = getFormDataValue(form, 'type')
		repeat = getFormDataValue(form, 'repeat')
		allDay = getFormDataValue(form, 'allDay')
		public = getFormDataValue(form, 'public')
		tagIdList = json.loads(getFormDataValue(form, 'tagIdList'))
		contactDetailIdList = json.loads(getFormDataValue(form, 'contactDetailIdList'))
		groupIdList = json.loads(getFormDataValue(form, 'groupIdList'))
		fileIdList = json.loads(getFormDataValue(form, 'fileIdList'))
		linkIdList = json.loads(getFormDataValue(form, 'linkIdList'))
		contactInviteIdList = json.loads(getFormDataValue(form, 'contactInviteIdList'))
		try:
			# userX
			userX = None
			if socialChannel != '':
				userX = UserDAO(self._ctx).getByChannel(user, socialChannel)
			calendar = Calendar.objects.create(
											owner = userX,
											name = name,
											location = location,
											notes = notes,
											repeat = repeat,
											type = type,
											timeDateStart = dateStart,
											timeDateEnd = dateEnd,
											allDay = allDay,
											public = public,
											userCreateId = user.pk)
			# Tags
			tagDict = TagDAO(self._ctx).getMap(tagIdList)
			for tagId in tagIdList:
				calendar.tags.add(tagDict[tagId])
			# Contacts
			contactDict = ContactDAO(self._ctx).getDetailMap(contactDetailIdList)
			for contactDetailId in contactDetailIdList:
				calendar.contacts.add(contactDict[contactDetailId])
			# Groups
			groupDict = GroupDAO(self._ctx).getMap(groupIdList)
			for groupId in groupIdList:
				calendar.groups.add(groupDict[groupId])
			# Invitations
			contactMap = ContactDAO(self._ctx).getDetailMap(contactInviteIdList)
			for contactId in contactInviteIdList:
				calendarInvite = CalendarInvite.objects.create(
															calendar=calendar, 
															contact=contactMap[contactId], 
															status=Choices.CALENDAR_INVITE_STATUS_PENDING)
			# Files
			fileDict = FileDAO(self._ctx).getMap(fileIdList)
			for fileId in fileIdList:
				calendar.files.add(fileDict[fileId])
			# Links
			linkDict = LinkDAO(self._ctx).getMap(linkIdList)
			for linkId in linkIdList:
				calendar.links.add(linkDict[linkId])
		except Exception as e:
			raise XpMsgException(e, _('Error in processing calendar add'))
		return calendar

	def attachContactDate(self, user, userX, contactId, type, dateStart, name='', location='', bPublic=False):
		"""Does insert and update.
		@param request: 
		@param userX: 
		@param contactId: 
		@param dateStart: 
		@param type: 
		@param name: [optional]
		@param location: [optional]
		@param bPublic: [optional]
		@return: calendar"""
		try:
			calendar, bCreate = Calendar.objects.get_or_create(owner=userX, contacts__in=[contactId], Type=type)
			calendar.name = name
			calendar.location = location
			calendar.repeat = Choices.CALENDAR_REPEAT_YEARLY
			calendar.timeDateStart = dateStart
			calendar.allDay = True
			calendar.public = bPublic
			if bCreate == False:
				calendar.userModifyId = user.pk
			else:
				calendar.userCreateId = user.pk
			calendar.save()
			# Attach contact
			if bCreate == True:
				# Get contact
				contact = ContactDAO(self._ctx).get(contactId)
				calendar.contacts.add(contact)
		except Exception as e:
			raise XpMsgException(e, _('Error in processing contact calendar attach'))
		return calendar

	def update(self, user, form):
		"""Updates a calendar activity"""
		calendarId = getFormDataValue(form, 'calendarId')
		socialChannel = getFormDataValue(form, 'socialChannel')
		name = getFormDataValue(form, 'name')
		location = getFormDataValue(form, 'location')
		notes = getFormDataValue(form, 'notes')
		dateStart = getFormDataValue(form, 'dateStart')
		dateEnd = getFormDataValue(form, 'dateEnd')
		type = getFormDataValue(form, 'type')
		repeat = getFormDataValue(form, 'repeat')
		allDay = getFormDataValue(form, 'allDay')
		public = getFormDataValue(form, 'public')
		tagIdList = json.loads(getFormDataValue(form, 'tagIdList'))
		contactDetailIdList = json.loads(getFormDataValue(form, 'contactDetailIdList'))
		groupIdList = json.loads(getFormDataValue(form, 'groupIdList'))
		fileIdList = json.loads(getFormDataValue(form, 'fileIdList'))
		linkIdList = json.loads(getFormDataValue(form, 'linkIdList'))
		contactInviteIdList = json.loads(getFormDataValue(form, 'contactInviteIdList'))
		try:
			# userX
			userX = None
			if socialChannel != '':
				userX = UserDAO(self._ctx).getByChannel(user, socialChannel)
			calendar = Calendar.objects.get(id=calendarId)
			calendar.owner = userX
			calendar.name = name
			calendar.location = location
			calendar.notes = notes
			calendar.repeat = repeat
			calendar.type = type
			calendar.timeDateStart = dateStart
			calendar.timeDateEnd = dateEnd
			calendar.allDay = allDay
			calendar.public = public
			calendar.userModifyId = user.pk
			calendar.save()
			# Tags
			calendar.Tags.all().delete()
			tagDict = TagDAO(self._ctx).getMap(tagIdList)
			for tagId in tagIdList:
				calendar.tags.add(tagDict[tagId])
			# Contacts
			calendar.Contacts.all().delete()
			contactDict = ContactDAO(self._ctx).getDetailMap(contactDetailIdList)
			for contactDetailId in contactDetailIdList:
				calendar.contacts.add(contactDict[contactDetailId])
			# Groups
			calendar.Groups.all().delete()
			groupDict = GroupDAO(self._ctx).getMap(groupIdList)
			for groupId in groupIdList:
				calendar.groups.add(groupDict[groupId])
			# Invitations
			contactMap = ContactDAO(self._ctx).getDetailMap(contactInviteIdList)
			for contactId in contactInviteIdList:
				calendarInvite = CalendarInvite.objects.create(
															calendar=calendar, 
															contact=contactMap[contactId], 
															status=Choices.CALENDAR_INVITE_STATUS_PENDING)
			# Files
			calendar.Files.all().delete()
			fileDict = FileDAO(self._ctx).getMap(fileIdList)
			for fileId in fileIdList:
				calendar.files.add(fileDict[fileId])
			# Links
			calendar.Links.all().delete()
			linkDict = LinkDAO(self._ctx).getMap(linkIdList)
			for linkId in linkIdList:
				calendar.links.add(linkDict[linkId])
		except Exception as e:
			raise XpMsgException(e, _('Error in processing calendar update'))
		return calendar

	def inviteList(self, calendarId, contactInviteIdList):
		"""Invite a contact list to a calendar activity
		@param request: 
		@param calendarId: 
		@param contactInviteIdList: 
		@return: None """
		try:
			# Calendar
			calendar = self.get(calendarId)
			# Invitations
			contactMap = ContactDAO(self._ctx).getDetailMap(contactInviteIdList)
			for contactId in contactInviteIdList:
				calendarInvite = CalendarInvite.objects.create(
															calendar=calendar, 
															contact=contactMap[contactId], 
															status=Choices.CALENDAR_INVITE_STATUS_PENDING)
		except Exception as e:
			raise XpMsgException(e, _('Error in inviting contacts to calendar'))

	def changeInviteStatus(self, calendarId, contactDetailId, status):
		"""Change invitation status
		@param request: 
		@param calendarId: 
		@param contactDetailId: 
		@param status: 
		@return: None"""
		try:
			calendarInvite = CalendarInvite.objects.get(calendar__id=calendarId, contact__id=contactDetailId)
			calendarInvite.status = status
			calendarInvite.save()
		except Exception as e:
			raise XpMsgException(e, _('Error in changing calendar invitation status'))

	def comment(self, user, calendarId, content, socialChannel):
		"""Comment on a calendar activity
		@param request: 
		@param calendarId: 
		@param content: 
		@param socialChannel: 
		@return: calendar"""
		try:
			# Calendar
			calendar = self.getById(calendarId)
			# Comment
			comment = self._dbComment.add(user, content, socialChannel)
			calendar.comments.add(comment)
		except Exception as e:
			raise XpMsgException(e, _('Error in commenting calendar'))
		return calendar

	def like(self, user, calendarId, socialChannel):
		"""Like a calendar activity
		@param request: 
		@param calendarId: 
		@param socialChannel: 
		@return: calendar"""
		try:
			# Calendar
			calendar = self.getById(calendarId)
			# Like
			like = LikeDAO(self._ctx).get(user, socialChannel)
			calendar.like.add(like)
		except Exception as e:
			raise XpMsgException(e, _('Error in liking calendar activity'))
		return calendar

	def share(self, request):
		"""Share a calendar activity"""
		pass

class FileDAO(CommonDAO):
	
	def __init__(self, ctx, *ArgsTuple, **ArgsDict):
		super(FileDAO, self).__init__(ctx, *ArgsTuple, **ArgsDict)
		self._model = File
	
	def getCreate(self, form, fileId=None):
		"""Get and create file object
		@param request: 
		@param form: 
		@param fileId: 
		@return: File"""
		file = None
		"""try:
			if fileId:
				file = File.objects.get(id=fileId)
			else:
				socialChannel = getFormDataValue(form, 'socialChannel')
				fileName = getFormDataValue(form, 'fileName')
				fileTitle = getFormDataValue(form, 'fileTitle')
				fileDescription = getFormDataValue(form, 'fileDescription')
				fileSize = getFormDataValue(form, 'fileSize')
				public = getFormDataValue(form, 'public')
				fileType = getFormDataValue(form, 'fileType')
				fileMessage = getFormDataValue(form, 'fileMessage')
				writeGroupList = json.loads(getFormDataValue(form, 'writeGroupList'))
				writeUserAccountList = json.loads(getFormDataValue(form, 'writeUserAccountList'))
				professional = UserAccountDAO(self._ctx).get(request, socialChannel)
				try:
					file = File.objects.get(Name=fileName)
				except File.DoesNotExist:
					file = File(
							UploadedBy=professional, 
							Name=fileName,
							Title=fileTitle,
							Description=fileDescription,
							Size=fileSize,
							Public=public,
							Type=fileType,
							Message=fileMessage)
					file.save()
					# Version
					version = Version.objects.get_or_create(id=1)
					fileVersion = FileVersion.objects.create(File=file, Version=version, Size=fileSize)
					# Access Rights => Read and write for Uploader, Read for group inside organization
					groupList = UserDAO(self._ctx).getGroupsByChannel(request, socialChannel)
					organizationList = GroupDAO(self._ctx).getOrganizations(groupList)
					file.AccessReadUserAccounts.add(professional)
					file.AccessWriteUserAccounts.add(professional)
					for groupX in groupList:
						file.AccessReadGroups.add(groupX)
					for organization in organizationList:
						file.AccessReadOrganizations.add(organization)
					if len(writeGroupList) != 0:
						writeOrganizationList = GroupDAO(self._ctx).getOrganizations(writeGroupList)
						for groupX in writeGroupList:
							file.AccessWriteGroups.add(groupX)
						for organization in writeOrganizationList:
							file.AccessWriteOrganizations.add(organization)
					if len(writeUserAccountList) != 0:
						for professional in writeUserAccountList:
							file.AccessWriteUserAccounts.add(professional)
		except File.DoesNotExist:
			raise File.DoesNotExist
		except UserAccount.DoesNotExist:
			raise UserAccount.DoesNotExist"""
		return file

	def create(self, user, form):
		"""Creates file object
		@param request: 
		@param form: 
		@return: File"""
		socialChannel = getFormDataValue(form, 'socialChannel')
		fileName = getFormDataValue(form, 'fileName')
		fileTitle = getFormDataValue(form, 'fileTitle')
		fileDescription = getFormDataValue(form, 'fileDescription')
		fileSize = getFormDataValue(form, 'fileSize')
		tagIdList = getFormDataValue(form, 'tagIdList')
		public = getFormDataValue(form, 'public')
		fileType = getFormDataValue(form, 'fileType')
		fileMessage = getFormDataValue(form, 'fileMessage')
		writeGroupIdList = json.loads(getFormDataValue(form, 'writeGroupIdList'))
		writeUserAccountIdList = json.loads(getFormDataValue(form, 'writeUserAccountIdList'))
		professional = UserAccountDAO(self._ctx).get(user, socialChannel)
		try:
			file = File.objects.get(name=fileName)
			# TODO: Implement exception
			raise Exception
		except File.DoesNotExist:
			file = File(
					uploadedBy=professional, 
					name=fileName,
					title=fileTitle,
					description=fileDescription,
					size=fileSize,
					public=public,
					type=fileType,
					message=fileMessage)
			file.save()
			# Tags
			tagDict = TagDAO(self._ctx).getMap(tagIdList)
			for tagId in tagIdList:
				tag = tagDict[tagId]
				file.tags.add(tag)
			# Version
			version, bCreate = Version.objects.get_or_create(id=1)
			fileVersion = FileVersion.objects.create(file=file, version=version, size=fileSize)
			# Access Rights => Read and write for Uploader, Read for group inside organization
			groupList = UserDAO(self._ctx).getGroupsByChannel(user, socialChannel)
			organizationList = GroupDAO(self._ctx).getOrganizations(groupList)
			file.accessReadUserAccounts.add(professional)
			file.accessWriteUserAccounts.add(professional)
			for groupX in groupList:
				file.accessReadGroups.add(groupX)
			for organization in organizationList:
				file.accessReadOrganizations.add(organization)
			if len(writeGroupIdList) != 0:
				writeGroupList = GroupDAO(self._ctx).getGroupsByIdList(writeGroupIdList)
				writeOrganizationList = GroupDAO(self._ctx).getOrganizations(writeGroupList)
				for groupX in writeGroupList:
					file.accessWriteGroups.add(groupX)
				for organization in writeOrganizationList:
					file.accessWriteOrganizations.add(organization)
			if len(writeUserAccountIdList) != 0:
				writeUserAccountList = UserAccountDAO(self._ctx).getListByIdList(writeUserAccountIdList)
				for professional in writeUserAccountList:
					file.accessWriteUserAccounts.add(professional)
		tuple = (file, fileVersion)
		return file

	def deleteVersion(self, fileId, versionId):
		"""Delete file version
		@param request: 
		@param fileId: 
		@param versionId: 
		@return: fileVersion"""
		try:
			fileVersion = FileVersion.objects.get(file__id = fileId, version__id = versionId)
			fileVersion.delete()
		except FileVersion.DoesNotExist:
			raise FileVersion.DoesNotExist
		return fileVersion

	def update(self, user, form):
		"""Update File object"""
		fileId = getFormDataValue(form, 'fileId')
		socialChannel = getFormDataValue(form, 'socialChannel')
		fileTitle = getFormDataValue(form, 'fileTitle')
		fileDescription = getFormDataValue(form, 'fileDescription')
		tagIdList = getFormDataValue(form, 'tagIdList')
		public = getFormDataValue(form, 'public')
		readGroupIdList = json.loads(getFormDataValue(form, 'readGroupIdList'))
		writeGroupIdList = json.loads(getFormDataValue(form, 'writeGroupIdList'))
		writeUserAccountIdList = json.loads(getFormDataValue(form, 'writeUserAccountIdList'))
		professional = UserAccountDAO(self._ctx).get(user, socialChannel)
		try:
			file = File.objects.get(id=fileId)
			file.title = fileTitle
			file.description = fileDescription
			file.public = public
			file.save()
			# Tags
			file.tags.all().delete()
			tagDict = TagDAO(self._ctx).getMap(tagIdList)
			for tagId in tagIdList:
				tag = tagDict[tagId]
				file.tags.add(tag)
			# Access Write UserAccount
			if len(writeUserAccountIdList) != 0:
				file.accessWriteUserAccounts.all().delete()
				file.accessWriteUserAccounts.add(professional)
				writeUserAccountList = UserAccountDAO(self._ctx).getListByIdList(writeUserAccountIdList)
				for professional in writeUserAccountList:
					file.accessWriteUserAccounts.add(professional)
			# Access Write Group
			if len(writeGroupIdList) != 0:
				writeGroupList = GroupDAO(self._ctx).getGroupsByIdList(writeGroupIdList)
				writeOrganizationList = GroupDAO(self._ctx).getOrganizations(writeGroupList)
				for groupX in writeGroupList:
					file.accessWriteGroups.add(groupX)
				for organization in writeOrganizationList:
					file.accessWriteOrganizations.add(organization)
			# Access Read Group
			if len(readGroupIdList) != 0:
				readGroupList = GroupDAO(self._ctx).getGroupsByIdList(readGroupIdList)
				file.accessReadGroups.all().delete()
				organizationList = GroupDAO(self._ctx).getOrganizations(readGroupList)
				for groupX in readGroupList:
					file.accessReadGroups.add(groupX)
				for organization in organizationList:
					file.accessReadOrganizations.add(organization)
		except File.DoesNotExist:
			raise File.DoesNotExist
		return file

	def list(self, user, form):
		"""list files with page support
		@param request: 
		@param form: 
		@return: fileList"""
		page = getFormDataValue(form, 'page')
		numberMatches = getFormDataValue(form, 'numberMatches')
		socialChannel = getFormDataValue(form, 'socialChannel')
		if not numberMatches:
			numberMatches = Constants.NUMBER_MATCHES
		if not page:
			page = 1
		try:
			iStart, iEnd = getPagingStartEnd(page, numberMatches)
			userDetail = UserDAO(self._ctx).getDetails(user)
			professional = UserAccount.objects.get(User=userDetail, SocialChannel=socialChannel)
			if socialChannel != None:
				groupList = UserDAO(self._ctx).getGroupsByChannel(user, socialChannel)
				organizationList = GroupDAO(self._ctx).getOrganizations(groupList)
				if socialChannel == Constants.PROFESSIONAL:
					fileList = File.objects.select_related().filter(accessReadUserAccounts__in=[professional])[iStart:iEnd]
				else:
					fileList = File.objects.select_related().filter(
																accessReadOrganizations__in=organizationList, 
																accessReadGroups__in=groupList)[iStart:iEnd]
			else:
				iStart, iEnd = getPagingStartEnd(page, numberMatches)
				groupList = UserDAO(self._ctx).getGroupsAllChannels(user)
				organizationList = GroupDAO(self._ctx).getOrganizations(groupList)
				fileList = File.objects.select_related().filter( 
											Q(accessReadUserAccounts__in=[professional]) | 
											Q(accessReadOrganizations__in=organizationList, accessReadGroups__in=groupList) )[iStart:iEnd]								
		except UserSocial.DoesNotExist:
			raise UserSocial.DoesNotExist
		return fileList

	def search(self, user, form):
		"""Search files.
		@param request: 
		@param form: 
		@return: fileList"""
		fileName = getFormDataValue(form, 'fileName')
		fileTitle = getFormDataValue(form, 'fileTitle')
		fileDescription = getFormDataValue(form, 'fileDescription')
		page = getFormDataValue(form, 'page')
		numberMatches = getFormDataValue(form, 'numberMatches')
		socialChannel = getFormDataValue(form, 'socialChannel')
		if not numberMatches:
			numberMatches = Constants.NUMBER_MATCHES
		if not page:
			page = 1
		try:
			iStart, iEnd = getPagingStartEnd(page, numberMatches)
			userDetail = UserDAO(self._ctx).getDetails(user)
			professional = UserAccount.objects.get(User=userDetail, SocialChannel=socialChannel)
			if socialChannel != None:
				groupList = UserDAO(self._ctx).getGroupsByChannel(user, socialChannel)
				organizationList = GroupDAO(self._ctx).getOrganizations(groupList)
				if socialChannel == Constants.PROFESSIONAL:
					fileList = File.objects.select_related().filter(
														Q(name__icontains=fileName, title__icontains=fileTitle, 
														description__icontains=fileDescription),
														accessReadUserAccounts__in=[professional])[iStart:iEnd]
				else:
					fileList = File.objects.select_related().filter(
																Q(name__icontains=fileName, title__icontains=fileTitle, 
																	description__icontains=fileDescription),
																accessReadOrganizations__in=organizationList, 
																accessReadGroups__in=groupList)[iStart:iEnd]
			else:
				iStart, iEnd = getPagingStartEnd(page, numberMatches)
				groupList = UserDAO(self._ctx).getGroupsAllChannels(user)
				organizationList = GroupDAO(self._ctx).getOrganizations(groupList)
				fileList = File.objects.select_related().filter( 
											Q(accessReadUserAccounts__in=[professional]) | 
											Q(accessReadOrganizations__in=organizationList, accessReadGroups__in=groupList),
											Q(name__icontains=fileName, 
												title__icontains=fileTitle, 
												description__icontains=fileDescription) )[iStart:iEnd]								
		except UserSocial.DoesNotExist:
			raise UserSocial.DoesNotExist
		return fileList

	def addVersion(self, form, fileId):
		"""Add version to file
		@param request: 
		@param form: 
		@param fileId: """
		fileSize = getFormDataValue(form, 'fileSize')
		try:
			file = File.objects.get(id=fileId)
			file.size = fileSize
			lastVersionNumber = file.lastVersion
			versionNumber = lastVersionNumber + 1
			file.lastVersion = versionNumber
			file.save()
			version, bCreate = Version.objects.get_or_create(id=versionNumber)
			fileVersion = FileVersion.objects.create(file=file, version=version, size=fileSize)
		except File.DoesNotExist:
			raise File.DoesNotExist
		except Version.DoesNotExist:
			raise Version.DoesNotExist
		return fileVersion

	def assignWriteRights(self, socialChannel, fileId, groupList=[], professionalList=[]):
		"""Assign write rights to groupList or professionalList
		@param request: 
		@param socialChannel: 
		@param fileId: 
		@param groupList: [optional]
		@param professionalList: [optional]
		@return: File"""
		try:
			file = File.objects.get(id=fileId)
			# Access Rights
			if len(groupList) != 0:
				organizationList = GroupDAO(self._ctx).getOrganizations(groupList)
				for groupX in groupList:
					file.accessWriteGroups.add(groupX)
				for organization in organizationList:
					file.accessWriteOrganizations.add(organization)
			elif len(professionalList) != 0:
				for professional in professionalList:
					file.accessWriteUserAccounts.add(professional)
		except File.DoesNotExist:
			raise File.DoesNotExist
		except UserAccount.DoesNotExist:
			raise UserAccount.DoesNotExist
		return file

	def assignReadRights(self, socialChannel, fileId, groupList):
		"""Assign read rights to group list
		@param request: 
		@param socialChannel:
		@param fileId: 
		@param groupList: 
		@return: File"""
		try:
			file = File.objects.get(id=fileId)
			# Access Rights
			organizationList = GroupDAO(self._ctx).getOrganizations(groupList)
			for groupX in groupList:
				file.accessReadGroups.add(groupX)
			for organization in organizationList:
				file.accessReadOrganizations.add(organization)
		except File.DoesNotExist:
			raise File.DoesNotExist
		except UserAccount.DoesNotExist:
			raise UserAccount.DoesNotExist
		return file

	def share(self, fileId):
		"""Share a file"""
		pass

	def makePublic(self, fileId):
		"""Make public in ximpia and world a file"""
		pass
