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
		var classPlus = '';
		if (obj.isCurrent == true && obj.zone == 'service') {
			classPlus = ' iconMenuCurrent';
		}
		var path = '/apps/' + obj.appSlug + '/' + obj.viewSlug + '/';
		if (obj.view == 'home') {
			path = '/';
		}
		if (obj.zone == 'main') {
			obj.title = '';
		}
		ximpia.console.log('xpObjIcon :: classPlus: ' + classPlus);
		htmlContent += "<div id=\"id_icon_" + obj.name + "\" data-xp-type=\"icon\" style=\"float: " + obj.align + "\" class=\"iconMenuBlock" + classPlus + "\" title=\"" + obj.description + "\" >";
		htmlContent += "<a href=\"" + path + "\" data-xp=\"{action: '" + obj.action + "', view: '" + obj.view + "', params: " + paramStr + ", app: '" + obj.app + "'}\"  >";		
		if (obj.title != '' && obj.icon != '') {
			// Have text and icon
			htmlContent += "<img src=\"" + ximpia.settings.STATIC_URL + "images/blank.png\" class=\"" + obj.icon + " iconMenu\" />";
			htmlContent += "<div >" + obj.title + "</div>";
		} else if (obj.title == '' && obj.icon != '') {
			// We center icon since we have no text
			htmlContent += "<img src=\"" + ximpia.settings.STATIC_URL + "images/blank.png\" class=\"" + obj.icon + " iconMenu\" style=\"margin-left: 0px\" />";
		} else if (obj.title != '' && obj.icon == '') {
			htmlContent += "<div style=\"margin-left: 7px\" >" + obj.title + "</div>";
		}
		return htmlContent;
        };
        var buildBlankIcon = function( obj ) {
        	var htmlContent = '';
        	htmlContent += "<div style=\"float: right\" class=\"iconMenuBlock\"><img src=\"" + ximpia.settings.STATIC_URL + "images/blank.png\" class=\"iconBlank\" /></div>";
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
			ximpia.console.log('xpObjIcon :: icon :: render: ');
			var menus = ximpia.common.Browser.getObject('menus');			
			// Parse sys => Create context menus for logo
			ximpia.console.log('xpObjIcon :: Parse sys...');
			ximpia.console.log(menus['sys']);
			if (menus.hasOwnProperty('sys')) {
				if (menus['sys'].length > 0) {
					var menuObj = menus['sys'][0];
					ximpia.console.log('xpObjIcon :: menuObj: ' + menuObj);
					var items = menuObj['items'];
					$("#id_sys_selector").css('display', 'block');
					$('#id_sys_selector').xpObjCtxMenu('render', 'id_ctx_menu_sys', items);
				} else {
					$("#id_sys_selector").css('display', 'none');
				}
			}
			// Parse main
			// TODO: Icons with personalized images, dropdown ?????
			ximpia.console.log('xpObjIcon :: Parse main...');
			ximpia.console.log(menus['main']);
			$('#id_mainIcons').empty();
			for (i in menus['main']) {
				var menuObj = menus['main'][i]
				menuObj.align = 'left';
				var elemId = 'id_icon_' + menuObj.name;
				ximpia.console.log('xpObjIcon :: elemId: ' + elemId + ' ' + !$('#' + elemId).length);
				// Check if #id_mainIcons already has this icon. If not, add to #id_mainIcons
				ximpia.console.log('xpObjIcon :: exsists: ' + $('#id_mainIcons:has(#' + elemId + ')').length);
				ximpia.console.log($('#id_mainIcons:has(#' + elemId + ')').length);
				if ($('#id_mainIcons:has(#' + elemId + ')').length == 0) {
					ximpia.console.log('xpObjIcon :: menuObj');
					ximpia.console.log(menuObj);
					var htmlContent = buildIcon(menuObj);
					ximpia.console.log(htmlContent);
					$('#id_mainIcons').append(htmlContent);
					$('#' + elemId).attr('data-xp-render', JSON.stringify(true));
				}
			}
			//Parse service
			ximpia.console.log('xpObjIcon :: Parse service...');
			ximpia.console.log(menus);
			ximpia.console.log(menus['service']);
			$('#id_serviceIcons').empty();
			for (i in menus['service']) {
				if (i < 7) {
					var menuObj = menus['service'][i]
					menuObj.align = 'right';
					var elemId = 'id_icon_' + menuObj.name;
					ximpia.console.log(menuObj);
					var htmlContent = buildIcon(menuObj);
					ximpia.console.log(htmlContent);
					$('#id_serviceIcons').prepend(htmlContent);
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
					at: 'bottom center',
					adjust: {
						y: 4
					}
				},
				events: {
					focus: function(event, api) {
					}
				},
				style: {
					classes: 'ui-tooltip-dark ui-tooltip-shadow ui-tooltip-rounded',
					style: 'margin-top: 2px'
				}
			});
			// Click event
			$("[data-xp-type='icon']").click(function(evt) {
				$(this).xpObjIcon('clickMenu', evt);	
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
		clickMenu: function(evt) {
			evt.preventDefault();
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
				pageJx.doAction( {action: attrs.action, app: attrs.app} );
			} else if (attrs.view != '') {
				// show view
				// popupNoView
				// popupView
				// view
				ximpia.console.log('view!!!!');
				ximpia.console.log('view: ' + attrs.view);
				ximpia.common.PageAjax.doFadeIn();
				var pageJx = ximpia.common.PageAjax();
				pageJx.getView({ view: attrs.view, params: JSON.stringify(attrs.params), app: attrs.app });
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
