from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User, Group as GroupSys
from filebrowser.fields import FileBrowseField

from ximpia.core.models import BaseModel, MetaKey
import ximpia.core.constants as CoreK
from ximpia.core.choices import Choices as CoreChoices

import constants as K
from choices import Choices

class Param ( BaseModel ):
	
	"""
	
	Site Parameters
	
	**Attributes**
	
	* ``id`` : Primary key
	* ``mode``:CharField(20) : Parameter mode. When parameters have same mode, table with key->value can be obtained.
	* ``name``:CharField(20) : Parameter name
	* ``value``:CharField(100) : Parameter value
	* ``paramType``:Charfield(10) : Parameter type: string, integer, date
	
	"""
	
	id = models.AutoField(primary_key=True, db_column='ID_SITE_PARAMETER')
	mode = models.CharField(max_length=20, db_column='MODE', null=True, blank=True, 
			verbose_name=_('Mode'), help_text=_('Parameter Mode'))
	name = models.CharField(max_length=20, db_column='NAME',
			verbose_name=_('Name'), help_text=_('Parameter Name'))
	value = models.CharField(max_length=100, null=True, blank=True, db_column='VALUE', 
			verbose_name=_('Value'), help_text=_('Parameter Value'))
	paramType = models.CharField(max_length=10, choices=CoreChoices.PARAM_TYPE, default=CoreChoices.PARAM_TYPE_STRING, 
			db_column='PARAM_TYPE',
			verbose_name=_('Parameter Type'), help_text=_('Type: either parameter or table'))
	def __unicode__(self):
		return self.name
	class Meta:
		db_table = 'SITE_PARAMETER'
		verbose_name = "Parameter"
		verbose_name_plural = "Parameters"

class MetaKey( BaseModel ):
	"""
	
	Model to store the keys allowed for meta values. Used for META tables and settings tables.
	
	**Attributes**
	
	* ``id``:AutoField : Primary key
	* ``name``:CharField(20) : Key META name
	
	**Relationships**
	
	* ``keyType`` : META Key type from SITE_PARAMETER table
	
	"""
	
	id = models.AutoField(primary_key=True, db_column='ID_SITE_META_KEY')
	name = models.CharField(max_length=100,
	        verbose_name = _('Key Name'), help_text = _('Meta Key Name'), db_column='NAME')
	keyType = models.ForeignKey(Param, limit_choices_to={'mode': CoreK.PARAM_META_TYPE}, db_column='ID_SITE_PARAMETER',
			verbose_name=_('Key META Type'), help_text=_('Key META Type') )
	def __unicode__(self):
		return self.name
	class Meta:
		db_table = 'SITE_META_KEY'
		ordering = ['name']
		verbose_name = _('Meta Key')
		verbose_name_plural = _('Meta Keys')

class TagMode ( BaseModel ):
	"""
	
	Tag Mode Model. Tags can have types (modes) in order to provide tag types
	
	**Attributes**
	
	* ``id`` : Primary key
	* ``mode``:CharField(30) : Tag mode (type)
	* ``isPublic``:BooleanField : is tag public or private?
	
	"""
	id = models.AutoField(primary_key=True, db_column='ID_SITE_TAG_MODE')
	mode = models.CharField(max_length=30, db_column='MODE',
			verbose_name = _('Mode'), help_text = _('Tag mode'))
	isPublic = models.BooleanField(default=True, db_column='IS_PUBLIC',
			verbose_name = _('Public'), help_text = _('Is tag mode public?'))
	def __unicode__(self):
		return self.mode
	class Meta:
		db_table = 'SITE_TAG_MODE'
		verbose_name = _('Tag Mode')
		verbose_name_plural = _("Tag Modes")

