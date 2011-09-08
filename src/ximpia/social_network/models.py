import types
import traceback

from django.db import models
from django.contrib.auth.models import User as UserSys, Group as GroupSys
from django.utils.translation import ugettext as _
from ximpia import settings
from django.utils import translation
from choices import Choices
from constants import Constants
from validators import *

class DeleteManager(models.Manager):
	def get_query_set(self):
		return super(DeleteManager, self).get_query_set().filter(delete=False)

class BaseModel(models.Model):
	"""Abstract Base Model"""
	_ctx = None
	dateCreate = models.DateTimeField(auto_now_add=True, null=True, blank=True, editable=False, 
					verbose_name= _('Create Date'), help_text= _('Create Date'))
	dateModify = models.DateTimeField(auto_now=True, null=True, blank=True, editable=False, 
					verbose_name= _('Modify Date'), help_text= _('Modify Date'))
	userCreateId = models.IntegerField(null=True, blank=True, editable=False, 
					verbose_name=_('User Create Id'), help_text=_('User that data'))
	userModifyId = models.IntegerField(null=True, blank=True, editable=False, 
					verbose_name=_('User Modify Id'), help_text=_('User that madofied data'))
	delete = models.BooleanField(default=False, editable=False,
				verbose_name=_('Delete'), help_text=_('Field that sets logical deletes'))
	"""def __init__(self, ctx=None, *argsTuple, **argsDict):
		self._ctx = ctx if ctx != None else None
		super(BaseModel, self).__init__(*argsTuple, **argsDict)"""
	objects = DeleteManager()
	objects_del = models.Manager()
	"""def save(self, ctx, *argsTuple, **argsDict):
		if self.pk:
			self.userModifyId = self._ctx.user.id
		else:
			self.userCreateId = self._ctx.user.id
		super(BaseModel, self).save(*argsTuple, **argsDict)"""
	class Meta:
		abstract = True

class MasterValue(BaseModel):
	"""Master Values"""
	name = models.CharField(max_length=50,
			verbose_name=_('Name'), help_text=_('Name'))
	value = models.CharField(max_length=100,
			verbose_name=_('Value'), help_text=_('Value'))
	type = models.CharField(max_length=30, db_index=True,
			verbose_name=_('Type'), help_text=_('Type'))
	def __unicode__(self):
		return str(self.name) + ' => ' + str(self.value)
	class Meta:
		db_table = 'SN_MASTER_VALUE'
		verbose_name = _('Master Value')
		verbose_name_plural = _('Master Values')

class UserParam(BaseModel):
	"""User Parameters"""
	mode = models.CharField(max_length=20, 
			verbose_name=_('Mode'), help_text=_('Parameter Mode'))
	name = models.CharField(max_length=20, 
			verbose_name=_('Name'), help_text=_('Parameter Name'))
	value = models.CharField(max_length=100, null=True, blank=True, 
			verbose_name=_('Value'), help_text=_('Parameter Value for Strings'))
	valueId = models.IntegerField(null=True, blank=True, 
			verbose_name=_('Value Id'), help_text=_('Parameter Value for Integers'))
	def __unicode__(self):
		return str(self.mode) + ' - ' + str(self.name)
	class Meta:
		db_table = 'SN_PARAM'
		verbose_name = "User Parameter"
		verbose_name_plural = "User Parameters"

class Address(BaseModel):
	"""Address"""
	street = models.CharField(max_length=50, null=True, blank=True,
			verbose_name = _('Street'), help_text = _('Street'))
	city = models.CharField(max_length=20,
			verbose_name = _('City'), help_text = _('City'))
	region = models.CharField(max_length=20, null=True, blank=True,
			verbose_name = _('Region'), help_text = _('Region'))
	zipCode = models.CharField(max_length=20, null=True, blank=True,
			verbose_name = _('Zip Code'), help_text = _('Zip Code'))
	country = models.CharField(max_length=2, choices=Choices.COUNTRY,
			verbose_name = _('Country'), help_text = _('Country'))
	def __unicode__(self):
		return str(self.street) + ' ' + str(self.city)
	class Meta:
		db_table = 'SN_ADDRESS'
		verbose_name = _('Address')
		verbose_name_plural = _('Addresses')

class SocialNetwork(BaseModel):
	type = models.ForeignKey(UserParam, limit_choices_to={'mode__lte': 'nets'},
				verbose_name = _('Social Network Type'), help_text = _('Type of social network'))
	def __unicode__(self):
		return str(self.type)
	def getName(self):
		return self.type.name
	class Meta:
		db_table = 'SN_SOCIAL_NETWORK'
		verbose_name = _('Social Network')
		verbose_name_plural = _("Social Networks")

class SocialNetworkUserSocial(models.Model):
	user = models.ForeignKey('UserDetail',
				verbose_name = _('User'), help_text = _('User'))
	socialNetwork = models.ForeignKey('SocialNetwork',
				verbose_name = _('Social Network'), help_text = _('Social network'))
	token = models.CharField(max_length=255,
				verbose_name = _('Token'), help_text = _('Token'))
	tokenSecret = models.CharField(max_length=255, null=True, blank=True,
				verbose_name = _('Token Secret'), help_text = _('Token secret'))
	def __unicode__(self):
		return str(self.getName()) + ' ' + str(self.user)
	def getName(self):
		return self.socialNetwork.getName()
	class Meta:
		db_table = 'SN_USER_socialNetwork'
		verbose_name = 'Social Network for User'
		verbose_name_plural = "Social Networks for User"

class UserSocial(BaseModel):
	"""Model for UserSocial
	FK : User
	MN: Groups
	SocialChannel"""
	user = models.ForeignKey(UserSys, 
				verbose_name = _('User'), help_text = _('User'))
	groups = models.ManyToManyField('GroupSocial',
				verbose_name = _('Groups'), help_text = _('Groups'))
	socialChannel = models.CharField(max_length=20, default=Constants.USER,
				verbose_name = _('Social Channel'), help_text = _('Social Channel'))
	def __unicode__(self):
		return str(self.user.username) + '-' + str(self.socialChannel)
	def getGroupById(self, groupId):
		"""Doc."""
		list = self.groups.filter(pk=groupId)
		if len(list) != 0:
			value = list[0]
		else:
			value = None
		return value
	def getFullName(self):
		"""Get full name: firstName lastName"""
		name = self.user.get_full_name()
		return name
	class Meta:
		db_table = 'SN_USER'
		verbose_name = 'User'
		verbose_name_plural = "Users"
		unique_together = ("user", "socialChannel")
	
class UserDetail(BaseModel):
	"""Model for UserSocial
	FK : User
	MN: SocialNetworks"""
	user = models.ForeignKey(UserSys,
				verbose_name = _('User'), help_text = _('User'))
	name = models.CharField(max_length=60,
				verbose_name = _('Name'), help_text = _('Name'))
	settings = models.TextField(default = '', null=True, blank=True,
				verbose_name = _('Settings'), help_text = _('Settings'))
	socialNetworks = models.ManyToManyField('SocialNetwork', through='SocialNetworkUserSocial',  null=True, blank=True,
				verbose_name = _('Social Networks'), help_text = _('Social Networks'))
	hasUploadPic = models.BooleanField(default=False,
				verbose_name = _('Uploaded Pic'), help_text = _('Has the user uploaded custom picture?'))
	isSuspended = models.BooleanField(default=False,
				verbose_name = _('Suspended'), help_text = _('Weather user account has been suspended'))
	picExt = models.CharField(max_length=3, null=True, blank=True,
				verbose_name = _('Picture Extension'), help_text = _('Picture file extension'))
	reminderId = models.CharField(max_length=15, null=True, blank=True,
				verbose_name = _('Reminder Id'), help_text = _('Reminder identification for password retreive'))
	lang = models.CharField(max_length=2, default='en',
				verbose_name = _('Language'), help_text = _('Language'))
	auth = models.TextField(default = '', null=True, blank=True,
				verbose_name = _('Authentication'), help_text = _('Authentication'))	
	netProfiles = models.TextField(default = '', null=True, blank=True,
				verbose_name = _('Network Profiles'), help_text = _('Network Profiles'))	
	msgPreference = models.CharField(max_length=10, choices=Choices.MSG_PREFERRED, default=Constants.XIMPIA,
				verbose_name = _('Messaging Preference'), help_text = _('Preference for sending messages: Facebook, Twitter, Email, etc...'))
	hasValidatedEmail = models.BooleanField(default=False,
				verbose_name = _('Validated Email'), help_text = _('User has validated his email address?'))
	filesQuota = models.IntegerField(default=Constants.FILE_QUOTA_DEFAULT,
				verbose_name = _('File Quota'), help_text = _('Maximum size storage for files'))
	def __unicode__(self):
		return str(self.user.username)
	def getSocialNetworkUser(self, socialNetName):
		"""Doc."""
		list = self.socialNetworks.filter(type__name=socialNetName)
		if len(list) != 0:
			value = list[0].socialnetworkuserSocial_set.all()[0]
		else:
			value = None
		return value
	class Meta:
		db_table = 'SN_USER_DETAIL'
		verbose_name = 'UserDetail'
		verbose_name_plural = "UsersDetail"

