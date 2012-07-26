from django.utils.translation import ugettext as _

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
ERR_changePassword = _('Invalid data to change password')
ERR_invitationUsed = _('This invitation has already been used')

ERR_passwordValidate = _('The password is not correct')
