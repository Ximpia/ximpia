import random
import simplejson as json
import base64
import cPickle
import traceback

from django.db.models import Q
from django.contrib.auth.models import User as UserSys, Group as GroupSys

from django.utils.translation import ugettext as _
from ximpia import util

from constants import Constants as K
from choices import Choices

from models import Video

from ximpia.core.models import parseText, XpMsgException, getDataDict, getFormDataValue, getPagingStartEnd, parseLinks, CoreParam, UserSocial
from ximpia.core.data import CommonDAO, CoreParameterDAO, ApplicationDAO
import sys

from ximpia.settings_visual import SocialNetworkIconData as SND
from ximpia.settings_visual import GenericComponent
from ximpia.core.constants import CoreKParam

class VideoDAO(CommonDAO):
	def __init__(self, ctx, *ArgsTuple, **ArgsDict):
		super(VideoDAO, self).__init__(ctx, *ArgsTuple, **ArgsDict)
		self._model = Video
