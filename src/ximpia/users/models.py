import base64
import time
import os
import string
import cPickle
import random
#import json
import simplejson as json
import types

from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User as UserSys, Group as GroupSys
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session
from django.utils.hashcompat import md5_constructor
from django.http import HttpResponse

from ximpia import util

from ximpia.human_resources.models import Professional, Profile, Organization, OrganizationGroup, Industry, Address, AddressOrganization, SocialNetworkOrganization, ProfessionalRelation, ProfessionalContract, File, BsFile 
from ximpia.human_resources.models import Choices as HRChoices 

from ximpia import settings

"""
Professional (Free)
============
- First Name, Last Name, Email, City(E), Country(E)
- Link to Twitter, Facebook, LinkedIn

Organization (Free for 3 users??????)
============
- Account (O)
- Organization Name (O)
- Organization address, phone (O)
- Departments, sharing options (O)
- Link to social networks: Twitter, Facebook(page) (O)
- Users (First Name, Last Name, Email, Social Nets, Department) added


===============================================
Ximpia Tables, refer to Ximps, with little logo
===============================================

- User: Additional user data
- GroupFollows: id, GroupIdTarget, GroupIdSource, Status(OK,Blocked,UnBlocked)
- GroupStream: id, PostId, UserIdSrc, Account, GroupId, Message(One-One), Comments(Many), Likes(Many), 
Shares(Many), Date, Public(Boolean)
- GroupStreamPublic: id, PostId(FK), Mediums(Many), UserMadePublic, DateMadePublic
- Messages: id, PostId, Message
- Comments: id, UserId, Message
- Likes: id, UserId 
- Shares: id, UserId, Message
- Medium: id, NameId, Name, LogoSrc

- OrganizationShareOpt: Organization sharing options and settings, defined by organization administrator


Twitter & Facebook Stream
=========================
- ximpia and ximps (public updates from ximpia)
- Will post all public posts and updates to twitter account ximps
- Organizations may define if they want a public org and which departments or groups are public
- Organizations can attach their twitter account, facebook page
- Groups inside organizations can attach their twitter account, facebook page
- We need a twitter client with requests every 10 seconds or so?????
- Settings: Org Public, Which Groups Are Public
- Management and Human Resources can make public any action and update.

Channels, Hashtags, Update Types
================================
- Twitter #ximp-contact, #ximp-opp, #ximp-client, #ximp-project, #ximp-procedure, etc... 
when making public
- Update Type include #. For example, if you had an idea would go to #idea. This would be
transfered to #ximp-idea when share outside
- A popup would show with options, can write yours too
- Profession activities would go to default channels
- Show message in stream for groups that follow group???? For emample if I am a business consultant,
someone writes #business-consultants then I would see the message. Only possible when sending
campaigns, sending to people streams.
- Professions will have a channel. Also department types and groups inside organizations.
- Settings, organization can choose not to receive campaigns for each channel, or no capaigns at all.
Still, they could get promotion shared by a group that we follow.


"""

class Constants(object):
	XIMPIA = 'ximpia'
	TWITTER = 'twitter'
	FACEBOOK = 'facebook'
	LINKEDIN = 'linkedin'
	EMAIL = 'email'
	FILE_QUOTA_DEFAULT = 2000
	FILE_QUOTA_ORG = 5000
	MSG_MODE_REC = 'received'
	MSG_MODE_SENT = 'sent'
	USER_SETTINGS = 'user_settings'
	SETTINGS_ALLOW_PRIVATE_GRP_SUBS = 'ALLOW_PRIVATE_GRP_SUBS'
	NUMBER_MATCHES = 10
	OK = 'ok'
	BLOCKED = 'blocked'
	UNBLOCKED = 'unblocked'
	ERROR = 'error'
	ARCHIVE = 'archive'
	UNARCHIVE = 'unarchive'
	PROFESSIONAL = 'professional'
	SETTINGS_DEFAULT = ''

class Choices(object):
	MSG_MEDIA = (
			(Constants.XIMPIA,'Ximpia'),
			(Constants.TWITTER,'Twitter'),
			(Constants.FACEBOOK,'Facebook'),
			(Constants.LINKEDIN,'LinkedIn'),
			(Constants.EMAIL,'Email'),
			)
	MSG_PREFERRED = (
			(Constants.XIMPIA,'Ximpia'),
			(Constants.TWITTER,'Twitter'),
			(Constants.FACEBOOK,'Facebook'),
			(Constants.LINKEDIN,'LinkedIn'),
			(Constants.EMAIL,'Email'),
			)
	SOCIAL_NETS = (
		(Constants.TWITTER,'Twitter'),
		(Constants.FACEBOOK,'Facebook'),
		(Constants.LINKEDIN,'LinkedIn'),
		(Constants.LINKEDIN,'Xing'),
		)
	COUNTRY = (
		('fr','France'),
		('es','Spain'),
		)
	MSG_LOG_ACTION_READ = 'read'
	MSG_LOG_ACTION_DOWNLOAD = 'download'
	MSG_LOG_ACTION = (
			(MSG_LOG_ACTION_READ,'Read'),
			(MSG_LOG_ACTION_DOWNLOAD,'File Download'),
			)
	FOLLOW_STATUS = (
			(Constants.OK,'Ok'),
			(Constants.BLOCKED,'Blocked'),
			(Constants.UNBLOCKED,'UnBlocked'),
			)

class DeleteManager(models.Manager):
	def get_query_set(self):
		return super(DeleteManager, self).get_query_set().filter(Delete=False)

class UserParam(models.Model):
	Mode = models.CharField(max_length=20)
	Name = models.CharField(max_length=20)
	Value = models.CharField(max_length=100, null=True, blank=True)
	ValueId = models.IntegerField(null=True, blank=True)
	DateCreate = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	DateModify = models.DateTimeField(auto_now=True, null=True, blank=True)
	UserCreateId = models.IntegerField(null=True, blank=True)
	UserModifyId = models.IntegerField(null=True, blank=True)
	Delete = models.BooleanField(default=False)
	objects = DeleteManager()
	objects_del = models.Manager()
	def __unicode__(self):
		return str(self.Mode) + ' - ' + str(self.Name)
	class Meta:
		db_table = 'US_PARAMS'
		verbose_name_plural = "UserParams"

class SocialNetwork(models.Model):
	Type = models.ForeignKey(UserParam, limit_choices_to={'Mode__lte': 'nets'})
	DateCreate = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	DateModify = models.DateTimeField(auto_now=True, null=True, blank=True)
	UserCreateId = models.IntegerField(null=True, blank=True)
	UserModifyId = models.IntegerField(null=True, blank=True)
	Delete = models.BooleanField(default=False)
	objects = DeleteManager()
	objects_del = models.Manager()
	def __unicode__(self):
		return str(self.Type)
	def getName(self):
		return self.Type.Name
	class Meta:
		db_table = 'US_SOCIAL_NETWORKS'

class SocialNetworkUserX(models.Model):
	User = models.ForeignKey('UserX')
	SocialNetwork = models.ForeignKey('SocialNetwork')
	Account = models.CharField(max_length=30)
	Password = models.CharField(max_length=30, null=True, blank=True)
	DateCreate = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	DateModify = models.DateTimeField(auto_now=True, null=True, blank=True)
	UserCreateId = models.IntegerField(null=True, blank=True)
	UserModifyId = models.IntegerField(null=True, blank=True)
	Delete = models.BooleanField(default=False)
	objects = DeleteManager()
	objects_del = models.Manager()
	def __unicode__(self):
		return str(self.getName()) + ' ' + str(self.Account)
	def getName(self):
		return self.SocialNetwork.getName()
	class Meta:
		db_table = 'US_USERS_SocialNetworks'
		verbose_name_plural = "SocialNetworks_ForUserX"

class UserX(models.Model):
	"""Model for UserX
	FK : User
	MN: Groups
	SocialProfile
	Settings"""
	User = models.ForeignKey(UserSys)
	Groups = models.ManyToManyField('users.GroupX')
	SocialProfile = models.CharField(max_length=20, default=Constants.PROFESSIONAL)
	Settings = models.TextField()
	DateCreate = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	DateModify = models.DateTimeField(auto_now=True, null=True, blank=True)
	UserCreateId = models.IntegerField(null=True, blank=True)
	UserModifyId = models.IntegerField(null=True, blank=True)
	Delete = models.BooleanField(default=False)
	objects = DeleteManager()
	objects_del = models.Manager()
	def __unicode__(self):
		return str(self.User.username)
	def getGroupById(self, groupId):
		"""Doc."""
		list = self.Groups.filter(pk=groupId)
		if len(list) != 0:
			value = list[0]
		else:
			value = None
		return value
	def getFullName(self):
		"""Get full name: firstName lastName"""
		name = self.User.get_full_name()
		return name
	class Meta:
		db_table = 'US_USERS'
		verbose_name = 'User'
		verbose_name_plural = "Users"
		unique_together = ("User", "ProfileType")
	
class UserDetail(models.Model):
	"""Model for UserX
	FK : User
	MN: Groups
	MN: SocialNetworks"""
	User = models.ForeignKey('UserX', 'User')
	Name = models.CharField(max_length=60)
	SocialNetworks = models.ManyToManyField('SocialNetwork', through='SocialNetworkUserX',  null=True, blank=True)
	UploadPic = models.BooleanField(default=False)
	Suspended = models.BooleanField(default=False)
	PicExt = models.CharField(max_length=3, null=True, blank=True)
	ReminderId = models.CharField(max_length=15, null=True, blank=True)
	Lang = models.CharField(max_length=2, default='en')
	FacebookAuth = models.BooleanField(default=False)
	TwitterAuth = models.BooleanField(default=False)
	LinkedInAuth = models.BooleanField(default=False)
	MsgPreference = models.CharField(max_length=10, choices=Choices.MSG_PREFERRED, default=Constants.XIMPIA)
	City = models.CharField(max_length=20)
	Country = models.CharField(max_length=2)
	ValidatedEmail = models.BooleanField(default=False)
	FilesQuota = models.IntegerField(default=Constants.FILE_QUOTA_DEFAULT)
	DateCreate = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	DateModify = models.DateTimeField(auto_now=True, null=True, blank=True)
	UserCreateId = models.IntegerField(null=True, blank=True)
	UserModifyId = models.IntegerField(null=True, blank=True)
	Delete = models.BooleanField(default=False)
	objects = DeleteManager()
	objects_del = models.Manager()
	def __unicode__(self):
		return str(self.User.username)
	def getSocialNetworkUser(self, socialNetName):
		"""Doc."""
		list = self.SocialNetworks.filter(Type__Name=socialNetName)
		if len(list) != 0:
			value = list[0].socialnetworkuserx_set.all()[0]
		else:
			value = None
		return value
	class Meta:
		db_table = 'US_USERS_DETAIL'
		verbose_name = 'UserDetail'
		verbose_name_plural = "UsersDetail"

