from models import CoreParam, Application, Menu, View, Action, Workflow, XpTemplate, Settings, MetaKey, ApplicationAccess, WorkflowView
from models import ApplicationMeta, MenuParam, ViewMeta, ViewParamValue, ViewMenu, ViewTmpl, WFParamValue, Param

from django.contrib import admin

# INLINES 

class ApplicationMetaInline(admin.StackedInline):
	model = ApplicationMeta

class ViewMetaInline(admin.StackedInline):
	model = ViewMeta

class MenuParamInline(admin.StackedInline):
	model = MenuParam

class ViewParamValueInline(admin.StackedInline):
	model = ViewParamValue

class ViewMenuInline(admin.StackedInline):
	model = ViewMenu

class ViewTemplateInline(admin.StackedInline):
	model = ViewTmpl

class WorkflowViewParamValueInline(admin.StackedInline):
	model = WFParamValue

# INLINES

class CoreParamAdmin(admin.ModelAdmin):
	list_display = ('id','mode','name','paramType','value','userCreateId', 'userModifyId', 'dateCreate', 'dateModify')
	list_filter = ('mode','paramType')
	list_display_links = ('name','mode')
	search_fields = ('name',)
	def save_model(self, request, obj, form, change):
		obj.userModifyId = request.user.id
		if not obj.id:
			obj.userCreateId = request.user.id
		obj.save()

class ParamAdmin(admin.ModelAdmin):
	list_display = ('id','name','title','application','paramType','isView','isWorkflow',\
		'userCreateId', 'userModifyId', 'dateCreate', 'dateModify')
	list_filter = ('application__title','paramType','isView','isWorkflow')
	list_display_links = ('name',)
	search_fields = ('title','name')
	def save_model(self, request, obj, form, change):
		obj.userModifyId = request.user.id
		if not obj.id:
			obj.userCreateId = request.user.id
		obj.save()


class ApplicationAdmin(admin.ModelAdmin):
	list_display = ('id','name','slug','title','developer','developerOrg','isSubscription','isPrivate','isAdmin',\
		'userCreateId', 'userModifyId', 'dateCreate', 'dateModify')
	list_display_links = ('name',)
	list_filter = ('isSubscription','isPrivate','isAdmin')
	search_fields = ('name', 'slug','title')
	raw_id_fields = ('developer','developerOrg')
	related_lookup_fields = {
	        'fk': ['developer','developerOrg'],
	    }
	inlines = [ ApplicationMetaInline ]
	def save_model(self, request, obj, form, change):
		obj.userModifyId = request.user.id
		if not obj.id:
			obj.userCreateId = request.user.id
		obj.save()

class ApplicationAccessAdmin(admin.ModelAdmin):
	list_display = ('id','application','userChannel',\
		'userCreateId', 'userModifyId', 'dateCreate', 'dateModify')
	list_display_links = ('userChannel',)
	list_filter = ('application__title',)
	search_fields = ('userChannel__user__first_name','userChannel__user__last_name','userChannel__user__username')
	raw_id_fields = ('userChannel',)
	related_lookup_fields = {
	        'fk': ['userChannel','userChannel'],
	    }
	def save_model(self, request, obj, form, change):
		obj.userModifyId = request.user.id
		if not obj.id:
			obj.userCreateId = request.user.id
		obj.save()

class MenuAdmin(admin.ModelAdmin):
	list_display = ('id','name','titleShort','title','view','application','action','icon','language',\
		'userCreateId', 'userModifyId', 'dateCreate', 'dateModify')
	list_display_links = ('titleShort',)
	list_filter = ('application__title',)
	search_fields = ('title','name','titleShort')
	raw_id_fields = ('application','view','action')
	related_lookup_fields = {
	        'fk': ['application','view','action'],
	    }
	inlines = [ MenuParamInline ]
	def save_model(self, request, obj, form, change):
		obj.userModifyId = request.user.id
		if not obj.id:
			obj.userCreateId = request.user.id
		obj.save()

