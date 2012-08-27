from ximpia_core.core.data import CommonDAO

from django.contrib.auth.models import User, Group

from models import Video, GroupChannel, Address, AddressOrganization, Organization, OrganizationGroup, Tag, TagMode, UserChannel, Invitation
from models import XmlMessage, Param, Category, UserDetail

class VideoDAO( CommonDAO ):
	def __init__(self, ctx, *argsTuple, **argsDict):
		super(VideoDAO, self).__init__(ctx, *argsTuple, **argsDict)
		self._model = Video

########################################################################

class UserDAO(CommonDAO):
	def __init__(self, ctx, *argsTuple, **argsDict):
		super(UserDAO, self).__init__(ctx, *argsTuple, **argsDict)
		self._model = User
	
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

class AddressOrganizationDAO( CommonDAO ):
	def __init__(self, ctx, *argsTuple, **argsDict):
		super(AddressOrganizationDAO, self).__init__(ctx, *argsTuple, **argsDict)
		self._model = AddressOrganization

class OrganizationDAO( CommonDAO ):	
	def __init__(self, ctx, *argsTuple, **argsDict):
		super(OrganizationDAO, self).__init__(ctx, *argsTuple, **argsDict)
		self._model = Organization

class OrganizationGroupDAO( CommonDAO ):
	def __init__(self, ctx, *argsTuple, **argsDict):
		super(OrganizationGroupDAO, self).__init__(ctx, *argsTuple, **argsDict)
		self._model = OrganizationGroup

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

class XmlMessageDAO(CommonDAO):
	def __init__(self, ctx, *argsTuple, **argsDict):
		super(XmlMessageDAO, self).__init__(ctx, *argsTuple, **argsDict)
		self._model = XmlMessage

class ParamDAO(CommonDAO):
	def __init__(self, ctx, *argsTuple, **argsDict):
		super(ParamDAO, self).__init__(ctx, *argsTuple, **argsDict)
		self._model = Param

class CategoryDAO(CommonDAO):
	def __init__(self, ctx, *argsTuple, **argsDict):
		super(CategoryDAO, self).__init__(ctx, *argsTuple, **argsDict)
		self._model = Category

class UserDetailDAO(CommonDAO):
	def __init__(self, ctx, *argsTuple, **argsDict):
		super(UserDetailDAO, self).__init__(ctx, *argsTuple, **argsDict)
		self._model = UserDetail
