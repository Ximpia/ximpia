/*
 * Ximpia Visual Component Option: Will show a checkbox. Will support many or just one. When click is performed,
 * could behave like an html option or as a html checkbox.
 *
 */

(function($) {	

	$.fn.xpObjOption = function( method ) {
	
	/**
	 * Options
	 * =======
	 * align: left|block
	 * multi: true|false
	 *  
	 */  

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
		render: function() {
			
		},
		click: function() {
			
		}
        };
		
        if ( methods[method] ) {
            return methods[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));
        } else if ( typeof method === 'object' || ! method ) {
            return methods.init.apply( this, arguments );
        } else {
            $.error( 'Method ' +  method + ' does not exist on jQuery.xpObjOption' );
        }    
		
	};

})(jQuery);
