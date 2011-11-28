var ximpia = ximpia || {};
ximpia.common = ximpia.common || {};
ximpia.visual = ximpia.visual || {};
ximpia.site = ximpia.site || {};

ximpia.common.List = {};
ximpia.common.List.getValue = (function(id, key) {
	console.log('value : ' + $("#" + id).attr('value'));
	var array = eval($("#" + id).attr('value'));
	var value = '';
	for (var i=0; i<array.length; i++) {
		var list = array[i];
		if (list[0] == key) {
			value = list[1];
		}
	}
	return value;
});
ximpia.common.List.hasKey = (function(id, key) {	
});
ximpia.common.List.getValueFromList = (function(key, list) {
	for (j in list) {
		if (list[j][0] == key) {
			value = list[j][1];
		}
	}
	return value;
});

ximpia.common.ArrayUtil = {};
ximpia.common.ArrayUtil.hasKey = function(array, keyTarget) {
	var exists = false;
	//console.log(JSON.stringify(array));
	for (key in array) {
		//console.log(key + ' ' + array[key] + ' ' + keyTarget);
		if (array[key] == keyTarget) {
			exists = true;
		}
	}
	return exists;
}

ximpia.common.Choices = {};
ximpia.common.Choices.get = function(choicesId) {
	// Integrate here the new location for choices object
	var list = JSON.parse($('#id_choices').attr('value'))[choicesId];
	return list;
}

/*
ximpia.common.ClassType10 = function() {
	var _attr = {
		priv: {
			_var1 : 9,
			_doSomething: (function() {
				var a = 3;
				alert('No soy lo que crees');
				console.log('Holaaa')
			})
		},
		pub: {
			MY_CONSTANT : 18726,
			myMethod1: (function() {
				alert('myMethod!!!' + _attr.priv.var1);
				var d = 2;
				var j = "Hola";
				console.log('myMethod1...');
				_attr.priv._doSomething();
			})
		}
	};
	return _attr.pub;
};
/**
 * XpClassTypeNew.HO_KO_LOST
 * @type {Number}
 */
/*ximpia.common.ClassType10.HO_KO_LOST = 40;*/


ximpia.common.Window = {};
/**
 * Show Remote Error Window
 */
ximpia.common.Window.showRemoteError = (function() {
	ximpia.common.Window.showPopUp('MessageERROR');
});
/**
 * Show Message Window
 */
ximpia.common.Window.showMessage = (function(messageOptions) {
	ximpia.common.Window.createPopHtml();
        var sTitle = '';
        var sMessage = '';
        var sButtons = 'MsgCPClose:' + eval($("#id_buttonConstants").attr('value'))['close'];
        var sEffectIn = 'fadeIn,1000';
        var sEffectOut = '';
        var bFadeBackground = true;
        var iWidth = null;
        var iHeight = null;
        functionShow = null;
        console.log('Will do...');
        //var htmlPage = "<!-- START POPUP MESSAGE --><div class=\"Pops\"><div id=\"PopMessage\" class=\"PopMessage\"><div id=\"PopMsgWrapper\"><div class=\"MsgTitle\"></div><div style=\"float: right ; width: 21px; margin-top: -40px"><a id=\"id_btX\" href=\"#\" class=\"buttonIcon btX\" onclick=\"return false\" >X</a></div><div class=\"MsgText\" style=\"clear: both\"></div><div class=\"MsgButtons\"></div></div><br class=\"clearfloat\" /></div><!--[if lte IE 6.5]><iframe></iframe><![endif]--></div><!-- END POPUP MESSAGE -->";
        //console.log(htmlPage);
        //$("body").before(htmlPage);
        if (messageOptions.title) sTitle = messageOptions.title;
        if (messageOptions.message) sMessage = messageOptions.message;
        if (messageOptions.buttons) sButtons = messageOptions.buttons;
        if (messageOptions.effectIn) sEffectIn = messageOptions.effectIn;
        if (messageOptions.effectOut) sEffectOut = messageOptions.effectOut;
        if (messageOptions.fadeBackground) bFadeBackground = messageOptions.fadeBackground;
        if (messageOptions.width) iWidth = messageOptions.width;
        if (messageOptions.height) iHeight = messageOptions.height;
        if (messageOptions.functionShow) functionShow = messageOptions.functionShow;
        bFadeOut = ximpia.common.Window.checkFadeOut();
        if (!bFadeOut) {
            bFadeBackground = false;
        }
        iScreenWidth = document.body.clientWidth;
        if (iWidth) {
            $("div.PopMessage").css('width', iWidth + 'px');
            $("div#PopMsgWrapper").css('width', iWidth + 'px');
        }
        else {
            $("div.PopMessage").css('width', '450px');
            $("div#PopMsgWrapper").css('width', '450px');
        }
        if (iHeight) {
            $("div.MsgText").css('height', iHeight + 'px');
            var iTopPosition = 80;
        }
        iLeft = (iScreenWidth/2)- parseInt($("div.PopMessage").css('width'))/2;
        if (!$.browser.msie) {
            iTopOffset = window.pageYOffset;
        }
        else {
            iTopOffset = document.documentElement.scrollTop;
        }
        //alert(sMessage.length);
        if (!iHeight) {
            if (sMessage.length <= 100) {
                //var iTopPosition = 160;
                var iTopPosition = 130;
                $("div.MsgText").css('height', '40px');
                $("div.MsgText").css('overflow', 'hidden');
            }
            else if (sMessage.length <= 250 && sMessage.length > 100) {
                //var iTopPosition = 160;
                var iTopPosition = 130;
                $("div.MsgText").css('height', '150px');
                $("div.MsgText").css('overflow', 'hidden');
            }
            else {
                var iTopPosition = 80;
                $("div.MsgText").css('height', '200px');
                $("div.MsgText").css('overflow', 'auto');
            }
        }
        iTop = iTopPosition + iTopOffset;
        $("div.MsgTitle").html('<div style="border: 0px solid; float: left; padding:7px 20px; width: 370px">' + sTitle + '</div>');
        $("div.MsgText").html(sMessage);
        //$("#PopMsgWrapper .MsgText").html(sMessage);
        ButtonList = sButtons.split(',');
        $("div.MsgButtons").text('');
        for (var i=0; i<ButtonList.length; i++) {
            Fields = ButtonList[i].split(':');
            sButtonId = Fields[0];
            sButtonText = Fields[1];
            buttonBefore = Fields[2];
            $("div.MsgButtons").append('<a id="' + sButtonId + '" href="#" class="buttonIcon btPop ' + buttonBefore + '" alt=" " onclick="return false;" >' + sButtonText + '</a>');
        }
        EffectInList = sEffectIn.split(',');
        sEffectInTxt = EffectInList[0];
        iEffectInTime = parseInt(EffectInList[1]);
        EffectOutList = sEffectOut.split(',');
        sEffectOutTxt = EffectOutList[0];
        iEffectOutTime = parseInt(EffectOutList[1]);        
        $("div.PopMessage").fadeIn('fast');        
        /*if (sEffectInTxt == 'fadeIn') {
            $("div.PopMessage").fadeIn(iEffectInTime);
        }*/   
        $("div.Pops").css('left', iLeft + 'px');
        $("div.Pops").css('top', iTop + 'px');
        $("div.Pops").css('visibility','visible');
        //$("div.PopMessage").fadeOut('slow');
        /*if (sEffectOutTxt == 'fadeOut') {
            $("div.PopMessage").fadeOut(iEffectOutTime);
        }*/
        if (bFadeBackground) {
            $("#Wrapper").fadeTo("fast", 0.50);
        }
        if (functionShow) {
            functionShow($(this));
        }	
});
/**
 * Click Ok Button
 */
