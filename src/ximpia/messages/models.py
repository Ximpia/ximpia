#import base64
#import time
#import os
#import string
#import cPickle
#import random
#import json
#import simplejson as json
import types

from django.db import models
#from django.db.models import Q
from django.contrib.auth.models import User as UserSys, Group as GroupSys
#from django.contrib.sessions.backends.db import SessionStore
#from django.contrib.sessions.models import Session
#from django.utils.hashcompat import md5_constructor
#from django.http import HttpResponse

from django.utils.translation import ugettext as _
#from ximpia import util

#from ximpia import settings
#from ximpia.users.models import Link

from ximpia.social_network.models import Constants
from ximpia.social_network.models import Choices as ChoicesMain

class DeleteManager(models.Manager):
    def get_query_set(self):
        return super(DeleteManager, self).get_query_set().filter(Delete=False)

class MessageAddr(models.Model):
    """Addreses in Messages Model
    Address: Can be email or social network id
    Type"""
    Address = models.CharField(max_length=200)
    Type = models.CharField(max_length=20, choices=ChoicesMain.MSG_MEDIA)
    Delete = models.BooleanField(default=False)
    DateCreate = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    DateModify = models.DateTimeField(auto_now=True, null=True, blank=True)
    UserCreateId = models.IntegerField(null=True, blank=True)
    UserModifyId = models.IntegerField(null=True, blank=True)
    objects = DeleteManager()
    objects_del = models.Manager()
    def __unicode__(self):
        return str(self.Address) + ' - ' + str(self.Type)
    class Meta:
        db_table = 'MG_MSG_ADDR'
        verbose_name_plural = "MessageAddresses"

class MessageSent(models.Model):
    """Message Sent Model
    FK: Message
    FK: UserFrom
    MN: UsersTo
    FK: GroupFrom [optional]
    FK: GroupTo [optional]
    MN: EmailAddrsTo
    MN: Logs"""
    Message = models.ForeignKey('Message')
    UserFrom = models.ForeignKey('social_network.UserX', related_name='sent_user_from')
    UsersTo = models.ManyToManyField('social_network.UserX', null=True, blank=True, related_name='sent_users_to')
    GroupFrom = models.ForeignKey('social_network.OrganizationGroup', null=True, blank=True, related_name='sent_group_from') # Representation rights for department ????
    GroupsTo = models.ManyToManyField('social_network.OrganizationGroup', null=True, blank=True, related_name='sent_groups_to') # Rights to send to that group, belong to group or follow group
    AddrsTo = models.ManyToManyField('MessageAddr', null=True, blank=True)
    Logs = models.ManyToManyField('MessageLog', null=True, blank=True)
    Delete = models.BooleanField(default=False)
    DateCreate = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    DateModify = models.DateTimeField(auto_now=True, null=True, blank=True)
    UserCreateId = models.IntegerField(null=True, blank=True)
    UserModifyId = models.IntegerField(null=True, blank=True)
    objects = DeleteManager()
    objects_del = models.Manager()
    def __unicode__(self):
        return _('Message Sent ') + str(self.pk)
    class Meta:
        db_table = 'MG_MSG_SENT'
        verbose_name_plural = "MessagesSent"

class MessageReply(models.Model):
    """Message Reply Model
    FK: Message
    FK: UserFrom [optional]
    FK: GroupFrom [optional]
    FK: Discussion [optional]
    MN: Like
    MN: Share
    MN: Files
    MN: Links
    MN: Tags
    Message
    DiscussionsUnread"""
    Message = models.ForeignKey('Message')
    UserFrom = models.ForeignKey('social_network.UserX', null=True, blank=True)
    GroupFrom = models.ForeignKey('social_network.OrganizationGroup', null=True, blank=True)
    MessageContent = models.TextField()
    Links = models.ManyToManyField('social_network.Link', null=True, blank=True)
    Tags = models.ManyToManyField('social_network.Tag', null=True, blank=True)
    Like = models.ManyToManyField('social_network.Like', null=True, blank=True)
    Share = models.ManyToManyField('social_network.StatusShare', null=True, blank=True)
    Files = models.ManyToManyField('social_network.File', null=True, blank=True)
    Discussion = models.ForeignKey('Discussion', null=True, blank=True)
    DiscussionsUnread = models.SmallIntegerField(default=0)
    Delete = models.BooleanField(default=False)
    DateCreate = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    DateModify = models.DateTimeField(auto_now=True, null=True, blank=True)
    UserCreateId = models.IntegerField(null=True, blank=True)
    UserModifyId = models.IntegerField(null=True, blank=True)
    objects = DeleteManager()
    objects_del = models.Manager()
    def __unicode__(self):
        return _('Message Reply') + ' ' + str(self.id)
    class Meta:
        db_table = 'MG_MSG_REPLY'
        verbose_name_plural = "MessagesReply"

