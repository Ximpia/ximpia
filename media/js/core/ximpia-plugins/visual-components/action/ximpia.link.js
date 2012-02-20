/*
 * Ximpia Visual Component 
 * Link
 *
 */

(function($) {	
	$.fn.xpObjLink = function( method ) {  
        // Settings		
        var settings = {
        };
        var doOpenPopup = function(obj) {
        	console.log('Open Popup!!!!');
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
			console.log('Render Link...');
			for (var i=0; i<$(this).length; i++) {
				var element = $(this)[i];
				var idLink = $(element).attr('id').split('_comp')[0];
				$.metadata.setType("attr", "data-xp");
				var attrs = $(element).metadata();
				var dataXp = "{op: '" + attrs.op + "', app: '" + attrs.app + "', name: '" + attrs.name + "', content: '" + attrs.content + "'}";
				var htmlContent = "<a href=\"javascript:return void(false)\" id=\"" + idLink + "\"  alt=\"" + attrs.alt + "\" data-xp=\"" + dataXp + "\">" + attrs.linkText + "</a>";
				$(element).html(htmlContent);
				$("#" + idLink).click(function() {
					$(this).xpObjLink('click');
				});
			}
		},
		click: function() {
			var element = $(this)[0];
			$.metadata.setType("attr", "data-xp");
			var attrs = $(element).metadata();
			attrs.element = element;
			var operation = attrs.op;
			console.log('operation: ' + operation);
			if (operation == 'openPopup') {
				doOpenPopup(attrs);
			}
		}
        };
		
        if ( methods[method] ) {
            return methods[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));
        } else if ( typeof method === 'object' || ! method ) {
            return methods.init.apply( this, arguments );
        } else {
            $.error( 'Method ' +  method + ' does not exist on jQuery.xpObjLink' );
        }    
		
	};

})(jQuery);