ximpia.common.Window.clickMsgOk = (function(bFadeBackground, functionName) {
        bFadeOut = ximpia.common.Window.checkFadeOut();
        $("div.PopMessage").fadeOut('fast');
        if (bFadeBackground) {
            $("#Wrapper").fadeTo("fast", 1.0);
        }
        //$(".Pops").css('left','-2000px');
        if (functionName) {
            functionName();
        }
	if (!bFadeOut) {
            bFadeBackground = false;
        }
        $("#id_pops").remove()
});
/**
 * Construct PopUp html
 */
ximpia.common.Window.createPopHtml = (function() {
	if (!$("#id_pops").length) {
		var htmlPage = "<div id=\"id_pops\" class=\"Pops\" ><div id=\"PopMessage\" class=\"PopMessage\"><div id=\"PopMsgWrapper\"><div class=\"MsgTitle\"></div><div style=\"float: right ; width: 21px; margin-top: -40px\"><a id=\"id_btX\" href=\"#\" class=\"buttonIcon btX\" onclick=\"return false\" >X</a></div><div class=\"MsgText\" style=\"clear: both\"></div><div class=\"MsgButtons\"></div></div><br class=\"clearfloat\" /></div><!--[if lte IE 6.5]><iframe></iframe><![endif]--></div>";
		$("body").append(htmlPage);
	}
});
/**
 * Show Pop Up. It is used for Ajax actions, like OK Message, Error messages, etc...
 */
ximpia.common.Window.showPopUp = (function(key) {
	ximpia.common.Window.createPopHtml();
        if (typeof key == 'string') {
            var sId = key;
            var messageOptions = new Object();
        }
        else {
            var messageOptions = key;
            var sId = '';
        }
        var sFadeOut = '';
        var sUrl = '';
        var sTitle = '';
        var sMessage = '';
        var iHeight = null;
        functionName = null;
        console.log('sId : ' + sId);
        if (sId.length != 0) {
            var popUpData = eval($("#" + sId).attr('value'));
            sTitle = popUpData[0];
            message = popUpData[1].replace(/[:]{2}[p][:]{2}/g,'</p>');
            message = message.replace(/[:][p][:]/g,'<p>');
            sMessage = '<table><tr><td style="vertical-align:top"><img class="' + popUpData[2] + '" src="' + $("#id_siteMedia").attr('value') 
            + 'images/blank.png" /></td><td style="vertical-align:top">' + message + '</td></tr></table>'
        } else {
            sFadeOut = messageOptions.fadeout;
            bFadeOut = messageOptions.fadeBackground;
            sUrl = messageOptions.url;
            sTitle = messageOptions.title;
            sMessage = messageOptions.message;
            iHeight = messageOptions.height;
            functionName = messageOptions.functionName;         
        }
        if (!sFadeOut){
            sFadeOut = ''
            bFadeOut = true;
        }
        else {
            if (sFadeOut == '') {
                bFadeOut = true;
            }
            else {
                bFadeOut = false;
            }
        }
        bIE = ximpia.common.Browser.checkIE();
        if (bIE) {
            bFadeOut = false;
        }
        // This is to prevent fadeouts in popups since Internet Explorer does not show frame border
        sFadeOut = '';
        var closeValue = ximpia.common.List.getValue('id_buttonConstants', 'close');
        ximpia.common.Window.showMessage({
            title: sTitle,
            message: sMessage,
            buttons: 'id_msgClose:' + closeValue + ':delete',
            effectIn: 'fadeIn,1000',
            effectOut: sFadeOut,
            fadeBackground: bFadeOut
        });
        //showMessage(sTitle, sMessage, 'MsgOk:OK', 'fadeIn,1000', sFadeOut, bFadeOut);
        if (sFadeOut == '') {
            $("#id_msgClose").click(function() {ximpia.common.Window.clickMsgOk(bFadeOut, functionName)});
            $("#id_btX").click(function() {ximpia.common.Window.clickMsgOk(bFadeOut, functionName)});
        }
        if (sUrl) {
            if (sUrl != '') {
                $("#id_msgClose").click(function() {
                    window.location = sUrl;
                });
                $("#id_btX").click(function() {
                    window.location = sUrl;
                });
            }
        }	
});
/**
 * Check Fade Out
 */
ximpia.common.Window.checkFadeOut = (function() {
        if (jQuery.browser.msie) {
            bCheck = false;
        }
        else {
            bCheck = true;
        }
        return bCheck	
});

ximpia.common.Page = {};
/**
 * Init page
 */
