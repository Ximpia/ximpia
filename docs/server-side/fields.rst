
.. |br| raw:: html
    
    <br />

Fields
======

Introduction
------------

Ximpia form provide a map with data sources and visual objects in templates. Forms are built from fields
and an additional clean method to provide advanced validations. 

Fields have:

* model instance
* model field name
* additional attributes like choices, required, min length, etc...

Forms are serialized in **JSON** format and rendered in visual engine. Any rendered object will have a form or a field inside
a form, weather or not those objects are rendered as fields that user enter data.

For example, a view to display detail for a customer could have a set of fields in a forms and only show display option for those
fields, therefore will never be a box to input text.

Some attributes like ``helpText`` can be informed in form fields or in visual components in templates. Values entered in templates
would overide values found in form fields.

.. code-block:: python

    class UserSignupInvitationForm(XBaseForm):
        _XP_FORM_ID = 'signup'
        # Instances 
        _dbUser = User()
        _dbUserChannel = UserChannel()
        _dbAddress = Address()
        _dbInvitation = Invitation()
        # Fields
        username = UserField(_dbUser, 'username', label='XimpiaId')
        password = PasswordField(_dbUser, 'password', minLength=6, required=False, jsRequired=False,  
            helpText = _('Must provide a good or strong password to signup. Allowed characters are letters, numbers and _ | . | $ | % | &'))
        passwordVerify = PasswordField(_dbUser, 'password', minLength=6, required=False, jsVal=["{equalTo: '#id_password'}"], 
                                    jsRequired=False, label= _('Password Verify'))
        email = EmailField(_dbInvitation, 'email', label='Email')
        firstName = CharField(_dbUser, 'first_name')
        lastName = CharField(_dbUser, 'last_name', required=False)
        city = CharField(_dbAddress, 'city', required=False)
        country = OneListField(_dbAddress, 'country', choicesId='country', required=False, choices=Choices.COUNTRY)
        invitationCode = CharField(_dbInvitation, 'invitationCode', required=False, jsRequired=True)
        authSource = HiddenField(initial=K.PASSWORD)
        socialId = HiddenField()
        socialToken = HiddenField()
        # Navigation and Message Fields
        params = HiddenField(initial=_jsf.encodeDict({
                                        'profiles': '', 
                                        'userGroup': K.SIGNUP_USER_GROUP_ID,
                                        'affiliateId': -1}))
        choices = HiddenField(initial=_jsf.encodeDict( {'country': Choices.COUNTRY } ) )
        errorMessages = HiddenField(initial=_jsf.buildMsgArray([_m,
                                            ['ERR_ximpia_id', 'ERR_email', 'ERR_social_id_exists']]))
        okMessages = HiddenField(initial=_jsf.buildMsgArray([_m, ['OK_USER_SIGNUP','OK_SOCIAL_SIGNUP']]))
    
        def clean(self):
            """Clean form: validate same password and captcha when implemented"""
            if self._get_field_value('authSource') == K.PASSWORD:
                self._validate_same_fields([('password','passwordVerify')])
            self._xp_clean()
            return self.cleaned_data


* :ref:`fields.field`
* :ref:`fields.booleanfield`
* :ref:`fields.charfield`
* :ref:`fields.datefield`
* :ref:`fields.datetimefield`
* :ref:`fields.decimalfield`
* :ref:`fields.emailfield`
* :ref:`fields.filebrowsefield`
* :ref:`fields.floatfield`
* :ref:`fields.genericipaddressfield`
* :ref:`fields.hiddenfield`
* :ref:`fields.integerfield`
* :ref:`fields.manylistfield`
* :ref:`fields.onelistfield`
* :ref:`fields.passwordfield`
* :ref:`fields.timefield`
* :ref:`fields.userfield`

.. _fields.field:

