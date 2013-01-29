/*
 * Ximpia Visual Component Input: Text, Password, etc...
 *
 * TODO: Include the html for component
 * 
 */

(function($) {	

	$.fn.xpObjField = function( method ) {
		
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
		render: function(xpForm) {
			ximpia.console.log('input :: renderField...');
			var data = ximpia.common.Browser.getFormDataFromSession(xpForm);
			ximpia.console.log(data);
			for (var i=0; i<$(this).length; i++) {
				ximpia.console.log($(this)[i]);
				var element = $(this)[i]; 
				var idInput = $(element).attr('id').split('_comp')[0];
				var doRender = ximpia.common.Form.doRender(element, settings.reRender);
				if (doRender == true) {
					ximpia.console.log('renderField :: id: ' + $(element).attr('id'));
					var nameInput = idInput.split('id_')[1];
					ximpia.console.log('nameInput: ' + nameInput);
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
						if (attrs.hasOwnProperty('label')) {
							$("label[for=\"" + idInput + "\"]").text(attrs['label']);
						} else {
							$("label[for=\"" + idInput + "\"]").text(dataAttrs['label']);
						}
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
		disable: function() {
			var idInput = $(this).attr('id').split('_comp')[0];
			$("#" + idInput).attr('disable', 'disable');
		},
		enable: function() {
		}
        };
		
        if ( methods[method] ) {
            return methods[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));
        } else if ( typeof method === 'object' || ! method ) {
            return methods.init.apply( this, arguments );
        } else {
            $.error( 'Method ' +  method + ' does not exist on jQuery.xpObjField' );
        }    
		
	};

})(jQuery);
