from models import HumanResourcesParam, Professional, OrganizationGroup, Tax
from models import Organization, Address, OrganizationOptions, ProfessionalContract
from models import ProfessionalIdentifier, ProfessionalTaskHistory, ProfessionalHistory, Curriculum
from models import ProfessionalEducation, ProfessionalWorkExperience, Skill, ProfessionalFeedback, ProfileDetail
from models import Profile, File, Custom
from django.contrib import admin

"""Copyright (c) 2010 Jorge Alegre Vilches
All rights reserved."""

class HumanResourcesParamAdmin(admin.ModelAdmin):
	exclude = ('UserModifyId','UserCreateId',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
        	obj.save()
class ProfessionalAdmin(admin.ModelAdmin):
	exclude = ('UserModifyId','UserCreateId',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
        	obj.save()
class OrganizationGroupAdmin(admin.ModelAdmin):
	exclude = ('UserModifyId','UserCreateId',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
        	obj.save()
class TaxAdmin(admin.ModelAdmin):
	exclude = ('UserModifyId','UserCreateId',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
        	obj.save()
class OrganizationAdmin(admin.ModelAdmin):
	exclude = ('UserModifyId','UserCreateId',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
        	obj.save()
class AddressAdmin(admin.ModelAdmin):
	exclude = ('UserModifyId','UserCreateId',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
        	obj.save()
class OrganizationOptionsAdmin(admin.ModelAdmin):
	exclude = ('UserModifyId','UserCreateId',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
        	obj.save()
class ProfessionalAdmin(admin.ModelAdmin):
	exclude = ('UserModifyId','UserCreateId',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
        	obj.save()
class ProfessionalContractAdmin(admin.ModelAdmin):
	exclude = ('UserModifyId','UserCreateId',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
        	obj.save()
class ProfessionalIdentifierAdmin(admin.ModelAdmin):
	exclude = ('UserModifyId','UserCreateId',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
        	obj.save()
class ProfessionalTaskHistoryAdmin(admin.ModelAdmin):
	exclude = ('UserModifyId','UserCreateId',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
        	obj.save()
class ProfessionalHistoryAdmin(admin.ModelAdmin):
	exclude = ('UserModifyId','UserCreateId',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
        	obj.save()
class CurriculumAdmin(admin.ModelAdmin):
	exclude = ('UserModifyId','UserCreateId',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
        	obj.save()
class ProfessionalEducationAdmin(admin.ModelAdmin):
	exclude = ('UserModifyId','UserCreateId',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
        	obj.save()
class ProfessionalWorkExperienceAdmin(admin.ModelAdmin):
	exclude = ('UserModifyId','UserCreateId',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
        	obj.save()
class SkillAdmin(admin.ModelAdmin):
	exclude = ('UserModifyId','UserCreateId',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
        	obj.save()
class ProfessionalFeedbackAdmin(admin.ModelAdmin):
	exclude = ('UserModifyId','UserCreateId',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
        	obj.save()
class ProfileDetailAdmin(admin.ModelAdmin):
	exclude = ('UserModifyId','UserCreateId',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
        	obj.save()
class ProfileAdmin(admin.ModelAdmin):
	exclude = ('UserModifyId','UserCreateId',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
        	obj.save()
class FileAdmin(admin.ModelAdmin):
	exclude = ('UserModifyId','UserCreateId',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
        	obj.save()
class CustomAdmin(admin.ModelAdmin):
	exclude = ('UserModifyId','UserCreateId',)
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
        	obj.save()

admin.site.register(HumanResourcesParam, HumanResourcesParamAdmin)
admin.site.register(OrganizationGroup, OrganizationGroupAdmin)
admin.site.register(Tax, TaxAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(OrganizationOptions, OrganizationOptionsAdmin)
admin.site.register(Professional, ProfessionalAdmin)
admin.site.register(ProfessionalContract, ProfessionalContractAdmin)
admin.site.register(ProfessionalIdentifier, ProfessionalIdentifierAdmin)
admin.site.register(ProfessionalTaskHistory, ProfessionalTaskHistoryAdmin)
admin.site.register(ProfessionalHistory, ProfessionalHistoryAdmin)
admin.site.register(Curriculum, CurriculumAdmin)
admin.site.register(ProfessionalEducation, ProfessionalEducationAdmin)
admin.site.register(ProfessionalWorkExperience, ProfessionalWorkExperienceAdmin)
admin.site.register(Skill, SkillAdmin)
admin.site.register(ProfessionalFeedback, ProfessionalFeedbackAdmin)
admin.site.register(ProfileDetail, ProfileDetailAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(File, FileAdmin)
admin.site.register(Custom, CustomAdmin)
