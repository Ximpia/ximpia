Visual Components (24)
======================

Common Attributes
-----------------

* ``class`` : Will add all classes in this field
* ``tabindex`` : Will include tabindex support for entry fields with sequence when hitting tab key.
* ``readonly`` : Component will be read-only.
* ``maxlength`` : Maximum length for entry components.
* ``value`` : Value.
* ``name`` : Name of component


Button
------

Check
-----

.. image:: ../images/check-vertical.png

.. image:: ../images/check-horizontal.png

.. image:: ../images/check-block-vertical.png

.. image:: ../images/check-block-horizontal.png

List of options with ``checkbox`` render. Allows horizontal or vertical render of list of entries. Checkbox can
be placed before or after the field entry and labels can be at top or left.

HTML
""""

.. code-block:: html

    <div id="id_mycheck_comp" data-xp-type="check" data-xp="{alignment: 'vertical'}" > </div>

Attributes
""""""""""

* ``label`` : Label
* ``size`` : Input box size
* ``helpText`` : Tooltip to show
* ``info`` : Weather to show tooltip.
* ``labelWidth`` : Width for label
* ``alignment`` [optional] : 'vertical', 'horizontal'
* ``hasLabel`` [optional] : "true" or "false". Weather to show or not a label, at left or top of check controls.
* ``labelPosition`` [optional] : 'top'|'left'. Label position, left of check buttons, or top for label at one line and check
                                 controls on a new line.
* ``controlPosition`` [optional] : 'before'|'after'. Default: 'before'. Position for the check control, after or before text.

Interfaces
""""""""""

* ``IInputList`` : Interface for list of entries

Methods
"""""""

* ``render`` : Render
* ``enable`` : Enable
* ``disable`` : Disable
* ``unrender`` : Reset


Container
---------


Content
-------

ContextMenu
-----------

Field
-----

.. image:: ../images/field.png

Field with formatting option and tooltip with ``helpText`` attribute. Option to provide auto-complete
from choices or server-side data.

HTML
""""

.. code-block:: html

    <div id="id_countryTxt_comp"    data-xp-type="field"    
                                    data-xp="{  label: 'Country Code', size: 2}" 
                                    data-xp-complete="{     choicesId: 'country', 
                                                            choiceDisplay: 'name',
                                                            minCharacters: 1    }"> </div>

Attributes
""""""""""

* ``label`` : Label
* ``size`` : Input box size
* ``helpText`` : Tooltip to show
* ``info`` : Weather to show tooltip.
* ``labelWidth`` : Width for label

Attributes for auto-completion choices
""""""""""""""""""""""""""""""""""""""

* ``choicesId`` : Choices id to reference to show list.
* ``choiceDisplay`` [optional] default:value : name|value. Display either name or value from choices.
* ``maxHeight`` [optional] : Max height of autocomplete box
* ``minCharacters`` [optional] : Min characters to trigger auto-complete box.

Attributes for auto-completion server-side
""""""""""""""""""""""""""""""""""""""""""

* ``app`` [optional] : Application code
* ``dbClass`` : Data class to show results from.
* ``searchField`` :String : Search field to match for text from input field.
* ``maxHeight`` [optional] : Max height of autocomplete box
* ``minCharacters`` [optional] : Min characters to trigger auto-complete box.
* ``params`` [optional] :Object : Parameters to filter completion list.
* ``fieldValue`` [optional] :String : Field to show results. In case not defined, will use the model string representation.
* ``extraFields`` [optional] :List : Fields to show in extra Object

methods
"""""""

* ``render`` : Renders the component
* ``complete`` : Bind autocomplete behavior
* ``enable`` : Enable field
* ``disable`` : Disable field
* ``unrender`` : Reset (remove) component data and remove ``data-xp-render`` attribute.


FieldCheck
----------

.. image:: ../images/field-check.png

Renders fields that are BooleanField, with values true / false or 1 for true and 0 for false

Support labels. Check control can be before label or after.

HTML
""""

.. code-block:: html

    <div id="id_hasUrl_comp" data-xp-type="field.check" data-xp="{}" > </div>

The above code will just show a checkbox with True/False logic. You can include label as well.

This case would show checkbox and a message after the box to agree to terms and conditions in a web site:

.. code-block:: html

    <div id="id_agree_comp" data-xp-type="field.check" 
                            data-xp="{  label: 'I agree to terms and conditions',
                                        controlPosition: 'before'}" > </div>

