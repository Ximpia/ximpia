
Services
========

Ximpia services have these parts:

* :ref:`forms`: Allows to map view fields to database models.
* :ref:`services`: Implement views and action logic.
* :ref:`choices`: List choices for data models and forms.
* :ref:`messages`: Messages used for action results and error messages, displayed to users.
* :ref:`context`: Request, response and service data is kept at service context. Context data is contained in service class with ``_ctx`` attribute, having forms and additional service data. Minimized version is propagated to business and data layers.

.. _forms:

Forms
-----

The way for your service layer to communicate with front-end is forms.

Every view has a form atatched, having fields for messages and visual components fields, weather
it is a ``list view``or ``detail view`` (CRUD).

Form data is produced in ``JSON`` format and consumed by front-end template parsers.

Ximpia forms are similar to django forms, except that data instances are mapped inside form
fields:

.. code-block:: python

    class CustomerForm(XBaseForm):
        _XP_FORM_ID = 'customer' 
        _db_user = User()
        username = UserField(_db_user, 'username', label='XimpiaId', required=False, 
            jsRequired=True, initial='')
        errorMessages = HiddenField(initial=_jsf.buildMsgArray([_m, ['ERR_wrong_username']]))
        okMessages = HiddenField(initial=_jsf.buildMsgArray([_m, ['success']]))

``User`` would be the model class for django user.

The first parameter ro ximpia fields is the form data instance. The second one is the
data model field in string format. In this case: ``_db_user`` and ``username``.

You map forms to services with service decorators.

XBaseForm
^^^^^^^^^

_validate_same_fields(tuple_list)
"""""""""""""""""""""""""""""""""

    **Attributes**
    
    * ``tuple_list`` (list) : List of tuples. Each tuple with have a couple of fields to match.

_validate_captcha()
"""""""""""""""""""

    Would validate the captcha field with ``recaptcha`` : ``recaptcha_channlenge_field``.
    
    You would only need to call this method in your form views to provide validation for form data:
    
    .. code-block:: python
    
        def clean(self):
            """Clean form"""
            self._validate_captcha()
            self._xp_clean()
            return self.cleaned_data

_get_field_value(field_name)
""""""""""""""""""""""""""""

    Get field value. This method is used in your ``clean`` method to provide additional validations for your form.
    
    **Attributes**
    
    * ``field_name`` (str) : Field name
    
    **Returns**
    
    Form field value.

_xp_clean()
"""""""""""

    Clean ximpia form, cheching validations. Used when extending ``clean`` method.


cleaned_data
""""""""""""

    Form cleaned data to be compatible with django forms. Used when extending ``clean`` method.


get_param_dict(param_list:list)
"""""""""""""""""""""""""""""""

    Get dictionary of parameter values for list of parameters.
    
    **Attributes**
    
    * ``param_list`` (list) : List of parameters
    
    **Returns**
    
    Dictionary with parameter values
    
    When we request ['param1', 'param2']
    
    {'param1': 'myValue', 'param2': 'myValue'}

get_form_id()
"""""""""""""

    Get the form id.
    
    **Returns**
    
    Form Id


has_param(name)
"""""""""""""""

    Checks if form has param name.
    
    **Attributes**
    
    * ``name`` (str) : Param name
    
    **Returns**
    
    True/False

put_param_list(args)
""""""""""""""""""""

    Put list of params into form. They will be in params form hidden field::
    
        self._f().put_param_list(mode='OK', type='new')
    
    These form parameters are attached to your form. You can attach as many as you want from your services to provide
    visual behavior in your visual components or templates.


save()
""""""

    Saves the form. It will save all model fields and related tables to the form.


clean()
"""""""

    You would extend this method in your form instances in order to provide cross validations in your form:
    
    .. code-block:: python
    
        def clean(self):
            """Clean form"""
            self._validate_same_fields([('newPassword','newPasswordConfirm')])
            self._xp_clean()
            return self.cleaned_data
    
    Would provide checking same field values for ``newPassword`` and ``newPasswordConfirm``
    
    You have no need to implement this method in case you don't need extra validations for your form. In that case,
    all fields would be validated relative to their types and data model associations.



.. _services:

Services
--------

Hold your logic for APIs and use case logic: views, actions and business or service
operation validation.

You may map views, actions and action validators inside same service or you may separate
action logic in additional services, having view-only services. You may map views and action
artifacts any way you want.

Views
^^^^^

Views are rendered to user browser using HTML5 templates for data detail (read operations) and
lists (db queries).

This view queries customer data and displays results:

