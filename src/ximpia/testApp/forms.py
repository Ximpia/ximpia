from django import forms
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User

from ximpia.util.js import Form as _jsf
from ximpia.core.form_fields import XpUserField, XpPasswordField, XpEmailField, XpCharField, XpChoiceField, XpHiddenField
from ximpia.core.form_fields import XpHiddenDataField
from ximpia.core.form_widgets import XpHiddenWidget
from ximpia.core.forms import XBaseForm

import messages as _m 
import constants as K
from choices import Choices

class HomeForm(XBaseForm):
	_XP_FORM_ID = 'home'
	errorMessages = forms.CharField(widget=XpHiddenWidget, initial=_jsf.buildMsgArray([_m, []]))
	okMessages = forms.CharField(widget=XpHiddenWidget, initial=_jsf.buildMsgArray([_m, []]))
