from ximpia.core.data import CommonDAO

from django.contrib.auth.models import User, Group

from models import UserChannel
from models import Param, SignupData, SocialNetworkUser, Settings, Category, Tag, TagMode, Invitation, Address, GroupChannel

class UserDAO(CommonDAO):
	def __init__(self, ctx, *argsTuple, **argsDict):
		super(UserDAO, self).__init__(ctx, *argsTuple, **argsDict)
		self._model = User
	
	def getInvitation(self, invitationCode, status=None):
		"""Get invitation for invitationCode 
		@param invitationCode: 
		@return: Invitation"""
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

class GroupDAO(CommonDAO):
	def __init__(self, ctx, *argsTuple, **argsDict):
		super(GroupDAO, self).__init__(ctx, *argsTuple, **argsDict)
		self._model = Group

class GroupChannelDAO( CommonDAO ):
	def __init__(self, ctx, *argsTuple, **argsDict):
		super(GroupChannelDAO, self).__init__(ctx, *argsTuple, **argsDict)
		self._model = GroupChannel

class AddressDAO( CommonDAO ):
	def __init__(self, ctx, *argsTuple, **argsDict):
		super(AddressDAO, self).__init__(ctx, *argsTuple, **argsDict)
		self._model = Address

class TagDAO( CommonDAO ):
	def __init__(self, ctx, *argsTuple, **argsDict):
		super(TagDAO, self).__init__(ctx, *argsTuple, **argsDict)
		self._model = Tag

class TagModeDAO(CommonDAO):
	def __init__(self, ctx, *argsTuple, **argsDict):
		super(TagModeDAO, self).__init__(ctx, *argsTuple, **argsDict)
		self._model = TagMode

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

class CategoryDAO(CommonDAO):
	def __init__(self, ctx, *argsTuple, **argsDict):
		super(CategoryDAO, self).__init__(ctx, *argsTuple, **argsDict)
		self._model = Category

class SignupDataDAO(CommonDAO):
	def __init__(self, ctx, *argsTuple, **argsDict):
		super(SignupDataDAO, self).__init__(ctx, *argsTuple, **argsDict)
		self._model = SignupData

class SocialNetworkUserDAO(CommonDAO):
	def __init__(self, ctx, *argsTuple, **argsDict):
		super(SocialNetworkUserDAO, self).__init__(ctx, *argsTuple, **argsDict)
		self._model = SocialNetworkUser

class SettingsDAO(CommonDAO):
	def __init__(self, ctx, *argsTuple, **argsDict):
		super(SettingsDAO, self).__init__(ctx, *argsTuple, **argsDict)
		self._model = Settings
