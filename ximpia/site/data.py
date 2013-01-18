from ximpia.core.data import CommonDAO

from django.contrib.auth.models import User, Group as GroupSys
from django.db.models import Q

from models import Address, Category, Group, GroupAccess, GroupTag, Invitation, InvitationMeta, MetaKey, Param, Setting, SignupData
from models import SocialNetworkUser, Tag, TagMode, UserAddress, UserChannel, UserChannelGroup, UserMeta, UserProfile

import constants as K

class UserDAO(CommonDAO):
	def __init__(self, ctx, *argsTuple, **argsDict):
		super(UserDAO, self).__init__(ctx, *argsTuple, **argsDict)
		self._model = User
	
	def getInvitation(self, invitationCode, status=None):
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
	def __init__(self, ctx, *argsTuple, **argsDict):
		super(GroupSysDAO, self).__init__(ctx, *argsTuple, **argsDict)
		self._model = GroupSys

class GroupDAO( CommonDAO ):
	def __init__(self, ctx, *argsTuple, **argsDict):
		super(GroupDAO, self).__init__(ctx, *argsTuple, **argsDict)
		self._model = Group

class GroupAccessDAO( CommonDAO ):
	def __init__(self, ctx, *argsTuple, **argsDict):
		super(GroupAccessDAO, self).__init__(ctx, *argsTuple, **argsDict)
		self._model = GroupAccess

class GroupTagDAO( CommonDAO ):
	def __init__(self, ctx, *argsTuple, **argsDict):
		super(GroupTagDAO, self).__init__(ctx, *argsTuple, **argsDict)
		self._model = GroupTag

class InvitationMetaDAO( CommonDAO ):
	def __init__(self, ctx, *argsTuple, **argsDict):
		super(InvitationMetaDAO, self).__init__(ctx, *argsTuple, **argsDict)
		self._model = InvitationMeta

class AddressDAO( CommonDAO ):
	def __init__(self, ctx, *argsTuple, **argsDict):
		super(AddressDAO, self).__init__(ctx, *argsTuple, **argsDict)
		self._model = Address

class CategoryDAO( CommonDAO ):
	def __init__(self, ctx, *argsTuple, **argsDict):
		super(CategoryDAO, self).__init__(ctx, *argsTuple, **argsDict)
		self._model = Category

class TagDAO( CommonDAO ):
	def __init__(self, ctx, *argsTuple, **argsDict):
		super(TagDAO, self).__init__(ctx, *argsTuple, **argsDict)
		self._model = Tag

class TagModeDAO(CommonDAO):
	def __init__(self, ctx, *argsTuple, **argsDict):
		super(TagModeDAO, self).__init__(ctx, *argsTuple, **argsDict)
		self._model = TagMode

class MetaKeyDAO( CommonDAO ):
	def __init__(self, ctx, *argsTuple, **argsDict):
		super(MetaKeyDAO, self).__init__(ctx, *argsTuple, **argsDict)
		self._model = MetaKey

class UserChannelDAO(CommonDAO):
	def __init__(self, ctx, *argsTuple, **argsDict):
		super(UserChannelDAO, self).__init__(ctx, *argsTuple, **argsDict)
		self._model = UserChannel

class InvitationDAO(CommonDAO):
	def __init__(self, ctx, *argsTuple, **argsDict):
		super(InvitationDAO, self).__init__(ctx, *argsTuple, **argsDict)
		self._model = Invitation

class ParamDAO(CommonDAO):
	def __init__(self, ctx, *argsTuple, **argsDict):
		super(ParamDAO, self).__init__(ctx, *argsTuple, **argsDict)
		self._model = Param
	def getUserStatusActive(self):
		return self.get(mode=K.PARAM_USER_STATUS, name=K.PARAM_USER_STATUS_ACTIVE)
	def getAddressTypePersonal(self):
		return self.get(mode=K.PARAM_ADDRESS_TYPE, name=K.PARAM_ADDRESS_TYPE_PERSONAL)

class SignupDataDAO(CommonDAO):
	def __init__(self, ctx, *argsTuple, **argsDict):
		super(SignupDataDAO, self).__init__(ctx, *argsTuple, **argsDict)
		self._model = SignupData

class SocialNetworkUserDAO(CommonDAO):
	def __init__(self, ctx, *argsTuple, **argsDict):
		super(SocialNetworkUserDAO, self).__init__(ctx, *argsTuple, **argsDict)
		self._model = SocialNetworkUser

class SettingDAO(CommonDAO):
	def __init__(self, ctx, *argsTuple, **argsDict):
		super(SettingDAO, self).__init__(ctx, *argsTuple, **argsDict)
		self._model = Setting
	def searchSettings(self, appName):
		"""
		Search settings with mustAutoLoad=True for global settings and settings linked to an application. Settings will be included
		in the response in the field ``settings``.
		
		** Attributes**
		
		* ``appName``:String : Application name
		
		**Returns**
		
		Queryset with settings
		"""
		settings = self._model.objects.filter( Q(application = None) | Q(application__name=appName), mustAutoload=True)
		return settings

class UserAddressDAO( CommonDAO ):
	def __init__(self, ctx, *argsTuple, **argsDict):
		super(UserAddressDAO, self).__init__(ctx, *argsTuple, **argsDict)
		self._model = UserAddress

class UserChannelGroupDAO( CommonDAO ):
	def __init__(self, ctx, *argsTuple, **argsDict):
		super(UserChannelGroupDAO, self).__init__(ctx, *argsTuple, **argsDict)
		self._model = UserChannelGroup

class UserMetaDAO( CommonDAO ):
	def __init__(self, ctx, *argsTuple, **argsDict):
		super(UserMetaDAO, self).__init__(ctx, *argsTuple, **argsDict)
		self._model = UserMeta

class UserProfileDAO( CommonDAO ):
	def __init__(self, ctx, *argsTuple, **argsDict):
		super(UserProfileDAO, self).__init__(ctx, *argsTuple, **argsDict)
		self._model = UserProfile
