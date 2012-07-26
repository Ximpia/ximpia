from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User, Group

from ximpia.core.models import BaseModel

import constants as K
from choices import Choices

#TODO: Video tags, video categories
#TODO: Video model to videos app

class Video(BaseModel):
	"""Videos"""
	embedCode = models.CharField(max_length=500,
			verbose_name = _('Embed Code'), help_text = _('Embed code from Video provider'))
	name = models.CharField(max_length=30,
			verbose_name = _('Name'), help_text = _('Media name'))
	title = models.CharField(max_length=50,
			verbose_name = _('Title'), help_text = _('Media Title'))
	description = models.CharField(max_length=500,
			verbose_name = _('Description'), help_text = _('Media Description, shown in search'))
	isFeatured = models.BooleanField(default=False,
			verbose_name = _('Is Featured?'), help_text = _('Is media shown as featured? Will be placed first on search and bigger'))
	tags = ''
	categories = ''
	def __unicode__(self):
		return str(self.name)
	class Meta:
		db_table = 'SITE_VIDEO'
		verbose_name = _('Video')
		verbose_name_plural = _('Videos')
		ordering = ['-isFeatured']

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
		db_table = 'SITE_ADDRESS'
		verbose_name = _('Address')
		verbose_name_plural = _('Addresses')

class UserChannel(BaseModel):
	"""Every user can have one or more social channels. In case social channels are disabled, only one registry will
	exist for each user."""
	user = models.ForeignKey(User, 
				verbose_name = _('User'), help_text = _('User'))
	groups = models.ManyToManyField(Group,
				verbose_name = _('Groups'), help_text = _('Groups'))
	title = models.CharField(max_length=20, 
				verbose_name = _('Channel Title'), help_text=_('Title for the social channel'))
	name = models.CharField(max_length=20, default=K.USER,
				verbose_name = _('Social Channel Name'), help_text = _('Name for the social channel'))
	"""isCompany = models.BooleanField(default=False,
				verbose_name=_('Company'), help_text=_('Is Company?'))"""
	def __unicode__(self):
		return str(self.user.username) + '-' + str(self.name)
	def getGroupById(self, groupId):
		"""Get group by id"""
		groups = self.groups.filter(pk=groupId)
		if len(groups) != 0:
			value = groups[0]
		else:
			value = None
		return value
	def getFullName(self):
		"""Get full name: firstName lastName"""
		name = self.user.get_full_name()
		return name
	class Meta:
		db_table = 'SITE_USER'
		verbose_name = 'User'
		verbose_name_plural = "Users"
		unique_together = ("user", "name")

