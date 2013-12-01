Business
========

Business layer will keep your app logic. Services should communicate with business layer
by models or entities, and business layer connect to data layer for data needs.

Business classes have parent ``CommonBusiness`` class, having attribute ``_ctx`` and
``_instances`` common method.

By having context, you may access at your business layer, user, workflow data, session
data and other common context data needed in driving logic for your app.

CommonBusiness
--------------

_ctx
""""

Attribute which holds the minimized context for  the application.

_instances(args)
""""""""""""""""

Method to collect data instances with context inyected:

.. code-block:: python

    from data import UserDAO, CustomerDAO

    db_user, db_customer = self._instances(UserDAO, CustomerDAO)


Implementation
--------------

.. code-block:: python

    from ximpia.xpcore.business import CommonBusiness

    class MyBusiness(CommonBusiness):
                
        def alocate_customer(self, customer):
            # logic for allocating a customer
            user = self._ctx.user
            session = self._ctx.session
            [ ... code .... ]

Coding Practises
----------------

You have organize your app having logic at services or move some or whole 'business' logic to the
business layer.

When you have a complex application you probably will have many common operations which define the
business. Youy may move them to the business layer and services do the job of managing forms and
use case requests.

Having business layer also allows you to have different service classes with unique service logic
but having same business operations.

You may have a service which is an external API that creates a new customer and you may have an internal
one (which does additional things). By having a common business logic of creating a customer, you may
call that business operations from both services. When logic for creating a customer changes, you only
need to change at the business operation you define.
