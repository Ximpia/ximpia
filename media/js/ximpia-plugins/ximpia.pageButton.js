/*
 * Ximpia Page Button, so far associated with button bar
 *
 */

(function($) {
	
	$.fn.xpPageButton = function( method ) {  

        // Settings		
        var settings = {
        	classButton: "button",
        	classButtonColor: "buttonBlue",
        	xpClass: "submit"
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
	render : function() {
		// Hover button
		$(this).hover(function() {
			$(this).addClass(settings.classButton +  '-hover');
			$(this).addClass(settings.classButtonColor +  '-hover');
		}, function() {		
			$(this).removeClass(settings.classButton +  '-hover');
			$(this).removeClass(settings.classButtonColor +  '-hover');
		});
		$("[data-xp-js='" + settings.xpClass + "']").mousedown(function() {
			$(this).addClass(settings.classButton +  '-active');
			$(this).addClass(settings.classButtonColor +  '-active');
		}).mouseup(function(){
			$(this).removeClass(settings.classButton +  '-active');
			$(this).removeClass(settings.classButtonColor +  '-active');
		})
	},
	disable: function() {
	   	$(this).addClass(settings.classButtonColor +  '-disabled');
	   	$(this).css('cursor', 'default');
	   	$(this).unbind('mouseenter mouseleave click mousedown mouseup');
	},
	enable: function(clickMethod) {
		$(this).removeClass(settings.classButtonColor +  '-disabled');
		$(this).css('cursor', 'pointer');
		$(this).hover(function() {
			$(this).addClass(settings.classButton +  '-hover');
			$(this).addClass(settings.classButtonColor +  '-hover');
		}, function() {		
			$(this).removeClass(settings.classButton +  '-hover');
			$(this).removeClass(settings.classButtonColor +  '-hover');
		});
		$(this).mousedown(function() {
			$(this).addClass(settings.classButton +  '-active');
			$(this).addClass(settings.classButtonColor +  '-active');
		}).mouseup(function(){
			$(this).removeClass(settings.classButton +  '-active');
			$(this).removeClass(settings.classButtonColor +  '-active');
		})
		$(this).click(clickMethod);
	}
	
        };
		
        if ( methods[method] ) {
            return methods[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));
        } else if ( typeof method === 'object' || ! method ) {
            return methods.init.apply( this, arguments );
        } else {
            $.error( 'Method ' +  method + ' does not exist on jQuery.xpPageButton' );
        }    
		
	};

})(jQuery);