ximpia.common.Page.init = (function() {
	// Insert basic tags	
	var basicTags = ximpia.common.BasicTags();
	basicTags.pageTags();	
		
	// set up the options to be used for jqDock...  
	var labelTransform = function(labelText, optionIndex){ //scope (this) is the #menu element
		rtn = "<div class='jqDockLabelNew' style='position: relative'>" + labelText + "</div>";
        	return rtn;
      	},
    	dockOptions = { align: 'top' // horizontal menu, with expansion DOWN from a fixed TOP edge
	        , labels: true  // add labels (defaults to 'br')
	        , size: 45
	   	,setLabel: labelTransform
    	};
    	// ...and apply...
    	$('#IconMenu').jqDock(dockOptions);
	// *************************
	// *** jQuery VALIDATORS ***
	// *************************
	//jQuery.validator.messages.required = "";
	// Ximpia Generic Validations
	jQuery.validator.addMethod("ximpiaId", function(value, element) {
		return this.optional(element) || /^[a-zA-Z0-9_.@+-]+$/i.test(value);
	}, "mensaje");
	jQuery.validator.addMethod("password", function(value, element) {
		return this.optional(element) || /^[a-zA-Z0-9$#!&%]+$/i.test(value);
	}, "mensaje");	
});

ximpia.common.Path = {}
/**
 * Get site media path
 */
ximpia.common.Path.getSiteMedia = (function() {
	var siteMedia = "http://localhost:8000/site_media/";
	return siteMedia;
});
/**
 * Get server path
 */
ximpia.common.Path.getServer = (function() {
	var server = "http://localhost:8000/";
	return server;
});

ximpia.common.Browser = {};
/**
 * Check Internet Explorer IE6
 */
ximpia.common.Browser.checkIE6 = (function() {
        if (jQuery.browser.msie && jQuery.browser.version.substr(0,3)=='6.0') {
            bIE6 = true;
        }
        else {
            bIE6 = false;
        }
        return bIE6;	
});
/**
 * Check Internet Explorer
 */
ximpia.common.Browser.checkIE = (function() {
        if (jQuery.browser.msie) {
            bIE = true;
        }
        else {
            bIE = false;
        }
        return bIE	
});
/*
 * Get url parameter value by name
 */
ximpia.common.Browser.fetchParamByName = (function(name) {
	  name = name.replace(/[\[]/,"\\\[").replace(/[\]]/,"\\\]");
	  var regexS = "[\\?&]"+name+"=([^&#]*)";
	  var regex = new RegExp( regexS );
	  var results = regex.exec( window.location.href );
	  if( results == null )
	  	return "";
	  else
	  	return results[1];
});


ximpia.common.BasicTags = function() {
	var _attr = {
		priv: {
			/**
			 * header tag
			 */
			head: function() {
				console.log('head...');
				$.metadata.setType("attr", "data-xp");
				var htmlI = $("head").html();
				var sm = ximpia.common.Path.getSiteMedia();
				var contentLength = $("head meta").length;
				if (contentLength < 1) {
					var attrs = $("head").metadata();
					htmlI = "<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\" />";
					htmlI += "<title>" + attrs.title + "</title>";
					htmlI += "<link rel=\"stylesheet\" href=\"" + sm + "jQueryThemes/start/jquery-ui-1.8.9.custom.css\" type=\"text/css\" />";
					htmlI += "<link href=\"" + sm + "css/main.css\" rel=\"stylesheet\" type=\"text/css\" />";
					htmlI += "<link href=\"" + sm + "css/ximpia.qtip.css\" rel=\"stylesheet\" type=\"text/css\" />";
					$("head").html(htmlI);
				}
			},
			/**
			 * header tag
			 */
			header: function() {
				console.log('header...');
				/**
				 * <div id="Header" >
<div id="Logo">
<a href="http://localhost:8000/"><img id="LogoImg" src="http://localhost:8000/site_media/images/blank.png" alt=" " /> <br/>
<img id="BetaImg" src="http://localhost:8000/site_media/images/blank.png" alt=" " /></a>	
</div>
<nav>
<div id="IconMenu">    	
<img src="http://localhost:8000/site_media/images/add_60.png" title="Signup" alt="Signup" />
<img src="http://localhost:8000/site_media/images/users_two_60.png" title="Friends" alt="Friends" />
<img src="http://localhost:8000/site_media/images/paper_content_60.png" title="About Us" alt="About Us" />
<img src="http://localhost:8000/site_media/images/mail_add_60.png" title="Contact Us" alt="Contact Us" />
<img src="http://localhost:8000/site_media/images/lock_60.png" title="Privacy" alt="Privacy" />
<img src="http://localhost:8000/site_media/images/go_60.png" title="Login" alt="Login" />		
</div>
</nav>
</div>
<!-- End Header -->
				 */
				var htmlI = $("header").html();
				var sm = ximpia.common.Path.getSiteMedia();
				var contentLength = $("header div").length;
				if (contentLength < 1) {
					htmlI = "<div id=\"Header\" >";
					htmlI += "<div id=\"Logo\">";
					htmlI += "<a href=\"http://localhost:8000/\"><img id=\"LogoImg\" src=\"http://localhost:8000/site_media/images/blank.png\" alt=\" \" /> <br/>";
					htmlI += "<img id=\"BetaImg\" src=\"http://localhost:8000/site_media/images/blank.png\" alt=\" \" /></a>";
					htmlI += "</div>";
					htmlI += "<nav>";
					htmlI += "<div id=\"IconMenu\">";
					htmlI += "<img src=\"http://localhost:8000/site_media/images/add_60.png\" title=\"Signup\" alt=\"Signup\" />";
					htmlI += "<img src=\"http://localhost:8000/site_media/images/users_two_60.png\" title=\"Friends\" alt=\"Friends\" />";
					htmlI += "<img src=\"http://localhost:8000/site_media/images/paper_content_60.png\" title=\"About Us\" alt=\"About Us\" />";
					htmlI += "<img src=\"http://localhost:8000/site_media/images/mail_add_60.png\" title=\"Contact Us\" alt=\"Contact Us\" />";
					htmlI += "<img src=\"http://localhost:8000/site_media/images/lock_60.png\" title=\"Privacy\" alt=\"Privacy\" />";
					htmlI += "<img src=\"http://localhost:8000/site_media/images/go_60.png\" title=\"Login\" alt=\"Login\" />";
					htmlI += "</div>";
					htmlI += "</nav>";
					htmlI += "</div>";
					$("header").html(htmlI);
				}
			},
			/**
			 * footer tag
			 */
			footer: function() {
				console.log('footer...');
				/**
				 * <div id="id_footerContent">
<div id="id_footerText">
<div  style=" float: left;; margin-left: 10px; margin-top: -5px">&copy; 2011 &nbsp;<a href="http://www.tecor.com"><img id="TecorLogo" 
        		src="http://ximpia-test.s3.amazonaws.com/images/blank.gif" 
        		alt="Tecor Communications S.L." title="Tecor Communications S.L." /></a>
</div>
<div><span><a href="http://twitter.com/ximpia" target="site">@ximpia</a></span></div>
</div>
</div>
				 */
				var htmlI = $("footer").html();
				var sm = ximpia.common.Path.getSiteMedia();
				var contentLength = $("footer div").length;
				if (contentLength < 1) {
					htmlI = "<div id=\"id_footerContent\">";
					htmlI += "<div id=\"id_footerText\">";
					htmlI += "<div  style=\" float: left;; margin-left: 10px; margin-top: -5px\">&copy; 2011 &nbsp;<a href=\"http://www.tecor.com\"><img id=\"TecorLogo\"";
					htmlI += "src=\"http://ximpia-test.s3.amazonaws.com/images/blank.gif\"";
					htmlI += "alt=\"Tecor Communications S.L.\" title=\"Tecor Communications S.L.\" /></a>";
					htmlI += "</div>";
					htmlI += "<div><span><a href=\"http://twitter.com/ximpia\" target=\"site\">@ximpia</a></span></div>";
					htmlI += "</div>";
					htmlI += "</div>";
					$("footer").html(htmlI);
				}
			}
		},
		pub: {
			/**
			 * Insert page tags : head, header and footer
			 */
			pageTags: function() {
				//_attr.priv.head();
				_attr.priv.header();
				_attr.priv.footer();
			}
		}
	}
	return _attr.pub;
}

ximpia.common.Form = function() {
	var _attr = {
		priv: {},
		pub: {
			/**
			* callback method for submit signup click.
			*/
			doSubmitButton: function() {
				var btObjStr = $(this).attr('data-xp-obj');
				var btObj = {};
				if (btObjStr) {
					btObj = JSON.parse(btObjStr);
				}
				var formId = btObj.form;
				var isValid = $("#" + formId).valid();
				var idImg = formId + '_Submit_Status';
				var idTxt = formId + '_Submit_Text';
				if (isValid == true) {
					// OK
					$("#" + formId).submit();
				} else {
					// Format errors
					$("#" + idImg).addClass('AjaxButtonERROR');
					$("#" + idTxt).text($("#id_ERR_GEN_VALIDATION").attr('value'));
				}				
			},
			/**        
	 		* Bind signup submit button. Binds the click event of button, shows waiting icon, sends data through AJAX
	 		*/
			doBindSubmitForm: function(formId, callbackFunction) {
    				$("a.button[data-xp-js='submit']").click(_attr.pub.doSubmitButton);
        			$("#" + formId).validate({
            			submitHandler: function(form) {
                			// Submit form
                			var idImg = form.id + '_Submit_Status';
                			var idTxt = form.id + '_Submit_Text';               
                			$("#" + idImg).xpLoadingSmallIcon();
                			$("#" + idImg).xpLoadingSmallIcon('wait');
                			$("#" + idTxt).text('');
                			$(form).ajaxSubmit({
                    			dataType: 'json',
                    			success: function(response, status) {
                        			var responseMap = eval(response);
                        			statusCode = responseMap['status'];
                        			if (statusCode.indexOf('.') != -1) {
                            				statusCode = statusCode.split('.')[0]
                        			}
                        			console.log('statusCode : ' + statusCode);
                        			if (statusCode == 'OK') {
                            				$("#" + idImg).xpLoadingSmallIcon('ok');
                            				$("#" + idTxt).text($("#id_msg_ok").attr('value'));
                            				// Put all fields inside form valid that are now errors
                            				$(".error").addClass('valid').removeClass("error");
                            				// Disable button
                            				$("[data-xp-js='submit']").xpPageButton('disable');
                            				// Change look to clicked
                            				if ($("#" + 'id_msgSubmit_Form1').attr('value')) {
                                				ximpia.common.Window.showPopUp('id_msgSubmit_Form1');
                            				} else {
                            					if (typeof callbackFunction != 'undefined') {
                            						callbackFunction();
                            					}
                            				}                       
                        			} else {
                            				$("#" + idImg).xpLoadingSmallIcon('error');
                            				$("#" + idTxt).text($("#id_ERR_GEN_VALIDATION").attr('value'));
                            				// Integrate showMessage, popUp, etc...
                            				var list = responseMap['errors'];
                            				message = '<ul>'
                            				var errorName = "";
                            				var errorId = "";
                            				for (var i=0; i<list.length; i++) {
                                				//var errorId = list[i][0];
                                				errorId = list[i][0];
                                				errorName = $("label[for='" + errorId + "']").text();
                                				console.log('errorName : ' + errorName + ' errorId: ' + errorId); 
                                				var errorMessage = list[i][1];
                                				//alert(errorId);
                                				$("#" + errorId).removeClass("valid");
                                				$("#" + errorId).addClass("error");
                                				message = message + '<li><b>' + errorName + '</b> : ' + errorMessage + '</li>';
                            				}
                            				message = message + '</ul>';
                            				// Show error Message in pop up
                            				ximpia.common.Window.showPopUp({
                                				title: 'Validation Errors Found',
                                				message: message,
                            				});
                        			}
                    			},
                    			error: function (data, status, e) {
                        			//alert(data + ' ' + status + ' ' + e);
                        			console.log(data + ' ' + status + ' ' + e);
                        			$("#" + idImg).xpLoadingSmallIcon('errorWithPopUp');
                        			ximpia.common.Window.showPopUp({
                            				title: 'System Error',
                            				message: 'I cannot process your request due to an unexpected error. Sorry for the inconvenience, please retry later. Thanks',
                            				height: 50
                        			});
                    			}
                			});
            			},
            			errorPlacement: function(error, element) {
                			element.next("img table").after(error);
            			}
        			});				
			},
			doReloadCaptcha: function() {
			        $("#id_ImgRefreshCaptcha").click(function() {
            			// reload captcha
            			$.get('/reloadCaptcha');
            			// Show image
            			var kk = Math.random();
            			$("#id_ImgCaptcha").attr('src', '/captcha/captcha.png?code=' + kk);
        			});
			},
			/**
			 * Tooltip for form labels
			 */
			doBindBubbles: function() {
       				$("label.info").mouseover(function() {
      					$(this).css('cursor', 'help');
       				});
       				$("label.info").qtip({
       					content: {
       						attr: 'data-xp-title'
       					},
       					events: {
       						focus: function(event, api) {
       						}
       					},
       					style: {
	       					width: 200,
       						classes: 'ui-tooltip-blue ui-tooltip-shadow ui-tooltip-rounded ui-tooltip-cluetip'
       					}
       				});
			}
		}
	}
	return _attr.pub;
}

ximpia.common.Ajax = {};
/**
 * Set suggest ajax view
 */
ximpia.common.Ajax.setAjaxSuggestView = (function() {
	$('#id_formAjax').attr('action', '/jxSuggestList');
});
/**
 * Set ajax view
 */
ximpia.common.Ajax.setAjaxView = (function() {
	$('#id_formAjax').attr('action', '/jxJSON');
});
/**
 * @returns {Object} Create new ajax object
 */
ximpia.common.Ajax.newAjaxObject = (function() {
        var oArg = new Object();
        oArg.jsonDataList = new Array();
        return oArg;
});
/**
 * New Ajax request
 */
ximpia.common.Ajax.newAjaxRequest = (function(oArg, method, argsTuple, argsDict) {
	var list = new Array();
        list[0] = method;
        list[1] = argsTuple;
        list[2] = argsDict;
        var index = oArg.jsonDataList.push(list);
        $('#id_formAjax_jsonData').attr('value', JSON.stringify(oArg));
});
/**
 * Send Ajax JSON Request
 */
ximpia.common.Ajax.sendAjaxJSONRequest = (function() {
        $('#id_formAjax').ajaxSubmit({
            dataType: 'json',
            async: false,
            timeout: 2000,
            success: function(responseMap, status) {
                if (responseMap && responseMap.status && responseMap.response) {
                    statusCode = responseMap['status'];
                    if (statusCode == 'OK') {
                        results = responseMap.response;
                    }
                }
            },
            error: function (data, status, e) {
                alert('ERROR : ' + status);
                results = new Array()               
            }
        });
        return results;
});


ximpia.common.PageAjax = function() {
	var _attr = {
		priv: {
			callback : null,
			path: "",
			formId: "",
			sectionId: "",
			verbose: false,
			data: {},
			formData: {}
		},
		pub: {
			init: function(obj) {
				_attr.priv.path = obj.path;
				_attr.priv.callback = obj.callback;
				_attr.priv.formId = obj.formId;
				_attr.priv.sectionId = obj.sectionId;
				_attr.priv.verbose = obj.verbose;
			},
			doFormOld: function() {
				$.getJSON(_attr.priv.path, function(data) {
					if (_attr.priv.verbose == true) {
						console.log(data)
					}
					//console.log(data)
					// forms
					var dataForm = data.response[_attr.priv.formId];
					//console.log('dataForm : ' + dataForm);
					for (var key in dataForm) {
						var objId = $("#id_" + key).attr('id');
						var keyAttrs = dataForm[key];
						var element = keyAttrs.element;
						//console.log(key + ' : ' + keyAttrs.value );
						if (element == 'input') {
							if (objId == null && keyAttrs.type == "hidden") {
								$("#id_variables").append("<input type=\"hidden\" id=\"id_" + key + "\" name=\"" + key + "\" value=\"\" />");
								$("#id_" + key).attr('value', keyAttrs.value);
							} else {
								for (keyAttr in keyAttrs) {
									if (keyAttrs[keyAttr] != null && keyAttr != "type") {					
										if (keyAttr == 'label' && keyAttrs.label != '') {
											$("label[for='" + 'id_' + key + "']").html(keyAttrs.label);
										} else if (keyAttr == 'help_text' && keyAttrs.help_text != '') {
											//console.log('help_text : ' + keyAttrs.help_text);
											$("label[for='" + 'id_' + key + "'].info").attr('data-xp-title', keyAttrs.help_text);
										} else {
											//console.log('attr || ' + keyAttr + ' : ' + keyAttrs[keyAttr]);
											$("#id_" + key).attr(keyAttr, keyAttrs[keyAttr]);
										}
									}
								}
							}
						} else if (element == 'select') {
							// label and help_text
							//console.log(keyAttrs);
							for (keyAttr in keyAttrs) {
								if (keyAttrs[keyAttr] != null && keyAttr != "type") {					
									if (keyAttr == 'label' && keyAttrs.label != '') {
										$("label[for='" + 'id_' + key + "']").html(keyAttrs.label);
									} else if (keyAttr == 'help_text' && keyAttrs.help_text != '') {
										//console.log('help_text : ' + keyAttrs.help_text);
										$("label[for='" + 'id_' + key + "'].info").attr('data-xp-title', keyAttrs.help_text);
									} else if (keyAttr == 'choices') {
										for (choiceIndex in keyAttrs.choices) {
											$("#id_" + key).append("<option value=\"" + keyAttrs.choices[choiceIndex][0] 
											+ "\">" + keyAttrs.choices[choiceIndex][1] + "</option>");
										}							
									} 
								}
							}
						}
					}
					//console.log('id_variables : ' + $("#id_variables").html());
					$("#id_sect_loading").fadeOut('fast');
					$("#" + _attr.priv.sectionId).css('visibility', 'visible');
					// Just call a method for the bindings of the page
					//var obj = ximpia.site.Signup();
					//obj.doProfessionalBind();
					_attr.priv.callback();
					//console.log('invitationCode : ' + $("#id_invitationCode").attr('value'));
				}).error(function(jqXHR, textStatus, errorThrown) {
					$("#id_sect_loading").fadeOut('fast');
					var html = "<div class=\"loadError\"><img src=\"http://localhost:8000/site_media/images/blank.png\" class=\"warning\" style=\"float:left; padding: 5px;\" /><div>Oops, something did not work right!<br/> Sorry for the inconvenience. Please retry later!</div></div>";
					$("body").before(html);
				});
			},
			doSections: function() {
				// section
				$.metadata.setType("attr", "data-xp-fields");
				var objects = $("section[data-xp-class='cond']");
				for (var i=0; i<objects.length; i++) {
					var obj = objects[i];
					var op = $(obj).attr('data-xp-op').toLowerCase();
					var action = $(obj).attr('data-xp-action').toLowerCase();
					var fields = $(obj).metadata();
					var field = "";
					var name = "";
					var value = "";
					var doAction = null;
					if (op == 'and') {
						doAction = true;
						for (name in fields) {
							value = fields[name];
							if (value != formData[name].value) {
								doAction = false;
							}
						}
					} else if (op == 'or') {
						doAction = false;
						for (name in fields) {
							value = fields[name];
							if (value == formData[name].value) {
								doAction = true;
							}
							
						}
					}
				}
				console.log('doAction : ' + doAction);				
			},
			doFade: function() {
				$("#id_sect_loading").fadeOut('fast');
				$("#" + "id_sect_signupUser").css('visibility', 'visible');
			},
			doForm: function() {
				$.getJSON(_attr.priv.path, function(data) {
					if (_attr.priv.verbose == true) {
						console.log(data)
					}
					//var formData = data.response[_attr.priv.formId];
					//$("[data-xp-type='basic.input']").xpObjInput('renderField', formData);
					//$("#id_variables").xpObjInput('addHidden', formData);
					//$("[data-xp-type='basic.select']").xpObjSelect('render', formData);
					//$("#id_sect_loading").fadeOut('fast');
					//$("#" + "id_sect_signupUser").css('visibility', 'visible');
					_attr.priv.callback(data);
				}).error(function(jqXHR, textStatus, errorThrown) {
					$("#id_sect_loading").fadeOut('fast');
					var html = "<div class=\"loadError\"><img src=\"http://localhost:8000/site_media/images/blank.png\" class=\"warning\" style=\"float:left; padding: 5px;\" /><div>Oops, something did not work right!<br/> Sorry for the inconvenience. Please retry later!</div></div>";
					$("body").before(html);
				});
			}
		}
	}
	return _attr.pub;
}
/**
 * Do fade out wait icon and show page
 */
ximpia.common.PageAjax.doFade = function() {
	$("#id_sect_loading").fadeOut('fast');
	$("#" + "id_sect_signupUser").css('visibility', 'visible');
}


ximpia.common.GoogleMaps = function() {
	var _attr = {
		priv:  {},
		pub:  {
			init: function() {},
			insertCityCountry: function(idCity, idCountry) {
  				var data = {};
				if (navigator.geolocation) {
	  				navigator.geolocation.getCurrentPosition(function(position) {
  						var loc = new google.maps.LatLng(position.coords.latitude,position.coords.longitude);
  						geocoder = new google.maps.Geocoder();
  						geocoder.geocode({'latLng': loc}, function(results, status) {
							var city = "";
  							var countryCode = "";
  							var list =  results[0].address_components;
  							for (var i=0; i<list.length; i++) {
	  							var fields = list[i].types;
  								for (var j=0; j<fields.length; j++) {
	  								if (fields[j] == "locality") {
  										city = list[i].long_name;
  										$("#" + idCity).attr('value', city);
  									} else if (fields[j] == "country") {
	  									countryCode = list[i].short_name.toLowerCase();
  										//$("#" + idCountry + " :selected").removeAttr('selected');
  										//$("#" + idCountry + " option[value=" + countryCode + "]")[0].selected = true;
  										//$("#" + idCountry).selectBox('value', countryCode);
  										$("#" + idCountry).xpObjListSelect('setValue', 'es');
  									}
  								}		  					
  							}
  						});
		  			});
				}
			}
		}
	}
	return _attr.pub;
};


ximpia.visual.Icon = {};
/**
 * bind icons fade effect
 */
ximpia.visual.Icon.bindFadeIcons = (function(className) {
	// .icon
	$("." + className).mouseover(function() {
		$(this).fadeTo("fast", 0.70);
	}).mouseout(function() {
		$(this).fadeTo("fast", 1.00);
	});	
});


ximpia.visual.SocialNetworkIconData = function() {
	var _attr = {
		priv: {
			id: null,
			inputData: null,
			dataDictList: null
		},
		pub: {
			/**
			 * Constructor
			 */
			init:(function(id) {
				_attr.priv.id = id
				_attr.priv.inputData = $("#" + this.id).attr('value');
				_attr.priv.dataDictList = JSON.parse(_attr.priv.inputData);
			}),
			/**
			 * Get list of data
			 */
			getDataDictList: function() {
				return _attr.priv.dataDictList
			},
			/**
			 * Get data
			 */
			getData: function() {
				return _attr.priv.dataDictList[1]
			},
			/**
			 * Get configuration
			 */
			getConfig: function() {
				return _attr.priv.dataDictList[0]
			},
			/**
			 * Get token
			 */
			getToken: function() {
				return _attr.priv.dataDictList[1].token
			},
			/**
			 * Set token
			 */
			setToken: function(token) {
				_attr.priv.dataDictList[1].token = token;
			}
		}
	}
	return _attr.pub;
}

ximpia.visual.GenericComponentData = function() {
	var _attr = {
		priv: {
			id: null,
			inputData: null,
			dataDictList: null
		},
		pub: {
			/**
			 * Constructor
			 */
			init: function(id) {
				_attr.priv.id = id
				_attr.priv.inputData = $("#" + this.id).attr('value');
				_attr.priv.dataDictList = JSON.parse(_attr.priv.inputData);
			},
			/**
			 * 
			 */
			getDataDictList: function() {
				return _attr.priv.dataDictList;
			},
			/**
			 * 
			 */
			getDataList: function() {
				return _attr.priv.dataDictList[1].data;
			},
			/**
			 * 
			 */
			getDataListPaging: function(page, numberPages) {
				var size = _attr.pub.getSize();
				// TODO
			},
			/**
			 * 
			 */
			setDataList: function(array) {
				_attr.priv.dataDictList[1].data = array;
			},
			/**
			 * 
			 */
			addDataEnd: function(obj) {
            			var size = _attr.priv.dataDictList[1].data.push(obj);
            			$("#" + _attr.priv.id).attr('value', JSON.stringify(_attr.priv.dataDictList));
			},
			/**
			 * 
			 */
			writeData: function(obj, i) {
            			_attr.priv.dataDictList[1].data[i] = obj;
            			$("#" + _attr.priv.id).attr('value', JSON.stringify(_attr.priv.dataDictList));
			},
			/**
			 * 
			 */
			getSize: function() {
				return _attr.priv.dataDictList[1].data.length;
			},
			/**
			 * Object has element by text?
			 */
			hasElement: function(searchText) {
            			var array = _attr.priv.getDataList();
            			var hasElement = false;
            			for (var i = 0; i< array.length; i++) {
                			if (array[i].text == searchText) {
                    				hasElement = true;
                			}
            			}
            			return hasElement;
			},
			/**
			 * Object has element by name?
			 */
			hasElementByName: function(searchText) {
            			var array = _attr.priv.getDataList();
            			var hasElement = false;
            			for (var i = 0; i< array.length; i++) {
                			if (array[i].name == searchText) {
                    				hasElement = true;
                			}
            			}
            			return hasElement;
			},
			/**
			 * Delete data from object
			 */
			deleteData: function(i) {
            			var newArray = [];
            			var array = _attr.pub.getDataList();
            			for (var j=0; j<array.length; j++) {
                			if (i != j) {
                    				newArray.push(array[j]);
                			}
            			}
            			_attr.pub.setDataList(newArray);
            			$("#" + _attr.priv.id).attr('value', JSON.stringify(_attr.priv.dataDictList));
			},
			/**
			 * 
			 */
			getConfigDict: function() {
				return _attr.priv.dataDictList[0];
			}
		}
	}
	return _attr.pub;
}
/**
 * deleteFromList using Generic Component Data. static method
 */
ximpia.visual.GenericComponentData.deleteFromList = function(element, oArg) {
        var idElementDel = $(element).attr('id');
        var idElement = idElementDel.replace('_del','');
        var list = idElement.split('_');
        var idContainer = 'id_' + list[1];
        var idContainerData = idContainer + '_data';
        var index = list[list.length-1];
        $('#' + idElement).remove();
        var obj = new GenericComponentData(idContainerData);
        obj.deleteData(index);
        if (oArg.callBack) {
            oArg.callBack(oArg);
        }	
}

ximpia.site.Signup = function() {
	var _attr = {
		priv: {
			/**
	 		* Show password strength indicator. Password leads to a strength variable. Analyze if this behavior is common
	 		* and make common behavior. One way would be to have a data-xp-obj variable strength and be part of validation, showing
	 		* the message of nor validating.
	 		*/
			doShowPasswordStrength: (function(userId, passwordId, submitId) {
	        		// Password Strength
		        	// TODO: Analyze a common way of associating a new variable to a input field, and influence click of a given button
		        	$("#" + passwordId).passStrengthener({
					userid: "#" + userId,
					strengthCallback:function(score, strength) {
						console.log('strength : ' + strength)                       
						if(strength == 'good' || strength == 'strong') {
							$("#" + submitId).xpPageButton('enable', ximpia.common.Form().doSubmitButton);
						} else {
							$("#" + submitId).xpPageButton('disable');
						}
					}
				});
			})
		},
		pub: {
			doProfessionalBind: (function(data) {
				// Pre-page : Binding ajax data to form
				var formData = data.response["form_signup"];
				$("[data-xp-type='basic.input']").xpObjInput('renderField', formData);
				$("#id_variables").xpObjInput('addHidden', formData);
				$("[data-xp-type='basic.select']").xpObjSelect('render', formData);
				ximpia.common.PageAjax.doFade();
				// Conditions
				// Post-Page : Page logic
				var formId = "id_Form1";
				_attr.priv.doShowPasswordStrength('id_ximpiaId', 'id_password', formId + '_Submit');
				var oForm = ximpia.common.Form();
				oForm.doBindBubbles();
				oForm.doBindSubmitForm(formId);
    				oForm.doReloadCaptcha();
				// fadeIcons
				ximpia.visual.Icon.bindFadeIcons(".icon");
				/*function processSnLogin() {	
					// Click on Facebook or LinkedIn button
					$(".SnLogin").click(function() {
						var sId = $(this).attr('id');
						if (sId == 'id_facebookLogin') {
							// Facebook
							FB.login(function(response) {
	  							if (response.session) {
									$("#id_facebookToken").attr('value', response.session.access_token);
									//alert(response.session.access_token);
    								if (response.perms) {
	      								// user is logged in and granted some permissions.
      									// perms is a comma separated list of granted permissions
									$("#id_fbLoginButton").css('display', 'block');
									$("#id_mixLoginButton").css('display', 'none');
									FB.XFBML.parse();
									// Hide passwords
									$("#id_showPassword").css('display','none');
									// Get profile
									FB.api('/me', function(responseProfile) {
										// Fillout fields in form
										$("#id_firstName").attr('value', responseProfile.first_name);
										$("#id_lastName").attr('value', responseProfile.last_name);
										$("#id_email").attr('value', responseProfile.email);
										$("#id_ximpiaId").attr('value', responseProfile.first_name.toLowerCase() + '.' + responseProfile.last_name.toLowerCase());
										var locationName = responseProfile.location.name;
										var locationFields = locationName.split(',');
										$("#id_city").attr('value', locationFields[0].trim());
										var locale = responseProfile.locale;
										$("#id_country").attr('value', locale.split('_')[1].toLowerCase());
										$("#id_facebookIcon").xpSocialNetworkIcon('changeStatusOK');
									});
    								} else {
	      								// user is logged in, but did not grant any permissions
									// Fillout fields in form
    								}
  								} else {
	    								// user is not logged in
  								}
							}, {perms:'email,user_birthday'});
						}
						else if (sId == 'id_linkedInLogin') {
							// LinkedIn
							//IN.UI.Authorize().place();
							alert('LinkedIn');
						}
					});
				}
				var fbAppId = $("#id_facebookAppId").attr('value');
				FB.init({appId: fbAppId, status: true, cookie: true, xfbml: true});
  				FB.Event.subscribe('auth.sessionChange', function(response) {
    					if (response.session) {
    						// A user has logged in, and a new cookie has been saved			
						var facebookList = JSON.parse($("#id_facebookIcon_data").attr('value'));
						facebookList[1].token = response.session.access_token;
						$("#id_facebookIcon_data").attr('value', JSON.stringify(facebookList));
						// Hide passwords
						$("#id_showPassword").css('display','none');
						$("#id_password").css('display','none');
						$("#id_passwordVerify").css('display','none');
						$("#id_password").removeClass('required');
						$("#id_passwordVerify").removeClass('required');
						// Get profile
						FB.api('/me', function(responseProfile) {
							// Fillout fields in form
							$("#id_firstName").attr('value', responseProfile.first_name);
							$("#id_lastName").attr('value', responseProfile.last_name);
							$("#id_email").attr('value', responseProfile.email);
							$("#id_ximpiaId").attr('value', responseProfile.first_name.toLowerCase() + '.' + responseProfile.last_name.toLowerCase());
							var locationName = responseProfile.location.name;
							var locationFields = locationName.split(',');
							$("#id_city").attr('value', locationFields[0].trim());
							var locale = responseProfile.locale;
							$("#id_country").attr('value', locale.split('_')[1].toLowerCase());
							$("#id_facebookIcon").xpSocialNetworkIcon('changeStatusOK');
						});			
    					} else {
    						// The user has logged out, and the cookie has been cleared
						//alert('Out....');
    					}
				});*/
				//processSnLogin();
				/*$(".AuthIcon").xpSocialNetworkIcon();
				$(".AuthIcon").click(function() {
	   				$(this).xpSocialNetworkIcon('click');
				});*/
				$("[data-xp-js='submit']").xpPageButton();
				$("[data-xp-js='submit']").xpPageButton('render');
				// Geo loc for city and country	
				var oGoogleMaps = ximpia.common.GoogleMaps();
				oGoogleMaps.insertCityCountry("id_city", "id_country");
			}),
			doOrganizationBind: (function(data) {
				console.log('doOrganizationBind()...');
				var formData = data.response["form_signupOrg"];
				sessionStorage.setItem('xpForm', JSON.stringify(formData));
				// Have doubts about this??????
				sessionStorage.setItem('form_signupOrg', JSON.stringify(formData));
				$("[data-xp-type='list.field']").xpObjListField('render');
				$("[data-xp-type='basic.text']").xpObjInput('renderField');
				$("#id_variables").xpObjInput('addHidden');				
				//$("[data-xp-type='list.select']").xpObjSelectList('render', formData);
				/*var countryList = JSON.parse($('#id_choices').attr('value'))['country'];
				var countries = {'results': []};
				for (i in countryList) {
					countries['results'][i] = {'id': countryList[i][0], 'name': countryList[i][1]}
				}
				$("[data-xp-type='list.select']").flexbox(countries,{
					autoCompleteFirstMatch: true,
					paging: false,
					maxVisibleRows: 6
				});*/				
				//console.log(ximpia.common.Choices.get('country'));				
				$("[data-xp-type='list.select']").xpObjListSelect('render');
				$("[data-xp-type='text.autocomplete']").xpObjInput('renderFieldAutoComplete');
				/*$("select").selectBox({
						'menuTransition': 'slide',
						'menuSpeed' : 'fast'
					});*/
				/*$("a.selectBox").jScrollPane(
					{
						showArrows: true,
						verticalArrowPositions: 'after',
						arrowButtonSpeed: 90,
						animateScroll: true,
						keyboardSpeed: 90,
						verticalDragMinHeight: 20
					}
				);*/
				/*$(".comboScroll").jScrollPane(
					{
						showArrows: true,
						verticalArrowPositions: 'after',
						arrowButtonSpeed: 130,
						animateScroll: true,
						keyboardSpeed: 100,
						verticalDragMinHeight: 20
					}
				);*/
				$(".scroll").jScrollPane(
					{	showArrows: true,
						verticalArrowPositions: 'after',
						arrowButtonSpeed: 90,
						animateScroll: false,
						keyboardSpeed: 90,
						animateDuration: 50,
						arrowRepeatFreq: 0
					}
				);				
				/*$("a.selectBox").each(function() {
					if ($(this).find(".jspArrow").length > 0) {
						$(this).find('.jspTrack').addClass("jspTrackPag");
					}
				});*/
				$(".scroll").each(function() {
					if ($(this).find(".jspArrow").length > 0) {
						$(this).find('.jspTrack').addClass("jspTrackPag");
					}
				});
				
				//$("#id_organizationCountry").selectBox('disable');
				ximpia.common.PageAjax.doFade();
				var formId = "id_Form1";
				_attr.priv.doShowPasswordStrength('id_ximpiaId', 'id_password', formId + '_Submit');
				var oForm = ximpia.common.Form();
				oForm.doBindBubbles();
				oForm.doBindSubmitForm(formId);
    				oForm.doReloadCaptcha();
				// fadeIcons
				ximpia.visual.Icon.bindFadeIcons(".icon");
				$("[data-xp-js='submit']").xpPageButton();
				$("[data-xp-js='submit']").xpPageButton('render');
				// Geo loc for city and country	
				var oGoogleMaps = ximpia.common.GoogleMaps();
				oGoogleMaps.insertCityCountry("id_city", "id_country_comp");
			})
		}
	}
	return _attr.pub;
}