class ViewAdmin(admin.ModelAdmin):
	list_display = ('id','name','slug','application','winType','hasAuth','userCreateId', 'userModifyId', 'dateCreate', 'dateModify',)
	list_display_links = ('name',)
	list_filter = ('application__title','winType','hasAuth',)
	search_fields = ('name','slug',)
	raw_id_fields = ('application','parent')
	related_lookup_fields = {
	        'fk': ['application','parent',],
	    }
	inlines = [ ViewMetaInline, ViewParamValueInline, ViewTemplateInline, ViewMenuInline ]
	def save_model(self, request, obj, form, change):
		obj.userModifyId = request.user.id
		if not obj.id:
			obj.userCreateId = request.user.id
		obj.save()

class ActionAdmin(admin.ModelAdmin):
	list_display = ('id','application','name','slug','hasAuth','userCreateId', 'userModifyId', 'dateCreate', 'dateModify')
	list_display_links = ('name',)
	list_filter = ('application',)
	search_fields = ('name', 'slug')
	raw_id_fields = ('application',)
	related_lookup_fields = {
	        'fk': ['application',],
	    }
	def save_model(self, request, obj, form, change):
		obj.userModifyId = request.user.id
		if not obj.id:
			obj.userCreateId = request.user.id
		obj.save()

class WorkflowAdmin(admin.ModelAdmin):
	list_display = ('id','code','application','resetStart','deleteOnEnd','jumpToView',\
		'userCreateId', 'userModifyId','dateCreate', 'dateModify')
	list_display_links = ('code',)
	list_filter = ('application__title',)
	raw_id_fields = ('application',)
	related_lookup_fields = {
	        'fk': ['application',],
	    }
	def save_model(self, request, obj, form, change):
		obj.userModifyId = request.user.id
		if not obj.id:
			obj.userCreateId = request.user.id
		obj.save()

class WorkflowViewAdmin(admin.ModelAdmin):
	list_display = ('id','order','flow','viewSource','viewTarget','action',\
		'userCreateId', 'userModifyId','dateCreate', 'dateModify')
	list_display_links = ('id',)
	list_filter = ('flow__code',)
	raw_id_fields = ('flow','viewSource','viewTarget','action')
	related_lookup_fields = {
	        'fk': ['flow','viewSource','viewTarget','action'],
	    }
	inlines = [ WorkflowViewParamValueInline ]
	def save_model(self, request, obj, form, change):
		obj.userModifyId = request.user.id
		if not obj.id:
			obj.userCreateId = request.user.id
		obj.save()

class XpTemplateAdmin(admin.ModelAdmin):
	list_display = ('id','name','alias','application','language','country','winType','device',\
		'userCreateId', 'userModifyId','dateCreate', 'dateModify')
	list_display_links = ('name',)
	list_filter = ('application__title',)
	search_fields = ('name', 'alias',)
	raw_id_fields = ('application',)
	related_lookup_fields = {
	        'fk': ['application','application'],
	    }
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

class SettingsAdmin(admin.ModelAdmin):
	list_display = ('id','name','description','mustAutoload','userCreateId', 'userModifyId', 'dateCreate', 'dateModify')
	list_display_links = ('name',)
	list_filter = ('mustAutoload',)
	ordering = ['name']
	def save_model(self, request, obj, form, change):
		obj.userModifyId = request.user.id
		if not obj.id:
			obj.userCreateId = request.user.id
		obj.save()

admin.site.register(CoreParam, CoreParamAdmin)
admin.site.register(Param, ParamAdmin)
admin.site.register(Application, ApplicationAdmin)
admin.site.register(ApplicationAccess, ApplicationAccessAdmin)
admin.site.register(Menu, MenuAdmin)
admin.site.register(View, ViewAdmin)
admin.site.register(Action, ActionAdmin)
admin.site.register(Workflow, WorkflowAdmin)
admin.site.register(WorkflowView, WorkflowViewAdmin)
admin.site.register(XpTemplate, XpTemplateAdmin)
admin.site.register(MetaKey, MetaKeyAdmin)
admin.site.register(Settings, SettingsAdmin)
