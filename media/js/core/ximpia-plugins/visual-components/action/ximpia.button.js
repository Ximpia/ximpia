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
	 * mode: actionMsg | action | closePopup | closeView
	 * action: Action that executes the button
	 * type: color | icon | iconPopup | simple
	 * icon: add | edit | delete | save | email | like | next | star | spark | play
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
        	modes: {actionMsg: 'page', action: 'page', popupAction: 'popup', popupActionMsg: 'popup'},
        	callbacks: {login: 'ximpia.site.Login.doLogin', logout: 'ximpia.site.Login.doLogout'}
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
         * Create the title message bar
         */
        var createTitleMsgBar = function(obj) {
        	// TODO: Address the issue of variable height of the title bar
        	$("#id_titleButton").xpObjButton('createTitleMsgBar');
        	$("#id_btTitleMsg").css('top', $("#" + obj.element.id).offset().top-$("#" + obj.element.id).height()+20);
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
         * Do action with message popup showing errors and result of actions
         */
        var doActionMsg = function(obj) {
        	console.log('doActionMsg...');
        	var oForm = ximpia.common.Form();
        	console.log(obj.form);
        	var isValid = $("#" + obj.form).valid(); 
        	console.log('isValid: ' + isValid);
        	var objMap = {	page: 'Page', title: 'Title', popup: 'Popup'	};
        	$("#id_bt" + objMap[obj.viewType] + "Msg_img").xpLoadingSmallIcon();
        	if (isValid == true) {
        		if (obj.viewType == 'page') {
        			createPageMsgBar(obj);
        		} else if (obj.viewType == 'title') {
        			createTitleMsgBar(obj);
        		}
                	$("#id_bt" + objMap[obj.viewType] + "Msg_img").xpLoadingSmallIcon('wait');
        		$("#id_bt" + objMap[obj.viewType] + "Msg_text").text('Waiting...');
        		// Set form values from data-xp and action
        		var attrs = getFormAttrs(obj.form)
        		$("#" + obj.form).attr('action', ximpia.common.Path.getBusiness());
        		//$("#id_" + obj.form + "_bsClass").val(attrs.className);
        		console.log('form :: button action : ' + obj.action)
        		$("#id_" + obj.form + "_action").val(obj.action);
        		$("#" + obj.form).submit();
        	} else {
        		if (obj.viewType == 'page') {
        			createPageMsgBar(obj);
        		} else if (obj.viewType == 'title') {
        			createTitleMsgBar(obj);
        		}
			$("#id_bt" + objMap[obj.viewType] + "Msg_img").xpLoadingSmallIcon('error');
			$("#id_bt" + objMap[obj.viewType] + "Msg_text").text($("#id_" + obj.form + "_ERR_GEN_VALIDATION").attr('value'));
        	}
        };
        /*
         * Close the Popup
         */
        var doPopupClose = function(obj) {
        	console.log('doPopupClose...');
        	$('body').xpObjPopUp('destroy');
        };
        /*
         * Executes an action and another view is shown
         */
        var doAction = function(obj) {
        	console.log('doAction...');
        	var oForm = ximpia.common.Form();
        	console.log(obj.form);
        	var isValid = $("#" + obj.form).valid();
        	console.log('isValid: ' + isValid);
        	var objMap = {	page: 'Page', title: 'Title', popup: 'Popup'	};
        	$("#id_bt" + objMap[obj.viewType] + "Msg_img").xpLoadingSmallIcon();
        	if (isValid == true) {
        		if (obj.viewType == 'page') {
        			createPageMsgBar(obj);
        		} else if (obj.viewType == 'title') {
        			createTitleMsgBar(obj);
        		}
                	$("#id_bt" + objMap[obj.viewType] + "Msg_img").xpLoadingSmallIcon('wait');
        		$("#id_bt" + objMap[obj.viewType] + "Msg_text").text('Waiting...');
        		// Set form values from data-xp and action
        		var attrs = getFormAttrs(obj.form)
        		$("#" + obj.form).attr('action', ximpia.common.Path.getBusiness());
        		//$("#id_" + obj.form + "_bsClass").val(attrs.className);
        		console.log('form :: button action : ' + obj.action)
        		$("#id_" + obj.form + "_action").val(obj.action);
        		$("#" + obj.form).submit();
        	} else {
        		if (obj.viewType == 'page') {
        			createPageMsgBar(obj);
        		} else if (obj.viewType == 'title') {
        			createTitleMsgBar(obj);
        		}
			$("#id_bt" + objMap[obj.viewType] + "Msg_img").xpLoadingSmallIcon('error');
			$("#id_bt" + objMap[obj.viewType] + "Msg_text").text($("#id_" + obj.form + "_ERR_GEN_VALIDATION").attr('value'));
        	}
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
					var idParent = $(element).parent().attr('id')
					console.log('idParent: ' + idParent);
					if (idParent == 'id_pageButton') {
						attrs.viewType = 'page';
					} else if (idParent == 'id_titleButton') {
						attrs.viewType = 'title';
					} else if (idParent == 'id_popupButton') {
						attrs.viewType = 'popup';
					}
					console.log('attrs.viewType : ' + attrs.viewType);
					var sStyle = "float: left; margin-top: 3px";
					if (attrs.hasOwnProperty('align')) {
						sStyle = "float: " + attrs.align + "; margin-top: 3px";
					}
					// form, action, actionData, type, icon, method, callback, clickStatus
					var dataXp = "{form: '" + attrs.form + "', mode: '" + attrs.mode + "', type: '" + attrs.type + "', icon: '" + attrs.icon + "', action: '" + attrs.action + "', callback: '" + attrs.callback + "', clickStatus: '" + attrs.clickStatus + "', viewType: '" + attrs.viewType + "'}";
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
					console.log('callback: ' + attrs.callback + ' ' +  settings.callbacks[attrs.callback]);
					if (attrs.callback != '') {
						callback = eval(settings.callbacks[attrs.callback]);
					}
					console.log('form :: bind callback : ' + attrs.callback);
					// Bind options to the bindaction for all types of buttons
					// callback, choose form callback or button callback
					var obj = {	attrs: attrs, 
							callback: callback, 
							idActionComp: idButton};
					if (attrs.mode == 'actionMsg') {
						obj.isMsg = true;
					} else if(attrs.mode == 'action') {
						obj.isMsg = false;
					}
					if (attrs.viewType == 'popup') {
						obj.idMsg = 'id_btPopupMsg';
						obj.showPopup = false;
						obj.destroyMethod = 'destroyPopupMsgBar';
					} else if (attrs.viewType == 'page') {
						obj.idMsg = 'id_btPageMsg';
						obj.showPopup = true;
						obj.destroyMethod = 'destroyPageMsgBar';
					} else if (attrs.viewType == 'title') {
						obj.idMsg = 'id_btPopupMsg';
						obj.showPopup = true;
						obj.destroyMethod = 'destroyTitleMsgBar';
					}
					oForm.bindAction( obj );		
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
			if (actionType == 'actionMsg') {
				doActionMsg(attrs);
			} else if (actionType == 'action') {
				doAction(attrs);
			} else if (actionType == 'closePopup') {
				doPopupClose(attrs);
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
		createTitleBar: function() {
			if ($("#id_btTitleMsg").length == 0) {
				var htmlContent = "<div id=\"id_btTitleMsg\" class=\"btMsg\">";
				htmlContent += "<div style=\"top: -5px; border: 0px solid; height: 25px; margin-top: 0px; padding: 0px; float: left\">";
				htmlContent += "<img id=\"id_btTitleMsg_img\" src=\"http://localhost:8000/site_media/images/blank.png\" alt=\" \" class=\"AjaxButtonLoading\" style=\"margin-top: -6px\" />";
				htmlContent += "<span id=\"id_btTitleMsg_text\">Waiting...</span>";
				htmlContent += "</div>";
				htmlContent += "<div id=\"id_btTitleMsg_close\" class=\"listFieldDel\" style=\"float: right; margin-right: 7px; margin-top: 5px\">X</div>";
				htmlContent += "</div>\r\n";
				$(this).before(htmlContent);
				// Bind close page message bar
				$("#id_btTitleMsg_close").click(function() {
					$(this).xpObjButton('destroyTitleMsgBar');
				});				
			}
		},
		destroyPageMsgBar: function() {
			$("#id_btPageMsg").remove();
		},
		destroyPopupMsgBar: function() {
			$("#id_btPopupMsg").remove();
		},
		destroyTitleMsgBar: function() {
			$("#id_btTitleMsg").remove();
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