class Tag ( BaseModel ):
	"""
	
	Tag Model. Tags have name, tag type (mode), popularity and weather or not they are public. Popularity is integer. Can
	be rating stars type of popularity, ranking alorithms, etc...
	
	**Attributes**
	
	* ``id`` : Primary key
	* ``name``:CharField(30) : Tag name
	* ``popularity``IntegerField : Tag popularity
	* ``isPublic``:BooleanField : is tag public or private?
	
	**Relationships**
	
	* ``mode`` -> TagMode
	
	**Properties**
	
	* ``url`` : Built by services / business to provide an url for tags. tag.url = myUrl
	
	"""

	id = models.AutoField(primary_key=True, db_column='ID_SITE_TAG')
	name = models.CharField(max_length=30, db_column='NAME',
			verbose_name = _('Name'), help_text = _('Tag name'))
	mode = models.ForeignKey(TagMode, related_name='tag_mode', db_column='ID_MODE',
			verbose_name = _('Mode'), help_text = _('Tag mode'))
	popularity = models.IntegerField(default=1, null=True, blank=True, db_column='POPULARITY',
			verbose_name = _('Popularity'), help_text = _('Popularity'))
	isPublic = models.BooleanField(default=True, db_column='IS_PUBLIC',
			verbose_name = _('Public'), help_text = _('Is tag public?'))
	url = ''
	def __unicode__(self):
		return self.name
	def getText(self):
		return self.name
	def related_label(self):
		return u"%s" % (self.name)
	def get_url(self):
		return self.__url
	def set_url(self, value):
		self.__url = value
	def del_url(self):
		del self.__url
	class Meta:
		db_table = 'SITE_TAG'
		verbose_name = _('Tag')
		verbose_name_plural = _("Tags")
		ordering = ['-popularity']
	url = property(get_url, set_url, del_url, "Url for tag")

class Address ( BaseModel ):
	"""
	
	Address model. It can store only cities and countries or sholw addresses with geo spatial information.
	
	**Attributes**
	
	* ``id`` : Primary key
	* ``street`` :CharField(50) : Street address.
	* ``city``:CharField(20) : City.
	* ``region``:CharField(20) : Region.
	* ``zipCode``:CharField(20) : Zip code.
	* ``country``:CharField(2) : Country from Choices.COUNTRY
	* ``long``:DecimalField(18,12) : Longitude for address (Geo Data)
	* ``lat``:DecimalField(18,12) : Latitude for address (Geo Data)
	
	"""
	id = models.AutoField(primary_key=True, db_column='ID_SITE_ADDRESS')
	street = models.CharField(max_length=50, null=True, blank=True, db_column='STREET',
			verbose_name = _('Street'), help_text = _('Street'))
	city = models.CharField(max_length=20, db_column='CITY',
			verbose_name = _('City'), help_text = _('City'))
	region = models.CharField(max_length=20, null=True, blank=True, db_column='REGION',
			verbose_name = _('Region'), help_text = _('Region'))
	zipCode = models.CharField(max_length=20, null=True, blank=True, db_column='ZIP_CODE',
			verbose_name = _('Zip Code'), help_text = _('Zip Code'))
	country = models.CharField(max_length=2, choices=Choices.COUNTRY, db_column='COUNTRY',
			verbose_name = _('Country'), help_text = _('Country'))
	long = models.DecimalField(max_digits=18, decimal_places=12, null=True, blank=True,
			verbose_name=_('Geo Longitude'), help_text=_('Geo longitude'))
	lat = models.DecimalField(max_digits=18, decimal_places=12, null=True, blank=True,
			verbose_name=_('Geo Latitude'), help_text=_('Geo latitude'))
	def __unicode__(self):
		return '%s %s' % (self.street, self.city)
	class Meta:
		db_table = 'SITE_ADDRESS'
		verbose_name = _('Address')
		verbose_name_plural = _('Addresses')

