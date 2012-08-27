from ximpia_core.core.models import ContextViewDecorator
from ximpia_core.core.business import ViewDecorator

import business

@ContextViewDecorator()
@ViewDecorator()
def home(request, **args):
	print 'home....'
	video = business.VideoBusiness(args['ctx'])
	result = video.showHome()
	return result