class GroupSocial(BaseModel):
	"""Ximpia Group Model.
	FK: Group
	FK: Owner
	MN: Tags
	MN: Admins->UserSocial
	MN: AccessGroups
	XimpiaGroup
	Industry
	SocialGroup
	OrgGroup
	Public"""
	group = models.ForeignKey(GroupSys, unique=True,
				verbose_name = _('Group'), help_text = _('Group'))
	groupNameId = models.CharField(max_length=20, null=True, blank=True,
				verbose_name = _('Group Name Id'), help_text = _('Identification for group'))
	isXimpiaGroup = models.BooleanField(default=False,
				verbose_name = _('Ximpia Group'), help_text = _('System Group'))
	isIndustry = models.BooleanField(default=False,
				verbose_name = _('Industry'), help_text = _('Industry'))
	isSocialGroup = models.BooleanField(default=False,
				verbose_name = _('Social Group'), help_text = _('Group is a social group'))
	isOrgGroup = models.BooleanField(default=False,
				verbose_name = _('Organization Group'), help_text = _('Group belongs to organization'))
	account = models.ForeignKey('Organization', null=True, blank=True,
				verbose_name = _('Account'), help_text = _('Account name'))
	isPublic = models.BooleanField(default=True,
				verbose_name = _('Public'), help_text = _('Group is public'))
	accessGroups = models.ManyToManyField('self', related_name='group_access', null=True, blank=True,
				verbose_name = _('Access Groups'), help_text = _('Groups that have access to this group'))
	tags = models.ManyToManyField('Tag', null=True, blank=True,
				verbose_name = _('Tags'), help_text = _('Tags'))
	owner = models.ForeignKey('UserSocial', related_name='group_owner', null=True, blank=True,
				verbose_name = _('Group Owner'), help_text = _('Owner of group'))
	admins = models.ManyToManyField('UserSocial', related_name='group_admins', null=True, blank=True,
				verbose_name = _('Administrators'), help_text = _('Administrators'))
	managers = models.ManyToManyField('UserSocial', related_name='group_managers', null=True, blank=True,
				verbose_name = _('Managers'), help_text = _('Managers'))
	def __unicode__(self):
		if self.account != None:
			return str(self.account) + '-' + str(self.group)
		else:
			return str(self.group)
	class Meta:
		db_table = 'SN_GROUP'
		verbose_name = 'Group'
		verbose_name_plural = "Groups"

class GroupFollow(BaseModel):
	"""Group Follow Model
	FK: GroupSource
	FK: GroupTarget
	Status"""
	groupSource = models.ForeignKey('GroupSocial', related_name='group_follow_source',
				verbose_name = _('Group Source'), help_text = _('Group that follows'))
	groupTarget = models.ForeignKey('GroupSocial', related_name='group_follow_target',
				verbose_name = _('Group Target'), help_text = _('Group followed'))
	status = models.CharField(max_length=10, choices=Choices.FOLLOW_STATUS, default=Constants.OK,
				verbose_name = _('Status'), help_text = _('Group status: ok, blocked, unblocked'))
	def __unicode__(self):
		return str(self.groupSource) + ' - ' + str(self.groupTarget)
	class Meta:
		db_table = 'SN_GROUP_FOLLOW'
		verbose_name = _('Group Follow')
		verbose_name_plural = _("Group Follows")

class StatusMessage(BaseModel):
	"""Status Message Model
	MN: Tags
	MN: Files
	MN: Links
	Message
	MessageTxt"""
	message = models.TextField(verbose_name = _('Message'), help_text = _('Message'))
	messageTxt = models.TextField(verbose_name = _('Message Text'), help_text = _('Message in text mode, no tags'))
	tags = models.ManyToManyField('Tag', null=True, blank=True,
				verbose_name = _('Tags'), help_text = _('Message tags'))
	files = models.ManyToManyField('File', null=True, blank=True,
				verbose_name = _('Files'), help_text = _('Message files'))
	links = models.ManyToManyField('Link', null=True, blank=True,
				verbose_name = _('Links'), help_text = _('Message links'))
	def __unicode__(self):
		return str(self.message[:30])
	class Meta:
		db_table = 'SN_STATUS_MESSAGE'
		verbose_name = _('Status Message')
		verbose_name_plural = _("Status Messages")

class Comment(BaseModel):
	"""Comment Model
	FK: User
	MN: Like
	MN: Share
	MN: Files
	MN: Links
	MN: Tags
	Message
	Public"""
	user = models.ForeignKey(UserSocial,
				verbose_name = _('User'), help_text = _('User'))
	message = models.TextField(verbose_name = _('Comment'), help_text = _('Comment message'))
	like = models.ManyToManyField('Like', null=True, blank=True,
				verbose_name = _('Likes'), help_text = _('Likes'))
	share = models.ManyToManyField('StatusShare', null=True, blank=True,
				verbose_name = _('Shares'), help_text = _('Shares'))
	files = models.ManyToManyField('File', null=True, blank=True,
				verbose_name = _('Files'), help_text = _('Files'))
	links = models.ManyToManyField('Link', null=True, blank=True,
				verbose_name = _('Links'), help_text = _('Links'))
	tags = models.ManyToManyField('Tag', null=True, blank=True,
				verbose_name = _('Tags'), help_text = _('Tags'))
	isPublic = models.BooleanField(default=True)
	def __unicode__(self):
		return str(self.user) + ' - ' + str(self.message[:20])
	class Meta:
		db_table = 'SN_COMMENT'
		verbose_name = _('Comment')
		verbose_name_plural = _("Comments")

class Like(BaseModel):
	"""Like Model
	FK: User
	Number"""
	user = models.ForeignKey(UserSocial,
				verbose_name = _('User'), help_text = _('User'))
	number = models.IntegerField(default=0,
				verbose_name = _('Number'), help_text = _('Number'))
	def __unicode__(self):
		return str(self.user)
	class Meta:
		db_table = 'SN_LIKE'
		verbose_name = _('Like')
		verbose_name_plural = _("Likes")

class StatusShare(BaseModel):
	"""Status share model
	FK: User
	Message"""
	user = models.ForeignKey(UserSocial,
				verbose_name = _('User'), help_text = _('User'))
	message = models.TextField(null=True, blank=True,
				verbose_name = _('Message'), help_text = _('Message'))
	def __unicode__(self):
		return str(self.user)
	class Meta:
		db_table = 'SN_STATUS_SHARE'
		verbose_name= _('Status Share')
		verbose_name_plural = _("StatusShares")

class GroupStream(BaseModel):
	"""Group Stream Model
	FK: User
	FK: Account [optional]
	FK: Group [optional]
	FK: Message
	MN: Comments
	MN: Shares
	MN: Like
	PostId
	Source
	Public"""
	postId = models.BigIntegerField(verbose_name = _('Post Id'), help_text = _('Post identification'))
	user = models.ForeignKey(UserSocial,
				verbose_name = _('User'), help_text = _('User'))
	account = models.ForeignKey('Organization', null=True, blank=True, related_name='group_stream_account',
				verbose_name = _('Account'), help_text = _('Account name'))
	group = models.ForeignKey(GroupSys, null=True, blank=True,
				verbose_name = _('Group'), help_text = _('Group'))
	message = models.ForeignKey('StatusMessage',
				verbose_name = _('Message'), help_text = _('Message'))
	comments = models.ManyToManyField('Comment', null=True, blank=True,
				verbose_name = _('Comments'), help_text = _('Comments'))
	like = models.ManyToManyField('Like', null=True, blank=True,
				verbose_name = _('Likes'), help_text = _('Likes'))
	shares = models.ManyToManyField(StatusShare, null=True, blank=True,
				verbose_name = _('Shares'), help_text = _('Shares'))
	isPublic = models.BooleanField(default=False,
				verbose_name = _('Public'), help_text = _('Public'))
	source = models.CharField(max_length=10, choices=Choices.MSG_MEDIA, default=Constants.XIMPIA,
				verbose_name = _('Source'), help_text = _('Where stream came from'))
	def __unicode__(self):
		return str(self.user) + ' - ' + str(self.postId)
	class Meta:
		db_table = 'SN_STATUS_STREAM'
		ordering = ['-dateCreate']
		verbose_name = _('Status Stream')
		verbose_name_plural = _("Status Streams")

class GroupStreamPublic(BaseModel):
	"""Group Stream Public Model
	FK: PostId
	FK: UserMadePublic
	MN: SocialNetwork
	DateMadePublic"""
	postId = models.ForeignKey(GroupStream,
				verbose_name = _('Post Id'), help_text = _('Post identification'))
	socialNetwork = models.ManyToManyField(SocialNetwork,
				verbose_name = _('Social Network'), help_text = _('Social Network'))
	userMadePublic = models.ForeignKey(UserSocial,
				verbose_name = _('User Public Action'), help_text = _('User that made public message'))
	dateMadePublic = models.DateTimeField(auto_now_add=True,
				verbose_name = _('Date Made Public'), help_text = _('Date made public message'))
	def __unicode__(self):
		return str(self.postId)
	class Meta:
		db_table = 'SN_STATUS_STREAM_PUBLIC'
		verbose_name = _('Group Stream Public')
		verbose_name_plural = _("Group Streams Public")

class Tag(BaseModel):
	"""Tag Model
	Tag : CharField
	SystemTag : Boolean:False
	Popularity : Integer
	Public : Boolean:True"""
	name = models.CharField(max_length=30,
			verbose_name = _('Name'), help_text = _('Tag name'))
	type = models.ForeignKey('TagType', related_name='Tag_Type',
			verbose_name = _('Type'), help_text = _('Tag type'))
	popularity = models.IntegerField(default=1, null=True, blank=True,
			verbose_name = _('Popularity'), help_text = _('Popularity'))
	isPublic = models.BooleanField(default=True,
			verbose_name = _('Public'), help_text = _('Is tag public?'))
	def __unicode__(self):
		return str(self.name)
	def getText(self):
		return self.name
	class Meta:
		db_table = 'SN_TAG'
		verbose_name = _('Tag')
		verbose_name_plural = _("Tags")
		ordering = ['-popularity']

class TagType(BaseModel):
	"""Tag Type Model"""
	type = models.CharField(max_length=30,
			verbose_name = _('Type'), help_text = _('Tag type'))
	isPublic = models.BooleanField(default=True,
			verbose_name = _('Public'), help_text = _('Is tag type public?'))
	def __unicode__(self):
		return str(self.type)
	class Meta:
		db_table = 'SN_TAG_TYPE'
		verbose_name = _('Tag Type')
		verbose_name_plural = _("Tag Types")

