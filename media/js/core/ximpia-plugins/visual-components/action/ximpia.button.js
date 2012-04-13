/*
 * Ximpia Visual Component 
 * Button
 *
 */

(function($) {
	
	/*
	 * Options accepted by button data-xp
	 * =================================
	 * form: The form id associated with the action
	 * align: left | right
	 * text: Button text, without multi-language. English only
	 * action: pageActionMsg | pageAction | popupAction | popupActionMsg | closePopup | closePanel | action
	 * type: color | icon | iconPopup | simple
	 * icon: add | edit | delete | save | email | like | next | star | spark | play
	 * method: The business method to execute when button is clicked
	 * callback:  The callback function to execute after button is clicked
	 * clickStatus : disable
	 * 
	 * data-xp-action
	 * ==============
	 */	

	$.fn.xpObjButton = function( method ) {  

        // Settings
        var settings = {
        	classButton: "button",
        	classButtonColor: "buttonBlue",
        	modes: {pageActionMsg: 'page', pageAction: 'page', popupAction: 'popup', popupActionMsg: 'popup', pageActionPopUp: 'page'}
        };
        /*
         * Creates the page message bar
         */
        var createPageMsgBar = function(obj) {
        	$("#id_pageButton").xpObjButton('createPageMsgBar');
        	$("#id_btPageMsg").css('top', $("#" + obj.element.id).offset().top-$("#" + obj.element.id).height()-10);
        };
        var createPopupMsgBar = function(obj) {
        	$("#id_popupButton").xpObjButton('createPopupMsgBar');
        	$("#id_btPopupMsg").css('top', $("#" + obj.element.id).offset().top-$("#" + obj.element.id).height()-20);
        	var windowWidth = $("div#PopMsgWrapper").css('width');
        	var index = windowWidth.search('px');
        	var iWindowWidth = windowWidth.substr(0, index);
        	var newWidth = iWindowWidth*.97;
        	$("#id_btPopupMsg").css('width', newWidth + 'px');
        }
        /*
         * Get attributes from form
         */
        var getFormAttrs = function(formId) {
        	$.metadata.setType("attr", "data-xp");
        	var attrs = $("#" + formId).metadata();
        	return attrs;
        };
        /*
         * Get class name for button
         */
        var getClassName = function(attrs) {
        	var className = '';
        	if (attrs.type == 'color') {
        		className = 'button buttonBlue';
        	} else if (attrs.type == 'iconPopup') {
        		className = 'buttonIcon btPop ' + attrs.icon;
        	} else if (attrs.type == 'simple') {
        		className = 'buttonIcon';
        	} else if (attrs.type == 'icon') {
        		className = 'buttonIcon ' + attrs.icon;
        	} else {
        		className = ''
        	}
        	return className;
        };
        /*
         * Do page action with message popup showing errors and result of actions
         */
        var doPageActionMsg = function(obj) {
        	console.log('doPageActionMsg...');
        	var oForm = ximpia.common.Form();
        	console.log(obj.form);
        	var isValid = $("#" + obj.form).valid();
        	console.log('isValid: ' + isValid);
        	$("#id_btPageMsg_img").xpLoadingSmallIcon();
        	if (isValid == true) {
        		createPageMsgBar(obj);
                	$("#id_btPageMsg_img").xpLoadingSmallIcon('wait');
        		$("#id_btPageMsg_text").text('Waiting...');
        		// Set form values from data-xp and action
        		var attrs = getFormAttrs(obj.form)
        		/*console.log('***** Business Class Data **********');
        		console.log(attrs.className + ' ' + obj.method);
        		console.log('**********************************');*/
        		$("#" + obj.form).attr('action', ximpia.common.Path.getBusiness());
        		//$("#id_" + obj.form + "_bsClass").val(attrs.className);
        		console.log('form :: button action : ' + obj.action)
        		$("#id_" + obj.form + "_action").val(obj.action);
        		$("#" + obj.form).submit();
        		/*if (obj.clickStatus == 'disable') {
        			$('#' + obj.element.id).disable();
        		}*/
        	} else {
			createPageMsgBar(obj);
			$("#id_btPageMsg_img").xpLoadingSmallIcon('error');
			$("#id_btPageMsg_text").text($("#id_" + obj.form + "_ERR_GEN_VALIDATION").attr('value'));
        	}
        };
        /*
         * Page action is called and result must be shown in popup window with all the errors
         */
        var doPageActionPopUp = function(obj) {
        	console.log('doPageActionPopUp...');
        	var oForm = ximpia.common.Form();
        	var isValid = $("#" + obj.form).valid();
        	console.log('isValid: ' + isValid);
        	$("#id_btPageMsg_img").xpLoadingSmallIcon();
        	if (isValid == true) {
        		createPageMsgBar(obj);
                	$("#id_btPageMsg_img").xpLoadingSmallIcon('wait');
        		$("#id_btPageMsg_text").text('Waiting...');
        		// Set form values from data-xp and action
        		var attrs = getFormAttrs(obj.form)
        		console.log('Form attributes');
        		console.log(attrs);
        		$("#" + obj.form).attr('action', ximpia.common.Path.getBusiness());
        		//$("#id_" + obj.form + "_bsClass").val(attrs.className);
        		console.log('form :: button action : ' + obj.action)
        		$("#id_" + obj.form + "_action").val(obj.action);
        		$("#" + obj.form).submit();
        	} else {
			createPageMsgBar(obj);
			$("#id_btPageMsg_img").xpLoadingSmallIcon('error');
			$("#id_btPageMsg_text").text($("#id_" + obj.form + "_ERR_GEN_VALIDATION").attr('value'));
        	}
        }
        /*
         * Close the Popup
         */
        var doPopupClose = function(obj) {
        	console.log('doPopupClose...');
        	$('body').xpObjPopUp('destroy');
        };
        /*
         * Execute method of business class defined in form. Show result in message area.
         */
        var doPopupActionMsg = function(obj) {
        	console.log('doPopupActionMsg...');
        	var oForm = ximpia.common.Form();
        	var isValid = $("#" + obj.form).valid();
        	console.log('isValid: ' + isValid);
        	$("#id_btPageMsg_img").xpLoadingSmallIcon();
        	if (isValid == true) {
        		createPopupMsgBar(obj);
                	$("#id_btPopupMsg_img").xpLoadingSmallIcon('wait');
        		$("#id_btPopupMsg_text").text('Waiting...');
        		// Set form values from data-xp and action
        		var attrs = getFormAttrs(obj.form)
        		$("#" + obj.form).attr('action', ximpia.common.Path.getBusiness());
        		//$("#id_" + obj.form + "_bsClass").val(attrs.className);
        		console.log('form :: button action : ' + obj.action)
        		$("#id_" + obj.form + "_action").val(obj.action);
        		$("#" + obj.form).submit();
        	} else {
			createPopupMsgBar(obj);
			$("#id_btPopupMsg_img").xpLoadingSmallIcon('error');
			$("#id_btPopupMsg_text").text($("#id_" + obj.form + "_ERR_GEN_VALIDATION").attr('value'));
        	}        	
        };
        /*
         * 
         */
        var doPopupAction = function(obj) {        	
        };
        var methods = {
		init : function( options ) {
			/*
			 * Initialize plugin
			 */ 
                	return this.each(function() {
                    		// If options exist, lets merge them
                    		// with our default settings
                    		if ( options ) {
	                        	$.extend( settings, options );
                    		}
                	});
		},
		render: function() {
			/*
			 * Render button: Page button, popup button and inline (button anywhere inside panels)
			 */
			//var settings = $(this).prop('settings');
			console.log('Button settings...');
			console.log(settings);
			var oForm = ximpia.common.Form();
			for (var i=0; i<$(this).length; i++) {
				var element = $(this)[i];
				var doRender = ximpia.common.Form.doRender(element, settings.reRender);
				if (doRender == true) {
					var idButton = $(element).attr('id').split('_comp')[0];
					$.metadata.setType("attr", "data-xp");
					var attrs = $(element).metadata();
					var sStyle = "float: left; margin-top: 3px";
					if (attrs.hasOwnProperty('align')) {
						sStyle = "float: " + attrs.align + "; margin-top: 3px";
					}
					// form, action, actionData, type, icon, method, callback, clickStatus
					var dataXp = "{form: '" + attrs.form + "', mode: '" + attrs.mode + "', type: '" + attrs.type + "', icon: '" + attrs.icon + "', action: '" + attrs.action + "', callback: '" + attrs.callback + "', clickStatus: '" + attrs.clickStatus + "'}";
					console.log('form :: dataXp : ' + dataXp);
					// buttonIcon, btPop $buttonBefore
					//<a id="' + sButtonId + '" href="#" class="buttonIcon btPop ' + buttonBefore + '" alt=" " onclick="return false;" >' + sButtonText + '</a>
					var className = getClassName(attrs);
					console.log('className: ' + className);
					var htmlContent = "<div style=\"" + sStyle + "\">"; 
					htmlContent += "<a id=\"" + idButton + "\" href=\"#\" class=\"" + className + "\" data-xp=\"" + dataXp + "\" onclick=\"return false;\"  >";
					htmlContent += "<span>" + attrs.text + "</span></a>";
					htmlContent += "</div>";
					$(element).html(htmlContent);
					$(element).attr('data-xp-render', JSON.stringify(true));
					var classNameList = className.split(' ');
					console.log('classNameList: ' + classNameList);
					console.log('idButton: ' + idButton);
					$("#" + idButton).hover(function() {
						console.log($(this));
						for (var classNameItem in classNameList) {
							$(this).addClass(classNameList[classNameItem] +  '-hover');
						}
					}, function() {
						for (var classNameItem in classNameList) {
							$(this).removeClass(classNameList[classNameItem] +  '-hover');
						}
					});
					$("#" + idButton).mousedown(function() {
						//console.log('mousedown...')
						for (var classNameItem in classNameList) {
							$(this).addClass(classNameList[classNameItem] +  '-active');
						}
					}).mouseup(function(){
						for (var classNameItem in classNameList) {
							$(this).removeClass(classNameList[classNameItem] +  '-active');
						}
					})
					$("#" + idButton).click(function() {
						$(this).xpObjButton('click');
					});
					// callback : We get method if defined. If none defined, will send undefined
					var callback = undefined;
					if (attrs.callback != '') {
						callback = eval(attrs.callback);
					}
					console.log('form :: bind callback : ' + attrs.callback);
					// Bind options to the bindaction for all types of buttons
					// callback, choose form callback or button callback
					if (settings.modes[attrs.mode] == 'page') {
						oForm.bindAction(	{	attrs: attrs, 
										callback: callback, 
										idActionComp: idButton,
										isMsg: true,
										idMsg: 'id_btPageMsg',
										showPopUp: true,
										destroyMethod: 'destroyPageMsgBar'
									});
					} else if (settings.modes[attrs.mode] == 'popup') {
						oForm.bindAction(	{	attrs: attrs, 
										callback: callback, 
										idActionComp: idButton,
										isMsg: true,
										idMsg: 'id_btPopupMsg',
										showPopUp: false,
										destroyMethod: 'destroyPopupMsgBar'
									});
					}					
				}
			}
		},
		click: function() {
			/*
			 * Function to be called when button is clicked. Calls all other action functions
			 */
			var element = $(this)[0];
			$.metadata.setType("attr", "data-xp");
			var attrs = $(element).metadata();
			attrs.element = element;
			var actionType = attrs.mode;
			console.log('actionType: ' + actionType);
			if (actionType == 'pageActionMsg') {
				doPageActionMsg(attrs);
			} else if (actionType == 'closePopup') {
				doPopupClose(attrs);
			} else if (actionType == 'popupActionMsg') {
				doPopupActionMsg(attrs);
			} else if (actionType == 'popupAction') {
				doPopupAction(attrs);
			} else if (actionType == 'pageActionPopUp') {
				doPageActionPopUp(attrs);
			}
		},
		disable: function() {
			/*
			 * Disable button
			 */
			$.metadata.setType("attr", "data-xp");
			var attrs = $(this).metadata();
			var className = getClassName(attrs);
			var classNameList = className.split(' ');			
			if (attrs.type == 'color') {
				$(this).addClass(settings.classButtonColor +  '-disabled');
			} else if (attrs.type == 'iconPopup') {
				$(this).addClass('buttonIcon-disabled');
			}
	   		$(this).css('cursor', 'default');
	   		$(this).unbind('mouseenter mouseleave click mousedown mouseup');
		},
		enable: function() {
			/*
			 * Enable button 
			 */
		},
		createPageMsgBar: function() {
			/*
			 * Creates the page bar to place buttons. Places the bar at right position
			 */
			if ($("#id_btPageMsg").length == 0) {
				var htmlContent = "<div id=\"id_btPageMsg\" class=\"btMsg\">";
				htmlContent += "<div style=\"top: -5px; border: 0px solid; height: 25px; margin-top: 0px; padding: 0px; float: left\">";
				htmlContent += "<img id=\"id_btPageMsg_img\" src=\"http://localhost:8000/site_media/images/blank.png\" alt=\" \" class=\"AjaxButtonLoading\" style=\"margin-top: -6px\" />";
				htmlContent += "<span id=\"id_btPageMsg_text\">Waiting...</span>";
				htmlContent += "</div>";
				htmlContent += "<div id=\"id_btPageMsg_close\" class=\"listFieldDel\" style=\"float: right; margin-right: 7px; margin-top: 5px\">X</div>";
				htmlContent += "</div>\r\n";
				$(this).before(htmlContent);
				// Bind close page message bar
				$("#id_btPageMsg_close").click(function() {
					$(this).xpObjButton('destroyPageMsgBar');
				});				
			}
		},
		createPopupMsgBar: function() {
			/*
			 * Creates the popup bar to show message.
			 */
			if ($("#id_btPopupMsg").length == 0) {
				var htmlContent = "<div id=\"id_btPopupMsg\" class=\"btMsgPopup\">";
				htmlContent += "<div style=\"top: -5px; border: 0px solid; height: 25px; margin-top: 0px; padding: 0px; float: left\">";
				htmlContent += "<img id=\"id_btPopupMsg_img\" src=\"http://localhost:8000/site_media/images/blank.png\" alt=\" \" class=\"AjaxButtonLoading\" style=\"margin-top: -6px\" />";
				htmlContent += "<span id=\"id_btPopupMsg_text\">Waiting...</span>";
				htmlContent += "</div>";
				htmlContent += "<div id=\"id_btPopupMsg_close\" class=\"listFieldDel\" style=\"float: right; margin-right: 7px; margin-top: 5px\">X</div>";
				htmlContent += "</div>\r\n";
				$(this).before(htmlContent);
				// Bind close page message bar
				$("#id_btPopupMsg_close").click(function() {
					$(this).xpObjButton('destroyPopupMsgBar');
				});				
			}
		},
		destroyPageMsgBar: function() {
			$("#id_btPageMsg").remove();
		},
		destroyPopupMsgBar: function() {
			$("#id_btPopupMsg").remove();
		}
        };
		
        if ( methods[method] ) {
            return methods[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));
        } else if ( typeof method === 'object' || ! method ) {
            return methods.init.apply( this, arguments );
        } else {
            $.error( 'Method ' +  method + ' does not exist on jQuery.xpObjButton' );
        }    
		
	};

})(jQuery);
