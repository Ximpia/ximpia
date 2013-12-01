
.. _workflow:

Workflow
========

Defines navigation for your application, which views trigger other views and which actions are called that trigger views.

Ximpia would query which view to show when actions are executed. You don't need to code navigation for your application. When 
your flow changes, you update variables and flow parameters and your flow is changes (For example, to plug in a new view).

We define flow and simple navigation without conditions. You would register flow in ``components.py``:

.. code-block:: python

    self._reg.registerFlow(__name__, flowCode='customer_provision')
    self._reg.registerFlowView(__name__, flowCode='customer_provision', 
        viewNameSource='create_customer', viewNameTarget='customer_provisioned_profile_a', 
        actionName='activate_customer', condition="profile='corporate'")
    self._reg.registerFlowView(__name__, flowCode='customer_provision', 
        viewNameSource='create_customer', viewNameTarget='customer_provisioned_profile_b', 
        actionName='activate_customer', condition="profile='smb'")

And then write flow variables in your service layer in action methods with correct decorator:

.. code-block:: python

    @workflow_action(forms.CustomerForm)
    def activate_customer(self, customer_id, activation_code):
        self._put_flow_params(profile='corporate')

Workflow would have enough info on which views to navigate to, depending on workflow variable ``profile``. You may
check for a number of conditions that all must match.

You can also:

* Define flow links with or without events: When having an event (click on button, for example), flow will not continue. But when no event then flow will continue while conditions meet or finds an event.
* Condition-less: You may define flow links without conditions for parameters. In these cases, it is like adding a hard link that will be met no matter what.

Decorators
----------

* ``ximpia.xpcore.service.workflow_action`` (form) : Set main form to be used for validation.

Extension
---------

In case the provided workflow is not enough for you, you can provide you own flow using provided methods in :ref:`commonservice`.

_show_view(view_name, view_attrs={})
""""""""""""""""""""""""""""""""""""

    Displays view with a set of parameters. In case you need to have advanced workflows, you may redirect flows
    to views from your service actions.
    
    **Attributes**
    
    * ``view_name`` (str) : View name
    * ``view_attrs`` (dict) : View attributes

_get_flow_params(\*name_list)
"""""""""""""""""""""""""""""

    Get flow params by list:
    
    .. code-block:: python
    
        params = self._get_flow_params('status', 'profile')

_get_wf_user()
""""""""""""""

    Get workflow user. Allows for user id and dealing with advanced flows.

Models
------

* :ref:`models.workflow`
* :ref:`models.workflowview`
* :ref:`models.workflowdata`


WorkflowBusiness
----------------


build_flow_data_dict
""""""""""""""""""""

    Build the flow data dictionary having the flowData instance

    **Attributes**
    
    * ``flow_data``
    
    **Returns**
    
    flow_data_dict (dict)

gen_user_id
"""""""""""

    Generate workflow user id.
        
    **Returns**
    user_id (long)

get
"""

    **Attributes**
    
    * ``flow_code`` (str)

    Get flow
    
    **Returns**
    
    workflow:Workflow

get_flow_data_dict
""""""""""""""""""

    Get flow data dictionary for user and flow code

    **Attributes**
    
    * ``wf_user_id``
    * ``flow_code``
    
    **Returns**
    
    flow_data_dict (dict)

get_flow_view_by_action
"""""""""""""""""""""""

    Get flow by action name. It queries the workflow data and returns flow associated with actionName

    **Attributes**
    
    * ``action_name``
    
    **Returns**
    
    flow_view (WorkflowView)

get_param
"""""""""

    Get workflow parameter value from context

    **Attributes**
    
    * ``name``
    
    **Returns**
    
    parameter value (str)

get_param_from_ctx
""""""""""""""""""

    Get flow parameter from context.

    **Attributes**
    
    * ``name``
    
    **Returns**
    
    Parameter value

get_view
""""""""

    Get view from flow
    
    **Attributes**
    
    * ``wf_user_id``
    * ``flow_code``
    
    **Returns**
    
    view (View)

get_view_name
"""""""""""""

    Get view name

get_view_params
"""""""""""""""

    Get view flow parameters
    
    **Attributes**
    
    * ``flow_code``
    * ``view_name``
    
    **Returns**
    
    params (dict) : {name: value, ... }

is_first_view
"""""""""""""

    Is first view in flow?
    
    **Attributes**
    
    * ``flow_code``
    * ``view_name``
    
    **Returns**
    
    True/False

is_last_view
""""""""""""

    Is last view in flow?
    
    **Attributes**
    
    * ``view_name_source``
    * ``view_name_target``
    * ``action_name``
    
    **Returns**
    
    True/False

put_params
""""""""""

    Put params in flow.
    
    **Attributes**
    
    keywork argumens

remove_data
"""""""""""
    
    Remove user data from flow.
    
    **Attributes**
    
    * ``wf_user_id``
    * ``flow_code``

reset_flow
""""""""""

    Reset flow
    
    **Attributes**
    
    * ``wf_user_id``
    * ``flow_code``
    * ``view_name``

resolve_flow_data_for_user
""""""""""""""""""""""""""

    Resolves flow for user and session key
    
    **Attributes**
    
    * ``wf_user_id``
    * ``flow_code``
    
    **Returns**
    
    flow:WorkflowData

resolve_view
""""""""""""

    Search destiny views with origin viewSource and operation actionName

    ** Attributes **

    * ``wf_user_id`` : Workflow user id
    * ``app_name`` : App name
    * ``flow_code`` : Flow code
    * ``view_name_source`` : Origin view
    * ``action_name`` : Action name

    ** Optional Attributes **

    * ``flow_views`` (list<WorkflowView>) : List of flow views to check flow links from. No need to query for flow links.

    ** Returns **
    flowView resolved, which represent flow link data
        
save
""""

    Save flow into data source
    
    **Attributes**
    
    * ``wf_user_id``
    * ``flow_code``

set_view_name
"""""""""""""

    Set view name
    
    **Attributes**
    
    * ``view_name``

