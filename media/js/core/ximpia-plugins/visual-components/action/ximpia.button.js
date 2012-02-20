/*
 * Ximpia Visual Component 
 * Button
 *
 */

(function($) {	

	$.fn.xpObjButton = function( method ) {  

        // Settings		
        var settings = {
        	classButton: "button",
        	classButtonColor: "buttonBlue"
        };
        var createPageMsgBar = function(obj) {
        	$("#id_pageButton").xpObjButton('createPageMsgBar');
        	$("#id_btPageMsg").css('top', $("#" + obj.element.id).offset().top-$("#" + obj.element.id).height()-10);
        };
        var getFormAttrs = function(formId) {
        	$.metadata.setType("attr", "data-xp");
        	var attrs = $("#" + formId).metadata();
        	return attrs
        };
        var doPageActionMsg = function(obj) {
        	console.log('doPageActionMsg...');
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
        		$("#" + obj.form).attr('action', ximpia.common.Path.getBusiness());
        		$("#id_bsClass").val(attrs.className);
        		console.log('form :: button method : ' + obj.method)
        		$("#id_method").val(obj.method);
        		$("#" + obj.form).submit();
        	} else {
			createPageMsgBar(obj);
			$("#id_btPageMsg_img").xpLoadingSmallIcon('error');
			$("#id_btPageMsg_text").text($("#id_ERR_GEN_VALIDATION").attr('value'));
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
			var oForm = ximpia.common.Form();
			for (var i=0; i<$(this).length; i++) {
				var element = $(this)[i];
				var idButton = $(element).attr('id').split('_comp')[0];
				$.metadata.setType("attr", "data-xp");
				var attrs = $(element).metadata();
				var sStyle = "float: left; margin-top: 3px";
				if (attrs.hasOwnProperty('align')) {
					sStyle = "float: " + attrs.align + "; margin-top: 3px";
				}
				var dataXp = "{form: '" + attrs.form + "', type: '" + attrs.type + "', method: '" + attrs.method + "', callback: '" + attrs.callback + "'}";
				console.log('form :: dataXp : ' + dataXp);
				var htmlContent = "<div style=\"" + sStyle + "\">"; 
				htmlContent += "<a id=\"" + idButton + "\" href=\"#\" class=\"button buttonBlue\" data-xp=\"" + dataXp + "\" onclick=\"return false;\"  >";
				htmlContent += "<span>" + attrs.text + "</span></a>";
				htmlContent += "</div>";
				$(element).html(htmlContent);
				$("#" + idButton).hover(function() {
					$("#" + idButton).addClass(settings.classButton +  '-hover');
					$("#" + idButton).addClass(settings.classButtonColor +  '-hover');
				}, function() {		
					$("#" + idButton).removeClass(settings.classButton +  '-hover');
					$("#" + idButton).removeClass(settings.classButtonColor +  '-hover');
				});
				$("#" + idButton).mousedown(function() {
					$("#" + idButton).addClass(settings.classButton +  '-active');
					$("#" + idButton).addClass(settings.classButtonColor +  '-active');
				}).mouseup(function(){
					$("#" + idButton).removeClass(settings.classButton +  '-active');
					$("#" + idButton).removeClass(settings.classButtonColor +  '-active');
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
				oForm.bindAction({attrs: attrs, callback: callback, idActionComp: idButton});
			}
		},
		click: function() {
			var element = $(this)[0];
			$.metadata.setType("attr", "data-xp");
			var attrs = $(element).metadata();
			attrs.element = element;
			var buttonType = attrs.type;
			console.log('buttonType: ' + buttonType);
			if (buttonType == 'pageActionMsg') {
				doPageActionMsg(attrs);
			}
		},
		disable: function() {
	   		$(this).addClass(settings.classButtonColor +  '-disabled');
	   		$(this).css('cursor', 'default');
	   		$(this).unbind('mouseenter mouseleave click mousedown mouseup');
		},
		enable: function() {
		},
		createPageMsgBar: function() {
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
		destroyPageMsgBar: function() {
			$("#id_btPageMsg").remove();
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