class GroupX(models.Model):
	"""Ximpia Group Model.
	FK: Group
	FK: Owner
	MN: Tags
	MN: Admins->UserX
	MN: AccessGroups
	XimpiaGroup
	Industry
	SocialGroup
	OrgGroup
	Public"""
	Group = models.ForeignKey(GroupSys, unique=True, primary_key=True)
	XimpiaGroup = models.BooleanField(default=False)
	Industry = models.BooleanField(default=False)
	SocialGroup = models.BooleanField(default=False)
	OrgGroup = models.BooleanField(default=False)
	Account = models.ForeignKey('human_resources.Organization', null=True, blank=True)
	Public = models.BooleanField(default=True)
	AccessGroups = models.ManyToManyField('self', related_name='group_access', null=True, blank=True)
	Tags = models.ManyToManyField('Tag', null=True, blank=True)
	Owner = models.ForeignKey('UserX', related_name='group_owner', null=True, blank=True)
	Admins = models.ManyToManyField('UserX', related_name='group_admins', null=True, blank=True)
	Managers = models.ManyToManyField('UserX', related_name='group_managers', null=True, blank=True)
	DateCreate = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	DateModify = models.DateTimeField(auto_now=True, null=True, blank=True)
	UserCreateId = models.IntegerField(null=True, blank=True)
	UserModifyId = models.IntegerField(null=True, blank=True)
	Delete = models.BooleanField(default=False)
	objects = DeleteManager()
	objects_del = models.Manager()
	def __unicode__(self):
		return str(self.Group)
	class Meta:
		db_table = 'US_GROUPS'
		verbose_name = 'Group'
		verbose_name_plural = "Groups"

class GroupFollow(models.Model):
	"""Group Follow Model
	FK: GroupSource
	FK: GroupTarget
	Status"""
	GroupSource = models.ForeignKey(GroupSys, related_name='group_follow_source')
	GroupTarget = models.ForeignKey(GroupSys, related_name='group_follow_target')
	Status = models.CharField(max_length=10, choices=Choices.FOLLOW_STATUS, default=Constants.OK)
	DateCreate = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	DateModify = models.DateTimeField(auto_now=True, null=True, blank=True)
	UserCreateId = models.IntegerField(null=True, blank=True)
	UserModifyId = models.IntegerField(null=True, blank=True)
	Delete = models.BooleanField(default=False)
	objects = DeleteManager()
	objects_del = models.Manager()
	def __unicode__(self):
		return str(self.GroupSource) + ' - ' + str(self.GroupTarget)
	class Meta:
		db_table = 'US_GROUP_FOLLOW'
		verbose_name_plural = "GroupFollows"

class StatusMessage(models.Model):
	"""Status Message Model
	MN: Tags
	MN: Files
	MN: Links
	Message"""
	Message = models.TextField()
	Tags = models.ManyToManyField('Tag', null=True, blank=True)
	Files = models.ManyToManyField('human_resources.File', null=True, blank=True)
	Links = models.ManyToManyField('Link', null=True, blank=True)
	DateCreate = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	DateModify = models.DateTimeField(auto_now=True, null=True, blank=True)
	UserCreateId = models.IntegerField(null=True, blank=True)
	UserModifyId = models.IntegerField(null=True, blank=True)
	Delete = models.BooleanField(default=False)
	objects = DeleteManager()
	objects_del = models.Manager()
	def __unicode__(self):
		return str(self.Message[:30])
	class Meta:
		db_table = 'US_STATUS_MESSAGE'
		verbose_name_plural = "StatusMessages"

class Comment(models.Model):
	"""Comment Model
	FK: User
	MN: Like
	MN: Share
	MN: Files
	Message
	Public"""
	User = models.ForeignKey(UserX)
	Message = models.TextField()
	Like = models.ManyToManyField('Like', null=True, blank=True)
	Share = models.ManyToManyField('StatusShare', null=True, blank=True)
	Files = models.ManyToManyField('human_resources.File', null=True, blank=True)
	Public = models.BooleanField(default=True)
	DateCreate = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	DateModify = models.DateTimeField(auto_now=True, null=True, blank=True)
	UserCreateId = models.IntegerField(null=True, blank=True)
	UserModifyId = models.IntegerField(null=True, blank=True)
	Delete = models.BooleanField(default=False)
	objects = DeleteManager()
	objects_del = models.Manager()
	def __unicode__(self):
		return str(self.User) + ' - ' + str(self.Message[:20])
	class Meta:
		db_table = 'US_COMMENTS'
		verbose_name_plural = "Comments"

class Like(models.Model):
	"""Like Model
	FK: User
	Number"""
	User = models.ForeignKey(UserX)
	Number = models.IntegerField(default=0)
	DateCreate = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	DateModify = models.DateTimeField(auto_now=True, null=True, blank=True)
	UserCreateId = models.IntegerField(null=True, blank=True)
	UserModifyId = models.IntegerField(null=True, blank=True)
	Delete = models.BooleanField(default=False)
	objects = DeleteManager()
	objects_del = models.Manager()
	def __unicode__(self):
		return str(self.User)
	class Meta:
		db_table = 'US_LIKES'
		verbose_name_plural = "Likes"

class StatusShare(models.Model):
	"""Status share model
	FK: User
	Message"""
	User = models.ForeignKey(UserX)
	Message = models.TextField(null=True, blank=True)
	DateCreate = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	DateModify = models.DateTimeField(auto_now=True, null=True, blank=True)
	UserCreateId = models.IntegerField(null=True, blank=True)
	UserModifyId = models.IntegerField(null=True, blank=True)
	Delete = models.BooleanField(default=False)
	objects = DeleteManager()
	objects_del = models.Manager()
	def __unicode__(self):
		return str(self.User)
	class Meta:
		db_table = 'US_STATUS_SHARE'
		verbose_name_plural = "StatusShares"

class GroupStream(models.Model):
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
	PostId = models.BigIntegerField()
	User = models.ForeignKey(UserX)
	Account = models.ForeignKey('human_resources.Organization', null=True, blank=True, related_name='group_stream_account')
	Group = models.ForeignKey(GroupSys, null=True, blank=True)
	Message = models.ForeignKey('StatusMessage')
	Comments = models.ManyToManyField('Comment', null=True, blank=True)
	Like = models.ManyToManyField('Like', null=True, blank=True)
	Shares = models.ManyToManyField(StatusShare, null=True, blank=True)
	Public = models.BooleanField(default=False)
	Source = models.CharField(max_length=10, choices=Choices.MSG_MEDIA, default=Constants.XIMPIA)
	DateCreate = models.DateTimeField(auto_now_add=True, null=True, blank=True, db_index=True)
	DateModify = models.DateTimeField(auto_now=True, null=True, blank=True)
	UserCreateId = models.IntegerField(null=True, blank=True)
	UserModifyId = models.IntegerField(null=True, blank=True)
	Delete = models.BooleanField(default=False)
	objects = DeleteManager()
	objects_del = models.Manager()
	def __unicode__(self):
		return str(self.User) + ' - ' + str(self.PostId)
	class Meta:
		db_table = 'US_STATUS_STREAM'
		ordering = ['-DateCreate']
		verbose_name_plural = "StatusStream"

class GroupStreamPublic(models.Model):
	"""Group Stream Public Model
	FK: PostId
	FK: UserMadePublic
	MN: SocialNetwork
	DateMadePublic"""
	PostId = models.ForeignKey(GroupStream)
	SocialNetwork = models.ManyToManyField(SocialNetwork)
	UserMadePublic = models.ForeignKey(UserX)
	DateMadePublic = models.DateTimeField(auto_now_add=True)
	DateCreate = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	DateModify = models.DateTimeField(auto_now=True, null=True, blank=True)
	UserCreateId = models.IntegerField(null=True, blank=True)
	UserModifyId = models.IntegerField(null=True, blank=True)
	Delete = models.BooleanField(default=False)
	objects = DeleteManager()
	objects_del = models.Manager()
	def __unicode__(self):
		return str(self.PostId)
	class Meta:
		db_table = 'US_STATUS_STREAM_PUBLIC'
		verbose_name_plural = "GroupStreamPublic"

class Tag(models.Model):
	"""Tag Model
	Tag : CharField
	SystemTag : Boolean:False
	Popularity : Integer
	Public : Boolean:True"""
	Name = models.CharField(max_length=30)
	SystemTag = models.BooleanField(default=False)
	Popularity = models.IntegerField(default=1, null=True, blank=True)
	Public = models.BooleanField(default=True)
	DateCreate = models.DateTimeField(auto_now_add=True, null=True, blank=True, db_index=True)
	DateModify = models.DateTimeField(auto_now=True, null=True, blank=True)
	UserCreateId = models.IntegerField(null=True, blank=True)
	UserModifyId = models.IntegerField(null=True, blank=True)
	Delete = models.BooleanField(default=False)
	objects = DeleteManager()
	objects_del = models.Manager()
	def __unicode__(self):
		return str(self.Tag)
	class Meta:
		db_table = 'US_TAGS'
		verbose_name_plural = "Tags"

class MessageAddr(models.Model):
	"""Addreses in Messages Model
	Address: Can be email or social network id
	Type"""
	Address = models.CharField(max_length=200)
	Type = models.CharField(max_length=20, choices=Choices.MSG_MEDIA)
	Delete = models.BooleanField(default=False)
	DateCreate = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	DateModify = models.DateTimeField(auto_now=True, null=True, blank=True)
	UserCreateId = models.IntegerField(null=True, blank=True)
	UserModifyId = models.IntegerField(null=True, blank=True)
	objects = DeleteManager()
	objects_del = models.Manager()
	def __unicode__(self):
		return str(self.UserFrom) + ' - ' + str(self.MessageId)
	class Meta:
		db_table = 'US_MSG_SENT'
		verbose_name_plural = "MessageAddresses"

