from models import Tag, Invitation, Param, UserChannel, SocialNetworkUser, Setting, Address, Category, MetaKey,\
	SignupData, TagMode, UserMeta, UserProfile, InvitationMeta, GroupTag, UserAddress, Group, UserChannelGroup

from django.contrib import admin

# INLINES

class InvitationMetaInline(admin.StackedInline):
	model = InvitationMeta

class GroupTagsInline(admin.StackedInline):
	model = GroupTag


class AddressInline(admin.StackedInline):
	model = UserAddress
	raw_id_fields = ('address',)
	related_lookup_fields = {
	        'fk': ['address',],
	    }

class GroupsInline(admin.StackedInline):
	model = UserChannelGroup

# INLINES

class AddressAdmin(admin.ModelAdmin):
	list_display = ('id','city','region','zipCode','country','userCreateId', 'userModifyId', 'dateCreate', 'dateModify')
	list_display_links = ('id',)
	search_fields = ('city', 'region','country','zipCode')
	def save_model(self, request, obj, form, change):
		obj.userModifyId = request.user.id
		if not obj.id:
			obj.userCreateId = request.user.id
		obj.save()

class ParamAdmin(admin.ModelAdmin):
	list_display = ('id','mode','name','paramType','value','userCreateId', 'userModifyId', 'dateCreate', 'dateModify')
	list_filter = ('mode','paramType')
	list_display_links = ('name','mode')
	search_fields = ('name',)
	ordering = ('mode',)
	def save_model(self, request, obj, form, change):
		obj.userModifyId = request.user.id
		if not obj.id:
			obj.userCreateId = request.user.id
		obj.save()

class SocialNetworkUserAdmin(admin.ModelAdmin):
	list_display = ('id','user','socialNetwork','socialId','token','userCreateId', 'userModifyId', 'dateCreate', 'dateModify')
	list_display_links = ('user',)
	list_filter = ('socialNetwork','socialId')
	search_fields = ('user__username','user__first_name','user__last_name',)
	raw_id_fields = ('user','socialNetwork')
	related_lookup_fields = {
	        'fk': ['user','socialNetwork'],
	    }
	def save_model(self, request, obj, form, change):
		obj.userModifyId = request.user.id
		if not obj.id:
			obj.userCreateId = request.user.id
		obj.save()

class TagAdmin(admin.ModelAdmin):
	list_display = ('id','name','mode','popularity','isPublic','userCreateId', 'userModifyId', 'dateCreate', 'dateModify')
	list_display_links = ('name',)
	list_filter = ('isPublic','mode__mode')
	search_fields = ('name',)
	raw_id_fields = ('mode',)
	related_lookup_fields = {
	        'fk': ['mode'],
	    }
	def save_model(self, request, obj, form, change):
		obj.userModifyId = request.user.id
		if not obj.id:
			obj.userCreateId = request.user.id
		obj.save()

class TagModeAdmin(admin.ModelAdmin):
	list_display = ('id','mode','isPublic','userCreateId', 'userModifyId', 'dateCreate', 'dateModify')
	list_display_links = ('mode',)
	list_filter = ('isPublic','mode')
	def save_model(self, request, obj, form, change):
		obj.userModifyId = request.user.id
		if not obj.id:
			obj.userCreateId = request.user.id
		obj.save()

class UserChannelAdmin(admin.ModelAdmin):
	list_display = ('id','name','title','user','tag','userCreateId', 'userModifyId', 'dateCreate', 'dateModify')
	list_display_links = ('name','title')
	list_filter = ('tag',)
	search_fields = ('name','title','user__first_name','user__last_name','user__username')
	raw_id_fields = ('user',)
	related_lookup_fields = {
	        'fk': ['user','user'],
	    }
	inlines = [ GroupsInline ]
	def save_model(self, request, obj, form, change):
		obj.userModifyId = request.user.id
		if not obj.id:
			obj.userCreateId = request.user.id
		obj.save()

class UserMetaAdmin(admin.ModelAdmin):
	list_display = ('id','user','meta','userCreateId', 'userModifyId', 'dateCreate', 'dateModify')
	list_display_links = ('user',)
	list_filter = ('meta__name',)
	search_fields = ('user__username','user__first_name','user__last_name','meta__name')
	raw_id_fields = ('user',)
	related_lookup_fields = {
	        'fk': ['user','user'],
	    }
	def save_model(self, request, obj, form, change):
		obj.userModifyId = request.user.id
		if not obj.id:
			obj.userCreateId = request.user.id
		obj.save()

