
  function getValue(id, key) {
    var array = eval($("#" + id).attr('value'));
    var value = '';
    for (var i=0; i<array.length; i++) {
        var list = array[i];
        if (list[0] == key) {
            value = list[1];
        }
    }
    return value;
  }
  function hasKey(id, key) {
    
  }

	/**
	 * Show password strength indicator. Password leads to a strength variable. Analyze if this behavior is common
	 * and make common behavior. One way would be to have a data-xp-obj variable strength and be part of validation, showing
	 * the message of nor validating.
	 */
	function doShowPasswordStrength(userId, passwordId, submitId) {
        	// Password Strength
        	// TODO: Analyze a common way of associating a new variable to a input field, and influence click of a given button
        	$("#" + passwordId).passStrengthener({
			userid: "#" + userId,
			strengthCallback:function(score, strength) {                       
				if(strength == 'good' || strength == 'strong') {
					$("#" + submitId).xpPageButton('enable', doBindSubmitButton);
				} else {
					$("#" + submitId).xpPageButton('disable');
				}
			}
		});         
	}
    
	/**
	* callback method for submit signup click.
	*/
	function doBindSubmitButton() {
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
	}

	/**        
	 * Bind signup submit button. Binds the click event of button, shows waiting icon, sends data through AJAX
	 */
    function doBindSubmitForm(formId, callbackFunction) {
    	$("a.button[data-xp-js='submit']").click(doBindSubmitButton);
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
                                showPopUp('id_msgSubmit_Form1');
                            } else {
                                callbackFunction();
                            }                       
                        } else {
                            $("#" + idImg).xpLoadingSmallIcon('error');
                            $("#" + idTxt).text($("#id_ERR_GEN_VALIDATION").attr('value'));
                            // Integrate showMessage, popUp, etc...
                            var list = responseMap['errors'];
                            message = '<ul>'
                            for (var i=0; i<list.length; i++) {
                                var errorId = list[i][0];
                                var errorMessage = list[i][1];
                                //alert(errorId);
                                $("#" + errorId).removeClass("valid");
                                $("#" + errorId).addClass("error");
                                message = message + '<li>' + errorMessage + '</li>';
                            }
                            message = message + '</ul>';
                            // Show error Message in pop up
                            showPopUp({
                                title: 'Errors Found',
                                message: message,
                            });
                        }
                    },
                    error: function (data, status, e) {
                        alert(data + ' ' + status + ' ' + e);
                        $("#" + idImg).xpLoadingSmallIcon('errorWithPopUp');
                        showPopUp({
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
    }
    
    function showRemoteError() {
        showPopUp('MessageERROR');
    }
        
    //function showMessage(sTitle, sMessage, sButtons, sEffectIn, sEffectOut, bFadeBackground, iWidth, iHeight, functionShow) {
    function showMessage(messageOptions) {
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
        bFadeOut = checkFadeOut();
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
            $("#Wrapper").fadeTo("fast", 0.60);
        }
        if (functionShow) {
            functionShow($(this));
        }
    }

    function clickMsgOk(bFadeBackground, functionName) {
        bFadeOut = checkFadeOut();
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
    }

    // Pop Up Message. It is used for Ajax actions, like OK Message, Error messages, etc...
    function showPopUp(key) {
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
        bIE = checkIE();
        if (bIE) {
            bFadeOut = false;
        }
        // This is to prevent fadeouts in popups since Internet Explorer does not show frame border
        sFadeOut = '';
        var closeValue = getValue('id_buttonConstants', 'close');
        showMessage({
            title: sTitle,
            message: sMessage,
            buttons: 'MsgOk:' + closeValue,
            effectIn: 'fadeIn,1000',
            effectOut: sFadeOut,
            fadeBackground: bFadeOut
        });
        //showMessage(sTitle, sMessage, 'MsgOk:OK', 'fadeIn,1000', sFadeOut, bFadeOut);
        if (sFadeOut == '') {
            $("#MsgOk").click(function() {clickMsgOk(bFadeOut, functionName)});
        }
        if (sUrl) {
            if (sUrl != '') {
                $("#MsgOk").click(function() {
                    window.location = sUrl;
                });
            }
        }
   }
   
    function checkFadeOut() {
        if (jQuery.browser.msie) {
            bCheck = false;
        }
        else {
            bCheck = true;
        }
        return bCheck
    }
    
    function checkIE6() {
        if (jQuery.browser.msie && jQuery.browser.version.substr(0,3)=='6.0') {
            bIE6 = true;
        }
        else {
            bIE6 = false;
        }
        return bIE6;
    }

    function checkIE() {
        if (jQuery.browser.msie) {
            bIE = true;
        }
        else {
            bIE = false;
        }
        return bIE
    }
    
    function doReloadCaptcha() {
        $("#id_ImgRefreshCaptcha").click(function() {
            // reload captcha
            $.get('/reloadCaptcha');
            // Show image
            var kk = Math.random();
            $("#id_ImgCaptcha").attr('src', '/captcha/captcha.png?code=' + kk);
        });
    }
    
    function doBindBubbles() {    	
        var bubbleOptions = {position : 'left', 
                        innerHtmlStyle: {color:'black', 'text-align':'left', 'font-size': '10pt', 'width': '200px', 'line-height' : '1.2em'},
                        themeName:  'blue',
                        themePath:  '/site_media/images/jquerybubblepopup-theme',
			alwaysVisible: true,
			closingDelay: 0,
        };
        $('label.info').CreateBubblePopup(bubbleOptions);
        $('label.info').mouseover(function() {
		$(this).css('cursor', 'help');
		$.metadata.setType("attr", "data-xp-obj");
		var data = $(this).metadata();
		if (data.msg) {
			$(this).SetBubblePopupInnerHtml(data.msg, true);
		}
        });
        /*$('input.Small').focus(function() {
            var name = $(this).attr('name');
            var textId = 'id_msg_' + name;
            var bubleText = $('#' + textId).attr('value');
            $('#' + 'id_img_' + name).SetBubblePopupInnerHtml(bubleText, true);
            $('#' + 'id_img_' + name).ShowBubblePopup();
        });
        $('input.Small').blur(function() {
            var name = $(this).attr('name');
            $('#' + 'id_img_' + name).HideBubblePopup();
        });*/       
    }

    // ***********************************************************************
    //     VISUAL COMPONENTS DATA
    // **********************************************************************

    // SocialNetworkIconData visual component data methods  
    function SocialNetworkIconData(id) {
        this.id = id;
        var inputData = $("#" + this.id).attr('value');
        this.dataDictList = JSON.parse(inputData);
        this.getDataDictList = function() {
            return this.dataDictList
        }
        this.getData = function() {
            return this.dataDictList[1]
        }
        this.getConfig = function() {
            return this.dataDictList[0]
        }
        this.getToken = function() {
            return this.dataDictList[1].token
        }
        this.setToken = function(token) {
            this.dataDictList[1].token = token;
            $("#" + this.id).attr('value',JSON.stringify(dataDictList))
        }
    }
    
    // GenericComponentData
    function GenericComponentData(id) {
        this.id = id;
        var inputData = $("#" + this.id).attr('value');
        this.dataDictList = JSON.parse(inputData);
        this.getDataDictList = function() {
            return this.dataDictList
        }
        this.getDataList = function() {
            return this.dataDictList[1].data;
        }
        this.getDataListPaging = function(page, numberPages) {
            var size = this.getSize();
            // TODO
        }
        this.setDataList = function(array) {
            this.dataDictList[1].data = array;
        }
        this.addDataEnd = function(obj) {
            var size = this.dataDictList[1].data.push(obj);
            $("#" + this.id).attr('value', JSON.stringify(this.dataDictList));
        }
        this.writeData = function(obj, i) {
            this.dataDictList[1].data[i] = obj;
            $("#" + this.id).attr('value', JSON.stringify(this.dataDictList));
        }
        this.getSize = function() {
            return this.dataDictList[1].data.length;
        }
        this.hasElement = function(searchText) {
            var array = this.getDataList();
            var hasElement = false;
            for (var i = 0; i< array.length; i++) {
                if (array[i].text == searchText) {
                    hasElement = true;
                }
            }
            return hasElement;
        }
        this.hasElementByName = function(searchText) {
            var array = this.getDataList();
            var hasElement = false;
            for (var i = 0; i< array.length; i++) {
                if (array[i].name == searchText) {
                    hasElement = true;
                }
            }
            return hasElement;
        }
        this.deleteData = function(i) {
            var newArray = new Array();
            var array = this.getDataList();
            for (var j=0; j<array.length; j++) {
                if (i != j) {
                    newArray.push(array[j]);
                }
            }
            this.setDataList(newArray);
            $("#" + this.id).attr('value', JSON.stringify(this.dataDictList));
        }
        this.getConfigDict = function() {
            return this.dataDictList[0];
        }
    }

    function fadeIcons() {
        $(".Icon").mouseover(function() {
            $(this).fadeTo("fast", 0.70);
        });
        $(".Icon").mouseout(function() {
            $(this).fadeTo("fast", 1.00);
        });
    }

    // Delete element from list using GenericComponentData
    function deleteFromList(element, oArg) {
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

    function setAjaxSuggestView() {
        $('#id_formAjax').attr('action', '/jxSuggestList');
    }

    function setAjaxView() {
        $('#id_formAjax').attr('action', '/jxJSON');
    }
    
    // Create new ajax object
    function newAjaxObject() {
        var oArg = new Object();
        oArg.jsonDataList = new Array();
        return oArg;
    }
    
    // Create new ajax request
    function newAjaxRequest( oArg, method, argsTuple, argsDict ) {
        var list = new Array();
        list[0] = method;
        list[1] = argsTuple;
        list[2] = argsDict;
        var index = oArg.jsonDataList.push(list);
        $('#id_formAjax_jsonData').attr('value', JSON.stringify(oArg));
    }

    // Send Ajax JSON Request   
    function sendAjaxJSONRequest() {
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
    }