class MessageSent(models.Model):
	"""Message Sent Model
	FK: Message
	FK: UserFrom
	MN: UsersTo
	FK: GroupFrom [optional]
	FK: GroupTo [optional]
	MN: EmailAddrsTo
	MN: Logs"""
	Message = models.ForeignKey('Message')
	UserFrom = models.ForeignKey('UserX')
	UsersTo = models.ManyToManyField('UserX', null=True, blank=True)
	GroupFrom = models.ForeignKey('human_resources.OrganizationGroup', null=True, blank=True) # Representation rights for department ????
	GroupsTo = models.ManyToManyField('human_resources.OrganizationGroup', null=True, blank=True) # Rights to send to that group, belong to group or follow group
	AddrsTo = models.ManyToManyField('MessageAddr', null=True, blank=True)
	Logs = models.ManyToManyField('MessageLog', null=True, blank=True)
	Delete = models.BooleanField(default=False)
	DateCreate = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	DateModify = models.DateTimeField(auto_now=True, null=True, blank=True)
	UserCreateId = models.IntegerField(null=True, blank=True)
	UserModifyId = models.IntegerField(null=True, blank=True)
	objects = DeleteManager()
	objects_del = models.Manager()
	def __unicode__(self):
		return str(self.UserFrom) + ' - ' + str(self.MessageId)
	class Meta:
		db_table = 'US_MSG_SENT'
		verbose_name_plural = "MessagesSent"

class MessageReply(models.Model):
	"""Message Reply Model
	FK: Message
	FK: UserFrom [optional]
	FK: GroupFrom [optional]
	FK: Discussion [optional]
	MN: Like
	MN: Share
	MN: Files
	MN: Links
	MN: Tags
	Message
	DiscussionsUnread"""
	Message = models.ForeignKey('Message')
	UserFrom = models.ForeignKey('UserX', null=True, blank=True)
	GroupFrom = models.ForeignKey('human_resources.OrganizationGroup', null=True, blank=True)
	MessageContent = models.TextField()
	Links = models.ManyToManyField('Link', null=True, blank=True)
	Tags = models.ManyToManyField('Tag', null=True, blank=True)
	Like = models.ManyToManyField('Like', null=True, blank=True)
	Share = models.ManyToManyField('StatusShare', null=True, blank=True)
	Files = models.ManyToManyField('human_resources.File', null=True, blank=True)
	Discussion = models.ForeignKey('Discussion', null=True, blank=True)
	DiscussionsUnread = models.SmallIntegerField(default=0)
	Delete = models.BooleanField(default=False)
	DateCreate = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	DateModify = models.DateTimeField(auto_now=True, null=True, blank=True)
	UserCreateId = models.IntegerField(null=True, blank=True)
	UserModifyId = models.IntegerField(null=True, blank=True)
	objects = DeleteManager()
	objects_del = models.Manager()
	def __unicode__(self):
		return str(self.MessageId) + ' ' + str(self.id)
	class Meta:
		db_table = 'US_MSG_REPLY'
		verbose_name_plural = "MessagesReply"
class Message(models.Model):
	"""Messages Received Model
	FK; Discussion [optional]	
	MN: Replies
	MN: Files
	MN: Tags
	MN: Links
	MN: Like
	Summary
	Message
	Source
	Secure"""
	Replies = models.ManyToManyField('MessageReply', null=True, blank=True)
	Summary = models.CharField(max_length=140)
	Message = models.TextField()
	Links = models.ManyToManyField('Link', null=True, blank=True)
	Files = models.ManyToManyField('human_resources.File', null=True, blank=True)
	Like = models.ManyToManyField('Like', null=True, blank=True)
	Discussion = models.ForeignKey('Discussion', null=True, blank=True)
	DiscussionsUnread = models.SmallIntegerField(default=0)
	Tags = models.ManyToManyField('Tag', null=True, blank=True)
	Archived = models.BooleanField(default=False, db_index=True)
	Source = models.CharField(max_length=10, choices=Choices.MSG_MEDIA, default=Constants.XIMPIA)
	Secure = models.BooleanField(default=False)
	Delete = models.BooleanField(default=False)
	DateCreate = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	DateModify = models.DateTimeField(auto_now=True, null=True, blank=True)
	UserCreateId = models.IntegerField(null=True, blank=True)
	UserModifyId = models.IntegerField(null=True, blank=True)
	objects = DeleteManager()
	objects_del = models.Manager()
	def __unicode__(self):
		return str(self.From) + ' - ' + str(self.UserTo)
	class Meta:
		db_table = 'US_MSGS'
		verbose_name_plural = "Messages"

class MessageReceived(models.Model):
	"""Messages Received Model
	FK: Message
	FK: UserTo [optional]
	FK: GroupTo [optional]
	FK: UserFrom [optional]
	FK: GroupFrom [optional]
	MN: AddrsFrom"""
	Message = models.ForeignKey('Message')
	UserFrom = models.ForeignKey('UserX', null=True, blank=True)
	GroupFrom = models.ForeignKey('human_resources.OrganizationGroup', null=True, blank=True)
	AddrsFrom = models.ManyToManyField('MessageAddr', null=True, blank=True)
	UserTo = models.ForeignKey('UserX', null=True, blank=True)
	GroupTo = models.ForeignKey('human_resources.OrganizationGroup', null=True, blank=True)
	AddrTo = models.ForeignKey('MessageAddr', null=True, blank=True)
	Delete = models.BooleanField(default=False)
	DateCreate = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	DateModify = models.DateTimeField(auto_now=True, null=True, blank=True)
	UserCreateId = models.IntegerField(null=True, blank=True)
	UserModifyId = models.IntegerField(null=True, blank=True)
	objects = DeleteManager()
	objects_del = models.Manager()
	def __unicode__(self):
		return str(self.From) + ' - ' + str(self.UserTo)
	class Meta:
		db_table = 'US_MSG_RECEIVED'
		verbose_name_plural = "MessagesReceived"

class MessageLog(models.Model):
	"""Message Log Model
	FK: UserFrom
	FK: UserTo
	FK: EmailAddr
	MessageId
	Action"""
	UserFrom = models.ForeignKey('UserX')
	MessageId = models.BigIntegerField(db_index=True)
	UserTo = models.ForeignKey('UserX', null=True, blank=True)
	Addr = models.ForeignKey('MessageAddr', null=True, blank=True)
	Action = models.CharField(max_length=10, choices=Choices.MSG_LOG_ACTION)
	Delete = models.BooleanField(default=False)
	DateCreate = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	DateModify = models.DateTimeField(auto_now=True, null=True, blank=True)
	UserCreateId = models.IntegerField(null=True, blank=True)
	UserModifyId = models.IntegerField(null=True, blank=True)
	objects = DeleteManager()
	objects_del = models.Manager()
	def __unicode__(self):
		return str(self.FileId)
	class Meta:
		db_table = 'US_MSG_LOGS'
		verbose_name_plural = "MessageLog"

class Discussion(models.Model):
	"""Discussion Model
	FK: UserPosting
	MN: UsersParticipate
	MN: Files
	MN: Tags
	MN: Links
	MN: Like
	MN: Share
	Topic"""
	UserPosting = models.ForeignKey('UserX')
	UsersParticipate = models.ManyToManyField('UserX', null=True, blank=True)
	Topic = models.TextField()
	Files = models.ManyToManyField('human_resources.File', null=True, blank=True)
	Tags = models.ManyToManyField('Tag', null=True, blank=True)
	Like = models.ManyToManyField('Like', null=True, blank=True)
	Links = models.ManyToManyField('Links', null=True, blank=True)
	Share = models.ManyToManyField('StatusShare', null=True, blank=True)
	Threads = models.ManyToManyField('DiscussionThreads', null=True, blank=True)
	Delete = models.BooleanField(default=False)
	DateCreate = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	DateModify = models.DateTimeField(auto_now=True, null=True, blank=True)
	UserCreateId = models.IntegerField(null=True, blank=True)
	UserModifyId = models.IntegerField(null=True, blank=True)
	objects = DeleteManager()
	objects_del = models.Manager()
	def __unicode__(self):
		return str(self.id) + ' ' + str(self.UserPosting)
	class Meta:
		db_table = 'US_DISCUSSIONS'
		verbose_name_plural = "Discussions"

class DiscussionThread(models.Model):
	"""Discussion Thread Model: Usefull for problems and solutions, brainstorming, discussions, etc...
	FK: User
	FK: Discussion
	MN: Files
	MN: Comments
	MN: Tags
	MN: Like
	MN: Links
	MN: Share
	Thread
	Content"""
	User = models.ForeignKey('UserX')
	Thread = models.CharField(max_length=140)
	Files = models.ManyToManyField('human_resources.File', null=True, blank=True)
	Content = models.TextField(null=True, blank=True)
	Comments = models.ManyToManyField(Comment, null=True, blank=True)
	Tags = models.ManyToManyField('Tag', null=True, blank=True)
	Like = models.ManyToManyField('Like', null=True, blank=True)
	Links = models.ManyToManyField('Link', null=True, blank=True)
	Share = models.ManyToManyField('StatusShare', null=True, blank=True)
	Delete = models.BooleanField(default=False)
	DateCreate = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	DateModify = models.DateTimeField(auto_now=True, null=True, blank=True)
	UserCreateId = models.IntegerField(null=True, blank=True)
	UserModifyId = models.IntegerField(null=True, blank=True)
	objects = DeleteManager()
	objects_del = models.Manager()
	def __unicode__(self):
		return str(self.id)
	class Meta:
		db_table = 'US_DISCUSSIONS_THREAD'
		verbose_name_plural = "DiscussionThreads"

class Link(models.Model):
	"""Link Model
	Url
	NumberShared
	Domain"""
	Url = models.URLField()
	Title = models.CharField(max_length=200, null=True, blank=True)
	Description = models.CharField(max_length=300, null=True, blank=True)
	ImgUrl = models.URLField()
	NumberShared = models.IntegerField(default=1)
	Domain = models.CharField(max_length=100, db_index=True)
	Delete = models.BooleanField(default=False)
	DateCreate = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	DateModify = models.DateTimeField(auto_now=True, null=True, blank=True)
	UserCreateId = models.IntegerField(null=True, blank=True)
	UserModifyId = models.IntegerField(null=True, blank=True)
	objects = DeleteManager()
	objects_del = models.Manager()
	def __unicode__(self):
		return str(self.id)
	class Meta:
		db_table = 'US_LINKS'
		verbose_name_plural = "Links"

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

def getPagingStartEnd(page, numberMatches):
	"""Get tuple (iStart, iEnd)"""
	iStart = (page-1)*numberMatches
	iEnd = iStart+numberMatches
	tuple = (iStart, iEnd)
	return tuple

