# coding: utf-8

from ximpia.xpcore.data import CommonDAO, XpMsgException

from django.contrib.auth.models import User, Group as GroupSys
from django.db.models import Q

from models import Address, Category, Group, GroupAccess, GroupTag, Invitation, InvitationMeta, MetaKey, Param, Setting, SignupData
from models import SocialNetworkUser, Tag, TagMode, UserAddress, UserChannel, UserChannelGroup, UserMeta, UserProfile

import constants as K

class UserDAO(CommonDAO):
    model = User
    
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
    model = GroupSys    

class GroupDAO( CommonDAO ):
    model = Group

class GroupAccessDAO( CommonDAO ):
    model = GroupAccess

class GroupTagDAO( CommonDAO ):
    model = GroupTag

class InvitationMetaDAO( CommonDAO ):
    model = InvitationMeta

class UserMetaDAO( CommonDAO ):
    model = UserMeta

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
    model = Address

class CategoryDAO( CommonDAO ):
    model = Category

class TagDAO( CommonDAO ):
    model = Tag

class TagModeDAO(CommonDAO):
    model = TagMode

class MetaKeyDAO(CommonDAO):
    model = MetaKey

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
    model = UserChannel

class InvitationDAO(CommonDAO):
    model = Invitation

class ParamDAO(CommonDAO):
    model = Param

    def get_user_status_active(self):
        return self.get(mode=K.PARAM_USER_STATUS, name=K.PARAM_USER_STATUS_ACTIVE)
    def get_address_type_personal(self):
        return self.get(mode=K.PARAM_ADDRESS_TYPE, name=K.PARAM_ADDRESS_TYPE_PERSONAL)

class SignupDataDAO(CommonDAO):
    model = SignupData

class SocialNetworkUserDAO(CommonDAO):
    model = SocialNetworkUser

class SettingDAO(CommonDAO):
    model = Setting

    def search_settings(self, app_name):
        """
        Search settings with mustAutoLoad=True for global settings and settings linked to an application. Settings will be included
        in the response in the field ``settings``.
        
        ** Attributes**
        
        * ``appName``:String : Application name
        
        **Returns**
        
        Queryset with settings
        """
        settings = self.model.objects.filter( Q(application = None) | Q(application__name=app_name), mustAutoload=True)
        return settings 

class UserAddressDAO( CommonDAO ):
    model = UserAddress

class UserChannelGroupDAO( CommonDAO ):
    model = UserChannelGroup

class UserProfileDAO( CommonDAO ):
    model = UserProfile