class Link(BaseModel):
	"""Link Model
	MN: Tags
	Url
	UrlShort
	UrlTitle
	UrlDescription
	Summary
	ImgUrl
	NumberShared
	Domain"""
	url = models.URLField(db_index=True,
			verbose_name = _('Url'), help_text = _('Link url'))
	urlShort = models.URLField(db_index=True,
			verbose_name = _('Url Shorted'), help_text = _('Url in short format'))
	urlTitle = models.CharField(max_length=200, null=True, blank=True,
			verbose_name = _('Url Title'), help_text = _('Title for url'))
	urlDescription = models.CharField(max_length=300, null=True, blank=True,
			verbose_name = _('Url Description'), help_text = _('Description for url'))
	summary = models.CharField(max_length=200, null=True, blank=True,
			verbose_name = _('Url Summary'), help_text = _('Summary'))
	imgUrl = models.URLField(null=True, blank=True,
			verbose_name = _('Image Url'), help_text = _('Image url for icon'))
	numberShared = models.IntegerField(default=1,
			verbose_name = _('Share Counter'), help_text = _('Number shares for url'))
	domain = models.CharField(max_length=100, db_index=True, null=True, blank=True,
			verbose_name = _('Domain'), help_text = _('Domain'))
	tags = models.ManyToManyField('Tag', null=True, blank=True,
			verbose_name = _('Url Tags'), help_text = _('Tags for link'))
	isPublic = models.BooleanField(default=False,
			verbose_name = _('Public'), help_text = _('Public?'))
	def __unicode__(self):
		return _('Link') + ' ' + str(self.id)
	class Meta:
		db_table = 'SN_LINK'
		verbose_name = _('Link')
		verbose_name_plural = _("Links")
		ordering = ['-numberShared']

class Version(BaseModel):
	"""Version for any object"""
	versionName = models.CharField(max_length=20, null=True, blank=True,
			verbose_name = _('Version Name'), help_text = _('Name for version'))
	def __unicode__(self):
		return str(self.pk)
	class Meta:
		db_table = 'SN_VERSION'
		verbose_name = _('Version')
		verbose_name_plural = _("Versions")

class ProfileDetail(BaseModel):
	"""Profile information for site, im, etc..."""
	mode = models.ForeignKey('UserParam', limit_choices_to={'mode__exact': 'mode'}, related_name='profile_detail_mode',
				verbose_name = _('Mode'), help_text = _('Mode: Site, Im, etc...'))
	value = models.CharField(max_length=50,
				verbose_name = _('Value'), help_text = _('Value'))
	def __unicode__(self):
		return str(self.mode)
	class Meta:
		db_table = 'SN_USER_PROFILE_DETAIL'
		verbose_name = _('Profile Detail')
		verbose_name_plural = _("Profiles Detail")

class UserProfile(BaseModel):
	"""Profile for users"""
	userAccount = models.ForeignKey('UserAccount', unique=True,
				verbose_name = _('User Account'), help_text = _('User account'))
	homeTown = models.CharField(max_length=100, null=True, blank=True,
				verbose_name = _('Home Town'), help_text = _('Home Town'))
	politicalViews = models.CharField(max_length=50, null=True, blank=True,
				verbose_name = _('Political Views'), help_text = _('Political Views'))
	religiousViews = models.CharField(max_length=50, null=True, blank=True,
				verbose_name = _('Religious Views'), help_text = _('Religious Views'))
	sex = models.CharField(max_length=20, choices=Choices.SEX, null=True, blank=True,
				verbose_name = _('Sex'), help_text = _('Sex'))
	bio = models.TextField(null=True, blank=True,
				verbose_name = _('Biography'), help_text = _('Biography'))
	relationship = models.CharField(max_length=20, choices=Choices.RELATIONSHIP, null=True, blank=True,
				verbose_name = _('Relationship'), help_text = _('Relationship')) 
	favQuotes = models.CharField(max_length=500, null=True, blank=True,
				verbose_name = _('Favorite Quotes'), help_text = _('Favorite Quotes'))
	activities = models.CharField(max_length=500, null=True, blank=True,
				verbose_name = _('Activities'), help_text = _('Activities'))
	interests = models.CharField(max_length=500, null=True, blank=True,
				verbose_name = _('Interests'), help_text = _('Interests'))
	music = models.CharField(max_length=500, null=True, blank=True,
				verbose_name = _('Music'), help_text = _('Tell about your favorite music'))
	books = models.CharField(max_length=500, null=True, blank=True,
				verbose_name = _('Books'), help_text = _('Favorite books'))
	movies = models.CharField(max_length=500, null=True, blank=True,
				verbose_name = _('Movies'), help_text = _('Favorite movies'))
	television = models.CharField(max_length=500, null=True, blank=True,
				verbose_name = _('Television'), help_text = _('Favorite Television Shows'))
	comments = models.ManyToManyField('Comment', null=True, blank=True,
				verbose_name = _('Comments'), help_text = _('Comments'))
	likes = models.ManyToManyField('Like', null=True, blank=True,
				verbose_name = _('Likes'), help_text = _('Likes'))
	shares = models.ManyToManyField('StatusShare', null=True, blank=True,
				verbose_name = _('Shares'), help_text = _('Shares'))
	def __unicode__(self):
		return str(self.userAccount)
	class Meta:
		db_table = 'SN_PROFILE'
		verbose_name = _('Profile')
		verbose_name_plural = _("Profiles")

class Organization(BaseModel):
	"""Organization Model"""
	invitedByUser = models.ForeignKey(UserSys, null=True, blank=True,
			verbose_name = _('Invited By User'), help_text = _('Invited by user'))
	invitedByOrg = models.ForeignKey('Organization', 'account', null=True, blank=True,
			verbose_name = _('Invited By Organization'), help_text = _('Invited by Organization'))
	affiliate = models.ForeignKey('Affiliate', null=True, blank=True, related_name='organization_affiliate',
			verbose_name = _('Affiliate'), help_text = _('Affiliate'))
	account = models.CharField(max_length=20, unique=True, null=True, blank=True,
			verbose_name = _('Account'), help_text = _('Account name'))
	accountType = models.CharField(max_length=15, choices=Choices.ACCOUNT_TYPE, default=Choices.ACCOUNT_TYPE_ORDINARY,
			verbose_name = _('Account Type'), help_text = _('Account type: ordinary, promotion, etc...'))
	relatedToUp = models.ManyToManyField('self', related_name='org_up', null=True, blank=True,
			verbose_name = _('Parent Organization'), help_text = _('Parent organization'))
	relatedToDown = models.ManyToManyField('self', related_name='org_down', null=True, blank=True,
			verbose_name = _('Child Organization'), help_text = _('Child Organization'))
	domain = models.CharField(max_length=50, unique=True,
			verbose_name = _('Domain'), help_text = _('Domain'))
	name = models.CharField(max_length=30,
			verbose_name = _('Name'), help_text = _('Name'))
	brand = models.CharField(max_length=20, null=True, blank=True,
			verbose_name = _('Brand Name'), help_text = _('Brand Name'))
	industries = models.ManyToManyField('GroupSocial', limit_choices_to={'industry': True}, related_name='organization_industries',
			verbose_name = _('Industries'), help_text = _('Industries'))
	taxes = models.ManyToManyField('TaxType', through='TaxOrganization', null=True, blank=True,
			verbose_name = _('Taxes'), help_text = _('Taxes'))
	addresses = models.ManyToManyField('Address', through='AddressOrganization', related_name='organization_addresses', 
			verbose_name = _('Addresses'), help_text = _('Addresses'))
	phone = models.CharField(max_length=20, null=True, blank=True,
			verbose_name = _('Phone'), help_text = _('Phone'))
	fax = models.CharField(max_length=20, null=True, blank=True,
			verbose_name = _('Fax'), help_text = _('Fax'))
	groups = models.ManyToManyField('GroupSocial', through='OrganizationGroup',
			verbose_name = _('Groups'), help_text = _('Organization Groups'))
	socialNetworks = models.ManyToManyField('SocialNetwork', through='SocialNetworkOrganization',
			verbose_name = _('Social Networks'), help_text = _('Social Networks'))
	description = models.CharField(max_length=500, null=True, blank=True,
			verbose_name = _('Description'), help_text = _('Description'))
	subscriptionStatus = models.CharField(max_length=10, choices= Choices.SUBSCRIPTION, default=Choices.SUBSCRIPTION_VALID,
			verbose_name = _('Subscription Status'), help_text = _('Subscription status: valid, etc...'))
	isValidated = models.BooleanField(default=False,
			verbose_name = _('Validated'), help_text = _('Validated'))
	filesQuota = models.IntegerField(null=True, blank=True,
			verbose_name = _('Files Quota'), help_text = _('Maximum file size for organization'))
	def __unicode__(self):
		return str(self.account)
	class Meta:
		db_table = 'SN_ORGANIZATION'
		verbose_name = _('Organization')
		verbose_name_plural = _("Organizations")

class OrganizationGroup(BaseModel):
	"""Organization Group Model (Departments)
	FK: Group->GroupSocial
	FK: Organization
	MN: RelatedToUp->self
	MN: RelatedToDown->self
	MN+: SocialNetworks->SocialNetworkOrganizationGroup"""
	group = models.ForeignKey('GroupSocial',
			verbose_name = _('Group'), help_text = _('Group'))
	organization = models.ForeignKey('Organization',
			verbose_name = _('Organization'), help_text = _('Organization'))
	relatedToUp = models.ManyToManyField('self', related_name='org_group_relate_up', null=True, blank=True,
			verbose_name = _('Parent Group'), help_text = _('Parent organization group'))
	relatedToDown = models.ManyToManyField('self', related_name='org_group_relate_down', null=True, blank=True,
			verbose_name = _('Child Group'), help_text = _('Child organization group'))
	socialNetworks = models.ManyToManyField('SocialNetwork', through='SocialNetworkOrganizationGroup',
			verbose_name = _('Social Networks'), help_text = _('Social Networks'))
	skills = models.ManyToManyField('Skill', through='SkillGroup',  null=True, blank=True,
			verbose_name = _('Skills'), help_text = _('Skills')) 
	def __unicode__(self):
		return str(self.group)
	class Meta:
		db_table = 'SN_ORGANIZATION_group'
		verbose_name = _('Organization Group')
		verbose_name_plural = _("Organization Groups")

