# coding: utf-8

import os

from ximpia.xpcore.models import context_view
from ximpia.xpcore.service import view

# Settings
from ximpia.xpcore.util import get_class
settings = get_class(os.getenv("DJANGO_SETTINGS_MODULE"))

# Logging
import logging.config
logging.config.dictConfig(settings.LOGGING)
logger = logging.getLogger(__name__)

@context_view()
@view()
def home(request, **args):
    logger.debug( 'home....' )
    result = None
    return result