##############################################################################################

class BsAccount(object):
	@staticmethod
	def linkUserSocialNetworks(request, form, userDetail):
		"""Doc."""
		twitter = getDataDict(form)['twitter']
		twitterPass = getDataDict(form)['twitterPass']
		facebook = getDataDict(form)['facebook']
		facebookPass = getDataDict(form)['facebookPass']
		linkedIn = getDataDict(form)['linkedIn']
		linkedInPass = getDataDict(form)['linkedInPass']
		user = userDetail.User.User
		typeTwitter = UserParam.objects.get(Mode='net', Name=Constants.TWITTER)
		typeFacebook = UserParam.objects.get(Mode='net', Name=Constants.FACEBOOK)
		typeLinkedIn = UserParam.objects.get(Mode='net', Name=Constants.LINKEDIN)
		netTwitter = SocialNetwork.objects.get(Type=typeTwitter)
		netFacebook = SocialNetwork.objects.get(Type=typeFacebook)
		netLinkedIn = SocialNetwork.objects.get(Type=typeLinkedIn)
		tupleSocialNets = (netTwitter, netFacebook, netLinkedIn)
		for socialNet in tupleSocialNets:
			if socialNet.getName() == Constants.TWITTER and twitter != '':
				userDetail.TwitterAuth = True
				netUser = SocialNetworkUserX(User=userDetail, SocialNetwork=socialNet)
				netUser.Account = twitter
				netUser.Password = twitterPass
			elif socialNet.getName() == Constants.FACEBOOK and facebook != '':
				userDetail.FacebookAuth = True
				netUser = SocialNetworkUserX(User=userDetail, SocialNetwork=socialNet)
				netUser.Account = facebook
				netUser.Password = facebookPass
			elif socialNet.getName() == Constants.LINKEDIN and linkedIn != '':
				userDetail.LinkedInAuth = True
				netUser = SocialNetworkUserX(User=userDetail, SocialNetwork=socialNet)
				netUser.Account = linkedIn
				netUser.Password = linkedInPass
			netUser.UserCreateId = user.pk
			netUser.save()
		userX.save()
	@staticmethod		
	def addGroupsToUser(request, form, groupIdList):
		"""Doc."""
		ximpiaId = getDataDict(form)['ximpiaId']
		user = UserSys.objects.get(username=ximpiaId)
		userX = UserX.objects.get(User=user)
		for groupId in groupIdList:
			group = GroupSys.objects.get(id=groupId)
			user.groups.add(group)
			groupX = GroupX.objects.get(Group__id=groupId)
			userX.Groups.add(groupX)
	@staticmethod
	def doSignup(request, form):
		"""Doc."""
		# Get data from form
		ximpiaId = getDataDict(form)['ximpiaId']
		email = getDataDict(form)['email']
		firstName = getDataDict(form)['firstName']
		lastName = getDataDict(form)['lastName']
		password = getDataDict(form)['password']
		industryList = getDataDict(form)['industry']
		city = getDataDict(form)['city']
		country = getDataDict(form)['country']
		twitter = getDataDict(form)['twitter']
		twitterPass = getDataDict(form)['twitterPass']
		facebook = getDataDict(form)['facebook']
		facebookPass = getDataDict(form)['facebookPass']
		linkedIn = getDataDict(form)['linkedIn']
		linkedInPass = getDataDict(form)['linkedInPass']
		userGroupList = eval(getDataDict(form)['userGroups'])
		# Build Id Lists
		listTools = util.basic_types.ListType()
		industryIdList = listTools.buildIdList(industryList)
		groupTmpList = listTools.mixLists(industryList, userGroupList)
		groupList = listTools.buildIdList(groupTmpList)
		# Django User
		user = UserSys(username=ximpiaId, email=email, first_name=firstName, last_name=lastName)
		user.set_password(password)
		user.save()
		# Ximpia User
		name = firstName + ' ' + lastName
		userX = BsUser.createProfile(request, user, Constants.PROFESSIONAL)
		userDetail = UserDetail.objects.create(User=userX, Name=name, City=city, Country=country, UserCreateId=user.id)
		# Add groups to user
		BsAccount.addGroupsToUser(request, form, groupList)
		# Social Networks Linked
		if twitter != '' or facebook != '' or linkedIn != '':
			BsAccount.linkUserSocialNetworks(request, form, userDetail)
		# Professional
		professional = Professional.objects.create(User=userX, UserCreateId = user.pk)
		if len(industryIdList) != 0:
			industryList = Industry.objects.in_bulk(industryIdList)
			for industry in industryList:
				professional.Industries.add(industry)
		# Profile
		profile = Profile.objects.create(Professional=professional, UserCreateId = user.pk)
	@staticmethod
	def getSocialNetwork(request, form, socialNet):
		"""Doc."""
		typeNet = UserParam.objects.get(Mode='net', Name=socialNet)
		socialNet = SocialNetwork.objects.get(Type=typeNet)
		return socialNet
	@staticmethod
	def doOrganizationSignup(request, form):
		"""Doc."""
		# Get data from form
		ximpiaId = getDataDict(form)['ximpiaId']
		email = getDataDict(form)['email']
		firstName = getDataDict(form)['firstName']
		lastName = getDataDict(form)['lastName']
		password = getDataDict(form)['password']
		industryList = getDataDict(form)['industry']
		city = getDataDict(form)['city']
		country = getDataDict(form)['country']
		twitter = getDataDict(form)['twitter']
		twitterPass = getDataDict(form)['twitterPass']
		facebook = getDataDict(form)['facebook']
		facebookPass = getDataDict(form)['facebookPass']
		linkedIn = getDataDict(form)['linkedIn']
		linkedInPass = getDataDict(form)['linkedInPass']
		userGroupList = eval(getDataDict(form)['userGroups'])
		organizationName = getDataDict(form)['organizationName']
		organizationDomain = getDataDict(form)['organizationDomain']
		organizationCity = getDataDict(form)['organizationCity']
		organizationCountry = getDataDict(form)['organizationCountry']
		jobTitle = getDataDict(form)['jobTitle']
		account = getDataDict(form)['account']
		#jobStatus = getDataDict(form)['jobStatus']
		#jobContractType = getDataDict(form)['jobContractType']
		#jobSchedule = getDataDict(form)['jobSchedule']
		organizationDescription = getDataDict(form)['organizationDescription']
		organizationGroup = getDataDict(form)['organizationGroup']
		organizationGroupTags = getDataDict(form)['organizationGroupTags']
		organizationTwitter = getDataDict(form)['organizationTwitter']
		organizationTwitterPass = getDataDict(form)['organizationTwitterPass']
		# Build Id Lists
		listTools = util.basic_types.ListType()
		industryIdList = listTools.buildIdList(industryList)
		groupTmpList = listTools.mixLists(industryList, userGroupList)
		groupList = listTools.buildIdList(groupTmpList)
		industryList = []
		if len(industryIdList) != 0:
			industryList = Industry.objects.in_bulk(industryIdList)
		# Django User
		user = UserSys(username=ximpiaId, email=email, first_name=firstName, last_name=lastName)
		user.set_password(password)
		user.save()
		# Ximpia User
		userX = UserX.objects.create(User=user, City=city, Country=country, UserCreateId = user.pk)
		BsAccount.addGroupsToUser(request, form, groupList)
		# Social Networks Linked
		if twitter != '' or facebook != '' or linkedIn != '':
			BsAccount.linkUserSocialNetworks(request, form, userX)
		# User Profile
		profile = Profile.objects.create(Professional=professional, UserCreateId = user.pk)
		# Organization
		organization = Organization.objects.create(
							Account=account, 
							Name=organizationName, 
							Domain=organizationDomain, 
							Description=organizationDescription, 
							FilesQuota = FILE_QUOTA_DEFAULT)
		# OrganizationGroup & Groups
		orgGroup, bGroup = GroupSys.objects.get_or_create(name=organizationGroup)
		orgGroupX, bGroupX = GroupX.objects.get_or_create(Group=orgGroup, Public=False, OrgGroup=True)
		organizationGroup = OrganizationGroup.objects.create(Group=orgGroupX, Organization=organization)
		# Industries
		for industry in industryList:
			organization.Industries.add(industry)
		# Address
		address = Address.objects.get_or_create(Type=HRChoices.ADDRESS_TYPE_BILL)
		addressOrg = AddressOrganization.objects.create(
							Address=address, 
							Organization=organization, 
							City=organizationCity, 
							Country=organizationCountry)
		# Social Networks
		netTwitter = BsAccount.getSocialNetwork(request, form, Constants.TWITTER)
		SocialNetworkOrganization.objects.create(
							Organization=organization, 
							SocialNetwork=netTwitter, 
							Account=organizationTwitter, 
							Password=organizationTwitterPass)
		# Professional
		professional = Professional.objects.create(User=userX, UserCreateId = user.pk)
		for industry in industryList:
			professional.Industries.add(industry)
		# Relation User to Organization
		contract, bContract = ProfessionalContract.objects.get_or_create(
										Status=HRChoices.STATUS_EMPLOYEE, 
										Schedule=HRChoices.SCHEDULE_FULL, 
										ContractType=HRChoices.CONTRACT_TYPE_REGULAR, 
										JobTitle=jobTitle)
		professionalRelation = ProfessionalRelation.objects.create(
									Organization=organization, 
									OrganizationGroup=organizationGroup, 
									ProfessionalContract=contract)
		professional.ProfessionalRelations.add(professionalRelation)
	@staticmethod
	def doOrganizationUserSignup(request, form):
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
		# Build Id Lists
		listTools = util.basic_types.ListType()
		groupList = listTools.buildIdList(userGroupList)
		#professionalRelationList
		# Django User
		user = UserSys(username=ximpiaId, email=email, first_name=firstName, last_name=lastName)
		user.set_password(password)
		user.save()
		# Ximpia User
		userX = UserX.objects.create(User=user, City=city, Country=country, UserCreateId = user.pk)
		# Organization user should be allowed to follow industries streams by default????
		BsAccount.addGroupsToUser(request, form, groupList)
		# Social Networks Linked
		if twitter != '' or facebook != '' or linkedIn != '':
			BsAccount.linkUserSocialNetworks(request, form, userX)
		# User Profile
		profile = Profile.objects.create(Professional=professional, UserCreateId = user.pk)
		# Professional
		professional = Professional.objects.create(User=userX, UserCreateId = user.pk)
		# Relation User to Organization
		# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
		professionalRelationList = []
		for professionalRelationTuple in professionalRelationList:
			jobStatus, jobSchedule, jobContractType, subcontractOrgName = professionalRelationTuple
			contract, bContract = ProfessionalContract.objects.get_or_create(
										Status=jobStatus, 
										Schedule=jobSchedule, 
										ContractType=jobContractType, 
										JobTitle=jobTitle)
			if subcontractOrgName != '':				
				try:
					subcontractOrg = Organization.objects.get(Name=subcontractOrgName)
				except Organization.DoesNotExist:
					subcontractOrg = None
				except Organization.MultiObjectsReturned:
					subcontractOrg = None
			professionalRelation = ProfessionalRelation.objects.create(
									Organization=organization, 
									OrganizationGroup=organizationGroup, 
									ProfessionalContract=contract,
									SubcontractOrganization=subcontractOrg)
			professional.ProfessionalRelations.add(professionalRelation)

