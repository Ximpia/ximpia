from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User, Group

from ximpia.core.models import BaseModel

import constants as K
from choices import Choices

class SocialNetworkUser(models.Model):
	id = models.AutoField(primary_key=True, db_column='ID_SITE_SOCIAL_USER')
	user = models.ForeignKey(User, db_column='ID_USER',
				verbose_name = _('User'), help_text = _('User'))
	socialNetwork = models.CharField(max_length=20, choices=Choices.SOCIAL_NETS, db_column='SOCIAL_NETWORK',
				verbose_name = _('Social Network'), help_text = _('Social network'))
	socialId = models.IntegerField(db_column='SOCIAL_ID', verbose_name = _('Social ID'), help_text = _('Social network user id'))
	token = models.CharField(max_length=255, db_column='TOKEN',
				verbose_name = _('Token'), help_text = _('Token'))
	tokenSecret = models.CharField(max_length=255, null=True, blank=True, db_column='TOKEN_SECRET',
				verbose_name = _('Token Secret'), help_text = _('Token secret'))
	def __unicode__(self):
		return str(self.getName()) + ' ' + str(self.user)
	def getName(self):
		return self.socialNetwork
	class Meta:
		db_table = 'SITE_SOCIAL_USER'
		unique_together = ("user", "socialNetwork")
		verbose_name = 'Social Networks for User'
		verbose_name_plural = "Social Networks for Users"

class Settings( BaseModel ):
	"""
	Settings model
	
	**Attributes**
	
	* ``name``:CharField(64) : Setting name
	* ``value``:TextField : Settings value
	* ``description``:CharField(255) : Setting description
	* ``mustAutoload``:BooleanField : Has to load settings on cache?
	
	"""
	name = models.CharField(max_length=64,
	        verbose_name = _('Name'), help_text = _('Settings name'), db_column='NAME')
	value = models.TextField(verbose_name = _('Value'), help_text = _('Settings value'), db_column='VALUE')
	description = models.CharField(max_length=255,
	        verbose_name = _('Description'), help_text = _('Description'), db_column='DESCRIPTION')
	mustAutoload = models.BooleanField(default=False,
	        verbose_name = _('Must Autoload?'), help_text = _('Must Autoload?'), db_column='MUST_AUTOLOAD')
	def __unicode__(self):
		return str(self.name)
	class Meta:
		db_table = 'SITE_SETTINGS'
		verbose_name = _('Settings')
		verbose_name_plural = _('Settings')

