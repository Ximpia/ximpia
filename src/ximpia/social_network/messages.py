from django.utils.translation import ugettext as _

# Sign up

# Messages
OK_SN_SIGNUP = _('Your signup has been received, check your email')
OK_PASSWORD_REMINDER = _('OK!. We sent you an email to reset password')
OK_PASSWORD_CHANGE = _('OK! Password changed')

# Errors
ERR_invitationCode = _("""Error in validating invitation code. Ximpia is invitation-only, you must have a valid invitation code from another user""")
#ERR_signupValidation = _('Errors validating your signup data. Please check data entered and try again.')
ERR_ximpiaId = _('An user with same ximpiaId already exists. Please choose another id for your ximpia account')
ERR_email = _('An user with same email address already exists. Please select another email')
ERR_captcha = _('Error in validation image. You can reload image to display another image.')
ERR_wrongPassword = _('The user or password is not correct')
ERR_emailDoesNotExist = _('The email address does not exist')


class Labels(object):
	pass

class MsgSignup(object):
	XIMPIA_ID = _("""XimpiaId must be alfanumeric. We also accept characters "_" and "."<br/>Password must be alfanumeric, 
			allowing for characters like $ # ! & %""")
	INVITATION_CODE = _('Ximpia is invitation-only. You must enter a valid<br/>invitation code')
	CAPTCHA = _('Please enter the validation code displayed in the image')
	PASSWORD_VERIFY = _('Please enter your password again to verify it')
	INDUSTRY = _('You can select more than one industry')
	ORGANIZATION_GROUP = _('Enter the department or group you manage in your organization. <br/>Select from list or enter your own group name')
	ORGANIZATION_GROUP_TAGS = _('Separate tags by commas')
	LINKEDIN_PROFILE = _('You must provide the URL of your public LinkedIn profile.<br/>You will not be able to add users until we validate your account<br/>If you link to LinkedIn, we generate automatically your profile URL')
	ORGANIZATION_INDUSTRY = _('You can select more than one industry')
	ACCOUNT = _('Account must be alfanumeric. We also accept characters "_" and "."')
