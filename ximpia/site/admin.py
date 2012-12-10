from models import Tag, GroupChannel, Invitation, Param, XmlMessage, UserChannel, SocialNetworkUser, Settings, Address, Category, MetaKey,\
	SignupData, TagMode, UserMeta, UserProfile 

from django.contrib import admin

admin.site.register(XmlMessage)
admin.site.register(Param)
admin.site.register(SocialNetworkUser)
admin.site.register(Tag)
admin.site.register(UserChannel)
admin.site.register(GroupChannel)
admin.site.register(Invitation)
admin.site.register(Settings)
#admin.site.register(Address)
admin.site.register(Category)
admin.site.register(MetaKey)
admin.site.register(SignupData)
#admin.site.register(TagMode)
#admin.site.register(UserMeta)
#admin.site.register(UserProfile)
