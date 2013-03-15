
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

var ximpia = ximpia || {};
ximpia.common = ximpia.common || {};
ximpia.visual = ximpia.visual || {};
ximpia.site = ximpia.site || {};
ximpia.constants = ximpia.constants || {};
ximpia.config = ximpia.config || {};
ximpia.external = ximpia.external || {};

//////////////////////////////////////////////////////////////////
// config.js
//////////////////////////////////////////////////////////////////

/*
* Constants
*/

//////////////////////////////////////////////////////////////////
// config.js
//////////////////////////////////////////////////////////////////

/*
* Main Constants
*/
ximpia.constants.main = {};
ximpia.constants.main.DEBUG_INFO = 'info';
ximpia.constants.main.DEBUG_WARN = 'warn';
ximpia.constants.main.DEBUG_ERROR = 'error';
ximpia.constants.main.DEBUG_DEBUG = 'debug';

var timeout = 2000;

//////////////////////////////////////////////////////////////////
// external
//////////////////////////////////////////////////////////////////

/*
* Facebook
*/
ximpia.external.Facebook = {};
/*
 * Facebook signup
 */
ximpia.external.Facebook.renderSignup = (function(attrs, callable) {
	ximpia.console.log('facebook API :: renderLogin :: ');
	ximpia.console.log('facebook API :: attrs...');
	//ximpia.console.log('facebook API :: callable: ' + callable);
	ximpia.console.log(attrs);
	$('body').css('cursor', 'wait');
	// Facebook button
	FB.init({
		appId : ximpia.settings.FACEBOOK_APP_ID,
		status : true,
		cookie : true,
		xfbml : true
	});
	// Login and change is response, like visiting page when user is logged in
	FB.Event.subscribe('auth.authResponseChange', function(response) {
		ximpia.console.log('facebook API :: auth.authResponseChange');
		ximpia.console.log(response);
		if (response.authResponse) {
			//TODO: Place waiting clock in case not displayed
			ximpia.console.log('facebook API :: Have response...');
			ximpia.console.log(response);
			//$("#id_passwordAuth").css('display', 'none');
			$("#id_passwordAuth").remove();
			$("#id_socialAuth .caption").css('display', 'none');
			$("input[name='authSource']").attr('value', 'facebook');
			// A user has logged in, and a new cookie has been saved
			$("input[name='socialId']").attr('value', response.authResponse.userID);
			$("input[name='socialToken']").attr('value', response.authResponse.accessToken);
			ximpia.console.log('facebook API :: accessToken: ' + response.authResponse.accessToken);
			ximpia.console.log('facebook API :: id: ' + response.authResponse.userID);
			// Get profile*/
			FB.api('/me', function(responseProfile) {
				//TODO: Place waiting clock in case not displayed
				ximpia.console.log('facebook API :: responseProfile...');
				ximpia.console.log(responseProfile);
				// Fillout fields in form
				ximpia.common.Browser.putAttr('isSocialLogged', true);
				ximpia.common.PageAjax.doRenderExceptFunctions('xpData-view-signup.form_signup');
				$("input[name='firstName']").attr('value', responseProfile.first_name);
				$("input[name='lastName']").attr('value', responseProfile.last_name);
				$("input[name='email']").attr('value', responseProfile.email);
				// Disable controls when available : In future use disable conditions for components
				$("input[name='firstName']").attr('readonly', 'readonly');
				$("input[name='lastName']").attr('readonly', 'readonly');
				$("input[name='email']").attr('readonly', 'readonly');
				$("#id_country_input").attr('readonly', 'readonly');
				$("input[name='city']").attr('readonly', 'readonly');
				var locationName = responseProfile.location.name;
				var locationFields = locationName.split(',');
				setTimeout(function() {
					ximpia.common.PageAjax.positionBars({
						'skipVisibility' : true
					});
					eval('new callable(attrs)');
				}, 500);
				var oGoogleMaps = ximpia.common.GoogleMaps();
				oGoogleMaps.insertCityCountry(ximpia.common.Browser.buildXpForm('signup', 'form_signup'), ["id_city"], ["id_country"]);
				eval('new callable(attrs)');
				$('body').css('cursor', 'auto');
			});
			//callable();
			//ximpia.common.PageAjax.positionBars();
		} else {
			ximpia.console.log('facebook API :: No response...');
			eval('new callable(attrs)');
			// The user has logged out, and the cookie has been cleared
			//alert('Out....');
			var oGoogleMaps = ximpia.common.GoogleMaps();
			oGoogleMaps.insertCityCountry(ximpia.common.Browser.buildXpForm('signup', 'form_signup'), ["id_city"], ["id_country"]);
			eval('new callable(attrs)');
			$('body').css('cursor', 'auto');
		}
		$('body').css('cursor', 'auto');
	});
	$('body').css('cursor', 'auto');
});
/*
 * Facebook login
 */
ximpia.external.Facebook.renderLogin = (function(attrs, callable) {
	ximpia.console.log('facebook API :: renderLogin :: ');
	ximpia.console.log('facebook API :: attrs...');
	ximpia.console.log(attrs);
	$('body').css('cursor', 'wait');
	// Facebook button
	FB.init({
		appId : ximpia.settings.FACEBOOK_APP_ID,
		status : true,
		cookie : true,
		xfbml : true
	});
	// Login and change is response, like visiting page when user is logged in
	FB.Event.subscribe('auth.authResponseChange', function(response) {
		ximpia.console.log('facebook API :: auth.authResponseChange');
		ximpia.console.log(response);
		if (response.authResponse) {
			//TODO: Place waiting clock in case not displayed
			ximpia.console.log('facebook API :: Have response...');
			ximpia.console.log(response);
			ximpia.common.Browser.putAttr('isSocialLogged', true);
			ximpia.common.PageAjax.doRenderExceptFunctions('xpData-view-signup.form_login');
			//$("#id_passwordAuth").remove();
			$("#id_socialAuth .caption").css('display', 'none');
			$("input[name='authSource']").attr('value', 'facebook');
			// A user has logged in, and a new cookie has been saved
			$("input[name='socialId']").attr('value', response.authResponse.userID);
			$("input[name='socialToken']").attr('value', response.authResponse.accessToken);
			ximpia.console.log('facebook API :: accessToken: ' + response.authResponse.accessToken);
			ximpia.console.log('facebook API :: id: ' + response.authResponse.userID);
			//ximpia.common.PageAjax.positionBars( {'skipVisibility': true} );
			eval('new callable(attrs)');			
		} else {
			ximpia.console.log('facebook API :: No response...');
			eval('new callable(attrs)');
			// The user has logged out, and the cookie has been cleared
			//alert('Out....');
		}
		$('body').css('cursor', 'auto');
	});
	eval('new callable(attrs)');
	$('body').css('cursor', 'auto');
});

ximpia.external.Captcha = {};
ximpia.external.Captcha.renderCaptcha = (function(attrs, callable) {
	ximpia.console.log('renderCaptcha :: ');
	Recaptcha.create(ximpia.settings.RECAPTCHA_PUBLIC_KEY, "id_recaptcha_comp", {
		theme : "clean",
		callback : function() {
			$("input[name='recaptcha_response_field']").addClass('fieldMust');
			$("input[name='recaptcha_response_field']").css('border', '2px inset');
			setTimeout(function() {
				ximpia.common.PageAjax.positionBars({
					'skipVisibility' : true
				});
				eval('new callable(attrs)');
			}, 500);
		}
	});
});

//////////////////////////////////////////////////////////////////
// external
//////////////////////////////////////////////////////////////////

ximpia.common.List = {};
/**
 * Get value from list representation in element, like ['1','2']
 * 
 */
ximpia.common.List.getValue = (function(id, key) {
	ximpia.console.log('value : ' + $("#" + id).attr('value'));
	var array = eval($("#" + id).attr('value'));
	var value = '';
	for (var i = 0; i < array.length; i++) {
		var list = array[i];
		if (list[0] == key) {
			value = list[1];
		}
	}
	return value;
});
/**
 * list has key: ['1','2']. id is the reference for element.
 */
ximpia.common.List.hasKey = (function(id, key) {
});
/*
 * Get value from input list.
 */
ximpia.common.List.getValueFromList = (function(key, list) {
	for (j in list) {
		if (list[j][0] == key) {
			value = list[j][1];
		}
	}
	return value;
});

ximpia.common.Util = {};
ximpia.common.Util.initVariable = (function(name, defaultValue, attrs) {
	var value = defaultValue;
	if (attrs.hasOwnProperty(name)) {
		value = attrs[name];
	}
	return value
});

ximpia.common.JxDataQuery = {};
/*
 * Search for data. Calls server view jxDataQuery
 * 
 * ** Ajax Attributes **
 * 
 * * ````
 * * ````
 * * ````
 * * ````
 * * ````
 * * ````
 * * ````
 * * ````
 * * ````
 * * ````
 * 
 * 
 * 	* ``dbClass``:str : Data class name (DAO)
	* ``fields``:list<str> [optional]
	* ``pageStart``:str [optional] [default:1] : Start page number
	* ``pageEnd``:str [optional] : End page number
	* ``orderBy``:tuple<str> [optional]
	* ``method``:str [optional] [default:searchFields]
	* ``args``:dict<str,str> [optional]
	* ``hasOrdering``:bool [optional]
	* ``orderField``:str [optional]
 * 
 */

ximpia.common.JxDataQuery.search = (function(app, dbClass, obj, func) {
	// Build data
	var request = obj;
	request.dbClass = dbClass;
	request.app = app;
	var keys = Object.keys(obj);
	for (var i=0; i<keys.length; i++) {
		if (typeof obj[keys[i]] == 'object') {
			request[keys[i]] = JSON.stringify(obj[keys[i]]);
		}
	}
	//request.disablePaging = true;
	ximpia.console.log('JxDataQuery.search :: request...');
	ximpia.console.log(request);
	var response = {};
	$.ajax({
  		type: "POST",
  		url: '/jxDataQuery',
  		data: request,
  		dataType: 'json',
  		traditional: false
	}).done(function( response ) {
		ximpia.console.log('JxDataQuery.search :: result...');
		ximpia.console.log(response);
		func(response);
	}).fail(function(jqXHR, textStatus) {
  		// TODO: throw exception????
  		ximpia.console.log('JxDataQuery.search :: request failed: ' + textStatus);
	});
});

ximpia.common.Object = {};
/*
 * Get values from object: key -> value
 * 
 * ** Attributes**
 * 
 * * ``obj``:Object
 * 
 * ** Returns **
 * 
 * * ``values``:List
 * 
 */
ximpia.common.Object.values = (function(obj) {
	var valueList = [];
	for (key in obj) {
		valueList.push(obj[key]);
	}
	return valueList
});
/*
 * Get metadata for object
 * 
 * ** Attributes **
 * 
 * * ``obj``:Object
 * 
 * ** Returns **
 * 
 * string for metadata object
 * 
 */
ximpia.common.Object.metadata = (function(obj) {
	var meta = '{';
	var value = '';
	var counter = 0;
	for (key in obj) {
		value = obj[key];
		if (typeof(value) == 'string') {
			value = "'" + value + "'";
		}
		if (counter == 0) {
			meta += key + ': ' + value;
		} else {
			meta += ', ' + key + ': ' + value;
		}
		counter += 1;		
	}
	meta += '}';
	return meta
})


/*
 * Start waiting clock for server response
 * 
 * ** Attributes** 
 * 
 * * ``op``:String: Method operation to show in log
 * 
 */
ximpia.common.startBackendResponse = (function(op) {
	// Waiting control to show loading bar if we wait more than 0.5 seconds
	// TODO: Place into ximpia.settings time variables used for loading bar
	var waitCounter = 1;
	window.serverWait = setInterval(function() {
		ximpia.console.log('startInterval :: ' + op + ' :: Waiting response from server(' + waitCounter + ') ... time: ' + 
				waitCounter*.1 + ' seconds...' );
		if (waitCounter > 2 && waitCounter < 100) {
			$("#id_sect_loading").fadeIn(300);
		} else if (waitCounter > 100) {
			ximpia.console.log('PageAjax.doForm :: We got to limit of 10 seconds... exit...');
			clearInterval(serverWait);
			$("#id_sect_loading").fadeOut(200);
		}
		waitCounter += 1;
	}, 100);
});

/*
 * End backend server response
 * 
 * ** Attributes **
 * 
 * * ``op``:String : Operation to show in log
 */
ximpia.common.endBackendResponse = (function(op) {
	// Fade out loading bar
	ximpia.console.log(op + ' :: We got response, clear interval...');
	clearInterval(window.serverWait);
	// Remove loading bar
	$("#id_sect_loading").fadeOut(200);
});

/*
 * set timeout for 10 seconds in periods of 1 second
 */
