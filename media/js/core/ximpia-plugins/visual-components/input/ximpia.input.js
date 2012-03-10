/*
 * Ximpia Visual Component Input: Text, Password, etc...
 *
 */

(function($) {	

	$.fn.xpObjInput = function( method ) {  

        // Settings		
        var settings = {
        	excudeListInput: ['type','id','element','help_text','label','left'],
        	excudeListInputSug: ['type','id','element','help_text','label','left'],
        	excludeListLabel: ['type','id','element'],
        	excludeList: ['info','type','left'],
        	reRender: false
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
		renderField: function(xpForm) {
			var data = ximpia.common.Browser.getFormDataFromSession(xpForm);
			for (var i=0; i<$(this).length; i++) {
				//console.log($(this)[i]);
				var element = $(this)[i]; 
				var idInput = $(element).attr('id').split('_comp')[0];
				var doRender = ximpia.common.Form.doRender(element, settings.reRender);
				if (doRender == true) {
					var nameInput = idInput.split('id_')[1];
					$.metadata.setType("attr", "data-xp");
					var attrs = $(element).metadata();
					//console.log('input attrs: ' + idInput);
					//console.log(attrs);
					var relatedId = $(element).attr('data-xp-related');
					var elementType = $(element).attr('data-xp-type');
					var dataAttrs = data[nameInput];
					var type = 'text';
					if (attrs.hasOwnProperty('type')) {
						type = attrs.type;
					}
					// id, name, type
					var htmlContent = "";
					if (attrs.hasOwnProperty('left')) {
						htmlContent = "<div style=\"width: " + attrs['left'] + "px; float: left\"><label for=\"" + idInput + "\"></label>:</div> <input id=\"" + idInput + "\" type=\"" + type + "\" name=\"" + nameInput + "\" value=\"\" />";
					} else {
						htmlContent = "<label for=\"" + idInput + "\"></label>: <input id=\"" + idInput + "\" type=\"" + type + "\" name=\"" + nameInput + "\" value=\"\" />";
					}
					$(element).html(htmlContent);
					$(element).attr('data-xp-render', JSON.stringify(true));
					// Input
					for (attr in dataAttrs) {
						var exists = ximpia.common.ArrayUtil.hasKey(settings.excudeListInput, attr);
						if (exists == false) {
							$("#" + idInput).attr(attr, dataAttrs[attr]);
						}					
					}
					for (attr in attrs) {
						var exists = ximpia.common.ArrayUtil.hasKey(settings.excludeList, attr);
						if (exists == false) {
							$("#" + idInput).attr(attr, attrs[attr]);
						}					
					}
					if (typeof relatedId != 'undefined') {
						$("#" + idInput).attr('data-xp-related', relatedId);
					}
					if (typeof elementType != 'undefined') {
						$("#" + idInput).attr('data-xp-type', elementType);
					}
					//console.log($("#" + idInput));
					// Label
					//console.log('dataAttrs');
					//console.log(dataAttrs);
					if (typeof dataAttrs != 'undefined' && dataAttrs.hasOwnProperty('label')) {
						$("label[for=\"" + idInput + "\"]").text(dataAttrs['label']);
						if (attrs.info == true) {
							$("label[for=\"" + idInput + "\"]").addClass("info");
							// help_text
							if (dataAttrs.hasOwnProperty('help_text')) {
								$("label[for=\"" + idInput + "\"]").attr('data-xp-title', dataAttrs['help_text']);
							}
						}
					}
				}
			}
		},
		renderFieldAutoComplete: function(xpForm) {
			var data = ximpia.common.Browser.getFormDataFromSession(xpForm);
			//var data = JSON.parse(sessionStorage.getItem("xpForm"));
			console.log('renderTextChoice...');
			for (var i=0; i<$(this).length; i++) {
				//console.log($(this)[i]);
				var element = $(this)[i]; 
				var idInput = $(element).attr('id').split('_comp')[0];
				var nameInput = idInput.split('id_')[1];
				var doRender = ximpia.common.Form.doRender(element, settings.reRender);
				if (doRender == true) {
					$.metadata.setType("attr", "data-xp");
					var attrs = $(element).metadata();
					//console.log('input attrs: ' + idInput);
					//console.log(attrs);
					/*console.log('element...');
					console.log(element);*/
					var relatedId = $(element).attr('data-xp-related');
					var elementType = $(element).attr('data-xp-type');
					var dataAttrs = data[nameInput];
					console.log(dataAttrs);
					var sugAttrs = {};
					var type = 'text';
					if (attrs.hasOwnProperty('type')) {
						type = attrs.type;
					}
					//console.log('type : ' + type);
					var htmlContent = "";
					if (attrs.hasOwnProperty('left')) {
						htmlContent = "<div style=\"width: " + attrs['left'] + "px; float: left\"><label for=\"" + idInput + "\"></label>:</div> <input id=\"" + idInput + "\" type=\"" + type + "\" name=\"" + nameInput + "\" value=\"\" />";
					} else {
						htmlContent = "<label for=\"" + idInput + "\"></label>: <input id=\"" + idInput + "\" type=\"" + type + "\" name=\"" + nameInput + "\" value=\"\" />";
					}
					$(element).html(htmlContent);
					$(element).attr('data-xp-render', JSON.stringify(true));
					// Input
					for (attr in dataAttrs) {
						//console.log(attr);
						var exists = ximpia.common.ArrayUtil.hasKey(settings.excudeListInputSug, attr);
						//console.log('attr : ' + attr + ' ' + typeof dataAttrs[attr]);
						if (exists == false) {
							if (typeof dataAttrs[attr] == 'object') {
								$("#" + idInput).attr(attr, JSON.stringify(dataAttrs[attr]));
							} else {
								$("#" + idInput).attr(attr, dataAttrs[attr]);
							}						
						}					
					}
					for (attr in attrs) {
						//console.log(attr);
						var exists = ximpia.common.ArrayUtil.hasKey(settings.excludeList, attr);
						if (exists == false) {
							$("#" + idInput).attr(attr, attrs[attr]);
						}					
					}
					if (typeof relatedId != 'undefined') {
						$("#" + idInput).attr('data-xp-related', relatedId);
					}
					if (typeof elementType != 'undefined') {
						$("#" + idInput).attr('data-xp-type', elementType);
					}
					//console.log($("#" + idInput));
					// Label				
					if (typeof dataAttrs != 'undefined' && dataAttrs.hasOwnProperty('label')) {
						$("label[for=\"" + idInput + "\"]").text(dataAttrs['label']);
						if (attrs.info == true) {
							$("label[for=\"" + idInput + "\"]").addClass("info");
							// help_text
							if (dataAttrs.hasOwnProperty('help_text')) {
								$("label[for=\"" + idInput + "\"]").attr('data-xp-title', dataAttrs['help_text']);
							}
						}	
					}
					sugAttrs = JSON.parse($("#" + idInput).attr('data-xp'));
					// Build property data from choices data
					var choicesId = dataAttrs['choicesId'];
					var choices = JSON.parse($("#id_choices").attr('value'))[choicesId];
					/*console.log('choices...');
					console.log('choicesId : ' + choicesId);
					console.log(choices)*/
					if (typeof(choices) != 'undefined') {
						sugAttrs.data = []
					}
					for (choiceIndex in choices) {
						sugAttrs.data[choiceIndex] = {}
						sugAttrs.data[choiceIndex]['id'] = choices[choiceIndex][0];
						sugAttrs.data[choiceIndex]['text'] = choices[choiceIndex][1];
					}
					//console.log(sugAttrs);
					if (sugAttrs.hasOwnProperty('data')) {
						$("#" + idInput).jsonSuggest({	data: sugAttrs.data, 
									maxHeight: sugAttrs.maxHeight, 
									minCharacters: sugAttrs.minCharacters
									});
					} else {
						$("#" + idInput).jsonSuggest({	url: sugAttrs.url, 
									maxHeight: sugAttrs.maxHeight, 
									minCharacters: sugAttrs.minCharacters
									});
					}
				}
			}
		},
		disable: function() {
			var idInput = $(this).attr('id').split('_comp')[0];
			$("#" + idInput).attr('disable', 'disable');
		},
		enable: function() {
		},
		addHidden: function(xpForm) {
			// xpData.form_login
			//console.log('addHidden...');
			//console.log('xpForm: ', xpForm);
			var data = ximpia.common.Browser.getFormDataFromSession(xpForm);
			var formId = ximpia.common.Browser.getForm(xpForm);
			var list = Object.keys(data);						
			for (key in list) {
				if (data[list[key]]['type'] == 'hidden') {					
					$('#' + formId).append("<input type=\"hidden\" id=\"id_" + formId + '_' + list[key] + "\" name=\"" + list[key] + "\" value=\"" + data[list[key]]['value'] + "\" />");
					$("#id_" + list[key]).attr('value', data[list[key]]['value']);
				}				
			}
			//console.log($('#' + formId));
		}
        };
		
        if ( methods[method] ) {
            return methods[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));
        } else if ( typeof method === 'object' || ! method ) {
            return methods.init.apply( this, arguments );
        } else {
            $.error( 'Method ' +  method + ' does not exist on jQuery.xpObjInput' );
        }    
		
	};

})(jQuery);
