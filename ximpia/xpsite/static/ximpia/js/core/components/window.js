
/*
 * 
 * 
 * Copyright 2013 Ximpia, Inc
 * 
 *    Licensed under the Apache License, Version 2.0 (the "License");
 *    you may not use this file except in compliance with the License.
 *    You may obtain a copy of the License at
 * 
 *        http://www.apache.org/licenses/LICENSE-2.0
 * 
 *    Unless required by applicable law or agreed to in writing, software
 *    distributed under the License is distributed on an "AS IS" BASIS,
 *    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *    See the License for the specific language governing permissions and
 *    limitations under the License. 
 * 
 * 
 */

/*
 * Ximpia Visual Component 
 * Popup
 * 
 * TODO: Include the html for component
 *
 */

(function($) {	
	$.fn.xpPopUp = function( method ) {  
        // Settings		
        var settings = {
        };
        /**
         * 
         */
        var doCreateMessage = function(obj) {
        };
        /**
         * Create popup with existing view
         */
        var doCreate = function(obj) {
		ximpia.console.log('xpObjPopUp :: Popup with existing view!!!!!!!!');
		ximpia.console.log('xpObjPopUp :: viewName : ' + obj.view);
		// Get the html template for popup
		var responseMap = ximpia.common.Browser.getObject('xpData-view');
		ximpia.console.log('xpObjPopUp :: reponseMap...');
		ximpia.console.log(responseMap);
		var tmplName = responseMap['response']['tmpl'][obj.tmplAlias];
		ximpia.console.log('xpObjPopUp :: tmplName: ' + tmplName);
		// Get application code from somewhere else
		var path = ximpia.common.Path.getTemplate(obj.app, tmplName, 'popup');
		ximpia.console.log('xpObjPopUp :: path: ' + path);
		ximpia.console.log('xpObjPopUp :: Will get it!!!');
		ximpia.console.log('xpObjPopUp :: path: ' + path);
		$.metadata.setType("attr", "data-xp");
		$.get(path, function(data) {
			ximpia.console.log('xpObjPopUp :: Got it...');
			// Save the template in xpData-popup-tmpl sessionStorage variable
			ximpia.common.Browser.setObject('xpData-popup-tmpl', data);
        	ximpia.console.log(data);
        	ximpia.console.log('xpObjPopUp :: content: #id_' + obj.name);
        	var elemContent = $(data).find('#id_' + obj.name);
        	var popupData = $(data).filter('#id_popup').metadata();
        	var elementButtons = $(data).filter('#id_sectionButton');        	
        	ximpia.console.log('xpObjPopUp :: popupData...');
        	ximpia.console.log(popupData);
        	var height = null;
        	var width = null;
        	if (popupData.height) height = popupData.height;
        	if (popupData.width) width = popupData.width;
        	ximpia.common.Window.showMessage({
            		title: popupData.title,
            		message: '<div class="msgPopBody">' + elemContent.html() + '</div>',
            		buttons: elementButtons.html(),
            		effectIn: {style: 'fadeIn', time: 500},
            		effectOut: {},
            		fadeBackground: true,
            		height: height,
            		width: width
        	});
        	$("#id_msgClose").click(function(evt) {ximpia.common.Window.clickMsgOk(evt, true)});
        	$("#id_btX").click(function(evt) {ximpia.common.Window.clickMsgOk(evt, true)});
        	ximpia.console.log('xpObjPopUp :: id_pops...');
        	ximpia.console.log($('#id_pops'));
        	ximpia.console.log('xpObjPopUp :: viewName: ' + obj.view);
	        // Render poup template
			ximpia.console.log('xpObjPopUp :: doFormPopupNoView...');
			ximpia.console.log(document.forms);
			ximpia.console.log(obj);
			// Get forms for popup
			var popupForms = $('#id_pops').find('form');
			for (var i=0; i<popupForms.length; i++) {
				var xpForm = 'xpData-view-' + obj.view + '.' + popupForms[i].id;
				ximpia.common.PageAjax.doRender(xpForm);
			}			
			$('.btBar').css('visibility', 'visible');
			ximpia.common.PageAjax.doFade();
			// Conditions
			// Post-Page : Page logic
			var oForm = ximpia.common.Form();
			oForm.doBindBubbles();
			ximpia.console.log('xpObjPopUp :: end doFormPopupNoView()');	            	
	        ximpia.console.log('xpObjPopUp :: I am done!!!');								
		}).error(function(jqXHR, textStatus, errorThrown) {
			ximpia.console.log('xpObjPopUp :: get html template ERROR!!!!');
			$("#id_sect_loading").fadeOut(300);
			//var html = "<div class=\"loadError\"><img src=\"http://localhost:8000/site_media/images/blank.png\" class=\"warning\" style=\"float:left; padding: 5px;\" /><div>Oops, something did not work right!<br/> Sorry for the inconvenience. Please retry later!</div></div>";
			//$("body").before(html);
		});
        };
        /**
         * Show popup message associated with a view. First, a waiting icon is rendered, while request is sent to server. Then
         * response from server is rendered into the visual components of popup template
         */
		var doCreateReqView = function(obj) {
        	ximpia.console.log('xpObjPopUp :: doCreateReqView :: Popup Request View!!!!!!!!');
        	ximpia.console.log(obj);
        	// 1. Show Message, waiting icon
        	var waitingImgHtml = "<img id=\"id_btPageMsg_img\" src=\"/static/images/loading.gif\" alt=\" \" style=\"margin-top: -6px\" />";
			waitingImgHtml += "&nbsp;&nbsp; <span id=\"id_btPageMsg_text\">Waiting...</span>";
        	var height= 160;
        	var width= 500;
        	ximpia.common.Window.showMessage({
            		title: '',
            		message: '<div class="msgPopBody">' + waitingImgHtml + '</div>',
            		buttons: '<div id="id_popupButton" class="btBar"><div id="id_doClose_comp" data-xp-type="button" data-xp="{align: \'right\', text: \'Close\', type: \'iconPopup\', mode: \'closePopup\', icon: \'delete\'}" ></div></div>',
            		effectIn: {style: 'fadeIn', time: 500},
            		effectOut: {},
            		fadeBackground: true,
            		height: height,
            		width: width
        	});
        	$("#id_msgClose").click(function(evt) {ximpia.common.Window.clickMsgOk(evt, true)});
        	$("#id_btX").click(function(evt) {ximpia.common.Window.clickMsgOk(evt, true)});
        	ximpia.console.log('xpObjPopUp :: doCreateReqView :: I displayed popup!!!');

        	// 2. Get view and place on sessionStorage, get from view template name
        	ximpia.common.PageAjax.getView( {	view: obj.view,
						params: obj.params,
						app: obj.app} , function(responseMap) {
        		ximpia.console.log('xpObjPopUp :: doCreateReqView :: responseMap...');
        		ximpia.console.log(responseMap);
        		ximpia.common.Browser.setXpDataView(obj.view, responseMap);
            		
			var viewName = responseMap['response']['view'];
			var tmplName = responseMap['response']['tmpl'][viewName];

    		// 3. Get template
    		ximpia.common.PageAjax.getTmpl( {	app: responseMap['response']['app'],
        						name: tmplName,
        						viewType: 'popup'} , function(tmplData) {

			// 4. Render template and view
			//ximpia.console.log('template...');
			//ximpia.console.log(tmplData);
			ximpia.common.Browser.setObject('xpData-popup-tmpl', tmplData);
	       	ximpia.console.log(tmplData);
        	var elemContent = $(tmplData).find('#id_' + obj.view);
        	ximpia.console.log('xpObjPopUp :: doCreateReqView :: elemContent...');
        	ximpia.console.log(elemContent);
        	var popupData = $(tmplData).filter('#id_popup').metadata();
        	var elementButtons = $(tmplData).filter('#id_sectionButton');
        	var hasButtons = true;
        	if ($(elementButtons).html().length <= 1) {
        		hasButtons = false;
        	}
        	/*if (hasButtons == true) {
        		$('.MsgText').css('border-bottom-left-radius', '0px');
        		$('.MsgText').css('border-bottom-right-radius', '0px');
        		$('.MsgButtons').css('border-top-left-radius', '0px');
        		$('.MsgButtons').css('border-top-right-radius', '0px');
        	}*/
        	if (hasButtons == false) {
        		$('.MsgText').css('border-bottom-left-radius', '10px');
        		$('.MsgText').css('border-bottom-right-radius', '10px');
        	}
        	ximpia.console.log('xpObjPopUp :: doCreateReqView :: elementButtons...');
        	ximpia.console.log(elementButtons);
        	ximpia.console.log('xpObjPopUp :: doCreateReqView :: popupData...');
        	ximpia.console.log(popupData);
        	var height = null;
        	var width = null;
        	if (popupData.height) height = popupData.height;
        	if (popupData.width) width = popupData.width;
        	ximpia.console.log('xpObjPopUp :: doCreateReqView :: height: ' + height);
        	ximpia.console.log('xpObjPopUp :: doCreateReqView :: width: ' + width);
        	var form = $(elemContent).find('form')[0];
        	// Insert data from template into message area
        	// Set title => popupData.title
        	$("div.MsgTitle").html('<div style="border: 0px solid; float: left; padding:7px 20px; width: 370px">' + popupData.title + '</div>');
        	// message: '<div class="msgPopBody">' + elemContent.html() + '</div>'
        	$("div.MsgText").html('<div class="msgPopBody">' + elemContent.html() + '</div>');
        	// Set buttons => elementButtons.html()
        	$("div.MsgButtons").text('');
        	$("div.MsgButtons").append(elementButtons.html());
        	// Set popup width and height
        	$("div.PopMessage").css('width', width + 'px');
        	$("div#PopMsgWrapper").css('width', width + 'px');
        	if (height > 400) height = 400;
        	$("div.MsgText").css('height', height + 'px');
        	// Render form from template
        	ximpia.console.log('xpObjPopUp :: doCreateReqView :: form: ...');
        	ximpia.console.log(form);
        	var xpForm = 'xpData-view-' + obj.view + '.' + form.id;
        	ximpia.console.log('xpObjPopUp :: doCreateReqView :: xpForm: ' + xpForm);
        	ximpia.common.PageAjax.doRender(xpForm);
        	$('.btBar').css('visibility', 'visible');
        	ximpia.common.PageAjax.doFade();
        	var oForm = ximpia.common.Form();
        	oForm.doBindBubbles();
			});
		});
        	
        	//var viewData = ximpia.common.Window.getViewAttrs();
        	//ximpia.console.log('viewData...');
        	//ximpia.console.log(viewData);
        	/*ximpia.console.log(data);
        	var elemContent = $(data).find('#id_' + settings.name);
        	var popupData = $(data).filter('#id_popup').metadata();
        	var elementButtons = $(data).filter('#id_sectionButton');
        	ximpia.console.log('popupData...');
        	ximpia.console.log(popupData);
        	var height = null;
        	var width = null;
        	if (popupData.height) height = popupData.height;
        	if (popupData.width) width = popupData.width;*/
        	/*var settings = $(this).prop('settings');
        	var pageJx = ximpia.common.PageAjax();
		var elemContent = $(data).filter('#id_content').children().filter('#id_' + settings.app + '_' + settings.name + '_' + settings.content);
		var closeValue = ximpia.common.List.getValue('id_buttonConstants', 'close');
		var popupData = $(data).filter('#id_' + settings.app + '_' + settings.name + '_conf').metadata();*/		
        	
        	/*ximpia.common.Window.showMessage({
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
		// Call showMessage with rendered html code*/
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
			var obj = $(this).prop('settings');
			ximpia.console.log(obj);
			ximpia.console.log('isPopupReqView: ' + obj.isPopupReqView);			
			
			if (obj.isPopupReqView == false) {
				// Popup No View
				ximpia.console.log('Popup View ..');
				doCreate(obj);
			} else {
				// Popup view
				ximpia.console.log('Popup Request View...');
				doCreateReqView(obj);
			}
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
            		$("[data-xp-type='button']").xpButton('render');
            		$('div#id_popupButton.btBar').css('visibility', 'visible');
		},
		destroy: function() {
			ximpia.console.log('Will destroy popup...');
			$("div.PopMessage").fadeOut('fast');
			$("#Wrapper").fadeTo("fast", 1.0);
			$("#id_pops").remove()
			//alert('Closing popup...');
		}
        };
		
        if ( methods[method] ) {
            return methods[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));
        } else if ( typeof method === 'object' || ! method ) {
            return methods.init.apply( this, arguments );
        } else {
            $.error( 'Method ' +  method + ' does not exist on jQuery.xpPopUp' );
        }    
		
	};

})(jQuery);