Attributes
""""""""""

* ``label`` [optional] : Label
* ``helpText`` [optional] : Tooltip to show at label
* ``info`` [optional] : Weather to show tooltip at label.
* ``labelWidth`` [optional] : Width for label
* ``controlPosition`` [optional] : 'before'|'after'. Default: 'before'. Position for the radio control, after or before text.

Interfaces
""""""""""

* ``IInputField`` 

Methods
"""""""

* ``render`` : Render
* ``enable`` : Enable
* ``disable`` : Disable
* ``unrender`` : Reset

FieldDateTime
-------------

.. image:: ../images/field-date.png

* Date and Time field representation. This component renders form fields Date, DateTime and Time.

* When field type is Date, a date tooltip will popup to select date.

* When field type is Time, a time tooltip will popup to select time with two selection bars for hour and minute.

* When field type is DateTime, a date with time tooltip will show up with calendar and time bars.

HTML
""""

.. code-block:: html

    <div id="id_updateDate_comp" data-xp-type="field.datetime" data-xp="{}"> </div>

Type can be ``field.datetime``, ``field.date`` or ``field.time``.

Attributes
""""""""""

* ``label`` [optional] : Label
* ``helpText`` [optional] : Tooltip to show at label
* ``info`` [optional] : Weather to show tooltip at label.
* ``labelWidth`` [optional] : Width for label
* ``hasLabel`` [optional]
* ``labelPosition`` [optional]

FieldList
---------

.. image:: ../images/field-list-input.png

.. image:: ../images/field-list-select.png

List of fields. Fields can be added and deleted. Can represent the many-to-many relationships in models. 
 
They can be rendered as tags horizontally.

HTML
""""

Input: 

.. code-block:: html

    <div id="id_meta_comp"  data-xp-type="field.list" 
                        data-xp="{  type: 'field', 
                                    labelWidth: '100px', 
                                    modelField: 'meta__name'}"
                        data-xp-complete="{ choicesId: 'metaKey', 
                                            minCharacters: 1  }" > </div>

Select:

.. code-block:: html

    <div id="id_meta_comp" data-xp-type="field.list" 
                data-xp="{  type: 'select.plus', 
                            selectObjId: 'id_metaKey_comp',
                            labelWidth: '100px', 
                            choicesId: 'meta'}" > </div>


Attributes
""""""""""

* ``type``:string [default: field] [optional] : Type of control for adding values: ``field`` and ``select.plus`` possible values.
* ``labelWidth``:string [optional]
* ``selectObjId``:string [optional]
* ``modelField``:string [optiona] : For field input type, the model field value. Required for fields. Not required for select input.
* ``choicesId``

Interfaces
""""""""""

* ``IInputList``
* ``IKeyInput``

Methods
"""""""

* ``render`` : Render.
* ``keypress`` : Deals with ``Enter`` key stroke and adding clicked to list of entries.
* ``enable`` : Enable
* ``disable`` : Disable
* ``unrender`` : Reset


FieldNumber
-----------

.. image:: ../images/field.number.png

HTML
""""

.. code-block:: html

    <div id="id_number_comp" data-xp-type="field.number" 
                            data-xp="{  size: 2, 
                                        labelWidth: '100px', 
                                        info: true, 
                                        helpText: 'Number of invitations'}" ></div>

Attributes
""""""""""

* ``label`` : Label
* ``size`` : Input box size
* ``helpText`` : Tooltip to show
* ``info`` : Weather to show tooltip.
* ``labelWidth`` : Width for label
* ``hideSpinner`` :Boolean : Hides spinner control

Interfaces
""""""""""

* ``IInputField``

Methods
"""""""

* ``render`` : Render
* ``enable`` : Enable
* ``disable`` : Disable
* ``unrender`` : Reset

Function
--------

Icon
----

Link
----

ListContent
-----------

ListData
--------

Image
-----

Option
------

.. image:: ../images/option-horizontal.png

.. image:: ../images/option-block-horizontal.png

.. image:: ../images/option-block-vertical.png

You can have options integrated into ``fieldset`` html element or having labels. You have the option of horizontal or vertical
layout with labels on left or top.

In case you select ``type: 'check'`` you would see a list of checkboxes. But they will behave like options, only one can be checked.
This has advantage that no entries can be checked by default and you can check uncheck the last option if you wish, having feature
to reset the option list.

