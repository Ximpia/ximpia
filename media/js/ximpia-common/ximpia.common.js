
var ximpia = ximpia || {};
ximpia.common = ximpia.common || {};
ximpia.visual = ximpia.visual || {};
ximpia.site = ximpia.site || {};

ximpia.common.List = {};
ximpia.common.List.getValue = (function(id, key) {
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
        var sTitle = '';
        var sMessage = '';
        var sButtons = 'MsgCPClose:' + eval($("#id_buttonConstants").attr('value'))['close'];
        var sEffectIn = 'fadeIn,1000';
        var sEffectOut = '';
        var bFadeBackground = true;
        var iWidth = null;
        var iHeight = null;
        functionShow = null;
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
        $("div.MsgTitle").text(sTitle);
        $("div.MsgText").html(sMessage);
        //$("#PopMsgWrapper .MsgText").html(sMessage);
        ButtonList = sButtons.split(',');
        $("div.MsgButtons").text('');
        for (var i=0; i<ButtonList.length; i++) {
            Fields = ButtonList[i].split(':');
            sButtonId = Fields[0];
            sButtonText = Fields[1];
            $("div.MsgButtons").append('<input type="button" id="' + sButtonId + '" value="' + sButtonText + '" class="Button"/>');
        }
        EffectInList = sEffectIn.split(',');
        sEffectInTxt = EffectInList[0];
        iEffectInTime = parseInt(EffectInList[1]);
        EffectOutList = sEffectOut.split(',');
        sEffectOutTxt = EffectOutList[0];
        iEffectOutTime = parseInt(EffectOutList[1]);
        if (sEffectInTxt == 'fadeIn') {
            $("div.PopMessage").fadeIn(iEffectInTime);
        }   
        $("div.Pops").css('left', iLeft + 'px');
        $("div.Pops").css('top', iTop + 'px');
        $("div.Pops").css('visibility','visible');
        if (sEffectOutTxt == 'fadeOut') {
            $("div.PopMessage").fadeOut(iEffectOutTime);
        }
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
        if (!bFadeOut) {
            bFadeBackground = false;
        }
        $(".Pops").css('left','-2000px');
        if (bFadeBackground) {
            $("#Wrapper").fadeTo("fast", 1.0);
        }
        if (functionName) {
            functionName();
        }	
});
/**
 * Show Pop Up. It is used for Ajax actions, like OK Message, Error messages, etc...
 */
ximpia.common.Window.showPopUp = (function(key) {
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
            buttons: 'MsgOk:' + closeValue,
            effectIn: 'fadeIn,1000',
            effectOut: sFadeOut,
            fadeBackground: bFadeOut
        });
        //showMessage(sTitle, sMessage, 'MsgOk:OK', 'fadeIn,1000', sFadeOut, bFadeOut);
        if (sFadeOut == '') {
            $("#MsgOk").click(function() {ximpia.common.Window.clickMsgOk(bFadeOut, functionName)});
        }
        if (sUrl) {
            if (sUrl != '') {
                $("#MsgOk").click(function() {
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
                                				callbackFunction();
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
                                				errorName = list[i][0];
                                				errorId = "id_" + errorName; 
                                				var errorMessage = list[i][1];
                                				//alert(errorId);
                                				$("#" + errorId).removeClass("valid");
                                				$("#" + errorId).addClass("error");
                                				message = message + '<li><b>' + errorName + '</b> : ' + errorMessage + '</li>';
                            				}
                            				message = message + '</ul>';
                            				// Show error Message in pop up
                            				ximpia.common.Window.showPopUp({
                                				title: 'Errors Found',
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
  										$("#" + idCountry + " :selected").removeAttr('selected');
  										$("#" + idCountry + " option[value=" + countryCode + "]")[0].selected = true;
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
			doProfessionalBind: (function() {
				var formId = "id_Form1";
				_attr.priv.doShowPasswordStrength('id_ximpiaId', 'id_password', formId + '_Submit');
				var oForm = ximpia.common.Form();
				oForm.doBindBubbles();
				oForm.doBindSubmitForm(formId);
    				oForm.doReloadCaptcha();
				// fadeIcons
				ximpia.visual.Icon.bindFadeIcons(".icon");
				function processSnLogin() {	
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
				});
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
			doOrganizationBind: (function() {
				
			})
		}
	}
	return _attr.pub;
}
