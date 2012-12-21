from models import CoreParam, Application, Menu, View, Action, Workflow, XpTemplate, Settings, MetaKey, WorkflowView
from models import ApplicationMeta, MenuParam, ViewMeta, ViewParamValue, ViewMenu, ViewTmpl, WFParamValue, Param, ViewTag, ApplicationMedia
from models import ApplicationTag, Service, ServiceMenu

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

class ViewTagsInline(admin.StackedInline):
	model = ViewTag

class AppTagsInline(admin.StackedInline):
	model = ApplicationTag

class ServiceMenuInline(admin.StackedInline):
	model = ServiceMenu

class WorkflowViewParamValueInline(admin.StackedInline):
	model = WFParamValue

class ApplicationMediaInline(admin.StackedInline):
	model = ApplicationMedia

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
	list_filter = ('isSubscription','isPrivate','isAdmin','category','tags__name')
	search_fields = ('name', 'slug','title')
	raw_id_fields = ('developer','developerOrg','accessGroup')
	related_lookup_fields = {
	        'fk': ['developer','developerOrg','accessGroup'],
	    }
	inlines = [ ApplicationMetaInline, ApplicationMediaInline, AppTagsInline ]
	def save_model(self, request, obj, form, change):
		obj.userModifyId = request.user.id
		if not obj.id:
			obj.userCreateId = request.user.id
		obj.save()

class ServiceAdmin(admin.ModelAdmin):
	list_display = ('id','name', 'application', 'userCreateId', 'userModifyId', 'dateCreate', 'dateModify')
	list_display_links = ('name',)
	list_filter = ('application__title',)
	search_fields = ('name', 'application__name',)
	raw_id_fields = ('application',)
	related_lookup_fields = {
	        'fk': ['application'],
	    }
	exclude = ('implementation',)
	inlines = [ ServiceMenuInline ]
	def save_model(self, request, obj, form, change):
		obj.userModifyId = request.user.id
		if not obj.id:
			obj.userCreateId = request.user.id
		obj.save()

class MenuAdmin(admin.ModelAdmin):
	list_display = ('id','name','title','description','view','application','action','icon','language',\
		'userCreateId', 'userModifyId', 'dateCreate', 'dateModify')
	list_display_links = ('name',)
	list_filter = ('application__title',)
	search_fields = ('description','name','title')
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
	list_display = ('id','name','slug','application', 'service', 'winType','hasAuth',\
				'userCreateId', 'userModifyId', 'dateCreate', 'dateModify',)
	list_display_links = ('name',)
	list_filter = ('winType','hasAuth','service__name','application__title')
	search_fields = ('name','slug',)
	raw_id_fields = ('parent',)
	related_lookup_fields = {
	        'fk': ['parent'],
	    }
	inlines = [ ViewMetaInline, ViewParamValueInline, ViewTemplateInline, ViewMenuInline, ViewTagsInline ]
	exclude = ['implementation']
	def save_model(self, request, obj, form, change):
		obj.userModifyId = request.user.id
		if not obj.id:
			obj.userCreateId = request.user.id
		obj.save()

class ActionAdmin(admin.ModelAdmin):
	list_display = ('id','name','slug','application','service','hasAuth','userCreateId', 'userModifyId', 'dateCreate', 'dateModify')
	list_display_links = ('name',)
	list_filter = ('application',)
	search_fields = ('name', 'slug')
	raw_id_fields = ('application',)
	related_lookup_fields = {
	        'fk': ['application',],
	    }
	exclude = ['implementation']
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
admin.site.register(Service, ServiceAdmin)
admin.site.register(Menu, MenuAdmin)
admin.site.register(View, ViewAdmin)
admin.site.register(Action, ActionAdmin)
admin.site.register(Workflow, WorkflowAdmin)
admin.site.register(WorkflowView, WorkflowViewAdmin)
admin.site.register(XpTemplate, XpTemplateAdmin)
admin.site.register(MetaKey, MetaKeyAdmin)
admin.site.register(Settings, SettingsAdmin)