.. code-block:: python

    from data import CustomerDAO
    
    class SiteService(CommonService):
    
        @view(forms.CustomerForm)
        def view_customer(self, pk):
            db_customer = self._instances(CustomerDAO)[0] 
            self._set_main_form(forms.CustomerForm(instances={
                'db_customer': db_customer.get(pk=pk)
                }))

You set the form instance with ``_set_main_form``. Keys for data instances must correspond to form fields with data instances. Form 
``CustomerForm`` has db field ``db_customer`` which is Customer().

The easiest way to get your data instances is through ``_instances`` common operation, since already inyects context into business 
and data objects. You can also call data objects directly inyecting context.

This view displays a list of customers:

.. code-block:: python

        @view(forms.CustomerListForm)
        def view_customers(self):
            self._add_list('customers', db_customer.search_fields(['first_name', 'last_name', 'email', 'phone']))

Front-end would have in context field ``customers`` with the fields selected. Additionaly, ``search_fields`` takes attribute
to search for them to filter out data and has paging support.

Actions
^^^^^^^

Action visual components like buttons, links and other event driven components would call server-side actions.

You may have different buttons in a view call different actions, mapping directly from your views the service actions (operations).

Service actions have logic validators which in most cases need to be checked before executing action logic. In case validations are
not passed, service action is not executed and user sees a warning or error message you specify. You would define service validators
for your actions and action logic. You may keep action logic inside your services or place common logic in business layer.

Example that customer has right status:

.. code-block:: python

    @validation()
    def _validate_customer_status(self, customer_id):
        """
        Validates that customer has right status
        """
        self._validate_exists([
                [self._db_customer, {'customer_id': customer_id, 'status': K.PENDING}, 
                        'status', _m.ERR_customer_wrong_status]
                                ])

Validate methods ``_validate_exists`` and ``validate_not_exists`` allows you to provide business validation for your actions.

Each element from list of validations has:

* ``db instance``: data instance to check for fields existance or not existance
* ``field dictionary``: fields to check: key: value in dictionary
* ``view field``: View field to highlight in case validation does not pass
* ``error message``: Error message to display in view

``@validation`` decorator checks that form validates.

And you implement calling validation in your action:

.. code-block:: python

    @action(forms.CustomerForm)
    def activate_customer(self):
        self._validate_customer_status(self._f()['customer_id'])
        [... Logic to stuff to do when customer status is OK]

Form Values
^^^^^^^^^^^

You get form cleaned values by calling common service operation ``_f``:

.. code-block:: python

    self._f()['my_field']

You may also access like:

.. code-block:: python

    self._ctx.form['my_field']

action decorator checks that form related to action is validated. In case not validated, returns error
message to front-end.

In your service logic you don't need to validate form and implement validations, you just fetch form field value using
the operation ``_f()`` which returns a dictionary of field values.

Workflow Actions
^^^^^^^^^^^^^^^^

Action that will redirect users to other views are managed by the :ref:`workflow`. Worflow allows to define app navigation in a 
separate place from your code, therefore you don't need to implement flow in your code but in the flow definitions when
registering flow components (manage.py xpcomponents yourapp).

You register views and actions related to flows in ``components.py`` file and you register components calling the xpcore
management command ``xpcomponents``.

You would place decorator ``@workflow_action`` when defining these actions, like:

.. code-block:: python

    @workflow_action(DefaultForm)
    def logout(self):
        """Logout user
        """
        self._logout()

This decorator will check workflow variables to resolve which view to navigate to.

You may write flow variables from your actions like this:

.. code-block:: python

    self._put_flow_params(status='OK', mode='new')

User flow data is persistent. So when user returns to flow, system knows about last actions and may redirect
to right location (you can configure flow behavior with properties). Service action would write ``status='OK'``
and ``mode='new'``. You may define your flows so that different views gets displayed with statuses and modes.
You don't need to change code when those requirements change, just update action logic and flow components.


Decorators
^^^^^^^^^^

* ``@view`` (form) : View decorator that must send main form to use for view.
* ``@action`` (form) : Action decorator that must send form to use.
* ``@workflow_action`` (form) : Workflow action and form to use


.. _commonservice:

CommonService
^^^^^^^^^^^^^

These are the most common service operations from ``CommonService`` :

_put_flow_params(args)
""""""""""""""""""""""

    Writes flow parameters, like::
    
        self._put_flow_params(name=value, ...)

_put_form_value(field_name, field_value, form_id=None)
""""""""""""""""""""""""""""""""""""""""""""""""""""""

    **Attributes**
    
    * ``field_name`` (str) : Field name
    * ``field_value`` (str) : Field value
    * ``form_id`` (str) : For multiple forms, set which form field is related to
    
    Writes form field values. Useful when you have form fields not related to your models and need to set value
    from the service layer.

_f()
""""

    You also get form from context:
    
    .. code-block:: python
    
        self._ctx.form['my_field']

    **Returns**
    form_values <dict> having format key:value

