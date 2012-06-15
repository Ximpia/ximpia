from django.contrib import admin

from models import Media

class MediaAdmin(admin.ModelAdmin):
	list_display = ('name','title','isFeatured')
	def save_model(self, request, obj, form, change):
		obj.UserModifyId = request.user.id
		obj.save()

admin.site.register(Media, MediaAdmin)
