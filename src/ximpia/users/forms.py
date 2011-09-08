import re

from django import forms
from models import Constants, Choices
from ximpia.human_resources.models import Choices as ChoicesHR

class AppWidgets(object):
	"""Doc."""
	TextInput = forms.TextInput(attrs={'class':''})
	TextArea = forms.Textarea(attrs={'class':''})
	Password = forms.PasswordInput(render_value=False)
	SelectMulti = forms.SelectMultiple(attrs={'class': ''})
	Select = forms.Select(attrs={'class': ''})
	Hidden = forms.HiddenInput()
	HiddenMuti = forms.MultipleHiddenInput(attrs={'class':''})

class AppRegex(object):
	"""Doc."""
	Str = re.compile('\w+', re.L)
	TxtFld = re.compile("^(\w*)\s?(\s?\w+)*$", re.L)
	Currency = re.compile('^[0-9]*\.?|\,?[0-9]{0,2}$')
	Id = re.compile('^[1-9]+[0-9]*$')
	UserId = re.compile('^[a-zA-Z0-9_.]+')
	Password = re.compile('^\w+')

class FrmCommon(forms.Form):
	"""Doc."""
	def __init__(self, *args, **kwargs): 
		"""Doc."""
		super(FrmCommon, self).__init__(*args, **kwargs)
	def validateSameFields(self, fieldName1, fieldName2):
		"""Doc."""
		fieldLabel1 = self.fields[fieldName1].label
		fieldLabel2 = self.fields[fieldName2].label
		fieldData1 = self.data[fieldName1]
		fieldData2 = self.data[fieldName2]		
		checkSame = False
		if fieldData1 == fieldData2:
			checkSame = True
		checkBasic = self.is_valid()
		check = False
		if checkBasic== True and checkSame == True:
			check = True
		else:
			if checkSame == False:
				self.errors['invalid'] = ' password. ' + fieldLabel1 + ' must be the same as ' + fieldLabel2
		return check
	def cleaned_data(self, data):
		value = super(FrmCommon, self).cleaned_data(data)
		return value

# Labels
LB_XIMPIA_ID = 'Ximpia Id'
LB_EMAIL = 'Email'
LB_FIRST_NAME = 'First Name'
LB_LAST_NAME = 'Last Name'
LB_PASSWORD = 'Password'
LB_PASSWORD_VERIFY = 'Password Verify'
LB_INDUSTRY = 'Industry'
LB_ORG_NAME = 'Organization Name'
LB_DOMAIN = 'Domain'
LB_ACCOUNT = 'Account'
LB_DESCRIPTION = 'Description'
LB_USER_GROUP = 'User Group'
LB_CITY = 'City'
LB_COUNTRY = 'Country'
LB_ORG_NAME = 'Organization Name'
LB_DOMAIN = 'Domain'
LB_ACCOUNT = 'Account'
LB_DESCRIPTION = 'Description'
LB_USER_GROUP = 'User Group'
LB_TAGS = 'Tags'
LB_JOB = 'Job'

# Help Texts
HT_XIMPIA_ID = 'Valid characters are letters, numbers, underscores (_) and period (.)'
HT_PASSWORD_VERIFY = 'Write again you password to verify'
HT_INDUSTRY = 'Tell us about your field of professional interest'
HT_TAGS = 'Describe this section using dynamic tags'


class FrmUserSignup(FrmCommon):
	ximpiaId = forms.RegexField(max_length=20, regex=AppRegex.UserId, widget=AppWidgets.TextInput, label=LB_XIMPIA_ID, help_text=HT_XIMPIA_ID)
	email = forms.EmailField(max_length=50, widget=AppWidgets.TextInput, required=False, label=LB_EMAIL)
	firstName = forms.RegexField(max_length=30, regex=AppRegex.TxtFld, widget=AppWidgets.TextInput, label=LB_FIRST_NAME)
	lastName = forms.RegexField(max_length=30, regex=AppRegex.TxtFld, widget=AppWidgets.TextInput, required=False, label=LB_LAST_NAME)
	password = forms.RegexField(max_length=10, min_length=6, regex=AppRegex.Password, widget=AppWidgets.Password, required=False, initial='', label=LB_PASSWORD, help_text='')
	passwordVerify = forms.RegexField(max_length=10, min_length=6, regex=AppRegex.Password, widget=AppWidgets.Password, required=False, initial='', label=LB_PASSWORD_VERIFY, help_text=HT_PASSWORD_VERIFY)
	industry = forms.MultipleChoiceField(choices=ChoicesHR.INDUSTRY, widget=AppWidgets.SelectMulti, label=LB_INDUSTRY, help_text=HT_INDUSTRY)
	city = forms.RegexField(max_length=20, regex=AppRegex.TxtFld, widget=AppWidgets.TextInput, label=LB_CITY)
	country = forms.ChoiceField(choices=Choices.COUNTRY, widget=AppWidgets.Select, label=LB_COUNTRY)
	twitter = forms.CharField(widget=AppWidgets.Hidden, required=False)
	twitterPass = forms.CharField(widget=AppWidgets.Hidden, required=False)
	facebook = forms.CharField(widget=AppWidgets.Hidden, required=False)
	facebookPass = forms.CharField(widget=AppWidgets.Hidden, required=False)
	linkedIn = forms.CharField(widget=AppWidgets.Hidden, required=False)
	linkedInPass = forms.CharField(widget=AppWidgets.Hidden, required=False)
	userGroups = forms.CharField(widget=AppWidgets.HiddenMuti)
	def isValid(self):
		check = self.validateSameFields('password','passwordVerify')
		return check

