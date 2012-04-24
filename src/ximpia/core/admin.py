from models import CoreParam, Application, CoreXmlMessage, UserSocial, Menu, MenuParam, View, ApplicationAccess, ViewMenu, Action
#from models import Navigation, NavigationParam, NavigationParamValue, Operation
from models import Workflow, WFParamValue, Param, WorkflowView

from django.contrib import admin

"""Copyright (c) 2011 Jorge Alegre Vilches
All rights reserved."""

class CoreParamAdmin(admin.ModelAdmin):
	list_display = ('id','mode','name','value','valueId', 'valueDate')
	list_filter = ('mode',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

class ApplicationAdmin(admin.ModelAdmin):
	list_display = ('code', 'name','developer','developerOrg','subscription','private')
	list_filter = ('subscription','private')
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

class ApplicationAccessAdmin(admin.ModelAdmin):
	list_display = ('application','userSocial')
	list_filter = ('application',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

class CoreXmlMessageAdmin(admin.ModelAdmin):
	list_display = ('id','name','lang')
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

class UserSocialAdmin(admin.ModelAdmin):
	list_display = ('id','user','name','title')
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

class MenuAdmin(admin.ModelAdmin):
	list_display = ('name','titleShort','parent')
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

class MenuParamAdmin(admin.ModelAdmin):
	list_display = ('menu','name','value')
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

class ViewMenuAdmin(admin.ModelAdmin):
	list_display = ('view','menu','order')
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

class WorkflowAdmin(admin.ModelAdmin):
	list_display = ('application','code')
	list_filter = ('application',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

class WorkflowViewAdmin(admin.ModelAdmin):
	list_display = ('flow', 'viewSource', 'viewTarget', 'action', 'order')
	list_filter = ('action','viewSource','viewTarget')
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

class ParamAdmin(admin.ModelAdmin):
	list_display = ('id',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

class WFParamValueAdmin(admin.ModelAdmin):
	list_display = ('id',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

admin.site.register(CoreParam, CoreParamAdmin)
admin.site.register(Application, ApplicationAdmin)
admin.site.register(ApplicationAccess, ApplicationAccessAdmin)
admin.site.register(CoreXmlMessage, CoreXmlMessageAdmin)
admin.site.register(UserSocial, UserSocialAdmin)
admin.site.register(Menu, MenuAdmin)
admin.site.register(MenuParam, MenuParamAdmin)
admin.site.register(View, ViewAdmin)
admin.site.register(Action, ActionAdmin)
admin.site.register(ViewMenu, ViewMenuAdmin)
admin.site.register(Workflow, WorkflowAdmin)
admin.site.register(WorkflowView, WorkflowViewAdmin)
admin.site.register(Param, ParamAdmin)
admin.site.register(WFParamValue, WFParamValueAdmin)
