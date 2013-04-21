# coding: utf-8

from ximpia.core.data import CommonDAO, XpMsgException

from django.contrib.auth.models import User, Group as GroupSys
from django.db.models import Q

from models import Address, Category, Group, GroupAccess, GroupTag, Invitation, InvitationMeta, MetaKey, Param, Setting, SignupData
from models import SocialNetworkUser, Tag, TagMode, UserAddress, UserChannel, UserChannelGroup, UserMeta, UserProfile

import constants as K

class UserDAO(CommonDAO):
	def __init__(self, ctx, *args_tuple, **args_dict):
		super(UserDAO, self).__init__(ctx, *args_tuple, **args_dict)
		self._model = User
	
	def get_invitation(self, invitation_code, status=None):
		"""
		Get invitation for invitationCode 
		@param invitationCode: 
		@return: Invitation
		"""
		"""try:
			if status:
				invitation = Invitation.objects.get(invitationCode=invitationCode, status=status)
			else:
				invitation = Invitation.objects.get(invitationCode=invitationCode)
		except Exception as e:
			raise e
			#raise XpMsgException(e, _('Error in checking invitation code'))
		return invitation"""
		pass

class GroupSysDAO(CommonDAO):
	def __init__(self, ctx, *args_tuple, **args_dict):
		super(GroupSysDAO, self).__init__(ctx, *args_tuple, **args_dict)
		self._model = GroupSys

class GroupDAO( CommonDAO ):
	def __init__(self, ctx, *args_tuple, **args_dict):
		super(GroupDAO, self).__init__(ctx, *args_tuple, **args_dict)
		self._model = Group

class GroupAccessDAO( CommonDAO ):
	def __init__(self, ctx, *args_tuple, **args_dict):
		super(GroupAccessDAO, self).__init__(ctx, *args_tuple, **args_dict)
		self._model = GroupAccess

class GroupTagDAO( CommonDAO ):
	def __init__(self, ctx, *args_tuple, **args_dict):
		super(GroupTagDAO, self).__init__(ctx, *args_tuple, **args_dict)
		self._model = GroupTag

class InvitationMetaDAO( CommonDAO ):
	def __init__(self, ctx, *args_tuple, **args_dict):
		super(InvitationMetaDAO, self).__init__(ctx, *args_tuple, **args_dict)
		self._model = InvitationMeta

class UserMetaDAO( CommonDAO ):
	def __init__(self, ctx, *args_tuple, **args_dict):
		super(UserMetaDAO, self).__init__(ctx, *args_tuple, **args_dict)
		self._model = UserMeta
	def save_meta(self, user, metas, keys):
		"""
		Save user meta keys
		
		** Attributes **
		
		* ``user``:Model : User model instance
		* ``metas``:Dict : Meta keys
		* ``metaDict``:Dict : Dictionary with key->value
		"""
		for key in keys:
			meta = metas[key]
			try:
				metaReminderId = self.get(user=user, meta=meta)
				metaReminderId.value = keys[key]
				metaReminderId.save()
			except XpMsgException:
				self.create(user=user, meta=meta, value=keys[key])

class AddressDAO( CommonDAO ):
	def __init__(self, ctx, *args_tuple, **args_dict):
		super(AddressDAO, self).__init__(ctx, *args_tuple, **args_dict)
		self._model = Address

class CategoryDAO( CommonDAO ):
	def __init__(self, ctx, *args_tuple, **args_dict):
		super(CategoryDAO, self).__init__(ctx, *args_tuple, **args_dict)
		self._model = Category

class TagDAO( CommonDAO ):
	def __init__(self, ctx, *args_tuple, **args_dict):
		super(TagDAO, self).__init__(ctx, *args_tuple, **args_dict)
		self._model = Tag

class TagModeDAO(CommonDAO):
	def __init__(self, ctx, *args_tuple, **args_dict):
		super(TagModeDAO, self).__init__(ctx, *args_tuple, **args_dict)
		self._model = TagMode

class MetaKeyDAO( CommonDAO ):
	def __init__(self, ctx, *args_tuple, **args_dict):
		super(MetaKeyDAO, self).__init__(ctx, *args_tuple, **args_dict)
		self._model = MetaKey
	def metas(self, keys):
		"""
		Get meta keys as a dictionary
		
		** Attributes **
		
		* ``keys``:List : Key names
		
		** Returns **
		
		Dict :: keyName -> MetaKey"""
		metaList = self.search(name__in=keys)
		metaDict = {}
		for metaKey in metaList:
			metaDict[metaKey.name] = metaKey
		return metaDict

class UserChannelDAO(CommonDAO):
	def __init__(self, ctx, *args_tuple, **args_dict):
		super(UserChannelDAO, self).__init__(ctx, *args_tuple, **args_dict)
		self._model = UserChannel

class InvitationDAO(CommonDAO):
	def __init__(self, ctx, *args_tuple, **args_dict):
		super(InvitationDAO, self).__init__(ctx, *args_tuple, **args_dict)
		self._model = Invitation

class ParamDAO(CommonDAO):
	def __init__(self, ctx, *args_tuple, **args_dict):
		super(ParamDAO, self).__init__(ctx, *args_tuple, **args_dict)
		self._model = Param
	def get_user_status_active(self):
		return self.get(mode=K.PARAM_USER_STATUS, name=K.PARAM_USER_STATUS_ACTIVE)
	def get_address_type_personal(self):
		return self.get(mode=K.PARAM_ADDRESS_TYPE, name=K.PARAM_ADDRESS_TYPE_PERSONAL)

class SignupDataDAO(CommonDAO):
	def __init__(self, ctx, *args_tuple, **args_dict):
		super(SignupDataDAO, self).__init__(ctx, *args_tuple, **args_dict)
		self._model = SignupData

class SocialNetworkUserDAO(CommonDAO):
	def __init__(self, ctx, *args_tuple, **args_dict):
		super(SocialNetworkUserDAO, self).__init__(ctx, *args_tuple, **args_dict)
		self._model = SocialNetworkUser

class SettingDAO(CommonDAO):
	def __init__(self, ctx, *args_tuple, **args_dict):
		super(SettingDAO, self).__init__(ctx, *args_tuple, **args_dict)
		self._model = Setting
	def search_settings(self, app_name):
		"""
		Search settings with mustAutoLoad=True for global settings and settings linked to an application. Settings will be included
		in the response in the field ``settings``.
		
		** Attributes**
		
		* ``appName``:String : Application name
		
		**Returns**
		
		Queryset with settings
		"""
		settings = self._model.objects.filter( Q(application = None) | Q(application__name=app_name), mustAutoload=True)
		return settings 

class UserAddressDAO( CommonDAO ):
	def __init__(self, ctx, *args_tuple, **args_dict):
		super(UserAddressDAO, self).__init__(ctx, *args_tuple, **args_dict)
		self._model = UserAddress

class UserChannelGroupDAO( CommonDAO ):
	def __init__(self, ctx, *args_tuple, **args_dict):
		super(UserChannelGroupDAO, self).__init__(ctx, *args_tuple, **args_dict)
		self._model = UserChannelGroup

class UserProfileDAO( CommonDAO ):
	def __init__(self, ctx, *args_tuple, **args_dict):
		super(UserProfileDAO, self).__init__(ctx, *args_tuple, **args_dict)
		self._model = UserProfile