class Message(models.Model):
    """Messages Received Model
    FK; Discussion [optional]    
    MN: Replies
    MN: Files
    MN: Tags
    MN: Links
    MN: Like
    Summary
    Message
    Source
    Secure"""
    Replies = models.ManyToManyField('MessageReply', null=True, blank=True)
    Summary = models.CharField(max_length=140)
    Message = models.TextField()
    Links = models.ManyToManyField('social_network.Link', null=True, blank=True)
    Files = models.ManyToManyField('social_network.File', related_name='message_files', null=True, blank=True)
    Like = models.ManyToManyField('social_network.Like', null=True, blank=True)
    Discussion = models.ForeignKey('Discussion', null=True, blank=True)
    DiscussionsUnread = models.SmallIntegerField(default=0)
    Tags = models.ManyToManyField('social_network.Tag', null=True, blank=True)
    Archived = models.BooleanField(default=False, db_index=True)
    Source = models.CharField(max_length=10, choices=ChoicesMain.MSG_MEDIA, default=Constants.XIMPIA)
    Secure = models.BooleanField(default=False)
    Delete = models.BooleanField(default=False)
    DateCreate = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    DateModify = models.DateTimeField(auto_now=True, null=True, blank=True)
    UserCreateId = models.IntegerField(null=True, blank=True)
    UserModifyId = models.IntegerField(null=True, blank=True)
    objects = DeleteManager()
    objects_del = models.Manager()
    def __unicode__(self):
        return _('Message') + ' ' + str(self.pk)
    class Meta:
        db_table = 'MG_MSG'
        verbose_name_plural = "Messages"

class MessageReceived(models.Model):
    """Messages Received Model
    FK: Message
    FK: UserTo [optional]
    FK: GroupTo [optional]
    FK: UserFrom [optional]
    FK: GroupFrom [optional]
    MN: AddrsFrom"""
    Message = models.ForeignKey('Message')
    UserFrom = models.ForeignKey('social_network.UserX', null=True, blank=True, related_name='recv_user_from')
    GroupFrom = models.ForeignKey('social_network.OrganizationGroup', null=True, blank=True, related_name='recv_group_from')
    AddrsFrom = models.ManyToManyField('MessageAddr', null=True, blank=True, related_name='recv_addr_from')
    UserTo = models.ForeignKey('social_network.UserX', null=True, blank=True, related_name='recv_user_to')
    GroupTo = models.ForeignKey('social_network.OrganizationGroup', null=True, blank=True, related_name='recv_group_to')
    AddrTo = models.ForeignKey('MessageAddr', null=True, blank=True, related_name='recv_addr_to')
    Delete = models.BooleanField(default=False)
    DateCreate = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    DateModify = models.DateTimeField(auto_now=True, null=True, blank=True)
    UserCreateId = models.IntegerField(null=True, blank=True)
    UserModifyId = models.IntegerField(null=True, blank=True)
    objects = DeleteManager()
    objects_del = models.Manager()
    def __unicode__(self):
        return _('Message Received') + ' ' + str(self.pk)
    class Meta:
        db_table = 'MG_MSG_RECEIVED'
        verbose_name_plural = "MessagesReceived"

