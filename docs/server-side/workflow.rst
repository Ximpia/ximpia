
Workflow
========

Defines navigation for your application, which views trigger other views and which actions are called that trigger views.

You would need:

1. ``Actions``: Flow navigation is triggered by action components. You need to define actions that will navigate to other views.
2. ``Flow Variables``: In order to define conditions for your flow, you would need to define variables. You register flow variables
    with register methods and define flows with variable values.
3. ``Label methods``: Include decorator into your views and actions to let ximpia know they must follow flows.

Ximpia would query which view to show when actions are executed. You don't need to code navigation for your application. When 
your flow changes, you update variables and flow parameters and your flow is changes (For example, to plug in a new view).

We define flow and simple navigation without conditions. You would register flow in ``components.py``:

.. code-block:: python

    self._reg.registerFlow(__name__, flowCode='login')
    self._reg.registerFlowView(__name__, flowCode='login', viewNameSource=Views.LOGIN, 
        viewNameTarget=Views.HOME_LOGIN, actionName='login', order=10)

And then write flow variables in your service layer in action methods:

.. code-block:: python

    self._put_flow_params(my_var='Customer')

Workflow would have enough info on which views to navigate to.

Decorators
----------

* ``ximpia.xpcore.service.workflow_view`` (flow_code, form) : Label view and relate to flow. Set main form to be used.
* ``ximpia.xpcore.service.workflow_action`` (flow_code, form) : Label action and relate to flow. Set main form to be used for validation.

Models
------

.. automodule:: ximpia.xpcore.models
   :members: Workflow, WorkflowView, WorkflowData

Service
-------

Service methods that deal with workflow are:

.. autoclass:: ximpia.xpcore.service.CommonService
   :members: _put_flow_params, _get_target_view, _get_flow_params, _get_wf_user

WorkflowBusiness
----------------

.. autoclass:: ximpia.xpcore.business.WorkFlowBusiness
   :members: 
