/*
 * Ximpia Visual Component Hidden
 * 
 * TODO: Include the html for component
 *
 */

(function($) {	

	$.fn.xpObjHidden = function( method ) {
		
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
            $.error( 'Method ' +  method + ' does not exist on jQuery.xpObjHidden' );
        }    
		
	};

})(jQuery);