class MessageLog(models.Model):
    """Message Log Model
    FK: UserFrom
    FK: UserTo
    FK: EmailAddr
    MessageId
    Action"""
    UserFrom = models.ForeignKey('social_network.UserX', related_name='msg_log_user_from')
    MessageId = models.BigIntegerField(db_index=True)
    UserTo = models.ForeignKey('social_network.UserX', null=True, blank=True, related_name='msg_log_user_to')
    Addr = models.ForeignKey('MessageAddr', null=True, blank=True)
    Action = models.CharField(max_length=10, choices=ChoicesMain.MSG_LOG_ACTION)
    Delete = models.BooleanField(default=False)
    DateCreate = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    DateModify = models.DateTimeField(auto_now=True, null=True, blank=True)
    UserCreateId = models.IntegerField(null=True, blank=True)
    UserModifyId = models.IntegerField(null=True, blank=True)
    objects = DeleteManager()
    objects_del = models.Manager()
    def __unicode__(self):
        return str(self.MessageId)
    class Meta:
        db_table = 'MG_MSG_LOG'
        verbose_name_plural = "MessagesLog"

class Discussion(models.Model):
    """Discussion Model
    FK: UserPosting
    MN: UsersParticipate
    MN: Files
    MN: Tags
    MN: Links
    MN: Like
    MN: Share
    Topic"""
    UserPosting = models.ForeignKey('social_network.UserX', related_name='discuss_user_post')
    UsersParticipate = models.ManyToManyField('social_network.UserX', null=True, blank=True, related_name='discusss_user_participate')
    Topic = models.TextField()
    Files = models.ManyToManyField('social_network.File', null=True, blank=True)
    Tags = models.ManyToManyField('social_network.Tag', null=True, blank=True)
    Like = models.ManyToManyField('social_network.Like', null=True, blank=True)
    Links = models.ManyToManyField('social_network.Link', null=True, blank=True)
    Share = models.ManyToManyField('social_network.StatusShare', null=True, blank=True)
    Threads = models.ManyToManyField('DiscussionThread', null=True, blank=True)
    Delete = models.BooleanField(default=False)
    DateCreate = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    DateModify = models.DateTimeField(auto_now=True, null=True, blank=True)
    UserCreateId = models.IntegerField(null=True, blank=True)
    UserModifyId = models.IntegerField(null=True, blank=True)
    objects = DeleteManager()
    objects_del = models.Manager()
    def __unicode__(self):
        return str(self.id) + ' ' + str(self.UserPosting)
    class Meta:
        db_table = 'MG_DISCUSSION'
        verbose_name_plural = "Discussions"

class DiscussionThread(models.Model):
    """Discussion Thread Model: Usefull for problems and solutions, brainstorming, discussions, etc...
    FK: User
    FK: Discussion
    MN: Files
    MN: Comments
    MN: Tags
    MN: Like
    MN: Links
    MN: Share
    Thread
    Content"""
    User = models.ForeignKey('social_network.UserX')
    Thread = models.CharField(max_length=140)
    Files = models.ManyToManyField('social_network.File', null=True, blank=True)
    Content = models.TextField(null=True, blank=True)
    Comments = models.ManyToManyField('social_network.Comment', null=True, blank=True)
    Tags = models.ManyToManyField('social_network.Tag', null=True, blank=True)
    Like = models.ManyToManyField('social_network.Like', null=True, blank=True)
    Links = models.ManyToManyField('social_network.Link', null=True, blank=True)
    Share = models.ManyToManyField('social_network.StatusShare', null=True, blank=True)
    Delete = models.BooleanField(default=False)
    DateCreate = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    DateModify = models.DateTimeField(auto_now=True, null=True, blank=True)
    UserCreateId = models.IntegerField(null=True, blank=True)
    UserModifyId = models.IntegerField(null=True, blank=True)
    objects = DeleteManager()
    objects_del = models.Manager()
    def __unicode__(self):
        return str(self.id)
    class Meta:
        db_table = 'MG_DISCUSSION_THREAD'
        verbose_name_plural = "DiscussionThreads"
