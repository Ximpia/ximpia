import random
import forms
import simplejson as json
import data
from datetime import date, timedelta

from ximpia.core.models import ContextDecorator as Ctx
from ximpia.core.business import CommonBusiness, EmailBusiness
from ximpia.core.business import ValidateFormDecorator, WFActionDecorator, DoBusinessDecorator, WFViewDecorator, MenuActionDecorator,\
	ValidationDecorator
from ximpia import settings

import constants as K
import forms

class HomeBusiness ( CommonBusiness ):
	
	def __init__(self, ctx):
		super(HomeBusiness, self).__init__(ctx)
	
	@DoBusinessDecorator(form = forms.HomeForm, pageError=True, isServerTmpl=True)
	def showHome(self):
		"""Show home view for test application"""
		pass
