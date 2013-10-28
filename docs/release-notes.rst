
Release Notes
=============

0.2.1
-----

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

0.2.0
-----

First mayor relase of Ximpia, adding visual components, service oriented architecture
and ximpia-app building app script.