ximpia.common.timeOutCounter = (function(func) {
	var waitCounter = 1;
	var timeout = setInterval(function() {
		var counter = $.find("[data-xp-render='']").length;
		ximpia.console.log('timeOutCounter :: counter: ' + counter + ' | ' + waitCounter*0.1 + ' sc');
		if (counter == 0) {
			clearInterval(timeout);
			eval('new func()');
		}
		if (waitCounter > 100) {
			clearInterval(timeout);
		}
		waitCounter += 1;
	}, 100);	
});

/*
 * Wait until list of components has been rendered, data-xp-render='true'
 */
ximpia.common.waitUntilListRenders = (function(func) {
	var waitCounter = 1;
	var timeout = setInterval(function() {
		var counterLeftRender = 0;
		//$.find('[data-xp-type*="list."]')[0].attributes['data-xp-render'].value
		$.find('[data-xp-type*="list."]').forEach(function(element) {
			if (element.attributes['data-xp-render'] == undefined) {
				counterLeftRender += 1;
			}
		});
		$.find('[data-xp-type*="container."]').forEach(function(element) {
			if (element.attributes['data-xp-render'] == undefined) {
				counterLeftRender += 1;
			}
		});
		if (waitCounter > 100) {
			clearInterval(timeout);
		}
		if (counterLeftRender == 0) {
			clearInterval(timeout);
			eval('new func()');
		}
		waitCounter += 1;
		ximpia.console.log('waitCounter: ' + waitCounter);
		ximpia.console.log('counterLeftRender: ' + counterLeftRender);
	}, 100);
});

/*
 * Get visual component div element for elements inside component
 */
ximpia.common.getParentComponent = (function(element) {
	var isComp = false;
	var counter = 0;
	var elementTarget = $(element).parent();
	if (elementTarget.attr('data-xp-type')) {
		isComp = true;
	}
	while (isComp == false) {
		if (counter > 20) {
			break;
		}
		var elementTarget = $(elementTarget).parent();
		if (elementTarget.attr('data-xp-type')) {
			isComp = true;
		}
		counter += 1;
	}
	return elementTarget;
});

ximpia.console = {};
/*
 * For log for levels: debug, info, warn, errors. If no level is informed, debug is default.
 * If level is same as debug level defined in constant ximpia.constants.main.DEBUG, we log
 * logData
 */
ximpia.console.log = (function(logData, level) {
	//TODO: Treat browsers. Browsers ot supporting console.log will not output logs
	if ( typeof (level) == 'undefined') {
		level = ximpia.constants.main.DEBUG_DEBUG;
	}
	if (ximpia.common.ArrayUtil.hasKey(ximpia.settings.LOG_LEVELS, level)) {
		console.log(logData);
	}
});

ximpia.common.ArrayUtil = {};
/*
 * Checks if array has key
 * 
 * ** Attributes **
 * 
 * * ``array``:object
 * * ``keyTarget``:string
 * 
 * ** Returns **
 * 
 * boolean
 * 
 */
ximpia.common.ArrayUtil.hasKey = function(array, keyTarget) {
	var exists = false;
	//ximpia.console.log(JSON.stringify(array));
	for (index in array) {
		//ximpia.console.log(key + ' ' + array[key] + ' ' + keyTarget);
		if (array[index] == keyTarget) {
			exists = true;
		}
	}
	return exists;
}

ximpia.common.Choices = {};
/*
 * Get choice
 * 
 * ** Attributes **
 * 
 * * ``formId``
 * * ``choicesId``
 * 
 * ** Returns **
 * 
 * choices:list<object>
 */
ximpia.common.Choices.get = function(formId, choicesId) {
	// Integrate here the new location for choices object
	var list = JSON.parse($('#id_' + formId + '_choices').attr('value'))[choicesId] || null;
	return list;
}
/*
 * Get choice data for dataId
 */
ximpia.common.Choices.getData = function(formId, choicesId, dataId) {
	var choiceList = ximpia.common.Choices.get(formId, choicesId);
	var data = '';
	for (j in choiceList) {
		if (choiceList[j][0] == dataId) {
			data = choiceList[j][1];
		}
	}
	return data
}
/*
 * Checks for value
 * 
 * ** Attributes **
 * 
 * * ``formId``
 * * ``choicesId``
 * * ``data``
 * 
 * ** Returns **
 * check:boolean
 */
ximpia.common.Choices.hasValue = function(formId, choicesId, data) {
	var choiceList = ximpia.common.Choices.get(formId, choicesId);
	var check = false;
	for (j in choiceList) {
		if (choiceList[j][1] == data) {
			check = true;
		}
	}
	return check
}
/*
 * Get choice data by name
 */
ximpia.common.Choices.getByName = function(formId, choicesId, name) {
	var choiceList = ximpia.common.Choices.get(formId, choicesId);
	var choiceData = null;
	for (j in choiceList) {
		if (choiceList[j][0] == name) {
			choiceData = choiceList[j];
		}
	}
	return choiceData;
}
/*
 * Get choice data by value
 */
ximpia.common.Choices.getByValue = function(formId, choicesId, value) {
	var choiceList = ximpia.common.Choices.get(formId, choicesId);
	var choiceData = null;
	for (j in choiceList) {
		if (choiceList[j][1] == value) {
			choiceData = choiceList[j];
		}
	}
	return choiceData;
}

/*
 ximpia.common.ClassType10 = function() {
 var _attr = {
 priv: {
 _var1 : 9,
 _doSomething: (function() {
 var a = 3;
 alert('No soy lo que crees');
 ximpia.console.log('Holaaa')
 })
 },
 pub: {
 MY_CONSTANT : 18726,
 myMethod1: (function() {
 alert('myMethod!!!' + _attr.priv.var1);
 var d = 2;
 var j = "Hola";
 ximpia.console.log('myMethod1...');
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
/*
 * Get attributes for view
 */
ximpia.common.Window.getViewAttrs = (function() {
	$.metadata.setType("attr", "data-xp");
	var viewData = $('#id_view').metadata();
	return viewData;
});
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
	var sButtons = '';
	var sEffectIn = 'fadeIn,500';
	var sEffectOut = '';
	var bFadeBackground = true;
	var iWidth = null;
	var iHeight = null;
	var isHidden = false;
	functionShow = null;
	ximpia.console.log('showMessage :: Will do...');
	ximpia.console.log('showMessage :: messageOptions...');
	ximpia.console.log(messageOptions);
	if (messageOptions.title)
		sTitle = messageOptions.title;
	if (messageOptions.message)
		sMessage = messageOptions.message;
	if (messageOptions.buttons)
		buttons = messageOptions.buttons;
	if (messageOptions.effectIn)
		effectIn = messageOptions.effectIn;
	if (messageOptions.effectOut)
		effectOut = messageOptions.effectOut;
	if (messageOptions.fadeBackground)
		bFadeBackground = messageOptions.fadeBackground;
	if (messageOptions.width)
		iWidth = messageOptions.width;
	if (messageOptions.height)
		iHeight = messageOptions.height;
	if (messageOptions.functionShow)
		functionShow = messageOptions.functionShow;
	if (messageOptions.isHidden)
		isHidden = messageOptions.isHidden;
	bFadeOut = ximpia.common.Window.checkFadeOut();
	if (!bFadeOut) {
		bFadeBackground = false;
	}
	iScreenWidth = document.body.clientWidth;
	if (iWidth) {
		$("div.PopMessage").css('width', iWidth + 'px');
		$("div#PopMsgWrapper").css('width', iWidth + 'px');
	} else {
		$("div.PopMessage").css('width', '450px');
		$("div#PopMsgWrapper").css('width', '450px');
	}
	// Max Height is 400 pixels
	// TODO: Make this dynamic depending on system resolution
	if (iHeight > 400)
		iHeight = 400;
	if (iHeight) {
		$("div.MsgText").css('height', iHeight + 'px');
		var iTopPosition = 80;
	}
	iLeft = (iScreenWidth / 2) - parseInt($("div.PopMessage").css('width')) / 2;
	if (!$.browser.msie) {
		iTopOffset = window.pageYOffset;
	} else {
		iTopOffset = document.documentElement.scrollTop;
	}
	if (!iHeight) {
		$("div.MsgText").css('overflow', 'auto');
		var iTopPosition = 110;
	}
	iTop = iTopPosition + iTopOffset;
	$("div.MsgTitle").html('<div style="border: 0px solid; float: left; padding:7px 20px; width: 370px">' + sTitle + '</div>');
	$("div.MsgText").html(sMessage);
	ximpia.console.log('showMessage :: MsgText height...');
	ximpia.console.log($('div.MsgText').height());
	ximpia.console.log('showMessage :: buttons: ' + buttons);
	$("div.MsgButtons").text('');
	$("div.MsgButtons").append(buttons);
	effectInTxt = effectIn.style;
	iEffectInTime = parseInt(effectIn.time);
	$("div.Pops").css('left', iLeft + 'px');
	$("div.Pops").css('top', iTop + 'px');
	$("div.PopMessage").fadeIn(iEffectInTime);
	if (isHidden == false) {
		if (bFadeBackground) {
			$("#Wrapper").fadeTo("fast", 0.50);
		}
	}
	// Position vertical align message area
	ximpia.console.log('showMessage :: div.msgPopBody: ' + $('div.msgPopBody').html());
	ximpia.console.log('showMessage :: div.msgPopBody: ' + $('div.msgPopBody').height());
	ximpia.console.log('showMessage :: div.MsgText: ' + $('div.MsgText').height());
	if (functionShow) {
		functionShow($(this));
	}
});
/**
 * Click Ok Button
 */
ximpia.common.Window.clickMsgOk = (function(evt, bFadeBackground, functionName) {
	evt.preventDefault();
	bFadeOut = ximpia.common.Window.checkFadeOut();
	$("div.PopMessage").fadeOut(500, function() {
		$("#id_pops").remove();
	});
	if (bFadeBackground) {
		$("#Wrapper").fadeTo("fast", 1.0);
	}
	if (functionName) {
		functionName();
	}
	if (!bFadeOut) {
		bFadeBackground = false;
	}
});
/**
 * Construct PopUp html
 */
ximpia.common.Window.createPopHtml = (function() {
	if (!$("#id_pops").length) {
		var htmlPage = "<div id=\"id_pops\" class=\"Pops\" ><div id=\"PopMessage\" class=\"PopMessage\"><div id=\"PopMsgWrapper\"><div class=\"MsgTitle\"></div><div style=\"float: right ; width: 21px; margin-top: -41px; margin-right: -3px\"><a id=\"id_btX\" href=\"#\" class=\"buttonIcon btX\" >X</a></div><div class=\"MsgText\" style=\"clear: both\"></div><div class=\"MsgButtons\"></div></div><br class=\"clearfloat\" /></div><!--[if lte IE 6.5]><iframe></iframe><![endif]--></div>";
		$("body").append(htmlPage);
	}
});
/**
 * Show Pop Up. It is used for Ajax actions, like OK Message, Error messages, etc...
 */
