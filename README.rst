==================
Ximpia Environment
==================

Description
-----------

Ximpia is an agile environment to speed up development of web projects.

On the Front-end, you have visual components with properties defined in HTML5 templates. Server side data is mixed
with components to render final HTML code. Most apps don't need to develop javascript, simply parametrize provided components 
to define visual behavior.

On the server side, you have a service-oriented architecture with views, actions, navigation flow and other server 
services to help speed up development. Services produce JSON data that is processed by visual components.

Documentation
-------------

https://ximpia.readthedocs.org/ 

Installation
------------

Using ``pip``::

	pip install ximpia

This will install ximpia and required packages:

* Grappelli
* Filebrowser
* South

Upgrading
---------

Using ``pip``::

    pip --upgrade install ximpia

Migrate Ximpia apps::

    python manage.py migrate ximpia.xpcore
    python manage.py migrate ximpia.xpsite

Update site components::

    python manage.py xpcomponents ximpia.xpsite

Setup Application
-----------------

To start your application, type::

	ximpia-app myproject.myapp

It will create folders and files needed for your application in ximpia. It will prompt for
basic information like database connection user, admin name and password and locale.

Creates and registers your application home view.

Then you only need to go to directory for your project::

	./manage.py runserver

And open your browser at ``http://127.0.0.1:8000/``

For further details, visit project documentation.

Follow Us
---------

https://ximpia.com

https://www.facebook.com/ximpia

https://twitter.com/ximpia

http://blog.ximpia.com

Release Notes
-------------

Adds changes to navigation system, default app, minor changes and bug fixes.

**Workflow Changes**

* **No workflow decorator for workflow views**
* **Decorators don’t need to configure flow code**
* **Workflow views don’t need flow decorator**
* **No event flow links**: Flow links can be triggered when flow variables match your criteria, with or without executing actions.
* **Flow META**: A new table for meta variable/value has been added. As new workflow configuration variables are added, we don’t need to change model structure, just a data migration with new workflow meta variables. Currently we have meta variables for reset on start of flow, delete user data on end and jump to last view by user.

**Default App**

You can configure default app in ``settings.py``. When building urls using slugs,
for components related to your default app, we do not show app slug, all views come from 
root path, like ``/contact-us``.

If you want to disable, just have default app to ''

**Upgrading**

You need to migrate the ximpia apps: ``ximpia.xpcore`` and ``ximpia.xpsite``::

    python manage.py migrate ximpia.xpcore ximpia.xpsite

Since we now add request property to services, we need to inyect request into site
service at your app views.py file:

.. code-block:: python

    @context_view(__name__)
    @view_tmpl(__name__)
    def home(request, **args):
        # Instantiage SiteService.home and return result
        site = SiteService(args['ctx'])
        site.request = request
        result = site.viewHome()
        return result

Foe release notes from previous releases, check Documentation.

License
-------

::

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at
 
        http://www.apache.org/licenses/LICENSE-2.0
 
    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License. 
