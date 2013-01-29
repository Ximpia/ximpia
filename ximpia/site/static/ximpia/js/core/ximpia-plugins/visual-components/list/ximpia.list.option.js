/*
 * 
 *
 * Ximpia Visual Component Option: Radio button with fields coming from choices
 * 
 * Foreign Keys???? How????
 * 
 * You can define in the form model instance and field. If no model instance defined, then it is a choice option field
 * if model and field defined, check that field is type foreign key, if no foreign key, then source is choices. Also check
 * form attributes choicesId, this is much easier!!!!
 * 
 * We need list of (name,value) pairs. Default: name is the id for the pk, value is string representation of foreign table
 * We can customize this, by attributes "listName" and "listValue" with model fields
 * 
 * we build id_choices_fk with list of (name, value) from form fields that require fk lookup tables: select boxes, option lists, etc...
 * when we instance form
 * 
 * choices is list of (name,value), choices_fk could be same, with choiceId -> [(name,value),()...]
 * 
 * definition:
 * 
 * choices_fk = XpHiddenField(xpType='input.hidden', required=False initial="[['$choiceId', '$model','$filter','$nameField',
 * 			'$valueField'],[]]") ????
 * 
 * ServiceDecorator will call queries with get list of fields in forms that require foreign key choices
 * 
 * Required information: choiceid, filter [opt], listName[opt], listValue[opt]
 * 
 * country = XpSelectField(_model, '_model.field', choiceId='countries', filter={}, listName='code', 
 * 			listValue='value') 
 * This field will allways link to foreign key for model
 * 
 * This select field will include in id_choices the (name, value) pairs, initial should be the model field value. 
 * 
 * Have a class Countries(FkChoice) ???
 * 
 * model.filter(**args)
 * 
 * 
 * 
 * Source: Should know source ????
 * 
 * ** HTML **
 * 
 * <div id="id_myoption_comp" data-xp-type="list.option" data-xp="{type: 'radio', alignment: 'vertical'}" > </div>
 * 
 * <div id="id_myoption_comp" data-xp-type="list.option" data-xp="{type: 'checkbox', alignment: 'vertical'}" > </div>
 * 
 * Your form should have ``myoption``field
 * 
 * ** Attributes (data-xp) **
 * 
 * * ``class`` [optional] : 'optVertical', 'optHorizontal'
 * * ``type`` : 'radio', 'checkbox'
 * * ``alignment`` [optional] : 'vertical', 'horizontal'
 * * ``source`` : 'choices' or 'fk' : Should know source????
 * * ``values`` : List of (name, value) pairs ... [['es','Spain'],['us','USA'], ... ]
 * 
 * 
 * ** Constraints ** 
 * 
 * ``class`` or ``alinment`` must be defined
 * 
 * You can include alignment or class for <ul> element which holds the input elements. If you include horizontal or vertical alignment
 * you don't need the class attribute. When horizontal is defined, we use css class ``optHorizontal``. When vertical is defined, we
 * use ``optVerical`` css class.
 * 
 * ** Interfaces **
 * 
 * This components implements these interfaces:
 * 
 * * ``IList``
 *  
 * 
 * ** Methods **
 * 
 * * ``render``
 * * ``click``
 * * ``disable``
 * * ``enable``
 * * ``disableItem``
 * * ``enableItem``
 * 
 * Types
 * radio: radio option box
 * checkbox: check box. Behaved like option, when user clicks on one, it gets selected. Ability to have no option cheched.
 * 
 * We need here support for choices and foreign keys in tables
 * 
 * Conditions??? Conditions could trigger clicks, disable / enable items, render / disble entire list
 * Triggers??? Any?? Clicks
 * 
 *
 */

