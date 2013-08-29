
Example
=======

I will show how easy is to develop apps in Ximpia.

Here goes the example for a change password popup. When user clicks on menu icon, a change password popup 
shows with current password and new password. The popup has button send to send new password to server.

First you start by defining your visual components and creating template `xp_templates/popup/changePassword.html` in site application:

.. code-block:: html

	<div id="id_password_comp" data-xp-type="basic.text" 
		data-xp="{type: 'password', info: true}" ></div><br />
	<div id="id_newPassword_comp" data-xp-type="basic.text" 
		data-xp="{type: 'password', info: true}" ></div><br />
	<div id="id_newPasswordConfirm_comp" data-xp-type="basic.text" 
		data-xp="{type: 'password', info: true}" ></div>

I use the visual component `basic.text` for the input fields. Then we create the form with fields::

	class UserChangePasswordForm( XBaseForm ):
		_XP_FORM_ID = 'userChangePassword'
		_dbUser = User()
		newPassword = XpPasswordField(_dbUser, '_dbUser.password', minValue=6, label='New Password', help_text = _('Your New Password'))
		newPasswordConfirm = XpPasswordField(_dbUser, '_dbUser.password', minValue=6, label='Confirm Password', 
						help_text = _('Write again your password'))
		password = XpPasswordField(_dbUser, '_dbUser.password', minValue=6, label='Password', help_text = _('Current password'))
		errorMessages = forms.CharField(widget=XpHiddenWidget, initial=_jsf.buildMsgArray([_m, ['ERR_wrongPassword']]))
		okMessages = forms.CharField(widget=XpHiddenWidget, initial=_jsf.buildMsgArray([_m, []]))
		def clean(self):
			'Clean form'
			self._validateSameFields([('newPassword','newPasswordConfirm')])
			self._xpClean()
			return self.cleaned_data


The form has cross validation for new password and the confirmation of new password.

Then implement the view inside business class `UserBusiness`:

```
@DoBusinessDecorator(form = forms.UserChangePasswordForm, pageError=True)
def showChangePassword(self):
	"""Change password form with current password and new password"""
	pass
```

We include `pageError=True` because we want error message to show in a bar above the button and no popup with error messages.

Register view and template:

```
ComponentRegister.registerView(appCode=K.APP, viewName='changePassword', myClass=business.UserBusiness, method='showChangePassword', winType=_Ch.WIN_TYPE_POPUP)
ComponentRegister.registerTemplate(appCode=K.APP, viewName='changePassword', name='changePassword', winType=_Ch.WIN_TYPE_POPUP)
```

Implement action to change password:

```
@ValidationDecorator()
def _validateUser(self):
	'Validate user: Check user password'
	self._ctx[Ctx.USER] = self._authenticateUser(self._ctx[Ctx.USER], self._f()['password'], 'password', _m.ERR_wrongPassword)
@ValidateFormDecorator(forms.UserChangePasswordForm)
@DoBusinessDecorator(pageError=True)
def doChangePassword(self):
	'Change password from user area'
	self._validateUser()
	user = self._dbUserSys.get(username= self._ctx[Ctx.USER])
	user.set_password(self._f()['newPassword'])
	user.save()
```

Register action:

```
ComponentRegister.registerAction(appCode=K.APP, actionName='doChangePassword', myClass=business.UserBusiness, method='doChangePassword')
```

Finally you link the view in the menu system to show in a popup bellow the logo:

```
ComponentRegister.registerMenu(appCode=K.APP, name='changePassword', titleShort='New Password', title='Change Password', iconName='', viewName='changePassword')
ComponentRegister.registerViewMenu(appCode=K.APP, viewName='homeLogin', menus=[
				{_K.ZONE: _Ch.MENU_ZONE_SYS, _K.GROUP: 'sys', _K.MENU_NAME: 'changePassword'},
			])
```