class UserAccount(BaseModel):
	"""UserAccount Model
	FK: User->UserDetail
	MN: UserAccountRelations
	MN: Industries
	MN+: Taxes
	MN: RelatedToUp
	MN: RelatedToDown
	MN+: Identifiers
	MN+: Skills
	Manager
	EmployeeId
	NickName
	Smoker
	EthnicRaceCode
	SSN
	NumberLisence
	LisenceExpDate
	MilitaryService
	Workstation
	[...]"""
	user = models.ForeignKey('UserDetail',
				verbose_name = _('User'), help_text = _('User'))
	invitedByUser = models.ForeignKey(UserSys, null=True, blank=True,
				verbose_name = _('Invited by User'), help_text = _('Invited by user'))
	invitedByOrg = models.ForeignKey('Organization', 'account', null=True, blank=True,
				verbose_name = _('Invited by Organization'), help_text = _('Invited for organization'))
	affiliate = models.ForeignKey('Affiliate', null=True, blank=True, related_name='user_affiliate',
				verbose_name = _('Affiliate'), help_text = _('Affiliate'))
	contact = models.ForeignKey('ContactDetail',
				verbose_name = _('Contact'), help_text = _('Contact'))
	userRelations = models.ManyToManyField('UserAccountRelation', null=True, blank=True, related_name='user_account_relations', 
				verbose_name = _('User Relations'), help_text = _('User Relations : Company you belong, other companies as provider, etc...'))	# For example, relation with your company and relation with company where you work on project
	isManager = models.BooleanField(default=False,
				verbose_name = _('Manager'), help_text = _('Am I Manager?'))
	employeeId = models.CharField(max_length=30, null=True, blank=True,
				verbose_name = _('Employee Id'), help_text = _('Identification for employee'))
	taxes = models.ManyToManyField('TaxType', through='TaxUserAccount', null=True, blank=True,
				verbose_name = _('Taxes'), help_text = _('Taxes'))
	relatedToUp = models.ManyToManyField('self', related_name='organization_related_up', null=True, blank=True,
				verbose_name = _('Parent Organization'), help_text = _('Parent Organization'))
	relatedToDown = models.ManyToManyField('self', related_name='organization_related_down', null=True, blank=True,
				verbose_name = _('Child Organization'), help_text = _(''))
	isSmoker = models.BooleanField(default=False,
				verbose_name = _('Smoker'), help_text = _('Smoker'))
	ethnicRaceCode = models.CharField(max_length=20, choices=Choices.ETHNIC, null=True, blank=True,
				verbose_name = _('Ethnic Race Code'), help_text = _('Ethnic Race Code'))
	ssn = models.CharField(max_length=30, null=True, blank=True,
				verbose_name = _('Social Security Number'), help_text = _('Social Security Number'))
	identifiers = models.ManyToManyField('UserAccountIdentifier', through='IdentifierUserAccount', null=True, blank=True,
				verbose_name = _('Identifiers'), help_text = _('Identifiers'))
	numberLisence = models.CharField(max_length=30, null=True, blank=True,
				verbose_name = _('License Number'), help_text = _('License Number'))
	lisenceExpDate = models.DateField(null=True, blank=True,
				verbose_name = _('License Expiration Date'), help_text = _('License Expiration Date'))
	militaryService = models.CharField(max_length=20, choices=Choices.MILITARY, null=True, blank=True,
				verbose_name = _('Military Service'), help_text = _('Military Service'))
	workStation = models.CharField(max_length=30, null=True, blank=True, 
				verbose_name = _('Workstation'), help_text = _('Workstation'))
	skills = models.ManyToManyField('Skill', through='SkillUserAccount',  null=True, blank=True,
				verbose_name = _('Skills'), help_text = _('Skills'))
	isPublic = models.BooleanField(default=True,
				verbose_name = _('Public'), help_text = _('Public'))
	isCVPublic = models.BooleanField(default=True,
				verbose_name = _('CV Public'), help_text = _('CV Public'))
	description = models.CharField(max_length=500, null=True, blank=True,
				verbose_name = _('Description'), help_text = _('Description'))
	linkedInProfile = models.CharField(max_length=255, null=True, blank=True,
				verbose_name = _('LinkedIn Profile'), help_text = _('LinkedIn Profile'))
	def __unicode__(self):
		return str(self.user)
	class Meta:
		db_table = 'SN_USER_ACCOUNT'
		verbose_name = _('UserAccount')
		verbose_name_plural = _("UserAccounts")

class IdentifierUserAccount(BaseModel):
	userAccountIdentifier = models.ForeignKey('UserAccountIdentifier',
				verbose_name = _('UserAccount Identifier'), help_text = _('UserAccount Identifier'))
	userAccount = models.ForeignKey('UserAccount',
				verbose_name = _('UserAccount'), help_text = _('UserAccount'))
	identifier = models.CharField(max_length=30,
				verbose_name = _('Identifier'), help_text = _('Identifier'))
	def __unicode__(self):
		return str(self.identifier)
	class Meta:
		db_table = 'SN_USER_ACCOUNT_identifiers'
		verbose_name = _('Identifier for User Accounts')
		verbose_name_plural = _("Identifiers for User Account")

class UserAccountIdentifier(BaseModel):
	type = models.CharField(max_length=20, null=True, blank=True,
			verbose_name = _('Type'), help_text = _('Type'))
	def __unicode__(self):
		return str(self.type)
	class Meta:
		db_table = 'SN_USER_ACCOUNT_IDENTIFIER'
		verbose_name = _('User Account Identifier')
		verbose_name_plural = _("UserAccount Identifiers")

class Skill(BaseModel):
	"""Skills, either technical or """
	catCode = models.ForeignKey('UserParam', limit_choices_to={'mode__exact': 'skill_cat'}, related_name='skill_cat_code',
				verbose_name = _('Skill'), help_text = _('Employee skill'))
	skillName = models.CharField(max_length=50,
				verbose_name = _('Skill Name'), help_text = _('Name of the employee skill'))
	def __unicode__(self):
		return str(self.catCode) + '-' + str(self.skillName)
	class Meta:
		db_table = 'SN_SKILL'
		verbose_name = _('Skill')
		verbose_name_plural = _("Skills")

class SkillUserAccount(BaseModel):
	"""Relationship between userAccount and skills."""
	skill = models.ForeignKey('Skill',
				verbose_name = _('Skill'), help_text = _('Skill'))
	userAccount = models.ForeignKey('UserAccount',
				verbose_name = _('UserAccount'), help_text = _('UserAccount'))
	numberMonths = models.IntegerField(null=True, blank=True,
				verbose_name = _('Number Months'), help_text = _('Number Months'))
	rating = models.IntegerField(null=True, blank=True,
				verbose_name = _('Rating'), help_text = _('Rating'))
	numberVotes = models.IntegerField(null=True, blank=True,
				verbose_name = _('Number Votes'), help_text = _('Number Votes'))
	isPublic = models.BooleanField(default=True,
				verbose_name = _('Public'), help_text = _('Is public?'))
	def __unicode__(self):
		return str(self.skill) + ' ' + str(self.userAccount)
	class Meta:
		db_table = 'SN_USER_ACCOUNT_skill'
		verbose_name = _('Skill for User Account')
		verbose_name_plural = _("Skills for User Accounts")

class SkillGroup(BaseModel):
	"""Relationship between organization group and skills."""
	skill = models.ForeignKey('Skill',
				verbose_name = _('Skill'), help_text = _('Skill'))
	group = models.ForeignKey('OrganizationGroup',
				verbose_name = _('Organization Group'), help_text = _('Organization Group'))
	numberMonths = models.IntegerField(null=True, blank=True,
				verbose_name = _('Number Months'), help_text = _('Number Months'))
	rating = models.IntegerField(null=True, blank=True,
				verbose_name = _('Rating'), help_text = _('Rating'))
	numberVotes = models.IntegerField(null=True, blank=True,
				verbose_name = _('Number Votes'), help_text = _('Number Votes'))
	isPublic = models.BooleanField(default=True,
				verbose_name = _('Public'), help_text = _('Is public?'))
	def __unicode__(self):
		return str(self.skill) + ' ' + str(self.group)
	class Meta:
		db_table = 'SN_ORGANIZATION_group_skill'
		verbose_name = _('Skill for Group')
		verbose_name_plural = _('Skills for Group')

class Industry(BaseModel):
	group = models.ForeignKey('GroupSocial', related_name='industry_group',
				verbose_name = _('Group'), help_text = _('Group for Industry: All industries are treated like groups of people'))
	def __unicode__(self):
		return str(self.group)
	class Meta:
		db_table = 'SN_INDUSTRY'
		verbose_name = _('Industry')
		verbose_name_plural = _("Industries")

class AddressOrganization(BaseModel):
	"""Address Organization Model"""
	addressType = models.CharField(max_length=20, choices=Choices.ADDRESS_TYPE,
			verbose_name = _('Address Type'), help_text = _('Address type'))
	organization = models.ForeignKey('Organization',
			verbose_name = _('Organization'), help_text = _('Organization'))
	address = models.ForeignKey('social_network.Address',
			verbose_name = _('Address'), help_text = _('Address'))
	def __unicode__(self):
		return str(self.pk) + ' ' + str(self.addressType) + ' ' + str(self.organization)
	class Meta:
		db_table = 'SN_ORGANIZATION_address'
		verbose_name = _('Address for Organization')
		verbose_name_plural = _('Addresses for Organization')

class SocialNetworkOrganization(BaseModel):
	"""Social Network Organization Model
	FK: Organization
	FK: SocialNetwork
	Account
	Password"""
	organization = models.ForeignKey('Organization')
	socialNetwork = models.ForeignKey('SocialNetwork')
	token = models.CharField(max_length=255)
	tokenSecret = models.CharField(max_length=255, null=True, blank=True)
	def __unicode__(self):
		return str(self.account)
	class Meta:
		db_table = 'SN_ORGANIZATION_socialNetwork'
		verbose_name = _('Social Network for Organization')
		verbose_name_plural = _('Social Networks for Organization')

