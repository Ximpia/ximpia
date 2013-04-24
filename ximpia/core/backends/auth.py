import os

# Import models
from django.contrib.auth.models import User
from ximpia.site.models import SocialNetworkUser

# Settings
from ximpia.core.util import get_class
settings = get_class(os.getenv("DJANGO_SETTINGS_MODULE"))

# Logging
import logging.config
logging.config.dictConfig(settings.LOGGING)
logger = logging.getLogger(__name__)

class SocialNetBackend(object):
	
	def authenticate(self, socialId=None, socialToken=None):
		# we get the social information for socialId
		try:
			social = SocialNetworkUser.objects.get(socialId=socialId)
			logger.debug('SocialNetBackend.authenticate :: Social network user: %s' % (social) )
			# TODO: We must call facebook with socialId, socialToken and authenticate user for ximpia app
			"""if social.token == socialToken:
				logger.debug('SocialNetBackend.authenticate :: social token match!!!')
				return social.user
			else:
				logger.debug('SocialNetBackend.authenticate :: social tokens do not match!!!')
				return None"""
			return social.user
		except SocialNetworkUser.DoesNotExist:
			logger.debug('SocialNetBackend.authenticate :: Cannot find user with socialId:%s' % (socialId) )
			return None
	
	def get_user(self, user_id):
		try:
			return User.objects.get(pk=user_id)
		except User.DoesNotExist:
			return None
