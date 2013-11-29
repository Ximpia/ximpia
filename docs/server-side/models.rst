
Models
======

.. toctree::
   :maxdepth: 2

**BaseModel**

    Abstract Base Model with fields for all other models. Ximpia models have this model as parent. This model provides audit
    information like date creating and updating, as well as user involved in the update or creation.
    
    When you delete rows in Ximpia, ``isDeleted``field is set to True. You can force to physical delete by passing ``real=True`` to 
    data delete methods (db.delete, db.deleteById and db.deleteIfExists).
    
    When deleting rows with the django admin interface, you cannot delete database records physically, therefore those rows will have
    isDeleted=True and will not show in the admin pages. You can delete for ever with your application code or directly connecting to
    your database.
    
    **Attributes**
    
    * ``id`` : Primary key
    * ``dateCreate``:DateTimeField
    * ``dateModify``:DateTimeField
    * ``userCreateId``:IntegerField
    * ``userModifyId``:IntegerField
    * ``isDeleted``:BooleanField
    
    **Relatinships**

**Action**

    Actions are mapped to service operations. Actions can be triggered by clicking on a button, a link, a menu icon or any other
    visual component that triggers actions.
    
    Here we map action names, implementations, slugs and action properties. Implementations are built by component registering.
    
    **Attributes**
    
    * ``id``:AutoField : Primary key
    * ``name``:CharField(30)
    * ``implementation``:CharField(100)
    * ``slug``:SlugField(50)
    * ``hasAuth``:BooleanField
    * ``image``:FileBrowserField
    
    **Relationships**
    
    * ``application`` -> Application
    * ``service`` -> Service
    * ``accessGroups`` <-> xpsite.Group through ActionAccessGroup

**Application**

    Applications. For most sites, they will have single application for N services which relate to use cases for views and actions.
    In case your application is big or have admin backdoors, your site with have more than one application.
    
    This table holds applications at your site. slug corresponds to the host name that related to the application, like 'slug.domain.com'.
    You can also access applications by /apps/slug in case application hosts is disabled.
    
    Applications can be grouped together using the ``parent`` field.
    
    Applications can have subscription business model or be free. In case subscription required, ``isSubscription`` would be ``True``
    
    Applications can be private and accessible only to a group of users. ``isPrivate`` would be ``True`` in this case. Applications can
    start private (like a private beta) and then make them public. When making public applications, you can publish at Ximpia 
    directory.
    
    Applications have meta information through model ApplicationMeta. You can attach meta values for application in this model.
    
    **Attributes**
    
    * ``id`` : Primary key
    * ``name``:CharField(15) : Application path, like ximpia.xpsite. Must contain package name and application name. Has format similar to installed apps django setting.
    * ``slug``:SlugField(30)
    * ``title``:CharField(30)
    * ``isSubscription``:BooleanField
    * ``isPrivate``:BooleanField
    * ``isAdmin``:BooleanField
    
    **Relationships**
    
    * ``developer`` -> User
    * ``developerOrg`` -> 'xpsite.Group'
    * ``parent`` -> self
    * ``accessGroup`` -> 'xpsite.Group'
    * ``users`` <-> UserChannel through ApplicationAccess and related name 'app_access'
    * ``meta`` <-> Meta through ApplicationMeta and related name 'app_meta'


**Condition**

    Conditions
    
    ** Attributes **
    
    * ``id``:AutoField : Primary key
    * ``name``:CharField(30) : Condition name
    * ``condition``:CharField(255)
    
    ** Relationships **     


**CoreParam**

    Parameters
    
    You would place tables (key->value) in choices module inside your application for tables that will not change often. When you
    have data that will change frequently, you can user this model to record parameters, lookup tables (like choices) and any other
    parametric information you may require.
    
    You can do:
    
    MY_FIRST_PARAM = 67 by inserting name='MY_FIRST_PARAM', value='67', paramType='integer'
    
    Country
    ||name||value||
    ||es||spain||
    ||us||United States||
    
    by...
    mode='COUNTRY', name='es', value='Spain', paramType='string'
    mode='COUNTRY', name='us', value='United States', paramType='string'
    
    **Attributes**
    
    * ``id`` : Primary key
    * ``mode``:CharField(20) : Parameter mode. This field allows you to group parameter to build lookup tables like the ones found in combo boxes (select boxes) with name->value pairs.
    * ``name``:CharField(20) : Parameter name
    * ``value``:CharField(100) : Parameter value
    * ``paramType``:CharField(10) : Parameter type, as Choices.PARAM_TYPE . Choices are string, integer, date.
    
    **Relationships**