class BsUser(object):
	@staticmethod
	def get(request):
		"""Get UserX
		@param request: 
		@return: userX"""
		try:
			userX = UserX.objects.get(User=request.user, SocialProfile=Constants.PROFESSIONAL)
		except UserX.DoesNotExist:
			raise UserX.DoesNotExist
		return userX
	@staticmethod
	def getByProfile(request, socialProfile):
		"""Get UserX by social profile
		@param request:
		@param socialProfile:
		@return: userX"""
		try:
			userX = UserX.objects.get(User=request.user, SocialProfile=socialProfile)
		except UserX.DoesNotExist:
			raise UserX.DoesNotExist
		return userX
	@staticmethod
	def getDetails(request):
		"""Get UserX
		@param request: 
		@return: userDetail"""
		try:
			userX = UserX.objects.get(User=request.user, SocialProfile=Constants.PROFESSIONAL)
			userDetail = UserDetail.objects.get(User=userX)
		except UserX.DoesNotExist:
			raise UserX.DoesNotExist
		except UserDetail.DoesNotExist:
			raise UserDetail.DoesNotExist
		return userDetail
	@staticmethod
	def getProfiles(request):
		"""Get social profiles for user
		@param request:
		@return: userList"""
		userList = UserX.objects.filter(User=request.user)
		return userList
	@staticmethod
	def getProfilesByGroupList(request, userId, groupList):
		"""Get profiles for user and list of groups. Used when user has in common two groups or more with user. Generally this will return a list of one element
		@param request:
		@param userId: 
		@param groupList: 
		@return: userList"""
		userList = UserX.objects.filter(User__id=userId, Groups__in=groupList)
		return userList
	@staticmethod
	def getMyGroupsByProfile(request, socialProfile):
		"""Get the groups (either OrgGroup or Industry) I belong to, given the social profile
		@param request: 
		@param socialProfile: 
		@return: groupList"""
		userX = BsUser.getByProfile(request, socialProfile)
		groupList = userX.Groups.filter(Q(OrgGroup=True) | Q(Industry=True))
		return groupList
	@staticmethod
	def getGroupsByProfile(request, socialProfile):
		"""Get all the groups I am subscribed, either those I belong (org or industry) and groups I subscribed with social profile
		@param request: 
		@param socialProfile: 
		@return: groupList"""
		userX = BsUser.getByProfile(request, socialProfile)
		groupList = userX.Groups.all()
		return groupList
	@staticmethod
	def search(request, name):
		"""Search users by name
		@param name: 
		@return: userList"""
		userList = UserDetail.objects.filter(Name__icontains=name)
		return userList
	@staticmethod
	def createProfile(request, user, socialProfile, settings=Constants.SETTINGS_DEFAULT):
		"""Create social profile
		@param request: 
		@param user: UserSys
		@param socialProfile: 
		@param settings: [Optional]
		@return: userX"""
		userX = UserX.objects.create(User=user, SocialProfile=socialProfile, settings=settings)
		return userX

class BsGroup(object):
	@staticmethod
	def create(request, form):
		"""Creates a Ximpia Group. Can be: XimpiaGroup, Industry, SocialGroup, Organization Group (Department), Public or Private.
		@raise UserX.DoesNotExist: """
		ximpiaId = getDataDict(form)['ximpiaId']
		groupName = getDataDict(form)['groupName']
		ximpiaGroup = getDataDict(form)['ximpiaGroup']
		industry = getDataDict(form)['industry']
		socialGroup = getDataDict(form)['socialGroup']
		orgGroup = getDataDict(form)['orgGroup']
		public = getDataDict(form)['public']
		accessGroupIdList = json.loads(getDataDict(form)['accessGroupIdList'])
		tagList = []
		adminList = [request.user]
		user = request.user
		try:
			userX = UserX.objects.get(User=user)
			group = GroupSys.objects.create(name=groupName)
			user.groups.add(group)
			groupX = GroupX(Group=group, Owner=userX)
			if ximpiaGroup != None:
				groupX.XimpiaGroup = ximpiaGroup
			if industry != None:
				groupX.Industry = industry
			if socialGroup != None:
				groupX.SocialGroup = socialGroup
			if orgGroup != None:
				groupX.OrgGroup = orgGroup
			if public != None:
				groupX.Public = public
			# Admins
			groupX.save()
			groupX.Admins.add(userX)
			# AccessGroups
			for accessGroupId in accessGroupIdList:
				accessGroup = GroupX.objects.get(id=accessGroupId)
				groupX.AccessGroups.add(accessGroup)
			userX.Groups.add(groupX)
			# Tags
			while sTag in tagList:
				tag, bTag = Tag.objects.get_or_create(Name=sTag)
				groupX.Tags.add(tag)
		except UserX.DoesNotExist:
			raise UserX.DoesNotExist
	@staticmethod
	def edit(request, form):
		"""Doc."""
		# getFormParameter(form, '') => Checks to obtain value from data or cleaned_data
		groupName = getDataDict(form)['groupName']
		ximpiaGroup = getDataDict(form)['ximpiaGroup']
		industry = getDataDict(form)['industry']
		socialGroup = getDataDict(form)['socialGroup']
		orgGroup = getDataDict(form)['orgGroup']
		public = getDataDict(form)['public']
		accessGroupIdList = json.loads(getDataDict(form)['accessGroupIdList'])
		groupId = getDataDict(form)['groupId']
		adminUserIdList = json.loads(getDataDict(form)['adminUserIdList'])
		ownerUserId = getDataDict(form)['ownerUserId']
		tagList = json.loads(getDataDict(form)['tagList'])
		try:
			groupX = GroupX.objects.get(id=groupId)
			if ximpiaGroup != None:
				groupX.XimpiaGroup = ximpiaGroup
			if industry != None:
				groupX.Industry = industry
			if socialGroup != None:
				groupX.SocialGroup = socialGroup
			if orgGroup != None:
				groupX.OrgGroup = orgGroup
			if public != None:
				groupX.Public = public
			groupX.save()
			# Admins
			groupX.Admins.all().delete()
			for adminUserId in adminUserIdList:
				adminUserX = UserX.objects.get(id=adminUserId)
				groupX.Admins.add(userX)
			# AccessGroups
			groupX.AccessGroups.all().delete()
			for accessGroupId in accessGroupIdList:
				accessGroup = GroupX.objects.get(id=accessGroupId)
				groupX.AccessGroups.add(accessGroup)
		except UserX.DoesNotExist:
			raise UserX.DoesNotExist
		except GroupX.DoesNotExist:
			raise GroupX.DoesNotExist
		except:
			pass
	@staticmethod
	def getById(request, form):
		"""Get group by GroupX id. Appends all data attached."""
		try:
			groupId = getDataDict(form)['groupId']
			groupX = GroupX.objects.select_related().get(id=groupId)
			return groupX
		except GroupX.DoesNotExist:
			raise GroupX.DoesNotExist
	@staticmethod
	def getByName(request, form):
		"""Get group by name. Appends all data attached."""
		try:
			groupName = getDataDict(form)['groupName']
			groupX = GroupX.objects.select_related().get(Group__name = groupName)
			return groupX
		except GroupX.DoesNotExist:
			raise GroupX.DoesNotExist
	@staticmethod
	def getId(request, form):
		"""Get group id giving group name"""
		try:
			groupName = getDataDict(form)['groupName']
			groupId = GroupX.objects.get(Group__name = groupName).id
			return groupId
		except GroupX.DoesNotExist:
			raise GroupX.DoesNotExist
	@staticmethod
	def delete(request, form):
		"""Deletes a group"""
		try:
			groupId = getDataDict(form)['groupId']
			groupX = GroupX.objects.get(id=groupId)
			group = GroupSys.objects.get(id=groupX.Group.id)
			group.delete()
			# Unlink from UserX
			UserX.Groups.get(id=groupId).delete()
			groupX.delete()
		except GroupX.DoesNotExist:
			raise GroupX.DoesNotExist
		except GroupSys.DoesNotExist:
			raise GroupSys.DoesNotExist
	@staticmethod
	def exists(request, form):
		"""Checks if group exists.
		@return: Boolean"""
		groupId = getDataDict(form)['groupId']
		check = GroupX.objects.exists(id=groupId)
		return check
	@staticmethod
	def listGroups(request, form):
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
			userX = UserX.objects.get(User=request.user)
			# Private group :: We assume that private groups will be granted access to other private groups
			myGroupsPrivate = userX.Groups.filter(Public=False)
			groupListNamePrivate = GroupX.objects.filter(AccessGroups__in=myGroupsPrivate)
			groupListTagPrivate = GroupX.objects.filter(AccessGroups__in=myGroupsPrivate)
			# Public groups
			groupListName = GroupX.objects.filter(Public=True)
			groupListTag = GroupX.objects.filter(Public=True)
			# Should merge and order by alpha
			sortDict = {}
			sortList = []
			try:			
				if request.session[Constants.USER_SETTINGS][Constants.SETTINGS_ALLOW_PRIVATE_GRP_SUBS] == True:
					for groupX in groupListNamePrivate:
						sortList.append(groupX.Group.name, groupX)
					for groupX in groupListTagPrivate:
						sortList.append(groupX.Group.name, groupX)
			except KeyError:
				pass
			for groupX in groupListName:
				sortList.append(groupX.Group.name, groupX)
			for groupX in groupListTag:
				sortList.append(groupX.Group.name, groupX)
			sortList.sort()
			groupList = []
			i = 1
			for tuple in sortList:
				if i>= iStart and i<iEnd:
					groupList.append(tuple[1])
				if i> iEnd:
					break
		except UserX.DoesNotExist:
			raise UserX.DoesNotExist
		return groupList
	@staticmethod
	def searchMyGroupsByNameTags(request, form):
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
			userX = UserX.objects.get(User=request.user)
			# Search for Name and Tag
			groupListName = userX.Groups.filter(Group__name__istartswith=query)
			groupListTag = []
			for word in wordList:
				groupListTagTmp = userX.Groups.filter(Group__name__istartswith=query)
				for field in groupListTagTmp:
					groupListTag.append(field)
			sortDict = {}
			sortList = []
			for groupX in groupListName:
				sortList.append(groupX.Group.name, groupX)
			for groupX in groupListTag:
				sortList.append(groupX.Group.name, groupX)
			sortList.sort()
			groupList = []
			i = 1
			for tuple in sortList:
				if i>= iStart and i<iEnd:
					groupList.append(tuple[1])
				if i> iEnd:
					break
		except UserX.DoesNotExist:
			raise UserX.DoesNotExist
		return groupList
	@staticmethod
	def searchGroupsByNameTags(request, form):
		"""Search groups I have access in name and tags, sorted alphabetically. Called when users start typing group name in tooltip #abcd...
		@return: groupList : [GroupX,...]"""
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
			userX = UserX.objects.get(User=request.user)
			# Private group :: We assume that private groups will be granted access to other private groups
			myGroupsPrivate = userX.Groups.filter(Public=False)
			groupListNamePrivate = GroupX.objects.filter(Group__name__istartswith=query, AccessGroups__in=myGroupsPrivate)
			groupListTagPrivate = []
			for word in wordList:
				groupListTagPrivateTmp = GroupX.objects.filter(Tags__Name__icontains=word, AccessGroups__in=myGroupsPrivate)
				for field in groupListTagPrivateTmp:
					groupListTagPrivate.append(field)
			# Public groups
			groupListName = GroupX.objects.filter(Group__name__istartswith=query, Public=True)
			groupListTag = []
			for word in wordList:
				groupListTagTmp = GroupX.objects.filter(Tags__Name__icontains=query, Public=True)
				for field in groupListTagTmp:
					groupListTag.append(field)
			# Should merge and order by alpha
			sortDict = {}
			sortList = []
			try:			
				if request.session[Constants.USER_SETTINGS][Constants.SETTINGS_ALLOW_PRIVATE_GRP_SUBS] == True:
					for groupX in groupListNamePrivate:
						sortList.append(groupX.Group.name, groupX)
					for groupX in groupListTagPrivate:
						sortList.append(groupX.Group.name, groupX)
			except KeyError:
				pass
			for groupX in groupListName:
				sortList.append(groupX.Group.name, groupX)
			for groupX in groupListTag:
				sortList.append(groupX.Group.name, groupX)
			sortList.sort()
			groupList = []
			i = 1
			for tuple in sortList:
				if i>= iStart and i<iEnd:
					groupList.append(tuple[1])
				if i> iEnd:
					break
		except UserX.DoesNotExist:
			raise UserX.DoesNotExist
		return groupList
	@staticmethod
	def hasAccess(request, form, userX, groupX):
		"""Checks in case group is private that my user belongs to a group that has access to the group"""
		accessGroupList = groupX.AccessGroups.all()
		accessGroupIdList = []
		for accessGroup in accessGroupList:
			accessGroupIdList.append(accessGroup.id)
		list = userX.Groups.in_bulk(accessGroupIdList)
		check = False
		if len(list) != 0:
			check = True
		return check
	@staticmethod
	def join(request, form):
		"""Join group"""
		try:
			groupId = getDataDict(form)['groupId']
			groupX = GroupX.objects.get(id=groupId)
			userX = UserX.objects.get(User=request.user)
			if groupX.Public == False:
				hasAccess = BsGroup.hasAccess(request, form, userX)
				if hasAccess:
					group = groupX.Group
					request.user.groups.add(group)
					userX.Groups.add(groupX)
			else:
				group = groupX.Group
				request.user.groups.add(group)
				userX.Groups.add(groupX)
		except GroupX.DoesNotExist:
			raise GroupX.DoesNotExist
		except UserX.DoesNotExist:
			raise UserX.DoesNotExist
	@staticmethod
	def leave(request, form):
		"""Leave group"""
		try:
			groupId = getDataDict(form)['groupId']
			groupX = GroupX.objects.get(id=groupId)
			# Delete django link from user to group
			request.user.groups.get(id=groupX.Group.id).delete()
			userX = UserX.objects.get(User=request.user)
			# Delete Ximpia link from userX to groupX
			userX.Groups.get(id=groupX.id).delete()
		except GroupX.DoesNotExist:
			raise GroupX.DoesNotExist
		except UserX.DoesNotExist:
			raise UserX.DoesNotExist

