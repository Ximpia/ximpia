# coding: utf-8

from django.utils.translation import ugettext as _

# Messages
OK_USER_SIGNUP = _('Your signup has been received, check your email')
OK_SOCIAL_SIGNUP = _('Thanks! Signup complete. You can now login')
OK_PASSWORD_REMINDER = _('OK!. We sent you an email to reset password')
OK_PASSWORD_CHANGE = _('OK! Password changed')

# Errors
ERR_ximpia_id = _('An user with same ximpiaId already exists. Please choose another id for your ximpia account')
ERR_ximpia_id_not_exist = _('User does not exist')
ERR_email = _('An user with same email address already exists. Please select another email')
ERR_wrong_password = _('The user or password is not correct')
ERR_email_does_not_exist = _('The email address does not exist')
ERR_change_password = _('Invalid data to change password')
ERR_social_id_exists = _('The social network user already exists at Ximpia')
ERR_invitation_not_valid = _('Invitation code is not valid')