Field
"""""

        Common field form class. Extends django field.
        
        **Required Arguments**
        
        * ``instance``
        * ``insField``
        
        **Optional Arguments**
        
        * ``required``:bool [None] : Field is required by back-end
        * ``jsRequired``:bool [None] : Field is required by front-end
        * ``jsVal``:bool [None] : Javascript validation
        * ``label``:str [None] : Field label
        * ``initial``:str [None] : Field initial value
        * ``helpText``:str [None] : Field tooltip
        * ``errorMessages``:dict [None] : Error messages in dict format
        * ``validators``:list [[]] : List of validators     

.. _fields.booleanfield:

BooleanField
""""""""""""

    Boolean field. This field can be rendered into any visual component: checkbox, selection box, etc... The most common use is to
    render into a checkbox.
    
    Example:
    
    isOrdered = BooleanField(_dbUserOrder, 'isOrdered')
    
    where _dbUserOrder is a form class attribute with the model instance, ``_dbUserOrder = UserOrder()``
    
    **Required Arguments**

    * ``instance``:object : Model instance
    * ``insField``:str : Model field
    
    **Optional Arguments**
    
    * ``required``:bool : Required field by back-end form valdiation
    * ``initial``:str : Initial value
    * ``jsRequired``:str    : Required field by javascript validation
    * ``label``:str : Field label
    * ``helpText``:str : Field tooptip
    
    **Attributes**
    
    * ``instance``:object
    * ``instanceFieldName``:str
    * ``required``:bool
    * ``initial``:str
    * ``jsRequired``:bool
    * ``label``:str
    * ``helpText``:str

.. _fields.charfield:

CharField
"""""""""

    Char field.
    
    Example:
    
    firstName = CharField(_dbUser, 'first_name')
    
    where _dbUser is a form class attribute with the model instance, ``_dbUser = User()``
    
    **Required Arguments**
    
    * ``instance``:object : Model instance
    * ``insField``:str : Model field
    
    **Optional Arguments**
    
    * ``minLength``:int : Field minimum length
    * ``maxLength``:int : Field maximum length
    * ``required``:bool : Required field by back-end form valdiation
    * ``initial``:str : Initial value
    * ``jsRequired``:str    : Required field by javascript validation
    * ``label``:str : Field label
    * ``helpText``:str : Field tooptip
    
    **Attributes**
    
    * ``instance``:object
    * ``instanceFieldName``:str
    * ``minLength``:str
    * ``maxLength``:str
    * ``required``:bool
    * ``initial``:str
    * ``jsRequired``:bool
    * ``label``:str
    * ``helpText``:str

.. _fields.datefield:

DateField
"""""""""

    Example:        
    
    where _dbModel is a form class attribute with the model instance.
    
    **Input Formats**
    
    A list of formats used to attempt to convert a string to a valid datetime.date object.

    If no input_formats argument is provided, the default input formats are:

    '%Y-%m-%d',       # '2006-10-25'|br|
    '%m/%d/%Y',       # '10/25/2006'|br|
    '%m/%d/%y',       # '10/25/06'|br|
    
    Additionally, if you specify USE_L10N=False in your settings, the following will also be included in the default input formats:

    '%b %d %Y',       # 'Oct 25 2006'|br|
    '%b %d, %Y',      # 'Oct 25, 2006'|br|
    '%d %b %Y',       # '25 Oct 2006'|br|
    '%d %b, %Y',      # '25 Oct, 2006'|br|
    '%B %d %Y',       # 'October 25 2006'|br|
    '%B %d, %Y',      # 'October 25, 2006'|br|
    '%d %B %Y',       # '25 October 2006'|br|
    '%d %B, %Y',      # '25 October, 2006'|br|
    
    **Required Arguments**

    * ``instance``:object : Model instance
    * ``insField``:str : Model field
    
    **Optional Arguments**
    
    * ``inputFormats``:list : Input formats
    * ``required``:bool : Required field by back-end form valdiation
    * ``initial``:str : Initial value
    * ``jsRequired``:str    : Required field by javascript validation
    * ``label``:str : Field label
    * ``helpText``:str : Field tooptip
    
    **Attributes**
    
    * ``instance``:object
    * ``instanceFieldName``:str
    * ``required``:bool
    * ``initial``:str
    * ``jsRequired``:bool
    * ``label``:str
    * ``helpText``:str


.. _fields.datetimefield:

DateTimeField
"""""""""""""

    Example:    
    
    where _dbModel is a form class attribute with the model instance.
    
    **Input Formats**
    
    A list of formats used to attempt to convert a string to a valid datetime.date object.

    If no input_formats argument is provided, the default input formats are:

    '%Y-%m-%d %H:%M:%S',     # '2006-10-25 14:30:59'|br|
    '%Y-%m-%d %H:%M',        # '2006-10-25 14:30'|br|
    '%Y-%m-%d',              # '2006-10-25'|br|
    '%m/%d/%Y %H:%M:%S',     # '10/25/2006 14:30:59'|br|
    '%m/%d/%Y %H:%M',        # '10/25/2006 14:30'|br|
    '%m/%d/%Y',              # '10/25/2006'|br|
    '%m/%d/%y %H:%M:%S',     # '10/25/06 14:30:59'|br|
    '%m/%d/%y %H:%M',        # '10/25/06 14:30'|br|
    '%m/%d/%y',              # '10/25/06'|br|
        
    **Required Arguments**

    * ``instance``:object : Model instance
    * ``insField``:str : Model field
    
    **Optional Arguments**
    
    * ``inputFormats``:list : Input formats
    * ``required``:bool : Required field by back-end form valdiation
    * ``initial``:str : Initial value
    * ``jsRequired``:str    : Required field by javascript validation
    * ``label``:str : Field label
    * ``helpText``:str : Field tooptip
    
    **Attributes**
    
    * ``instance``:object
    * ``instanceFieldName``:str
    * ``required``:bool
    * ``initial``:str
    * ``jsRequired``:bool
    * ``label``:str
    * ``helpText``:str

.. _fields.decimalfield:

DecimalField
""""""""""""

    Decimal field with support for maxValue, minValue, maxDigits and decimalPlaces
    
    Example:
    
    amount = DecimalField(_dbModel, 'field', maxValue=9800, minValue=100, maxDigits=4, decimalPlaces=2)
    
    where _dbModel is a form class attribute with the model instance.
    
    **Required Arguments**

    * ``instance``:object : Model instance
    * ``insField``:str : Model field
    
    **Optional Arguments**
    
    * ``maxValue``:decimal.Decimal : Maximum value
    * ``minValue``:decimal.Decimal : Minimum value
    * ``maxDigits``:int : Maximum number of digits (before decimal point plus after decimal point)
    * ``decimalPlaces``:int : Number of decimal places
    * ``required``:bool : Required field by back-end form valdiation
    * ``initial``:str : Initial value
    * ``jsRequired``:str    : Required field by javascript validation
    * ``label``:str : Field label
    * ``helpText``:str : Field tooptip
    
    **Attributes**
    
    * ``instance``:object
    * ``instanceFieldName``:str
    * ``required``:bool
    * ``initial``:str
    * ``jsRequired``:bool
    * ``label``:str
    * ``helpText``:str

.. _fields.emailfield:

EmailField
""""""""""

    Email field. Validates email address    
    
    **Required Arguments**
    
    * ``instance``:object : Model instance
    * ``insField``:str : Model field
    
    **Optional Arguments**
    
    * ``minLength``:int : Field minimum length
    * ``maxLength``:int : Field maximum length
    * ``required``:bool : Required field by back-end form valdiation
    * ``initial``:str : Initial value
    * ``jsRequired``:str    : Required field by javascript validation
    * ``label``:str : Field label
    * ``helpText``:str : Field tooptip
    
    **Attributes**
    
    * ``instance``:object
    * ``instanceFieldName``:str
    * ``minLength``:str
    * ``maxLength``:str
    * ``required``:bool
    * ``initial``:str
    * ``jsRequired``:bool
    * ``label``:str
    * ``helpText``:str

.. _fields.filebrowsefield:

FileBrowseField
"""""""""""""""

    File browser form field.
    
    We keep additional attributes for visual component into ``data-xp`` html attribute:
    
    * ``site`` : Site to search for files.
    * ``directory`` : Directory to search for files.
    * ``extensions`` : File extensions to search for files.
    * ``fieldFormats`` : File formats to search for.
    
    These attributes are used to search for files when search icon in file browser field is clicked.
    
    In case these attributes are None, files will be searched in default media home with all extensions and file formats.
    
    **Required Arguments**

    * ``instance``:object : Model instance
    * ``insField``:str : Model field    

    
    **Optional Arguments**
    
    * ``site``:str : Site that keeps media files
    * ``directory``:str : Directory that keeps media files
    * ``extensions``:list : Extensions
    * ``fieldFormat``:list : Field formats
    
    **Attributes**
    
    * ``instance``:object
    * ``instanceFieldName``:str
    * ``minLength``:str
    * ``maxLength``:str
    * ``required``:bool
    * ``initial``:str
    * ``jsRequired``:bool
    * ``label``:str
    * ``helpText``:str
    * ``site``:str : Site that keeps media files
    * ``directory``:str : Directory that keeps media files
    * ``extensions``:list : Extensions
    * ``fieldFormat``:list : Field formats

.. _fields.floatfield:

FloatField
""""""""""

    Integer field with maxValue and minValue
    
    Example:
    
    number = FloatField(_dbModel, 'field', maxValue=9800, minValue=100)
    
    where _dbModel is a form class attribute with the model instance.
    
    **Required Arguments**

    * ``instance``:object : Model instance
    * ``insField``:str : Model field
    
    **Optional Arguments**
    
    * ``maxValue``:decimal.Decimal : Maximum value
    * ``minValue``:decimal.Decimal : Minimum value
    * ``required``:bool : Required field by back-end form valdiation
    * ``initial``:str : Initial value
    * ``jsRequired``:str    : Required field by javascript validation
    * ``label``:str : Field label
    * ``helpText``:str : Field tooptip
    
    **Attributes**
    
    * ``instance``:object
    * ``instanceFieldName``:str
    * ``required``:bool
    * ``initial``:str
    * ``jsRequired``:bool
    * ``label``:str
    * ``helpText``:str

.. _fields.genericipaddressfield:

GenericIPAddressField
"""""""""""""""""""""

    Generic IP Address field, IPv4 and IPv6
    
    Example:
    
    isOrdered = IPGenericAddressField(_dbModel, 'ip')
    
    where _dbModel is a form class attribute with the model instance.
    
    **Required Arguments**

    * ``instance``:object : Model instance
    * ``insField``:str : Model field
    
    **Optional Arguments**
    
    * ``protocol``:str ['both'] : Protocol, possible values: both|ipv4|ipv6
    * ``unpackIpv4``:bool [False]
    * ``required``:bool : Required field by back-end form valdiation
    * ``initial``:str : Initial value
    * ``jsRequired``:str    : Required field by javascript validation
    * ``label``:str : Field label
    * ``helpText``:str : Field tooptip
    
    **Attributes**
    
    * ``instance``:object
    * ``instanceFieldName``:str
    * ``required``:bool
    * ``initial``:str
    * ``jsRequired``:bool
    * ``label``:str
    * ``helpText``:str

.. _fields.hiddenfield:

HiddenField
"""""""""""

    Hidden Field, name and value.
    
    **Optional Arguments**
    
    * ``initial``:str : Initial value
    
    **Attributes**
    
    * ``initial``:str : Initial value

.. _fields.ipaddressfield:

IPAddressField
""""""""""""""

    Ip Address field, IPv4, like 255.255.255.0
    
    Example:
    
    isOrdered = IPAddressField(_dbModel, 'ip')
    
    where _dbModel is a form class attribute with the model instance.
    
    **Required Arguments**

    * ``instance``:object : Model instance
    * ``insField``:str : Model field
    
    **Optional Arguments**
    
    * ``required``:bool : Required field by back-end form valdiation
    * ``initial``:str : Initial value
    * ``jsRequired``:str    : Required field by javascript validation
    * ``label``:str : Field label
    * ``helpText``:str : Field tooptip
    
    **Attributes**
    
    * ``instance``:object
    * ``instanceFieldName``:str
    * ``required``:bool
    * ``initial``:str
    * ``jsRequired``:bool
    * ``label``:str
    * ``helpText``:str

.. _fields.integerfield:

IntegerField
""""""""""""

    Integer field with maxValue and minValue
    
    Example:
    
    number = IntegerField(_dbModel, 'field', maxValue=9800, minValue=100)
    
    where _dbModel is a form class attribute with the model instance.
    
    **Required Arguments**

    * ``instance``:object : Model instance
    * ``insField``:str : Model field
    
    **Optional Arguments**
    
    * ``maxValue``:decimal.Decimal : Maximum value
    * ``minValue``:decimal.Decimal : Minimum value
    * ``required``:bool : Required field by back-end form valdiation
    * ``initial``:str : Initial value
    * ``jsRequired``:str    : Required field by javascript validation
    * ``label``:str : Field label
    * ``helpText``:str : Field tooptip
    
    **Attributes**
    
    * ``instance``:object
    * ``instanceFieldName``:str
    * ``required``:bool
    * ``initial``:str
    * ``jsRequired``:bool
    * ``label``:str
    * ``helpText``:str

.. _fields.manylistfield:

ManyListField
"""""""""""""

    Selection with many possible values. Will render: select with multiple attribute, list of items with checkbox, other
    visual components with multiple values from a list.
    
    In case choices is not null, we attempt to skip many search for values and get values from choices object.
    
    From choices...
    country = ManyListField(_dbAddress, 'country', choicesId='country', required=False, choices=Choices.COUNTRY)
    
    From many relationship...
    country = ManyListField(_dbAddress, 'country', choicesId='country', required=False)
    
    **From Choices**
    
    You need to include arguments ``choicesId``, ``choices``.
    
    **From Many to Many relationship**
    
    You need to include arguments: ``choicesId``. Optional ``limitTo``, ``listName``and ``listValue``. In case these
    optional attributes not defined, will search without filter and name will be FK and value string representation of model instance.
    
    **Required Arguments**
    
    * ``instance``:object : Model instance
    * ``insField``:str : Model field, like '_myModel.fieldName'
    * ``choicesId``:str: Choice id to save into id_choices hidden field, like {myChoiceId: [(name1,value1),(name2,value2),...] ... }
    
    **Optional Arguments**
    
    * ``limitTo``:dict : Dictionary with attributes sent to model filter method
    * ``listValue``:str : Model field to be used for value in (name, value) pairs. By default, string notation of model used.
    * ``values``:tuple
    * ``orderBy``:tuple : Order by tuples, like ('field', '-field2'). field ascending and field2 descending.
    * ``choices``:list
    
    **Attributes**
    
    * ``instance``:object
    * ``instanceFieldName``:str
    * ``required``:bool
    * ``initial``:str
    * ``jsRequired``:bool
    * ``label``:str
    * ``helpText``:str
    * ``choicesId``:str
    * ``limitTo``:dict
    * ``orderBy``:tuple
    * ``values``:tuple
    * ``listValue``:str
    
    **Visual Component Attributes**
    
    Attributes inside attrs field attribute:
    
    * ``choicesId``
    * ``data-xp-val``
    * ``help_text``
    * ``class``
    * ``label``
        
    **Methods**
    
    * ``buildList()``:list<(name:str, value:str, data:dict)> : Build list of tuples (name, value) and data associated to values argument    

.. _fields.onelistfield:

OneListField
""""""""""""

    Select field. Will render to combobox, option lists, autocomplete, etc... when form instance is rendered, values are
    fetched from database to fill ``id_choices`` hidden field with data for field values.
    
    In case choices is not null, we attempt to skip foreign key search for values and get values from choices object.
    
    From choices...
    country = OneListField(_dbAddress, 'country', choicesId='country', required=False, choices=Choices.COUNTRY)
    
    From fk...
    country = OneListField(_dbAddress, 'country', choicesId='country', required=False)
    
    **From Choices**
    
    You need to include arguments ``choicesId``, ``choices``.
    
    **From Foreign Key**
    
    You need to include arguments: ``choicesId``. Optional ``limitTo``, ``orderBy`` and ``listValue``. In case these
    optional attributes not defined, will search without filter and name will be FK and value string representation of model instance.
    
    **Required Arguments**
    
    * ``instance``:object : Model instance
    * ``insField``:str : Model field, like '_myModel.fieldName'
    * ``choicesId``:str: Choice id to save into id_choices hidden field, like {myChoiceId: [(name1,value1),(name2,value2),...] ... }
    
    **Optional Arguments**
    
    * ``limitTo``:dict : Dictionary with attributes sent to model filter method
    * ``repr``:str : Model field to be used for value in (name, value) pairs. By default, string notation of model used.
    * ``values``:list : List of values to append to 'id_choices'
    * ``orderBy``:tuple : Order by tuples, like ('field', '-field2'). field ascending and field2 descending.
    * ``choices``:list
    
    **Attributes**
    
    * ``instance``:object
    * ``instanceFieldName``:str
    * ``required``:bool
    * ``initial``:str
    * ``jsRequired``:bool
    * ``label``:str
    * ``helpText``:str
    * ``choicesId``:str
    * ``limitTo``:dict
    * ``orderBy``:tuple
    * ``listValue``:str
    * ``values``:tuple
    
    **Visual Component Attributes**
    
    Attributes in attrs field attribute:
    
    * ``choicesId``
    * ``data-xp-val``
    * ``help_text``
    * ``class``
    * ``label``
    
    **Methods**
    
    * ``buildList()``:list<(name:str, value:str, data:dict)> : Build list of tuples (name, value) and data associated to values argument

.. _fields.passwordfield:

PasswordField
"""""""""""""

    Password field. Checks valid password
    
    **Required Arguments**
    
    * ``instance``:object : Model instance
    * ``insField``:str : Model field
    
    **Optional Arguments**
    
    * ``minLength``:int : Field minimum length
    * ``maxLength``:int : Field maximum length
    * ``required``:bool : Required field by back-end form valdiation
    * ``initial``:str : Initial value
    * ``jsRequired``:str    : Required field by javascript validation
    * ``label``:str : Field label
    * ``helpText``:str : Field tooptip
    
    **Attributes**
    
    * ``instance``:object
    * ``instanceFieldName``:str
    * ``minLength``:str
    * ``maxLength``:str
    * ``required``:bool
    * ``initial``:str
    * ``jsRequired``:bool
    * ``label``:str
    * ``helpText``:str

.. _fields.timefield:

TimeField
"""""""""

    Example:
    
    where _dbModel is a form class attribute with the model instance.
    
    **Input Formats**
    
    A list of formats used to attempt to convert a string to a valid datetime.date object.
    
    If no input_formats argument is provided, the default input formats are:

    '%H:%M:%S',     # '14:30:59'
    '%H:%M',        # '14:30'
    
    **Required Arguments**

    * ``instance``:object : Model instance
    * ``insField``:str : Model field
    
    **Optional Arguments**
    
    * ``inputFormats``:list : Input formats
    * ``required``:bool : Required field by back-end form valdiation
    * ``initial``:str : Initial value
    * ``jsRequired``:str    : Required field by javascript validation
    * ``label``:str : Field label
    * ``helpText``:str : Field tooptip
    
    **Attributes**
    
    * ``instance``:object
    * ``instanceFieldName``:str
    * ``required``:bool
    * ``initial``:str
    * ``jsRequired``:bool
    * ``label``:str
    * ``helpText``:str

.. _fields.userfield:

UserField
"""""""""

    User id field
    
    **Required Arguments**
    
    * ``instance``:object : Model instance
    * ``insField``:str : Model field
    
    **Optional Arguments**
    
    * ``minLength``:int : Field minimum length
    * ``maxLength``:int : Field maximum length
    * ``required``:bool : Required field by back-end form valdiation
    * ``initial``:str : Initial value
    * ``jsRequired``:str    : Required field by javascript validation
    * ``label``:str : Field label
    * ``helpText``:str : Field tooptip
    
    **Attributes**
    
    * ``instance``:object
    * ``instanceFieldName``:str
    * ``minLength``:str
    * ``maxLength``:str
    * ``required``:bool
    * ``initial``:str
    * ``jsRequired``:bool
    * ``label``:str
    * ``helpText``:str  