class BsSocial(object):
	@staticmethod
	def followGroup(request, groupIdSource, groupIdTarget):
		"""Follow group, I will get all status from the group with hashtah '#Group Name'. 
		@param groupIdSource: 
		@param groupIdTarget: """
		try:
			groupTarget = GroupX.objects.get(groupIdTarget)
			groupSource = GroupX.objects.get(groupIdSource)
			if groupTarget.Public == False:
				doFollow = groupTarget.AccessGroups.exists(Group=groupSource)
			else:
				doFollow = True
			if doFollow:
				groupFollow = GroupFollow.objects.create(GroupSource=groupSource, GroupTarget=groupTarget)
			else:
				# Raise exception XimpiaException with message
				pass
		except GroupX.DoesNotExist:
			raise GroupX.DoesNotExist
	@staticmethod
	def unfollowGroup(request, groupIdSource, groupIdTarget):
		"""Unfollow group target from source group, we delete the table GroupFollow for that criteria"""
		try:
			groupTarget = GroupX.objects.get(groupIdTarget)
			groupSource = GroupX.objects.get(groupIdSource)
			GroupFollow.objects.get(GroupSource=groupSource, GroupTarget=groupTarget).delete()
		except GroupX.DoesNotExist:
			raise GroupX.DoesNotExist
		except GroupFollow.DoesNotExist:
			raise GroupFollow.DoesNotExist
	@staticmethod
	def blockGroup(request, groupIdSource, groupIdTarget):
		"""Change status of link from groupSource to groupTarget"""
		try:
			groupTarget = GroupX.objects.get(groupIdTarget)
			groupSource = GroupX.objects.get(groupIdSource)
			groupFollow = GroupFollow.objects.get(GroupSource=groupSource, GroupTarget=groupTarget)
			groupFollow.Status = Constants.BLOCKED
			groupFollow.save()
		except GroupX.DoesNotExist:
			raise GroupX.DoesNotExist
		except GroupFollow.DoesNotExist:
			raise GroupFollow.DoesNotExist
	@staticmethod
	def unblockGroup(request, groupIdSource, groupIdTarget):
		"""Change status of link from groupSource to groupTarget"""
		try:
			groupTarget = GroupX.objects.get(groupIdTarget)
			groupSource = GroupX.objects.get(groupIdSource)
			groupFollow = GroupFollow.objects.get(GroupSource=groupSource, GroupTarget=groupTarget)
			groupFollow.Status = Constants.OK
			groupFollow.save()
		except GroupX.DoesNotExist:
			raise GroupX.DoesNotExist
		except GroupFollow.DoesNotExist:
			raise GroupFollow.DoesNotExist
	@staticmethod
	def listFollows(request, groupIdSource, page, numberMatches=Constants.NUMBER_MATCHES):
		"""List of groups that we follow
		@param groupIdSource: 
		@param page: 1-XX
		@param numberMatches: Constants.NUMBER_MATCHES [optional]
		@return: list : List of Groups"""
		try:
			iStart, iEnd = getPagingStartEnd(page, numberMatches)
			groupSource = GroupX.objects.get(groupIdSource)
			list = GroupFollow.objects.filter(GroupSource=groupSource)[iStart:iEnd]
		except GroupX.DoesNotExist:
			raise GroupX.DoesNotExist
		return list
	@staticmethod
	def listFollowed(request, groupIdTarget, page, numberMatches=Constants.NUMBER_MATCHES):
		"""List of groups that follow us
		@param groupIdTarget: 
		@param page: 1-XX
		@param numberMatches: Constants.NUMBER_MATCHES [optional]
		@return: list : List of Groups"""
		try:
			iStart, iEnd = getPagingStartEnd(page, numberMatches)
			groupTarget = GroupX.objects.get(groupIdTarget)
			list = GroupFollow.objects.filter(GroupTarget=groupTarget)[iStart:iEnd]
		except GroupX.DoesNotExist:
			raise GroupX.DoesNotExist
		return list