class UserChannel ( BaseModel ):
	"""
	
	Every user can have one or more social channels. In case social channels are disabled, only one registry will
	exist for each user.
	
	User channels allow different social activities for users, for example data for private channel, friends channel,
	professional channel, company A channel, company B channel, etc...
	
	In case you need to provide your app model channel functionality, create a foreign key to UserChannel instead of
	django User model.
	
	**Attributes**
	
	* ``id`` : Primary key
	* ``title``CharField(20) : Title for the user channel
	* ``name``:CharField(20) : Name. Default USER name. When creating users, USER channel is created. Later on, more channels can
	be added
	
	**Relationships**
	
	* ``user`` -> Foreign key to User
	* ``groups`` <-> Many to many relationship with Group
	* ``tag`` -> Foreign key relationship with Tag 
	
	"""
	
	id = models.AutoField(primary_key=True, db_column='ID_SITE_USER')
	user = models.ForeignKey(User, db_column='ID_USER',
				verbose_name = _('User'), help_text = _('User'))
	groups = models.ManyToManyField('site.Group', related_name='user_groups', through='UserChannelGroup',  
				verbose_name = _('Groups'), help_text = _('Groups'))
	title = models.CharField(max_length=20, db_column='TITLE',
				verbose_name = _('Title'), help_text=_('Title for the user channel'))
	name = models.CharField(max_length=20, default=K.USER, db_column='NAME',
				verbose_name = _('Name'), help_text = _('Name for the user channel'))
	tag = models.ForeignKey(Tag, db_column='ID_TAG', null=True, blank=True,
				verbose_name=_('Tag'), help_text=_('User channel tag'))
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

class Category ( BaseModel ):
	
	"""
	
	Category model
	
	**Attributes**
	
	* ``id`` : Primary key
	* ``name``:CharField(55) : Category name.
	* ``slug``:CharField(200) : Category slug to build urls.
	* ``description``:CharField(255) : Category description.
	* ``image``:FileBrowserField(200) : Image path with django-filebrowser. Native version. Additional versions can be created
	with filebrowser version creating features.
	* ``type``:CharField(20) : Category type.
	* ``isPublished``:BooleanField : Category has been published and no longer in draft mode.
	* ``isPublic``:BooleanField : Category is private or public.
	*  ``popularity``:IntegerField : Category popularity
	* ``menuOrder``:PositiveSmallIntegerField : Menu order. Used by menu systems to display categories in ordered lists.
	
	**Relationships**
	
	* ``parent`` -> self : Foreign key to self for hierarchy
	
	**Properties**

	* ``url``:String : Url built from layers using slugs and parent slugs to provide hierarchable urls.
	* ``imgThumbnail``:String : Image version for showing in lists.
	* ``count``:int : Number of elements in category. Using aggregation features of django, this value is created by layers and shown
	in this model entity.
	
	"""

	id = models.AutoField(primary_key=True, db_column='ID_SITE_CATEGORY')
	name = models.CharField(max_length=55,
		verbose_name = _('name'), help_text = _('Category name'), db_column='NAME')
	slug = models.SlugField(max_length=200,
		verbose_name = _('Slug'), help_text = _('Slug'), db_column='SLUG')
	description = models.CharField(max_length=255, null=True, blank=True,
		verbose_name = _('Description'), help_text = _('Description'), db_column='DESCRIPTION')
	parent = models.ForeignKey('self', null=True, blank=True, related_name='category_parent', 
		    verbose_name = _('Parent'), help_text = _('Parent'), db_column='ID_PARENT')
	image = FileBrowseField(max_length=200, format='image', null=True, blank=True, 
		    verbose_name = _('Image'), help_text = _('Category image. Will be shown in listing categories or links to category'), 
		    db_column='IMAGE')
	type = 	models.ForeignKey(Param, limit_choices_to={'mode': K.PARAM_CATEGORY_TYPE}, db_column='ID_SITE_PARAMETER',
			verbose_name=_('Category Type'), help_text=_('Category Type') )
	isPublished = models.BooleanField(default=False,
		verbose_name = _('Is Published?'), help_text = _('Is Published?'), db_column='IS_PUBLISHED')
	isPublic = models.BooleanField(default=True, db_column='IS_PUBLIC',
			verbose_name = _('Public'), help_text = _('Is category public?'))
	popularity = models.IntegerField(default=1, null=True, blank=True, db_column='POPULARITY',
			verbose_name = _('Popularity'), help_text = _('Popularity'))
	menuOrder = models.PositiveSmallIntegerField(default=1,
		    verbose_name = _('Menu Order'), help_text = _('Menu Order'), db_column='MENU_ORDER')

	url = ''
	imgThumbnail = ''
	count = 0
	
	def __unicode__(self):
		return self.name
	def related_label(self):
		return u"%s" % (self.name)	
	def get_url(self):
		return self.__url
	def get_img_thumbnail(self):
		return self.__imgThumbnail
	def set_url(self, value):
		self.__url = value
	def set_img_thumbnail(self, value):
		self.__imgThumbnail = value
	def del_url(self):
		del self.__url
	def del_img_thumbnail(self):
		del self.__imgThumbnail
	def get_count(self):
		return self.__count
	def set_count(self, value):
		self.__count = value
	def del_count(self):
		del self.__count
	
	class Meta:
		db_table = 'SITE_CATEGORY'
		verbose_name = _('Category')
		verbose_name_plural = _('Categories')

	url = property(get_url, set_url, del_url, "url for category")
	imgThumbnail = property(get_img_thumbnail, set_img_thumbnail, del_img_thumbnail, "thumb image for category")
	count = property(get_count, set_count, del_count, "number of items in category")