ximpia.common.Window.showPopUp = (function(key) {
	ximpia.common.Window.createPopHtml();
	if ( typeof key == 'string') {
		var sId = key;
		var messageOptions = new Object();
	} else {
		var messageOptions = key;
		var sId = '';
	}
	var sFadeOut = '';
	var sUrl = '';
	var sTitle = '';
	var sMessage = '';
	var iHeight = null;
	functionName = null;
	ximpia.console.log('sId : ' + sId);
	if (sId.length != 0) {
		var popUpData = eval($("#" + sId).attr('value'));
		sTitle = popUpData[0];
		message = popUpData[1].replace(/[:]{2}[p][:]{2}/g, '</p>');
		message = message.replace(/[:][p][:]/g, '<p>');
		sMessage = '<table><tr><td style="vertical-align:top"><img class="' + popUpData[2] + '" src="' + $("#id_siteMedia").attr('value') + 'images/blank.png" /></td><td style="vertical-align:top">' + message + '</td></tr></table>'
	} else {
		sFadeOut = messageOptions.fadeout;
		bFadeOut = messageOptions.fadeBackground;
		sUrl = messageOptions.url;
		sTitle = messageOptions.title;
		sMessage = messageOptions.message;
		iHeight = messageOptions.height;
		functionName = messageOptions.functionName;
	}
	if (!sFadeOut) {
		sFadeOut = ''
		bFadeOut = true;
	} else {
		if (sFadeOut == '') {
			bFadeOut = true;
		} else {
			bFadeOut = false;
		}
	}
	bIE = ximpia.common.Browser.checkIE();
	if (bIE) {
		bFadeOut = false;
	}
	// This is to prevent fadeouts in popups since Internet Explorer does not show frame border
	sFadeOut = '';
	//var closeValue = ximpia.common.List.getValue('id_buttonConstants', 'close');
	var closeValue = 'Close';
	ximpia.common.Window.showMessage({
		title : sTitle,
		message : sMessage,
		buttons : 'id_msgClose:' + closeValue + ':delete',
		effectIn : 'fadeIn,1000',
		effectOut : sFadeOut,
		fadeBackground : bFadeOut
	});
	//showMessage(sTitle, sMessage, 'MsgOk:OK', 'fadeIn,1000', sFadeOut, bFadeOut);
	if (sFadeOut == '') {
		$("#id_msgClose").click(function() {
			ximpia.common.Window.clickMsgOk(bFadeOut, functionName)
		});
		$("#id_btX").click(function() {
			ximpia.common.Window.clickMsgOk(bFadeOut, functionName)
		});
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
	} else {
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
	/*var labelTransform = function(labelText, optionIndex){ //scope (this) is the #menu element
	rtn = "<div class='jqDockLabelNew' style='position: relative'>" + labelText + "</div>";
	return rtn;
	},
	dockOptions = { align: 'top' // horizontal menu, with expansion DOWN from a fixed TOP edge
	, labels: true  // add labels (defaults to 'br')
	, size: 45
	,setLabel: labelTransform
	};
	// ...and apply...
	$('#IconMenu').jqDock(dockOptions);*/
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
	var siteMedia = ximpia.settings.SITE_MEDIA_URL;
	return siteMedia;
});
/**
 * Get server path
 */
ximpia.common.Path.getServer = (function() {
	var server = ximpia.settings.HOST + '/';
	return server;
});
/**
 * Get business path: jxService
 */
ximpia.common.Path.getBusiness = (function() {
	var path = ximpia.common.Path.getServer() + 'jxService';
	return path;
});
/**
 * Get service path: jxService
 */
ximpia.common.Path.getService = (function() {
	var path = ximpia.common.Path.getServer() + 'jxService';
	return path;
});
/*
 * Get save path
 */
ximpia.common.Path.getSave = (function() {
	var path = ximpia.common.Path.getServer() + 'jxSave';
	return path;
});
/*
 * Get delete path
 */
ximpia.common.Path.getDelete = (function() {
	var path = ximpia.common.Path.getServer() + 'jxDelete';
	return path;
});
/*
 * Get template for popups and views
 *
 */
ximpia.common.Path.getTemplate = (function(app, name, tmplType) {
	return ximpia.common.Path.getServer() + 'jxTemplate/' + app + '/' + tmplType + '/' + name;
});

ximpia.common.Browser = {};
/**
 * Check Internet Explorer IE6
 */
ximpia.common.Browser.checkIE6 = (function() {
	if (jQuery.browser.msie && jQuery.browser.version.substr(0, 3) == '6.0') {
		bIE6 = true;
	} else {
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
	} else {
		bIE = false;
	}
	return bIE
});
/*
 * Get url parameter value by name
 */
ximpia.common.Browser.fetchParamByName = (function(name) {
	name = name.replace(/[\[]/, "\\\[").replace(/[\]]/, "\\\]");
	var regexS = "[\\?&]" + name + "=([^&#]*)";
	var regex = new RegExp(regexS);
	var results = regex.exec(window.location.href);
	if (results == null)
		return "";
	else
		return results[1];
});
/*
 * Get form from xpForm, like xpData.my_form
 */
ximpia.common.Browser.getForm = (function(xpForm) {
	return xpForm.split('.')[1];
});
/*
 * Build xpForm literal from view name and form name
 */
ximpia.common.Browser.buildXpForm = (function(viewName, formId) {
	return 'xpData-view-' + viewName + '.' + formId
});
/*
 * Set key in browser
 */
ximpia.common.Browser.setObject = (function(keyName, data) {
	sessionStorage.setItem(keyName, JSON.stringify(data));
})
/*
 * Get key data from browser
 */
ximpia.common.Browser.getObject = (function(keyName) {
	var dataS = sessionStorage.getItem(keyName);
	data = JSON.parse(dataS);
	return data
})
/**
 * Get response object
 * 
 * **Attributes**
 * 
 * **Returns**
 * 
 * Response object from xpData-view session storage variable
 *  
 */
ximpia.common.Browser.getResponse = (function() {
	var viewObj = ximpia.common.Browser.getObject('xpData-view');
	return viewObj.response;
});
/**
 * Delete key from session storage
 */
ximpia.common.Browser.deleteObject = (function(keyName) {
	sessionStorage.removeItem(keyName);
});
/*
 * Get form data from sessionStorage
 */
ximpia.common.Browser.getFormDataFromSession = (function(xpForm) {
	ximpia.console.log('getFormDataFromSession :: xpForm: ' + xpForm);
	var fields = xpForm.split('.');
	//var data = JSON.parse(sessionStorage.getItem(fields[0]))['response'][fields[1]];
	//ximpia.console.log(sessionStorage.getItem('xpData-view'));
	var data = JSON.parse(sessionStorage.getItem('xpData-view'))['response'][fields[1]];
	return data
});
/*
 * Set sessionStorage xpData with viewname
 */
ximpia.common.Browser.setXpDataView = (function(viewName, data) {
	// 29/05/2012 : We only keep a view key
	//sessionStorage.setItem('xpData-view-' + viewName, JSON.stringify(data));
	sessionStorage.setItem('xpData-view', JSON.stringify(data));
});
/**
 * Set sessionStorage xpData with viewName. Attibute data comes serialzed and needs not to be serialzed with JSON
 */
ximpia.common.Browser.setXpDataViewSerial = (function(viewName, data) {
	// 29/05/2012 : We only keep a view key
	//sessionStorage.setItem('xpData-view-' + viewName, data);
	sessionStorage.setItem('xpData-view', data);
});
/*
 * Set sessionStorage for action
 */
ximpia.common.Browser.setSessionAction = (function(data) {
	sessionStorage.setItem('xpData-action', JSON.stringify(data));
});
/*
 * Set sessionStorage for popup
 */
ximpia.common.Browser.setSessionPopUp = (function(data) {
	sessionStorage.setItem('xpData-popup', JSON.stringify(data));
});
/*
 * Get view name from the xpForm, xpData-view-$view.form_$formId
 */
ximpia.common.Browser.getView = (function(xpForm) {
	var viewName = xpForm.split('.')[0].split('-')[2]
	return viewName
});
/*
 * Add response attribute
 * 
 * ** Attributes**
 * 
 * * ``name``:String
 * * ``value``:String
 * 
 * ** Returns **
 * 
 * None
 * 
 */
ximpia.common.Browser.putAttr = (function(name, value) {
	// I get the xpData-view object with response data
	var viewObj = ximpia.common.Browser.getObject('xpData-view');
	// Set attribute
	viewObj.response[name] = value;
	// Set new response
	ximpia.common.Browser.setObject('xpData-view', viewObj);
});
/*
 * Get application from response object
 * 
 * ** Returns **
 * 
 * Application name, like ximpia.site
 * 
 */
ximpia.common.Browser.getApp = (function() {
	var response = ximpia.common.Browser.getResponse();
	return response.app
});

ximpia.common.Session = {};
/**
 * Get object from session
 */
ximpia.common.Session.get = (function(keyName) {
	var sessionObj = ximpia.common.Browser.getObject('session')
	var value = '';
	if (sessionObj.hasOwnProperty(keyName)) {
		value = sessionObj[keyName];
	}
	return value;
});

ximpia.common.BasicTags = function() {
	var _attr = {
		priv : {
			/**
			 * header tag
			 */
			head : function() {
				ximpia.console.log('head...');
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
			header : function() {
				ximpia.console.log('header...');
				var htmlI = $("header").html();
				var sm = ximpia.common.Path.getSiteMedia();
				var contentLength = $("header div").length;
				ximpia.console.log('contentLength : ' + contentLength);
				if (contentLength < 1) {
					htmlI = "<div id=\"Header\" >";
					htmlI += "<div id=\"Logo\">";
					htmlI += "<a href=\"#\" onclick=\"return false\"><img id=\"LogoImg\" src=\"" + ximpia.settings.SITE_MEDIA_URL + "images/blank.png\" alt=\" \" /> </a>";
					htmlI += "</div>";
					htmlI += "<nav>";
					htmlI += "<div id=\"id_loginForm\"></div>";
					htmlI += "<div id=\"IconMenu\">";
					htmlI += "<div style=\"border: 1px solid; float: left\"><a href=\"#\" onclick=\"return false\"><img src=\"" + ximpia.settings.SITE_MEDIA_URL + "images/add_48.png\" style=\"width: 30px, height: 30px\" /></a></div>";
					htmlI += "<!--<img src=\"" + ximpia.settings.SITE_MEDIA_URL + "images/users_two_60.png\" title=\"Friends\" alt=\"Friends\" />";
					htmlI += "<img src=\"" + ximpia.settings.SITE_MEDIA_URL + "images/paper_content_60.png\" title=\"About Us\" alt=\"About Us\" />";
					htmlI += "<img src=\"" + ximpia.settings.SITE_MEDIA_URL + "images/mail_add_60.png\" title=\"Contact Us\" alt=\"Contact Us\" />";
					htmlI += "<img src=\"" + ximpia.settings.SITE_MEDIA_URL + "images/lock_60.png\" title=\"Privacy\" alt=\"Privacy\" />";
					htmlI += "<img src=\"" + ximpia.settings.SITE_MEDIA_URL + "images/go_60.png\" title=\"Login\" alt=\"Login\" />-->";
					htmlI += "</div>";
					htmlI += "</nav>";
					htmlI += "</div>";
					//$("header").html(htmlI);
				}
			},
			/**
			 * footer tag
			 */
			footer : function() {
				ximpia.console.log('footer...');
				var htmlI = $("footer").html();
				var sm = ximpia.common.Path.getSiteMedia();
				var contentLength = $("footer div").length;
				if (contentLength < 1) {
					htmlI = "<div id=\"id_footerContent\">";
					htmlI += "<div id=\"id_footerText\">";
					htmlI += "<div  style=\" float: left;; margin-left: 10px; margin-top: -5px\">&copy; 2011 &nbsp;<a href=\"http://www.ximpia.com\"><img id=\"XimpiaLogo\"";
					htmlI += "src=\"http://ximpia-test.s3.amazonaws.com/images/blank.gif\"";
					htmlI += "alt=\"Ximpia Inc\" title=\"Ximpia Inc\" /></a>";
					htmlI += "</div>";
					htmlI += "<div><span><a href=\"http://twitter.com/ximpia\" target=\"site\">@ximpia</a></span></div>";
					htmlI += "</div>";
					htmlI += "</div>";
					$("footer").html(htmlI);
				}
			}
		},
		pub : {
			/**
			 * Insert page tags : head, header and footer
			 */
			pageTags : function() {
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
		priv : {},
		pub : {
			/**
			 * callback method for submit signup click.
			 */
			doSubmitButton : function() {
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
			 * Do action form submit. Will post form to server and write to sessionStorage xpData-action results
			 * obj: formId
			 *
			 * Options
			 * =======
			 * attrs: 		Button attributes: action, align, callback, form, method, text, type
			 * callback: 		Callback function
			 * idActionComp: 	Id of button to bind
			 * isMsg: 		Show message area check
			 * isMsg: 		Id of message area
			 * showPopUp: 		Check if new popup is shown to display validation errors in form and system error.
			 * 			false for popup buttons.
			 * destroyMethod: 	Button plugin method to use to destroy message area.
			 *
			 */
			bindAction : function(obj) {
				//$("#" + obj.formId).val(ximpia.common.Path.getBusiness());
				//ximpia.console.log('Submit form: ' + $("#" + obj.formId).val());
				ximpia.console.log('bindAction :: obj...');
				ximpia.console.log(obj);
				var idOkMsg = '';
				var okMsg = '';
				var doMsgError = false;
				$("#" + obj.attrs.form).validate({
					submitHandler : function(form) {
						$(form).ajaxSubmit({
							dataType : 'json',
							success : function(response, status) {
								ximpia.console.log('bindAction :: suscess');
								ximpia.console.log(response);
								// Set action into session
								ximpia.common.Browser.setSessionAction(response);
								var responseMap = eval(response);
								statusCode = responseMap['status'];
								if (statusCode.indexOf('.') != -1) {
									statusCode = statusCode.split('.')[0]
								}
								ximpia.console.log('bindAction :: form :: statusCode : ' + statusCode);
								if (statusCode == 'OK') {
									ximpia.console.log('bindAction :: isMsg: ' + obj.isMsg);
									if (obj.isMsg == true) {
										$("#" + obj.idMsg + "_img").xpLoadingSmallIcon('ok');
										var okMessagesStr = responseMap['response'][obj.attrs.form]['okMessages'].value;
										var okMessages = JSON.parse(okMessagesStr);
										okMsg = responseMap['response'][obj.attrs.form]['msg_ok'].value;
										var msg = '';
										if (okMsg.length != 0) {
											msg = okMsg;
										} else {
											if (obj.attrs.hasOwnProperty('msg')) {
												msg = okMessages[obj.attrs.msg];
											} else {
												var msgList = ximpia.common.Object.values(okMessages);
												if (msgList.length != 0) {
													msg = ximpia.common.Object.values(okMessages)[0];
												}
											}
										}
										ximpia.console.log('bindAction :: okMsg: ' + msg);
										$("#" + obj.idMsg + "_text").text(msg);										
										
										var timeout = setTimeout(function() {
											$("#" + obj.idMsg).animate({top: parseInt($('#' + obj.idMsg).css('top')) + 30});
										}, ximpia.settings.pagebutton.msg.slideTimeout);
										
									} else {
										if (responseMap['response']['winType'] == 'popup') {
											// popup : Must show in same popup
											ximpia.console.log('bindAction :: popup!!!!!!!!!!');
											$("#" + obj.idMsg).xpButton(obj.destroyMethod);
											ximpia.console.log(obj.attrs);
											var tmplPath = ximpia.common.PageAjax.getTemplatePath({
												app : responseMap['response']['app'],
												name : responseMap['response']['view'],
												viewType : obj.attrs.viewType
											});
											ximpia.console.log('bindAction :: tmplPath: ' + tmplPath)
											$.get(tmplPath, function(data) {
												var tmplData = data;
												var viewName = responseMap['response']['view'];
												ximpia.console.log('bindAction :: viewName: ' + viewName);
												ximpia.console.log('bindAction :: Got template');
												//ximpia.console.log(tmplData);
												ximpia.common.Browser.setObject('xpData-popup-tmpl', tmplData);
												var elemContent = $(tmplData).find('#id_' + viewName);
												ximpia.console.log('bindAction :: elemContent...');
												ximpia.console.log(elemContent);
												var popupData = $(tmplData).filter('#id_conf').metadata();
												var elementButtons = $(tmplData).filter('#id_sectionButton');
												ximpia.console.log('bindAction :: elementButtons...');
												ximpia.console.log(elementButtons);
												ximpia.console.log('bindAction :: popupData...');
												ximpia.console.log(popupData);
												var height = null;
												var width = null;
												if (popupData.height)
													height = popupData.height;
												if (popupData.width)
													width = popupData.width;
												ximpia.console.log('bindAction :: height: ' + height);
												ximpia.console.log('bindAction :: width: ' + width);
												var form = $(elemContent).find('form')[0];
												ximpia.console.log('bindAction :: form...');
												ximpia.console.log(form);
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
												if (height > 400)
													height = 400;
												$("div.MsgText").css('height', height + 'px');
												var xpForm = 'xpData-view-' + viewName + '.' + form.id;
												ximpia.console.log('bindAction :: xpForm: ' + xpForm);
												ximpia.common.PageAjax.doRender(xpForm);
												ximpia.common.timeOutCounter(function() {
													$('.btBar').css('visibility', 'visible');
													ximpia.common.PageAjax.doFade();
													var oForm = ximpia.common.Form();
													oForm.doBindBubbles();
												});
											}).error(function(jqXHR, textStatus, errorThrown) {
												ximpia.console.log('bindAction :: get html template ERROR!!!! : ' + textStatus + ' ' + errorThrown);
											});
										} else {
											// window
											ximpia.console.log('bindAction :: window!!!!!!!!!!!');
											$("#" + obj.idMsg).xpButton(obj.destroyMethod);
											// Get template
											ximpia.console.log(obj.attrs);
											var tmplPath = ximpia.common.PageAjax.getTemplatePath({
												app : responseMap['response']['app'],
												name : responseMap['response']['view'],
												viewType : obj.attrs.viewType
											});
											ximpia.console.log('tmplPath: ' + tmplPath)
											$.get(tmplPath, function(data) {
												ximpia.common.PageAjax.doTmplInject(data);
												// Do menus
												ximpia.common.PageAjax.processMenus(responseMap);
												ximpia.console.log('bindAction :: menus...');
												// Update session data into SessionStorage
												// Render template
												ximpia.common.PageAjax.doFormsRender({
													viewName : responseMap['response']['view'],
													data : response
												});
												ximpia.common.PageAjax.positionBars();
												// Update session data into SessionStorage
												// Process login and logout layout changes
												ximpia.common.PageAjax.processLogin(responseMap);
											}).error(function(jqXHR, textStatus, errorThrown) {
												ximpia.console.log('bindAction :: get html template ERROR!!!! : ' + textStatus + ' ' + errorThrown);
											});
										}
									}
									// Put all fields inside form valid that are now errors
									$(".error").addClass('valid').removeClass("error");
									ximpia.console.log('bindAction :: clickStatus: ' + obj.attrs.clickStatus);
									if ( typeof obj.attrs.clickStatus != 'undefined' && obj.attrs.clickStatus == 'disable') {
										//ximpia.console.log('disable on click: ' + obj.attrs.disableOnClick + ' ' + obj.idActionComp);
										$("#" + obj.idActionComp).xpButton('disable');
									}
									// Callback
									if ( typeof obj.callback != 'undefined') {
										//ximpia.console.log('form :: callback : ' + obj.callback);
										obj.callback();
									}
								} else {
									// Business Error Messages
									// Can be associated to fields or not
									// Integrate showMessage, popUp, etc...
									var list = responseMap['errors'];
									ximpia.console.log('list errors...');
									ximpia.console.log(list);
									if (list.length > 0) {
										doMsgError = list[0][2]
									}
									ximpia.console.log('bindAction :: doMsgError: ' + doMsgError);
									ximpia.console.log('bindAction :: isMsg: ' + obj.isMsg);
									if (doMsgError == true) {
										$("#" + obj.idMsg + "_img").xpLoadingSmallIcon('error');
										$("#" + obj.idMsg + "_text").text(list[0][1]);
										/*obj.isMsg = true;
										 if (obj.isMsg == true) {
										 $("#" + obj.idMsg + "_img").xpLoadingSmallIcon('error');
										 $("#" + obj.idMsg + "_text").text(list[0][1]);
										 } else {
										 $("#" + obj.idMsg).xpButton(obj.destroyMethod);
										 }*/
									} else {
										ximpia.console.log('bindAction :: form :: errors: ' + list);
										obj.showPopUp = true;
										if (obj.showPopUp == true) {
											message = '<ul>'
											var errorName = "";
											var errorId = "";
											for (var i = 0; i < list.length; i++) {
												errorId = list[i][0];
												errorName = $("label[for='" + errorId + "']").text();
												ximpia.console.log('bindAction :: errorName : ' + errorName + ' errorId: ' + errorId);
												var errorMessage = list[i][1];
												$("#" + errorId).removeClass("valid");
												$("#" + errorId).addClass("error");
												if (errorName.length != 0) {
													message = message + '<li><b>' + errorName + '</b> : ' + errorMessage + '</li>';
												} else {
													message = message + '<li>' + errorMessage + '</li>';
												}
											}
											message = message + '</ul>';
											ximpia.console.log(message);
											//$("#" + obj.idMsg + "_img").xpLoadingSmallIcon('error');
											//$("#" + obj.idMsg + "_text").text('Error!!!');
											$("#" + obj.idMsg).xpButton(obj.destroyMethod);
											// Show error Message in pop up
											$('body').xpPopUp({
												title : 'Errors Found',
												message : message,
												height : 160
											}).xpPopUp('createMsg');
										} else {
											$("#" + obj.idMsg + "_img").xpLoadingSmallIcon('error');
											$("#" + obj.idMsg + "_text").text('Error!!!');
										}
									}
								}
							},
							error : function(data, status, e) {
								ximpia.console.log('bindAction :: ' + data + ' ' + status + ' ' + e);
								var errorMsg = 'I cannot process your request due to an unexpected error. Sorry for the inconvenience, please retry later. Thanks';
								if (obj.showPopUp == true) {
									// All have a waiting message
									/*if (doMsgError == false) {
									 $("#" + obj.idMsg).xpButton(obj.destroyMethod);
									 }*/
									$("#" + obj.idMsg).xpButton(obj.destroyMethod);
									$('body').xpPopUp({
										title : 'Could not make it!',
										message : errorMsg
									}).xpPopUp('createMsg');
								} else {
									//TODO: Place errors in ximpia.errors.NAME_ERROR, placed outside of ximpia.common.js
									errorMsg = 'I received an unexpected error. Please retry later. Thanks';
									$("#" + obj.idMsg + "_img").xpLoadingSmallIcon('error');
									$("#" + obj.idMsg + "_text").text(errorMsg);
								}
							}
						});
					},
					errorPlacement : function(error, element) {
						ximpia.console.log('bindAction :: error placement...');
						ximpia.console.log(error);
						ximpia.console.log(element);
						ximpia.console.log('bindAction :: error placement...');
						element.next("img table").after(error);
					}
				});
			},
			/**
			 * Bind signup submit button. Binds the click event of button, shows waiting icon, sends data through AJAX
			 */
			doBindSubmitForm : function(formId, callbackFunction) {
				$("a.button[data-xp-js='submit']").click(_attr.pub.doSubmitButton);
				$("#" + formId).validate({
					submitHandler : function(form) {
						// Submit form
						var idImg = form.id + '_Submit_Status';
						var idTxt = form.id + '_Submit_Text';
						$("#" + idImg).xpLoadingSmallIcon();
						$("#" + idImg).xpLoadingSmallIcon('wait');
						$("#" + idTxt).text('');
						$(form).ajaxSubmit({
							dataType : 'json',
							success : function(response, status) {
								var responseMap = eval(response);
								statusCode = responseMap['status'];
								if (statusCode.indexOf('.') != -1) {
									statusCode = statusCode.split('.')[0]
								}
								ximpia.console.log('statusCode : ' + statusCode);
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
										if ( typeof callbackFunction != 'undefined') {
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
									for (var i = 0; i < list.length; i++) {
										//var errorId = list[i][0];
										errorId = list[i][0];
										errorName = $("label[for='" + errorId + "']").text();
										ximpia.console.log('errorName : ' + errorName + ' errorId: ' + errorId);
										var errorMessage = list[i][1];
										//alert(errorId);
										$("#" + errorId).removeClass("valid");
										$("#" + errorId).addClass("error");
										message = message + '<li><b>' + errorName + '</b> : ' + errorMessage + '</li>';
									}
									message = message + '</ul>';
									// Show error Message in pop up
									ximpia.common.Window.showPopUp({
										title : 'Validation Errors Found',
										message : message,
									});
								}
							},
							error : function(data, status, e) {
								//alert(data + ' ' + status + ' ' + e);
								ximpia.console.log(data + ' ' + status + ' ' + e);
								$("#" + idImg).xpLoadingSmallIcon('errorWithPopUp');
								ximpia.common.Window.showPopUp({
									title : 'System Error',
									message : 'I cannot process your request due to an unexpected error. Sorry for the inconvenience, please retry later. Thanks',
									height : 50
								});
							}
						});
					},
					errorPlacement : function(error, element) {
						element.next("img table").after(error);
					}
				});
			},
			doReloadCaptcha : function() {
				$("#id_ImgRefreshCaptcha").click(function() {
					// reload captcha
					$.get('/reloadCaptcha');
					// Show image
					var kk = Math.random();
					$("#id_ImgCaptcha").attr('src', '/captcha/captcha.png?code=' + kk);
				});
			},
			/*
			 * Bind tooltip for button
			 */
			doBindButton : function(element) {
				$(element).qtip({
					content : {
						attr : 'data-xp-title'
					},
					events : {
						focus : function(event, api) {
						}
					},
					position: {
						my: 'bottom center',
						at: 'top center',
						adjust: {
							y: -2
						}
					},
					style : {
						//classes : 'ui-tooltip-blue ui-tooltip-shadow ui-tooltip-rounded ui-tooltip-cluetip'
						classes: 'ui-tooltip-dark ui-tooltip-shadow ui-tooltip-rounded ui-tooltip-opacity'
					}
				});				
			},
			/**
			 * Tooltip for form labels
			 */
			doBindBubbles : function() {
				$("label.info").mouseover(function() {
					$(this).css('cursor', 'help');
				});
				$("label.info").qtip({
					content : {
						attr : 'data-xp-title'
					},
					events : {
						focus : function(event, api) {
						}
					},
					style : {
						width : 200,
						classes : 'ui-tooltip-blue ui-tooltip-shadow ui-tooltip-rounded ui-tooltip-cluetip'
					}
				});
				$("a.button").qtip({
					content : {
						attr : 'data-xp-title'
					},
					events : {
						focus : function(event, api) {
						}
					},
					position: {
						my: 'bottom center',
						at: 'top center',
						adjust: {
							y: -2
						}
					},
					style : {
						//classes : 'ui-tooltip-blue ui-tooltip-shadow ui-tooltip-rounded ui-tooltip-cluetip'
						classes: 'ui-tooltip-dark ui-tooltip-shadow ui-tooltip-rounded ui-tooltip-opacity'
					}
				});
				if (ximpia.settings.IMAGE_TOOLTIP == true) {
					$("img").qtip({
						content : {
							attr : 'title'
						},
						events : {
							focus : function(event, api) {
							}
						},
						position: {
							/*my: 'top center',
							at: 'bottom center',*/
							target: 'mouse',
							adjust: {
								y: 20
							}
						},
						style : {
							//classes : 'ui-tooltip-blue ui-tooltip-shadow ui-tooltip-rounded ui-tooltip-cluetip'
							classes: 'ui-tooltip-dark ui-tooltip-shadow ui-tooltip-rounded ui-tooltip-opacity'
						}
					});
				}
			}
		}
	}
	return _attr.pub;
}
/**
 * Has to render
 * 
 * ** Attributes **
 * 
 * * ``element``:Object
 * * ``reRender``:Bolean
 * 
 * **Returns**
 * 
 * Boolean
 * 
 */
ximpia.common.Form.doRender = (function(element, reRender) {
	if ( typeof $(element).attr('data-xp-render') != 'undefined') {
		var isRender = $(element).attr('data-xp-render');
		ximpia.console.log('Form.doRender :: isRender: ', isRender);
		var doRender = false;
		//if (isRender == false || reRender == true) {
		if (reRender == true) {
			doRender = true;
		} else if (isRender == '' || isRender == 'true') {
			doRender = true;
		} else {
			doRender = false;
		}
	} else {
		var isRender = false;
		ximpia.console.log('Form.doRender :: isRender: ', isRender);
		var doRender = true;
	}
	return doRender;
});
/**
 * Has to render
 * 
 * ** Attributes **
 * 
 * * ``element``:Object
 * * ``reRender``:Bolean
 * 
 * **Returns**
 * 
 * Boolean
 * 
 */
ximpia.common.Form.hasToRender = (function(element, reRender) {
	return ximpia.common.Form.doRender(element, reRender);
});
/**
 * Get for from xpForm
 */
ximpia.common.Form.getForm = (function(xpForm) {
	var fields = xpForm.split('.');
	return fields[fields.length - 1]
});
/*
 * Append attribute values, separated by spaces
 */
ximpia.common.Form.appendAttrs = (function(idElement, attr, valueNew) {
	var exclude = {
		tabindex : ''
	};
	valueOld = $("#" + idElement).attr(attr);
	value = valueNew;
	if ( typeof valueOld != 'undefined') {
		if (!exclude.hasOwnProperty(attr)) {
			if (valueOld != valueNew && valueOld != '') {
				value = valueOld + ' ' + valueNew;
			} else if (valueOld != valueNew && valueOld == '') {
				value = valueNew;
			}
		}
	}
	$("#" + idElement).attr(attr, value);
}),
/*
 * Include attributes in form elements from metadata of div components and server attributes
 * obj:
 * djangoAttrs: List of attributes identified in django and should not pass to html
 * htmlAttrs: List of attributes that must be included in html as attributes. The ones not in the list will be included in data-xp
 * excludeList: List of attributes to exclude
 * dataAttrs: Attributes from server
 * attrs: Attributes from component in metadata
 * idElement: Id of form element to include attributes to
 * skipName: True|False . Weather skip assign name attribute
 *
 */
ximpia.common.Form.doAttributes = (function(obj) {
	var attrData = {};
	var attrDataS = "{";
	var valueNew = "";
	var valueOld = "";
	var value = '';
	ximpia.console.log('doAttributes :: skipName: ' + obj.skipName);
	for (attr in obj.dataAttrs) {
		if (ximpia.common.ArrayUtil.hasKey(obj.djangoAttrs, attr) == false) {
			if (ximpia.common.ArrayUtil.hasKey(obj.htmlAttrs, attr) == true) {
				if (attr != 'name' || (attr == 'name' && obj.hasOwnProperty('skipName') && obj.skipName != true)) {
					ximpia.console.log('doAttributes :: data attr: ' + attr + ' ' + obj.dataAttrs[attr]);
					ximpia.common.Form.appendAttrs(obj.idElement, attr, obj.dataAttrs[attr])
				}
			} else {
				if (attr.search('data') == 0) {
					ximpia.common.Form.appendAttrs(obj.idElement, attr, obj.dataAttrs[attr])
				} else {
					if (!attrData.hasOwnProperty(attr)) {
						if (Object.keys(attrData).length == 0) {
							attrDataS += attr + ": '" + obj.dataAttrs[attr] + "'";
						} else {
							attrDataS += ', ' + attr + ": '" + obj.dataAttrs[attr] + "'";
						}
						attrData[attr] = obj.dataAttrs[attr];
					}
				}
			}
		}
	}
	for (attr in obj.attrs) {
		ximpia.console.log('doAttributes :: attr: ' + attr);
		if (ximpia.common.ArrayUtil.hasKey(obj.htmlAttrs, attr) == true) {
			ximpia.common.Form.appendAttrs(obj.idElement, attr, obj.attrs[attr])
		} else {
			if (ximpia.common.ArrayUtil.hasKey(obj.excludeList, attr) == false) {
				if (attr.search('data') == 0) {
					ximpia.common.Form.appendAttrs(obj.idElement, attr, obj.attrs[attr])
				} else {
					if (!attrData.hasOwnProperty(attr)) {
						if (Object.keys(attrData).length == 0) {
							attrDataS += attr + ": '" + obj.attrs[attr] + "'";
						} else {
							attrDataS += ', ' + attr + ": '" + obj.attrs[attr] + "'";
						}
						attrData[attr] = obj.attrs[attr];
					}
				}
			}
		}
	}
	attrDataS += '}';
	$("#" + obj.idElement).attr('data-xp', attrDataS);
});


/**
 * Condition
 * 
 * Class with operations for ximpia condition rules and condition matching
 *  
 */
ximpia.common.Condition = {};
/**
 * Evaluate condition 
 * 
 * condition like...
 * ``settings.SIGNUP_USER_PASSWORD == true``
 * 
 * Strings...
 * ``view == "signup" && settings.SIGNUP_USER_PASSWORD == true``
 * 
 * 
 * OR : ``||``
 * AND : ``&&``
 * 
 * ==
 * !=
 * >
 * <
 * >=
 * <=
 * 
 * Paranthesis...
 * ``(isLogin == true) || (isLogin == false && view == "signup")
 * 
 * **Attributes**
 * 
 * * ``condition``:String : Evaluate condition
 * 
 * **Returns**
 * 
 * true / false
 * 
 */
ximpia.common.Condition.eval = (function(condition) {
	var resp = ximpia.common.Browser.getResponse();
	var patts = [/([a-zA-Z0-9._]+\ *==)/g, /([a-zA-Z0-9._]+\ *!=)/g, /([a-zA-Z0-9._]+\ *>)/g, /([a-zA-Z0-9._]+\ *<)/g, 
					/([a-zA-Z0-9._]+\ *>=)/g, /([a-zA-Z0-9._]+\ *<=)/g];
	var index = -1;
	var conditionNew = condition;
	for (var i = 0; i<patts.length; i++) {
		index = conditionNew.search(patts[i]);
		if (index != -1) {
			conditionNew = conditionNew.replace(patts[i],
				function( $0, $1, $2){
					return( "resp." + $0 );
				}
			);			
		}
	}
	ximpia.console.log('common.Condition.eval :: conditionNew: ' + conditionNew);
	var check = eval(conditionNew);
	return check;
});
/*
 * Processing evaluation condition rules. Returns evaluation object.
 * 
 * ** Attributes**
 * 
 * ** Returns ** 
 * 
 * Evaluation object:
 * 
 * {
 * 	conditionRule:Boolean
 * }
 * 
 * Processes all condition rules from attribute ``data-xp-cond-rules`` in ``id_view`` node and adds to evaluation object.
 * 
 * It calls method ``eval`` sending conditionRule.
 * 
 */
ximpia.common.Condition.processRules = (function() {
	// Get condition rules and Eval conditions and built evals 
	$.metadata.setType("attr", "data-xp-cond-rules");
	var conditionRules = $("#id_view").metadata();
	//ximpia.console.log('xpObjContainer :: conditionRules...');
	//ximpia.console.log(conditionRules);
	var evals = {};
	for (conditionRule in conditionRules) {
		var checkCondition = ximpia.common.Condition.eval(conditionRules[conditionRule]);
		evals[conditionRule] = checkCondition;
	}
	ximpia.console.log('xpObjContainer :: evals...');
	ximpia.console.log(evals);
	return evals;
});
/*
 * Process condition actions: Render
 * 
 * ** Attributes**
 * 
 * * ``element``:Object : Element
 * * ``evals``:Object : Condition evaluations
 * 
 * ** Returns **
 * 
 */
ximpia.common.Condition.doElements = (function(evals, element) {
	var conditions = $(element).metadata({type: 'attr', name: 'data-xp-cond'});
	ximpia.console.log('xpObjContainer :: conditions...');
	ximpia.console.log(conditions);
	if (conditions.hasOwnProperty('conditions')) {
		for (var c=0; c<conditions['conditions'].length; c++) {
			var condition = conditions['conditions'][c];
			ximpia.console.log('xpObjContainer :: condition: ' + condition.condition);
			if (condition.action == 'render') {
				var conditionCheck =  evals[condition.condition];
				ximpia.console.log('xpObjContainer :: conditionCheck: ' + conditionCheck + ' condition.value: ' + condition.value);
				if (condition.value == true && conditionCheck == true) {
					ximpia.console.log('xpObjContainer :: I render true elements in container...');
					$(element).css('display', 'block');
					$(element).children().attr('data-xp-render', 'true');
					$(element).children().css('display', 'block');
					// TODO: Call render api method of component
				} else if(condition.value == false && conditionCheck == true) {
					ximpia.console.log('xpObjContainer :: I render false elements in container...');
					$(element).css('display', 'none');
					$(element).children().attr('data-xp-render', 'false');
					$(element).children().css('display', 'none');
					$(element).children().children().remove();
					// TODO: Call unrender api method of component
				} else {
					ximpia.console.log('xpObjContainer :: I render false elements in container...');
					$(element).css('display', 'none');
					$(element).children().attr('data-xp-render', 'false');
					$(element).children().css('display', 'none');
					$(element).children().children().remove();
					// TODO: Call unrender api method of component
				}
			} else if (condition.action == 'disable') {
				// TODO: Implement disable action				
			}
		}
	}
});

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
		dataType : 'json',
		async : false,
		timeout : 2000,
		success : function(responseMap, status) {
			if (responseMap && responseMap.status && responseMap.response) {
				statusCode = responseMap['status'];
				if (statusCode == 'OK') {
					results = responseMap.response;
				}
			}
		},
		error : function(data, status, e) {
			alert('ERROR : ' + status);
			results = new Array()
		}
	});
	return results;
});

ximpia.common.PageAjax = function() {
	var _attr = {
		priv : {
			callback : null,
			path : ximpia.common.Path.getBusiness(),
			formId : "",
			sectionId : "",
			verbose : false,
			data : {},
			formData : {},
			/*doRenders: (function(xpForm) {
			 ximpia.console.log('xpForm: ' + xpForm);
			 var formId = xpForm.split('.')[1];
			 //ximpia.console.log('text: ' + $('#' + formId).find("[data-xp-type='basic.text']"));
			 $('#' + formId).find("[data-xp-type='basic.text']").xpInput('renderField', xpForm);
			 $('#' + formId).find("#id_variables").xpInput('addHidden', xpForm);
			 $('#' + formId).find("[data-xp-type='list.select']").xpListSelect('render', xpForm);
			 $('#' + formId).find("[data-xp-type='text.autocomplete']").xpInput('renderFieldAutoComplete', xpForm);
			 $('#' + formId).find("[data-xp-type='basic.textarea']").xpTextArea('render', xpForm);
			 $('#' + formId).find("input[data-xp-related='list.field']")
			 .filter("input[data-xp-type='basic.text']")
			 .xpListField('bindKeyPress', xpForm);
			 $("[data-xp-type='button']").xpButton('render');
			 $("[data-xp-type='link']").xpLink('render');
			 _attr.priv.doShowPasswordStrength('id_ximpiaId', 'id_password');
			 //_attr.priv.doLocal();
			 }),*/
			/*
			 * Process Google maps local
			 */
			doLocal : (function() {
				//ximpia.console.log($(".gmaps"));
				/*$(".gmaps").each(function() {
				 });*/
				ximpia.console.log('***************************************');
				ximpia.console.log( typeof $(".gmaps"));
				ximpia.console.log($(".gmaps").length);
				var values = $(".gmaps");
				var cityList = [];
				var countryList = [];
				$.metadata.setType("attr", "data-xp");
				var metaObj = {};
				for (var i = 0; i < values.length; i++) {
					ximpia.console.log(values[i]);
					ximpia.console.log(values[i].id);
					metaObj = $("#" + values[i].id).metadata();
					if (metaObj.gmaps == 'city') {
						cityList.push(values[i].id)
					} else {
						countryList.push(values[i].id)
					}
				}
				ximpia.console.log('cityList');
				ximpia.console.log(cityList);
				ximpia.console.log('countryList');
				ximpia.console.log(countryList);
				if (cityList.length != 0 || countryList.length != 0) {
					var oGoogleMaps = ximpia.common.GoogleMaps();
					oGoogleMaps.insertCityCountry(cityList, countryList);
				}
			})
			/**
			 * Show password strength indicator. Password leads to a strength variable. Analyze if this behavior is common
			 * and make common behavior. One way would be to have a data-xp-obj variable strength and be part of validation, showing
			 * the message of nor validating.
			 */
			/**doShowPasswordStrength: (function(userId, passwordId) {
			 // Password Strength
			 // TODO: Analyze a common way of associating a new variable to a input field, and influence click of a given button
			 // TODO: Include validation of strength when clicking on signup button or buttons
			 $('.passStrength').passStrengthener({
			 userid: "#" + userId
			 /*strengthCallback:function(score, strength) {
			 ximpia.console.log('strength : ' + strength)
			 if(strength == 'good' || strength == 'strong') {
			 $("#" + submitId).xpPageButton('enable', ximpia.common.Form().doSubmitButton);
			 } else {
			 $("#" + submitId).xpPageButton('disable');
			 }
			 }
			 });
			 })*/
		},
		pub : {
			init : function(obj) {
				_attr.priv.path = obj.path;
				_attr.priv.callback = obj.callback;
				_attr.priv.formId = obj.formId;
				_attr.priv.sectionId = obj.sectionId;
				_attr.priv.viewName = obj.viewName;
				_attr.priv.verbose = obj.verbose;
			},
			doFormOld : function() {
				$.getJSON(_attr.priv.path, function(data) {
					if (_attr.priv.verbose == true) {
						ximpia.console.log(data)
					}
					//ximpia.console.log(data)
					// forms
					var dataForm = data.response[_attr.priv.formId];
					//ximpia.console.log('dataForm : ' + dataForm);
					for (var key in dataForm) {
						var objId = $("#id_" + key).attr('id');
						var keyAttrs = dataForm[key];
						var element = keyAttrs.element;
						//ximpia.console.log(key + ' : ' + keyAttrs.value );
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
											//ximpia.console.log('help_text : ' + keyAttrs.help_text);
											$("label[for='" + 'id_' + key + "'].info").attr('data-xp-title', keyAttrs.help_text);
										} else {
											//ximpia.console.log('attr || ' + keyAttr + ' : ' + keyAttrs[keyAttr]);
											$("#id_" + key).attr(keyAttr, keyAttrs[keyAttr]);
										}
									}
								}
							}
						} else if (element == 'select') {
							// label and help_text
							//ximpia.console.log(keyAttrs);
							for (keyAttr in keyAttrs) {
								if (keyAttrs[keyAttr] != null && keyAttr != "type") {
									if (keyAttr == 'label' && keyAttrs.label != '') {
										$("label[for='" + 'id_' + key + "']").html(keyAttrs.label);
									} else if (keyAttr == 'help_text' && keyAttrs.help_text != '') {
										//ximpia.console.log('help_text : ' + keyAttrs.help_text);
										$("label[for='" + 'id_' + key + "'].info").attr('data-xp-title', keyAttrs.help_text);
									} else if (keyAttr == 'choices') {
										for (choiceIndex in keyAttrs.choices) {
											$("#id_" + key).append("<option value=\"" + keyAttrs.choices[choiceIndex][0] + "\">" + keyAttrs.choices[choiceIndex][1] + "</option>");
										}
									}
								}
							}
						}
					}
					//ximpia.console.log('id_variables : ' + $("#id_variables").html());
					//$("#id_sect_loading").fadeOut('fast');
					$("#" + _attr.priv.sectionId).css('visibility', 'visible');
					// Just call a method for the bindings of the page
					//var obj = ximpia.site.Signup();
					//obj.doProfessionalBind();
					_attr.priv.callback();
					//ximpia.console.log('invitationCode : ' + $("#id_invitationCode").attr('value'));
				}).error(function(jqXHR, textStatus, errorThrown) {
					//$("#id_sect_loading").fadeOut('fast');
					var html = "<div class=\"loadError\"><img src=\"" + ximpia.settings.SITE_MEDIA_URL + "images/blank.png\" class=\"warning\" style=\"float:left; padding: 5px;\" /><div>Oops, something did not work right!<br/> Sorry for the inconvenience. Please retry later!</div></div>";
					$("body").before(html);
				});
			},
			doSections : function() {
				// section
				$.metadata.setType("attr", "data-xp-fields");
				var objects = $("section[data-xp-class='cond']");
				for (var i = 0; i < objects.length; i++) {
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
				ximpia.console.log('doAction : ' + doAction);
			},
			doFade : function() {
				//ximpia.console.log('doFade()...');
				//$("#id_sect_loading").fadeOut('fast');
				//$("#" + "id_sect_signupUser").css('visibility', 'visible');
				//$(":hidden").removeClass('hidden');
				//$(".sectionComp").css('visibility', 'visible');
				//ximpia.console.log('.sectionComp: ' + $(".sectionComp"));
			},
			doFormPopupNoView : function(view) {
				ximpia.console.log('doFormPopupNoView...');
				ximpia.console.log(document.forms);
				var data = JSON.parse(sessionStorage.getItem('xpData-view-' + view));
				for (var i = 0; i < document.forms.length; i++) {
					var myForm = document.forms[i];
					var xpForm = 'xpData-view-' + view + '.' + myForm.id;
					//ximpia.console.log('xpForm: ' + xpForm);
					ximpia.common.PageAjax.doRender(xpForm);
					//_attr.priv.doRenders(xpForm);
				}
				$('.btBar').css('visibility', 'visible');
				ximpia.common.PageAjax.doFade();
				// Conditions
				// Post-Page : Page logic
				var oForm = ximpia.common.Form();
				oForm.doBindBubbles();
				//_attr.priv.callback(data);
				ximpia.console.log('end doFormPopupNoView()');
			},
			doFormPopup : function() {
				/**
				 *
				 */
				ximpia.console.log('doFormPopup...');
				$.getJSON(_attr.priv.path, function(data) {
					if (_attr.priv.verbose == true) {
						ximpia.console.log(data)
					}
					sessionStorage.setItem('xpData-view-' + _attr.priv.viewName, JSON.stringify(data));
					var xpForm = 'xpData' + '.' + _attr.priv.formId;
					items = JSON.parse(sessionStorage.getItem('xpData'));
					items['response'][_attr.priv.formId] = data;
					sessionStorage.setItem('xpData', JSON.stringify(items));
					_attr.priv.doRenders(xpForm);
					var oForm = ximpia.common.Form();
					oForm.doBindBubbles();
					ximpia.console.log('verbose: ' + _attr.priv.verbose);
					_attr.priv.callback(data);
				}).error(function(jqXHR, textStatus, errorThrown) {
					//$("#id_sect_loading").fadeOut('fast');
					var html = "<div class=\"loadError\"><img src=\"" + ximpia.settings.SITE_MEDIA_URL + "images/blank.png\" class=\"warning\" style=\"float:left; padding: 5px;\" /><div>Oops, something did not work right!<br/> Sorry for the inconvenience. Please retry later!</div></div>";
					$("body").before(html);
				});
			},
			renderCtx : function(data) {
				/**
				 * Render forms once context is passed as attribute (data)
				 */
				//ximpia.common.Browser.setXpDataViewSerial(viewName, data);
				ximpia.console.log(document.forms);
				ximpia.console.log('renderCtx :: forms length: ' + document.forms.length);
				// Consider only one form, since this is a server generated content
				var myForm = '';
				for (var i = 0; i < document.forms.length; i++) {
					ximpia.console.log('form: ' + document.forms[i].id);
					if (document.forms[i].id != 'form_header') {
						myForm = document.forms[i];
					}
				}
				ximpia.console.log('renderCtx :: myForm: ' + myForm);
				ximpia.console.log('renderCtx :: data...');
				ximpia.console.log(data);
				var dataObj = JSON.parse(data);
				var viewName = dataObj.response.view;
				ximpia.common.Browser.setXpDataViewSerial(viewName, data);
				ximpia.console.log('renderCtx :: dataObj...');
				ximpia.console.log(dataObj);
				var status = dataObj.status;
				var errorMsg = '';
				ximpia.console.log('renderCtx :: status: ' + status);
				if (status != 'ERROR') {
					var xpForm = 'xpData-view-' + viewName + '.' + myForm.id;
					ximpia.console.log('renderCtx :: xpForm: ' + xpForm);
					// Do menus
					responseMap = dataObj;
					ximpia.common.PageAjax.processMenus(responseMap);
					ximpia.common.timeOutCounter(function() {
						ximpia.common.PageAjax.positionBars();						
						ximpia.common.PageAjax.doRender(xpForm);
						ximpia.common.PageAjax.doFade();
						var oForm = ximpia.common.Form();
						oForm.doBindBubbles();
					});
				} else {
					errorMsg = dataObj.errors[0][1];
					//$("#id_sect_loading").fadeOut('fast');
					var html = "<div class=\"loadError\"><img src=\"" + ximpia.settings.SITE_MEDIA_URL + "images/blank.png\" class=\"warning\" style=\"float:left; padding: 5px;\" /><div>" + errorMsg + "</div></div>";
					$("body").before(html);
				}
			},
			doForm : function(obj, state) {
				/**
				 * Process forms for view request
				 */
				ximpia.console.log('PageAjax.doForm...');
				ximpia.console.log(obj);
				if (typeof(state) == 'undefined') {
					state = true;
				}
				ximpia.common.startBackendResponse('PageAjax.doForm');
				$.post(_attr.priv.path, obj, function(data) {
					ximpia.common.endBackendResponse('PageAjax.doForm');
					
					// Get responseMap
					var responseMap = eval(data);
					var viewName = responseMap['response']['view'];
					var app = responseMap['response']['app'];
					var tmplName = responseMap['response']['tmpl'][viewName];
					ximpia.console.log('PageAjax.doForm :: tmpl: ' + tmplName);
					ximpia.console.log('PageAjax.doForm :: view: ' + obj.view + ' viewNew: ' + responseMap['response']['view']);
					//if (responseMap['response']['view'] != _attr.priv.viewName) {
					// Get new view template, insert into DOM
					var tmplPath = ximpia.common.PageAjax.getTemplatePath({
						app : responseMap['response']['app'],
						name : tmplName,
						viewType : 'page'
					});
					ximpia.console.log('tmplPath: ' + tmplPath);
					ximpia.console.log('viewName: ' + viewName);
					$.get(tmplPath, function(dataTmpl) {
						ximpia.common.PageAjax.doTmplInject(dataTmpl);
						//$('#id_content').wrap('<form id="form_' + viewName + '" method="post" action="" />');
						// Do menus
						ximpia.common.PageAjax.processMenus(responseMap);
						//
						ximpia.common.PageAjax.doFormsRender({
							viewName : responseMap['response']['view'],
							data : data
						});
						//ximpia.common.PageAjax.positionBars();
						// Update session data into SessionStorage
						ximpia.common.PageAjax.processLogin(responseMap);
						$(".ui-tooltip").remove();
						// TODO: Place state logic in method
						ximpia.console.log('PageAjax.doForm :: window state info: ' + state);
						if (state == true) {
							var title = $(dataTmpl).filter('title').text();
							var appSlug = responseMap['response']['appSlug'];
							var viewSlug = responseMap['response']['viewSlug'];
							$('title').text(title);
							// params
							var location = '/' + appSlug + '/' + viewSlug + '/';
							if (obj.hasOwnProperty('params')) {
								var params = JSON.parse(obj.params);
								var paramList = Object.keys(params);
								if (paramList.length != 0) {
									for (var i=0; i<paramList.length; i++) {
										if (i == 0) {
											location += params[paramList[i]];
										} else {
											location += '/' + params[paramList[i]];
										}
										
									}
								}								
							}
							var stateData = {
												appSlug: appSlug,
												viewSlug: viewSlug,
												app: responseMap['response']['app'],
												view: responseMap['response']['view']
							}
							if (viewName != 'home') {
								window.history.pushState(stateData, title, location);
							} else {
								window.history.pushState(stateData, title, '/');
							}
						}
					}).error(function(jqXHR, textStatus, errorThrown) {
						ximpia.console.log('get html template ERROR!!!! : ' + textStatus + ' ' + errorThrown);
					});
				}, 'json').error(function(jqXHR, textStatus, errorThrown) {
					//$("#id_sect_loading").fadeOut('fast');
					var html = "<div class=\"loadError\"><img src=\"" + ximpia.settings.SITE_MEDIA_URL + "images/blank.png\" class=\"warning\" style=\"float:left; padding: 5px;\" /><div>Oops, something did not work right!<br/> Sorry for the inconvenience. Please retry later!</div></div>";
					$("body").before(html);
				});
			},
			getView : function(obj, state) {
				try {
					$('div.loadError').remove();
					ximpia.console.log('PageAjax.getView :: Path: ' + _attr.priv.path);
					ximpia.console.log('PageAjax.getView :: winType: ' + obj.winType);					
					if (obj.winType == 'popup') {
						ximpia.console.log('PageAjax.getView :: getView() :: Will open popup...');
						var obj = {
							isPopupReqView : true,
							view : obj.view,
							params : obj.params,
							app : obj.app
						};
						$('body').xpPopUp(obj).xpPopUp('create');
					} else {
						_attr.pub.doForm({
							view : obj.view,
							app : obj.app,
							params : obj.params
						}, state);
					}
				} catch (err) {
					ximpia.console.log('PageAjax.getView :: Exception catched in getting view');
					ximpia.console.log(err);
					//$("#id_sect_loading").fadeOut('fast');
					var html = "<div class=\"loadError\"><img src=\"" + ximpia.settings.SITE_MEDIA_URL + "images/blank.png\" class=\"warning\" style=\"float:left; padding: 5px;\" /><div>Oops, something did not work right!<br/> Sorry for the inconvenience. Please retry later!</div></div>";
					$("body").before(html);
				}
			},
			doAction : function(obj) {
				ximpia.console.log('PageAjax.doAction :: path: ' + _attr.priv.path);
				_attr.pub.doForm({
					app : obj.app,
					action : obj.action
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
	ximpia.console.log('doFade :: ');
	ximpia.console.log($.find("[data-xp-render='']"));
	$("#id_view_zone").fadeIn(250);
}
/**
 * Do fade out wait icon and show page
 */
ximpia.common.PageAjax.doFadeIn = function() {
	$("#id_sect_loading").css('left', $(".sectionComp").offset().left);
	$("#id_view_zone").fadeOut(250);
}
/**
 * Inject template into DOM
 * 
 * ** Attributes **
 * 
 * * ``dataTmpl``:String : Template from server
 * 
 */
ximpia.common.PageAjax.doTmplInject = (function(dataTmpl) {
	ximpia.console.log('PageAjax.doForm :: Got template...');
	ximpia.console.log(dataTmpl);
	ximpia.console.log($(dataTmpl));
	var contentHtml = $(dataTmpl).filter('div#id_view_zone').find('#id_content').html();
	$('#id_sectionTitle').html($(dataTmpl).filter('div#id_view_zone').find('#id_sectionTitle').html());
	$('#id_content').html(contentHtml);
	$('#id_sectionButton').html($(dataTmpl).filter('div#id_view_zone').find('#id_sectionButton').html());
	var viewAttrs = $(dataTmpl).filter('div#id_view_zone').find('#id_view')[0].attributes;
	ximpia.console.log(viewAttrs);
	for (var a=0; a<viewAttrs.length; a++) {
		$('#id_view').attr(viewAttrs[a].name, viewAttrs[a].value);
	}
})
/**
 * Get template path
 */
ximpia.common.PageAjax.getTemplatePath = function(obj) {
	var tmplType = '';
	if (obj.viewType == 'page' || obj.viewType == 'title') {
		tmplType = 'window';
	} else {
		tmplType = 'popup';
	}
	var path = ximpia.common.Path.getTemplate(obj.app, obj.name, tmplType);
	return path;
}
/*
 * Get template
 */
ximpia.common.PageAjax.getTemplate = function(obj) {
	var tmplType = '';
	if (obj.viewType == 'page' || obj.viewType == 'title') {
		tmplType = 'window';
	} else {
		tmplType = 'popup';
	}
	var path = ximpia.common.Path.getTemplate(obj.app, obj.name, tmplType);
	$.get(path, function(data) {
		return data;
	}).error(function(jqXHR, textStatus, errorThrown) {
		ximpia.console.log('get html template ERROR!!!! : ' + textStatus + ' ' + errorThrown);
	});
}
/*
 * Get template with function
 */
ximpia.common.PageAjax.getTmpl = function(obj, functionName) {
	var tmplType = '';
	if (obj.viewType == 'page' || obj.viewType == 'title') {
		tmplType = 'window';
	} else {
		tmplType = 'popup';
	}
	var path = ximpia.common.Path.getTemplate(obj.app, obj.name, tmplType);
	$.get(path, function(data) {
		functionName(data);
	}).error(function(jqXHR, textStatus, errorThrown) {
		ximpia.console.log('get html template ERROR!!!! : ' + textStatus + ' ' + errorThrown);
	});
}
/**
 * Process password strength
 */
ximpia.common.PageAjax.doShowPasswordStrength = (function(userId) {
	// Password Strength
	// TODO: Analyze a common way of associating a new variable to a input field, and influence click of a given button
	// TODO: Include validation of strength when clicking on signup button or buttons
	// TODO: Way to integrate settings into visual engine and define settings for password strength
	$('.passwordStrength').passStrengthener({
		userid : "#" + userId
		/*strengthCallback:function(score, strength) {
		 ximpia.console.log('strength : ' + strength)
		 if(strength == 'good' || strength == 'strong') {
		 $("#" + submitId).xpPageButton('enable', ximpia.common.Form().doSubmitButton);
		 } else {
		 $("#" + submitId).xpPageButton('disable');
		 }
		 }*/
	});
})
/**
 * Render content
 */
ximpia.common.PageAjax.doRender = function(xpForm) {
	ximpia.common.PageAjax.doRenderExceptFunctions(xpForm);
	var formId = xpForm.split('.')[1];
	// function.render
	$('#' + formId).find("[data-xp-type='function.render']").xpRenderExt('render', xpForm);
}
/*
 * 
 */
ximpia.common.PageAjax.doRenderExceptFunctions = function(xpForm) {
	ximpia.console.log('xpForm: ' + xpForm);
	var formId = xpForm.split('.')[1];
	//ximpia.console.log('text: ' + $('#' + formId).find("[data-xp-type='basic.text']"));
	$('body').xpHidden('addHidden', xpForm);
	// container
	$('#' + formId).find("[data-xp-type='container']").xpContainer('render', xpForm);
	// list.data
	$('#' + formId).find("[data-xp-type='list.data']").xpListData('render', xpForm);
	// Wait until containers and lists have rendered other components like images, fields, etc...
	ximpia.common.waitUntilListRenders(function() {
		// Paging More
		$('#' + formId).find("[data-xp-type='paging.more']").xpPagingMore('render', xpForm);
		// field.list
		$('#' + formId).find("[data-xp-type='field.list']").xpFieldList('render', xpForm);
		// basic.text
		$('#' + formId).find("[data-xp-type='field']").xpField('render', xpForm);
		// field.datetime
		$('#' + formId).find("[data-xp-type='field.datetime']").xpFieldDateTime('render', xpForm);
		// field.number
		$('#' + formId).find("[data-xp-type='field.number']").xpFieldNumber('render', xpForm);
		// select.plus
		$('#' + formId).find("[data-xp-type='select.plus']").xpSelectPlus('render', xpForm);
		// select
		$('#' + formId).find("[data-xp-type='select']").xpSelect('render', xpForm);
		// option
		$('#' + formId).find("[data-xp-type='option']").xpOption('render', xpForm);
		// check
		$('#' + formId).find("[data-xp-type='check']").xpCheck('render', xpForm);
		// field check
		$('#' + formId).find("[data-xp-type='field.check']").xpFieldCheck('render', xpForm);
		// textarea
		$('#' + formId).find("[data-xp-type='textarea']").xpTextArea('render', xpForm);
		// field.list
		$('#' + formId).find("input[data-xp-related='field.list']")
				.filter("input[data-xp-type='field']")
				.xpFieldList('keyPress', xpForm);
		// button
		$("[data-xp-type='button']").xpButton('render');
		// link
		$("[data-xp-type='link.popup']").xpLink('render');
		$("[data-xp-type='link.url']").xpLink('render');
		$("[data-xp-type='link.action']").xpLink('render');
		$("[data-xp-type='link.view']").xpLink('render');
		// Image
		$('#' + formId).find("[data-xp-type='image']").xpImage('render', xpForm);
		// TODO: Replace password strength dur to license problems with GPL
		ximpia.common.PageAjax.doShowPasswordStrength('id_username', 'id_password');
		// TODO: analyse the onSelect function
		// TODO: Integrate header search with jxSuggestList
		// TODO: Alternative for jsonSuggest due to license problems with GPL
		$("#id_header_search").jsonSuggest({
			url : '/jxSearchHeader',
			maxHeight : ximpia.settings.COMPLETE_MAX_HEIGHT,
			minCharacters : ximpia.settings.COMPLETE_MIN_CHARACTERS,
			onSelect : ximpia.common.Search.doClick
		});
		// Bind bubbles
		oform = ximpia.common.Form();
		oform.doBindBubbles();		
	});
}
/**
 * Do render of forms in a view
 * Options ( obj )
 * =======
 * data :
 * viewName :
 */
ximpia.common.PageAjax.doFormsRender = (function(obj) {
	ximpia.console.log(obj.data)
	ximpia.console.log('doFormsRender :: viewName: ' + obj.viewName);
	ximpia.common.Browser.setXpDataView(obj.viewName, obj.data);
	ximpia.console.log('doFormsRender :: forms length: ' + document.forms.length);
	ximpia.console.log(document.forms);
	ximpia.common.PageAjax.positionBars();
	for (var i = 0; i < document.forms.length; i++) {
		var myForm = document.forms[i];
		var xpForm = 'xpData-view-' + obj.viewName + '.' + myForm.id;
		ximpia.console.log('doFormsRender :: xpForm: ' + xpForm);
		//_attr.priv.doRenders(xpForm);
		ximpia.common.PageAjax.doRender(xpForm);
	}
	ximpia.common.timeOutCounter(function() {
		ximpia.common.PageAjax.doFade();
		// Conditions
		// Post-Page : Page logic
		var oForm = ximpia.common.Form();
		oForm.doBindBubbles();
		//ximpia.common.PageAjax.positionBars();
	});
});
/**
 * Position the button bars and content
 */
ximpia.common.PageAjax.positionBars = (function(obj) {
	ximpia.console.log('positionBars :: ');
	// Place bars and content
	// Position title bar and content
	if ($('#id_titleBar').hasOwnProperty('length')) {
		//
		var height = $('#id_titleBar').height();
		/*if ($('#id_titleBar').offset().top == $('#id_content').offset().top) {
			alert('offset top variable...');
			$('#id_content').offset({
				top : height + $('#id_content').offset().top + 4
			});
		}*/
		//$('#id_content').css('border-top-left-radius', '0px');
		//$('#id_content').css('border-top-right-radius', '0px');
		//$('#id_content').css('border-top', '0px');
		//padding-top: 30px sectionComp
		//$('.sectionComp').css('padding-top', '25px');
		$('#id_content').css('padding-top', '35px');
		//ximpia.console.log('********** paddong-top: ' + $('.sectionComp').css('padding-top'));
		//$('.sectionComp').css('padding-top', parseInt($('.sectionComp').css('padding-top'))+ 25 + 'px');
		//$('header').css('border-bottom-right-radius', '0px');
		//$('header').css('border-bottom-left-radius', '0px');
		$('#id_titleBar').css('width', parseInt($('#id_content').css('width')) - 5 + 'px');
		$('#id_titleBar').css('visibility', 'visible');
		$('#id_sectionTitle').css('visibility', 'visible');
	}
	// position page button bar
	if ($('#id_pageButton').hasOwnProperty('length')) {
		var height = $('#id_content').height();
		var winHeight = $(window).height();
		ximpia.console.log('positionBars :: height:' + height + ' winHeight:' + winHeight);
		if (height > winHeight) {
			// Place bar at bottom
			$('#id_sectionButton').offset({
				top : $(window).height() - $('#id_pageButton').height()
			});
		} else {
			// Place buttons at end of content dic layer
			//$('#id_sectionButton').offset({top: height+$('#id_content').offset().top-$('#id_pageButton').height()});
			var html = $('#id_sectionButton').html();
			ximpia.console.log('********************** buttons html:  ' + html);
			$('.sectionComp').append(html);
			$('#id_sectionButton').html('');
			//$('#id_pageButton').css('top', '15px');
			$('#id_pageButton').css('top', '1px');
			//margin-bottom: 0px; left: 0px
		}
		if (( typeof obj != 'undefined' && !obj.hasOwnProperty('skipVisibility')) || typeof obj == 'undefined') {
			$('#id_pageButton').css('visibility', 'visible');
		}
		$('#id_pageButton').offset({
			left : $('#id_content').offset().left
		});
		$('#id_pageButton').css('width', parseInt($('.sectionComp').css('width')) - 3 + 'px');
		//$('#id_pageButton').css('width', $('#id_content').css('width'));
	}
});
/**
 * Get view
 */
ximpia.common.PageAjax.getView = (function(obj, functionName) {
	ximpia.console.log('getView:: obj : ');
	ximpia.console.log(obj);
	$.post(ximpia.common.Path.getBusiness(), obj, function(data) {
		// Get responseMap
		var responseMap = eval(data);
		functionName(responseMap);
	}, 'json').error(function(jqXHR, textStatus, errorThrown) {
		//$("#id_sect_loading").fadeOut('fast');
		var html = "<div class=\"loadError\"><img src=\"" + ximpia.settings.SITE_MEDIA_URL + "images/blank.png\" class=\"warning\" style=\"float:left; padding: 5px;\" /><div>Oops, something did not work right!<br/> Sorry for the inconvenience. Please retry later!</div></div>";
		$("body").before(html);
	});
});
/**
 * Process menus
 */
ximpia.common.PageAjax.processMenus = (function(responseMap) {
	ximpia.console.log('menus...');
	var menuObj = responseMap['response']['menus'];
	var menuSessObj = ximpia.common.Browser.getObject('menus');
	if (menuSessObj == null) {
		menuSessObj = {};
	}
	if (menuObj.hasOwnProperty('sys')) {
		menuSessObj['sys'] = menuObj['sys']
	}
	if (menuObj.hasOwnProperty('main')) {
		menuSessObj['main'] = menuObj['main']
	}
	if (menuObj.hasOwnProperty('service')) {
		menuSessObj['service'] = menuObj['service']
	}
	menuSessObj['view'] = menuObj['view']
	/*if (responseMap['response']['isLogin'] == false && menuSessObj.hasOwnProperty('sys')) {
		delete menuSessObj['sys']
	}*/
	ximpia.common.Browser.setObject('menus', menuSessObj);
	$("[data-xp-type='icon']").xpIcon('renderMenu');
});
/**
 * Process login and session information
 */
ximpia.common.PageAjax.processLogin = (function(responseMap) {
	if (responseMap['response']['isLogin'] == true) {
		ximpia.common.Browser.setObject('session', responseMap['response']['session']);
	}
	// Process login and logout layout changes
	// id_header_extra is allways displayed. Temporaly, the search field is hidden in public site
	// 01/10/2013 - jalegre - search box (id_header_search) is allways displayed. In future release, ability to configure by settings
	/*if (responseMap['response']['view'] == 'homeLogin') {
		$('#id_header_search').css('display', 'block');
	} else if (responseMap['response']['view'] == 'logout') {
		$('#id_header_search').css('display', 'none');
	}*/
});

ximpia.common.Search = {};
/**
 * Click on the search result box ??? Should go to plugin???
 */
ximpia.common.Search.doClick = (function(item) {
	ximpia.console.log('Search.doClick :: I clicked on the search result...');
	ximpia.console.log(item);
	attrs = item.extra;
	ximpia.console.log('Search.doClick :: attrs...');
	ximpia.console.log(attrs);
	if (attrs.action != '') {
		// do action
		ximpia.console.log('Search.doClick :: action!!!!');
		var pageJx = ximpia.common.PageAjax();
		pageJx.doAction({
			action : attrs.action
		});
	} else if (attrs.view != '') {
		// show view
		// popupNoView
		// popupView
		// view
		ximpia.console.log('Search.doClick :: view!!!!');
		ximpia.console.log('Search.doClick :: view: ' + attrs.view);
		ximpia.common.PageAjax.doFadeIn();
		var pageJx = ximpia.common.PageAjax();
		pageJx.getView({
			view : attrs.view,
			params : JSON.stringify(attrs.params)
		});
	}
});

ximpia.common.GoogleMaps = function() {
	var _attr = {
		priv : {},
		pub : {
			init : function() {
			},
			insertCityCountry : function(xpForm, idCityList, idCountryList) {
				ximpia.console.log('GoogleMaps :: insertCityCountry...');
				var data = {};
				if (navigator.geolocation) {
					ximpia.console.log('1');
					navigator.geolocation.getCurrentPosition(function(position) {
						ximpia.console.log('2');
						var loc = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);
						ximpia.console.log('2.1');
						geocoder = new google.maps.Geocoder();
						ximpia.console.log('2.2');
						geocoder.geocode({
							'latLng' : loc
						}, function(results, status) {
							ximpia.console.log('3');
							ximpia.console.log(status);
							ximpia.console.log(results);
							var city = "";
							var countryCode = "";
							var list = results[0].address_components;
							for (var i = 0; i < list.length; i++) {
								var fields = list[i].types;
								for (var j = 0; j < fields.length; j++) {
									if (fields[j] == "locality") {
										city = list[i].long_name;
										ximpia.console.log('city: ' + city);
										for (var k = 0; k < idCityList.length; k++) {
											$("#" + idCityList[k]).attr('value', city);
										}
										//$("#" + idCity).attr('value', city);
									} else if (fields[j] == "country") {
										countryCode = list[i].short_name.toLowerCase();
										ximpia.console.log('country: ' + countryCode);
										for (var k = 0; k < idCountryList.length; k++) {
											$("#id_country_comp").xpListSelect('setValue', xpForm, countryCode);
										}
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
		priv : {
			id : null,
			inputData : null,
			dataDictList : null
		},
		pub : {
			/**
			 * Constructor
			 */
			init : (function(id) {
				_attr.priv.id = id
				_attr.priv.inputData = $("#" + this.id).attr('value');
				_attr.priv.dataDictList = JSON.parse(_attr.priv.inputData);
			}),
			/**
			 * Get list of data
			 */
			getDataDictList : function() {
				return _attr.priv.dataDictList
			},
			/**
			 * Get data
			 */
			getData : function() {
				return _attr.priv.dataDictList[1]
			},
			/**
			 * Get configuration
			 */
			getConfig : function() {
				return _attr.priv.dataDictList[0]
			},
			/**
			 * Get token
			 */
			getToken : function() {
				return _attr.priv.dataDictList[1].token
			},
			/**
			 * Set token
			 */
			setToken : function(token) {
				_attr.priv.dataDictList[1].token = token;
			}
		}
	}
	return _attr.pub;
}

/*
 * Generic component data object
 * 
 * Deals with containers adding fields and utility methods to check on items, add items, etc...
 * 
 * ** Methods **
 * 
 * * ``getDataDictList``
 * * ``getDataList``
 * * ``setDataList``
 * * ``addDataEnd``
 * * ``writeData``
 * * ``getSize``
 * * ``hasElement``
 * * ``hasElementByName``
 * * ``deleteData``
 * * ``getConfigDict``
 * 
 */
ximpia.visual.GenericComponentData = function() {
	var _attr = {
		priv : {
			id : null,
			inputData : null,
			dataDictList : null
		},
		pub : {
			/**
			 * Constructor
			 */
			init : function(id) {
				_attr.priv.id = id
				_attr.priv.inputData = $("#" + id).attr('value');
				_attr.priv.dataDictList = JSON.parse(_attr.priv.inputData);
			},
			/**
			 *
			 */
			getDataDictList : function() {
				return _attr.priv.dataDictList;
			},
			/**
			 *
			 */
			getDataList : function() {
				return _attr.priv.dataDictList[1].data;
			},
			/**
			 *
			 */
			getDataListPaging : function(page, numberPages) {
				var size = _attr.pub.getSize();
				// TODO
			},
			/**
			 *
			 */
			setDataList : function(array) {
				_attr.priv.dataDictList[1].data = array;
			},
			/**
			 *
			 */
			addDataEnd : function(obj) {
				var size = _attr.priv.dataDictList[1].data.push(obj);
				$("#" + _attr.priv.id).attr('value', JSON.stringify(_attr.priv.dataDictList));
			},
			/**
			 *
			 */
			writeData : function(obj, i) {
				_attr.priv.dataDictList[1].data[i] = obj;
				$("#" + _attr.priv.id).attr('value', JSON.stringify(_attr.priv.dataDictList));
			},
			/**
			 *
			 */
			getSize : function() {
				return _attr.priv.dataDictList[1].data.length;
			},
			/**
			 * Object has element by text?
			 */
			hasElement : function(searchText) {
				var array = _attr.pub.getDataList();
				ximpia.console.log('array');
				ximpia.console.log(array);
				var hasElement = false;
				for (var i = 0; i < array.length; i++) {
					if (array[i].text == searchText) {
						hasElement = true;
					}
				}
				return hasElement;
			},
			/**
			 * Object has element by name?
			 */
			hasElementByName : function(searchText) {
				var array = _attr.priv.getDataList();
				var hasElement = false;
				for (var i = 0; i < array.length; i++) {
					if (array[i].name == searchText) {
						hasElement = true;
					}
				}
				return hasElement;
			},
			/**
			 * Delete data from object
			 */
			deleteData : function(i) {
				var newArray = [];
				var array = _attr.pub.getDataList();
				for (var j = 0; j < array.length; j++) {
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
			getConfigDict : function() {
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
	var idElement = idElementDel.replace('_del', '');
	var list = idElement.split('_');
	var idContainer = 'id_' + list[1];
	var idContainerData = idContainer + '_data';
	var index = list[list.length - 1];
	$('#' + idElement).remove();
	var obj = new ximpia.visual.GenericComponentData();
	obj.init(idContainerData);
	obj.deleteData(index);
	/*if (oArg.callBack) {
	 oArg.callBack(oArg);
	 }*/
}

ximpia.site.Signup = function() {
	var _attr = {
		priv : {
			/**
			 * Show password strength indicator. Password leads to a strength variable. Analyze if this behavior is common
			 * and make common behavior. One way would be to have a data-xp-obj variable strength and be part of validation, showing
			 * the message of nor validating.
			 */
			doShowPasswordStrength : (function(userId, passwordId, submitId) {
				// Password Strength
				// TODO: Analyze a common way of associating a new variable to a input field, and influence click of a given button
				$("#" + passwordId).passStrengthener({
					userid : "#" + userId,
					strengthCallback : function(score, strength) {
						ximpia.console.log('strength : ' + strength)
						if (strength == 'good' || strength == 'strong') {
							$("#" + submitId).xpPageButton('enable', ximpia.common.Form().doSubmitButton);
						} else {
							$("#" + submitId).xpPageButton('disable');
						}
					}
				});
			})
		},
		pub : {
			doProfessionalBind : (function(data) {
				ximpia.console.log('doProfessionalBind()...');
				// Pre-page : Binding ajax data to form
				var formData = data.response["form_signup"];
				sessionStorage.setItem('xpForm', JSON.stringify(formData));
				sessionStorage.setItem('form_signup', JSON.stringify(formData));
				$("[data-xp-type='list.field']").xpListField('render');
				$("[data-xp-type='basic.text']").xpInput('renderField');
				$("#id_variables").xpInput('addHidden');
				$("[data-xp-type='list.select']").xpListSelect('render');
				$("[data-xp-type='text.autocomplete']").xpInput('renderFieldAutoComplete');
				$("[data-xp-type='basic.textarea']").xpTextArea('render');
				$("input[data-xp-related='list.field']").filter("input[data-xp-type='basic.text']").xpListField('bindKeyPress');
				$(".scroll").jScrollPane({
					showArrows : true,
					verticalArrowPositions : 'after',
					arrowButtonSpeed : 90,
					animateScroll : false,
					keyboardSpeed : 90,
					animateDuration : 50,
					arrowRepeatFreq : 0
				});
				$(".scroll").each(function() {
					if ($(this).find(".jspArrow").length > 0) {
						$(this).find('.jspTrack').addClass("jspTrackPag");
					}
				});
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
			doOrganizationBind : (function(data) {
				ximpia.console.log('doOrganizationBind()...');
				var formData = data.response["form_signupOrg"];
				sessionStorage.setItem('xpForm', JSON.stringify(formData));
				sessionStorage.setItem('form_signupOrg', JSON.stringify(formData));
				$("[data-xp-type='list.field']").xpListField('render');
				$("[data-xp-type='basic.text']").xpInput('renderField');
				$("#id_variables").xpInput('addHidden');
				$("[data-xp-type='list.select']").xpListSelect('render');
				$("[data-xp-type='text.autocomplete']").xpInput('renderFieldAutoComplete');
				// Binds related objects: Simple objects events binded to compound objects
				// We do not bind enter event in autocomplete becaouse not compatible with enter event of complete list
				$("[data-xp-type='basic.textarea']").xpTextArea('render');
				$("input[data-xp-related='list.field']").filter("input[data-xp-type='basic.text']").xpListField('bindKeyPress');
				$(".scroll").jScrollPane({
					showArrows : true,
					verticalArrowPositions : 'after',
					arrowButtonSpeed : 90,
					animateScroll : false,
					keyboardSpeed : 90,
					animateDuration : 50,
					arrowRepeatFreq : 0
				});
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

ximpia.site.Login = {};
/*
 * Login Form
 */
ximpia.site.Login.showLogin = (function() {
	ximpia.console.log('Show login...');
});
/*
 * Do login : After login button has been clicked
 */
ximpia.site.Login.doLogin = (function() {
	ximpia.console.log('Do login...');
});
