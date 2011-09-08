from models import Comment, GroupFollow, GroupStream, GroupStreamPublic, Like
from models import SocialNetwork, StatusMessage, StatusShare, Tag, UserParam, UserX, GroupX
from django.contrib import admin

"""Copyright (c) 2010 Jorge Alegre Vilches
All rights reserved."""

class CommentAdmin(admin.ModelAdmin):
	list_display = ('id','User','Message')
	search_fields = ('Message',)
	exclude = ('UserModifyId','UserCreateId',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
        	obj.save()
class GroupFollowAdmin(admin.ModelAdmin):
	list_display = ('id','GroupSource','GroupTarget','Status')
	exclude = ('UserModifyId','UserCreateId',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
        	obj.save()
class GroupStreamAdmin(admin.ModelAdmin):
	list_display = ('id','PostId','User','Account','Group','Message')
	search_fields = ('Message',)
	exclude = ('UserModifyId','UserCreateId',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
        	obj.save()
class GroupStreamPublicAdmin(admin.ModelAdmin):
	list_display = ('id','PostId')
	exclude = ('UserModifyId','UserCreateId',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
        	obj.save()
class LikeAdmin(admin.ModelAdmin):
	list_display = ('id','User')
	exclude = ('UserModifyId','UserCreateId',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
        	obj.save()
class SocialNetworkAdmin(admin.ModelAdmin):
	list_display = ('Type',)
	exclude = ('UserModifyId','UserCreateId',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
        	obj.save()
class StatusMessageAdmin(admin.ModelAdmin):
	list_display = ('id','Message')
	exclude = ('UserModifyId','UserCreateId',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
        	obj.save()
class StatusShareAdmin(admin.ModelAdmin):
	list_display = ('User','Message')
	exclude = ('UserModifyId','UserCreateId',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
        	obj.save()
class TagAdmin(admin.ModelAdmin):
	list_display = ('Tag','SystemTag','Popularity')
	search_fields = ('Tag',)
	exclude = ('UserModifyId','UserCreateId',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
        	obj.save()
class UserParamAdmin(admin.ModelAdmin):
	list_display = ('Mode','Name','Value','ValueId')
	list_filter = ('Mode',)
	exclude = ('UserModifyId','UserCreateId',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
        	obj.save()
class UserXAdmin(admin.ModelAdmin):
	list_display = ('User','UploadPic','Suspended',)
	exclude = ('UserModifyId','UserCreateId',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
        	obj.save()
class GroupXAdmin(admin.ModelAdmin):
	list_display = ('Group','XimpiaGroup','Industry', 'Public')
	list_filter = ('XimpiaGroup','Industry','Public')
	search_fields = ('Group',)
	exclude = ('UserModifyId','UserCreateId',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
        	obj.save()

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
admin.site.register(UserX, UserXAdmin)
admin.site.register(GroupX, GroupXAdmin)