class SocialNetworkUser ( BaseModel ):
	
	"""
	
	Social Networks for users
	
	**Attributes**
	
	* ``id`` : Primary key
	* ``socialNetwork``:CharField(20) : Social network.
	* ``socialId``:IntegerField : Social user id for network.
	* ``token``:CharField(255) : Token for user in network.
	* ``tokenSecret``:CharField(255) : Token secret for user in network.
	
	**Relationships**
	
	* ``user`` -> User : Foreign key to User mode.
	* ``socialNetwork`` -> CoreParam. Limit choices to 'mode=net'
	
	"""
	
	id = models.AutoField(primary_key=True, db_column='ID_SITE_SOCIAL_NETWORK_USER')
	user = models.ForeignKey(User, db_column='ID_USER',
				verbose_name = _('User'), help_text = _('User'))
	socialNetwork = models.ForeignKey('core.CoreParam', limit_choices_to={'mode': CoreK.NET}, db_column='ID_CORE_PARAMETER',
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
		db_table = 'SITE_SOCIAL_NETWORK_USER'
		unique_together = ("user", "socialNetwork")
		verbose_name = 'User Network'
		verbose_name_plural = "User Networks"

class Settings ( BaseModel ):
	"""
	Settings model
	
	**Attributes**
	
	* ``id``:AutoField : Primary key
	* ``value``:TextField : Settings value.
	* ``description``:CharField(255) : Setting description.
	* ``mustAutoload``:BooleanField : Has to load settings on cache?
	
	**Relationships**
	
	* ``name`` -> MetaKey : Foreign key to MetaKey model.
	
	"""
	
	id = models.AutoField(primary_key=True, db_column='ID_SITE_SETTINGS')
	name = models.ForeignKey(MetaKey, db_column='ID_META', limit_choices_to={'keyType__value': CoreK.PARAM_SETTINGS},
				verbose_name=_('Name'), help_text=_('Settings name'))
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

class UserMeta ( BaseModel ):
	"""
	
	User meta values for user in site. This has meta keys for ximpia site. You can add your user meta keys here for any values you need
	for your users like file quotas, session generated data you need to save into database, etc...
	
	**Attributes**
	
	* ``id`` : Primary key
	* ``value``:TextField : User meta value.
	
	**Relationships**
	
	* ``user`` -> User . Foreign key relationship with User model.
	* ``meta`` -> MetaKey . Foreign key relationship with MetaKey.
	
	"""
	
	id = models.AutoField(primary_key=True, db_column='ID_SITE_USER_PROFILE')
	user = models.ForeignKey(User, db_column='ID_USER',
				verbose_name = _('User'), help_text = _('User'))
	meta = models.ForeignKey(MetaKey, limit_choices_to={'keyType__value': CoreK.PARAM_META}, db_column='ID_META',
				verbose_name=_('Meta Key'), help_text=_('Meta Key'))
	value = models.TextField(db_column='VALUE', verbose_name = _('Value'), help_text = _('Value'))
	
	class Meta:
		db_table = 'SITE_USER_META'
		verbose_name = 'User Meta'
		verbose_name_plural = "Users Meta"

class UserProfile ( BaseModel ):
	"""
	
	Basic user profile for site users
	
	**Attributes**
	
	* ``id`` : Primary key
	* ``image``:FileBrowserField(200) : User image profile.
	
	**Relationships**
	
	* ``user`` -> User. Foreign key with User model.
	* ``status`` -> Param . Foreign key with SITE_PARAMETER for valud user statuses: mode='USER_STATUS'.
	
	"""
	
	id = models.AutoField(primary_key=True, db_column='ID_SITE_USER_PROFILE')
	user = models.ForeignKey(User, db_column='ID_USER',
				verbose_name = _('User'), help_text = _('User'))
	image = FileBrowseField(max_length=200, format='image', null=True, blank=True, 
		    verbose_name = _('Image'), help_text = _('User profile image'), 
		    db_column='IMAGE')
	status = models.ForeignKey(Param, limit_choices_to={'mode': K.PARAM_USER_STATUS}, db_column='ID_SITE_PARAMETER',
			verbose_name=_('Status'), help_text=_('User Status') )
	addresses = models.ManyToManyField(Address, through='site.UserAddress', related_name='userprofile_addresses',  
				verbose_name = _('Addresses'), help_text = _('User addresses'))
	
	def __unicode__(self):
		return self.user
	class Meta:
		db_table = 'SITE_USER_PROFILE'
		verbose_name = 'User Profile'
		verbose_name_plural = "User Profiles"

class UserAddress ( BaseModel ):
	id = models.AutoField(primary_key=True, db_column='ID_SITE_USER_ADDRESS')
	userProfile = models.ForeignKey(UserProfile, db_column='ID_SITE_USER_PROFILE',
				verbose_name = _('User Profile'), help_text = _('User Profile'))
	address = models.ForeignKey(Address, db_column='ID_ADDRESS',
				verbose_name = _('Address'), help_text = _('User Address') )
	type = models.ForeignKey(Param, limit_choices_to={'mode': K.PARAM_ADRESS_TYPE}, db_column='ID_SITE_PARAMETER',
			verbose_name=_('Type'), help_text=_('Address Type') )
	def __unicode__(self):
		return self.user
	class Meta:
		db_table = 'SITE_USER_ADDRESS'
		verbose_name = 'User Address'
		verbose_name_plural = "User Addresses"

class Group ( BaseModel ):
	"""
	
	Groups with access information, tagging and categorization. This model has been designed to allow discussion groups, definition of 
	departments inside organizations, work groups inside departments, user profiles, etc... It is a pretty flexible design to accommodate 
	your needs. Groups can be tagged and categorized to provide group types: profiles, departments, work groups...
	
	**Attributes**
	
	* ``id`` : Primary key
	* ``groupNameId``:CharField(20)
	* ``isPublic``:BooleanField
	
	**Relationships**
	
	* ``group`` -> GroupSys
	* ``parent`` -> Group
	* ``accessGroups`` <-> GroupAccess
	* ``tags`` <-> GroupTags
	* ``category`` -> Category	
	
	"""
	
	id = models.AutoField(primary_key=True, db_column='ID_SITE_GROUP')
	group = models.ForeignKey(GroupSys, unique=True, db_column='ID_GROUP_SYS',
				verbose_name = _('Group'), help_text = _('Group'))
	parent = models.ForeignKey('self', null=True, blank=True, related_name='groupchannel_parent', 
		    verbose_name = _('Parent'), help_text = _('Parent'), db_column='ID_PARENT')
	groupNameId = models.CharField(max_length=20, null=True, blank=True, db_column='GROUP_NAME_ID',
				verbose_name = _('Group Name Id'), help_text = _('Identification for group'))
	isPublic = models.BooleanField(default=True, db_column='IS_PUBLIC',
				verbose_name = _('Public'), help_text = _('Group is public'))
	accessGroups = models.ManyToManyField('self', through='site.GroupAccess', related_name='group_access', symmetrical=False, 
				verbose_name = _('Access Groups'), help_text = _('Profiles that have access to this group'))
	tags = models.ManyToManyField(Tag, through='site.GroupTag', null=True, blank=True, related_name='groupchannel_tags',
				verbose_name = _('Tags'), help_text = _('Tags'))
	category = models.ForeignKey(Category, limit_choices_to={}, db_column='ID_CATEGORY',
				verbose_name=_('Category'), help_text=_('Category for group'))
	
	def __unicode__(self):
		return self.group.name
	class Meta:
		db_table = 'SITE_GROUP'
		verbose_name = 'Group'
		verbose_name_plural = "Groups"

class GroupAccess ( BaseModel ):
	"""
	
	Access to group channels : User profiles.
	
	**Attributes**
	
	* ``id`` : Primary key
	
	**Relationships**
	
	* ``groupFrom`` -> Group
	* ``groupTo`` -> Group
	
	"""
	
	id = models.AutoField(primary_key=True, db_column='ID_SITE_GROUP_ACCESS')
	groupFrom = models.ForeignKey(Group, db_column='ID_GROUP_FROM', related_name='groupaccess_from',
					verbose_name=_('Group'), help_text=_('Group to grant access to'))
	groupTo = models.ForeignKey(Group, db_column='ID_GROUP_TO', related_name='groupaccess_to',
					verbose_name=_('Access Group'), help_text=_('Access Group for Group'))
	
	def __unicode__(self):
		return '%s %s' % (self.groupFrom, self.groupTo)
	
	class Meta:
		db_table = 'SITE_GROUP_ACCESS'
		verbose_name = 'Access Group'
		verbose_name_plural = "Access Groups"

class UserChannelGroup ( BaseModel ):
	"""
	
	User related to channel and their role (relationship). Relationships can be user, owner, admin and manager.
	
	**Attributes**
	
	* ``id`` : Primary key
	* ``relationship``:CharField(20) : Choices.ACCESS_RELATIONSHIP : user, admin, manager, owner
	
	**Relationships**
	
	* ``group`` -> Group
	* ``userChannel`` -> UserChannel
	
	"""
	
	id = models.AutoField(primary_key=True, db_column='ID_SITE_USER_GROUP')
	group = models.ForeignKey(Group, db_column='ID_GROUP',
					verbose_name=_('Group'), help_text=_('Group'))
	userChannel = models.ForeignKey(UserChannel, db_column='ID_USER_CHANNEL',
					verbose_name=_('User'), help_text=_('User channel'))
	
	def __unicode__(self):
		return '%s %s' % (self.group, self.userChannel)
	
	class Meta:
		db_table = 'SITE_USER_GROUP'
		verbose_name = 'User Group'
		verbose_name_plural = "User Groups"

class GroupTag ( BaseModel ):
	"""
	
	Tags for group channels
	
	**Attributes**
	
	* ``id`` : Primary key
	
	**Relationships**
	
	* ``group`` -> Group
	* ``tag`` -> Tag
	
	"""
	
	id = models.AutoField(primary_key=True, db_column='ID_SITE_GROUP_TAG')
	group = models.ForeignKey(Group, db_column='ID_GROUP',
					verbose_name=_('Group'), help_text=_('Group'))
	tag = models.ForeignKey(Tag, db_column='ID_TAG',
					verbose_name=_('Tag'), help_text=_('Tag'))
	
	def __unicode__(self):
		return '%s - %s' % (self.group, self.tag)
	
	class Meta:
		db_table = 'SITE_GROUP_TAG'
		verbose_name = 'Group Tag'
		verbose_name_plural = "Group Tags"

class SignupData ( BaseModel ):
	
	"""	
	SignUp Data. When users signup and further validation is required, signup data is recorded into this table. When they are validated 
	(email, etc...) an user and userchannel is created.
	
	**Attributes**
	
	* ``id`` : Primary key
	* ``user``:CharField(30) : User id.
	* ``activationCode``:POsitiveSmallIntegerField : Activation code used in validation message (email).
	* ``data``:TextField : User data.
	
	"""
	
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


class Invitation ( BaseModel ):
	"""
	
	Invitation Model
	
	**Attributes**
	
	* ``id`` : Primary key
	* ``invitationCode``:CharField(10) : Invitation code.
	* ``email``:EmailField : Invitation sent to this email address.
	* ``status``:CharField(10) : Invitation status from Choices.INVITATION_STATUS.
	* ``number``:PositiveSmallIntegerField : Number of invitations (either sent or used, depending on logic)
	* ``message``:TextField : Invitation message.
	
	**Relationships**
	
	* ``fromUser`` -> User : Foreign key for origin user which send invitation. 
	
	"""
	id = models.AutoField(primary_key=True, db_column='ID_SITE_INVITATION')
	fromUser = models.ForeignKey(User, db_column='ID_USER',
				verbose_name = _('From User'), help_text = _('Invitation from user'))
	invitationCode = models.CharField(max_length=10, unique=True, db_column='INVITATION_CODE',
				verbose_name = _('Inivitation Code'), help_text = _('Invitation Code'))
	email = models.EmailField(unique=True, db_column='EMAIL', verbose_name = _('Email'), help_text = _('Email attached to invitation'))
	status = models.CharField(max_length=10, choices=Choices.INVITATION_STATUS, default=K.PENDING, db_column='STATUS',
				verbose_name = _('Status'), help_text = _('Invitation status : pending, used.'))
	number = models.PositiveSmallIntegerField(default=1, db_column='NUMBER',
				verbose_name = _('Number'), help_text = _('Invitation Number'))
	message = models.TextField(null=True, blank=True, db_column='MESSAGE',
				verbose_name = _('Message'), help_text = _('Message'))
	meta = models.ManyToManyField(MetaKey, through='site.InvitationMeta', related_name='invitation_meta',
			verbose_name=_('META Keys'), help_text=_('META Keys for invitation') )
	def __unicode__(self):
		return '%s %s' % (self.fromUser, self.invitationCode)
	class Meta:
		db_table = 'SITE_INVITATION'
		verbose_name = _('Invitation')
		verbose_name_plural = _('Invitations')

class InvitationMeta ( BaseModel ):
	"""
	
	Invitation attached data.
	
	**Attributes**
	
	* ``id`` : Primary key
	* ``value``:TextField : User meta value.
	
	**Relationships**
	
	* ``invitation`` -> Invitation . Foreign key relationship with Invitation model.
	* ``meta`` -> MetaKey . Foreign key relationship with MetaKey.
	
	"""
	
	id = models.AutoField(primary_key=True, db_column='ID_SITE_USER_PROFILE')
	invitation = models.ForeignKey(Invitation, db_column='ID_INVITATION',
				verbose_name = _('Invitation'), help_text = _('Invitation'))
	meta = models.ForeignKey(MetaKey, limit_choices_to={'keyType__value': CoreK.PARAM_META}, db_column='ID_META',
				verbose_name=_('Meta Key'), help_text=_('Meta Key'))
	value = models.TextField(db_column='VALUE', verbose_name = _('Value'), help_text = _('Value'))
	
	class Meta:
		db_table = 'SITE_INVITATION_META'
		verbose_name = 'Invitation Meta Keys'
		verbose_name_plural = "Invitation Meta Keys"