_ctx
""""

    Service context

_validate_exists(db_data_list)
""""""""""""""""""""""""""""""

    Validates that list of fields for each data entity check. You can include list of entities with
    list of fields to check. In case rule does not check, front-end highlights field with error message.
    **All validation data must check**. You keep these in your ``_validate_*`` method for logic validations using
    ``@validation()`` decorator.
    
    .. code-block:: python
    
        self._validate_exists([
                [self._dbInvitation, {'invitationCode': invitation_code, 'status': K.PENDING}, 
                        'invitationCode', _m.ERR_invitation_not_valid]
                                ])
    
    **Attributes**
    
    * ``db_data_list`` (list) : Validation data instance list:
        * ``db_instance`` (data)
        * ``fields`` (dict)
        * ``view field`` (str)
        * ``error message`` (str)

_validate_not_exists(db_data_list)
""""""""""""""""""""""""""""""""""

    Validates that list of fields for each data entity does not check (NOT). You can include list of entities with
    list of fields to check. In case rule does not check, front-end highlights field with error message.
    **All validation data must check**. You keep these in your ``_validate_*`` method for logic validations using
    ``@validation()`` decorator.
    
    .. code-block:: python
    
        self._validate_not_exists([
                    [self._dbUser, {'username': self._f()['username']}, 'username', _m.ERR_ximpia_id],
                    [self._dbUser, {'email': self._f()['email']}, 'email', _m.ERR_email]
                    ])
    
    **Attributes**
    
    * ``db_data_list`` (list) : Validation data instance list:
        * ``db_instance`` (data)
        * ``fields`` (dict)
        * ``view field`` (str)
        * ``error message`` (str)


_get_setting(setting:str)
"""""""""""""""""""""""""

    Get setting. Returns the setting model instance. In case you want value, you would:
    
    .. code-block:: python
    
        my_setting_value = self._get_setting('my_setting').value
    
    In case you need to check if setting is True/False:
    
    .. code-block:: python
    
        if self._get_setting('has_feature').is_checked()
    
    **Attributes**
    
    * ``setting`` (str) : Setting name
    
    **Returns**
    
    setting (Setting model instance)


_add_attr(name, value)
""""""""""""""""""""""

    Adds attribute to front-end context. You may add any key/value to the context used by front-end. This is 
    useful for writing your own visual components that need additional server-side data, or adding extra
    data for your views.
    
    **Attributes**
    
    * ``name`` (str) : Name
    * ``value`` (str) : Value
    
    Example::
    
        self._add_attr('isSocialLogged', False)
    
    Used by xpsite login. This attribute, ``isSocialLogged`` is used by conditions in login view.

_set_main_form(form_instance)
"""""""""""""""""""""""""""""

    When dealing with multiple forms inside views, allows you to set which one is used for validations,
    no matter which one you have in decorator.
    
    **Attributes**
    
    * ``form_instance`` (XBaseForm) : Form instance

_add_form(form_instance)
""""""""""""""""""""""""

    We add additional form to view. This form can be mapped into popups.
    
    **Attributes**
    
    * ``form_instance`` (XBaseForm) : Form instance

_show_view(view_name, view_attrs={})
""""""""""""""""""""""""""""""""""""

    Displays view with a set of parameters. In case you need to have advanced workflows, you may redirect flows
    to views from your service actions.
    
    **Attributes**
    
    * ``view_name`` (str) : View name
    * ``view_attrs`` (dict) : View attributes

_set_cookie(key, value)
"""""""""""""""""""""""

    Sets cookie.
    
    **Attributes**
    
    * ``key`` (str) : Key
    * ``value`` (str) : Value

_set_ok_msg(idOK)
"""""""""""""""""

    Sets which ``OK`` message will be shown to user. Pretty useful when different messages can be shown depending
    on conditions. You set which one to show in service logic and users will see that particular message.
    
    **Attributes**
    
    * ``idOK`` (str) : Ok message id from messages.py file

_set_form(form_instance)
""""""""""""""""""""""""

    Set which form instance is used in service context.
    
    **Attributes**
    
    * ``form_instance`` (XBaseForm) : Form instance