**MetaKey**

    Model to store the keys allowed for meta values
    
    **Attributes**
    
    * ``id``:AutoField : Primary key
    * ``name``:CharField(20) : Key META name
    
    **Relationships**
    
    * ``keyType`` -> CoreParam : Foreign key to CoreParam having mode='META_TYPE'    


**Menu**

    **Attributes**
    
    * ``id``:AutoField : Primary Key
    * ``name``:CharField(20) : Menu item name
    * ``titleShort``:CharField(15) : Title short. Text shown in icon. Default menu shows this text right to the icon image.
    * ``title``:CharField(30) : Title shown in tooptip when mouse goes over.
    * ``url``:URLField : Url to launch . Used for external urls mapped to menu items.
    * ``urlTarget``:CharField(10) : target to launch url
    * ``language``:CharField(2) : Language code, like ``es``, ``en``, etc...
    * ``country``:CharField(2) : Country as Choices.COUNTRY
    * ``device``:CharField(10) : Device. Smartphones, tablets can have their own menu, customized to screen width
    
    **Relationships**
    
    * ``application`` -> Application
    * ``icon`` -> CoreParam
    * ``view`` -> View
    * ``action`` -> Action
    * ``params`` <-> Param through MenuParam with related name 'menu_params'


**Params**

    Parameters for WF and Views
    
    **Attributes**
    
    * ``id``:AutoField : Primary Key
    * ``name``:CharField(15)
    * ``title``:CharField(30)
    * ``paramType``:CharField(10) : As Choices.BASIC_TYPES
    * ``isView``:BooleanField
    * ``isWorkflow``:BooleanField
    
    **Relationships**
    
    * ``application`` -> Application
    

**Service**

    **Attributes**
    
    * ``id``
    * ``name``
    * ``implementation``
    
    **Relationships**
    
    * ``application``


**Setting**

    Settings model
    
    **Attributes**
    
    * ``value``:TextField : Settings value.
    * ``description``:CharField(255) : Setting description.
    * ``mustAutoload``:BooleanField : Has to load settings on cache?
    
    **Relationships**
    
    * ``name`` -> MetaKey : Foreign key to MetaKey model.


**View**

    View. Pages in ximpia are called views. Views render content obtaine from database or other APIs. They hit the slave databases. In
    case writing content is needed, could be accomplished by calling queues. Views can show lists, record detalils in forms, reports,
    static content, etc... 
    
    In case no logic is needed by view, simply include ``pass`` in the service operation.
    
    Views have name to be used internally in component registering and code and slug which is the name used in urls.
    
    View implementation is the path to the service operation that will produce view JSON data to server the frontend. Implementation
    is built by registering a view component.
    
    Window types can be 'window', 'popup' and 'panel' (this one coming soon). Windows render full width, popups are modal windows, and
    panels are tooltip areas inside your content. Popups can be triggered using icons, buttons or any other action. Panels will be
    triggered by mouse over components, clicking on visual action components.
    
    In case view needs authentication to render, would have hasAuth = True.
    
    Views can be grouped together using the ``parent`` field.
    
    Params are entry parameters (dynamic or static) that view will accept. Parameters are inyected to service operations with args 
    variable. The parameter name you include will be called by args['MY_PARAM'] in case your parameter name is 'MY_PARAM'.
    
    **Attributes**
    
    * ``id``:AutoField : Primary Key
    * ``name``:CharField(30)
    * ``implementation``:CharField(100)
    * ``winType``:CharField(20) : Window type, as Choices.WIN_TYPE_WINDOW
    * ``slug``:SlugField(50) : View slug to form url to call view
    * ``hasAuth``:BooleanField : Needs view authentication?
    * ``image``:FileBrowserField : View image
    
    **Relationships**
    
    * ``parent`` -> self
    * ``application`` -> Application
    * ``service`` -> Service
    * ``category`` -> xpsite.Category
    * ``templates`` <-> XpTemplate through ViewTmpl with related name `view_templates`
    * ``params`` <-> Param through ViewParamValue with related nam 'view_params'
    * ``menus`` <-> Menu through ViewMenu with related name 'view_menus'
    * ``tags`` <-> xpsite.Tag through ViewTag
    * ``accessGroups`` <-> xpsite.Group through ViewAccessGroup


