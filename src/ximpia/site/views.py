from ximpia_core.core.models import ContextViewDecorator
from ximpia_core.core.business import ViewDecorator

import business

from ximpia import settings

# Logging
import logging.config
logging.config.dictConfig(settings.LOGGING)
logger = logging.getLogger(__name__)

@ContextViewDecorator()
@ViewDecorator()
def home(request, **args):
	logger.debug( 'home....' )
	video = business.VideoBusiness(args['ctx'])
	result = video.showHome()
	return result
