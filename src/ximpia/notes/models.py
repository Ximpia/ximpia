from django.db import models
from django.utils.translation import ugettext as _

# Create your models here.

class DeleteManager(models.Manager):
    def get_query_set(self):
        return super(DeleteManager, self).get_query_set().filter(Delete=False)

class Note(models.Model):
    """Notes."""
    Owner = models.ForeignKey('social_network.UserX', related_name='note_owner')
    Editors = models.ManyToManyField('social_network.UserX', related_name='note_editors')
    Title = models.CharField(max_length=75)
    Content = models.TextField()
    Comments = models.ManyToManyField('social_network.Comment', null=True, blank=True)
    Like = models.ManyToManyField('social_network.Like', null=True, blank=True)
    Tags = models.ManyToManyField('social_network.Tag', null=True, blank=True)
    Links = models.ManyToManyField('social_network.Link', null=True, blank=True)
    Delete = models.BooleanField(default=False)
    DateCreate = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    DateModify = models.DateTimeField(auto_now=True, null=True, blank=True)
    UserCreateId = models.IntegerField(null=True, blank=True)
    UserModifyId = models.IntegerField(null=True, blank=True)
    objects = DeleteManager()
    objects_del = models.Manager()
    def __unicode__(self):
        return str(self.Title)
    class Meta:
        db_table = 'NO_NOTE'
        verbose_name_plural = "Notes"
