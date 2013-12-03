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
* ``labelWidth``:number [optional]
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
* ``keypress`` : Deals with ``Enter``key stroke and adding clicked to list of entries.
* ``enable`` : Enable
* ``disable`` : Disable
* ``unrender`` : Reset


FieldNumber
-----------

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

Hidden
------

Image
-----

Option
------

PagingBullet
------------

PagingMore
----------

PopUp
-----

Select
------

SelectPlus
----------

TextArea
--------

