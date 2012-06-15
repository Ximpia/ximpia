import types
import traceback

from django.db import models
from django.contrib.auth.models import User as UserSys, Group as GroupSys
from django.utils.translation import ugettext as _
from ximpia import settings
from django.utils import translation
from choices import Choices
from constants import Constants as K
from ximpia.core.models import BaseModel

class Media(BaseModel):
	"""Media"""
	embedCode = models.CharField(max_length=500,
			verbose_name = _('Embed Code'), help_text = _('Embed code from Video provider'))
	name = models.CharField(max_length=30,
			verbose_name = _('Name'), help_text = _('Media name'))
	title = models.CharField(max_length=50,
			verbose_name = _('Title'), help_text = _('Media Title'))
	description = models.CharField(max_length=500,
			verbose_name = _('Description'), help_text = _('Media Description, shown in search'))
	isFeatured = models.BooleanField(default=False,
			verbose_name = _('Is Featured?'), help_text = _('Is media shown as featured? Will be placed first on search and bigger'))
	def __unicode__(self):
		return str(self.name)
	class Meta:
		db_table = 'SITE_MEDIA'
		verbose_name = _('Media')
		verbose_name_plural = _('Media')
		ordering = ['-isFeatured']
