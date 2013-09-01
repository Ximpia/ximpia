
Example
=======

Here goes the example for a change password popup. When user clicks on menu icon, a change password popup 
shows with current password and new password. The popup has button send to send new password to server.

Model
-----

Since change password uses django User model, you have no changes in model for this example

Visual Components
-----------------

Define components in template ``myproject/myapp/templates/xpsite/popup/change_password.html``:

.. code-block:: html

	<div id="id_changePassword">
	<form id="form_userChangePassword" action="" method="post" data-xp="{}">
	<!-- ximpiaId -->
	<div id="id_username_comp" 
			data-xp-type="field" 
			data-xp="{tabindex: '1', label: 'XimpiaId', 'readonly': 'readonly'}" >
	</div>
	<!-- password -->
	<div id="id_password_comp" data-xp-type="field"  style="margin-top: 10px"
			data-xp="{type: 'password', info: true}" >
	</div>
	<!-- newPassword -->
	<div id="id_newPassword_comp" data-xp-type="field" style="margin-top: 10px" 
			data-xp="{type: 'password', info: true, class: 'passwordStrength'}" >
	</div>
	<!-- newPasswordConfirm -->
	<div id="id_newPasswordConfirm_comp" data-xp-type="field" style="margin-top: 10px"
			data-xp="{type: 'password', info: true}" >
	</div>
	</form>
	</div>

All components are ``field`` type. You include attributes in ``data-`` html5 attrs. 

Form would need to have ``_XP_FORM_ID`` equal to ``changePassword``, the id for the ``div`` element.

Form
----

.. code-block:: python

	class ChangePasswordForm(XBaseForm):
		_XP_FORM_ID = 'changePassword'
		_dbUser = User()
		username = UserField(_dbUser, 'username', label='Username')
		newPassword = PasswordField(_dbUser, 'password', minLength=6, 
			label='Password', helpText = _('Your New Password'))
		newPasswordConfirm = PasswordField(_dbUser, 'password', minLength=6, 
			label='Confirm Password', 
			helpText = _('Write again your password to make sure there are no errors'))
		errorMessages = HiddenField(initial=_jsf.buildMsgArray([_m, ['ERR_change_password']]))
		okMessages = HiddenField(initial=_jsf.buildMsgArray([_m, ['OK_PASSWORD_CHANGE']]))
		def clean(self):
			"""Clean form"""
			self._validate_same_fields([('newPassword','newPasswordConfirm')])
			self._xp_clean()
			return self.cleaned_data

The form has cross validation for new password and confirmation for password. Template must reference ``_XP_FORM_ID``.

Next step would be implement view for popup.

View
----

.. code-block:: python

	@view(forms.UserChangePasswordForm)
	def view_change_password(self):
		"""Change password form with current password and new password
		"""
		self._put_form_value('username', self._ctx.user.username)


We need to insert user from context. In this case we have no database value since we have user
in context. Otherwise, we would not need to call ``_put_form_value`` and method would only have
``pass`` command.

For database fields cases, form would populate your field data from database without need to code
inside view.

Action
------

Code to run when Save button is clicked by user:

.. code-block:: python

	@validation()
	def _validate_user(self):
		"""Validate user: Check user password"""
		self._ctx.user = self._authenticate_user(self._ctx.user, 
			self._f()['password'], 'password', _m.ERR_wrong_password)

	@action(forms.UserChangePasswordForm)
	def change_password(self):
		"""Change password from user area
		"""
		self._dbUser = self._instances(UserDAO)[0]
		self._validate_user()
		user = self._dbUser.get(username= self._ctx.user)
		user.set_password(self._f()['newPassword'])
		user.save()

1. Get user data instance with context inyected
2. Validate user: Will show message ``ERR_wrong_password`` in case user does not authenticate.
3. Call ``set_password``django method with new password and save changes

Registering
-----------

.. code-block:: python

	# view
	self._reg.registerView(__name__, serviceName='Users', viewName='changePassword', 
		slug='change-password', className=SiteService, method='view_change_password', 
		hasAuth=True, winType='popup')
	# template
	self._reg.registerTemplate(__name__, viewName='changePassword', name='changePassword', 
		winType='popup')
	# action
	self._reg.registerAction(__name__, serviceName='Users', actionName='changePassword', 
		slug='change-password', className=SiteService, method='change_password', 
		hasAuth=True)
	# search
	self._reg.registerSearch(__name__, text='Change Password', viewName='changePassword')
