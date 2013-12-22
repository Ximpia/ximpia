
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
	 * mode: actionMsg | action | closePopup | closeView | contentInsert
	 * action: Action that executes the button
	 * type: color | icon | iconPopup | simple
	 * icon: add | edit | delete | save | email | like | next | star | spark | play
	 * callback:  The callback function to execute after button is clicked
	 * title [optional] : Tooltip for button
	 * titleDisabled [optional] : Title to show when state is disabled
	 * clickStatus : disable : Button status when button has been clicked and action processed.
	 * 
	 * data-xp-action
	 * ==============
	 */	

	$.fn.xpButton = function( method ) {  

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
        	$("#id_pageButton").xpButton('createPageMsgBar');
        	$("#id_btPageMsg").css('top', $("#" + obj.element.id).offset().top);
        	var newTop = $("#" + obj.element.id).offset().top-$("#" + obj.element.id).height()-10;
        	$("#id_btPageMsg").animate({
        		top: newTop
        	});
        };
        var createPopupMsgBar = function(obj) {
        	$("#id_popupButton").xpButton('createPopupMsgBar');
        	var offset_vars = $(".MsgButtons").offset();
        	$("#id_btPopupMsg").offset({top: $(".MsgButtons").position().top+53, left: offset_vars.left+3});
        	var windowWidth = $("div#PopMsgWrapper").css('width');
        	var index = windowWidth.search('px');
        	var iWindowWidth = windowWidth.substr(0, index);
        	var newWidth = iWindowWidth*.99;
        	$("#id_btPopupMsg").css('width', newWidth + 'px');
        }
        /*
         * Create the title message bar
         */
        var createTitleMsgBar = function(obj) {
        	// TODO: Address the issue of variable height of the title bar
        	$("#id_titleButton").xpButton('createTitleMsgBar');
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
        		className = '';
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
        	ximpia.console.log('viewType: ' + obj.viewType);
        	if (isValid == true) {
        		// Set form values from data-xp and action
        		var attrs = getFormAttrs(obj.form);
        		var cancelAction = false;
        		if (obj.action == 'save') {
        			// process parameters sent to action through data-xp-params
        			$("#" + obj.form).attr('action', ximpia.common.Path.getSave());
        		} else if (obj.action == 'delete') {
        			// process parameters sent to action through data-xp-params
        			var doDelete = confirm('Are you sure you want to delete it?');
        			if (doDelete == true) {
        				$("#" + obj.form).attr('action', ximpia.common.Path.getDelete());
        			} else {
        				cancelAction = true;
        			}
        		}else {
        			$("#" + obj.form).attr('action', ximpia.common.Path.getBusiness());
        		}
        		if (cancelAction == false) {
	        		if (obj.viewType == 'page') {
	        			createPageMsgBar(obj);
	        		} else if (obj.viewType == 'popup') {
	        			createPopupMsgBar(obj);
	        		} else if (obj.viewType == 'title') {
	        			createTitleMsgBar(obj);
	        		}
	                $("#id_bt" + objMap[obj.viewType] + "Msg_img").xpLoadingSmallIcon('wait');
	        		$("#id_bt" + objMap[obj.viewType] + "Msg_text").text('Waiting...');
	        		$("#" + obj.form).append('<input type="hidden" name="form" value="' + obj.form.split('_')[1] + '" />');
	        		console.log('form :: button action : ' + obj.action);
	        		$("#id_" + obj.form + "_action").val(obj.action);
	        		$("#" + obj.form).submit();        			
        		}
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
        	$('body').xpPopUp('destroy');
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
        		var attrs = getFormAttrs(obj.form);
        		$("#" + obj.form).attr('action', ximpia.common.Path.getBusiness());
        		console.log('form :: button action : ' + obj.action);
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
			console.log('Button settings...');
			console.log(settings);
			var oForm = ximpia.common.Form();
			for (var i=0; i<$(this).length; i++) {
				var element = $(this)[i];
				var doRender = ximpia.common.Form.doRender(element, settings.reRender);
				if (doRender == true) {
					var idButton = $(element).attr('id');
					$.metadata.setType("attr", "data-xp");
					var attrs = $(element).metadata();
					var idParent = $(element).parent().attr('id');
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
						sStyle = "float: " + attrs.align;
					}
					// form, action, actionData, type, icon, method, callback, clickStatus
					var dataXp = "{form: '" + attrs.form + "', mode: '" + attrs.mode + "', type: '" + attrs.type + "', icon: '" + attrs.icon + "', action: '" + attrs.action + "', callback: '" + attrs.callback + "', clickStatus: '" + attrs.clickStatus + "', viewType: '" + attrs.viewType + "'}";
					console.log('form :: dataXp : ' + dataXp);
					// buttonIcon, btPop $buttonBefore
					var className = getClassName(attrs);
					console.log('className: ' + className);
					var htmlContent = "<div style=\"" + sStyle + "\">"; 
					htmlContent += "<a id=\"" + idButton + "\" href=\"#\" class=\"" + className + "\" data-xp=\"" + dataXp + "\" onclick=\"return false;\"  >";
					htmlContent += "<span>" + attrs.text + "</span></a>";
					htmlContent += "</div>";
					$(element).html(htmlContent);
					$(element).attr('data-xp-render', JSON.stringify(true));
					if (attrs.hasOwnProperty('title')) {
						$('#' + idButton).attr('data-xp-title', attrs.title);
					}
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
						$(this).xpButton('click');
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
			var myId = $(this).attr('id'); 
			var isRendered = $('#' + myId).attr('data-xp-render');
			$.metadata.setType("attr", "data-xp");
			var attrs = $(this).metadata();
			oform = ximpia.common.Form();
			var timeout = setInterval(function() {
				if (isRendered == 'true') {
					var className = getClassName(attrs);
					var classNameList = className.split(' ');
					if (attrs.type == 'color') {
						$('#'+ myId + ' a').addClass(settings.classButtonColor +  '-disabled');
					} else if (attrs.type == 'iconPopup') {
						$('#'+ myId + ' a').addClass('buttonIcon-disabled');
					}
			   		$('#'+ myId + ' a').css('cursor', 'default');
			   		$('#'+ myId + ' a').unbind('mouseenter mouseleave click mousedown mouseup');
			   		if (attrs.hasOwnProperty('titleDisabled')) {
			   			$('#' + myId + ' a').attr('data-xp-title', attrs.titleDisabled);
			   			oform.doBindButton($('#' + myId + ' a'));
			   		}
					clearInterval(timeout);
				}
				isRendered = $('#' + myId).attr('data-xp-render');
			}, 100);

		},
		enable: function() {
			/*
			 * Enable button 
			 */
			var myId = $(this).attr('id');
			$.metadata.setType("attr", "data-xp");
			var attrs = $(this).metadata();
			var className = getClassName(attrs);
			var classNameList = className.split(' ');
			if (attrs.type == 'color') {
				$('#'+ myId + ' a').removeClass(settings.classButtonColor +  '-disabled');
			} else if (attrs.type == 'iconPopup') {
				$('#'+ myId + ' a').removeClass('buttonIcon-disabled');
			}
			$('#'+ myId + ' a').css('cursor', 'pointer');
			var idButton = myId;
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
				$(this).xpButton('click');
			});
	   		if (attrs.hasOwnProperty('title')) {
	   			$('#' + myId + ' a').attr('data-xp-title', attrs.title);
	   			oform.doBindButton($('#' + myId + ' a'));
	   		} else {
	   			// Must unbind tooltip
	   			$('#' + myId + ' a').qtip('destroy');
	   		}
		},
		/*
		 * Unrender button: delete content inside component and remove attribute ``data-xp-render``
		 */
		unrender: function() {
			var myId = $(this).attr('id');			
			var timeout = setInterval(function() {
				isRendered = $('#' + myId).attr('data-xp-render');
				ximpia.console.log('xpButton.unrender :: isRendered: ' + isRendered);
				if (isRendered == 'true') {
					$('#' + myId).empty();
					$('#' + myId).removeAttr('data-xp-render');
					clearInterval(timeout);
				}
			}, 100);
		},
		createPageMsgBar: function() {
			/*
			 * Creates the page bar to place buttons. Places the bar at right position
			 */
			if ($("#id_btPageMsg").length == 0) {
				var htmlContent = "<div id=\"id_btPageMsg\" class=\"btMsg\" >";
				htmlContent += "<div style=\"top: -5px; border: 0px solid; height: 25px; margin-top: 0px; padding: 0px; float: left\">";
				htmlContent += "<img id=\"id_btPageMsg_img\" src=\"" + ximpia.settings.SITE_MEDIA_URL + "images/blank.png\" alt=\" \" class=\"AjaxButtonLoading\" style=\"margin-top: -6px\" />";
				htmlContent += "<span id=\"id_btPageMsg_text\">Waiting...</span>";
				htmlContent += "</div>";
				htmlContent += "<div id=\"id_btPageMsg_close\" class=\"listFieldDel\" style=\"float: right; margin-right: 7px; margin-top: 5px\">X</div>";
				htmlContent += "</div>\r\n";
				$(this).before(htmlContent);
				// Bind close page message bar
				$("#id_btPageMsg_close").click(function() {
					$(this).xpButton('destroyPageMsgBar');
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
				htmlContent += "<img id=\"id_btPopupMsg_img\" src=\"" + ximpia.settings.SITE_MEDIA_URL + "images/blank.png\" alt=\" \" class=\"AjaxButtonLoading\" style=\"margin-top: -6px\" />";
				htmlContent += "<span id=\"id_btPopupMsg_text\">Waiting...</span>";
				htmlContent += "</div>";
				htmlContent += "<div id=\"id_btPopupMsg_close\" class=\"listFieldDel\" style=\"float: right; margin-right: 7px; margin-top: 5px\">X</div>";
				htmlContent += "</div>\r\n";
				$(this).before(htmlContent);
				// Bind close page message bar
				$("#id_btPopupMsg_close").click(function() {
					$(this).xpButton('destroyPopupMsgBar');
				});				
			}
		},
		createTitleBar: function() {
			if ($("#id_btTitleMsg").length == 0) {
				var htmlContent = "<div id=\"id_btTitleMsg\" class=\"btMsg\">";
				htmlContent += "<div style=\"top: -5px; border: 0px solid; height: 25px; margin-top: 0px; padding: 0px; float: left\">";
				htmlContent += "<img id=\"id_btTitleMsg_img\" src=\"" + ximpia.settings.SITE_MEDIA_URL + "images/blank.png\" alt=\" \" class=\"AjaxButtonLoading\" style=\"margin-top: -6px\" />";
				htmlContent += "<span id=\"id_btTitleMsg_text\">Waiting...</span>";
				htmlContent += "</div>";
				htmlContent += "<div id=\"id_btTitleMsg_close\" class=\"listFieldDel\" style=\"float: right; margin-right: 7px; margin-top: 5px\">X</div>";
				htmlContent += "</div>\r\n";
				$(this).before(htmlContent);
				// Bind close page message bar
				$("#id_btTitleMsg_close").click(function() {
					$(this).xpButton('destroyTitleMsgBar');
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
            $.error( 'Method ' +  method + ' does not exist on jQuery.xpButton' );
        }    
		
	};

})(jQuery);

/*
 * Context Menu
 * 
 * 
 * ** Attributes**
 * 
 * ** Methods **
 * 
 * * ``render(idMenu:String, items:List)``
 * * ``clickItem(name:String)``
 * 
 * ** Returns **
 *
 */

(function($) {	
	$.fn.xpCtxMenu = function( method ) {  
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
				ximpia.console.log('xpObjCtxMenu :: ***************** ctx ******************');
				ximpia.console.log(ctx);
        			var paramStr = '{';
        			for (param in ctx.params) {
        				paramStr += param + ": '" + ctx.params[param] + "'";
        			}
        			paramStr += '}';
				// data-xp : viewName, actionName, windowType
				var dataXp = "{winType: '" + ctx.winType + "', view: '" + ctx.view + "', action: '" + 
					ctx.action + "', params: " + paramStr + ", app: '" + ctx.app + "'}";
				var liAttr = (ctx.icon != '') ? "class=\"" + ctx.icon + "Small" : '';
				liAttr += (ctx.sep == true) ? ' separator' : '';
				liAttr += "\"";
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
			// Disable link href
		    $(this).click(function(e) {
		    	e.preventDefault();
		    });
			$(this).contextMenu({ menu: idMenu, alignElement: true, isCombo:true, paddingTop: 5},
				function(action, el, pos) {
					ximpia.console.log('xpObjCtxMenu :: itemAction: ' + action);
					$(this).xpCtxMenu('clickItem', action);
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
            $.error( 'Method ' +  method + ' does not exist on jQuery.xpIcon' );
        }    
		
	};

})(jQuery);

/*
 * Ximpia Visual Component 
 * Icon
 *
 */

(function($) {	
	$.fn.xpMenuIcon = function( method ) {  
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
		var path = '';
		if (obj.isDefaultApp) {
			path = '/' + obj.viewSlug + '/';
		} else {
			path = '/' + obj.appSlug + '/' + obj.viewSlug + '/';
		}
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
					$('#id_sys_selector').xpCtxMenu('render', 'id_ctx_menu_sys', items);
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
				var menuObj = menus['main'][i];
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
					var menuObj = menus['service'][i];
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
					var menuObj = menus['view'][i];
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
				$(this).xpIcon('clickMenu', evt);	
			});
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
            $.error( 'Method ' +  method + ' does not exist on jQuery.xpIcon' );
        }
	};

})(jQuery);

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
 * ** Attributes **
 * 
 * * ``class``
 * * ``textSize``
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
	$.fn.xpLink = function( method ) {  
        // Settings		
        var settings = {
        };
        var doOpenPopup = function(obj) {
        	ximpia.console.log('xpObjLink.doOpenPopup :: Link Open Popup!!!!');
        	ximpia.console.log(obj);
        	// TODO: Call openPopup method in PageAjax
        	// This should call request view and normal popups
        	if (obj.hasOwnProperty('tmplAlias') && obj.tmplAlias.length != 0) {
        		obj.isPopupReqView = false;
        	} else {
        		obj.isPopupReqView = true;
        	}
        	ximpia.console.log('xpObjLink.doOpenPopup :: obj.isPopupReqView: ' + obj.isPopupReqView);
        	$('body').xpPopUp(obj).xpPopUp('create');
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
					var idLink = $(element).attr('id');
					ximpia.console.log('xpObjLink.render :: idLink: ' + idLink);
					$.metadata.setType("attr", "data-xp");
					var attrs = $(element).metadata();
					ximpia.console.log('xpObjLink.render :: Link Attrs...');
					ximpia.console.log(attrs);
					// TODO: We should give these to open popup: tmplAlias
					// tmplAlias should resolve into a tmpl using the result context
					// In case no app, we get the default application from the response object in session storage
					if (!attrs.hasOwnProperty('app')) {
						attrs.app = ximpia.common.Browser.getApp();
					}
                    if (!attrs.hasOwnProperty('class')) {
                        attrs['class'] = '';
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
					htmlContent += " class=\"xpLink " + attrs['class'] + "\"><span>" + attrs.linkText + "</span></a>";
					ximpia.console.log(htmlContent);
					$(element).html(htmlContent);
					$(element).attr('data-xp-render', JSON.stringify(true));
					if (attrs.hasOwnProperty('textSize')) {
					    $(element).children('a').children('span').css('font-size', '1.6em');
					}
					$("#" + idLink).click(function(evt) {
						// preventDefault in case not url operation 
						evt.preventDefault();
						// Check if disable
						ximpia.console.log('xpObjLink.render :: event...');
						ximpia.console.log(evt);
						var isDisabled = $(this).attr('disabled');
						ximpia.console.log('xpObjLink.render :: isDisabled: ' + isDisabled);
						if (!isDisabled) {
							$(this).xpLink('click');
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
			var idLink = $(element).attr('id');
			$("#" + idLink).attr('disabled', 'true');
		},
		enable: function() {
			var element = $(this)[0];
			ximpia.console.log('xpObjLink.enable :: element: ' + element);
			var idLink = $(element).attr('id');
			$("#" + idLink).removeAttr('disabled');
		}
        };		
        if ( methods[method] ) {
            return methods[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));
        } else if ( typeof method === 'object' || ! method ) {
            return methods.init.apply( this, arguments );
        } else {
            $.error( 'Method ' +  method + ' does not exist on jQuery.xpLink' );
        }    		
	};

})(jQuery);
