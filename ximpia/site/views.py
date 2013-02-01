# coding: utf-8

import os

from ximpia.core.models import ContextViewDecorator
from ximpia.core.service import ViewDecorator

# Settings
from ximpia.core.util import getClass
settings = getClass(os.getenv("DJANGO_SETTINGS_MODULE"))

# Logging
import logging.config
logging.config.dictConfig(settings.LOGGING)
logger = logging.getLogger(__name__)

@ContextViewDecorator()
@ViewDecorator()
def home(request, **args):
	logger.debug( 'home....' )
	#video = business.VideoBusiness(args['ctx'])
	#result = video.showHome()
	result = None
	return result