HTML
""""

.. code-block:: html

    <div id="id_status_comp" data-xp-type="option" 
                            data-xp="{  labelWidth: '100px', 
                                        hasLabel: true, 
                                        info: true, 
                                        helpText: 'Invitation status'}" > </div>


Attributes
""""""""""

* ``type`` : 'radio', 'check' default 'radio'
* ``alignment`` [optional] : 'vertical', 'horizontal'. Default. horizontal.
* ``hasLabel`` [optional] : "true"|"false". Weather to show or not a label, at left or top of radio controls.
* ``label`` [optional] : Field label
* ``labelPosition`` [optional] : 'top'|'left'. Label position, left of radio buttons, or top for label at one line and radio
                                  controls on a new line. Default ``left``
* ``controlPosition`` [optional] : 'before'|'after'. Default: 'before'. Position for the radio control, after or before text.
* ``info`` [optional] : Displays tooltip with helpText field data.

Interfaces
""""""""""

* ``IInputList``

Types
"""""
* ``radio`` : radio option box
* ``checkbox`` : check box. Behaved like option, when user clicks on one, it gets selected. Ability to have no option cheched. Good for many relationships with null=true.

Methods
"""""""

* ``render``
* ``disable``
* ``enable``


PagingBullet
------------

PagingMore
----------

PopUp
-----

Select
------

.. image:: ../images/select.png

HTML
""""

.. code-block:: html

    <div id="id_status_comp" data-xp-type="select" 
                                data-xp="{  labelWidth: '100px', 
                                            info: true, 
                                            helpText: 'Invitation status'}" > </div>

Attributes
""""""""""

* ``label`` : Label
* ``size`` : Input box size
* ``helpText`` : Tooltip to show
* ``info`` : Weather to show tooltip.
* ``labelWidth`` : Width for label

Interfaces
""""""""""

* ``IInputField``

Methods
"""""""

* ``render``
* ``disable``
* ``enable``
* ``unrender``


SelectPlus
----------

.. image:: ../images/combo.plus.png

.. image:: ../images/select.plus-open.png

HTML
""""

.. code-block:: html

    <div id="id_fromUser_comp" data-xp-type="select.plus" 
                            data-xp="{  labelWidth: '100px', 
                                        info: true, 
                                        label: 'Sent by', 
                                        helpText: 'User that sent invitation'}" > </div>

Choices from server-side form field is used by default. You may include field attribute ``choicesId`` in the properties
to modify defult value.

As you type text, auto-complete will drop under to help you on selection. For cases withmany entries you will have paging
support on entry list to browse on different pages of results, very handy for big lists.

When you have ``hasBestMatch`` the best match is highligted and selected in the input box. So when you start typing in a country
list "Spa", when best match is Spain will automatically get selected in the text box.

Attributes
""""""""""

* ``label`` : Label
* ``size`` : Input box size
* ``helpText`` : Tooltip to show
* ``info`` : Weather to show tooltip.
* ``labelWidth`` : Width for label
* ``hasBestMatch`` :String : Highlight best match relative to field text. Default true.
* ``gmaps`` : Google maps association, like 'country'. Used for list of countries. Google maps library will set country based on location.
* ``choicesId`` : Id for choice list.

Interfaces
""""""""""

* ``IInputField``

Methods
"""""""

* ``render``
* ``setValue`` : Sets value in selection box
* ``disable``
* ``enable``
* ``unrender``


TextArea
--------

.. image:: ../images/textarea.png

When you set ``isCollapsible: true``, as you type and get to end of row, a new row will be added to text area. This way you
don't need to size text box and size adapts to size user needs to write. You may start with one or two lines, and as users type,
end up with more lines.

HTML
""""

.. code-block:: html

    <div id="id_message_comp" data-xp-type="textarea" 
                                data-xp="{  labelWidth: '100px', 
                                            cols:50, 
                                            rows:1, 
                                            isCollapsible: true, 
                                            info: true, 
                                            helpText: 'Invitation message'}" > </div>

Attibutes
"""""""""

* ``label`` : Label
* ``size`` : Input box size
* ``helpText`` : Tooltip to show
* ``info`` : Weather to show tooltip.
* ``labelWidth`` : Width for label
* ``cols``
* ``rows``
* ``isCollapsible``

Interfaces
""""""""""

* ``IInputField``

Methods
"""""""

* ``render``
* ``disable``
* ``enable``
* ``unrender``
