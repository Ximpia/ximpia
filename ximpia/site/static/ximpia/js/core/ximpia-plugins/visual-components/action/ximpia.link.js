/*
 * 
 * Links used to:
 * 
 * 1. Launch views (new and popups) - launchView
 * 2. Open popups (openPopup) - openPopup
 * 3. Launch actions - doAction
 * 4. Link to url - callUrl
 * 
 * Place types like...
 * link.popup
 * link.url
 * link.view
 * link.action
 * 
 * 
 * <!--<div id="id_passwordReminderLinkUrl_comp" data-xp-type="link.url" style="margin-top: 20px; margin-left: 20px"  
		data-xp="{	op: 'callUrl', 
					url: '/',
					target: '_blank',
					width: 800,
					height: 600,
					title: 'go to home...', 
					linkText: 'Take me to Home'}" ></div>

<div id="id_lnkCode_comp" data-xp-type="link.view" style="margin-top: 20px; margin-left: 20px"  
		data-xp="{	op: 'showView', 
					app: 'ximpia_site.web',
					title: 'go to home...', 
					linkText: 'Show Code',
					view: 'code'}" ></div>

<div id="id_lnkSignout_comp" data-xp-type="link.action" style="margin-top: 20px; margin-left: 20px"  
		data-xp="{	op: 'doAction', 
					app: 'ximpia.site',
					title: 'will logout...', 
					linkText: 'Logout',
					action: 'logout'}" ></div>-->
 *
 */

(function($) {	
	$.fn.xpObjLink = function( method ) {  
        // Settings		
        var settings = {
        };
        var doOpenPopup = function(obj) {
        	//ximpia.console.log('xpObjLink.doOpenPopup :: Link Open Popup!!!!');
        	//ximpia.console.log(obj);
        	// TODO: Call openPopup method in PageAjax
        	// This should call request view and normal popups
        	ximpia.console.log('xpObjLink.doOpenPopup :: tmplAlias length: ' + obj.tmplAlias.length);
        	if (obj.tmplAlias.length != 0) {
        		obj.isPopupReqView = false;
        	} else {
        		obj.isPopupReqView = true;
        	}
        	//obj.isPopupReqView = false;
        	ximpia.console.log('xpObjLink.doOpenPopup :: obj.isPopupReqView: ' + obj.isPopupReqView);
        	$('body').xpObjPopUp(obj).xpObjPopUp('create');
        };
        var showView = function(obj) {
        	ximpia.console.log('xpObjLink.showview...');
			ximpia.common.PageAjax.doFadeIn();
			var pageJx = ximpia.common.PageAjax();
			if (!obj.hasOwnProperty('app')) {
				obj.app = ximpia.common.Browser.getApp();
			}
			ximpia.console.log('xpObjLink.showview :: view: ' + obj.view + ' app: ' + obj.app);
			pageJx.getView({ view: obj.view, params: '{}', app: obj.app });
        };
        var doAction = function(obj) {
			if (!obj.hasOwnProperty('app')) {
				obj.app = ximpia.common.Browser.getApp();
			}
			var pageJx = ximpia.common.PageAjax();
			pageJx.doAction( {action: obj.action, app: obj.app} );
        };
        var callUrl = function(obj) {
        	if (obj.hasOwnProperty('target') || obj.hasOwnProperty('width') || obj.hasOwnProperty('height')) {
        		ximpia.console.log('xpObjLink.callUrl :: target');
        		var specs = '';
	        	if (obj.hasOwnProperty('height')) {
	        		specs += 'height=' + obj.height;
	        	}
	        	if (obj.hasOwnProperty('width')) {
	        		specs += ',width=' + obj.width;
	        	}
	        	ximpia.console.log('url: ' + obj.url + ' name: ' + obj.target + ' specs: ' + specs);
        		window.open(obj.url, obj.target, specs);
        	} else {
        		ximpia.console.log('xpObjLink.callUrl :: no target');
        		window.location = obj.url;
        	}        	
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
			ximpia.console.log('xpObjLink.render :: Render Link... ' + $(this).length);
			for (var i=0; i<$(this).length; i++) {
				var element = $(this)[i];
				ximpia.console.log(element);
				var doRender = ximpia.common.Form.doRender(element, settings.reRender);
				if (doRender == true) {
					var idLinkSrc = $(element).attr('id');
					var idLink = $(element).attr('id').split('_comp')[0];
					ximpia.console.log('xpObjLink.render :: idLink: ' + idLink);
					$.metadata.setType("attr", "data-xp");
					var attrs = $(element).metadata();
					//var attrs = $('#' + idLinkSrc).metadata();
					ximpia.console.log('xpObjLink.render :: Link Attrs...');
					ximpia.console.log(attrs);
					// TODO: We should give these to open popup: tmplAlias
					// tmplAlias should resolve into a tmpl using the result context
					// In case no app, we get the default application from the response object in session storage
					if (!attrs.hasOwnProperty('app')) {
						attrs.app = ximpia.common.Browser.getApp();
					}
					var dataXp = ximpia.common.Object.metadata(attrs);
					var htmlContent = "<a href=\"#\" id=\"" + idLink + "\" data-xp=\"" + dataXp + "\"";
					if (attrs.hasOwnProperty('title')) {
						htmlContent += " title=\"" + attrs.title + "\"";
					}
					if (attrs.hasOwnProperty('tabindex')) {
						htmlContent += " tabindex=\"" + attrs.tabindex + "\"";
					}
					if (attrs.hasOwnProperty('target')) {
						htmlContent += " target=\"" + attrs.target + "\"";
					}
					htmlContent += " class=\"xpLink\">" + attrs.linkText + "</a>";
					ximpia.console.log(htmlContent);
					$(element).html(htmlContent);
					$(element).attr('data-xp-render', JSON.stringify(true));
					$("#" + idLink).click(function(evt) {
						// preventDefault in case not url operation 
						evt.preventDefault();
						// Check if disable
						ximpia.console.log('xpObjLink.render :: event...');
						ximpia.console.log(evt);
						var isDisabled = $(this).attr('disabled');
						ximpia.console.log('xpObjLink.render :: isDisabled: ' + isDisabled);
						if (!isDisabled) {
							//alert('click!!!');
							$(this).xpObjLink('click');
						}
					});
				}
			}
		},
		click: function() {
			var element = $(this)[0];
			ximpia.console.log('xpObjLink.click :: element: ');
			ximpia.console.log(element);
			$.metadata.setType("attr", "data-xp");
			var attrs = $(element).metadata();
			attrs.element = element;
			var operation = attrs.op;
			ximpia.console.log('operation: ' + operation);
			ximpia.console.log(attrs);
			if (operation == 'openPopup') {
				doOpenPopup(attrs);
			} else if (operation == 'showView') {
				showView(attrs);
			} else if (operation == 'doAction') {
				doAction(attrs);
			} else if (operation == 'callUrl') {
				callUrl(attrs);
			}
		},
		disable: function() {
			var element = $(this)[0];
			ximpia.console.log('xpObjLink.disable :: element: ' + element);
			var idLink = $(element).attr('id').split('_comp')[0];
			$("#" + idLink).attr('disabled', 'true');
		},
		enable: function() {
			var element = $(this)[0];
			ximpia.console.log('xpObjLink.enable :: element: ' + element);
			var idLink = $(element).attr('id').split('_comp')[0];
			$("#" + idLink).removeAttr('disabled');
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
