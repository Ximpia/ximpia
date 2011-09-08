from django.db import models
from django.utils.translation import ugettext as _

# Create your models here.

class Choices(object):
    # TASK_FINISH_TYPE
    TASK_FINISH_TYPE_DEFAULT = 'all'
    TASK_FINISH_TYPE = (
        ('all', _('All')),
        ('any', _('Any')),
            )
    # TASK_STATUS
    TASK_STATUS_DEFAULT = 'notStarted'
    TASK_STATUS = (
        ('notStarted', _('Not Started')),
        ('inProgress', _('In Progress')),
        ('completed', _('Completed')),
        ('waiting', _('Waiting')),
        ('deferred', _('Deferred')),
        )

class DeleteManager(models.Manager):
    def get_query_set(self):
        return super(DeleteManager, self).get_query_set().filter(Delete=False)

class TaskList(models.Model):
    """Tasks grouped in task lists or procedures"""
    owner = models.ForeignKey('social_network.UserX')
    name = models.CharField(max_length=75)
    tasks = models.ManyToManyField('Task')
    comments = models.ManyToManyField('social_network.Comment', null=True, blank=True)
    tags = models.ManyToManyField('social_network.Tag', null=True, blank=True)
    files = models.ManyToManyField('social_network.File', null=True, blank=True)
    links = models.ManyToManyField('social_network.Link', null=True, blank=True)
    public = models.BooleanField(default=True)
    delete = models.BooleanField(default=False)
    dateCreate = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    dateModify = models.DateTimeField(auto_now=True, null=True, blank=True)
    userCreateId = models.IntegerField(null=True, blank=True)
    userModifyId = models.IntegerField(null=True, blank=True)
    objects = DeleteManager()
    objects_del = models.Manager()
    def __unicode__(self):
        return str(self.name)
    class Meta:
        db_table = 'TK_TASK_LIST'

class Task(models.Model):
    """Doc."""
    owner = models.ForeignKey('social_network.UserX')
    name = models.CharField(max_length=75)
    notes = models.TextField()
    comments = models.ManyToManyField('social_network.Comment', null=True, blank=True)
    tags = models.ManyToManyField('social_network.Tag', null=True, blank=True)
    delete = models.BooleanField(default=False)
    dateCreate = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    dateModify = models.DateTimeField(auto_now=True, null=True, blank=True)
    userCreateId = models.IntegerField(null=True, blank=True)
    userModifyId = models.IntegerField(null=True, blank=True)
    objects = DeleteManager()
    objects_del = models.Manager()
    def __unicode__(self):
        return str(self.name)
    class Meta:
        db_table = 'TK_TASK'
        
class TaskDetail(models.Model):
    """Information about assignments and dates"""
    task = models.ForeignKey(Task)
    finishType = models.CharField(max_length=15, choices=Choices.TASK_FINISH_TYPE, default=Choices.TASK_FINISH_TYPE_DEFAULT)
    status = models.CharField(max_length=15, choices=Choices.TASK_STATUS, default=Choices.TASK_STATUS_DEFAULT)
    assignedTo = models.ManyToManyField('social_network.UserX', through='TaskAssign', related_name='task_detail_assigned')
    timeDateStart = models.DateTimeField()
    timeDateEnd = models.DateTimeField(null=True, blank=True)
    delete = models.BooleanField(default=False)
    dateCreate = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    dateModify = models.DateTimeField(auto_now=True, null=True, blank=True)
    userCreateId = models.IntegerField(null=True, blank=True)
    userModifyId = models.IntegerField(null=True, blank=True)
    objects = DeleteManager()
    objects_del = models.Manager()
    def __unicode__(self):
        return str(self.task)
    class Meta:
        db_table = 'TK_TASK_DETAIL'

class TaskAssign(models.Model):
    """Task assignments"""
    taskDetail = models.ForeignKey('TaskDetail')
    user = models.ForeignKey('social_network.UserX')
    status = models.CharField(max_length=15, choices=Choices.TASK_STATUS, default=Choices.TASK_STATUS_DEFAULT)
    delete = models.BooleanField(default=False)
    dateCreate = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    dateModify = models.DateTimeField(auto_now=True, null=True, blank=True)
    userCreateId = models.IntegerField(null=True, blank=True)
    userModifyId = models.IntegerField(null=True, blank=True)
    objects = DeleteManager()
    objects_del = models.Manager()
    def __unicode__(self):
        return str(self.TaskDetail) + ' ' + str(self.User)
    class Meta:
        db_table = 'TK_TASK_DETAIL_assign'