class TaxType(BaseModel):
	type = models.CharField(max_length=100,
			verbose_name = _('Type'), help_text = _('Type'))
	def __unicode__(self):
		return str(self.type)
	class Meta:
		db_table = 'SN_TAX_TYPE'
		verbose_name = _('Tax Type')
		verbose_name_plural = _('TaxTypes')

class TaxOrganization(BaseModel):
	taxType = models.ForeignKey('TaxType',
				verbose_name = _('Tax Type'), help_text = _('Type of tax'))
	organization = models.ForeignKey('Organization',
				verbose_name = _('Organization'), help_text = _('Organization'))
	taxCode = models.CharField(max_length=50,
				verbose_name = _('Tax Code'), help_text = _('Tax Code'))
	def __unicode__(self):
		return str(self.taxCode)
	class Meta:
		db_table = 'SN_ORGANIZATION_tax'
		verbose_name = _('Tax for Organization')
		verbose_name_plural = _('Taxes for Organization')

class TaxUserAccount(BaseModel):
	taxType = models.ForeignKey('TaxType',
				verbose_name = _('Tax Type'), help_text = _('Tax Type'))
	userAccount = models.ForeignKey('UserAccount',
				verbose_name = _('User Account'), help_text = _('User Account'))
	taxCode = models.CharField(max_length=50,
				verbose_name = _('Tax Code'), help_text = _('Tax Code'))
	def __unicode__(self):
		return str(self.taxCode)
	class Meta:
		db_table = 'SN_USER_ACCOUNT_tax'
		verbose_name = _('Tax for User Account')
		verbose_name_plural = _('Taxes for User Account')

class SocialNetworkOrganizationGroup(BaseModel):
	organizationGroup = models.ForeignKey('OrganizationGroup',
				verbose_name = _('Organization Group'), help_text = _('Organization Group'))
	socialNetwork = models.ForeignKey('SocialNetwork',
				verbose_name = _('Social Network'), help_text = _('Social Network'))
	token = models.CharField(max_length=255,
				verbose_name = _('Token'), help_text = _('Token'))
	tokenSecret = models.CharField(max_length=255, null=True, blank=True,
				verbose_name = _('Token Secret'), help_text = _('Token Secret'))
	def __unicode__(self):
		return str(self.account)
	class Meta:
		db_table = 'SN_ORGANIZATION_group_socialNetwork'
		verbose_name = _('Social Network for Organization Group')
		verbose_name_plural = _('Social Networks for Organization Group')

class UserAccountRelation(BaseModel):
	"""UserAccount Relation Model.
	FK: Organization
	FK: OrganizationGroup
	FK: UserAccountContract
	FK: SubcontractOrganization"""
	organization = models.ForeignKey('Organization', related_name='userAccountrelation_organization',
				verbose_name = _('Organization'), help_text = _('Organization'))
	organizationGroup = models.ForeignKey('OrganizationGroup', related_name='userAccountrelation_group',
				verbose_name = _('Organization Group'), help_text = _('Organization Group'))
	contract = models.ForeignKey('UserAccountContract', related_name='userAccountrelation_contract',
				verbose_name = _('Contract'), help_text = _('Contract'))
	subcontractOrganization = models.ForeignKey('Organization', null=True, blank=True,
				verbose_name = _('Subcontract Organization'), help_text = _('Organization that is subcontracted'))
	isPublic = models.BooleanField(default=False,
				verbose_name = _('Public'), help_text = _('Is public?'))
	def __unicode__(self):
		return str(self.organization) + ' ' + str(self.contract)
	class Meta:
		db_table = 'SN_USER_ACCOUNT_RELATION'
		verbose_name = _('User Account Relation')
		verbose_name_plural = _('User Account Relations')

class UserAccountContract(BaseModel):
	"""UserAccount Contract Model
	Status : Choices.STATUS
	Schedule : Choices.SCHEDULE
	ContractType : Choices.CONTRACT_TYPE
	JobTitle"""
	status = models.CharField(max_length=20, choices=Choices.STATUS,
			verbose_name = _('Status'), help_text = _('Status: Employee, self-contractor, ...'))
	schedule = models.CharField(max_length=20, choices=Choices.SCHEDULE,
			verbose_name = _('Schedule'), help_text = _('Schedule: Full time or part time'))
	contractType = models.CharField(max_length=20, choices=Choices.CONTRACT_TYPE,
			verbose_name = _('Contract Type'), help_text = _('Contract Type: regular or part time'))
	jobTitle = models.CharField(max_length=50,
			verbose_name = _('Job Title'), help_text = _('Job Title'))
	def __unicode__(self):
		return str(self.status) + ' - ' + str(self.schedule) + ' - ' + str(self.contractType) + ' - ' + str(self.jobTitle)
	class Meta:
		db_table = 'SN_USER_ACCOUNT_CONTRACT'
		verbose_name = _('User Account Contract')
		verbose_name_plural = _('User Account Contracts')

class Invitation(BaseModel):
	"""Invitation Model
	FK: User
	FK: Contact"""
	fromUser = models.ForeignKey(UserSys,
				verbose_name = _('From User'), help_text = _('Invitation from user'))
	fromAccount = models.ForeignKey('Organization', 'account', null=True, blank=True,
				verbose_name = _('From Account'), help_text = _('Invitation from account name'))
	contact = models.ForeignKey('Contact', null=True, blank=True,
				verbose_name = _('Contact'), help_text = _('Invitation for contact'))
	invitationCode = models.CharField(max_length=10, unique=True,
				verbose_name = _('Inivitation Code'), help_text = _('Invitation Code'))
	email = models.EmailField(null=True, blank=True,
				verbose_name = _('Email'), help_text = _('Email'))
	mobile = models.CharField(max_length=15, null=True, blank=True,
				verbose_name = _('Mobile Phone'), help_text = _('Mobile Phone'))
	contactMethod = models.CharField(max_length=15, choices=Choices.MSG_MEDIA, null=True, blank=True,
				verbose_name = _('Contact Method'), help_text = _('Contact Method for invitation'))
	status = models.CharField(max_length=10, choices=Choices.INVITATION_STATUS, default=Constants.PENDING,
				verbose_name = _('Status'), help_text = _('Invitation status : pending, used.'))
	number = models.PositiveSmallIntegerField(default=1,
				verbose_name = _('Number'), help_text = _('Invitation Number'))
	affiliate = models.ForeignKey('Affiliate', null=True, blank=True,
				verbose_name = _('Affiliate'), help_text = _('Affiliate'))
	message = models.CharField(max_length=200, null=True, blank=True,
				verbose_name = _('Message'), help_text = _('Message'))
	type = models.CharField(max_length=15, choices=Choices.INVITATION_TYPE, default=Choices.INVITATION_TYPE_ORDINARY,
				verbose_name = _('Type'), help_text = _('Invitation Type : Ordinary, promotion.'))
	domain = models.CharField(max_length=100, null=True, blank=True,
				verbose_name = _('Domain'), help_text = _('Domain'))
	def __unicode__(self):
		return str(self.fromUser) + ' ' + str(self.invitationCode)
	class Meta:
		db_table = 'SN_INVITATION'
		verbose_name = _('Invitation')
		verbose_name_plural = _('Invitations')

class Affiliate(BaseModel):
	"""Affiliate Model"""
	affiliateId = models.PositiveIntegerField(unique=True,
				verbose_name = _('Affiliate Id'), help_text = _('Affiliate identity'))
	organization = models.ForeignKey('Organization', null=True, blank=True, related_name='affiliate_organization',
				verbose_name = _('Organization'), help_text = _('Organization'))
	userAccount = models.ForeignKey('UserAccount', null=True, blank=True, related_name='affiliate_userAccount',
				verbose_name = _('User Account'), help_text = _('User Account'))
	def __unicode__(self):
		return str(self.organization)
	class Meta:
		db_table = 'SN_AFFILIATE'
		verbose_name = _('Affiliate')
		verbose_name_plural = _('Affiliates')

class TagUserTotal(BaseModel):
	"""Tags for User in all Objects Model"""
	user = models.ForeignKey(UserSys,
			verbose_name = _('User'), help_text = _('User'))
	userSocial = models.ForeignKey('UserSocial',
			verbose_name = _('Ximpia User'), help_text = _('Ximpia User'))
	tag = models.ForeignKey(Tag,
			verbose_name = _('Tag'), help_text = _('Tag'))
	number = models.IntegerField(default=1,
			verbose_name = _('Number'), help_text = _('Number'))
	def __unicode__(self):
		return str(self.pk)
	class Meta:
		db_table = 'SN_TAG_USER_TOTAL'
		ordering = ['-number','-dateModify']
		verbose_name= _('Tag for User')
		verbose_name_plural = _('Tags for User')

class LinkUserTotal(BaseModel):
	"""Links for User in all Objects Model"""
	user = models.ForeignKey(UserSys, 
			verbose_name = _('User'), help_text = _('User'))
	userSocial = models.ForeignKey('UserSocial',
			verbose_name = _('Ximpia User'), help_text = _('Ximpia User'))
	link = models.ForeignKey('Link',
			verbose_name = _('Link'), help_text = _('Link'))
	number = models.IntegerField(default=1,
			verbose_name = _('Number'), help_text = _('Number'))
	def __unicode__(self):
		return str(self.pk)
	class Meta:
		db_table = 'SN_LINK_USER_TOTAL'
		ordering = ['-number','-dateModify']
		verbose_name = _('Link for User')
		verbose_name_plural = _("Links for User")

