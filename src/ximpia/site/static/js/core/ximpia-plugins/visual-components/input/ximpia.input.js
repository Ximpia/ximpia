/*
 * Ximpia Visual Component Input: Text, Password, etc...
 *
 */

(function($) {	

	$.fn.xpObjInput = function( method ) {
		
	// Include documentation from wiki here  

        // Settings		
        var settings = {
        	excudeListInput: ['type','id','element','help_text','label','left'],
        	excudeListInputSug: ['type','id','element','help_text','label','left'],
        	excludeListLabel: ['type','id','element'],
        	excludeList: ['info','type','left'],
        	htmlAttrs: ['tabindex','readonly','maxlength','class','value','name','autocomplete'],
        	djangoAttrs: ['type','id','info','help_text','label','element','left','xptype'],
        	reRender: false
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
		renderField: function(xpForm) {
			ximpia.console.log('input :: renderField...');
			var data = ximpia.common.Browser.getFormDataFromSession(xpForm);
			ximpia.console.log(data);
			for (var i=0; i<$(this).length; i++) {
				//ximpia.console.log($(this)[i]);
				var element = $(this)[i]; 
				var idInput = $(element).attr('id').split('_comp')[0];
				var doRender = ximpia.common.Form.doRender(element, settings.reRender);
				if (doRender == true) {
					ximpia.console.log('renderField :: id: ' + $(element).attr('id'));
					var nameInput = idInput.split('id_')[1];
					$.metadata.setType("attr", "data-xp");
					var attrs = $(element).metadata();
					//ximpia.console.log('input attrs: ' + idInput);
					//ximpia.console.log(attrs);
					var relatedId = $(element).attr('data-xp-related');
					var elementType = $(element).attr('data-xp-type');
					var dataAttrs = data[nameInput];
					var type = 'text';
					if (attrs.hasOwnProperty('type')) {
						type = attrs.type;
					}
					// id, name, type
					var htmlContent = "";
					ximpia.console.log(dataAttrs);
					var myValue = dataAttrs.value;
					if (attrs.hasOwnProperty('left')) {
						htmlContent = "<div style=\"width: " + attrs['left'] + "px; float: left\"><label for=\"" + idInput + "\"></label>:</div> <input id=\"" + idInput + "\" type=\"" + type + "\" name=\"" + nameInput + "\" value=\"" + myValue + "\" />";
					} else {
						htmlContent = "<label for=\"" + idInput + "\"></label>: <input id=\"" + idInput + "\" type=\"" + type + "\" name=\"" + nameInput + "\" value=\"" + myValue + "\" />";
					}
					$(element).html(htmlContent);
					$(element).attr('data-xp-render', JSON.stringify(true));
					// Input
					// Insert attributes to form element from server and metadata of visual component
					ximpia.common.Form.doAttributes({
						djangoAttrs: settings.djangoAttrs,
						htmlAttrs: settings.htmlAttrs,
						excludeList: settings.excludeList,
						dataAttrs: dataAttrs,
						attrs: attrs,
						idElement: idInput
					});
					if (typeof relatedId != 'undefined') {
						$("#" + idInput).attr('data-xp-related', relatedId);
					}
					if (typeof elementType != 'undefined') {
						$("#" + idInput).attr('data-xp-type', elementType);
					}
					//ximpia.console.log($("#" + idInput));
					// Label
					//ximpia.console.log('dataAttrs');
					//ximpia.console.log(dataAttrs);
					if (typeof dataAttrs != 'undefined' && dataAttrs.hasOwnProperty('label')) {
						$("label[for=\"" + idInput + "\"]").text(dataAttrs['label']);
						if (attrs.info == true) {
							$("label[for=\"" + idInput + "\"]").addClass("info");
							// help_text
							if (dataAttrs.hasOwnProperty('help_text')) {
								$("label[for=\"" + idInput + "\"]").attr('data-xp-title', dataAttrs['help_text']);
							}
						}
					}
				}
			}
		},
		renderFieldAutoComplete: function(xpForm) {
			var data = ximpia.common.Browser.getFormDataFromSession(xpForm);
			//var data = JSON.parse(sessionStorage.getItem("xpForm"));
			ximpia.console.log('renderTextChoice...');
			for (var i=0; i<$(this).length; i++) {
				//ximpia.console.log($(this)[i]);
				var element = $(this)[i]; 
				var idInput = $(element).attr('id').split('_comp')[0];
				var nameInput = idInput.split('id_')[1];
				var doRender = ximpia.common.Form.doRender(element, settings.reRender);
				if (doRender == true) {
					$.metadata.setType("attr", "data-xp");
					var attrs = $(element).metadata();
					//ximpia.console.log('input attrs: ' + idInput);
					//ximpia.console.log(attrs);
					/*ximpia.console.log('element...');
					ximpia.console.log(element);*/
					var relatedId = $(element).attr('data-xp-related');
					var elementType = $(element).attr('data-xp-type');
					var dataAttrs = data[nameInput];
					ximpia.console.log(dataAttrs);
					var sugAttrs = {};
					var type = 'text';
					if (attrs.hasOwnProperty('type')) {
						type = attrs.type;
					}
					//ximpia.console.log('type : ' + type);
					var htmlContent = "";
					if (attrs.hasOwnProperty('left')) {
						htmlContent = "<div style=\"width: " + attrs['left'] + "px; float: left\"><label for=\"" + idInput + "\"></label>:</div> <input id=\"" + idInput + "\" type=\"" + type + "\" name=\"" + nameInput + "\" value=\"\" />";
					} else {
						htmlContent = "<label for=\"" + idInput + "\"></label>: <input id=\"" + idInput + "\" type=\"" + type + "\" name=\"" + nameInput + "\" value=\"\" />";
					}
					$(element).html(htmlContent);
					$(element).attr('data-xp-render', JSON.stringify(true));
					// Input
					ximpia.common.Form.doAttributes({
						djangoAttrs: settings.djangoAttrs,
						htmlAttrs: settings.htmlAttrs,
						excludeList: settings.excludeList,
						dataAttrs: dataAttrs,
						attrs: attrs,
						idElement: idInput
					});
					if (typeof relatedId != 'undefined') {
						$("#" + idInput).attr('data-xp-related', relatedId);
					}
					if (typeof elementType != 'undefined') {
						$("#" + idInput).attr('data-xp-type', elementType);
					}
					//ximpia.console.log($("#" + idInput));
					// Label				
					if (typeof dataAttrs != 'undefined' && dataAttrs.hasOwnProperty('label')) {
						$("label[for=\"" + idInput + "\"]").text(dataAttrs['label']);
						if (attrs.info == true) {
							$("label[for=\"" + idInput + "\"]").addClass("info");
							// help_text
							if (dataAttrs.hasOwnProperty('help_text')) {
								$("label[for=\"" + idInput + "\"]").attr('data-xp-title', dataAttrs['help_text']);
							}
						}	
					}
					sugAttrs = JSON.parse($("#" + idInput).attr('data-xp'));
					// Build property data from choices data
					var choicesId = dataAttrs['choicesId'];
					var choices = JSON.parse($("#id_choices").attr('value'))[choicesId];
					/*ximpia.console.log('choices...');
					ximpia.console.log('choicesId : ' + choicesId);
					ximpia.console.log(choices)*/
					if (typeof(choices) != 'undefined') {
						sugAttrs.data = []
					}
					for (choiceIndex in choices) {
						sugAttrs.data[choiceIndex] = {}
						sugAttrs.data[choiceIndex]['id'] = choices[choiceIndex][0];
						sugAttrs.data[choiceIndex]['text'] = choices[choiceIndex][1];
					}
					//ximpia.console.log(sugAttrs);
					if (sugAttrs.hasOwnProperty('data')) {
						$("#" + idInput).jsonSuggest({	data: sugAttrs.data, 
										maxHeight: sugAttrs.maxHeight, 
										minCharacters: sugAttrs.minCharacters
										});
					} else {
						$("#" + idInput).jsonSuggest({	url: sugAttrs.url, 
										maxHeight: sugAttrs.maxHeight, 
										minCharacters: sugAttrs.minCharacters
										});
					}
				}
			}
		},
		disable: function() {
			var idInput = $(this).attr('id').split('_comp')[0];
			$("#" + idInput).attr('disable', 'disable');
		},
		enable: function() {
		},
		addHidden: function(xpForm) {
			// xpData.form_login
			//ximpia.console.log('addHidden...');
			//ximpia.console.log('xpForm: ', xpForm);
			var data = ximpia.common.Browser.getFormDataFromSession(xpForm);
			var formId = ximpia.common.Browser.getForm(xpForm);
			var viewName = ximpia.common.Browser.getView(xpForm);
			//ximpia.console.log('data length : ' + data.length());
			if (typeof data != 'undefined') {
				var list = Object.keys(data);
				//JSON.stringify(data[list[key]]['value'])
				for (key in list) {
					if (data[list[key]]['type'] == 'hidden') {
						//var value = JSON.stringify(data[list[key]]['value']);
						var value = data[list[key]]['value'];
						$('#' + formId).append("<input type=\"hidden\" id=\"id_" + formId + '_' + list[key] + "\" name=\"" + list[key] + "\"  />");
						$("#id_" + formId + '_' + list[key]).attr('value', value);
						// Inject viewNameSource : viewName is same as formId
						if (list[key] == 'viewNameSource') {
							$("#id_" + formId + '_' + list[key]).attr('value', viewName);
						}
					}				
				}				
			}
			//ximpia.console.log($('#' + formId));
		}
        };
		
        if ( methods[method] ) {
            return methods[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));
        } else if ( typeof method === 'object' || ! method ) {
            return methods.init.apply( this, arguments );
        } else {
            $.error( 'Method ' +  method + ' does not exist on jQuery.xpObjInput' );
        }    
		
	};

})(jQuery);
