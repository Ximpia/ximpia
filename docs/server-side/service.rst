
Service Layer
=============

Form
----

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
``CustomerForm`` has db field ``db_customer``which is Customer().

The easiest way to get your data instances is through ``_instances`` common operation, since already inyects context into business 
and data objects. You can also call data objects directly inyecting context.

This views displays a list of invitations:

[...Code for list of data...]

Actions
^^^^^^^

Action visual components like buttons, links and other event driven components would call server-side actions.

You may have different buttons in a view call different actions, mapping directly from your views the service actions (operations).

Service actions have logic validators which in most cases need to be checked before executing action logic. In case validations are
not passed, service action is not executed and user sees a warning or error message you specify:


Workflow Actions
^^^^^^^^^^^^^^^^


Decorators
^^^^^^^^^^


Operations
^^^^^^^^^^

These are the most common service operations from ``CommonService``:

----

We provide these decorators:


Choices
-------

Parametric data which is not meant to change much is contained in ``choices.py`` for your app:

You refer to choices in form fields and django data model fields.

Messages
--------


Context
-------
