from ximpia_core.core.business import ComponentRegister
from ximpia_core.core.choices import Choices as _Ch
import ximpia_core.core.constants as _K
import constants as K
import business

#################################################
# Parameters used in Menu, Views and Workflow
#################################################

##########
# Application
##########
ComponentRegister.registerApp(code=K.APP, name='Test Application')


##########
# Views
##########
ComponentRegister.registerView(appCode=K.APP, viewName='home', myClass=business.HomeBusiness, method='showHome')

##########
# Actions
##########


###############
# Menu
###############
# Ximpia Menu
ComponentRegister.cleanMenu(K.APP)
# Home Menu
ComponentRegister.registerMenu(appCode=K.APP, name='home', titleShort='Home', title='Home', iconName='iconHome', viewName='home')

###############
# View Menus
###############
ComponentRegister.registerViewMenu(appCode=K.APP, viewName='home', menus=[
				{_K.ZONE: 'main', _K.MENU_NAME: 'home'}
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