(function($) {	

	$.fn.xpObjListOption = function( method ) {  

        // Settings		
        var settings = {
        	/*excudeListSelect: ['type','id','element','help_text','label','data-xp-val', 'value', 'choices','choicesId'],
        	excludeListLabel: ['type','id','element'],
        	excludeList: ['info','type','left'],
        	htmlAttrs: ['tabindex','value','name'],
        	djangoAttrs: ['type','id','info','help_text','label','element','left','xptype','choices'],
        	formData: {}*/
        };
		
        var methods = {
		init : function( options ) { 
                	return this.each(function() {        
                    		// If options exist, lets merge them
                    		// with our default settings
                    		if ( options ) { 
	                        	$.extend( settings, options );
                    		}
                	});
		},
		render: function() {
			/**
			 * Render for radio buttons
			 */
			// id_month_comp : choiceId:'months'
			ximpia.console.log('option ... render...');
			var data = JSON.parse(sessionStorage.getItem("xpForm"));
			for (var i=0; i<$(this).length; i++) {
				var element = $(this)[i];
				ximpia.console.log('element : ' + element); 
				var idBase = $(element).attr('id').split('_comp')[0];
				console.log('idBase : ' + idBase);
				var doRender = ximpia.common.Form.doRender(element, settings.reRender);
				if (doRender == true) {
					var name = idBase.split('id_')[1];
					var value = "";
					var choicesId = "";
					if (data.hasOwnProperty(name)) {
						value = data[name]['value'];
						choicesId = data[name]['choicesId']
					}					
					$.metadata.setType("attr", "data-xp");
					var attrs = $(element).metadata();
	        		// Choices
	        		//ximpia.console.log('choiceId: ' + attrs['choiceId']); ????
	        		var choiceList = JSON.parse($('#id_choices').attr('value'))[choicesId];
	        		var htmlContent = "";
	        		if (attrs.hasOwnProperty('alignment')) {
		        		if (attrs.alignment == 'horizontal') {
		        			htmlContent += "<ul class=\"optHorizontal\"";
		        		} else  {
		        			htmlContent += "<ul class=\"optVertical\"";
		        		}
	        		} else {
	        			htmlContent += "<ul class=\"" + attrs['class'] + "\"";
	        		}	        		
	        		// Use class for ul, attrs.class, check for 'optVertical', 'optHorizontal'
					for (var j=0 ; i<choiceList.length; j++) {
						htmlContent += "<li>";
						if (choiceList[j][0] == value || j == 0) {
							if (attrs.type == 'radio') {
								htmlContent += "<input type=\"radio\" data-xp-type=\"list.option\" name=\"" + name + 
									"\" value=\"" + choiceList[j][0] + "\" selected />" + choiceList[j][1];
							} else {
								htmlContent += "<input type=\"checkbox\" data-xp-type=\"list.option\" name=\"" + name + 
									"\" value=\"" + choiceList[j][0] + "\" checked />" + choiceList[j][1];
							}
						} else {
							if (attrs.type == 'radio') {
								htmlContent += "<input type=\"radio\" data-xp-type=\"list.option\" name=\"" + name + 
									"\" value=\"" + choiceList[j][0] + "\" />" + choiceList[j][1];
							} else {
								htmlContent += "<input type=\"checkbox\" data-xp-type=\"list.option\" name=\"" + name + 
									"\" value=\"" + choiceList[j][0] + "\" />" + choiceList[j][1];
							}
						}
						htmlContent += "</li>";
					}
					htmlContent += "</ul>";
					// Assign html visual component div element
					$(element).html(htmlContent);
					// Set render, since we have rendered visual component
					$(element).attr('data-xp-render', JSON.stringify(true));
					// Trace
					ximpia.console.log(htmlContent);					
				}
			}
			$("input[type='checkbox'][data-xp-type='list.option']").click() {
				$(this).xpObjListOption("click", {type: 'check'});
			}
		},
		click: function(obj) {
			if (obj.type == 'check') {
				/*
				 * When user clicks on the option checkbox, current clicked element is unchecked and new element checked
				 */
				// TODO: Complete the checkbox click feature 				
			}
		},
		disable: function() {			
		},
		enable: function() {			
		},
		disableItem: function() {
		},
		enableItem: function() {
		},
		unrender: function() {
		}
        };		
        if ( methods[method] ) {
            return methods[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));
        } else if ( typeof method === 'object' || ! method ) {
            return methods.init.apply( this, arguments );
        } else {
            $.error( 'Method ' +  method + ' does not exist on jQuery.xpObjListOption' );
        }
	};

})(jQuery);