class GroupChannel(BaseModel):
	"""Ximpia Group Model."""
	group = models.ForeignKey(Group, unique=True,
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
	account = models.ForeignKey('site.Organization', 'account', null=True, blank=True,
				verbose_name = _('Account'), help_text = _('Account name'))
	isPublic = models.BooleanField(default=True,
				verbose_name = _('Public'), help_text = _('Group is public'))
	accessGroups = models.ManyToManyField('self', related_name='group_access', null=True, blank=True,
				verbose_name = _('Access Groups'), help_text = _('Groups that have access to this group'))
	tags = models.ManyToManyField('site.Tag', null=True, blank=True,
				verbose_name = _('Tags'), help_text = _('Tags'))
	owner = models.ForeignKey('site.UserChannel', related_name='group_owner', null=True, blank=True,
				verbose_name = _('Group Owner'), help_text = _('Owner of group'))
	admins = models.ManyToManyField('site.UserChannel', related_name='group_admins', null=True, blank=True,
				verbose_name = _('Administrators'), help_text = _('Administrators'))
	managers = models.ManyToManyField('site.UserChannel', related_name='group_managers', null=True, blank=True,
				verbose_name = _('Managers'), help_text = _('Managers'))
	def __unicode__(self):
		if self.account != None:
			return str(self.account) + '-' + str(self.group)
		else:
			return str(self.group)
	class Meta:
		db_table = 'SITE_GROUP'
		verbose_name = 'Group Channel'
		verbose_name_plural = "Group Channels"

class SocialNetwork(BaseModel):
	myType = models.ForeignKey('core.CoreParam', limit_choices_to={'mode__lte': K},
				verbose_name = _('Social Network Type'), help_text = _('Type of social network'))
	def __unicode__(self):
		return str(self.myType)
	def getName(self):
		return self.myType.name
	class Meta:
		db_table = 'SITE_SOCIAL_NETWORK'
		verbose_name = _('Social Network')
		verbose_name_plural = _("Social Networks")

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
		db_table = 'SITE_SOCIAL_ORG'
		verbose_name = _('Social Network for Organization')
		verbose_name_plural = _('Social Networks for Organization')

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
		db_table = 'SITE_SOCIAL_GROUP'
		verbose_name = _('Social Network for Organization Group')
		verbose_name_plural = _('Social Networks for Organization Group')

class SocialNetworkUser(models.Model):
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
		db_table = 'SITE_SOCIAL_USER'
		verbose_name = 'Social Network for User'
		verbose_name_plural = "Social Networks for User"

class Organization(BaseModel):
	"""Organization Model"""
	invitedByUser = models.ForeignKey(User, null=True, blank=True,
			verbose_name = _('Invited By User'), help_text = _('Invited by user'))
	invitedByOrg = models.ForeignKey('self', null=True, blank=True,
			verbose_name = _('Invited By Organization'), help_text = _('Invited by Organization'))
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
	industries = models.ManyToManyField('site.GroupChannel', limit_choices_to={'industry': True}, related_name='organization_industries',
			verbose_name = _('Industries'), help_text = _('Industries'))
	addresses = models.ManyToManyField('site.Address', through='AddressOrganization', related_name='organization_addresses', 
			verbose_name = _('Addresses'), help_text = _('Addresses'))
	phone = models.CharField(max_length=20, null=True, blank=True,
			verbose_name = _('Phone'), help_text = _('Phone'))
	fax = models.CharField(max_length=20, null=True, blank=True,
			verbose_name = _('Fax'), help_text = _('Fax'))
	groups = models.ManyToManyField('site.GroupChannel', through='OrganizationGroup',
			verbose_name = _('Groups'), help_text = _('Organization Groups'))
	socialNetworks = models.ManyToManyField('SocialNetwork', through='SocialNetworkOrganization',
			verbose_name = _('Social Networks'), help_text = _('Social Networks'))
	description = models.CharField(max_length=500, null=True, blank=True,
			verbose_name = _('Description'), help_text = _('Description'))
	isValidated = models.BooleanField(default=False,
			verbose_name = _('Validated'), help_text = _('Validated'))
	def __unicode__(self):
		return str(self.account)
	class Meta:
		db_table = 'SITE_ORGANIZATION'
		verbose_name = _('Organization')
		verbose_name_plural = _("Organizations")

class AddressOrganization(BaseModel):
	"""Address Organization Model"""
	addressType = models.CharField(max_length=20, choices=Choices.ADDRESS_TYPE,
			verbose_name = _('Address Type'), help_text = _('Address type'))
	organization = models.ForeignKey('Organization',
			verbose_name = _('Organization'), help_text = _('Organization'))
	address = models.ForeignKey('Address',
			verbose_name = _('Address'), help_text = _('Address'))
	def __unicode__(self):
		return str(self.pk) + ' ' + str(self.addressType) + ' ' + str(self.organization)
	class Meta:
		db_table = 'SITE_ORGANIZATION_ADDRESS'
		verbose_name = _('Address for Organization')
		verbose_name_plural = _('Addresses for Organization')

class OrganizationGroup(BaseModel):
	"""Organization Group Model (Departments, groups of people, etc...)."""
	group = models.ForeignKey('site.GroupChannel',
			verbose_name = _('Group'), help_text = _('Group'))
	organization = models.ForeignKey('site.Organization',
			verbose_name = _('Organization'), help_text = _('Organization'))
	relatedToUp = models.ManyToManyField('self', related_name='org_group_relate_up', null=True, blank=True,
			verbose_name = _('Parent Group'), help_text = _('Parent organization group'))
	relatedToDown = models.ManyToManyField('self', related_name='org_group_relate_down', null=True, blank=True,
			verbose_name = _('Child Group'), help_text = _('Child organization group'))
	socialNetworks = models.ManyToManyField('SocialNetwork', through='SocialNetworkOrganizationGroup',
			verbose_name = _('Social Networks'), help_text = _('Social Networks'))
	def __unicode__(self):
		return str(self.group)
	class Meta:
		db_table = 'SITE_ORGANIZATION_GROUP'
		verbose_name = _('Organization Group')
		verbose_name_plural = _("Organization Groups")

class Category(BaseModel):
	"""Category Model"""
	name = models.CharField(max_length=30,
			verbose_name = _('Name'), help_text = _('Category name'))
	description = models.CharField(max_length=50,
			verbose_name = _('Description'), help_text = _('Category description'))
	popularity = models.IntegerField(default=1, null=True, blank=True,
			verbose_name = _('Popularity'), help_text = _('Popularity'))
	isPublic = models.BooleanField(default=True,
			verbose_name = _('Public'), help_text = _('Is category public?'))
	def __unicode__(self):
		return str(self.name)
	def getText(self):
		return self.name
	class Meta:
		db_table = 'SITE_CATEGORY'
		verbose_name = _('Category')
		verbose_name_plural = _("Categories")
		ordering = ['-popularity']

class Tag(BaseModel):
	"""Tag Model"""
	name = models.CharField(max_length=30,
			verbose_name = _('Name'), help_text = _('Tag name'))
	mode = models.ForeignKey('site.TagMode', related_name='Tag_Mode',
			verbose_name = _('Mode'), help_text = _('Tag mode'))
	popularity = models.IntegerField(default=1, null=True, blank=True,
			verbose_name = _('Popularity'), help_text = _('Popularity'))
	isPublic = models.BooleanField(default=True,
			verbose_name = _('Public'), help_text = _('Is tag public?'))
	def __unicode__(self):
		return str(self.name)
	def getText(self):
		return self.name
	class Meta:
		db_table = 'SITE_TAG'
		verbose_name = _('Tag')
		verbose_name_plural = _("Tags")
		ordering = ['-popularity']

class TagMode(BaseModel):
	"""Tag Mode Model"""
	mode = models.CharField(max_length=30,
			verbose_name = _('Type'), help_text = _('Tag type'))
	isPublic = models.BooleanField(default=True,
			verbose_name = _('Public'), help_text = _('Is tag type public?'))
	def __unicode__(self):
		return str(self.myType)
	class Meta:
		db_table = 'SITE_TAG_MODE'
		verbose_name = _('Tag Mode')
		verbose_name_plural = _("Tag Modes")

class Invitation(BaseModel):
	"""Invitation Model"""
	fromUser = models.ForeignKey(User,
				verbose_name = _('From User'), help_text = _('Invitation from user'))
	fromOrg = models.ForeignKey('site.Organization', null=True, blank=True,
				verbose_name = _('From Account'), help_text = _('Invitation from organization'))
	invitationCode = models.CharField(max_length=10, unique=True,
				verbose_name = _('Inivitation Code'), help_text = _('Invitation Code'))
	email = models.EmailField(unique=True, verbose_name = _('Email'), help_text = _('Email attached to invitation'))
	status = models.CharField(max_length=10, choices=Choices.INVITATION_STATUS, default=K.PENDING,
				verbose_name = _('Status'), help_text = _('Invitation status : pending, used.'))
	number = models.PositiveSmallIntegerField(default=1,
				verbose_name = _('Number'), help_text = _('Invitation Number'))
	message = models.CharField(max_length=200, null=True, blank=True,
				verbose_name = _('Message'), help_text = _('Message'))
	domain = models.CharField(max_length=100, null=True, blank=True,
				verbose_name = _('Domain'), help_text = _('Domain'))
	def __unicode__(self):
		return str(self.fromUser) + ' ' + str(self.invitationCode)
	class Meta:
		db_table = 'SITE_INVITATION'
		verbose_name = _('Invitation')
		verbose_name_plural = _('Invitations')

class XmlMessage(BaseModel):
	"""XML Messages"""
	name = models.CharField(max_length=255,
			verbose_name = _('Name'), help_text = _('Code name of XML'))
	lang = models.CharField(max_length=2, choices=Choices.LANG, default=Choices.LANG_ENGLISH,
			verbose_name = _('Language'), help_text = _('Language for xml'))
	body = models.TextField(verbose_name = _('Xml Content'), help_text = _('Xml content'))
	def __unicode__(self):
		return str(self.name)
	class Meta:
		db_table = 'SITE_XML_MESSAGE'
		verbose_name = _('Xml Message')
		verbose_name_plural = _('Xml Messages')

class Param(BaseModel):
	"""Social Network Parameters"""
	mode = models.CharField(max_length=20, 
			verbose_name=_('Mode'), help_text=_('Parameter Mode'))
	name = models.CharField(max_length=20, 
			verbose_name=_('Name'), help_text=_('Parameter Name'))
	value = models.CharField(max_length=100, null=True, blank=True, 
			verbose_name=_('Value'), help_text=_('Parameter Value for Strings'))
	valueId = models.IntegerField(null=True, blank=True, 
			verbose_name=_('Value Id'), help_text=_('Parameter Value for Integers'))
	valueDate = models.DateTimeField(null=True, blank=True, 
			verbose_name = _('Value Date'), help_text = _('Parameter Value for Date'))
	paramType = models.CharField(max_length=10, choices=Choices.PARAM_TYPE,
			verbose_name=_('Mode'), help_text=_('Mode: either parameter or table'))
	def __unicode__(self):
		return str(self.mode) + ' - ' + str(self.name)
	class Meta:
		db_table = 'SITE_PARAMETER'
		verbose_name = "Parameter"
		verbose_name_plural = "Parameters"

class UserDetail(BaseModel):
	"""Model for UserSocial
	FK : User
	MN: SocialNetworks"""
	user = models.ForeignKey(User,
				verbose_name = _('User'), help_text = _('User'))
	name = models.CharField(max_length=60,
				verbose_name = _('Name'), help_text = _('Name'))
	settings = models.TextField(default = '', null=True, blank=True,
				verbose_name = _('Settings'), help_text = _('Settings'))
	socialNetworks = models.ManyToManyField('SocialNetwork', through='SocialNetworkUser',  null=True, blank=True,
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
	msgPreference = models.CharField(max_length=10, choices=Choices.MSG_PREFERRED, default=K.XIMPIA,
				verbose_name = _('Messaging Preference'), help_text = _('Preference for sending messages: Facebook, Twitter, Email, etc...'))
	hasValidatedEmail = models.BooleanField(default=False,
				verbose_name = _('Validated Email'), help_text = _('User has validated his email address?'))
	filesQuota = models.IntegerField(default=K.FILE_QUOTA_DEFAULT,
				verbose_name = _('File Quota'), help_text = _('Maximum size storage for files in MB'))
	resetPasswordDate = models.DateField(null=True, blank=True, 
				verbose_name = _('Reset Password Date'), help_text = _('Maximum date for reset password link validation'))
	showIntro = models.BooleanField(default=True,
				verbose_name=_('Show Introduction content'), help_text=_('Show introduction content to user for help'))
	def __unicode__(self):
		return str(self.user.username)
	def getSocialNetworkUser(self, socialNetName):
		"""Get social network name for user"""
		nets = self.socialNetworks.filter(myType__name=socialNetName)
		if len(nets) != 0:
			value = nets[0].socialnetworkuserSocial_set.all()[0]
		else:
			value = None
		return value
	class Meta:
		db_table = 'SITE_USER_DETAIL'
		verbose_name = 'UserDetail'
		verbose_name_plural = "UsersDetail"
