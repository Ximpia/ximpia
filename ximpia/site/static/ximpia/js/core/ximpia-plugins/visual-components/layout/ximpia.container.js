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
 *  ```<div id="id_passwordAuth" data-xp-type="container" data-xp-cond="{condition: 'socialNetLogged', render: false}" >
 *  ...your objects...
 *  </div>```
 * 
 * ** Attributes**
 * 
 * * ``data-xp-type`` : container
 * * ``data-xp-cond`` : Condition object
 * 		* ``condition`` : condition key from ``data-xp-cond-rules``
 * 		* ``render``:Boolean : Render (display) objects
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