class SubscriptionDaily(BaseModel):
	"""Subscriptions for apps"""
	userAccount = models.ForeignKey('UserAccount', null=True, blank=True,
			verbose_name = _('User Account'), help_text = _('User Account'))
	organization = models.ForeignKey('Organization', null=True, blank=True,
			verbose_name = _('Organization'), help_text = _('Organization'))
	app = models.ForeignKey('Application',
			verbose_name = _('Application'), help_text = _('Application'))
	numberUsers = models.PositiveIntegerField(verbose_name = _('Number Users'), help_text = _('Number Users'))
	date = models.DateField(auto_now_add=True, verbose_name = _('Date'), help_text = _('Date'))
	def __unicode__(self):
		return str(self.app)
	class Meta:
		db_table = 'SN_SUBSCRIPTION_DAY'
		verbose_name = _('Subscription Daily')
		verbose_name_plural = _('Subscriptions Daily')

class Subscription(BaseModel):
	"""Subscriptions for apps"""
	userAccount = models.ForeignKey('UserAccount', null=True, blank=True,
				verbose_name = _('User Account'), help_text = _('User Account'))
	organization = models.ForeignKey('Organization', null=True, blank=True,
				verbose_name = _('Organization'), help_text = _('Organization'))
	app = models.ForeignKey('Application',
				verbose_name = _('Application'), help_text = _('Application'))
	users = models.ManyToManyField(UserSys,
				verbose_name = _('Users'), help_text = _('Users'))
	subscriptionStatus = models.CharField(max_length=10, choices= Choices.SUBSCRIPTION, default=Choices.SUBSCRIPTION_TRIAL,
				verbose_name = _('Subscription Status'), help_text = _('Subscription status : pending, used'))
	def __unicode__(self):
		return str(self.app)
	class Meta:
		db_table = 'SN_SUBSCRIPTION'
		verbose_name = _('Subscription')
		verbose_name_plural = _('Subscriptions')

class SubscriptionItemMonth(BaseModel):
	"""Subscription items billed monthly"""
	userAccount = models.ForeignKey('UserAccount', null=True, blank=True,
				verbose_name = _('User Account'), help_text = _('User Account'))
	organization = models.ForeignKey('Organization', null=True, blank=True,
				verbose_name = _('Organization'), help_text = _('Organization'))
	date = models.DateField(auto_now_add=True, 
			verbose_name = _('Date'), help_text = _('Date'))
	number = models.PositiveIntegerField(verbose_name = _('Number'), help_text = _('Number'))
	item = models.CharField(max_length=20, choices=Choices.SUBSCRIPTION_ITEMS,
			verbose_name = _('Item'), help_text = _('Item'))
	def __unicode__(self):
		return str(self.pk)
	class Meta:
		db_table = 'SN_SUBSCRIPTION_ITEM_MONTH'
		verbose_name = _('Subscription Item per Month')
		verbose_name_plural = _('Subscription Items per Month')

class Application(BaseModel):
	"""Applications"""
	code = models.CharField(max_length=20,
		verbose_name = _('Code'), help_text = _('Application code'))
	name = models.CharField(max_length=30,
		verbose_name = _('Name'), help_text = _('Application name'))
	developer = models.ForeignKey('UserAccount', null=True, blank=True,
		verbose_name = _('Developer'), help_text = _('Developer'))
	developerOrg = models.ForeignKey('Organization', null=True, blank=True,
		verbose_name = _('Organization'), help_text = _('Developer organization'))
	def __unicode__(self):
		return str(self.name)
	class Meta:
		db_table = 'SN_APPLICATION'
		verbose_name = _('Application')
		verbose_name_plural = _('Applications')

class Notification(BaseModel):
	"""Notifications"""
	owner = models.ForeignKey('UserSocial', related_name='notification_owner',
			verbose_name = _('Owner'), help_text = _('Owner'))
	content = models.CharField(max_length=200,
			verbose_name = _('Content'), help_text = _('Notification content'))
	def __unicode__(self):
		return str(self.pk)
	class Meta:
		db_table = 'SN_NOTIFICATION'
		ordering = ['-dateCreate']
		verbose_name = _('Notification')
		verbose_name_plural = _('Notifications')

class XmlMessage(BaseModel):
	"""XML Message"""
	name = models.CharField(max_length=255,
			verbose_name = _('Name'), help_text = _('Code name of XML'))
	lang = models.CharField(max_length=2, choices=Choices.LANG, default=Choices.LANG_ENGLISH,
			verbose_name = _('Language'), help_text = _('Language for xml'))
	body = models.TextField(verbose_name = _('Xml Content'), help_text = _('Xml content'))
	def __unicode__(self):
		return str(self.name)
	class Meta:
		db_table = 'SN_XML_MESSAGE'
		verbose_name = _('Xml Message')
		verbose_name_plural = _('Xml Messages')

class SignupData(BaseModel):
	"""SignUp Data"""
	invitationByUser = models.ForeignKey(UserSys, blank=True, null=True,
			verbose_name = _('Invited by user'), help_text = _('User that sent invitation'))
	invitationByOrg = models.ForeignKey('Organization', 'account', null=True, blank=True,
			verbose_name = _('Invited by account'), help_text = _('Organization that sent invitation'))
	user = models.CharField(max_length=30, unique=True,
			verbose_name = _('User'), help_text = _('User'))
	activationCode = models.PositiveSmallIntegerField(verbose_name = _('Activation Code'), help_text = _('Activation code'))
	invitationType = models.CharField(max_length=15, choices=Choices.INVITATION_TYPE, default=Choices.INVITATION_TYPE_ORDINARY,
			verbose_name = _('Invitation Type'), help_text = _('Type of invitation'))
	data = models.TextField(verbose_name = _('Data'), help_text = _('Data'))
	def __unicode__(self):
		return str(self.user)
	class Meta:
		db_table = 'SN_SIGNUP_DATA'
		verbose_name = _('Signup Data')
		verbose_name_plural = _('Signup Data')


class File(BaseModel):
	"""File Model. Must supply userAccount, organization+group"""
	name = models.CharField(max_length=200, unique=True,
			verbose_name = _('File Name'), help_text = _('File Name'))
	uploadedBy = models.ForeignKey('social_network.UserAccount',
			verbose_name = _('Uploaded By'), help_text = _('Uploaded By'))
	accessReadOrganizations = models.ManyToManyField('social_network.Organization', null=True, blank=True, related_name='file_read_org',
			verbose_name = _('Read Access Orgs'), help_text = _('Organizations that have read access'))
	accessReadGroups = models.ManyToManyField('social_network.OrganizationGroup', null=True, blank=True, related_name='file_read_groups',
			verbose_name = _('Read Access Groups'), help_text = _('Groups that have read access'))
	accessReadUserAccounts = models.ManyToManyField('social_network.UserAccount', related_name='file_read_userAccounts', null=True, blank=True,
			verbose_name = _('Read Access User Accounts'), help_text = _('User Accounts that have read access to the file'))
	accessWriteOrganizations = models.ManyToManyField('social_network.Organization', null=True, blank=True, related_name='file_write_org',
			verbose_name = _('Write Access Orgs'), help_text = _('Organizations that have write access to the file'))
	accessWriteGroups = models.ManyToManyField('social_network.OrganizationGroup', null=True, blank=True, related_name='file_write_groups',
			verbose_name = _('Write Access Groups'), help_text = _('Groups that have write access to the file'))
	accessWriteUserAccounts = models.ManyToManyField('social_network.UserAccount', related_name='file_write_userAccounts', null=True, blank=True,
			verbose_name = _('Write Access User Accounts'), help_text = _('User Accounts that have write access permission to file'))
	versions = models.ManyToManyField('social_network.Version', through='FileVersion', related_name='file_versions',
			verbose_name = _('File Versions'), help_text = _('Versions for the file'))
	latestVersion = models.PositiveIntegerField(default=1,
			verbose_name = _('Latest Version'), help_text = _('Latest Version'))
	title = models.CharField(max_length=200, null=True, blank=True,
			verbose_name = _('File Title'), help_text = _('File Title'))
	description = models.TextField(null=True, blank=True,
			verbose_name = _('File Description'), help_text = _('File Description'))
	type = models.CharField(max_length=50, choices=Choices.FILE_TYPE,
			verbose_name = _('File Type'), help_text = _('File Type'))
	tags = models.ManyToManyField('social_network.Tag', null=True, blank=True,
			verbose_name = _('Tags'), help_text = _('Tags'))
	comments = models.ManyToManyField('social_network.Comment', null=True, blank=True,
			verbose_name = _('Coments'), help_text = _('Comments'))
	like = models.ManyToManyField('social_network.Like', null=True, blank=True,
			verbose_name = _('Like'), help_text = _('Like'))
	shares = models.ManyToManyField('social_network.StatusShare', null=True, blank=True,
			verbose_name = _('Shares'), help_text = _('Shares'))
	hasMessage = models.BooleanField(default=False,
			verbose_name = _('Has Message'), help_text = _('Has message associated?'))
	isPublic = models.BooleanField(default=False,
			verbose_name = _('Public'), help_text = _('Is Public?'))
	downloadCount = models.IntegerField(default=0,
			verbose_name = _('Download Count'), help_text = _('DownloadCount'))
	size = models.IntegerField(null=True, blank=True,
			verbose_name = _('Size'), help_text = _('Size'))
	def __unicode__(self):
		#TODO: Include metadata, or key=>value pairs where users can search for key
		return str(self.name)
	class Meta:
		db_table = 'SN_FILE'
		ordering = ['-dateCreate']
		verbose_name = _('File')
		verbose_name_plural = _('Files')

class FileVersion(BaseModel):
	"""Version for file"""
	file = models.ForeignKey('File',
			verbose_name = _('File'), help_text = _('File'))
	version = models.ForeignKey('social_network.Version',
			verbose_name = _('Version'), help_text = _('Version'))
	downloadCount = models.IntegerField(default=0,
			verbose_name = _('Download Count'), help_text = _('Download Count'))
	size = models.IntegerField(null=True, blank=True,
			verbose_name = _('Size'), help_text = _('Size'))
	isPublic = models.BooleanField(default=False,
			verbose_name = _('Public'), help_text = _('Is Public?'))
	def __unicode__(self):
		return str(self.file) + ' - ' + str(self.version)
	class Meta:
		db_table = 'SN_VERSION_file'
		verbose_name = _('File Version')
		verbose_name_plural = _('File Versions')

