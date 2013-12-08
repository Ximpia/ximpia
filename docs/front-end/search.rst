Search
======

We provide a search box with auto-complete to have a shortcut place where call all views and actions.

You can register which views and actions show up in search auto-complete and also associate specific data to be searchable, like
customer names for example.

.. code-block:: python

    self._reg.registerSearch(__name__, text='Change Password', viewName=Views.CHANGE_PASSWORD)

When you want to register data, you would do in your services:

.. code-block:: python

    search = SearchService(self._ctx)
    search.add_index(customer_name, self._app, view_name='show_customer', 
        action_name=None, params={customer_id=876}):

This would add to search index a particular customer. Would show ``customer_name`` in auto-complete, which would be linked
to view ``show_customer`` with attributes ``customer_id=876``.