class BsStatus(object):
	@staticmethod
	def update(request, status, socialProfile, source=None, fileIdList=[], tagIdList=[], linkIdList=[], groupIdList=[]):
		"""Update status
		@param status: Status message. In case of ximpia status, the html code. In case of other sources, json obtained.
		@param source: Used for twitter, facebook, etc... statuses [optional]
		@param fileIdList: [optional] 
		@param tagIdList: [optional]
		@param linkIdList: [optional]
		@param groupIdList: [optional]"""
		try:	
			# Message
			statusMessage = StatusMessage.objects.create(Message=status)
			postId = statusMessage.id
			# Files
			fileDict = BsFile.getMap(request, fileIdList)
			for fileId in fileIdList:
				statusMessage.Files.add(file)
			# Tags
			tagDict = BsTag.getMap(request, tagIdList)
			for tagId in tagIdList:
				statusMessage.Files.add(tagDict[tagId])
			# Links
			linkDict = BsLink.getMap(request, linkIdList)
			for linkId in linkIdList:
				statusMessage.Files.add(linkDict[linkId])
			# Stream
			streamGroupList = []
			userX = BsUser.getByProfile(request, socialProfile)
			myGroupList = BsUser.getMyGroupsByProfile(request, socialProfile)
			groupFollowerList = GroupFollow.objects.filter(GroupTarget__in=myGroupList)			
			# Groups mentioned with hash tag #GroupName
			if len(groupIdList) != 0: 
				groupList = GroupX.objects.filter(pk__in=groupIdList)
				for group in groupList:
					groupFollowerList.append(group)
			if source == None:
				for group in groupFollowerList:
					if group.OrgGroup == True:
						streamGroupList.append((group, group.Account, group.Public, Constants.XIMPIA))
					else:
						streamGroupList.append((group, '', group.Public, Constants.XIMPIA))
			else:
				for group in groupFollowerList:
					streamGroupList.append((group, '', True, source))						
			for tuple in streamGroupList:
				group, account, public, source = tuple 
				groupStream = GroupStream(
							User=userX,  
							Group=group,  
							Message=statusMessage, 
							PostId=postId, 
							Public=public,
							Source=source)
				if account != '':
					groupStream.Account = account
				groupStream.save()
		except UserX.DoesNotExist:
			raise UserX.DoesNotExist
	@staticmethod
	def getList(request, socialProfile, numberMatches=50):
		"""Get status for all groups I belong and groups I belong follow
		@param socialProfile: 
		@param numberMatches: [optional]
		@return: statusList"""
		try:
			myGroupList = BsUser.getGroupsByProfile(request, socialProfile)
			groupFollowList = GroupFollow.objects.filter(GroupSource__in=myGroupList)
			statusList = GroupStream.objects.select_related().filter(Group__in=groupFollowList)[:numberMatches]
		except UserX.DoesNotExist:
			raise UserX.DoesNotExist
		return statusList
	@staticmethod
	def like(request, postId, socialProfile):
		"""Like the status
		@param postId: 
		@param socialProfile: """
		try:
			groupStream = GroupStream.objects.get(PostId=postId)
			like = BsLike.get(request)
			groupStream.Like.add(like)
		except GroupStream.DoesNotExist:
			raise GroupStream.DoesNotExist
		except UserX.DoesNotExist:
			raise UserX.DoesNotExist
	@staticmethod
	def comment(request, postId, socialProfile, content, public=True, fileIdList=[]):
		"""Comment status
		@param request: 
		@param postId: 
		@param socialProfile: 
		@param content: 
		@param public: [optional, default True]
		@param fileIdList: [optional]"""
		try:
			groupStream = GroupStream.objects.get(PostId=postId)
			comment = BsComment.add(request, content, socialProfile, public, fileIdList)
			groupStream.Comments.add(comment)
		except GroupStream.DoesNotExist:
			raise GroupStream.DoesNotExist
		except UserX.DoesNotExist:
			raise UserX.DoesNotExist
		except Comment.DoesNotExist:
			raise Comment.DoesNotExist
	@staticmethod
	def share(request):
		pass
	@staticmethod
	def makePublic(request):
		pass

class BsTag(object):
	@staticmethod
	def getCreate(request, tagId=None, tag='', public=False, systemTag=False):
		"""Get or create a tag. If given tagId, we get tag. If we have more data we get or create
		@param tagId: [optional]
		@param tag: [optional]
		@param public: False [optional]
		@param systemFlag: [optional]
		@return: tag"""
		try:
			if tagId:
				tag = Tag.objects.get(id=tagId)
				tag.Popularity += 1
				tag.save()
			else:
				tag, create = Tag.objects.get_or_create(Tag=tag, Public=public, SystemTag=systemTag)
		except Tag.DoesNotExist:
			raise Tag.DoesNotExist
		return tag
	@staticmethod
	def getMap(request, tagIdList):
		"""Get tag map for a list if tagId"""
		dict = {}
		if len(tagIdList) != 0:
			list = Tag.objects.filter(id__in=tagIdList)
			for tag in list:
				dict[tag.id] = tag
		return dict

class BsComment(object):
	@staticmethod
	def add(request, content, socialProfile, public=False, fileIdList=[]):
		"""Create comment for user
		@param content: Comment text
		@param socialProfile: 
		@param public: If comment private for organization domain or public [optional]
		@param fileIdList: File attached to comment [optional]
		@return: comment"""
		try:
			userX = BsUser.getByProfile(request, socialProfile)
			comment = Comment.objects.create(User=userX, Message=content, Public=public)
			# Files
			if len(fileIdList) != 0:
				fileDict = BsFile.getMap(request, fileIdList)
				for fileId in fileIdList:
					file = fileDict[fileId]
					comment.Files.add(file)
		except UserX.DoesNotExist:
			raise UserX.DoesNotExist
		return comment
	@staticmethod
	def delete(request, commentId):
		"""Deletes a comment
		@param commentId: """
		try:
			comment = Comment.objects.get(id=commentId)
			comment.delete()
			#TODO: Manage deletes by owner, staff and organization administrators
		except Comment.DoesNotExist:
			raise Comment.DoesNotExist
	@staticmethod
	def like(request, commentId):
		"""Likes a comment
		@param commentId: """
		try:
			like = BsLike.get(request)
			comment = Comment.objects.get(id=commentId)
			comment.Like.add(like)
		except Comment.DoesNotExist:
			raise Comment.DoesNotExist
	@staticmethod
	def share(request):
		"""Share a comment"""
		pass

class BsLike(object):
	@staticmethod
	def get(request):
		"""Get like object for signed on user. It uses get_or_create()"""
		userX = BsUser.get(request)
		# Like
		like, bCreated = Like.objects.get_or_create(User=userX)
		like.Number += 1
		like.save()
		return like

class BsLink(object):
	@staticmethod
	def getCreate(request, linkId=None, url=''):
		"""Get or create a link. If given linkId, we get link. If we have more data we get or create link
		@param linkId: [optional]
		@param url: [optional]
		@return: link"""
		try:
			if linkId:
				link = Link.objects.get(id=linkId)
				link.NumberShared += 1
				link.save()
			else:
				oUrl = util.resources.Url()
				domain = oUrl.getDomainName(url)
				link, create = Link.objects.get_or_create(Url=url, Domain=domain)
		except Link.DoesNotExist:
			raise Link.DoesNotExist
		return link
	@staticmethod
	def getMap(request, linkIdList):
		"""Get tag map for a list if tagId
		@param linkIdList: 
		@return: dict"""
		dict = {}
		if len(linkIdList) != 0:
			list = Link.objects.filter(id__in=linkIdList)
			for link in list:
				dict[link.id] = link
		return dict