class Contact(BaseModel):
	"""Contact Model
	FK: Owner
	FK: OwnerOrg [optional]
	FK: OwnerGroup [optional]
	ContactId"""
	_RANKING_USER_ACCOUNT = 10
	_RANKING_GROUP = 200
	_RANKING_ORG = 100
	_RANKING_USER = 50
	user = models.ForeignKey('social_network.UserSocial', related_name='contact_user', null=True, blank=True,
			verbose_name = _('User'), help_text = _('User'))
	detail = models.ForeignKey('ContactDetail',
			verbose_name = _('Detail'), help_text = _('Detail'))
	notes = models.TextField(null=True, blank=True,
			verbose_name = _('Notes'), help_text = _('Notes'))
	def __unicode__(self):
		return _('Contact') + ' ' + str(self.detail)
	class Meta:
		db_table = 'SN_CONTACT'
		verbose_name = _('Contact')
		verbose_name_plural = _('Contacts')

class ContactDetail(BaseModel):
	"""Contact Model
	MN: Communications
	MN: Assistants [optional]
	MN: ReportsTo [optional]
	MN: Tags [optional]
	MN: RelatedContacts [optional]
	MN: Addresses [optional]"""
	owner = models.ForeignKey('social_network.UserAccount', related_name='contact_owner_pro', null=True, blank=True,
			verbose_name = _('Owner'), help_text = _('Owner'))
	ownerGroup = models.ForeignKey('social_network.OrganizationGroup', related_name='contact_owner_group', null=True, blank=True,
			verbose_name = _('Group Owner'), help_text = _('Group that owns the contact'))
	ownerOrg = models.ForeignKey('social_network.Organization', related_name='contact_owner_org', null=True, blank=True,
			verbose_name = _('Organizattion Owner'), help_text = _('Organization that owns the contact'))
	user = models.ForeignKey(UserSys, unique=True, null=True, blank=True,
			verbose_name = _('User'), help_text = _('User'))
	firstName = models.CharField(max_length=100,
			verbose_name = _('First Name'), help_text = _('First Name'))
	lastName = models.CharField(max_length=100,
			verbose_name = _('Last Name'), help_text = _('Last Name'))
	middleName = models.CharField(max_length=100, null=True, blank=True,
			verbose_name = _('Middle Name'), help_text = _('Middle Name'))
	name = models.CharField(max_length=200, db_index=True, null=True, blank=True,
			verbose_name = _('Name'), help_text = _('Name'))
	nickName = models.CharField(max_length=20, db_index=True, null=True, blank=True,
			verbose_name = _('Nickname'), help_text = _('Nickname'))
	socialInfo = models.CharField(max_length=500, default='', null=True, blank=True,
			verbose_name = _('Social Info'), help_text = _('Social Information'))
	salutation = models.CharField(max_length=10, null=True, blank=True, choices=Choices.SALUTATION,
			verbose_name = _('Salutation'), help_text = _('Salutation'))
	birthDay = models.DateField(null=True, blank=True,
			verbose_name = _('Birthday'), help_text = _('Birthday'))
	anniversary = models.DateField(null=True, blank=True,
			verbose_name = _('Anniversary'), help_text = _('Anniversary'))
	communications = models.ManyToManyField('MasterValue', through='CommunicationTypeContact', null=True, blank=True, 
			limit_choices_to={"type": "SN.COMMTYPE"}, related_name='contact_communications', verbose_name = _('Communications'), 
			help_text = _('Communications'))
	comBy = models.CharField(max_length=15, null=True, blank=True, choices=Choices.CONTACT_COMM,
			verbose_name = _('Communication By'), help_text = _('Preferred way of communication'))
	preferredSocialNet = models.CharField(max_length=20, null=True, blank=True, choices=Choices.SOCIAL_NETS,
			verbose_name = _('Fav Social Net'), help_text = _('Preferred social network'))
	organization = models.CharField(max_length=30, null=True, blank=True,
			verbose_name = _('Organization'), help_text = _('Organization'))
	jobTitle = models.CharField(max_length=30, null=True, blank=True,
			verbose_name = _('Job Title'), help_text = _('Job Title'))
	department = models.CharField(max_length=30, null=True, blank=True,
			verbose_name = _('Department'), help_text = _('Department'))
	office = models.CharField(max_length=30, null=True, blank=True,
			verbose_name = _('Office'), help_text = _('Office'))
	profession = models.CharField(max_length=30, null=True, blank=True,
			verbose_name = _('Profession'), help_text = _('Profession'))
	industries = models.ManyToManyField('social_network.GroupSocial', limit_choices_to={'industry': True}, related_name='contact_industries', null=True, blank=True,
			verbose_name = _('Industries'), help_text = _('Industries'))
	groups = models.ManyToManyField('social_network.GroupSocial', limit_choices_to={'industry': False}, related_name='contact_groups', null=True, blank=True,
			verbose_name = _('Groups'), help_text = _('Groups'))
	organizations = models.ManyToManyField('social_network.Organization', related_name='contact_organizations', null=True, blank=True,
			verbose_name = _('Organizations'), help_text = _('Organizations'))
	assistants = models.ManyToManyField('self', related_name='contact_assistants', null=True, blank=True,
			verbose_name = _('Assistants'), help_text = _('Assistants'))
	reportsTo = models.ManyToManyField('self', related_name='contact_reports_to', null=True, blank=True,
			verbose_name = _('Reports to'), help_text = _('Person the contact reports to'))
	tags = models.ManyToManyField('social_network.Tag', null=True, blank=True,
			verbose_name = _('Tags'), help_text = _('Tags for contact'))
	relatedContacts = models.ManyToManyField('self', related_name='contact_rel_contacts', null=True, blank=True,
			verbose_name = _('Related Contacts'), help_text = _('Contacts this contact is related to'))
	addresses = models.ManyToManyField('social_network.Address', through='AddressContact', null=True, blank=True,
			related_name='contact_addresses', verbose_name = _('Addresses'), help_text = _('Addresses for contact'))
	source = models.CharField(max_length=10, choices=Choices.CONTACT_SOURCE, null=True, blank=True,
			verbose_name = _('Source'), help_text = _('Source for contact: Method was acquired'))
	isPublic = models.BooleanField(default=False,
			verbose_name = _('Public'), help_text = _('Is Public?'))
	extraInfo = models.TextField(verbose_name = _('Extra Info'), help_text = _('Extra information in json format'))
	def isDirectory(self):
		"""Checks if contact belongs to user directory. Groups and Organizations may also be informed"""
		bCheck = False
		if self.user != None:
			bCheck = True
		return bCheck
	def isAgenda(self):
		"""Checks that contact belongs to the agenda of user, group or organization"""
		bCheck = False
		if self.owner != None or self.ownerGroup != None or self.ownerOrg != None:
			bCheck = True
		return bCheck
	def addressHome(self):
		"""Home Address"""
		obj = self.addresses.filter(addressType=Choices.ADDRESS_TYPE_HOME)
		address = None
		if obj:
			address = obj.address
		return address
	def __unicode__(self):
		if self.nickName != None:
			return str(self.name) + ' - ' + str(self.nickName)
		else:
			return str(self.name)
	class Meta:
		db_table = 'SN_CONTACT_DETAIL'
		verbose_name = _('Contact Detail')
		verbose_name_plural = _('Contacts Detail')

class AddressContact(BaseModel):
	"""Address Organization Model"""
	addressType = models.CharField(max_length=20, choices=Choices.ADDRESS_TYPE,
			verbose_name = _('Address Type'), help_text = _('Address Type'))
	contact = models.ForeignKey('ContactDetail',
			verbose_name = _('Contact'), help_text = _('Contact details'))
	address = models.ForeignKey('social_network.Address',
			verbose_name = _('Address'), help_text = _('Address'))
	def __unicode__(self):
		return str(self.contact) + ' - ' + str(self.addressType)
	class Meta:
		db_table = 'SN_CONTACT_address'
		verbose_name = _('Address Contact')
		verbose_name_plural = _('Address Contacts')

class CommunicationTypeContact(BaseModel):
	"""Communication type for contact"""
	contact = models.ForeignKey('ContactDetail')
	communicationType = models.ForeignKey("MasterValue", related_name='contactcommtype_value')
	name = models.CharField(max_length=50, null=True, blank=True,
			verbose_name = _('Name'), help_text = _('Name'))
	value = models.CharField(max_length=250,
			verbose_name = _('Value'), help_text = _('Value'))
	def __unicode__(self):
		return str(self.contact) + ' ' + str(self.communicationType)
	class Meta:
		db_table = 'SN_CONTACT_communications'
		verbose_name = _('Contact Communication Type')
		verbose_name_plural = _('Contact Communication Types')

