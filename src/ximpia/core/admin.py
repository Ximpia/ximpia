from models import CoreParam, Application, CoreXmlMessage

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
	list_display = ('id','code', 'name','developer','developerOrg',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

class CoreXmlMessageAdmin(admin.ModelAdmin):
	list_display = ('id','name','lang')
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

admin.site.register(CoreParam, CoreParamAdmin)
admin.site.register(Application, ApplicationAdmin)
admin.site.register(CoreXmlMessage, CoreXmlMessageAdmin)
