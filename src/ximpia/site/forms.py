import re
import json
import types

from django.core import serializers as _s
from django import forms
from django.forms import ValidationError
from django.utils.translation import ugettext as _

from choices import Choices

from ximpia import settings

import messages as _m

from ximpia.settings_visual import SocialNetworkIconData as SocialNetwork
from ximpia.settings_visual import SuggestBox, GenericComponent

#from yacaptcha.models import Captcha

from django.contrib.auth.models import User, Group
#from ximpia.core.models import getResultOK, getResultERROR

from ximpia.core.form_fields import XpMultiField, XpCharField, XpEmailField, XpPasswordField, XpSocialIconField, XpChoiceField, XpTextChoiceField
from ximpia.core.form_fields import XpChoiceTextField, XpUserField
from ximpia.core.form_widgets import XpHiddenWidget, XpPasswordWidget, XpSelectWidget, XpTextareaWidget, XpTextInputWidget, XpMultipleWidget
from ximpia.core.form_fields import XpHiddenDataField

from ximpia.util.js import Form as _jsf

from ximpia.core.validators import validateCaptcha
from ximpia.core.models import UserSocial
from ximpia.core.form_fields import XpHiddenField
from ximpia.core.forms import XBaseForm, AppRegex

class HomeForm(XBaseForm):
	_XP_FORM_ID = 'home'
	errorMessages = forms.CharField(widget=XpHiddenWidget, initial=_jsf.buildMsgArray([_m, []]))
	okMessages = forms.CharField(widget=XpHiddenWidget, initial=_jsf.buildMsgArray([_m, []]))
