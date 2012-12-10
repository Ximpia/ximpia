from models import CoreParam, Application, Menu, View, Action, Workflow, XpTemplate, Settings, MetaKey 

from django.contrib import admin

class CoreParamAdmin(admin.ModelAdmin):
	list_display = ('id','mode','name','value',)
	list_filter = ('mode',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

class ApplicationAdmin(admin.ModelAdmin):
	list_display = ('code', 'name','developer','developerOrg','isSubscription','isPrivate')
	list_filter = ('isSubscription','isPrivate')
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

class UserSocialAdmin(admin.ModelAdmin):
	list_display = ('id','user','name','title')
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

class MenuAdmin(admin.ModelAdmin):
	list_display = ('name','titleShort','title','view','action','icon')
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

class ViewAdmin(admin.ModelAdmin):
	list_display = ('application','name')
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

class ActionAdmin(admin.ModelAdmin):
	list_display = ('application','name')
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

class WorkflowAdmin(admin.ModelAdmin):
	list_display = ('application','code')
	list_filter = ('application',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

class XpTemplateAdmin(admin.ModelAdmin):
	list_display = ('id',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

class MetaKeyAdmin(admin.ModelAdmin):
	list_display = ('id',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

class SettingsAdmin(admin.ModelAdmin):
	list_display = ('id',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

admin.site.register(CoreParam, CoreParamAdmin)
admin.site.register(Application, ApplicationAdmin)
admin.site.register(Menu, MenuAdmin)
admin.site.register(View, ViewAdmin)
admin.site.register(Action, ActionAdmin)
admin.site.register(Workflow, WorkflowAdmin)
admin.site.register(XpTemplate, XpTemplateAdmin)
admin.site.register(MetaKey, MetaKeyAdmin)
admin.site.register(Settings, SettingsAdmin)