**XpTemplate**

    Ximpia Template.
    
    Views can have N templates with language, country and device target features. You can target templates with device and localization.
    In case you want to provide different templates for user groups, profiles, etc... you would need to create different views and then
    map those views to access groups. Each of those views would have default templates and templates targetted at pads, smartphones,
    desktop and localization if required.
    
    Templates can window types:
    
    * Window - Views which render whole available screen area.
    * Popup - Modal views that popup when user clicks on actions or menu items.
    * Panel (Coming soon) - This window types is embedded within content, as a tooltip when user clicks on action or mouse goes over
    
    **Attributes**
    
    * ``id``:AutoField : Primary Key
    * ``name``:CharField(50)
    * ``alias``:CharField(20)
    * ``language``:CharField(2) : As Choices.LANG
    * ``country``:CharField(2) : As Choices.COUNTRY
    * ``winType``:CharField(20) : As Choices.WIN_TYPES
    * ``device``:CharField(10) : As Choices.DEVICES : Desktop computer, smartphones and tablets
    
    **Relationships**
    
    * ``application`` -> Application 

**Workflow**

    Ximpia comes with a basic application workflow to provide navigation for your views.
    
    Navigation is provided in window and popup window types.
    
    You "mark" as workflow view any service method with flow code (decorator). Actions are also "marked" as worflow actions with
    decorators.
    
    When actions are triggered by clicking on a button or similar, action logic is executed, and user displays view based on flow
    information and data inserted in the flow by actions. You do not have to map navigation inside your service operations.
    
    Plugging in a new view is pretty simple. You code the service view operation, include it in your flow, and view (window or popup)
    will be displayed when requirements are met 
    
    **Attributes**
    
    * ``id``:AutoField : Primary Key
    * ``code``:CharField(15) : Flow code
    * ``resetStart``:BooleanField : The flow data will be deleted when user displays first view of flow. The flow will be reset when user visits again any page in the flow.
    * ``deleteOnEnd``:BooleanField : Flow data is deleted when user gets to final view in the flow.
    * ``jumpToView``:BooleanField : When user visits first view in the flow, will get redirected to last visited view in the flow. User jumps to last view in the flow.
    
    **Relationships**
    
    * ``application`` -> Application

**WorkflowView**

    WorkFlow View. Relationship between flows and your views.
    
    Source view triggers action, logic is executed and target view is displayed to user.
    
    **Attributes**
    
    * ``id``:AutoField : Primary Key
    * ``order``:IntegerField : View orderi flow. You can place order like 10, 20, 30 for views in our flow. And then later inyect views between those values, like 15, for example.
    
    **Relationships**
    
    * ``flow`` -> WorkFlow
    * ``viewSource`` -> View : Source view for flow
    * ``viewTarget`` -> View : Target view for flow
    * ``action`` -> Action : Action mapped to flow. Source view triggers action, logic is executed and target view is rendered and displayed.
    * ``params`` <-> Param through WFParamValue with related name 'flowView_params'

**WorkflowData**

    User Workflow Data
    
    userId is the workflow user id. Flows support authenticated users and anonymous users. When flows start, in case not authenticated,
    workflow user id is generated. This feature allows having a flow starting at non-authenticated views and ending in authenticated 
    views, as well as non-auth flows.
    
    **Attributes**
    
    * ``id``:AutoField : Primary Key
    * ``userId``:CharField(40) : Workflow user id
    * ``data``:TextField : Workflow data encoded in json and base64
    
    **Relationships**
    
    * ``flow`` -> Workflow
    * ``view`` -> View
