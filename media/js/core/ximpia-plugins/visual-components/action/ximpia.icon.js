/*
 * Ximpia Visual Component 
 * Icon
 *
 */

(function($) {	
	$.fn.xpObjIcon = function( method ) {  
        // Settings		
        var settings = {
        };
        var buildIcon = function( obj ) {
        	var paramStr = '{';
        	for (param in obj.params) {
        		paramStr += param + ": '" + obj.params[param] + "'";
        	}
        	paramStr += '}';
		var htmlContent = '';
		htmlContent += "<div id=\"id_icon_" + obj.name + "\" data-xp-type=\"icon\" style=\"float: " + obj.align + "\" class=\"iconMenuBlock\" title=\"" + obj.title + "\" >";
		htmlContent += "<a href=\"#\" onclick=\"return false\" data-xp=\"{action: '" + obj.action + "', view: '" + obj.view + "', params: " + paramStr + "}\"  >";
		htmlContent += "<img src=\"/site_media/images/blank.png\" class=\"" + obj.icon + " iconMenu\" />";
		htmlContent += "<div>" + obj.titleShort + "</div>";
		return htmlContent;
        };
        var buildBlankIcon = function( obj ) {
        	var htmlContent = '';
        	htmlContent += "<div style=\"float: right\" class=\"iconMenuBlock\"><img src=\"/site_media/images/blank.png\" class=\"iconBlank\" /></div>";
        	return htmlContent;
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
		renderMenu: function() {
			/**
			 * Render icon
			 */
			ximpia.console.log('icon :: render: ');
			var menus = ximpia.common.Browser.getObject('menus');
			
			// Parse sys => Create context menus for logo
			ximpia.console.log('Parse sys...');
			ximpia.console.log(menus['sys']);
			if (menus.hasOwnProperty('sys')) {
				var menuObj = menus['sys'][0];
				ximpia.console.log('menuObj: ' + menuObj);
				var items = menuObj['items'];
				$('#LogoImg').xpObjCtxMenu('render', 'id_ctx_menu_sys', items);
			}			
			
			// Parse main
			// TODO: Icon with personalized images, dropdown ?????
			ximpia.console.log('Parse main...');
			ximpia.console.log(menus['main']);
			for (i in menus['main']) {
				var menuObj = menus['main'][i]
				menuObj.align = 'left';
				var elemId = 'id_icon_' + menuObj.name;
				if (!$('#' + elemId).length) {
					ximpia.console.log('menuObj');
					ximpia.console.log(menuObj);
					var htmlContent = buildIcon(menuObj);
					ximpia.console.log(htmlContent);
					$('#id_mainIcons').prepend(htmlContent);
					$('#' + elemId).attr('data-xp-render', JSON.stringify(true));
				}
			}			
			
			// Parse view
			$('#id_viewIcons').empty();
			for (i in menus['view']) {
				if (i < 7) {
					var menuObj = menus['view'][i]
					menuObj.align = 'right';
					var elemId = 'id_icon_' + menuObj.name;
					ximpia.console.log(menuObj);
					var htmlContent = buildIcon(menuObj);
					ximpia.console.log(htmlContent);
					$('#id_viewIcons').prepend(htmlContent);
					$('#' + elemId).attr('data-xp-render', JSON.stringify(true));					
				}
			}
			
			// Tooltip
			$("[data-xp-type='icon']").qtip({
				content: {
					attr: 'title'
				},
				position: {
					my: 'top center',
					at: 'bottom center'
				},
				events: {
					focus: function(event, api) {
					}
				},
				style: {
					classes: 'ui-tooltip-dark ui-tooltip-shadow ui-tooltip-rounded'
				}
			});
			
			// Click event
			$("[data-xp-type='icon']").click(function() {
				$($(this)).xpObjIcon('clickMenu');	
			});
			
			/*for (var i=0; i<$(this).length; i++) {
				ximpia.console.log('i: ' + i);
				var element = $(this)[i];
				ximpia.console.log('element: ' + element);
				var doRender = ximpia.common.Form.doRender(element, settings.reRender);
				ximpia.console.log('doRender: ' + doRender);
				if (doRender == true) {
					$.metadata.setType("attr", "data-xp");
					var attrs = $(element).metadata();
					ximpia.console.log('attrs');
					ximpia.console.log(attrs);
					$(element).attr('style', 'float: left');
					$(element).addClass('iconMenuBlock');
					var htmlInside = "<a href=\"#\" onclick=\"return false\" data-xp=\"{action: '" + attrs.action + "', view: '" + attrs.view + "'}\">";
					htmlInside += "<img src=\"/site_media/images/blank.png\" class=\"" + attrs.icon + " iconMenu\" />";
					htmlInside += "<div>" + attrs.text + "</div>";
					ximpia.console.log(htmlInside);
					$(element).html(htmlInside);
					$(element).attr('data-xp-render', JSON.stringify(true));
					// Click
					$(element).click(function() {
						ximpia.console.log('Icon click!!!!!');
						//
					});
					// Context Menu
				}
			}*/
		},
		clickMenu: function() {
			ximpia.console.log('Icon Menu Click!!!');
			ximpia.console.log($('#' + $(this).attr('id') + ' > a '));
			var clickObj = $('#' + $(this).attr('id') + ' > a ');
			$.metadata.setType("attr", "data-xp");
			var attrs = clickObj.metadata();
			ximpia.console.log('attrs...');
			ximpia.console.log(attrs);
			if (attrs.action != '') {
				// do action
				ximpia.console.log('action!!!!');
				var pageJx = ximpia.common.PageAjax();
				pageJx.doAction( {action: attrs.action} );
			} else if (attrs.view != '') {
				// show view
				// popupNoView
				// popupView
				// view
				ximpia.console.log('view!!!!');
				ximpia.console.log('view: ' + attrs.view);
				ximpia.common.PageAjax.doFadeIn();
				var pageJx = ximpia.common.PageAjax();
				pageJx.getView({ view: attrs.view, params: JSON.stringify(attrs.params) });
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