class FrmOrganizationSignup(FrmCommon):
	ximpiaId = forms.RegexField(max_length=20, regex=AppRegex.UserId, widget=AppWidgets.TextInput, label=LB_XIMPIA_ID, help_text=HT_XIMPIA_ID)
	email = forms.EmailField(max_length=50, widget=AppWidgets.TextInput, required=False, label=LB_EMAIL)
	firstName = forms.RegexField(max_length=30, regex=AppRegex.TxtFld, widget=AppWidgets.TextInput, label=LB_FIRST_NAME)
	lastName = forms.RegexField(max_length=30, regex=AppRegex.TxtFld, widget=AppWidgets.TextInput, required=False, label=LB_LAST_NAME)
	password = forms.RegexField(max_length=10, min_length=6, regex=AppRegex.Password, widget=AppWidgets.Password, required=False, initial='', label=LB_PASSWORD, help_text='')
	passwordVerify = forms.RegexField(max_length=10, min_length=6, regex=AppRegex.Password, widget=AppWidgets.Password, required=False, initial='', label=LB_PASSWORD_VERIFY, help_text=HT_PASSWORD_VERIFY)
	industry = forms.MultipleChoiceField(choices=ChoicesHR.INDUSTRY, widget=AppWidgets.SelectMulti, label=LB_INDUSTRY, help_text=HT_INDUSTRY)
	city = forms.RegexField(max_length=20, regex=AppRegex.TxtFld, widget=AppWidgets.TextInput, label=LB_CITY)
	country = forms.ChoiceField(choices=Choices.COUNTRY, widget=AppWidgets.Select, label=LB_COUNTRY)
	organizationName = forms.RegexField(max_length=30, regex=AppRegex.TxtFld, widget=AppWidgets.TextInput, label=LB_ORG_NAME, help_text='')
	organizationdomain = forms.RegexField(max_length=50, regex=AppRegex.TxtFld, widget=AppWidgets.TextInput, label=LB_DOMAIN, help_text='')
	organizationCity = forms.RegexField(max_length=20, regex=AppRegex.TxtFld, widget=AppWidgets.TextInput, label=LB_CITY)
	organizationCountry = forms.ChoiceField(choices=Choices.COUNTRY, widget=AppWidgets.Select, label=LB_COUNTRY)
	account = forms.RegexField(max_length=20, regex=AppRegex.TxtFld, widget=AppWidgets.TextInput, label=LB_ACCOUNT, help_text='')
	description = forms.RegexField(max_length=500, regex=AppRegex.Str, widget=AppWidgets.TextArea, label=LB_DESCRIPTION, help_text='')
	organizationGroup = forms.RegexField(max_length=20, regex=AppRegex.TxtFld, widget=AppWidgets.TextInput, label=LB_USER_GROUP, help_text='')
	organizationGroupTags = forms.RegexField(max_length=15, regex=AppRegex.TxtFld, widget=AppWidgets.TextInput, label=LB_TAGS, help_text=HT_TAGS)
	organizationTwitter = forms.CharField(widget=AppWidgets.Hidden, required=False)
	organizationTwitterPass = forms.CharField(widget=AppWidgets.Hidden, required=False)
	jobTitle = forms.RegexField(max_length=50, regex=AppRegex.TxtFld, widget=AppWidgets.TextInput, label=LB_JOB)
	twitter = forms.CharField(widget=AppWidgets.Hidden, required=False)
	twitterPass = forms.CharField(widget=AppWidgets.Hidden, required=False)
	facebook = forms.CharField(widget=AppWidgets.Hidden, required=False)
	facebookPass = forms.CharField(widget=AppWidgets.Hidden, required=False)
	linkedIn = forms.CharField(widget=AppWidgets.Hidden, required=False)
	linkedInPass = forms.CharField(widget=AppWidgets.Hidden, required=False)
	userGroups = forms.CharField(widget=AppWidgets.HiddenMuti)
	def isValid(self):
		check = self.validateSameFields('password','passwordVerify')
		return check 