class BsMessage(object):
	@staticmethod
	def send(request, form):
		"""Sends a message, writing into table MessageReceived if ximpia user and MessageSent"""
		userIdToList = json.loads(getFormDataValue(form, 'usersToList'))
		groupIdFrom = getFormDataValue(form, 'groupFrom')
		groupIdToList = json.loads(getFormDataValue(form, 'groupToList'))
		addrList = json.loads(getFormDataValue(form, 'addrList'))
		tagIdList = json.loads(getFormDataValue(form, 'tagIdList'))
		fileIdList = json.loads(getFormDataValue(form, 'fileIdList'))
		linkIdList = json.loads(getFormDataValue(form, 'linkIdList'))
		discussionTopic = getFormDataValue(form, 'discussionTopic')
		discussionFileIdList = json.loads(getFormDataValue(form, 'discussionFileList'))
		discussionTagIdList = json.loads(getFormDataValue(form, 'discussionTagList'))
		summary = getFormDataValue(form, 'summary')
		message = getFormDataValue(form, 'message')
		secure = getFormDataValue(form, 'secure')
		sendAsGroup = getFormDataValue(form, 'sendAsGroup')
		try:
			# MessageId
			messageId = random.randint(1,999999999999)
			bMessageId = MessageSent.objects.exists(Message__id=messageId)
			while bMessageId:
				messageId = random.randint(1,999999999999)
				bMessageId = MessageSent.objects.exists(Message__id=messageId)
			userX = UserX.objects.get(User=request.user)
			# Message
			message = Message(Summary=summary, Message=message, Secure=secure)
			# MessageSent
			messageSent = MessageSent(Message=message, UserFrom=userX)
			GroupDict = {}
			if groupIdFrom != None:
				groupFrom = GroupX.objects.get(id=groupIdFrom)
				GroupDict[groupIdFrom] = groupFrom
				messageSent.GroupFrom = groupFrom
			for groupIdTo in groupIdToList:
				groupTo = GroupX.objects.get(id=groupIdTo)
				GroupDict[groupIdTo] = groupTo
				messageSent.GroupTo.add(groupTo)
			messageSent.save()
			# Discussion
			if discussionTopic != '':
				discussion = Discussion.objects.create(UserPosting=userX, Topic=discussionTopic)
				# UsersParticipate
				for userParticipateId in userToList:
					userParticipate = UserX.objects.get(id=userParticipateId)
					discussion.UsersParticipate.add(userParticipate)
				# Files
				for fileId in discussionFileIdList:
					file = File.objects.get(id=fileId)
					discussion.Files.add(file)
				# Tags
				for tagId in discussionTagIdList:
					tag = Tag.objects.get(id=tagId)
					discussion.Tags.add(tag)
				message.Discussion = discussion
			message.save()
			# UsersTo
			for userId in userToList:
				userTo = UserX.objects.get(id=userId)
				messageSent.UsersTo.add(userTo)
			# AddrsTo
			for addrNameList in addrList:
				type, addrName = addrNameList
				addr, created = MessageAddr.objects.get_or_create(Address=addrName, Type=type)
				messageSent.AddrsTo.add(addr)
			# Tags
			tagDict = BsTag.getMap(request, tagIdList)
			for tagId in tagIdList:
				message.Tags.add(tagDict[tagId])
			# Files
			for fileId in fileIdList:
				file = File.objects.get(id=fileId)
				message.Files.add(file)
			# Links
			for linkId in linkIdList:
				link = Link.objects.get(id=linkId)
				message.Links.add(link)
			# Write to MessageReceived for all Ximpia Users and Groups
			for userId in userToList:
				userTo = UserX.objects.get(id=userId)
				messageReceived = MessageReceived(Message=message, UserTo=userTo)
				if sendAsGroup:
					messageReceived.GroupFrom = groupFrom
				else:
					messageReceived.UserFrom = userX
				messageReceived.save()
			for groupIdTo in groupToList:
				if GroupDict.has_key(groupIdTo):
					group = GroupDict[groupIdTo]
					messageReceived = MessageReceived(Message=message, GroupTo=group)
					if sendAsGroup:
						messageReceived.GroupFrom = groupFrom
					else:
						messageReceived.UserFrom = userX
					messageReceived.save()
		except UserX.DoesNotExist:
			raise UserX.DoesNotExist
		except GroupX.DoesNotExist:
			raise GroupX.DoesNotExist
		except File.DoesNotExist:
			raise File.DoesNotExist
		except Tag.DoesNotExist:
			raise Tag.DoesNotExist
		except Link.DoesNotExist:
			raise Link.DoesNotExist
	@staticmethod
	def getFromList(request, form):
		"""Get list of groups that I can send messages from. First row will be the user and then the groups the
		user is listed as admin.
		@return: tuple : (id, name)"""
		list = []
		try:
			userX = UserX.objects.get(User=request.user)
			groupList = GroupX.objects.filter(Admins=userX)
			list.append((userX.User.id, userX.getFullName()))
			for group in groupList:
				list.append((group.id, group.Group.name))
		except UserX.DoesNotExist:
			raise UserX.DoesNotExist
		return list
	@staticmethod
	def search(request, form):
		"""Search for a query in summary and message fields in either sent messages or received messages. It searches
		archived messages too."""
		mode = getFormDataValue(form, 'mode')
		page = getFormDataValue(form, 'page')
		numberMatches = getFormDataValue(form, 'numberMatches')
		receiveGroup = getFormDataValue(form, 'receiveGroup')
		query = getFormDataValue(form, 'query')
		groupIdList = json.loads(getFormDataValue(form, 'groupIdList'))
		if not archived:
			archived = False
		if not numberMatches:
			numberMatches = Constants.NUMBER_MATCHES
		if not page:
			page = 1
		try:
			iStart, iEnd = getPagingStartEnd(page, numberMatches)
			userX = UserX.objects.get(User=request.user)
			if mode == Constants.MSG_MODE_REC:
				messageList = MessageReceived.objects.select_related().filter(
											Q(UserTo=userX) | 
											Q(GroupTo__in=groupIdList),
											Q(Message__Message__search=query) |
											Q(Message__Summary__search=query))[iStart:iEnd]
			else:
				messageList = MessageSent.objects.select_related().filter(
											Q(UserFrom=userX) | 
											Q(GroupFrom__in=groupIdList),
											Q(Message__Message__search=query) |
											Q(Message__Summary__search=query))[iStart:iEnd]
		except UserX.DoesNotExist:
			raise UserX.DoesNotExist
		return messageList
	@staticmethod
	def list(request, form):
		"""List message from received or sent collections."""
		mode = getFormDataValue(form, 'mode')
		archived = getFormDataValue(form, 'archived')
		page = getFormDataValue(form, 'page')
		numberMatches = getFormDataValue(form, 'numberMatches')
		receiveGroup = getFormDataValue(form, 'receiveGroup')
		groupIdList = json.loads(getFormDataValue(form, 'groupIdList'))
		if not archived:
			archived = False
		if not numberMatches:
			numberMatches = Constants.NUMBER_MATCHES
		if not page:
			page = 1
		try:
			iStart, iEnd = getPagingStartEnd(page, numberMatches)
			userX = UserX.objects.get(User=request.user)
			if mode == Constants.MSG_MODE_REC:
				messageList = MessageReceived.objects.select_related().filter(
											Q(UserTo=userX) | 
											Q(GroupTo__in=groupIdList), 
											Archived=archived)[iStart:iEnd]
			else:
				messageList = MessageSent.objects.select_related().filter(
											Q(UserFrom=userX) | 
											Q(GroupFrom__in=groupIdList), 
											Archived=archived)[iStart:iEnd]
		except UserX.DoesNotExist:
			raise UserX.DoesNotExist
		return messageList
	@staticmethod
	def archiveList(request, form):
		"""Archive and unarchive list of messages be id, one or more than one message"""
		messageIdList = json.loads(getFormDataValue(form, 'messageIdList'))
		mode = getFormDataValue(form, 'mode')
		if mode == Constants.ARCHIVE:
			Message.objects.filter(id__in=messageIdList).update(Archived=True)
		else:
			Message.objects.filter(id__in=messageIdList).update(Archived=False)
	@staticmethod
	def get(request, form):
		"""Get message. Either from received, received archived, or sent messages. Returns all objects attached in one query."""
		messageId = getFormDataValue(form, 'messageId')
		mode = getFormDataValue(form, 'mode')
		userIdTo = getFormDataValue(form, 'userIdTo')
		groupIdTo = getFormDataValue(form, 'groupIdTo')
		archived = getFormDataValue(form, 'archived')
		if not archived:
			archived = False
		if mode == Constants.MSG_MODE_REC:
			try:
				# User or Group
				if userIdTo:
					message = MessageReceived.objects.select_related().get(
											UserTo__id=userIdTo, 
											Message__id=messageId, 
											Message__Archived=archived)
				elif groupIdTo:
					message = MessageReceived.objects.select_related().get(
											GroupTo__id=groupIdTo, 
											Message__id=messageId,
											Message__Archived=archived)
			except MessageReceived.DoesNotExist:
				raise MessageReceived.DoesNotExist
			except MessageReceived.MultiObjectsReturned:
				raise MessageReceived.MultiObjectsReturned
		else:
			try:
				message = MessageSent.objects.select_related().get(Message__id=messageId)
			except MessageSent.DoesNotExist:
				raise MessageSent.DoesNotExist
			except MessageSent.MultiObjectsReturned:
				raise MessageSent.MultiObjectsReturned
		return message
	@staticmethod
	def reply(request, form):
		"""Replies message. Writes into MessageReply"""
		replyMessage = getFormDataValue(form, 'replyMessage')
		messageId = getFormDataValue(form, 'messageId')
		groupIdFrom = getFormDataValue(form, 'groupIdFrom')
		fileIdList = json.loads(getFormDataValue(form, 'fileIdList'))
		tagIdList = json.loads(getFormDataValue(form, 'tagIdList'))
		linkIdList = json.loads(getFormDataValue(form, 'linkIdList'))
		sendAsGroup = getFormDataValue(form, 'sendAsGroup')
		try:
			# Message
			message = Message.objects.get(id=messageId)
			# Create MessageReply
			messageReply = MessageReply(Message=message, MessageContent=replyMessage)
			if sendAsGroup:
				groupX = GroupX.objects.get(id=groupIdFrom)
				messageReply.GroupFrom = groupX
			else:
				userX = UserX.objects.get(User__id=request.user)
				messageReply.UserFrom = userX
			messageReply.save()
			# Link to MessageReceived for all entries related to messageId		
			messageList = MessageReceived.objects.filter(Message__id=messageId)
			for message in messageList:
				message.Replies.add(messageReply)
			# Link to MessageSent
			messageSent = MessageSent.objects.get(Message__id=messageId)
			messageSent.Replies.add(messageReply)
			# Files
			for fileId in fileIdList:
				file = File.objects.get(id=fileId)
				messageReply.Files.add(file)
			# Tags
			for tagId in tagIdList:
				tag = Tag.objects.get(id=tagId)
				messageReply.Tags.add(tag)
			# Links
			for linkId in linkIdList:
				link = Link.objects.get(id=linkId)
				messageReply.Links.add(link)
		except MessageSent.DoesNotExist:
			raise MessageSent.DoesNotExist
		except UserX.DoesNotExist:
			raise UserX.DoesNotExist
		except GroupX.DoesNotExist:
			raise GroupX.DoesNotExist
		except File.DoesNotExist:
			raise File.DoesNotExist
		except Tag.DoesNotExist:
			raise Tag.DoesNotExist
		except Link.DoesNotExist:
			raise Link.DoesNotExist
	@staticmethod
	def getLogList(request, form):
		"""Get log activity list for message for all users"""
		messageId = getDataDict(form)['messageId']
		messageLogList = MessageLog.objects.filter(MessageId=messageId)
		return messageLogList
	@staticmethod
	def getLogDetail(request, form):
		"""Get log of read and downloads activities for message and user"""
		messageId = getDataDict(form)['messageId']
		userTo = getDataDict(form)['userTo']
		messageLogList = MessageLog.objects.filter(MessageId=messageId, UserTo__User__username=userTo)
		return messageLogList
	@staticmethod
	def addDiscussionThread(request, form):
		"""Add thread to discussion.
		@param discussionId: 
		@param thread: 
		@param fileList: 
		@param content: """
		discussionId = getDataDict(form)['discussionId']
		thread = getDataDict(form)['thread']
		fileList = json.loads(getDataDict(form)['fileList'])
		content = getDataDict(form)['content']
		tagList = json.loads(getDataDict(form)['tagList'])
		try:
			userX = UserX.objects.get(User=request.user)
			discussion = Discussion.objects.get(id=discussionId)
			DiscussionThread.objects.create(
					User=userX, 
					Discussion=discussion, 
					Thread=thread, 
					Content=content)
			for fileId in fileList:
				file = File.objects.get(id=fileId)
				DiscussionThread.Files.add(file)
			tagIdDict = BsTag.getMap(request, tagList)
			for tagId in tagList:
				DiscussionThread.Tags.add(tagIdDict[tagId])
		except UserX.DoesNotExist:
			raise UserX.DoesNotExist
		except Discussion.DoesNotExist:
			raise Discussion.DoesNotExist
		except File.DoesNotExist:
			raise File.DoesNotExist
	@staticmethod
	def share(request, form):
		"""Allows to share the message threads to other people than recipients, publish in twitter or facebook. All message objects"""
		# Implemented after sharing logic
		pass
	@staticmethod
	def makePublic(request, form):
		"""Doc."""
		pass
	@staticmethod
	def like(request, form):
		"""Like request for messages, replies, discussions and discussion threads"""
		try:
			discussionId = getFormDataValue(form, 'discussionId')
			discussionThreadId = getFormDataValue(form, 'discussionThreadId')
			messageId = getFormDataValue(form, 'messageId')
			like = BsLike.get(request)
			# Discussion
			if discussionId:
				discussion = Discussion.objects.get(id=discussionId)
				discussion.Like.add(like)
			# DiscussionThread
			if discussionThreadId:
				discussionThread = DiscussionThreads.objects.get(id=discussionThreadId)
				discussionThread.Like.add(like)
			# Messages
			if messageId:
				message = Message.objects.get(id=messageId)
				message.Like.add(like)
		except Discussion.DoesNotExist:
			raise Discussion.DoesNotExist
		except DiscussionThreads.DoesNotExist:
			raise DiscussionThreads.DoesNotExist
	@staticmethod
	def comment(request, form):
		"""Doc."""
		discussionId = getDataDict(form)['discussionId']
		discussionThreadId = getDataDict(form)['discussionThreadId']
		commentContent = getDataDict(form)['commentContent']
		try:		
			userX = UserX.objects.get(User__id=request.user)
			comment = Comment.objects.create(
						User=userX, 
						Message=commentContent,
						Public=False)
			discussionThread = DiscussionThread.objects.get(id=discussionThreadId)
			discussionThread.Comments.add(comment)
		except UserX.DoesNotExist:
			raise UserX.DoesNotExist
		except DiscussionThread.DoesNotExist:
			raise DiscussionThread.DoesNotExist
