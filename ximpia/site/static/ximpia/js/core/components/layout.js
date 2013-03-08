
/*
 * 
 * Copyright (c) 2013 Ximpia, Inc, All rights reserved
 * This Source Code Form is subject to the terms of the Mozilla Public License, 
 * v. 2.0. If a copy of the MPL was not distributed with this file, You can obtain 
 * one at http://mozilla.org/MPL/2.0/.
 * 
 */

/*
 * Container
 * 
 * Group set of visual components in a block.
 * 
 * Supports conditions. You can place your visual objects inside containers to force condition for rendering.
 * 
 * Conditions are defined in the view definitions with attribute ``data-xp-cond-rules``, like:
 * 
 * ```
 * <div 	id="id_view" 
 * 		data-xp="{viewName: 'signup'}" 
 * 		data-xp-cond-rules="{hasUserAuth: 'settings.SIGNUP_USER_PASSWORD == true', hasNetAuth: 'settings.SIGNUP_SOCIAL_NETWORK == true', socialNetLogged: 'socialNetLogged == true'}" >
 * </div>```
 * 
 * Then we define condition for the container, like:
 * 
 *  ```<div id="id_passwordAuth" data-xp-type="container" data-xp-cond="{conditions: [{condition: 'socialNetLogged', render: false}]}" >
 *  ...your objects...
 *  </div>```
 * 
 * ** Attributes**
 * 
 * * ``data-xp-type`` : container
 * * ``data-xp-cond``:ListType : Condition objects, like [{}, {}, ...] First matched condition will execute action
 * 		* ``conditions``:ListType : List of conditions:
 * 			* ``condition`` : condition key from ``data-xp-cond-rules``
 * 			* ``action`` : Supported values: 'render'
 * 			* ``value``:Boolean : true / false
 * 
 */

(function($) {	

	$.fn.xpContainer = function( method ) {  

        // Settings		
        var settings = {
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
			ximpia.console.log('xpObjContainer :: render...');
			var data = ximpia.common.Browser.getFormDataFromSession(xpForm);
			ximpia.console.log(data);
			// Process Condition rules
			var evals = ximpia.common.Condition.processRules();
			for (var i=0; i<$(this).length; i++) {
				var element = $(this)[i];
				ximpia.console.log('xpObjContainer :: Element ' + $(element).attr('id'));
				var idInput = $(element).attr('id').split('_comp')[0];
				var hasToRender = ximpia.common.Form.hasToRender(element, settings.reRender);
				if (hasToRender == true) {					
					// do element conditions
					ximpia.common.Condition.doElements(evals, element)
				}
			}
		}
        };
		
        if ( methods[method] ) {
            return methods[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));
        } else if ( typeof method === 'object' || ! method ) {
            return methods.init.apply( this, arguments );
        } else {
            $.error( 'Method ' +  method + ' does not exist on jQuery.xpContainer' );
        }
	};

})(jQuery);
