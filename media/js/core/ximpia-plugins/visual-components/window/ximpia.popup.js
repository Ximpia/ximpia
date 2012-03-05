/*
 * Ximpia Visual Component 
 * Popup
 *
 */

(function($) {	
	$.fn.xpObjPopUp = function( method ) {  
        // Settings		
        var settings = {
        };
        var doCreateNoView = function(obj) {
        	var data = obj.data;
        	var settings = obj.settings;
        	var pageJx = ximpia.common.PageAjax();
        	var viewData = ximpia.common.Window.getViewAttrs();
        	console.log('viewData...');
        	console.log(viewData);
        	var elemContent = $(data).filter('#id_content').children().filter('#id_' + settings.app + '_' + settings.name + '_' + settings.content);
        	var closeValue = ximpia.common.List.getValue('id_buttonConstants', 'close');
        	var popupData = $(data).filter('#id_' + settings.app + '_' + settings.name + '_conf').metadata();
        	ximpia.common.Window.showMessage({
            		title: popupData.title,
            		message: '<div>' + elemContent.html() + '</div>',
            		buttons: 'id_msgClose:' + closeValue + ':delete',
            		effectIn: 'fadeIn,1000',
            		effectOut: '',
            		fadeBackground: true
            		//isHidden: true
        	});
            	$("#id_msgClose").click(function() {ximpia.common.Window.clickMsgOk(true)});
            	$("#id_btX").click(function() {ximpia.common.Window.clickMsgOk(true)});
            	console.log('id_pops');
            	console.log($('#id_pops'));
		pageJx.init({	path: ximpia.common.Path.getBusiness(),
			viewName: viewData.viewName,
			verbose: true});
		pageJx.doBusinessGetRequest({ className: viewData.className, method: viewData.method, mode: 'popupNoView' });
            	console.log('I am done!!!');
        };
        var doCreateView = function(obj) {
        	var pageJx = ximpia.common.PageAjax();
        	var settings = $(this).prop('settings');
		// Parse DOM template and get div wanted.
		var elemContent = $(data).filter('#id_content').children().filter('#id_' + settings.app + '_' + settings.name + '_' + settings.content);
		// Call server and render popup forms with new PageAjax method
		// Get all forms inside dic section, call server for each and add to js context
		var closeValue = ximpia.common.List.getValue('id_buttonConstants', 'close');
		//console.log('closeValue: ' + closeValue);
		var popupData = $(data).filter('#id_' + settings.app + '_' + settings.name + '_conf').metadata();
		//console.log('popupData...');
		//console.log(popupData);
		//console.log($(data).filter('#id_SN_passwordReminder_conf'));
        	ximpia.common.Window.showMessage({
            		title: popupData.title,
            		message: '<div>' + elemContent.html() + '</div>',
            		buttons: 'id_msgClose:' + closeValue + ':delete',
            		effectIn: 'fadeIn,1000',
            		effectOut: '',
            		fadeBackground: true
            		//isHidden: true
        	});
            	$("#id_msgClose").click(function() {ximpia.common.Window.clickMsgOk(true)});
            	$("#id_btX").click(function() {ximpia.common.Window.clickMsgOk(true)});
            	console.log('id_pops');
            	console.log($('#id_pops'));
		var formList = elemContent.children().filter('form');
		for (var i = 0; i<formList.length; i++) {
			console.log(formList[i].id);
			var formData = $("#" + formList[i].id).metadata();
			console.log(formData);
			var callback = eval(formData.callback)
			pageJx.init({	path: ximpia.common.Path.getBusiness(),
				callback: callback,
				formId: formList[i].id,
				verbose: true});
			pageJx.doBusinessGetRequest({	className: formData.className, 
				method: formData.method, mode: 'popupNoView'});
		}
		// Test on render on template origin, then get html
		// Call showMessage with rendered html code
        };
        var methods = {
		init : function( options ) { 
                	return this.each(function() {        
                    		// If options exist, lets merge them
                    		// with our default settings
                    		if ( options ) { 
	                        	$.extend( settings, options );
	                        	$(this).prop('settings', settings);
                    		}					
                	});
		},
		create: function() {
			console.log('create popup!!!');
			// Must validate if we request view or not
			var settings = $(this).prop('settings');
			console.log(settings);
			console.log('path: ' + ximpia.common.Path.getTemplate(settings.app, settings.name));
			// Get the html template for popup
			var path = ximpia.common.Path.getTemplate(settings.app, settings.name);
			console.log('Will get it!!!');
			$.metadata.setType("attr", "data-xp");
			$.get(path, function(data) {
				console.log('Got it...');
				// Save the template in xpData-popup-tmpl sessionStorage variable
				ximpia.common.Browser.setObject('xpData-popup-tmpl', data);
				var idViewList = $(data).find('#id_view');
				if (idViewList.length == 0) {
					console.log('No View!!!!!!!!');
					doCreateNoView({data: data, settings: settings});
				} else {
					console.log('View!!!!!!!!!');
				}
			}).error(function(jqXHR, textStatus, errorThrown) {
				console.log('get ERROR!!!!');
				//$("#id_sect_loading").fadeOut('fast');
				//var html = "<div class=\"loadError\"><img src=\"http://localhost:8000/site_media/images/blank.png\" class=\"warning\" style=\"float:left; padding: 5px;\" /><div>Oops, something did not work right!<br/> Sorry for the inconvenience. Please retry later!</div></div>";
				//$("body").before(html);
			});
		},
		destroy: function() {			
		}
        };
		
        if ( methods[method] ) {
            return methods[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));
        } else if ( typeof method === 'object' || ! method ) {
            return methods.init.apply( this, arguments );
        } else {
            $.error( 'Method ' +  method + ' does not exist on jQuery.xpObjPopUp' );
        }    
		
	};

})(jQuery);
