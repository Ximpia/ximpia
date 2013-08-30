
============
About Ximpia
============

Overview
--------

Ximpia allows you to model back-end and front-end in an easy way to minimize lines of code for
your application.

On the front-end, you parametrize javascript components in HTML5 and define stylesheets to
customize look and feel.

On the back-end, you define your services (=use cases) with views, actions and app flow and 
other services like search, settings, parameters, already defined so you can speed up
development.

Context
-------

Instead of request and response, this framework uses context which contains session, cookies
and it is shared in all layers: service, business and data. We have full contexts with all
data from front-end like forms, flow, session and cookies and minimized context with common
data for business and data layers. Service layer uses full context and other layers interchange
minimized context.

You can extend our common context to include extended attributes needed for common parts of
your services, useful when you need custom decorators for your applications.

You can write data into context from service and business layers to interchange domain layer 
information like user metadata, user profile information, etc...

Services
--------

Use cases are materialized in the framework as services. Services will hold view methods,
action methods and validation operations.

Think of Apps as collections of services, and services collections of views and operations:

.. code-block:: python

	class SiteService(CommonService):

		@validation()
		def _validate_invitation_pending(self, invitation_code):
			"""
			Validates that invitation is pending
			"""
			setting = self._get_setting(K.SET_SITE_SIGNUP_INVITATION) 
			(K.SET_SITE_SIGNUP_INVITATION, setting.is_checked()) )
			if setting.is_checked():
				self._validate_exists([
						[self._dbInvitation, {'invitationCode': invitation_code, 'status': K.PENDING}, 
								'invitationCode', _m.ERR_invitation_not_valid]
										])

		@view(forms.HomeForm)
		def viewHome(self):
			db_setting = self._instances('ximpia.xpsite.data.SettingDAO')[0]
			# your code...

		@action(forms.HomeForm)
		def activateGroup(self):
			"""Activate group"""
			groups = self._get_list_pk_values('groups')


In case you have use cases with a set of operations, you can choose to materialize those
into a service class or have n services with ``do``operation or similar.

You register services to map them into database and you would write code by extending from ``CommonService`` and have methods
for views, actions, workflow views, etc...(components.py)::

	self._reg.registerService(__name__, serviceName='My Service', className=SiteService)

Views
-----

Views are called from menu items, search or other action components like buttons, links, etc...

They query your database and display information to your users, so framework uses slave databases for them. For example,
they would be list of customers, search customers and customer detail.

Views must all have a form which is defined in the decorator. Forms hold fields as well as window success messages and error 
messages.

In case you need to link views in a flow, you would set views into the workflow. You don't need to write code for this, all flow
logic is kept parametrized into the Workflow. You may write variables into the workflow and then define flows for views and actions
depending on variable data. Your services may write into workflow as well. It is easy to write wizards, use cases that link to other
use cases in a business operational flow.

.. code-block:: python

	@view(forms.HomeForm)
	def viewHome(self):
		db_setting = self._instances('ximpia.xpsite.data.SettingDAO')[0]
		# your code...

We have HomeForm with messages and fields for home view.

You would need to register the view, template, menu items and search for each view. In case you don't map views with menu, you can
skip menu registering::

	self._reg.registerView(__name__, serviceName='Users', viewName='login', slug='login', 
							className=SiteService, method='view_login')
	self._reg.registerTemplate(__name__, viewName='login', name='passwordReminder', winType='popup', 
						alias='password_reminder')
	self._reg.registerSearch(__name__, text='Login', viewName='login')


Forms
-----

Ximpia forms are a bit different from django forms since they keep database fields inyected into fields.

.. code-block:: python

	class LoginForm(XBaseForm):
		_XP_FORM_ID = 'login' 
		_dbUser = User()
		username = UserField(_dbUser, 'username', label='XimpiaId', required=False, jsRequired=True, 
		initial='')
		password = PasswordField(_dbUser, 'password', minLength=6, required=False, jsRequired=True, 
		initial='')
		socialId = HiddenField()
		socialToken = HiddenField()
		authSource = HiddenField(initial=K.PASSWORD)
		choices = HiddenField(initial=_jsf.encodeDict({'authSources': Choices.SOCIAL_NETS}))
		errorMessages = HiddenField(initial=_jsf.buildMsgArray([_m, ['ERR_wrong_password']]))
		okMessages = HiddenField(initial=_jsf.buildMsgArray([_m, []]))

We need ``_XP_FORM_ID`` to have an unique id used in front-end. Your forms in a service should have an unique id. When we build
form data for front-end, we use field attributes from model like maxlength, labels and helptext. You can customize these attributes
in the form class as well.


Workflow
--------

It allows you to glue together your views (navigation) without writing code, just defining your flow with views and actions.
Depending on flow parameters you map flow to certain view. Your layers may write parameters to flow as you do with sessions. Session
data starts when user starts flow and end when flow ends. There is a set of parameters that control the way flows behave to adapt to
your needs.

In case you need it, you may also redirect to views from code inside your services. The drawback of this is that when you insert a new
view in a flow you need to modify code and test it. With built workflow, you simply plug view in the flow.

You would register flow parameters through components.py file::

	self._reg.registerFlow(__name__, flowCode='login')
	self._reg.registerFlowView(__name__, flowCode='login', viewNameSource='login', viewNameTarget='homeLogin', 
							actionName='login', order=10)

Actions
-------

Visual components associated with actions like buttons and links will call your actions. They may be called from search and menu items
as well.

Action operations may be mapped to your services. Each action would have an implementation associated with it in a method.

.. code-block:: python

	@validation()
	def _authen_user(self):
		if self._f()['authSource'] == K.FACEBOOK and self._f()['socialId'] != '':
			self._ctx.user = self._authenticate_user_soc_net(self._f()['socialId'], self._f()['socialToken'], 
			self._f()['authSource'], 'facebook', _m.ERR_wrong_password)
		else:
			self._ctx.user = self._authenticate_user(self._f()['username'], self._f()['password'], 
			'password', _m.ERR_wrong_password)

	@action(forms.LoginForm)
	def login(self):
		"""
		Performs the login action. Puts workflow parameter username, write context variables 
		userChannel and session.
		"""
		self._authen_user()
		self._login()
		user_channel_name = self._get_user_channel_name()
		self._dbUserChannel = UserChannelDAO(self._ctx_min)
		self._ctx.userChannel = self._dbUserChannel.get(user=self._ctx.user, name=user_channel_name)
		self._ctx.session['userChannel'] = self._ctx.userChannel

You need to map form associated with the action. Form is validated prior to process form. You don't need any code for that, when
form is not validated, then ``@action`` would send right JSON data to front-end to send messages to user.

You can implement validation operations that need to pass in order to execute your actions. You call them inside your action method (like
``self._authen_user()). You can think of this as service-level validaations or business validations.

You would register them like::

	self._reg.registerAction(__name__, serviceName='Users', actionName='login', slug='login', 
	className=SiteService, method='login')

Templates
---------


Visual Components
-----------------

