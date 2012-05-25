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
        /**
         * 
         */
        var doCreateMessage = function(obj) {
        };
        /**
         * 
         */
        var doCreateNoView = function(obj) {
        	var data = obj.data;
        	var settings = obj.settings;
        	var pageJx = ximpia.common.PageAjax();
        	var viewData = ximpia.common.Window.getViewAttrs();
        	ximpia.console.log('viewData...');
        	ximpia.console.log(viewData);
        	ximpia.console.log(data);
        	var elemContent = $(data).find('#id_' + settings.name);
        	var popupData = $(data).filter('#id_conf').metadata();
        	var elementButtons = $(data).filter('#id_sectionButton');        	
        	ximpia.console.log('popupData...');
        	ximpia.console.log(popupData);
        	var height = null;
        	var width = null;
        	if (popupData.height) height = popupData.height;
        	if (popupData.width) width = popupData.width;
        	ximpia.common.Window.showMessage({
            		title: popupData.title,
            		message: '<div class="msgPopBody">' + elemContent.html() + '</div>',
            		//buttons: 'id_msgClose:' + closeValue + ':delete',
            		buttons: elementButtons.html(),
            		//effectIn: 'fadeIn,1000',
            		effectIn: {style: 'fadeIn', time: 1000},
            		effectOut: {},
            		fadeBackground: true,
            		height: height,
            		width: width
            		//isHidden: true
        	});
            	$("#id_msgClose").click(function() {ximpia.common.Window.clickMsgOk(true)});
            	$("#id_btX").click(function() {ximpia.common.Window.clickMsgOk(true)});
            	ximpia.console.log('id_pops...');
            	ximpia.console.log($('#id_pops'));
            	ximpia.console.log('viewName: ' + viewData.viewName),
		pageJx.getView({ view: viewData.viewName, mode: 'popupNoView' });
            	ximpia.console.log('I am done!!!');
        };
        /**
         * 
         */
        var doCreateView = function(obj) {
        	var settings = $(this).prop('settings');
        	var pageJx = ximpia.common.PageAjax();
		// Parse DOM template and get div wanted.
		var elemContent = $(data).filter('#id_content').children().filter('#id_' + settings.app + '_' + settings.name + '_' + settings.content);
		// Call server and render popup forms with new PageAjax method
		// Get all forms inside dic section, call server for each and add to js context
		var closeValue = ximpia.common.List.getValue('id_buttonConstants', 'close');
		//ximpia.console.log('closeValue: ' + closeValue);
		var popupData = $(data).filter('#id_' + settings.app + '_' + settings.name + '_conf').metadata();
		//ximpia.console.log('popupData...');
		//ximpia.console.log(popupData);
		//ximpia.console.log($(data).filter('#id_SN_passwordReminder_conf'));
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
            	ximpia.console.log('id_pops');
            	ximpia.console.log($('#id_pops'));
		var formList = elemContent.children().filter('form');
		for (var i = 0; i<formList.length; i++) {
			ximpia.console.log(formList[i].id);
			var formData = $("#" + formList[i].id).metadata();
			ximpia.console.log(formData);
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
			ximpia.console.log('create popup!!!');
			// Must validate if we request view or not
			var settings = $(this).prop('settings');
			ximpia.console.log(settings);
			ximpia.console.log('path: ' + ximpia.common.Path.getTemplate(settings.app, settings.name));
			// Get the html template for popup
			var path = ximpia.common.Path.getTemplate(settings.app, settings.name, 'popup');
			ximpia.console.log('Will get it!!!');
			ximpia.console.log('path: ' + path);
			$.metadata.setType("attr", "data-xp");
			$.get(path, function(data) {
				ximpia.console.log('Got it...');
				// Save the template in xpData-popup-tmpl sessionStorage variable
				ximpia.common.Browser.setObject('xpData-popup-tmpl', data);
				var idViewList = $(data).find('#id_view');
				if (idViewList.length == 0) {
					ximpia.console.log('Popup No View!!!!!!!!');
					doCreateNoView({data: data, settings: settings});
				} else {
					ximpia.console.log('Popup View!!!!!!!!!');
					doCreateView({data: data, settings: settings});
				}
			}).error(function(jqXHR, textStatus, errorThrown) {
				ximpia.console.log('get html template ERROR!!!!');
				//$("#id_sect_loading").fadeOut('fast');
				//var html = "<div class=\"loadError\"><img src=\"http://localhost:8000/site_media/images/blank.png\" class=\"warning\" style=\"float:left; padding: 5px;\" /><div>Oops, something did not work right!<br/> Sorry for the inconvenience. Please retry later!</div></div>";
				//$("body").before(html);
			});
		},
		createMsg: function() {
			ximpia.console.log('create message popup!!!');
			var settings = $(this).prop('settings');
			ximpia.console.log(settings);
			var height = 50;
			if (settings.hasOwnProperty('height')) {
				height = settings.height;
			}
			ximpia.console.log('createMsg :: height: ' + height);
        		ximpia.common.Window.showMessage({
	            		title: settings.title,
            			message: settings.message,
            			buttons: '<div id="id_popupButton" class="btBar"><div id="id_doClose_comp" data-xp-type="button" data-xp="{align: \'right\', text: \'Close\', type: \'iconPopup\', mode: \'closePopup\', icon: \'delete\'}" ></div></div>',
            			effectIn: {style: 'fadeIn', time: 1000},
            			effectOut: {},
            			fadeBackground: true,
            			height: height
        		});
        		// height: 50
            		//$("#id_doClose").click(function() {ximpia.common.Window.clickMsgOk(true)});
            		$("#id_btX").click(function() {ximpia.common.Window.clickMsgOk(true)});
            		$("#id_msgClose").click(function() {ximpia.common.Window.clickMsgOk(true)});
            		$("[data-xp-type='button']").xpObjButton('render');
            		$('div#id_popupButton.btBar').css('visibility', 'visible');
		},
		destroy: function() {
			ximpia.console.log('Will destroy popup...');
			$("div.PopMessage").fadeOut('fast');
			$("#Wrapper").fadeTo("fast", 1.0);
			$("#id_pops").remove()
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
