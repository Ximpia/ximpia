/*
 * Ximpia Small Loading Icon
 *
 */

(function($) {
	
	$.fn.xpLoadingSmallIcon = function( method ) {  

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
            wait : function() {
				$(this).removeClass('AjaxButton');
				$(this).removeClass('AjaxButtonERROR');
				$(this).addClass('AjaxButtonLoading');
			},
            ok : function() {
				$(this).removeClass('AjaxButtonLoading');
				$(this).removeClass('AjaxButtonERROR');
				$(this).addClass('AjaxButtonOK');
			},
            error : function() {
				$(this).removeClass('AjaxButtonLoading');
				$(this).addClass('AjaxButtonERROR');
			},
            errorWithPopUp : function() {
                $(this).removeClass('AjaxButtonLoading');
            }
        };
		
        if ( methods[method] ) {
            return methods[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));
        } else if ( typeof method === 'object' || ! method ) {
            return methods.init.apply( this, arguments );
        } else {
            $.error( 'Method ' +  method + ' does not exist on jQuery.xpLoadingSmallIcon' );
        }    
		
	};

})(jQuery);
