import random
import simplejson as json
import base64
import cPickle

from django.db.models import Q
from django.contrib.auth.models import User as UserSys, Group as GroupSys

from django.utils.translation import ugettext as _
from ximpia import util

import sys

from ximpia.settings_visual import SocialNetworkIconData as SND

from models import Note

from ximpia.social_network.data import CommonDAO

class NoteDAO(CommonDAO):
	
	_model = None
	
	def __init__(self, ctx, *ArgsTuple, **ArgsDict):
		super(NoteDAO, self).__init__(ctx, *ArgsTuple, **ArgsDict)
		self._model = Note