# TODO: UserDetail?? FileBrowser?? UserProfile???
class UserDetail(BaseModel):
	"""Model for UserSocial
	FK : User
	MN: SocialNetworks"""
	id = models.AutoField(primary_key=True, db_column='ID_SITE_USER_DETAIL')
	user = models.ForeignKey(User, db_column='ID_USER',
				verbose_name = _('User'), help_text = _('User'))
	name = models.CharField(max_length=60, db_column='NAME',
				verbose_name = _('Name'), help_text = _('Name'))
	settings = models.TextField(default = '', null=True, blank=True, db_column='SETTINGS',
				verbose_name = _('Settings'), help_text = _('Settings'))
	socialNetworks = models.ManyToManyField('SocialNetwork', through='SocialNetworkUser',  null=True, blank=True,
				verbose_name = _('Social Networks'), help_text = _('Social Networks'))
	hasUploadPic = models.BooleanField(default=False, db_column='HAS_UPLOAD_PIC',
				verbose_name = _('Uploaded Pic'), help_text = _('Has the user uploaded custom picture?'))
	isSuspended = models.BooleanField(default=False, db_column='IS_SUSPENDED',
				verbose_name = _('Suspended'), help_text = _('Weather user account has been suspended'))
	picExt = models.CharField(max_length=3, null=True, blank=True, db_column='PIC_EXT',
				verbose_name = _('Picture Extension'), help_text = _('Picture file extension'))
	reminderId = models.CharField(max_length=15, null=True, blank=True, db_column='REMINDER_ID',
				verbose_name = _('Reminder Id'), help_text = _('Reminder identification for password retreive'))
	lang = models.CharField(max_length=2, default='en', db_column='LANG',
				verbose_name = _('Language'), help_text = _('Language'))
	auth = models.TextField(default = '', null=True, blank=True, db_column='AUTH',
				verbose_name = _('Authentication'), help_text = _('Authentication'))	
	netProfiles = models.TextField(default = '', null=True, blank=True, db_column='NET_PROFILES',
				verbose_name = _('Network Profiles'), help_text = _('Network Profiles'))	
	msgPreference = models.CharField(max_length=10, choices=Choices.MSG_PREFERRED, default=K.XIMPIA, db_column='MSG_PREFERENCE',
				verbose_name = _('Messaging Preference'), help_text = _('Preference for sending messages: Facebook, Twitter, Email, etc...'))
	hasValidatedEmail = models.BooleanField(default=False, db_column='HAS_VALIDATED_EMAIL',
				verbose_name = _('Validated Email'), help_text = _('User has validated his email address?'))
	filesQuota = models.IntegerField(default=K.FILE_QUOTA_DEFAULT, db_column='FILES_QUOTA',
				verbose_name = _('File Quota'), help_text = _('Maximum size storage for files in MB'))
	resetPasswordDate = models.DateField(null=True, blank=True, db_column='RESET_PASSWORD_DATE', 
				verbose_name = _('Reset Password Date'), help_text = _('Maximum date for reset password link validation'))
	showIntro = models.BooleanField(default=True, db_column='SHOW_INTRO',
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

class UserChannel(BaseModel):
	"""Every user can have one or more social channels. In case social channels are disabled, only one registry will
	exist for each user."""
	id = models.AutoField(primary_key=True, db_column='ID_SITE_USER')
	user = models.ForeignKey(User, db_column='ID_USER',
				verbose_name = _('User'), help_text = _('User'))
	groups = models.ManyToManyField(Group, 
				verbose_name = _('Groups'), help_text = _('Groups'))
	title = models.CharField(max_length=20, db_column='TITLE',
				verbose_name = _('Channel Title'), help_text=_('Title for the social channel'))
	name = models.CharField(max_length=20, default=K.USER, db_column='NAME',
				verbose_name = _('Social Channel Name'), help_text = _('Name for the social channel'))
	"""isCompany = models.BooleanField(default=False, db_column='IS_COMPANY',
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

class SocialNetwork(BaseModel):
	id = models.AutoField(primary_key=True, db_column='ID_SITE_SOCIAL_NETWORK')
	myType = models.ForeignKey('core.CoreParam', limit_choices_to={'mode__lte': K}, db_column='ID_TYPE',
				verbose_name = _('Social Network Type'), help_text = _('Type of social network'))
	def __unicode__(self):
		return str(self.myType)
	def getName(self):
		return self.myType.name
	class Meta:
		db_table = 'SITE_SOCIAL_NETWORK'
		verbose_name = _('Social Network')
		verbose_name_plural = _("Social Networks")


class XmlMessage(BaseModel):
	"""XML Messages"""
	# TODO: This table will go to settings, having name as name
	# @deprecated: Move table data to SITE_SETTINGS
	id = models.AutoField(primary_key=True, db_column='ID_SITE_XML_MESSAGE')
	name = models.CharField(max_length=255, db_column='NAME',
			verbose_name = _('Name'), help_text = _('Code name of XML'))
	lang = models.CharField(max_length=2, choices=Choices.LANG, default=Choices.LANG_ENGLISH, db_column='LANG',
			verbose_name = _('Language'), help_text = _('Language for xml'))
	body = models.TextField(db_column='BODY', verbose_name = _('Xml Content'), help_text = _('Xml content'))
	def __unicode__(self):
		return str(self.name)
	class Meta:
		db_table = 'SITE_XML_MESSAGE'
		verbose_name = _('Xml Message')
		verbose_name_plural = _('Xml Messages')

class Param(BaseModel):
	"""Site Parameters"""
	id = models.AutoField(primary_key=True, db_column='ID_SITE_PARAMETER')
	mode = models.CharField(max_length=20, db_column='MODE', 
			verbose_name=_('Mode'), help_text=_('Parameter Mode'))
	name = models.CharField(max_length=20, db_column='NAME',
			verbose_name=_('Name'), help_text=_('Parameter Name'))
	value = models.CharField(max_length=100, null=True, blank=True, db_column='VALUE', 
			verbose_name=_('Value'), help_text=_('Parameter Value for Strings'))
	valueId = models.IntegerField(null=True, blank=True, db_column='VALUE_ID',
			verbose_name=_('Value Id'), help_text=_('Parameter Value for Integers'))
	valueDate = models.DateTimeField(null=True, blank=True, db_column='VALUE_DATE',
			verbose_name = _('Value Date'), help_text = _('Parameter Value for Date'))
	paramType = models.CharField(max_length=10, choices=Choices.PARAM_TYPE, db_column='PARAM_TYPE',
			verbose_name=_('Parameter Type'), help_text=_('Type: either parameter or table'))
	def __unicode__(self):
		return str(self.mode) + ' - ' + str(self.name)
	class Meta:
		db_table = 'SITE_PARAMETER'
		verbose_name = "Parameter"
		verbose_name_plural = "Parameters"


class SignupData(BaseModel):
	"""SignUp Data"""
	id = models.AutoField(primary_key=True, db_column='ID_SITE_SIGNUP_DATA')
	user = models.CharField(max_length=30, unique=True, db_column='USER',
			verbose_name = _('User'), help_text = _('User'))
	activationCode = models.PositiveSmallIntegerField(db_column='ACTIVATION_CODE', 
			verbose_name = _('Activation Code'), help_text = _('Activation code'))
	data = models.TextField(db_column='DATA', verbose_name = _('Data'), help_text = _('Data'))
	def __unicode__(self):
		return str(self.user)
	class Meta:
		db_table = 'SITE_SIGNUP_DATA'
		verbose_name = _('Signup Data')
		verbose_name_plural = _('Signup Data')
