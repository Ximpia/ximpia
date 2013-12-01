Component Registry
==================

You need to register server-side components through ``components.py`` file.

* **Apps and Services**
* **Views**
* **Templates**
* **Actions**
* **Flows and flow data**
* **Menus**
* **Search commands**

.. _register.apps:

Apps and Services
-----------------

.. code-block:: python

    from service import SiteService
    class AppReg (AppCompRegCommonBusiness):
        def __init__(self):
            super(AppReg, self).__init__(__name__)
            # Application
            self._reg.registerApp(__name__, title='My App', slug='my-app')
            # Services
            self._reg.registerService(__name__, serviceName='MyService', className=SiteService)

By default your app comes with SiteService. You can have as many services as you want, you can create them
here and implement in ``service.py``. Each use case can become a service, with views and actions associated.

.. _register.views:

Views
-----

.. code-block:: python

     self._reg.registerView(__name__, serviceName='MyService', viewName='myView', slug='my-view', 
                            className=SiteService, method='view_mine')

You refer to above service name, defining a view name, slug and which class and method implements it.

.. _register.templates:

Templates
---------

.. code-block:: python

    self._reg.registerTemplate(__name__, viewName='myView', name='my_template')

You map views and templates. Templates will be found in ``templates`` directory. They can be window or popup types,
holding different directories for ech template type.

.. _register.actions:

Actions
-------

.. code-block:: python

    self._reg.registerAction(__name__, serviceName='MyService', actionName='changeStatus', slug='change-status', 
                                className=SiteService, method='change_status')

    Your SiteService would need a method ``change_status``.

.. _register.flows:

Flows and flow data
-------------------

.. code-block:: python

    self._reg.registerFlow(__name__, 'activate-user', resetStart=True, deleteOnEnd=True, jumpToView=False)
    self._reg.registerFlowView(__name__, 'activate-user', actionName='activateUser', viewNameTarget='activationUser')

You would attach additional attributes to map flow variables.

.. _register.menus:

Menus
-----

.. code-block:: python

    self._reg.registerMenu(__name__, name='signup', title='Signup', description='Signup', iconName='iconSignup', 
                    viewName='signup')
    self._reg.registerServMenu(__name__, serviceName='MyService', menus=[
                    {_K.ZONE: _Ch.MENU_ZONE_MAIN, _K.MENU_NAME: Menus.LOGIN, _K.CONDITIONS: 'notLogin:render:True'},
                    {_K.ZONE: _Ch.MENU_ZONE_MAIN, _K.MENU_NAME: Menus.SIGNUP, _K.CONDITIONS: 'notLogin:render:True'},
                    {_K.ZONE: _Ch.MENU_ZONE_MAIN, _K.MENU_NAME: Menus.HOME_LOGIN, _K.CONDITIONS: 'login:render:True'}
                ])

The first one creates menu entity. The second creates relationship between a view or service and which menu items holds. In this case,
we map a service having icons login, signup and home login with conditions based on user login. In case you map services, you don't need
to map menu items for each view. But you may, for example, define shortcut views related to your view. You can do that mapping menu
items to views. For example, you can have a service about customer management and link views related to functionality related to
your service use case like "Invite Customer".

This is how you map individual views:

.. code-block:: python

    self._reg.registerViewMenu(__name__, viewName=Views.SIGNUP, menus=[
                    {_K.ZONE: _Ch.MENU_ZONE_VIEW, _K.MENU_NAME: Menus.HOME},
                    {_K.ZONE: _Ch.MENU_ZONE_VIEW, _K.MENU_NAME: Menus.LOGIN}
                ])

We map signup page with home and login.

.. _register.search:

Search commands
---------------

.. code-block:: python

    self._reg.registerSearch(__name__, text='Change Password', viewName=Views.CHANGE_PASSWORD)

Allows to map views and actions to happen at auto-complete box in top menu. When clicked, a new view (window or popup) would
come or action be executed, redirecting in this case to another view.