class UserProfileAdmin(admin.ModelAdmin):
	list_display = ('id','user','status','userCreateId', 'userModifyId', 'dateCreate', 'dateModify')
	list_display_links = ('user',)
	list_filter = ('status',)
	search_fields = ('user__username','user__first_name','user__last_name')
	raw_id_fields = ('user',)
	related_lookup_fields = {
	        'fk': ['user','user'],
	    }
	inlines = [ AddressInline ]
	def save_model(self, request, obj, form, change):
		obj.userModifyId = request.user.id
		if not obj.id:
			obj.userCreateId = request.user.id
		obj.save()

class GroupAdmin(admin.ModelAdmin):
	list_display = ('id','group','groupNameId','isPublic','parent','category','userCreateId', 'userModifyId', 'dateCreate', 'dateModify')
	list_display_links = ('group',)
	list_filter = ('category','isPublic')
	search_fields = ('groupNameId','group__name')
	raw_id_fields = ('group','parent',)
	related_lookup_fields = {
	        'fk': ['group','parent'],
	    }
	inlines = [ GroupTagsInline ]
	def save_model(self, request, obj, form, change):
		obj.userModifyId = request.user.id
		if not obj.id:
			obj.userCreateId = request.user.id
		obj.save()

class InvitationAdmin(admin.ModelAdmin):
	list_display = ('id','fromUser','invitationCode','status','number','userCreateId', 'userModifyId', 'dateCreate', 'dateModify')
	list_display_links = ('invitationCode',)
	list_filter = ('status',)
	search_fields = ('fromUser',)
	raw_id_fields = ('fromUser',)
	related_lookup_fields = {
	        'fk': ['fromUser','fromUser'],
	    }
	inlines = [ InvitationMetaInline ]
	def save_model(self, request, obj, form, change):
		obj.userModifyId = request.user.id
		if not obj.id:
			obj.userCreateId = request.user.id
		obj.save()

class SettingAdmin(admin.ModelAdmin):
	list_display = ('id','name','application','description','mustAutoload','userCreateId', 'userModifyId', 'dateCreate', 'dateModify')
	list_display_links = ('name',)
	list_filter = ('mustAutoload',)
	raw_id_fields = ('application',)
	related_lookup_fields = {
	        'fk': ['application',],
	    }
	ordering = ['name']
	def save_model(self, request, obj, form, change):
		obj.userModifyId = request.user.id
		if not obj.id:
			obj.userCreateId = request.user.id
		obj.save()

class CategoryAdmin(admin.ModelAdmin):
	list_display = ('id','name','parent','type','isPublished','isPublic','menuOrder',\
		'userCreateId', 'userModifyId', 'dateCreate', 'dateModify')
	list_display_links = ('name',)
	list_filter = ('type','isPublished','isPublic')
	search_fields = ('name','description')
	def save_model(self, request, obj, form, change):
		obj.userModifyId = request.user.id
		if not obj.id:
			obj.userCreateId = request.user.id
		obj.save()

class MetaKeyAdmin(admin.ModelAdmin):
	list_display = ('id','name','keyType','userCreateId', 'userModifyId', 'dateCreate', 'dateModify')
	list_display_links = ('name',)
	list_filter = ('keyType__name',)
	ordering = ['name']
	def save_model(self, request, obj, form, change):
		obj.userModifyId = request.user.id
		if not obj.id:
			obj.userCreateId = request.user.id
		obj.save()

class SignupDataAdmin(admin.ModelAdmin):
	list_display = ('id','user','activationCode','userCreateId', 'userModifyId', 'dateCreate', 'dateModify')
	list_display_links = ('user',)
	def save_model(self, request, obj, form, change):
		obj.userModifyId = request.user.id
		if not obj.id:
			obj.userCreateId = request.user.id
		obj.save()

admin.site.register(Param, ParamAdmin)
admin.site.register(SocialNetworkUser, SocialNetworkUserAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(TagMode, TagModeAdmin)
admin.site.register(UserChannel, UserChannelAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Invitation, InvitationAdmin)
admin.site.register(Setting, SettingAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(MetaKey, MetaKeyAdmin)
admin.site.register(SignupData, SignupDataAdmin)
admin.site.register(UserMeta, UserMetaAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