_instances(args)
""""""""""""""""

    Instances data and business classes inyecting context.
    
    args can be list of strings or classes.
    
    When these DAO's are in same app:
    
    .. code-block:: python
    
        db_user, db_customer = self._instances('data.UserDAO', 'data.CustomerDAO')
    
    When in another app:
    
    .. code-block:: python
    
        db_user, db_customer = self._instances('ximpia.xpcore.data.UserDAO', 
            'ximpia.xpcore.data.CustomerDAO')
    
    For these cases, we import class, create instance and inyect minimized context
    
    .. code-block:: python
    
        from my_module import UserDAO, CustomerDAO
        db_user, db_customer = self._instances(UserDAO, CustomerDAO)
    
    We just create instance from classes without importing.
    
    You may do same with business classes as well as data classes.


.. _choices:

Choices
-------

Parametric data which is not meant to change much is contained in ``choices.py`` for your app:

You refer to choices in form fields and django data model fields.

.. code-block:: python

    class Choices(object):
    # SUBSCRIPTION
    SUBSCRIPTION_TRIAL = 'trial'
    SUBSCRIPTION_VALID = 'valid'
    SUBSCRIPTION_NONE = 'None'
    SUBSCRIPTION = (
            (SUBSCRIPTION_TRIAL, _('30-Day Free Trial')),
            (SUBSCRIPTION_VALID, _('Valid')),
            (SUBSCRIPTION_NONE, _('None')),
            )

For data lists that are not meant to change often, you may define your lists at ``choices.py`` inside your app. These choices
can be referenced in your models or forms.

You may refer default values in models and forms::

    from choices import Choices as _Ch

    default=_Ch.SUBSCRIPTION_TRIAL


.. _messages:

Messages
--------

You keep error and ``OK`` messages in ``messages.py`` file in your app.

.. code-block:: python

    # Messages
    OK_USER_SIGNUP = _('Your signup has been received, check your email')
    OK_SOCIAL_SIGNUP = _('Thanks! Signup complete. You can now login')
    OK_PASSWORD_REMINDER = _('OK!. We sent you an email to reset password')
    OK_PASSWORD_CHANGE = _('OK! Password changed')
    ERR_change_password = _('Invalid data to change password')

You would reference message ids in form messages fields like:

.. code-block:: python

    import messages as _m
    from ximpia.util.js import Form as _jsf

    errorMessages = HiddenField(initial=_jsf.buildMsgArray([_m, ['ERR_change_password']]))
    okMessages = HiddenField(initial=_jsf.buildMsgArray([_m, ['OK_PASSWORD_CHANGE']]))

.. _context:

Context
-------

Ximpia context keeps important app data like user profile, service request, service data which is shared by all
layer in our applications.

You may extend context to include additional fields and data for your applications.

**Attributes**

* ``app``:String : Application name
* ``user``:User : User
* ``lang``:String : Language
* ``session``:String : Django session object
* ``cookies``:object : Django cookies
* ``meta``:object : Django META object
* ``post``:object . Django POST request
* ``request``:object . Django request object
* ``get``:object : Django get result
* ``userChannel``:String : User channel name
* ``auth``:Dict : User has logged in?
* ``form``:object : Main form for view
* ``forms``:Dict : Forms container for view
* ``captcha``:String : Captcha text
* ``ctx``:object : Context
* ``jsData``:JsResultDict : json data response object, JsResultDict()
* ``viewNameSource``:String : For workflows, source view name. In case we have no workflow, this value will be the requested view
* ``viewNameTarget``:String : For workflows, target view name.
* ``action``:String : Action name
* ``isView``:Boolean : View is requested
* ``isAction``:Boolean : Action is requested
* ``flowCode``:String : Flow code
* ``flowData``:String : Flow data
* ``isFlow``:Boolean : When True, view is inside workflow.
* ``set_cookies``:List
* ``device``:String : Device
* ``country``:String : Country code
* ``winType``:String : Type of windows: window, popup
* ``tmpl``:String : Template container
* ``wfUserId``:String : Workflow user id
* ``isLogin``:Boolean : Weather user has logged in
* ``container``:Dict : Container with key->value in dict format
* ``doneResult``:Boolean : Used by decorators to define that result has been built.
* ``isServerTmpl``:Boolean : Defines if requesting JSON or web response. In case we have an AJAX request, we will have this to False. In case we request an url this value will be True. ServiceDecorator will build different response based on this.
* ``dbName`` : Resolved connection from data layer. Assigned for first operation, either action or view.
* ``path`` : Path for actions or vies, like /apps/appSlug/viewSlug or /apps/appSlug/do/actionSlug. Filled by decorators
* ``application`` : Application model instance 

You would have minimized context in business and data layers without forms and other service data.

You would access with ``_ctx`` attributes in services, data or businesses classes:

.. code-block:: python

    app = self._ctx.app
