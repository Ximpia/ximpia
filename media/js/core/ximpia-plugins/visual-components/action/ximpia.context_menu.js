/*
 * Ximpia Visual Component 
 * Context Menu
 *
 */

(function($) {	
	$.fn.xpObjCtxMenu = function( method ) {  
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
		render: function( idMenu, items ) {
			/**
			 * Render the context menu
			 * idMenu: 	Id for the menu html
			 * items: 	List of objects with context menu data [ {icon: '', viewName: '', actionName: '', 
			 * 		windowType: 'window|popup', sep: True|False, text: ''} ]
			 */			
			var contextMenu = '';
			contextMenu += "<ul id=\"" + idMenu + "\" class=\"contextMenu\">";
			for (ctxI in items) {
				var ctx = items[ctxI];
				ximpia.console.log(ctx);
				// data-xp : viewName, actionName, windowType
				var dataXp = "{windowtype: '" + "window" + "', viewName: '" + ctx.view + "', actionName: '" + 
					ctx.action + "'}";
				var liAttr = (ctx.icon != '') ? "class=\"" + ctx.icon + "Small\"" : '';
				liAttr += (ctx.sep == true) ? ' separator' : '';
				var action = (ctx.view != '') ? 'openView' : 'openAction';
				contextMenu += "<li " + liAttr + "><a href=\"#" + action + "\" data-xp-type=\"ctxMenuItem\" data-xp=\"" + dataXp + "\" >" + ctx.title + "</a></li>";
			}
			contextMenu += "</ul>";
			//ximpia.console.log('contextMenu: ' + contextMenu);
			// Insert content into DOM
			$('body').append(contextMenu);
			// Call context menu plugin
			ximpia.console.log($(this));
			$(this).contextMenu({ menu: idMenu, alignElement: true},
				function(action, el, pos) {
					ximpia.console.log('itemAction: ' + action);
					$(this).xpObjCtxMenu('clickItem');
			});
		},
		clickItem: function() {
			/**
			 * Click on context menu item
			 */
			ximpia.console.log('clickItem!!!!');
		}
        };
		
        if ( methods[method] ) {
            return methods[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));
        } else if ( typeof method === 'object' || ! method ) {
            return methods.init.apply( this, arguments );
        } else {
            $.error( 'Method ' +  method + ' does not exist on jQuery.xpObjIcon' );
        }    
		
	};

})(jQuery);
