Data
====

Ximpia provides a data layer to connect to your data sources. These data sources can be
relational (SQL) data sources or noSQL data sources.

We follow philosophy that service layer do not call django model data access methods directly
and use data classes (what could be similar to a django model manager).

You may have your data operations return django models or simple entities like dictionaries
with attribute calling (customer.name) when you deal with data sources and noSQL.

Advantages of data layer:

* You keep simple and complex data access methods in the data layer
* Knows which data nodes to call (master or replicas) depending on type of request (view or action)
* You may change your data sources without changing your services / business layers
* You may change data sources (django, sqlalchemy, redis, mongo)

Currenly we offer CommonDAO which deals with django data model access. This class has common
data operations.

Master/Replicas
---------------

In case you use master/slave data nodes, you don't need to have routers to route to master or slaves.
We think a simpler design is good. Depending on view or action request, the data layer hits master
or slave nodes. In case no slaves defined, will allways hit default data node.

BaseModel
---------

Keeps attributes about auditory (create_user and update_user) and create and update fields.

All django models would extend this model.

Keeps delete management. When we delete data, we write ``isDeleted=True``.

You can delete data for ever with ``is_real`` attribute in delete operations.

CommonDAO
---------

Your data layer classes will be related to django models, like:

.. code-block:: python

    from ximpia.xpcore.data import CommonDAO

    class UserMetaDAO(CommonDAO):
        model = UserMeta
        
        def my_data_operation(self, customer_id):
            # you return django queryset, django model, attribute dictionary or plain dictionary
            # good place to have complex queries, Q objects, etc...

Implementation:

.. code-block:: python

    db_customer = self._instances(CustomerDAO)[0]
    customers = db_customer.search(id=23)

Will return a django queryset, where you can filter (``customers.filter(name='john')``)

In case you need to access model (from services and business) and do operations on model, do:

.. code-block:: python

    db_customer.model.objects.all()

**Exception**

Will raise ``XpMsgException`` with error literal message and attribute ``origin='data'``:

.. code-block:: python

    from ximpia.xpcore.models import XpMsgException
    try:
        db_customers.get(id=34)
    except XpMsgException:
        # treat exception

* :ref:`commondao.check`
* :ref:`commondao.create`
* :ref:`commondao.delete`
* :ref:`commondao.delete_if_exists`
* :ref:`commondao.delete_by_id`
* :ref:`commondao.filter_data`
* :ref:`commondao.get`
* :ref:`commondao.get_all`
* :ref:`commondao.get_create`
* :ref:`commondao.get_map`
* :ref:`commondao.get_by_id`
* :ref:`commondao.save`
* :ref:`commondao.search`
* :ref:`commondao.search_fields`


.. _commondao.check:

check
"""""

    Checks if exists

    **Attributes**

    keyword attributes, like:

    .. code-block:: python
    
        if db_customer.check(name='john', status='new'):
            # more...

    **Returns**

    True/False

.. _commondao.create:

create
""""""

    Will create model with attributes 

    .. code-block:: python
    
        customer = db_customer.create(name='john', status='new')

    **Attributes**
    
    keyword attributes
    
    **Returns**
    
    Django model created

.. _commondao.delete:

delete
""""""

    Will delete rows that match the keyword attributes
    
    .. code-block:: python
    
        db_customer.delete(name='john', status='new')
    
    **Attributes**
    
    * ``is_real`` (boolean)
    
    keywork attributes
    
    **Returns**
    
    None

.. _commondao.delete_if_exists:

delete_if_exists
""""""""""""""""

    Will delete rows that match the keyword attributes in case exists. If not, does not throw exception.
    
    .. code-block:: python
    
        db_customer.delete_if_exists(name='john', status='new')
    
    **Attributes**
    
    * ``is_real`` (boolean)
    
    keywork attributes
    
    **Returns**
    
    None

.. _commondao.delete_by_id:

delete_by_id
""""""""""""

    Delete by primary key
    
    .. code-block:: python
    
        db_customer.delete_by_id(23)
        db_customer.delete_by_id(23, is_real=True)
    
    **Attributes**
    
    * ``pk`` (long)
    
    **Optional Attributes**
    
    * ``is_real`` (boolean)
     
    **Returns**
    
    None

.. _commondao.filter_data:

filter_data
"""""""""""

    Search model with ordering and paging
    
    .. code-block:: python
    
        db_customer.filter_data(status='OK')
        db_customer.filter_data(status='OK', xpNumberMatches=100)
    
    **Attributes**
    
    keyword attributes
    
    **Optional Attributes**
    
    * ``xpNumberMatches`` (int) : default 100
    * ``xpPage`` (int) : default 1
    * ``xpOrderBy`` (tuple)
    
    keywork attributes
    
    **Returns**
    
    queryset

.. _commondao.get:

get
"""

    Get model which match attributes

    **Attributes**
    
    keyword attributes for query
    
    **Returns**
    
    django model

.. _commondao.get_all:

get_all
"""""""

    Get all results for model
    
    **Returns**
    
    django queryset

.. _commondao.get_create:

get_create
""""""""""

    Get object. In case does not exist, create model object
    
    **Attributes**
    
    Keyword attributes
    
    **Returns**
    
    (object, created) <model, boolean>

.. _commondao.get_map:

get_map
"""""""

    Get container (dictionary) of {id: object, ...} for list of ids
    
    **Attributes**
    
    * ``id_list`` (list) : List of ids
    
    **Returns**
    
    Dictionary with ids and objects

.. _commondao.get_by_id:

get_by_id
"""""""""

    Get object by id
    
    **Attributes**
    
    * ``field_id``
    
    **Returns**
    
    Model object

.. _commondao.save:

save
""""

    Saves the model
    
    .. code-block:: python
    
        customer = CustomerDAO.model(name='john', status='OK')
        customer.save()
        
        db_customer = self._instances(CustomerDAO)[0]
        customer = db_customer.get_by_id(23)
        customer.name='james'
        customer.save()
    
    **Returns**
    
    None

.. _commondao.search:

search
""""""

    Search model to get queryset (like filter)
    
    Search model, like:
    
    .. code-block:: python
    
        customers = db_customer.search(name='john')
    
    **Attributes**
    
    * ``qs_args`` (dict) : Keywork attributes like attr=value
    
    **Returns**
    
    Django queryset

.. _commondao.search_fields:

search_fields
"""""""""""""

    Search table with paging, ordering for set of fields. listMap allows mapping from keys to model fields.    
    
    ** Attributes **
    
    * ``fields``:tuple<str>

    **Optional Attributes**

    * ``page_start``:int [optional] [default:1]
    * ``page_end``:int [optional]
    * ``number_results``:int [optional] [default:from settings]
    * ``order_by``:tuple<str> [optional] [default:[]]    

    keyword attributes
    
    ** Returns **
    
    Returns the query set with values(\*fields).
    
    xpList:ValuesQueryset
