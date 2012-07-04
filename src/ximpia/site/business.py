import forms
import data

from ximpia.core.business import CommonBusiness
from ximpia.core.business import DoBusinessDecorator

class VideoBusiness ( CommonBusiness ):
	
	def __init__(self, ctx):
		super(VideoBusiness, self).__init__(ctx)
		self._dbVideo = data.VideoDAO(ctx)
	
	@DoBusinessDecorator(form = forms.HomeForm, pageError=True, isServerTmpl=True)
	def showHome(self):
		"""Show videos in the home view"""
		self._addList('featuredVideos', self._dbVideo.searchFields( 	['embedCode', 'name', 'title', 'description', 'isFeatured'], 
										isFeatured=True  ) )
		self._addList('videos', self._dbVideo.searchFields( 	['embedCode', 'name', 'title', 'description', 'isFeatured'], 
									isFeatured=False  ) )
