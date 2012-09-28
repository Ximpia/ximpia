from models import SocialNetwork, Tag, GroupChannel, Organization, OrganizationGroup, Invitation, Param, XmlMessage, UserDetail
from models import SocialNetworkUser

from django.contrib import admin

from models import Video

class VideoAdmin(admin.ModelAdmin):
	list_display = ('name','title','isFeatured')
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

#######################################################

class XmlMessageAdmin(admin.ModelAdmin):
	list_display = ('id','name','lang')
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

class ParamAdmin(admin.ModelAdmin):
	list_display = ('id','mode','name','value','valueId', 'valueDate', 'paramType')
	list_filter = ('paramType', 'mode',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

class SocialNetworkAdmin(admin.ModelAdmin):
	list_display = ('id','myType',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

class SocialNetworkUserAdmin(admin.ModelAdmin):
	list_display = ('socialNetwork','socialId',)
	list_filter = ('socialNetwork',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

class TagAdmin(admin.ModelAdmin):
	list_display = ('id','name','mode','popularity')
	list_filter = ('mode',)
	search_fields = ('name',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

class GroupChannelAdmin(admin.ModelAdmin):
	list_display = ('id','group','groupNameId', 'isXimpiaGroup','isIndustry', 'isOrgGroup', 'isPublic',)
	list_filter = ('isXimpiaGroup','isIndustry','isPublic','isOrgGroup',)
	search_fields = ('group',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

class OrganizationAdmin(admin.ModelAdmin):
	list_display = ('id','account','accountType','domain','name',)
	search_fields = ('name','description','accountType',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

class OrganizationGroupAdmin(admin.ModelAdmin):
	list_display = ('id','group','organization',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

class InvitationAdmin(admin.ModelAdmin):
	list_display = ('id','fromUser','invitationCode','status','domain',)
	list_filter = ('status',)
	search_fields = ('domain','message')
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

admin.site.register(Video, VideoAdmin)

###############################################

admin.site.register(XmlMessage, XmlMessageAdmin)
admin.site.register(Param, ParamAdmin)
admin.site.register(SocialNetwork, SocialNetworkAdmin)
admin.site.register(SocialNetworkUser, SocialNetworkUserAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(GroupChannel, GroupChannelAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(OrganizationGroup, OrganizationGroupAdmin)
admin.site.register(Invitation, InvitationAdmin)
admin.site.register(UserDetail)
