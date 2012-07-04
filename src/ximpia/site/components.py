from ximpia.core.business import ComponentRegister
from ximpia.core.choices import Choices as _Ch
from ximpia.core.constants import CoreConstants as _K

from constants import Constants as K
import business

##########
# Application
##########
ComponentRegister.registerApp(code=K.APP, name='Site')

##########
# Views
##########
# login
ComponentRegister.registerView(appCode=K.APP, viewName='home', myClass=business.VideoBusiness, method='showHome')

##########
# Actions
##########


###############
# Menu
###############
ComponentRegister.cleanMenu(K.APP)
ComponentRegister.registerMenu(appCode=K.APP, name='siteHome', titleShort='Home', title='Home', iconName='iconHome', viewName='home')

###############
# View Menus
###############
ComponentRegister.registerViewMenu(appCode=K.APP, viewName='home', menus=[
				{_K.ZONE: 'main', _K.MENU_NAME: 'siteHome'}
			])

#############
# Templates
#############
ComponentRegister.registerTemplate(appCode=K.APP, viewName='home', name='home', winType=_Ch.WIN_TYPE_WINDOW)


##########
# Flows
##########

##########
# Search
##########