class Calendar(BaseModel):
	"""Calendar activities: meetings, events, deadlines, tasks, alerts, etc..."""
	owner = models.ForeignKey('social_network.UserSocial', null=True, blank=True,
			verbose_name = _('Owner'), help_text = _('Owner'))
	contacts = models.ManyToManyField('social_network.Contact', null=True, blank=True, related_name='calendar_contacts',
			verbose_name = _('Contacts'), help_text = _('Contacts'))
	groups = models.ManyToManyField('social_network.GroupSocial', null=True, blank=True,
			verbose_name = _('Groups'), help_text = _('Groups'))
	invitations = models.ManyToManyField('social_network.Contact', null=True, blank=True, through='CalendarInvite', related_name='calendar_invitations',
			verbose_name = _('Invitations'), help_text = _('Invitations'))
	name = models.CharField(max_length=75,
			verbose_name = _('Name'), help_text = _('Name'))
	location = models.CharField(max_length=75, null=True, blank=True,
			verbose_name = _('Location'), help_text = _('Location'))
	repeat = models.CharField(max_length=15, choices=Choices.CALENDAR_REPEAT, null=True, blank=True,
			verbose_name = _('Repeat'), help_text = _('Repeat'))
	notes = models.TextField(null=True, blank=True,
			verbose_name = _('Notes'), help_text = _('Notes'))
	comments = models.ManyToManyField('social_network.Comment', null=True, blank=True,
			verbose_name = _('Comments'), help_text = _('Comments'))
	like = models.ManyToManyField('social_network.Like', null=True, blank=True,
			verbose_name = _('Likes'), help_text = _('Likes'))
	tags = models.ManyToManyField('social_network.Tag', null=True, blank=True,
			verbose_name = _('Tags'), help_text = _('Tags'))
	files = models.ManyToManyField('social_network.File', null=True, blank=True,
			verbose_name = _('Files'), help_text = _('Files'))
	links = models.ManyToManyField('social_network.Link', null=True, blank=True,
			verbose_name = _('Links'), help_text = _('Links'))
	timeDateStart = models.DateTimeField(verbose_name = _('Start'), help_text = _('Start'))
	timeDateEnd = models.DateTimeField(null=True, blank=True,
			verbose_name = _('End'), help_text = _('End'))
	type = models.CharField(max_length=15, choices=Choices.CALENDAR_TYPE,
			verbose_name = _('Type'), help_text = _('Type'))
	isAllDay = models.BooleanField(default=False,
			verbose_name = _('All Day'), help_text = _('All Day'))
	isPublic = models.BooleanField(default=True,
			verbose_name = _('Public'), help_text = _('Is Public?'))
	def __unicode__(self):
		return str(self.name)
	class Meta:
		db_table = 'SN_CALENDAR'
		ordering = ['-timeDateStart']
		verbose_name = _('Calendar')
		verbose_name_plural = _('Calendar')

class CalendarInvite(BaseModel):
	"""Invites to events and other calendar activities"""
	calendar = models.ForeignKey('Calendar',
			verbose_name = _('Calendar'), help_text = _('Calendar'))
	contact = models.ForeignKey('social_network.Contact',
			verbose_name = _('Contact'), help_text = _('Contact'))
	status = models.CharField(max_length=15, choices=Choices.CALENDAR_INVITE_STATUS, default= Constants.PENDING,
			verbose_name = _('Status'), help_text = _('Status'))
	def __unicode__(self):
		return str(self.calendar) + ' ' + str(self.contact)
	class Meta:
		db_table = 'SN_CALENDAR_invite'
		verbose_name = _('Calendar Invite')
		verbose_name_plural = _('Calendar Invites')


##############################################################################################

class XpMsgException(Exception):
	Msg = ''
	Exception = None
	ArgsDict = {}
	def __init__(self, exception, msg, **argsDict):
		"""Doc.
		@param exception: 
		@param msg: 
		@param **argsDict: """
		self.Msg = msg
		self.Exception = exception
		self.ArgsDict = argsDict
	def _log(self, exception, msg, argsDict):
		"""Will use log facility of django 1.3"""
		"""txt = repr(self.Exception)
		for name in self.ArgsDict.keys():
			txt += name + ':' + self.ArgsDict[name]
		txt += ' ' + self.Msg"""
		# Log txt  in error log
		traceback.print_exc()
	def __str__(self):
		#self._log()
		#return repr(self.Msg)
		return self.Msg


##############################################################################################

def getDataDict(form):
	"""Doc."""
	try:
		dict = form.cleaned_data
		if type(dict) != types.DictType:
			dict = form.data
		else:
			dict = form.cleaned_data
	except:
		dict = form.data
	return dict

def getFormDataValue(form, keyName):
	"""Doc."""
	try:
		dict = form.cleaned_data
		if type(dict) != types.DictType:
			dict = form.data
			keyValue = form.data[keyName]
		else:
			dict = form.cleaned_data
			if dict.has_key(keyName):
				keyValue = dict[keyName]
			else:
				keyValue = form.data[keyName]
	except KeyError:
		keyValue = ''
	return keyValue

def setIfNotBlank():
	"""Doc."""
	pass

def getFromDict(key, dict):
	"""Get value from a dict for key. If not found, returns blank string."""
	value = ''
	if dict.has_key(key):
		value = dict[key]
	return value

def getPagingStartEnd(page, numberMatches):
	"""Get tuple (iStart, iEnd)"""
	iStart = (page-1)*numberMatches
	iEnd = iStart+numberMatches
	tuple = (iStart, iEnd)
	return tuple

def parseText(content):
	"""Parse text from content. Useful for indexing fields.
	@param content: 
	@return: parsed text"""
	text = ''
	# TODO: Finish parse with code found in B+
	return text

def parseLinks(content):
	"""Parse links from content
	@param content: 
	@return: linkList"""
	linkList = []
	# TODO: Finish parse with code found in B+
	return linkList 

##############################################################################################

def context(f):
	"""Context and inital variables packed into ArgsDict"""
	def new_f(*ArgsTuple, **ArgsDict):
		print 'context....'
		request = ArgsTuple[0]
		# ContextDict
		lang = translation.get_language()
		contextDict = {
				'lang': lang,
				'settings': settings,
				}
		#ArgsDict['contextDict'] = contextDict
		# lang
		#ArgsDict['lang'] = lang
		# Context
		ctx = ContextObj(request.user, lang, contextDict, request.session, request.COOKIES, request.META)
		# userSocial and socialChannel
		if request.REQUEST.has_key('socialChannel') and request.user.is_authenticated():
			ctx.socialChannel = request.REQUEST['socialChannel']			
		ArgsDict['ctx'] = ctx
		resp = f(*ArgsTuple, **ArgsDict)
		return resp
	return new_f

class Context(object):
	def __init__(self, f):
		self.f = f
	def __call__(self, *argsTuple, **argsDict):
		"""Decorator call method"""
		request = argsTuple[0] 
		langs = ('en')
		lang = translation.get_language()
		if lang not in langs:
			lang = 'en'
		ctx = {}
		ctx['user'] = request.user
		ctx['lang'] = lang
		ctx['settings'] = settings
		ctx['session'] = request.session
		ctx['cookies'] = request.COOKIES
		ctx['meta'] = request.META
		ctx['post'] = request.POST
		ctx['request'] = request.REQUEST
		ctx['get'] = request.GET
		ctx['socialChannel'] = ''
		ctx['userSocial'] = ''
		ctx['auth'] = {}
		ctx['form'] = None
		ctx['captcha'] = None
		if request.REQUEST.has_key('socialChannel') and request.user.is_authenticated():
			ctx['socialChannel'] = request.REQUEST['socialChannel']
			ctx['userSocial'] = request.REQUEST['userSocial']
		argsDict['ctx'] = ctx
		resp = self.f(*argsTuple, **argsDict)
		return resp

class XpTemplate(object):
	_tmplDict = {}
	def __init__(self, tmplDict, *argsTuple, **argsDict):
		self._tmplDict = tmplDict
	def __call__(self, f):
		"""Decorator call method"""		
		def wrapped_f(*argsTuple, **argsDict):
			"""Doc."""
			argsDict['tmplDict'] = self._tmplDict
			resp = f(*argsTuple, **argsDict)
			return resp			
		return wrapped_f

##############################################################################################

class ContextObj(object):
	_user = None
	_userSocial= None
	_socialChannel = ''
	_lang = ''
	_context = {}
	_session = {}
	_cookies = {}
	_META = {}
	def __init__(self, user, lang, contextDict, session, cookies, META):
		self._user = user
		self._lang = lang
		self._context = contextDict
		self._session = session
		self._cookies= cookies
		self._META = META
	def _getUser(self):
		"""Get user"""
		return self._user
	def _getLang(self):
		return self._lang
	def _getContextDict(self):
		"""Doc."""
		return self._context
	def _setUser(self, user):
		"""Sets user"""
		self._user = user
	def _setLang(self, lang):
		"""Doc."""
		self._lang = lang
	def _setContextDict(self, contextDict):
		"""Doc."""
		self._context = contextDict
	def _getSession(self):
		"""Doc."""
		return self._session
	def _getCookies(self):
		"""Doc."""
		return self._cookies
	def _getMETA(self):
		"""Doc."""
		return self._META
	def _getUserSocial(self):
		"""Doc."""
		return self._userSocial
	def _getSocialChannel(self):
		"""Doc."""
		return self._socialChannel
	def _setSession(self, session):
		"""Doc."""
		self._session = session
	def _setCookies(self, cookies):
		"""Doc."""
		self._cookies = cookies
	def _setMETA(self, meta):
		"""Doc."""
		self._META = meta
	def _setUserSocial(self, userSocial):
		"""Doc."""
		self._userSocial = userSocial
	def _setSocialChannel(self, socialChannel):
		"""Doc."""
		self._socialChannel = socialChannel
	def __str__(self):
		dict = {'user': self._user, 'lang': self._lang, 'session': self._session, 'cookies': self._cookies, 'META': self._META, 'context': self._context}
		return str(dict)
	user = property(_getUser, _setUser)
	lang = property(_getLang, _setLang)
	context = property(_getContextDict, _setContextDict)
	session = property(_getSession, _setSession)
	cookies = property(_getCookies, _setCookies)
	META = property(_getMETA, _setMETA)
	userSocial = property(_getUserSocial, _setUserSocial)
	socialChannel = property(_getSocialChannel, _setSocialChannel)

def getResultOK(resultList, status='OK'):
	"""Build result dict for OK status. resultList is a list of objects or content to show in client"""
	resultDict = {}
	resultDict['status'] = status
	resultDict['response'] = resultList
	resultDict['errors'] = []
	return resultDict

def getResultERROR(errorList, response=''):
	"""Build result dict for errors. status ir "ERROR" and response empty as default. "errors" has the errorList attribute"""
	resultDict = {}
	resultDict['status'] = 'ERROR'
	resultDict['response'] = response
	resultDict['errors'] = errorList
	return resultDict
