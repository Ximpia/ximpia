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
				ximpia.console.log('***************** ctx ******************');
				ximpia.console.log(ctx);
        			var paramStr = '{';
        			for (param in ctx.params) {
        				paramStr += param + ": '" + ctx.params[param] + "'";
        			}
        			paramStr += '}';
				// data-xp : viewName, actionName, windowType
				var dataXp = "{winType: '" + ctx.winType + "', view: '" + ctx.view + "', action: '" + 
					ctx.action + "', params: " + paramStr + ", app: '" + ctx.app + "'}";
				var liAttr = (ctx.icon != '') ? "class=\"" + ctx.icon + "Small\"" : '';
				liAttr += (ctx.sep == true) ? ' separator' : '';
				//var action = (ctx.view != '') ? 'openView' : 'openAction';
				var action = 'menu-' + ctx.name;
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
					$(this).xpObjCtxMenu('clickItem', action);
			});
		},
		clickItem: function(name) {
			/**
			 * Click on context menu item
			 */
			ximpia.console.log('clickItem!!!! ' + name);
			ximpia.console.log($("a[href='#" + name + "']"));
			var clickObj = $("a[href='#" + name + "']");
			$.metadata.setType("attr", "data-xp");
			var attrs = clickObj.metadata();
			ximpia.console.log('attrs...');
			ximpia.console.log(attrs);
			if (attrs.action != '') {
				// do action
				ximpia.console.log('action!!!!');
				var pageJx = ximpia.common.PageAjax();
				pageJx.doAction( {action: attrs.action, app: attrs.app} );
			} else if (attrs.view != '') {
				// show view
				// popupNoView
				// popupView
				// view
				ximpia.console.log('view!!!!');
				ximpia.console.log('view: ' + attrs.view);
				ximpia.console.log('winType: ' + attrs.winType);
				ximpia.console.log('app: ' + attrs.app);
				if (attrs.winType != 'popup') {
					ximpia.common.PageAjax.doFadeIn();
				}
				var pageJx = ximpia.common.PageAjax();
				pageJx.getView({ view: attrs.view, params: JSON.stringify(attrs.params), winType: attrs.winType, app: attrs.app });
			}
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
