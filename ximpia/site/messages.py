# coding: utf-8

from django.utils.translation import ugettext as _

# Messages
OK_USER_SIGNUP = _('Your signup has been received, check your email')
OK_SOCIAL_SIGNUP = _('Thanks! Signup complete. You can now login')
OK_PASSWORD_REMINDER = _('OK!. We sent you an email to reset password')
OK_PASSWORD_CHANGE = _('OK! Password changed')

# Errors
ERR_ximpiaId = _('An user with same ximpiaId already exists. Please choose another id for your ximpia account')
ERR_ximpiaId_notExist = _('User does not exist')
ERR_email = _('An user with same email address already exists. Please select another email')
ERR_wrongPassword = _('The user or password is not correct')
ERR_emailDoesNotExist = _('The email address does not exist')
ERR_changePassword = _('Invalid data to change password')
ERR_socialIdExists = _('The social network user already exists at Ximpia')
ERR_invitationNotValid = _('Invitation code is not valid')
