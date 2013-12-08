Menu
====

Menu items get generated from the information you define in ``components.py`` configuration file.

Example:

.. code-block:: python

    from ximpia.xpcore.choices import Choices as _Ch
    import ximpia.xpcore.constants as _K

    self._reg.registerViewMenu(__name__, viewName=Views.HOME_LOGIN, menus=[
                    {_K.ZONE: _Ch.MENU_ZONE_SYS, _K.MENU_NAME: Menus.SYS},
                    {_K.ZONE: _Ch.MENU_ZONE_SYS, _K.GROUP: Menus.SYS, 
                        _K.MENU_NAME: Menus.CHANGE_PASSWORD},
                    {_K.ZONE: _Ch.MENU_ZONE_SYS, _K.GROUP: Menus.SYS, 
                        _K.MENU_NAME: Menus.SIGN_OUT},
                    {_K.ZONE: _Ch.MENU_ZONE_MAIN, _K.MENU_NAME: Menus.HOME_LOGIN}
                ])
    self._reg.registerViewMenu(__name__, viewName=Views.ACTIVATION_USER, menus=[
                    {_K.ZONE: _Ch.MENU_ZONE_VIEW, _K.MENU_NAME: Menus.HOME},
                    {_K.ZONE: _Ch.MENU_ZONE_VIEW, _K.MENU_NAME: Menus.LOGIN}
                ])
    self._reg.registerViewMenu(__name__, viewName=Views.SIGNUP, menus=[
                    {_K.ZONE: _Ch.MENU_ZONE_VIEW, _K.MENU_NAME: Menus.HOME},
                    {_K.ZONE: _Ch.MENU_ZONE_VIEW, _K.MENU_NAME: Menus.LOGIN}
                ])
    self._reg.registerServMenu(__name__, serviceName=Services.USERS, menus=[
                    {_K.ZONE: _Ch.MENU_ZONE_MAIN, _K.MENU_NAME: Menus.LOGIN, 
                        _K.CONDITIONS: 'notLogin:render:True'},
                    {_K.ZONE: _Ch.MENU_ZONE_MAIN, _K.MENU_NAME: Menus.SIGNUP, 
                        _K.CONDITIONS: 'notLogin:render:True'},
                    {_K.ZONE: _Ch.MENU_ZONE_MAIN, _K.MENU_NAME: Menus.HOME_LOGIN, 
                        _K.CONDITIONS: 'login:render:True'}
                ])

Zones
-----

* ``sys`` : Entries displayed when you click on logo item and drop down displays.
* ``main`` : Entries right to search box, which generally would be without text (Small icons)
* ``view`` : Entries of views either associated to services or views related to currentl view.

Services
--------

You can register views inside services in menu or you can use the ``registerServMenu`` which has some highlight for current
view in a service. All views from services would be visible (when you register them) and users would know which view they are in.
It is nice for SiteService and small sites, where you have 4 or 5 views and users know which site zone they are in.

Also nice with services that you want users to have some 'location' of where they are.

Linked Views
------------

You can link related views to current one from the view zone. It is a nice way to tell users what related features exist on 
current view. These additional views will add value to information shown to user.

These views can be from other services within your app or services in another apps users have access.

Views would be popup or normal full views.

Conditions
----------

You may associate conditions to your menu with conditions based on visual context:

.. code-block:: python

    self._reg.registerCondition(__name__, 'notLogin', 'isLogin == false')
    self._reg.registerCondition(__name__, 'login', 'isLogin == true')

    self._reg.registerServMenu(__name__, serviceName=Services.USERS, menus=[
                    {_K.ZONE: _Ch.MENU_ZONE_MAIN, _K.MENU_NAME: Menus.LOGIN, 
                        _K.CONDITIONS: 'notLogin:render:True'},
                    {_K.ZONE: _Ch.MENU_ZONE_MAIN, _K.MENU_NAME: Menus.SIGNUP, 
                        _K.CONDITIONS: 'notLogin:render:True'},
                    {_K.ZONE: _Ch.MENU_ZONE_MAIN, _K.MENU_NAME: Menus.HOME_LOGIN, 
                        _K.CONDITIONS: 'login:render:True'}
                ])

The home login button will only display when we are logged in. Otherwise, will not render.
