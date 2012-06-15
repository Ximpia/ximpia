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
        	//console.log('Link Open Popup!!!!');
        	//console.log(obj);
        	// TODO: Call openPopup method in PageAjax
        	// This should call request view and normal popups
        	ximpia.console.log('tmplAlias length: ' + obj.tmplAlias.length);
        	if (obj.tmplAlias.length != 0) {
        		obj.isPopupReqView = false;
        	} else {
        		obj.isPopupReqView = true;
        	}
        	//obj.isPopupReqView = false;
        	ximpia.console.log('link :: doOpenPopup :: obj.isPopupReqView: ' + obj.isPopupReqView);
        	$('body').xpObjPopUp(obj).xpObjPopUp('create');
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
				var doRender = ximpia.common.Form.doRender(element, settings.reRender);
				if (doRender == true) {
					var idLink = $(element).attr('id').split('_comp')[0];
					ximpia.console.log('idLink: ' + idLink);
					$.metadata.setType("attr", "data-xp");
					var attrs = $(element).metadata();
					ximpia.console.log('Link Attrs...');
					ximpia.console.log(attrs);
					attrs.viewName = 'login';
					attrs.tmplAlias = 'passwordReminder';
					//ximpia.console.log($(element));
					// TODO: We should give these to open popup: tmplAlias
					// TODO: Way to get application code
					// tmplAlias should resolve into a tmpl using the result context
					var dataXp = "{op: '" + attrs.op + "', app: '" + attrs.app + "', name: '" + attrs.name + "', viewName: '" + attrs.viewName + "', tmplAlias: '" + attrs.tmplAlias + "'}";
					var htmlContent = "<a href=\"javascript:return void(false)\" id=\"" + idLink + "\"  alt=\"" + attrs.alt + "\" data-xp=\"" + dataXp + "\">" + attrs.linkText + "</a>";
					$(element).html(htmlContent);
					$(element).attr('data-xp-render', JSON.stringify(true));
					$("#" + idLink).click(function() {
						$(this).xpObjLink('click');
					});
				}
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
