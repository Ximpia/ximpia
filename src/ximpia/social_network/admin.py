from models import Comment, GroupFollow, GroupStream, GroupStreamPublic, Like
from models import SocialNetwork, StatusMessage, StatusShare, Tag, UserParam, UserSocial, GroupSocial

from models import SocialNetworkUserSocial, UserDetail
from models import Link, Version
from models import UserProfile, ProfileDetail, Organization, OrganizationGroup, UserAccount, IdentifierUserAccount, UserAccountIdentifier 
from models import Skill, SkillUserAccount, SkillGroup, Industry, AddressOrganization, SocialNetworkOrganization, TaxType, TaxOrganization
from models import TaxUserAccount, SocialNetworkOrganizationGroup, UserAccountRelation, UserAccountContract, Invitation, Affiliate
from models import TagUserTotal, LinkUserTotal, SubscriptionDaily, Subscription, SubscriptionItemMonth, Application, Contact, ContactDetail, MasterValue
from models import Notification, XmlMessage

from django.contrib import admin

"""Copyright (c) 2011 Jorge Alegre Vilches
All rights reserved."""

class CommentAdmin(admin.ModelAdmin):
	list_display = ('id','user','message','isPublic',)
	list_filter = ('isPublic',)
	search_fields = ('message',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

class GroupFollowAdmin(admin.ModelAdmin):
	list_display = ('id','groupSource','groupTarget','status')
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

class GroupStreamAdmin(admin.ModelAdmin):
	list_display = ('id','postId','user','account','group','message')
	search_fields = ('message',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

class GroupStreamPublicAdmin(admin.ModelAdmin):
	list_display = ('id','postId')
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

class LikeAdmin(admin.ModelAdmin):
	list_display = ('id','user')
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

class SocialNetworkAdmin(admin.ModelAdmin):
	list_display = ('id','type',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

class StatusMessageAdmin(admin.ModelAdmin):
	list_display = ('id','message')
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

class StatusShareAdmin(admin.ModelAdmin):
	list_display = ('id','user','message')
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

class TagAdmin(admin.ModelAdmin):
	list_display = ('id','name','type','popularity')
	list_filter = ('type',)
	search_fields = ('name',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

class UserParamAdmin(admin.ModelAdmin):
	list_display = ('id','mode','name','value','valueId')
	list_filter = ('mode',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

class UserSocialAdmin(admin.ModelAdmin):
	list_display = ('id','user','socialChannel',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

class GroupSocialAdmin(admin.ModelAdmin):
	list_display = ('id','group','groupNameId', 'isXimpiaGroup','isIndustry', 'isOrgGroup', 'isPublic',)
	list_filter = ('isXimpiaGroup','isIndustry','isPublic','isOrgGroup',)
	search_fields = ('group',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

########################################################################################

class SocialNetworkUserSocialAdmin(admin.ModelAdmin):
	list_display = ('user','socialNetwork','token')
	list_filter = ('socialNetwork',)
	search_fields = ('token',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

class UserDetailAdmin(admin.ModelAdmin):
	list_display = ('user','name','isSuspended','lang',)
	list_filter = ('lang',)
	search_fields = ('name',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

class MessageAddrAdmin(admin.ModelAdmin):
	list_display = ('address','type',)
	list_filter = ('type',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

class MessageSentAdmin(admin.ModelAdmin):
	list_display = ('id','userFrom',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

class MessageReplyAdmin(admin.ModelAdmin):
	list_display = ('id','userFrom',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

class MessageAdmin(admin.ModelAdmin):
	list_display = ('id','source','archived','secure','summary',)
	list_filter = ('archived','secure','source',)
	search_fields = ('summary',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

class MessageReceivedAdmin(admin.ModelAdmin):
	list_display = ('id','userFrom',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

class MessageLogAdmin(admin.ModelAdmin):
	list_display = ('id','userFrom','messageId','action',)
	list_filter = ('action',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

class DiscussionAdmin(admin.ModelAdmin):
	list_display = ()
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

class DiscussionThreadAdmin(admin.ModelAdmin):
	list_display = ()
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

class LinkAdmin(admin.ModelAdmin):
	list_display = ('id','domain','url','numberShared',)
	search_fields = ('urlTitle','urlDescription','summary',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

class AddressContactAdmin(admin.ModelAdmin):
	list_display = ('id','contact','addressType','city','country','zipCode',)
	list_filter = ('addressType','country',)
	search_fields = ('street','city','region','country',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

class ContactAdmin(admin.ModelAdmin):
	list_display = ('id','user','detail',)
	def save_model(self, request, obj, form, change):
		obj.userModifyId = request.user.id
		obj.save()

class ContactDetailAdmin(admin.ModelAdmin):
	list_display = ('id','owner','name','nickName','source','isPublic',)
	search_fields = ('name','firstName','lastName','nickName',)
	def save_model(self, request, obj, form, change):
		obj.userModifyId = request.user.id
		obj.save()

class CommunicationTypeContactAdmin(admin.ModelAdmin):
	list_display = ('id','communicationType','contact','name','value',)
	list_filter = ('communicationType',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

class CommunicationTypeAdmin(admin.ModelAdmin):
	list_display = ('id','type',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

class FileAdmin(admin.ModelAdmin):
	list_display = ('id','name','type',)
	list_filter = ('type',)
	search_fields = ('name','title','description',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

class FileVersionAdmin(admin.ModelAdmin):
	list_display = ('id','file','version','size','downloadCount','isPublic',)
	list_filter = ('isPublic',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

class VersionAdmin(admin.ModelAdmin):
	list_display = ('id','versionName',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

class ProfileAdmin(admin.ModelAdmin):
	list_display = ('id','userAccount',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

class ProfileDetailAdmin(admin.ModelAdmin):
	list_display = ('id','mode','value',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

"""class AddressTypeAdmin(admin.ModelAdmin):
	list_display = ('id','type',)
	exclude = ('userModifyId','userCreateId',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()"""

class OrganizationAdmin(admin.ModelAdmin):
	list_display = ('id','account','accountType','domain','name','brand','affiliate',)
	search_fields = ('name','description','accountType',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

class OrganizationGroupAdmin(admin.ModelAdmin):
	list_display = ('id','group','organization',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

class UserAccountAdmin(admin.ModelAdmin):
	list_display = ('id','user','isPublic',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

class IdentifierUserAccountAdmin(admin.ModelAdmin):
	list_display = ('id','userAccount','userAccountIdentifier','identifier',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

class UserAccountIdentifierAdmin(admin.ModelAdmin):
	list_display = ('id','type',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

class SkillAdmin(admin.ModelAdmin):
	list_display = ('id','catCode','skillName',)
	list_filter = ('catCode',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

class SkillUserAccountAdmin(admin.ModelAdmin):
	list_display = ('id','userAccount','skill','numberMonths','rating','isPublic',)
	list_filter = ('skill',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

class SkillGroupAdmin(admin.ModelAdmin):
	list_display = ('id','group','skill','numberMonths','rating','isPublic',)
	list_filter = ('skill',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

class IndustryAdmin(admin.ModelAdmin):
	list_display = ('id','group',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

class AddressOrganizationAdmin(admin.ModelAdmin):
	list_display = ('id','addressType','organization','address',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

class SocialNetworkOrganizationAdmin(admin.ModelAdmin):
	list_display = ('id','organization','socialNetwork','token',)
	list_filter = ('socialNetwork',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

class TaxTypeAdmin(admin.ModelAdmin):
	list_display = ('id','type',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

class TaxOrganizationAdmin(admin.ModelAdmin):
	list_display = ('id','organization','taxType','taxCode',)
	list_filter = ('taxType',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

class TaxUserAccountAdmin(admin.ModelAdmin):
	list_display = ('id','userAccount','taxType','taxCode',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

class SocialNetworkOrganizationGroupAdmin(admin.ModelAdmin):
	list_display = ('id','organizationGroup','socialNetwork','token',)
	list_filter = ('socialNetwork',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

class UserAccountRelationAdmin(admin.ModelAdmin):
	list_display = ('id','organization','organizationGroup','contract','isPublic',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

class UserAccountContractAdmin(admin.ModelAdmin):
	list_display = ('id','jobTitle','contractType','status',)
	list_filter = ('contractType','status',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

class InvitationAdmin(admin.ModelAdmin):
	list_display = ('id','fromUser','invitationCode','status',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

class AffiliateAdmin(admin.ModelAdmin):
	list_display = ('id','affiliateId', 'userAccount','organization',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

class TagUserTotalAdmin(admin.ModelAdmin):
	list_display = ('id','user','tag','number',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

class LinkUserTotalAdmin(admin.ModelAdmin):
	list_display = ('id','user','link','number',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

class SubscriptionDailyAdmin(admin.ModelAdmin):
	list_display = ('id','organization','userAccount','app','numberUsers','date',)
	list_filter = ('app',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

class SubscriptionAdmin(admin.ModelAdmin):
	list_display = ('id','organization','userAccount','app','subscriptionStatus',)
	list_filter = ('app',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

class SubscriptionItemMonthAdmin(admin.ModelAdmin):
	list_display = ('id','userAccount','organization','number','item','date',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

class ApplicationAdmin(admin.ModelAdmin):
	list_display = ('id','name','developer','developerOrg',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

class CalendarAdmin(admin.ModelAdmin):
	list_display = ('id','owner','timeDateStart','type',)
	list_filter = ('type',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

class CalendarInviteAdmin(admin.ModelAdmin):
	list_display = ('id','calendar','contact','status',)
	list_filter = ('status',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

class TaskListAdmin(admin.ModelAdmin):
	list_display = ()
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

class TaskAdmin(admin.ModelAdmin):
	list_display = ()
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

class TaskDetailAdmin(admin.ModelAdmin):
	list_display = ()
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

class TaskAssignAdmin(admin.ModelAdmin):
	list_display = ()
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

class NoteAdmin(admin.ModelAdmin):
	list_display = ()
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

class NotificationAdmin(admin.ModelAdmin):
	list_display = ('id','owner',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

class XmlMessageAdmin(admin.ModelAdmin):
	list_display = ('id','name','lang')
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

class MasterValueAdmin(admin.ModelAdmin):
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

########################################################################################

admin.site.register(Comment, CommentAdmin)
admin.site.register(GroupFollow, GroupFollowAdmin)
admin.site.register(GroupStream, GroupStreamAdmin)
admin.site.register(GroupStreamPublic, GroupStreamPublicAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(SocialNetwork, SocialNetworkAdmin)
admin.site.register(StatusMessage, StatusMessageAdmin)
admin.site.register(StatusShare, StatusShareAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(UserParam, UserParamAdmin)
admin.site.register(UserSocial, UserSocialAdmin)
admin.site.register(GroupSocial, GroupSocialAdmin)

admin.site.register(SocialNetworkUserSocial, SocialNetworkUserSocialAdmin)
admin.site.register(UserDetail, UserDetailAdmin)
admin.site.register(Link, LinkAdmin)
admin.site.register(Version, VersionAdmin)
admin.site.register(UserProfile, ProfileAdmin)
admin.site.register(ProfileDetail, ProfileDetailAdmin)
#admin.site.register(AddressType, AddressTypeAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(OrganizationGroup, OrganizationGroupAdmin)
admin.site.register(UserAccount, UserAccountAdmin)
admin.site.register(IdentifierUserAccount, IdentifierUserAccountAdmin)
admin.site.register(UserAccountIdentifier, UserAccountIdentifierAdmin)
admin.site.register(Skill, SkillAdmin)
admin.site.register(SkillUserAccount, SkillUserAccountAdmin)
admin.site.register(SkillGroup, SkillGroupAdmin)
admin.site.register(Industry, IndustryAdmin)
admin.site.register(AddressOrganization, AddressOrganizationAdmin)
admin.site.register(SocialNetworkOrganization, SocialNetworkOrganizationAdmin)
admin.site.register(TaxType, TaxTypeAdmin)
admin.site.register(TaxOrganization, TaxOrganizationAdmin)
admin.site.register(TaxUserAccount, TaxUserAccountAdmin)
admin.site.register(SocialNetworkOrganizationGroup, SocialNetworkOrganizationGroupAdmin)
admin.site.register(UserAccountRelation, UserAccountRelationAdmin)
admin.site.register(UserAccountContract, UserAccountContractAdmin)
admin.site.register(Invitation, InvitationAdmin)
admin.site.register(Affiliate, AffiliateAdmin)
admin.site.register(TagUserTotal, TagUserTotalAdmin)
admin.site.register(LinkUserTotal, LinkUserTotalAdmin)
admin.site.register(SubscriptionDaily, SubscriptionDailyAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(SubscriptionItemMonth, SubscriptionItemMonthAdmin)
admin.site.register(Application, ApplicationAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(XmlMessage, XmlMessageAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(ContactDetail, ContactDetailAdmin)
admin.site.register(MasterValue, MasterValueAdmin)
