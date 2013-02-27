/*
 * Ximpia Visual Component Input: Text, Password, Decimal, etc... with autocompletion support
 * 
 * <div id="id_countryTxt_comp" data-xp-type="field" 	data-xp="{	label: 'Country Code', size: 2}" 
														data-xp-complete="{		choicesId: 'country', 
																				choiceDisplay: 'name',
																				minCharacters: 1	}"> </div>
 *
 * 
 * ** Attributes **
 * 
 * 
 * ** Attributes for Autocompletion Choices (data-xp-complete) **
 *
 * * ``choicesId``
 * * ``choiceDisplay`` [optional] default:value : name|value. Display either name or value from choices.
 * * ``maxHeight`` [optional]
 * * ``minCharacters`` [optional]
 * 
 * ** Attributes for Autocompletion Server (data-xp-complete) **
 *
 * * ``app`` [optional]
 * * ``dbClass``
 * * ``searchField`` :String : Search field to match for text from input field.
 * * ``maxHeight`` [optional]
 * * ``minCharacters`` [optional]
 * * ``params`` [optional] :Object : Parameters to filter completion list.
 * * ``fieldValue`` [optional] :String : Field to show results. In case not defined, will use the model string representation.
 * * ``extraFields`` [optional] :List : Fields to show in extra Object
 * 
 * ** Methods **
 * 
 * * ``render``
 * * ``complete``
 * * ``enable``
 * * ``disable``
 * * ``unrender``
 * 
 * ** Interfaces **
 * 
 * IComplete, IInputField
 * 
 */

(function($) {	

	$.fn.xpField = function( method ) {
		
	// Include documentation from wiki here  

        // Settings		
        var settings = {
        	excudeListInput: ['type','id','element','help_text','label','left'],
        	excudeListInputSug: ['type','id','element','help_text','label','left'],
        	excludeListLabel: ['type','id','element'],
        	excludeList: ['info','type','left'],
        	htmlAttrs: ['tabindex','readonly','maxlength','class','value','name','autocomplete','size'],
        	djangoAttrs: ['type','id','info','help_text','label','element','left','xptype'],
        	reRender: false,
        	labelPosition: 'left',
        	choiceDisplay: 'value'
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
		render: function(xpForm) {
			ximpia.console.log('input :: renderField...');
			var data = ximpia.common.Browser.getFormDataFromSession(xpForm);
			ximpia.console.log(data);
			for (var i=0; i<$(this).length; i++) {
				ximpia.console.log($(this)[i]);
				var element = $(this)[i]; 
				var idInput = $(element).attr('id').split('_comp')[0];
				var nameInput = idInput.split('id_')[1];
				var doRender = ximpia.common.Form.doRender(element, settings.reRender);
				if (doRender == true) {
					ximpia.console.log('renderField :: id: ' + $(element).attr('id'));
					ximpia.console.log('nameInput: ' + nameInput);
					$.metadata.setType("attr", "data-xp");
					var attrs = $(element).metadata();
					//ximpia.console.log('input attrs: ' + idInput);
					//ximpia.console.log(attrs);
					var relatedId = $(element).attr('data-xp-related');
					var elementType = $(element).attr('data-xp-type');
					var dataAttrs = {};
					if (data.hasOwnProperty(nameInput)) {
						dataAttrs = data[nameInput];
					} 
					var type = 'text';
					if (attrs.hasOwnProperty('type')) {
						type = attrs.type;
					}
					if (!attrs.hasOwnProperty('labelPosition')) {
						attrs['labelPosition'] = settings.labelPosition;
					}
					// id, name, type
					var htmlContent = "";
					ximpia.console.log(dataAttrs);
					var myValue = '';
					if (dataAttrs.hasOwnProperty('value')) {
						myValue = dataAttrs.value;
					}
					var labelWidth = attrs.labelWidth || ximpia.settings.LABEL_WIDTH;
					if (attrs['labelPosition'] == 'top') {
						htmlContent = "<div class=\"input-label-top\" style=\"width: " + labelWidth + "\"><label for=\"" + idInput + "\"></label></div><br/>";
						htmlContent += "<input id=\"" + idInput + "\" type=\"" + type + "\" name=\"" + 
							nameInput + "\" value=\"" + myValue + "\" />"
					} else {
						htmlContent = "<div class=\"input-label-left\" style=\"width: " + labelWidth + "\"><label for=\"" + idInput + "\"></label>: </div>";
						htmlContent += "<input id=\"" + idInput + "\" type=\"" + type + "\" name=\"" + 
							nameInput + "\" value=\"" + myValue + "\" /><div style=\"clear:both\"> <div>";
					}
					$(element).html(htmlContent);
					$(element).attr('data-xp-render', JSON.stringify(true));
					// Input
					// Insert attributes to form element from server and metadata of visual component
					ximpia.common.Form.doAttributes({
						djangoAttrs: settings.djangoAttrs,
						htmlAttrs: settings.htmlAttrs,
						excludeList: settings.excludeList,
						dataAttrs: dataAttrs,
						attrs: attrs,
						idElement: idInput
					});
					if (Object.keys(dataAttrs).length == 0) {
						$("#" + idInput).attr('class', 'field');
					}
					if (typeof relatedId != 'undefined') {
						$("#" + idInput).attr('data-xp-related', relatedId);
					}
					if (typeof elementType != 'undefined') {
						$("#" + idInput).attr('data-xp-type', elementType);
					}
					//ximpia.console.log($("#" + idInput));
					// Label
					//ximpia.console.log('dataAttrs');
					//ximpia.console.log(dataAttrs);
					if (!attrs.hasOwnProperty('hasLabel')) {
						attrs['hasLabel'] = true;
					}
					if (attrs['hasLabel'] == true) {
						if (attrs.hasOwnProperty('label')) {
							$("label[for=\"" + idInput + "\"]").text(attrs['label']);
						} else {
							$("label[for=\"" + idInput + "\"]").text(dataAttrs['label']);
						}
						if (attrs.info == true) {
							$("label[for=\"" + idInput + "\"]").addClass("info");
							// help_text
							if (attrs.hasOwnProperty('helpText')) {
								$("label[for=\"" + idInput + "\"]").attr('data-xp-title', attrs['helpText']);
							} else {
								if (dataAttrs && dataAttrs.hasOwnProperty('helpText')) {
									$("label[for=\"" + idInput + "\"]").attr('data-xp-title', dataAttrs['helpText']);
								}								
							}
						}
					}
					// Autocompletion
					$(element).xpField('complete', xpForm);
				}
			}
		},
		complete: function() {
        	// Autocompletion
			for (var i=0; i<$(this).length; i++) {
				ximpia.console.log($(this)[i]);
				var element = $(this)[i];         	
				$.metadata.setType("attr", "data-xp-complete");
				var attrs = $(element).metadata();
				ximpia.console.log('xpField.complete ::  attrs...');
				ximpia.console.log(attrs);
				var hasComplete = true;
				var idInput = $(element).attr('id').split('_comp')[0];
				ximpia.console.log('xpField.complete :: idInput: ' + idInput);
				if (typeof(attrs) == 'undefined') {
					hasComplete = false;
				}
				if (hasComplete == true) {
					ximpia.console.log('xpField.complete ::  Autocomplete...');
					// maxHeight
					var maxHeight = ximpia.settings.COMPLETE_MAX_HEIGHT;
					if (attrs.hasOwnProperty('maxHeight')) {
						maxHeight = attrs['maxHeight'];
					}
					// minCharacters
					var minCharacters = ximpia.settings.COMPLETE_MIN_CHARACTERS;
					if (attrs.hasOwnProperty('minCharacters')) {
						minCharacters = attrs['minCharacters'];
					}
					if (attrs.hasOwnProperty('choicesId')) {
						// From choices...
						ximpia.console.log('xpField.complete :: Autocomplete from choices...');
						var choicesId = attrs['choicesId'];
						var choices = JSON.parse($("input[name='choices']").attr('value'))[choicesId];
						var sugData = {};
						if (typeof(choices) != 'undefined') {
							sugData = []
						}
						if (!attrs.hasOwnProperty('choiceDisplay')) {
							attrs['choiceDisplay'] = settings.choiceDisplay;
						}
						for (choiceIndex in choices) {
							sugData[choiceIndex] = {}
							sugData[choiceIndex]['id'] = choices[choiceIndex][0];
							if (attrs['choiceDisplay'] == 'value') {
								sugData[choiceIndex]['text'] = choices[choiceIndex][1];
							} else {
								sugData[choiceIndex]['text'] = choices[choiceIndex][0];
							}
						}
						ximpia.console.log('xpField.complete :: Autocomplete :: sugData...');
						ximpia.console.log(sugData);
						$("#" + idInput).jsonSuggest({	data: sugData, 
														maxHeight: maxHeight, 
														minCharacters: minCharacters
														});
					} else if(attrs.hasOwnProperty('dbClass')) {
						// From server...
						ximpia.console.log('xpField.complete :: Autocomplete from server...');
						var app = ximpia.common.Browser.getApp();
						if (attrs.hasOwnProperty('app')) {
							app = attrs['app']
						}
						var params = {};
						if (attrs.hasOwnProperty('params')) {
							params = eval("(" + attrs['params'] + ")");
						}
						var dbClass = attrs['dbClass'];
						url = '/jxSuggestList?app=' + app + '&dbClass=' + dbClass + '&searchField=' + attrs['searchField'];
						if (Object.keys(params).length != 0) {
							url += "&params=" + JSON.stringify(params);
						}
						if (attrs.hasOwnProperty('fieldValue')) {
							url += "&fieldValue=" + attrs['fieldValue'];
						}
						if (attrs.hasOwnProperty('extraFields')) {
							url += "&extraFields=" + JSON.stringify(attrs['extraFields'])
						}
						$("#" + idInput).jsonSuggest({	url: url, 
														maxHeight: maxHeight, 
														minCharacters: minCharacters
													});
					}						
				}
			}
		},
		disable: function() {
			/*var idInput = $(this).attr('id').split('_comp')[0];
			$("#" + idInput).attr('disable', 'disable');*/
			for (var i=0; i<$(this).length; i++) {
				// Get all option items and disable them
				$(this).find("input[data-xp-type='field']").each(function() {
					$(this).attr('disabled', true);
				})				
			}
		},
		enable: function() {
			for (var i=0; i<$(this).length; i++) {
				// Get all option items and disable them
				$(this).find("input[data-xp-type='field']").each(function() {
					$(this).attr('disabled', false);
				})				
			}
		},
		unrender: function() {
			for (var i=0; i<$(this).length; i++) {
				$(this).empty();
				$(this).removeAttr('data-xp-render');
			}
		}
		};		
        if ( methods[method] ) {
            return methods[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));
        } else if ( typeof method === 'object' || ! method ) {
            return methods.init.apply( this, arguments );
        } else {
            $.error( 'Method ' +  method + ' does not exist on jQuery.xpField' );
        }    
		
	};

})(jQuery);


/*
 * Field for number fields with spinner control. Attributes for decimal formatting.
 * 
 * <div id="id_amount_comp" data-xp-type="field" data-xp="{}" > </div>
 *
 * 
 * ** Attributes **
 * 
 * * ``hideSpinner`` :Boolean : Hides spinner control
 * 
 * 
 * ** Methods **
 * 
 * * ``render``
 * * ``unrender``
 * * ``enable``
 * * ``disable``
 * 
 * ** Interfaces **
 * 
 * * IInputField
 * 
 */

(function($) {	

	$.fn.xpFieldNumber = function( method ) {
		
	// Include documentation from wiki here  

        // Settings		
        var settings = {
        	excudeListInput: ['type','id','element','help_text','label','left'],
        	excudeListInputSug: ['type','id','element','help_text','label','left'],
        	excludeListLabel: ['type','id','element'],
        	excludeList: ['info','type','left'],
        	htmlAttrs: ['tabindex','readonly','maxlength','class','value','name','autocomplete','size'],
        	djangoAttrs: ['type','id','info','help_text','label','element','left','xptype'],
        	reRender: false,
        	labelPosition: 'left',
        	hideSpinner: false
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
		render: function(xpForm) {
			ximpia.console.log('input :: renderField...');
			var data = ximpia.common.Browser.getFormDataFromSession(xpForm);
			ximpia.console.log(data);
			for (var i=0; i<$(this).length; i++) {
				ximpia.console.log($(this)[i]);
				var element = $(this)[i]; 
				var idInput = $(element).attr('id').split('_comp')[0];
				var nameInput = idInput.split('id_')[1];
				var doRender = ximpia.common.Form.doRender(element, settings.reRender);
				if (doRender == true && data.hasOwnProperty(nameInput)) {
					ximpia.console.log('renderField :: id: ' + $(element).attr('id'));
					ximpia.console.log('nameInput: ' + nameInput);
					$.metadata.setType("attr", "data-xp");
					var attrs = $(element).metadata();
					//ximpia.console.log('input attrs: ' + idInput);
					//ximpia.console.log(attrs);
					var relatedId = $(element).attr('data-xp-related');
					var elementType = $(element).attr('data-xp-type');
					var dataAttrs = data[nameInput];
					var type = 'text';
					if (attrs.hasOwnProperty('type')) {
						type = attrs.type;
					}
					if (!attrs.hasOwnProperty('labelPosition')) {
						attrs['labelPosition'] = settings.labelPosition;
					}
					// id, name, type
					var htmlContent = "";
					ximpia.console.log(dataAttrs);
					var myValue = dataAttrs.value;
					var labelWidth = attrs.labelWidth || ximpia.settings.LABEL_WIDTH;
					if (attrs['labelPosition'] == 'top') {
						htmlContent = "<div class=\"input-label-top\" style=\"width: " + labelWidth + "\"><label for=\"" + idInput + "\"></label></div><br/><input id=\"" + 
							idInput + "\" type=\"" + type + "\" name=\"" + nameInput + "\" value=\"" + myValue + "\" />";						
					} else {
						htmlContent = "<div class=\"input-label-left\" style=\"width: " + labelWidth + "\"><label for=\"" + idInput + "\"></label>: </div><input id=\"" + 
							idInput + "\" type=\"" + type + "\" name=\"" + nameInput + "\" value=\"" + 
							myValue + "\" /><div style=\"clear:both\"> </div>";					
					}
					$(element).html(htmlContent);
					$(element).attr('data-xp-render', JSON.stringify(true));
					// Input
					// Insert attributes to form element from server and metadata of visual component
					ximpia.common.Form.doAttributes({
						djangoAttrs: settings.djangoAttrs,
						htmlAttrs: settings.htmlAttrs,
						excludeList: settings.excludeList,
						dataAttrs: dataAttrs,
						attrs: attrs,
						idElement: idInput
					});
					if (typeof relatedId != 'undefined') {
						$("#" + idInput).attr('data-xp-related', relatedId);
					}
					if (typeof elementType != 'undefined') {
						$("#" + idInput).attr('data-xp-type', elementType);
					}
					//ximpia.console.log($("#" + idInput));
					// Label
					//ximpia.console.log('dataAttrs');
					//ximpia.console.log(dataAttrs);
					if (!attrs.hasOwnProperty('hasLabel')) {
						attrs['hasLabel'] = true;
					}
					/*if (attrs['labelPosition'] == 'left' && attrs['hasLabel'] == true) {
						$("label[for=\"" + idInput + "\"]").addClass("labelSep");
					}*/
					if (typeof dataAttrs != 'undefined' && dataAttrs.hasOwnProperty('label') && attrs['hasLabel'] == true) {
						if (attrs.hasOwnProperty('label')) {
							$("label[for=\"" + idInput + "\"]").text(attrs['label']);
						} else {
							$("label[for=\"" + idInput + "\"]").text(dataAttrs['label']);
						}
						if (attrs.info == true) {
							$("label[for=\"" + idInput + "\"]").addClass("info");
							// help_text
							if (dataAttrs.hasOwnProperty('helpText')) {
								$("label[for=\"" + idInput + "\"]").attr('data-xp-title', dataAttrs['helpText']);
							}
						}
					}
					// spinner for numbers
					var hideSpinner = settings.hideSpinner;
					if (attrs.hasOwnProperty('hideSpinner')) {
						hideSpinner = attrs['hideSpinner'];
					}
					if (hideSpinner == false) {
						var spinObj = {};
						if (dataAttrs.hasOwnProperty('maxValue')) {
							spinObj['max'] = dataAttrs['maxValue'];
						}
						if (dataAttrs.hasOwnProperty('minValue')) {
							spinObj['min'] = dataAttrs['minValue'];
						}
						if (dataAttrs['fieldType'] == 'IntegerField') {
							spinObj.step = 1;
							spinObj.numberFormat = 'n';
							$('#' + idInput).spinner(spinObj);
						} else if (dataAttrs['fieldType'] == 'FloatField') {
							spinObj.step = 1;
							spinObj.numberFormat = 'n';
							$('#' + idInput).spinner(spinObj);
						} else if (dataAttrs['fieldType'] == 'DecimalField' && dataAttrs.hasOwnProperty('decimalPlaces')
								&& parseInt(dataAttrs['decimalPlaces']) <= 6) {
							spinObj.numberFormat = 'n';
							spinObj.step = eval('1/(1e' + dataAttrs['decimalPlaces'] + ')');
							$('#' + idInput).spinner(spinObj);
						}
						if (attrs.labelPosition == 'left') {
							$('#' + idInput).parent().css('margin-left', '3px');
						}
					}
				}
			}
		},
		disable: function() {
			/*var idInput = $(this).attr('id').split('_comp')[0];
			$("#" + idInput).attr('disable', 'disable');*/
			for (var i=0; i<$(this).length; i++) {
				// Get all option items and disable them
				$(this).find("input[data-xp-type='field']").each(function() {
					$(this).attr('disabled', true);
				})				
			}
		},
		enable: function() {
			for (var i=0; i<$(this).length; i++) {
				// Get all option items and disable them
				$(this).find("input[data-xp-type='field']").each(function() {
					$(this).attr('disabled', false);
				})				
			}
		},
		unrender: function() {
			for (var i=0; i<$(this).length; i++) {
				$(this).empty();
				$(this).removeAttr('data-xp-render');
			}
		}
		};		
        if ( methods[method] ) {
            return methods[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));
        } else if ( typeof method === 'object' || ! method ) {
            return methods.init.apply( this, arguments );
        } else {
            $.error( 'Method ' +  method + ' does not exist on jQuery.xpFieldNumber' );
        }    
		
	};

})(jQuery);


/*
 * Ximpia Field Check
 * 
 * Renders fields that are BooleanField, with values true / false or 1 for true and 0 for false
 * 
 * Support labels. Check control can be before label or after.
 * 
 * <div id="id_hasUrl_comp" data-xp-type="field.check" data-xp="{}" > </div>
 *
 * ** Attributes (data-xp) **
 * 
 * * ``label`` [optional] : Field label
 * * ``controlPosition`` [optional] : 'before'|'after'. Default: 'before'. Position for the radio control, after or before text. 
 * 
 * ** Interfaces **
 * 
 * This components implements these interfaces:
 * 
 * * ``IInputField``
 * 
 * ** Methods **
 * 
 * * ``render``
 * * ``disable``
 * * ``enable``
 * 
 * 
 */

(function($) {	

	$.fn.xpFieldCheck = function( method ) {
		
	// Include documentation from wiki here  

        // Settings		
        var settings = {
        	controlPosition: 'after',
        	excudeListInput: ['type','id','element','help_text','label','left'],
        	excudeListInputSug: ['type','id','element','help_text','label','left'],
        	excludeListLabel: ['type','id','element'],
        	excludeList: ['info','type','left'],
        	htmlAttrs: ['tabindex','maxlength','readonly','class','name'],
        	djangoAttrs: ['type','id','info','help_text','label','element','left','xptype'],
        	isRender: false
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
		render: function(xpForm) {
			/**
			 * Render for radio buttons
			 */
			// id_month_comp : choiceId:'months'
			ximpia.console.log('xpOption :: option ... render...');
			var data = ximpia.common.Browser.getFormDataFromSession(xpForm);
			ximpia.console.log(data);
			for (var i=0; i<$(this).length; i++) {
				var element = $(this)[i];
				ximpia.console.log('xpFieldCheck :: element : ' + element); 
				var idBase = $(element).attr('id').split('_comp')[0];
				var name = idBase.split('id_')[1];
				ximpia.console.log('xpFieldCheck :: idBase : ' + idBase);
				var hasToRender = ximpia.common.Form.hasToRender(element, settings.reRender);
				if (hasToRender == true && data.hasOwnProperty(name)) {					
					var value = "";
					var choicesId = "";
					value = data[name]['value'];
					$.metadata.setType("attr", "data-xp");
					var attrs = $(element).metadata();
					ximpia.console.log('xpFieldCheck.render :: attrs...');
					ximpia.console.log(attrs);
	        		var htmlContent = "";
	        		if (!attrs.hasOwnProperty('controlPosition')) {
	        			attrs['controlPosition'] = settings.controlPosition;
	        		}
	        		// Label:
	        		var label = data[name]['label'];
	        		if (attrs.hasOwnProperty('label')) {
	        			label = attrs['label'];
	        		}
					var controlHtml = "";
					var ctlId = "id_" + name;
					if (value == true || value == '1') {
						controlHtml += "<input id=\"" + ctlId + "\" type=\"checkbox\" data-xp-type=\"field.check\" name=\"" + name + 
							"\" data-xp=\"{}\" checked=\"checked\"";
					} else {
						controlHtml += "<input id=\"" + ctlId + "\" type=\"checkbox\" data-xp-type=\"field.check\" name=\"" + name + 
							"\" data-xp=\"{}\"";
					}
					controlHtml += "/>";
        			var helpText = "";
        			if (attrs.hasOwnProperty('info') && attrs.info == true && data[name].hasOwnProperty('helpText') && 
        						attrs['controlPosition'] == 'after') {
        				helpText = "data-xp-title=\"" + data[name]['helpText'] + "\""
        			}
        			var attrClass = "";
        			if (attrs.hasOwnProperty('info') && attrs.info == true) {
        				attrClass = "class=\"info\"";
        			}
        			var labelWidth = attrs.labelWidth || ximpia.settings.LABEL_WIDTH;
					if (attrs['controlPosition'] == 'before') {
						htmlContent += controlHtml + "<div style=\"width: " + labelWidth + "\"><label for=\"" + ctlId + "\"" + attrClass + ' ' + helpText + ">" + 
							label + "</label></div>";
					} else {
						htmlContent += "<div style=\"width: " + labelWidth + "\"><label for=\"" + ctlId + "\"" + attrClass + ' ' + helpText + ">" + label + ": </label></div>" + 
							controlHtml;
					}
					// Assign html visual component div element
					$(element).html(htmlContent);
					// Help text...
					// Set render, since we have rendered visual component					
					ximpia.common.Form.doAttributes({
						djangoAttrs: settings.djangoAttrs,
						htmlAttrs: settings.htmlAttrs,
						excludeList: settings.excludeList,
						dataAttrs: data[name],
						attrs: attrs,
						idElement: idBase
					});
					if (typeof relatedId != 'undefined') {
						$("#" + idInput).attr('data-xp-related', relatedId);
					}					
					$(element).attr('data-xp-render', JSON.stringify(true));
					// Trace
					ximpia.console.log(htmlContent);
				} else if (!data.hasOwnProperty(name)) {
					ximpia.console.log('xpOption.render :: server data has no variable');
				}
			}
		},
		disable: function() {
			for (var i=0; i<$(this).length; i++) {
				// Get all option items and disable them
				$(this).find("input[data-xp-type='field.check']").each(function() {
					$(this).attr('disabled', true);
				})				
			}
		},
		enable: function() {
			for (var i=0; i<$(this).length; i++) {
				// Get all option items and disable them
				$(this).find("input[data-xp-type='field.check']").each(function() {
					$(this).attr('disabled', false);
				})				
			}
		},
		unrender: function() {
			for (var i=0; i<$(this).length; i++) {
				$(this).empty();
				$(this).removeAttr('data-xp-render');
			}
		}
        };
		
        if ( methods[method] ) {
            return methods[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));
        } else if ( typeof method === 'object' || ! method ) {
            return methods.init.apply( this, arguments );
        } else {
            $.error( 'Method ' +  method + ' does not exist on jQuery.xpFieldCheck' );
        }    
		
	};

})(jQuery);


/*
 * Date and Time field representation. This component renders form fields Date, DateTime and Time.
 * 
 * When field type is Date, a date tooltip will popup to select date.
 * 
 * When field type is Time, a time tooltip will popup to select time with two selection bars for hour and minute.
 * 
 * When field type is DateTime, a date with time tooltip will show up with calendar and time bars.
 *
 * <div id="id_updateDate_comp" data-xp-type="field.datetime" data-xp="{}"> </div>
 * 
 * We need to render the input field like Field, then apply the correct plugin depending on format: date, time or datetime
 * 
 * ** Attributes **
 * 
 * * ``hasLabel``
 * * ``labelPosition``
 * * ``info``
 * * ``class``
 * * ``tabindex``
 * * ``readonly``
 * * ``maxlength``
 * * ``value``
 * * ``name``
 * * ``autocomplete``
 * 
 * ** Methods **
 * 
 * * ``render``
 * * ``disable``
 * * ``enable``
 * * ``unrender``
 * 
 */

(function($) {	

	$.fn.xpFieldDateTime = function( method ) {

        // Settings		
        var settings = {
        	excudeListInput: ['type','id','element','help_text','label','left'],
        	excudeListInputSug: ['type','id','element','help_text','label','left'],
        	excludeListLabel: ['type','id','element'],
        	excludeList: ['info','type','left'],
        	htmlAttrs: ['tabindex','maxlength','class','value','name','autocomplete'],
        	djangoAttrs: ['type','id','info','help_text','label','element','left','xptype'],
        	reRender: false,
        	labelPosition: 'left'
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
		render : function(xpForm) {
			ximpia.console.log('xpFieldDateTime.render ...');
			var data = ximpia.common.Browser.getFormDataFromSession(xpForm);
			ximpia.console.log(data);
			for (var i=0; i<$(this).length; i++) {
				ximpia.console.log($(this)[i]);
				var element = $(this)[i]; 
				var idInput = $(element).attr('id').split('_comp')[0];
				var nameInput = idInput.split('id_')[1];
				var doRender = ximpia.common.Form.doRender(element, settings.reRender);
				if (doRender == true && data.hasOwnProperty(nameInput)) {
					ximpia.console.log('xpFieldDateTime.render :: id: ' + $(element).attr('id'));					
					ximpia.console.log('xpFieldDateTime.render :: nameInput: ' + nameInput);
					$.metadata.setType("attr", "data-xp");
					var attrs = $(element).metadata();
					var relatedId = $(element).attr('data-xp-related');
					var elementType = $(element).attr('data-xp-type');
					var dataAttrs = data[nameInput];
					var type = 'text';
					if (attrs.hasOwnProperty('type')) {
						type = attrs.type;
					}
					if (!attrs.hasOwnProperty('labelPosition')) {
						attrs['labelPosition'] = settings.labelPosition;
					}
					// id, name, type					
					var htmlContent = "";
					ximpia.console.log(dataAttrs);
					var myValue = dataAttrs.value;
					var labelWidth = attrs.labelWidth || ximpia.settings.LABEL_WIDTH;
					if (attrs['labelPosition'] == 'top') {
						htmlContent = "<div class=\"input-label-top\" style=\"width: " + labelWidth + "\"><label for=\"" + idInput + "\"></label></div><br/><input id=\"" + 
								idInput + "\" type=\"" + type + "\" name=\"" + nameInput + "\" value=\"" + myValue + 
								"\" readonly=\"readonly\" />";
						
					} else {
						htmlContent = "<div class=\"input-label-left\" style=\"width: " + labelWidth + "\"><label for=\"" + idInput + "\"></label>: </div><input id=\"" + 
								idInput + "\" type=\"" + type + "\" name=\"" + nameInput + "\" value=\"" + myValue + 
								"\" readonly=\"readonly\" /><div style=\"clear:both\"> </div>";
						
					}
					$(element).html(htmlContent);					
					// Input
					// Insert attributes to form element from server and metadata of visual component
					ximpia.common.Form.doAttributes({
						djangoAttrs: settings.djangoAttrs,
						htmlAttrs: settings.htmlAttrs,
						excludeList: settings.excludeList,
						dataAttrs: dataAttrs,
						attrs: attrs,
						idElement: idInput
					});
					if (typeof relatedId != 'undefined') {
						$("#" + idInput).attr('data-xp-related', relatedId);
					}
					$("#" + idInput).attr('data-xp-type', 'field.datetime');
					// Label
					if (!attrs.hasOwnProperty('hasLabel')) {
						attrs['hasLabel'] = true;
					}
					/*if (attrs['labelPosition'] == 'left' && attrs['hasLabel'] == true) {
						$("label[for=\"" + idInput + "\"]").addClass("labelSep");
					}*/
					if (typeof dataAttrs != 'undefined' && dataAttrs.hasOwnProperty('label') && attrs['hasLabel'] == true) {
						if (attrs.hasOwnProperty('label')) {
							$("label[for=\"" + idInput + "\"]").text(attrs['label']);
						} else {
							$("label[for=\"" + idInput + "\"]").text(dataAttrs['label']);
						}
						if (attrs.info == true) {
							$("label[for=\"" + idInput + "\"]").addClass("info");
							// help_text
							if (dataAttrs.hasOwnProperty('helpText')) {
								$("label[for=\"" + idInput + "\"]").attr('data-xp-title', dataAttrs['helpText']);
							}
						}
					}
					if (dataAttrs['fieldType'] == 'DateField') {			
						$('#' + idInput).datepicker();
					} else if (dataAttrs['fieldType'] == 'DateTimeField') {
						$('#' + idInput).datetimepicker();
					} else if (dataAttrs['fieldType'] == 'TimeField') {
						$('#' + idInput).timepicker();
					}
					$(element).attr('data-xp-render', JSON.stringify(true));
				}
			}
		},
		disable: function() {
			for (var i=0; i<$(this).length; i++) {
				// Get all option items and disable them
				$(this).find("input[data-xp-type='field.date']").each(function() {
					$(this).attr('disabled', true);
				})				
			}
		},
		enable: function() {
			for (var i=0; i<$(this).length; i++) {
				// Get all option items and disable them
				$(this).find("input[data-xp-type='field.date']").each(function() {
					$(this).attr('disabled', false);
				})				
			}
		},
		unrender: function() {
			for (var i=0; i<$(this).length; i++) {
				$(this).empty();
				$(this).removeAttr('data-xp-render');
			}
		}
		};		
        if ( methods[method] ) {
            return methods[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));
        } else if ( typeof method === 'object' || ! method ) {
            return methods.init.apply( this, arguments );
        } else {
            $.error( 'Method ' +  method + ' does not exist on jQuery.xpFieldDateTime' );
        }
	};

})(jQuery);



/*
 * Ximpia Visual Component Hidden
 * 
 * TODO: Include the html for component
 *
 */

(function($) {	

	$.fn.xpHidden = function( method ) {
		
	// Include documentation from wiki here  

        // Settings		
        var settings = {
        	excudeListInput: ['type','id','element','help_text','label','left'],
        	excudeListInputSug: ['type','id','element','help_text','label','left'],
        	excludeListLabel: ['type','id','element'],
        	excludeList: ['info','type','left'],
        	htmlAttrs: ['tabindex','readonly','maxlength','class','value','name','autocomplete'],
        	djangoAttrs: ['type','id','info','help_text','label','element','left','xptype'],
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
		addHidden: function(xpForm) {
			// xpData.form_login
			//ximpia.console.log('addHidden...');
			//ximpia.console.log('xpForm: ', xpForm);
			var data = ximpia.common.Browser.getFormDataFromSession(xpForm);
			var formId = ximpia.common.Browser.getForm(xpForm);
			var viewName = ximpia.common.Browser.getView(xpForm);
			//ximpia.console.log('data length : ' + data.length());
			if (typeof data != 'undefined') {
				var list = Object.keys(data);
				//JSON.stringify(data[list[key]]['value'])
				for (var i=0; i<list.length; i++) {
					if (data[list[i]]['type'] == 'hidden') {
						//var value = JSON.stringify(data[list[key]]['value']);
						var value = data[list[i]]['value'];
						$('#' + formId).append("<input type=\"hidden\" id=\"id_" + formId + '_' + list[i] + "\" name=\"" + list[i] + "\"  />");
						$("#id_" + formId + '_' + list[i]).attr('value', value);
						// Inject viewNameSource : viewName is same as formId
						if (list[i] == 'viewNameSource') {
							$("#id_" + formId + '_' + list[i]).attr('value', viewName);
						}
					}				
				}				
			}
			//ximpia.console.log($('#' + formId));
		}
        };
		
        if ( methods[method] ) {
            return methods[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));
        } else if ( typeof method === 'object' || ! method ) {
            return methods.init.apply( this, arguments );
        } else {
            $.error( 'Method ' +  method + ' does not exist on jQuery.xpHidden' );
        }    
		
	};

})(jQuery);

/*
 * 
 *
 * Ximpia Visual Component Check: Checkbox button with fields coming from choices (choices class or foreign key)
 *  
 * ** HTML **
 * 
 * <div id="id_mycheck_comp" data-xp-type="check" data-xp="{alignment: 'vertical'}" > </div>
 * 
 * 
 * Your form should have ``mycheck``field
 * 
 * ** Attributes (data-xp) **
 * 
 * * ``alignment`` [optional] : 'vertical', 'horizontal'
 * * ``hasLabel`` [optional] : "true"|"false". Weather to show or not a label, at left or top of check controls.
 * * ``label`` [optional] : Field label
 * * ``labelPosition`` [optional] : 'top'|'left'. Label position, left of check buttons, or top for label at one line and check
 * 									controls on a new line.
 * * ``controlPosition`` [optional] : 'before'|'after'. Default: 'before'. Position for the check control, after or before text.
 * * ``info``[optional] : Displays tooltip with helpText field data.
 * 
 * Having alignment vertical will show ``ui-option-vertical`` class. Alignment horizontal has class ``ui-option-horizontal``
 * 
 * 
 * ** Interfaces **
 * 
 * This components implements these interfaces:
 * 
 * * ``IInputList``
 *  
 * 
 * ** Methods **
 * 
 * * ``render``
 * * ``disable``
 * * ``enable``
 * 
 * 
 *
 */

(function($) {	

	$.fn.xpCheck = function( method ) {  

        // Settings		
        var settings = {
        	labelPosition: 'left',
        	controlPosition: 'before',
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
		render: function(xpForm) {
			/**
			 * Render for radio buttons
			 */
			// id_month_comp : choiceId:'months'
			ximpia.console.log('xpOption :: option ... render...');
			var data = ximpia.common.Browser.getFormDataFromSession(xpForm);
			ximpia.console.log(data);
			for (var i=0; i<$(this).length; i++) {
				var element = $(this)[i];
				ximpia.console.log('xpCheck :: element : ' + element); 
				var idBase = $(element).attr('id').split('_comp')[0];
				var name = idBase.split('id_')[1];
				ximpia.console.log('xpCheck :: idBase : ' + idBase);
				var hasToRender = ximpia.common.Form.hasToRender(element, settings.reRender);
				if (hasToRender == true && data.hasOwnProperty(name)) {					
					var value = "";
					var choicesId = "";
					var valueList = eval(data[name]['value']);
					choicesId = data[name]['choicesId']
					$.metadata.setType("attr", "data-xp");
					var attrs = $(element).metadata();
	        		// Choices
	        		ximpia.console.log('xpCheck :: choicesId: ' + choicesId);
	        		var choiceList = JSON.parse(data['choices']['value'])[choicesId];
	        		ximpia.console.log('xpCheck :: choicesList: ' + choiceList);
	        		var htmlContent = "";
	        		if (!attrs.hasOwnProperty('labelPosition') && attrs.hasOwnProperty('hasLabel')) {
	        			attrs['labelPosition'] = settings.labelPosition;
	        		}
	        		if (!attrs.hasOwnProperty('controlPosition')) {
	        			attrs['controlPosition'] = settings.controlPosition;
	        		}
	        		if (attrs['alignment'] == 'vertical' && attrs.hasOwnProperty('hasLabel') && attrs['hasLabel'] == true) {	        			
	        			attrs['labelPosition'] = 'top';
	        		}
	        		// Label:
	        		var label = data[name]['label'];
	        		if (attrs.hasOwnProperty('label')) {
	        			label = attrs['label'];
	        		}
	        		var classLabel = 'ui-check-label-left';
	        		if (attrs.hasOwnProperty('hasLabel') && attrs.hasOwnProperty('labelPosition') && attrs['labelPosition'] == 'top') {
	        			classLabel = 'ui-check-label-top';
	        		}
	        		var labelWidth = attrs.labelWidth || ximpia.settings.LABEL_WIDTH;
	        		if (attrs.hasOwnProperty('hasLabel') && attrs['hasLabel']) {
	        			htmlContent += "<div class=\"" + classLabel + "\" style=\"width: " + labelWidth + "\" >";
	        			var helpText = "";
	        			if (attrs.hasOwnProperty('info') && attrs.info == true && data[name].hasOwnProperty('helpText')) {
	        				helpText = "data-xp-title=\"" + data[name]['helpText'] + "\""
	        			}
	        			var attrClass = "";
	        			if (attrs.hasOwnProperty('info') && attrs.info == true) {
	        				attrClass = "class=\"info\"";
	        			}
	        			htmlContent += "<label for=\"id_" + name + "_" + choiceList[0][0] + "\" " + attrClass+ " " + helpText + 
	        					" style=\"margin-right: 5px\">" + label + "</label>";
	        			if (attrs.labelPosition == 'left') {
	        				htmlContent += ': ';
	        			}
	        			htmlContent += "</div>";
	        		}
	        		// Option items
	        		if (attrs.alignment == 'horizontal') {
	        			htmlContent += "<ul class=\"ui-check-horizontal\">";
	        		} else  {
	        			htmlContent += "<ul class=\"ui-check-vertical\">";
	        		}
	        		var valueNewList = [];
	        		for (var j=0; j<valueList.length; j++) {
	        			valueNewList.push(valueList[j].pk);
	        		};
					for (var j=0 ; j<choiceList.length; j++) {
						htmlContent += "<li>";
						var controlHtml = "";
						var ctlId = "id_" + name + "_" + choiceList[j][0];
						var hasValue = ximpia.common.ArrayUtil.hasKey(valueNewList, choiceList[j][0]);
						if (hasValue) {
							controlHtml += "<input id=\"" + ctlId + "\" type=\"checkbox\" data-xp-type=\"check\" name=\"" + name + 
								"\" value=\"" + choiceList[j][0] + "\" data-xp=\"{}\" checked=\"checked\"";
						} else {
							controlHtml += "<input id=\"" + ctlId + "\" type=\"checkbox\" data-xp-type=\"check\" name=\"" + name + 
								"\" value=\"" + choiceList[j][0] + "\" data-xp=\"{}\"";
						}
						controlHtml += "/>";
						if (attrs['controlPosition'] == 'before') {
							htmlContent += controlHtml + "<label for=\"" + ctlId + "\">" + choiceList[j][1] + "</label>";
						} else {
							htmlContent += "<label for=\"" + ctlId + "\">" + choiceList[j][1] + "</label>" + controlHtml;
						}
						htmlContent += "</li>";
					}
					htmlContent += "</ul>";
					// Assign html visual component div element
					$(element).html(htmlContent);
					// Help text...
					// Set render, since we have rendered visual component
					$(element).attr('data-xp-render', JSON.stringify(true));
					// Trace
					ximpia.console.log(htmlContent);
				} else if (!data.hasOwnProperty(name)) {
					ximpia.console.log('xpCheck.render :: server data has no variable');
				}
			}
		},
		disable: function() {
			for (var i=0; i<$(this).length; i++) {
				// Get all option items and disable them
				$(this).find("input[data-xp-type='check']").each(function() {
					$(this).attr('disabled', true);
				})				
			}
		},
		enable: function() {
			for (var i=0; i<$(this).length; i++) {
				// Get all option items and disable them
				$(this).find("input[data-xp-type='check']").each(function() {
					$(this).attr('disabled', false);
				})				
			}
		},
		unrender: function() {
			for (var i=0; i<$(this).length; i++) {
				$(this).empty();
				$(this).removeAttr('data-xp-render');
			}
		}
        };		
        if ( methods[method] ) {
            return methods[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));
        } else if ( typeof method === 'object' || ! method ) {
            return methods.init.apply( this, arguments );
        } else {
            $.error( 'Method ' +  method + ' does not exist on jQuery.xpCheck' );
        }
	};

})(jQuery);

/*
 * List of fields. Fields can be added and deleted. Can represent the many-to-many relationships in models 
 * 
 * They can be rendered as tags horizontally
 * 
 * ** Field Type HTML **
 * 
 * ** Select Type HTML **
 * 
 * 
 * ** Attributes **
 * 
 * * ``type``:string [default: field] [optional] : Type of control for adding values: ``field`` and ``select.plus`` possible values.
 * * ``labelWidth``:number [optional]
 * * ``selectObjId``:string [optional]
 * * ``modelField``:string [optiona] : For field input type, the model field value. Required for fields. Not required for select input.
 * 
 * ** Methods **
 * 
 * * ``render``
 * * ``keypress``
 * * ``enable``
 * * ``disable``
 * * ``unrender``
 * 
 * ** Interfaces **
 * 
 * IInputField
 *
 */

(function($) {	

	$.fn.xpFieldList = function( method ) {  

        // Settings		
        var settings = {
        	excudeListSelect: ['type','id','element','help_text','label','data-xp-val', 'value', 'choices','choicesId'],
        	excludeListLabel: ['type','id','element'],
        	excludeList: ['info','type'],
        	limit: 10,
        	type: 'field'
        };
        /*
         * Variables
         */
        var vars = {
        	form: ''
        };
        /**
         * Build Item html code
         * 
         * ** Attributes **
         * 
         * * ``obj``
         * 		* ``dataId``
         * 		* ``idBase``
         * 		* ``inputDataId``
         * 		* ``data``
         */
        var buildItemHtml = function(obj) {
			var sHtml = '<div class="listField" style=\"float:left\"><div class="listFieldText"' +  
				' style=\"float:left\">' + obj.data + '</div>' + 
				'<div class="listFieldDel" style=\"float:left\" data-xp-field-id=\"' + obj.dataId + 
				'\" data-xp-field-input-id=\"' + obj.inputDataId + '\" data-xp-field-hidden-id=\"' + obj.idBase + '\"';
			/*if (obj.hasOwnProperty('attrs') && obj.attrs.hasOwnProperties('modelField')) {
				sHtml += ' data-xp-field-model=\"' + obj.attrs.modelField + '\"';
			}*/
			sHtml += '>X</div></div>';
			return sHtml;
        };
        /**
         * Delete the item.
         * 
         * ** Arguments **
         * 
         * * ``element``: Delete control
         * * ``idBase``: id for component
         * * ``inputDataId``: input id (field, select, etc...)
         */
        var deleteItem = function(element, idBase, inputDataId) {
        	var index = $(element).parent().index();
			var idElementHid = $(element).attr('data-xp-field-hidden-id');
    		$(element).parent().remove();
    		var baseValue = $("#" + idElementHid).attr('value');
			var valueList = eval(baseValue);
			valueList.splice(index, 1);
			ximpia.console.log('xpFieldList.deleteItem :: valueList...');
			ximpia.console.log(valueList);
			var valueListStr = JSON.stringify(valueList).replace(/"/g, "'");
			$('#' + idBase).val(valueListStr);
			$('#' + inputDataId).focus();
        };
        /**
         * Get global type: field, select. Field would group all field types and select would group all select components
         */
        var getGlobalType = function(type) {
			if (type == 'field') {
				var globalType = 'field';
			} else if (type == 'select' || type == 'select.plus') {
				var globalType = 'select';
			}
			return globalType;
       };
       /**
        * Get data values : [dataId, data]
        */
       var getDataValues = function(globalType, dataItemObj, attrs, dataObj) {
			if (globalType == 'select') {
				var dataId = dataItemObj.pk;
				var data = dataObj[dataId] || '';
			} else {
				var dataId = dataItemObj.pk;
				if (attrs.hasOwnProperty('modelField')) {
					var data = dataItemObj[attrs['modelField']];
				} else {
					var data = '';
				}
			}
			return [dataId, data];
      };
        /**
         * Add field
         * 
         * ** Arguments +*
         * 
         * * ``inputField``
         * * ``feedType``
         * * ``choicesId``
         */
		var addField = function(inputField, feedType, choicesId) {
        	ximpia.console.log('xpFieldList.addField...');
        	ximpia.console.log('xpFieldList.addField :: inputField: ' + inputField + ' feedType: ' + feedType);
        	var inputDataId = inputField.split('_comp')[0];
        	var globalType = getGlobalType(feedType);
        	if (globalType == 'field') {
        		var idBase = inputField.split('Input_comp')[0];
				var data = $("#" + inputDataId).prop('value');
				var dataId = data;
        	} else if (globalType == 'select') {
        		var idBase = $('#' + inputField).parent().attr('id').split('_comp')[0];
        		var dataId = $("#" + inputDataId).prop('value');
        		// Get from choices data
        		var data = ximpia.common.Choices.getData(vars.form, choicesId, dataId);
        	}
			ximpia.console.log('xpFieldList.addField :: data: ' + data + ' dataId: ' + dataId);
			var idBaseList = idBase;
			var baseValue = $("#" + idBase).attr('value');
			var baseFields = [];
			if (typeof baseValue != 'undefined') {
				baseFields = baseValue.split(',');
			}
			$.metadata.setType("attr", "data-xp");
			var attrs = $("#" + idBase).parent().metadata();
			var limit = attrs['limit'] || settings.limit;
			ximpia.console.log('xpFieldList.addField :: idBaseList: ' + idBaseList);
			var hasElement = false;
			var valueList = eval(baseValue);
			for (i=0; i<valueList.length; i++) {
				if (globalType == 'select') {
					if (valueList[i].pk == dataId) {
						hasElement = true;
					}
				} else {
					fieldModelName = attrs['modelField']
					if (valueList[i][fieldModelName] == data) {
						hasElement = true;
					}
				}
			}
			var size = 0;
			if (baseFields != "") {
				size = baseFields.length
			}			
			var validate = false;
			ximpia.console.log('xpFieldList.addField :: dataId: ' + dataId);
			ximpia.console.log('xpFieldList.addField :: size: ' + size);
			ximpia.console.log('xpFieldList.addField :: hasElement: ' + hasElement);
			if (dataId != '' && size < limit && hasElement == false) {
				validate = true;
			}
			ximpia.console.log('xpFieldList.addField :: validate: ' + validate);
			if (validate == true) {
				var sHtml = buildItemHtml({dataId: dataId, inputDataId:inputDataId, idBase:idBase, data:data});
				ximpia.console.log(sHtml);
				$('#' + idBase + 'Show').append(sHtml);
				var baseList = eval(baseValue);
				if (feedType == 'field') {
					var itemObj = {};					
					if ($('#' + inputField).attr('data-xp-complete')) {
						$.metadata.setType("attr", "data-xp-complete");
						var attrsComplete = $("#" + inputField).metadata();
						if (attrsComplete.hasOwnProperty('choicesId')) {
							var choicesId = attrsComplete.choicesId;
							var itemChObj = ximpia.common.Choices.getByValue(vars.form, choicesId, data);
							if (itemChObj) {
								itemObj.pk = itemChObj[0];
							}
						}
					}
					itemObj[attrs['modelField']] = data;
					baseList.push(itemObj);
				} else {
					baseList.push({ pk: dataId });
				}
				ximpia.console.log(baseList);
				baseListStr = JSON.stringify(baseList).replace(/"/g, "'");
				$('#' + idBase).val(baseListStr);
				if (globalType == 'field') {
					$('#' + inputDataId).prop('value', '');
					$('#' + inputDataId).focus();
				} else {
					$('#' + inputField).xpSelectPlus('setValue', '', '');
				}
				// Remove Field Bind
				$('#' + idBase + 'Show').children().last().find('.listFieldDel').click(function() {
					deleteItem($(this), idBase, inputDataId);
				});
			} else if (size >= limit) {
				// TODO: Show a fancy messahe window
				alert('Can´t include more fields to the list!');
			} else if (hasElement == true) {
				if (globalType == 'field') {
					$('#' + inputDataId).prop('value', '');
					$('#' + inputDataId).focus();
				} else {
					$('#' + inputField).xpSelectPlus('setValue', '', '');
				}
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
		render: function(xpForm) {
			ximpia.console.log('xpFieldList :: render...');
			var data = ximpia.common.Browser.getFormDataFromSession(xpForm);
			vars.form = ximpia.common.Browser.getForm(xpForm); 
			ximpia.console.log(data);
			for (var i=0; i<$(this).length; i++) {
				//ximpia.console.log($(this)[i]);
				var element = $(this)[i];
				ximpia.console.log('element : ' + element); 
				var idBase = $(element).attr('id').split('_comp')[0];
				var name = idBase.split('id_')[1];
				ximpia.console.log('xpFieldList.render :: idBase : ' + idBase);
				var doRender = ximpia.common.Form.doRender(element, settings.reRender);				
				if (doRender == true) {
					var nameInput = name + 'Input';
					var nameList = name;
					$.metadata.setType("attr", "data-xp");
					var attrs = $(element).metadata();
					var dataAttrs = {};
					if (data.hasOwnProperty(name)) {
						dataAttrs = data[name];
					}
					ximpia.console.log('xpFieldList.render :: attrs....');
					ximpia.console.log(attrs); 
					var type = attrs.type || settings.type;
					var label = '';
					if (dataAttrs.hasOwnProperty('label')) {
						label = dataAttrs['label'];
					}
					if (attrs.hasOwnProperty('label')) {
						label = attrs['label'];
					}
					// myValue would be ['value1','value2',...]
					var myValue = '[]';
					if (dataAttrs.hasOwnProperty('value')) {
						myValue = dataAttrs.value;
					}
					// TODO: Generate complex components from any basic field.
					var labelWidth = attrs.labelWidth || "auto";
					var info = attrs.info || false;
					var helpText = attrs.helpText || dataAttrs.helpText;
					var choicesId = attrs.choicesId || '';
					var inputField = '';
					var globalType = getGlobalType(type);
					if (type == "field") {
						var htmlContent = "";
						inputField = idBase + 'Input_comp';
						htmlContent += "<div id=\"" + idBase + 'Input_comp' + "\" data-xp-type=\"field\"";
						htmlContent += " data-xp=\"{label: '" + label + "', labelWidth: '" + labelWidth + "', info:" + info + "}\" style=\"float: left; margin-top: 0px\" data-xp-related=\"field.list\" ></div>";
						htmlContent += "<div style=\"float: left\"><a href=\"#\" class=\"buttonIcon buttonIconSmall\"";
						htmlContent += " data-xp-type=\"button.field\"";
						htmlContent += " data-xp=\"{input: '" + idBase + "Input_comp', type: 'field'}\" style=\"font-size:97% !important; margin-top: 3px\" >Add</a></div>";
						htmlContent += "<div id=\"" + idBase + "Show\" class=\"listContainer\"";
						htmlContent += " style=\"width: 300px; margin-left: 15px; \" ></div><div style='clear:both'></div>";
						htmlContent += "<input id=\"id_" + nameList + "\" type=\"hidden\" name=\"" + nameList + "\" value=\"" + myValue + "\" />";
					} else if (type == "select.plus") {
						var htmlContent = "";
						inputField = attrs['selectObjId'];
						htmlContent += "<div id=\"" + attrs['selectObjId'] + "\" data-xp-type=\"select.plus\"";
						htmlContent += " data-xp=\"{label: '" + label + "', labelWidth: '" + labelWidth + "', info:" + info + ", helpText:'" + helpText + "', choicesId: '" + choicesId + "'}\" style=\"float: left; margin-top: 2px\" data-xp-related=\"field.list\"  ></div>";
						htmlContent += "<div style=\"float: left\"><a href=\"#\" class=\"buttonIcon buttonIconSmall\"";
						htmlContent += " onclick=\"return false;\" data-xp-type=\"button.field\" data-xp=\"{input: '" + attrs['selectObjId'];
						htmlContent += "', type: 'select', choicesId: '" + choicesId + "'}\" style=\"margin-top:4px\" >Add</a></div>";
						htmlContent += "<div id=\"" + idBase + "Show\" class=\"listContainer\" style=\"width: 300px;";
						htmlContent += " margin-left: 15px; margin-top: 2px\" ></div><div style='clear:both'></div>";
						htmlContent += "<input id=\"id_" + nameList + "\" type=\"hidden\" name=\"" + nameList + "\" value=\"" + 
											myValue + "\" />";
					}
					$(element).html(htmlContent);
					if (globalType == 'field' && $(element).attr('data-xp-complete')) {
						$('#' + idBase + 'Input_comp').attr('data-xp-complete', $(element).attr('data-xp-complete'));
					}
					$(element).attr('data-xp-render', JSON.stringify(true));
					$(element).css('clear', 'both');
					// Render item values
					if (myValue != '[]') {
		        		var dataObj = {};
		        		var choiceList = JSON.parse($("[name='choices']").attr('value'))[choicesId];
		        		for (j in choiceList) {
		        			dataObj[choiceList[j][0]] = choiceList[j][1];
		        		}
		        		ximpia.console.log(dataObj);
						var itemList = eval(myValue);
						ximpia.console.log('xpFieldList.render :: itemList...');
						ximpia.console.log(itemList);
						var inputDataId = inputField.split('_comp')[0];
						for (var i=0; i<itemList.length; i++) {
							var dataItemObj = itemList[i];
							var dataValues = getDataValues(globalType, dataItemObj, attrs, dataObj);
							var dataId = dataValues[0];
							var data = dataValues[1];
							if (data != '') {
								var sHtml = buildItemHtml({dataId: dataId, inputDataId:inputDataId, idBase:idBase, data: data});
								$('#' + idBase + 'Show').append(sHtml);
							}
						}
						// Remove Field Bind
						$('.listFieldDel').click(function() {
							deleteItem($(this), idBase, inputDataId);
						});
					}
					ximpia.console.log('xpFieldList.render :: field list html...');
					ximpia.console.log(htmlContent);
				}				
			}			
			// Bind click event to add button
			$("[data-xp-type='button.field']").click(function(evt) {
				evt.preventDefault();
				$.metadata.setType("attr", "data-xp");
				var attrsButton = $(this).metadata();
				ximpia.console.log(attrsButton);
				var inputField = attrsButton['input'];
				ximpia.console.log('xpFieldList.render :: click button :: inputField: ' + inputField);
				var feedType = attrsButton['type'];
				ximpia.console.log('xpFieldList.render :: click button :: feedType: ' + feedType);
				var choicesId = "";
				if (attrsButton.hasOwnProperty('choicesId')) {
					choicesId = attrsButton['choicesId'];
					ximpia.console.log('xpFieldList.render :: click button :: choicesId: ' + choicesId);
				}
				addField(inputField, feedType, choicesId);
			});
		},
		keyPress: function() {
			for (var i=0; i<$(this).length; i++) {
				var element = $(this)[i];
				$(element).keypress(function(e) {
					if (e.which == 13) {
						// Enter Key
						var inputField = e.currentTarget.id + '_comp';
						ximpia.console.log('xpFieldList.keyPress :: inputField: ' + inputField);
						//ximpia.console.log($(element)[0].form.id);
						vars.form = $(element)[0].form.id;
                		addField(inputField, 'field');
					}
				});
			}			
		}
        };
        if ( methods[method] ) {
            return methods[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));
        } else if ( typeof method === 'object' || ! method ) {
            return methods.init.apply( this, arguments );
        } else {
            $.error( 'Method ' +  method + ' does not exist on jQuery.xpFieldList' );
        }
	};

})(jQuery);

/*
 * 
 *
 * Ximpia Visual Component Option: Radio button with fields coming from choices
 *  
 * ** HTML **
 * 
 * <div id="id_myoption_comp" data-xp-type="option" data-xp="{type: 'radio', alignment: 'vertical'}" > </div>
 * 
 * <div id="id_myoption_comp" data-xp-type="option" data-xp="{type: 'check', alignment: 'vertical'}" > </div>
 * 
 * Your form should have ``myoption``field
 * 
 * ** Attributes (data-xp) **
 * 
 * * ``type`` : 'radio', 'check'
 * * ``alignment`` [optional] : 'vertical', 'horizontal'. Default. horizontal.
 * * ``hasLabel`` [optional] : "true"|"false". Weather to show or not a label, at left or top of radio controls.
 * * ``label`` [optional] : Field label
 * * ``labelPosition`` [optional] : 'top'|'left'. Label position, left of radio buttons, or top for label at one line and radio
 * 									controls on a new line.
 * * ``controlPosition`` [optional] : 'before'|'after'. Default: 'before'. Position for the radio control, after or before text.
 * * ``info``[optional] : Displays tooltip with helpText field data.
 * 
 * Having alignment vertical will show ``ui-option-vertical`` class. Alignment horizontal has class ``ui-option-horizontal``
 * 
 * 
 * ** Interfaces **
 * 
 * This components implements these interfaces:
 * 
 * * ``IInputList``
 *  
 * 
 * ** Methods **
 * 
 * * ``render``
 * * ``disable``
 * * ``enable``
 * 
 * ** Types **
 * * ``radio``: radio option box
 * * ``checkbox``: check box. Behaved like option, when user clicks on one, it gets selected. Ability to have no option cheched.
 * 
 *
 */


(function($) {	

	$.fn.xpOption = function( method ) {  

        // Settings		
        var settings = {
        	labelPosition: 'left',
        	controlPosition: 'before',
        	alignment: 'horizontal',
        	type: 'radio',
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
		render: function(xpForm) {
			/**
			 * Render for radio buttons
			 */
			// id_month_comp : choiceId:'months'
			ximpia.console.log('xpOption :: option ... render...');
			var data = ximpia.common.Browser.getFormDataFromSession(xpForm);
			ximpia.console.log(data);
			for (var i=0; i<$(this).length; i++) {
				var element = $(this)[i];
				ximpia.console.log('xpOption :: element : ' + element); 
				var idBase = $(element).attr('id').split('_comp')[0];
				var name = idBase.split('id_')[1];
				ximpia.console.log('xpOption :: idBase : ' + idBase);
				var hasToRender = ximpia.common.Form.hasToRender(element, settings.reRender);
				if (hasToRender == true && data.hasOwnProperty(name)) {					
					var value = "";
					var choicesId = "";
					value = data[name]['value'];
					choicesId = data[name]['choicesId']
					$.metadata.setType("attr", "data-xp");
					var attrs = $(element).metadata();
	        		// Choices
	        		ximpia.console.log('xpOption :: choicesId: ' + choicesId);
	        		var choiceList = JSON.parse(data['choices']['value'])[choicesId];
	        		ximpia.console.log('xpOption :: choicesList: ' + choiceList);
	        		var htmlContent = "";
	        		if (!attrs.hasOwnProperty('labelPosition') && attrs.hasOwnProperty('hasLabel')) {
	        			attrs['labelPosition'] = settings.labelPosition;
	        		}
	        		if (!attrs.hasOwnProperty('controlPosition')) {
	        			attrs['controlPosition'] = settings.controlPosition;
	        		}
	        		if (attrs['alignment'] == 'vertical' && attrs.hasOwnProperty('hasLabel') && attrs['hasLabel'] == true) {	        			
	        			attrs['labelPosition'] = 'top';
	        		}
	        		// Label:
	        		var label = data[name]['label'];
	        		if (attrs.hasOwnProperty('label')) {
	        			label = attrs['label'];
	        		}
	        		var classLabel = 'ui-option-label-left';
	        		if (attrs.hasOwnProperty('hasLabel') && attrs.hasOwnProperty('labelPosition') && attrs['labelPosition'] == 'top') {
	        			classLabel = 'ui-option-label-top';
	        		}
	        		var labelWidth = attrs.labelWidth || ximpia.settings.LABEL_WIDTH;
	        		if (attrs.hasOwnProperty('hasLabel') && attrs['hasLabel']) {
	        			htmlContent += "<div class=\"" + classLabel + "\" style=\"width: " + labelWidth + "\" >";
	        			var helpText = "";
	        			if (attrs.hasOwnProperty('info') && attrs.info == true && data[name].hasOwnProperty('helpText')) {
	        				helpText = "data-xp-title=\"" + data[name]['helpText'] + "\""
	        			}
	        			var attrClass = "";
	        			if (attrs.hasOwnProperty('info') && attrs.info == true) {
	        				attrClass = "class=\"info\"";
	        			}
	        			htmlContent += "<label for=\"id_" + name + "_" + choiceList[0][0] + "\" " + attrClass+ " " + helpText + 
	        					" style=\"\">" + label + "</label>";
	        			if (attrs.labelPosition == 'left') {
	        				htmlContent += ': ';
	        			}
	        			htmlContent += "</div>";	        			
	        		}
	        		// Option items
	        		if (!attrs.hasOwnProperty('alignment')) {
	        			attrs.alignment = settings.alignment;
	        		}
	        		if (attrs.alignment == 'horizontal') {
	        			htmlContent += "<ul class=\"ui-option-horizontal\">";
	        		} else  {
	        			htmlContent += "<ul class=\"ui-option-vertical\">";
	        		}
	        		if (!attrs.hasOwnProperty('type')) {
	        			attrs['type'] = settings.type;
	        		}
					for (var j=0 ; j<choiceList.length; j++) {
						htmlContent += "<li>";
						var controlHtml = "";
						var ctlId = "id_" + name + "_" + choiceList[j][0];
						if (choiceList[j][0] == value) {
							if (attrs.type == 'radio') {
								controlHtml += "<input id=\"" + ctlId + "\" type=\"radio\" data-xp-type=\"option\" name=\"" + name + 
									"\" value=\"" + choiceList[j][0] + "\" data-xp=\"{}\" checked=\"checked\"";
							} else {
								controlHtml += "<input id=\"" + ctlId + "\" type=\"checkbox\" data-xp-type=\"option\" name=\"" + name + 
									"\" value=\"" + choiceList[j][0] + "\" data-xp=\"{}\" checked=\"checked\"";
							}
						} else if (attrs.type == 'radio' && j == 0 && choiceList[j][0] != value) {
							controlHtml += "<input id=\"" + ctlId + "\" type=\"radio\" data-xp-type=\"option\" name=\"" + name + 
									"\" value=\"" + choiceList[j][0] + "\" data-xp=\"{}\" checked=\"checked\"";
						} else {
							if (attrs.type == 'radio') {
								controlHtml += "<input id=\"" + ctlId + "\" type=\"radio\" data-xp-type=\"option\" name=\"" + name + 
									"\" value=\"" + choiceList[j][0] + "\" data-xp=\"{}\"";
							} else {
								controlHtml += "<input id=\"" + ctlId + "\" type=\"checkbox\" data-xp-type=\"option\" name=\"" + name + 
									"\" value=\"" + choiceList[j][0] + "\" data-xp=\"{}\"";
							}
						}
						controlHtml += "/>";
						if (attrs['controlPosition'] == 'before') {
							htmlContent += controlHtml + "<label for=\"" + ctlId + "\">" + choiceList[j][1] + "</label>";
						} else {
							htmlContent += "<label for=\"" + ctlId + "\">" + choiceList[j][1] + "</label>" + controlHtml;
						}
						htmlContent += "</li>";
					}
					htmlContent += "</ul><div style=\"clear: both\"></div>";
					// Assign html visual component div element
					$(element).html(htmlContent);
					// Help text...
					// Set render, since we have rendered visual component
					$(element).attr('data-xp-render', JSON.stringify(true));
					$(element).css('line-height','20px');
					$(element).css('margin-top','-5px');
					$(element).css('margin-bottom','2px');
					// Trace
					ximpia.console.log(htmlContent);
				} else if (!data.hasOwnProperty(name)) {
					ximpia.console.log('xpOption.render :: server data has no variable');
				}
			}
			// Click option items
			$("input[type='checkbox'][data-xp-type='option']").click(function(evt, unchecked) {
				if ($(this)[0].checked == true && typeof(unchecked) == 'undefined') {
					// New click from user
					//ximpia.console.log('xpOption.render :: checked: ' + $(this)[0].checked);
					var name = $(this).attr('name');
					var checkedItems = $("input[name='" + name + "']:checked");
					//ximpia.console.log(checkedItems);
					// Uncheck item
					if (checkedItems.length > 0) {
						for (var i=0; i<checkedItems.length; i++) {
							if (checkedItems[i].id != $(this).attr('id')) {
								//ximpia.console.log('xpOption.render :: Will click on ' + checkedItems[i].id);
								// We set uncheck to true, so that will not try to check values
								$("#" + checkedItems[i].id).trigger('click', [true]);
							}							
						}
					}				
				}
			})
		},
		disable: function() {
			for (var i=0; i<$(this).length; i++) {
				// Get all option items and disable them
				$(this).find("input[data-xp-type='option']").each(function() {
					$(this).attr('disabled', true);
				})				
			}
		},
		enable: function() {
			for (var i=0; i<$(this).length; i++) {
				// Get all option items and disable them
				$(this).find("input[data-xp-type='option']").each(function() {
					$(this).attr('disabled', false);
				})				
			}
		},
		unrender: function() {
			for (var i=0; i<$(this).length; i++) {
				$(this).empty();
				$(this).removeAttr('data-xp-render');
			}
		}
        };		
        if ( methods[method] ) {
            return methods[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));
        } else if ( typeof method === 'object' || ! method ) {
            return methods.init.apply( this, arguments );
        } else {
            $.error( 'Method ' +  method + ' does not exist on jQuery.xpOption' );
        }
	};

})(jQuery);

/*
 * Ximpia Visual Component Input: Text, Password, etc...
 * 
 * 
 * ** Methods **
 * 
 * * ``render``
 * * ``disable``
 * * ``setValue``
 * * ``enable``
 * * ``unrender``
 * 
 * ** Interfaces **
 *
 */

(function($) {	

	$.fn.xpSelectPlus = function( method ) {  

        // Settings		
        var settings = {
        	excudeListSelect: ['type','id','element','help_text','label','data-xp-val', 'value', 'choices','choicesId'],
        	excludeListLabel: ['type','id','element'],
        	excludeList: ['info','type','left'],
        	htmlAttrs: ['tabindex','readonly','maxlength','class','value','name','autocomplete'],
        	djangoAttrs: ['type','id','info','help_text','label','element','left','xptype','choices'],
        	formData: {}
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
		render: function(xpForm) {
			var data = ximpia.common.Browser.getFormDataFromSession(xpForm);
			var myForm = ximpia.common.Form.getForm(xpForm);
			//var data = JSON.parse(sessionStorage.getItem("xpForm"));
			console.log($(this));
			console.log('Elements : ' + $(this).length);
			for (var i=0; i<$(this).length; i++) {
				console.log($(this)[i]);
				var element = $(this)[i];
				var doRender = ximpia.common.Form.doRender(element, settings.reRender);
				if (doRender == true) {				 
					var idInputSrc = $(element).attr('id').split('_comp')[0];
					var idInput = $(element).attr('id').split('_comp')[0] + '_input';
					var idInputValue = $(element).attr('id').split('_comp')[0];
					var nameInput = idInputSrc.split('id_')[1];
					var idField = $(element).attr('id').split('_comp')[0] + '_field';
					$.metadata.setType("attr", "data-xp");
					var attrs = $(element).metadata();
					var dataAttrs = {};
					if (data.hasOwnProperty(nameInput)) {
						dataAttrs = data[nameInput];
					} 
					console.log('XpObjListSelect...');
					console.log(dataAttrs);
					console.log(attrs);
					var type = 'text';
					var value = "";
					var choicesId = "";
					if (dataAttrs.hasOwnProperty('choicesId')) {
						choicesId = dataAttrs['choicesId'];
					}
					if (attrs.hasOwnProperty('choicesId')) {
						choicesId = attrs['choicesId'];
					}
					//alert(choicesId);
					if (attrs.hasOwnProperty('type')) {
						type = attrs.type;
					}
					// id, name, type
					var htmlContent = "";
					var labelWidth = attrs.labelWidth || ximpia.settings.LABEL_WIDTH;
					if (attrs['labelPosition'] == 'top') {
						htmlContent = "<div class=\"input-label-top\" style=\"width: " + labelWidth + "\"><label for=\"" + idInput + "\"></label></div><br/>";
						htmlContent += "<div id=\"" + idField + "\"  > </div><div style=\"clear: both\" > </div>";
					} else {
						htmlContent = "<div class=\"input-label-left\" style=\"width: " + labelWidth + "\" ><label for=\"" + idInput + "\"></label>: </div>";
						htmlContent += "<div id=\"" + idField + "\" style=\"float: left; margin-top: 3px; /*margin-left: 3px*/\" ></div>";
						htmlContent += "<div style=\"clear: both\" > </div>";
					}
					console.log(htmlContent);
					$(element).html(htmlContent);
					$(element).attr('data-xp-render', JSON.stringify(true));
					$(element).css('line-height', '22px');
					// Plugin
					var values = ['',''];
					if (dataAttrs.hasOwnProperty('value')) {
						values[0] = dataAttrs.value;
					}
					var controlList = JSON.parse($('#id_' + myForm + '_choices').attr('value'))[choicesId];
					var results = {'results': []};
					for (j in controlList) {
						results['results'][j] = {'id': controlList[j][0], 'name': controlList[j][1]}
						if (values[0] != '' && controlList[j][0] == values[0]) {
							values[1] = controlList[j][1];
						}
					}
					console.log('idField : ' + idField);
					// *************
					// ** Flexbox **
					// *************
					// input: maxVisibleRows, allowInput
					var fb = $("#" + idField).flexbox(results,{
						autoCompleteFirstMatch: true,
						paging: false,
						maxVisibleRows: 10
					});
					if (dataAttrs.hasOwnProperty('value')) {
						fb.setValue(values[0], values[1]);
					}
					// Input
					if (!dataAttrs.hasOwnProperty('class')) {
						dataAttrs['class'] = 'field';
					}
					ximpia.common.Form.doAttributes({
						djangoAttrs: settings.djangoAttrs,
						htmlAttrs: settings.htmlAttrs,
						excludeList: settings.excludeList,
						dataAttrs: dataAttrs,
						attrs: attrs,
						idElement: idInput,
						skipName: true
					});					
					// Label
					if (!attrs.hasOwnProperty('hasLabel')) {
						attrs['hasLabel'] = true;
					}
					if (attrs['hasLabel'] == true) {
						if (attrs.hasOwnProperty('label')) {
							$("label[for=\"" + idInput + "\"]").text(attrs['label']);
						} else {
							$("label[for=\"" + idInput + "\"]").text(dataAttrs['label']);
						}
						if (attrs.info == true) {
							$("label[for=\"" + idInput + "\"]").addClass("info");
							// help_text
							if (attrs.hasOwnProperty('helpText')) {
								$("label[for=\"" + idInput + "\"]").attr('data-xp-title', attrs['helpText']);
							}else {
								if (dataAttrs && dataAttrs.hasOwnProperty('helpText')) {
									$("label[for=\"" + idInput + "\"]").attr('data-xp-title', dataAttrs['helpText']);
								}								
							}
						}
					} else {
						if (attrs['hasLabel'] == true) {
							$("label[for=\"" + idInput + "\"]").text(attrs['label']);
						}
					}
					/*console.log($("#" + idInput));*/
					console.log($(element));
				}
			}
		},
		disable: function() {
			var idField = $(this).attr('id').split('_comp')[0] + '_field';
			var id = '#' + idField.split('_field')[0];
			$(id + '_input').attr('disabled', 'disabled');
			$('#' + idField + '_arrow').unbind('mouseenter mouseleave click mousedown mouseup');
		},		
		enable: function() {
			for (var i=0; i<$(this).length; i++) {
				// Get all option items and disable them
				$(this).find("input[data-xp-type='field']").each(function() {
					$(this).attr('disabled', false);
				})				
			}
		},
		unrender: function() {
			for (var i=0; i<$(this).length; i++) {
				$(this).empty();
				$(this).removeAttr('data-xp-render');
			}
		},
		setValue: function(xpForm, code) {
			var formId = ximpia.common.Browser.getForm(xpForm);
			ximpia.console.log('setValue :: formId: ' + formId);
			ximpia.console.log('setValue :: xpForm: ' + xpForm);
			var data = ximpia.common.Browser.getFormDataFromSession(xpForm);
			var idField = $(this).attr('id').split('_comp')[0] + '_field';
    		var id = '#' + idField.split('_field')[0];
    		var nameField = idField.split('_field')[0].split('id_')[1];
    		ximpia.console.log('setValue :: nameField: ' + nameField);
    		ximpia.console.log(data);
    		if (typeof data != 'undefined' && data.hasOwnProperty(nameField)) {
    			var field = data[nameField];
    			var choicesId = field['choicesId'];
    			ximpia.console.log('setValue :: choicesId: ' + choicesId);
    			var controlList = ximpia.common.Choices.get(formId, choicesId);
    			ximpia.console.log('setValue :: controlList: ' + controlList);
    			var value = ximpia.common.List.getValueFromList(code, controlList);
    			$(id).val(code).removeClass('watermark');
    			$(id + '_input').val(value).removeClass('watermark');
    		} else {
    			$(id).val(code).removeClass('watermark');
    			$(id + '_input').val(value).removeClass('watermark');
    		}
		}	
        };		
        if ( methods[method] ) {
            return methods[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));
        } else if ( typeof method === 'object' || ! method ) {
            return methods.init.apply( this, arguments );
        } else {
            $.error( 'Method ' +  method + ' does not exist on jQuery.xpSelectPlus' );
        }    		
	};

})(jQuery);

/*
 * Ximpia Visual Component Input: Text, Password, etc...
 * 
 * ** Methods **
 * 
 * * ``render``
 * * ``setValue``
 * * ``disable``
 * * ``enable``
 * * ``unrender``
 * 
 * ** Interfaces **
 *
 */

(function($) {	

	$.fn.xpSelect = function( method ) {  

        // Settings		
        var settings = {
        	excudeListSelect: ['type','id','element','help_text','label','left','choices','choicesId'],
        	excudeListInputSug: ['type','id','element','help_text','label','left'],
        	excludeListLabel: ['type','id','element'],
        	excludeList: ['info','type','left','choices'],
        	htmlAttrs: ['tabindex','readonly','maxlength','class','value','name','autocomplete','size'],
        	djangoAttrs: ['type','id','info','help_text','label','element','left','choices'],
        	reRender: false,
        	labelPosition: 'left',
        	choiceDisplay: 'value'
        	//excudeListSelect: ['type','id','element','help_text','label','data-xp-val', 'value', 'choices','choicesId'],
        	//excludeListLabel: ['type','id','element'],
        	//excludeList: ['info','type']
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
		render: function(xpForm) {
			ximpia.console.log('input :: renderField...');
			var data = ximpia.common.Browser.getFormDataFromSession(xpForm);
			ximpia.console.log(data);
			for (var i=0; i<$(this).length; i++) {
				//console.log($(this)[i]);
				var element = $(this)[i]; 
				var idInput = $(element).attr('id').split('_comp')[0];
				var nameInput = idInput.split('id_')[1];
				var doRender = ximpia.common.Form.doRender(element, settings.reRender);
				if (doRender == true && data.hasOwnProperty(nameInput)) {
					$.metadata.setType("attr", "data-xp");
					var attrs = $(element).metadata();
					var dataAttrs = data[nameInput];
					var type = 'text';
					if (attrs.hasOwnProperty('type')) {
						type = attrs.type;
					}
					if (!attrs.hasOwnProperty('labelPosition')) {
						attrs['labelPosition'] = settings.labelPosition;
					}
					var value = "";
					if (dataAttrs.hasOwnProperty('value')) {
						value = dataAttrs.value;
					}
					// id, name, type
					var htmlContent = "";
					var labelWidth = attrs.labelWidth || ximpia.settings.LABEL_WIDTH;
					if (attrs['labelPosition'] == 'top') {
						htmlContent = "<div class=\"input-label-top\" style=\"width: " + labelWidth + "\"><label for=\"" + idInput + "\"></label></div><br/>";
						htmlContent += " <select id=\"" + idInput + "\" name=\"" + nameInput + "\"  ></select></div>";
					} else {
						htmlContent = "<div class=\"input-label-left\" style=\"width: " + labelWidth + "\" ><label for=\"" + idInput + "\"></label>: </div>";
						htmlContent += " <select id=\"" + idInput + "\" name=\"" + nameInput + "\"  ></select></div>";
					}
					$(element).html(htmlContent);
					$(element).attr('data-xp-render', JSON.stringify(true));				
					// Input
					// Insert attributes to form element from server and metadata of visual component
					ximpia.common.Form.doAttributes({
						djangoAttrs: settings.djangoAttrs,
						htmlAttrs: settings.htmlAttrs,
						excludeList: settings.excludeList,
						dataAttrs: dataAttrs,
						attrs: attrs,
						idElement: idInput
					});
					// Choices
					var choicesId = dataAttrs['choicesId'];
					var choices = JSON.parse($("[name='choices']").attr('value'))[choicesId];
					if (dataAttrs['required'] == false) {
						$("#" + idInput).append("<option value=\"\"></option>");
					}
					for (choiceIndex in choices) {
						if (choices[choiceIndex][0] == value) {
							var htmlSelect = "<option value=\"" + choices[choiceIndex][0] + "\" selected=\"selected\">" + choices[choiceIndex][1] + "</option>";
						} else {
							var htmlSelect = "<option value=\"" + choices[choiceIndex][0] + "\">" + choices[choiceIndex][1] + "</option>";
						}
						$("#" + idInput).append(htmlSelect);
					}
					// Label				
					if (!attrs.hasOwnProperty('hasLabel')) {
						attrs['hasLabel'] = true;
					}
					if (typeof dataAttrs != 'undefined' && dataAttrs.hasOwnProperty('label') && attrs['hasLabel'] == true) {
						if (attrs.hasOwnProperty('label')) {
							$("label[for=\"" + idInput + "\"]").text(attrs['label']);
						} else {
							$("label[for=\"" + idInput + "\"]").text(dataAttrs['label']);
						}
						if (attrs.info == true) {
							$("label[for=\"" + idInput + "\"]").addClass("info");
							// help_text
							if (dataAttrs.hasOwnProperty('helpText')) {
								$("label[for=\"" + idInput + "\"]").attr('data-xp-title', dataAttrs['helpText']);
							}
						}
					} else {
						if (attrs['hasLabel'] == true) {
							$("label[for=\"" + idInput + "\"]").text(attrs['label']);
						}
					}
				}				
			}
		},
		disable: function() {
			for (var i=0; i<$(this).length; i++) {
				// Get all option items and disable them
				$(this).find("input[data-xp-type='select']").each(function() {
					$(this).attr('disabled', true);
				})				
			}
		},
		enable: function() {
			for (var i=0; i<$(this).length; i++) {
				// Get all option items and disable them
				$(this).find("input[data-xp-type='select']").each(function() {
					$(this).attr('disabled', false);
				})				
			}
		},
		unrender: function() {
			for (var i=0; i<$(this).length; i++) {
				$(this).empty();
				$(this).removeAttr('data-xp-render');
			}
		}
        };		
        if ( methods[method] ) {
            return methods[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));
        } else if ( typeof method === 'object' || ! method ) {
            return methods.init.apply( this, arguments );
        } else {
            $.error( 'Method ' +  method + ' does not exist on jQuery.xpSelect' );
        }
	};

})(jQuery);

/*
 * TextArea
 * 
 * ** Attributes **
 * 
 * * ``cols``
 * * ``rows``
 * * ``isCollapsible``
 * 
 * ** Methods **
 * 
 * * ``render``
 * * ``unrender``
 * * ``enable``
 * * ``disable``
 * 
 *
 */

(function($) {	

	$.fn.xpTextArea = function( method ) {  

        // Settings		
        var settings = {
        	excudeListInput: ['type','id','element','help_text','label','left'],
        	excudeListInputSug: ['type','id','element','help_text','label','left'],
        	excludeListLabel: ['type','id','element'],
        	excludeList: ['info','type','left'],
        	htmlAttrs: ['tabindex','readonly','maxlength','class','value','name','autocomplete','size'],
        	djangoAttrs: ['type','id','info','help_text','label','element','left','xptype'],
        	reRender: false,
        	labelPosition: 'left',        	
			'maxLimit' : 144,
			'maxHeight' : 150,
			isCollapsible: false
        };
                
        var setCSS = function(which){
        	// Init the div for the current textarea
        	var id = which.attr('id') + '_hidden';
        	$("#" + id).css({
        		'position':'absolute',
        		'top': -10000,
        		'left': -10000,
        		'width': $(which).width(),
        		'min-height': $(which).height(),
        		'font-family': $(which).css('font-family'),
        		'font-size': $(which).css('font-size'),
        		'line-height': $(which).css('line-height')
        	});
        	if($.browser.msie && parseFloat($.browser.version) < 7){
        		$("#" + id).css('height',$(which).height());
        	};
        };                
        var copyContent = function(which){
        	// Convert the line feeds into BRs
        	var id = which.attr('id') + '_hidden';
        	$("#" + id).css('width', which.width());
        	theValue = $(which).val() || "";
        	theValue = theValue.replace(/\n/g,'<br />');
        	$("#" + id).html(theValue + '<br />');
        	$(which).height($("#" + id).height());						
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
		render: function(xpForm) {
			ximpia.console.log('input :: renderField...');
			var data = ximpia.common.Browser.getFormDataFromSession(xpForm);
			ximpia.console.log(data);
			for (var i=0; i<$(this).length; i++) {
				console.log($(this)[i]);
				var element = $(this)[i];
				var idInput = $(element).attr('id').split('_comp')[0];
				var nameInput = idInput.split('id_')[1];
				var doRender = ximpia.common.Form.doRender(element, settings.reRender);
				if (doRender == true && data.hasOwnProperty(nameInput)) {
					$.metadata.setType("attr", "data-xp"); 
					var attrs = $(element).metadata();
					var dataAttrs = data[nameInput];
					console.log('xpTextArea.render :: idInput: ' + idInput);
					console.log('xpTextArea.render :: nameInput: ' + nameInput)
					console.log('xpTextArea.render :: *** text area data : dataAttrs ***');
					console.log(dataAttrs);
					console.log('xpTextArea.render :: *** text area data : attrs ***');
					console.log(attrs);					
					if (!attrs.hasOwnProperty('labelPosition')) {
						attrs['labelPosition'] = settings.labelPosition;
					}
					var areaAttrs = "";
					if (attrs.hasOwnProperty('cols')) {
						areaAttrs += " cols=" + attrs['cols']
					}
					if (attrs.hasOwnProperty('rows')) {
						areaAttrs += " rows=" + attrs['rows']
					}
					var htmlContent = "";
					var labelWidth = attrs.labelWidth || ximpia.settings.LABEL_WIDTH;
					if (attrs['labelPosition'] == 'top') {
						htmlContent = "<div class=\"input-label-top\" style=\"width: " + labelWidth + "\"><label for=\"" + idInput + "\"></label></div>";
						htmlContent += "<textarea id=\"" + idInput + "\" " + areaAttrs + " name=\"" + nameInput + "\"/>";
					} else {
						htmlContent = "<div class=\"input-label-left\" style=\"width: " + labelWidth + "\"><label for=\"" + idInput + "\"></label>: </div>";
						htmlContent += "<textarea id=\"" + idInput + "\" " + areaAttrs + " name=\"" + nameInput + "\"";
						htmlContent += " style=\"margin-top: 5px\" /> <div style=\"clear:both\"> </div>";
					}
					$(element).html(htmlContent);
					$(element).attr('data-xp-render', JSON.stringify(true));
					// Input
					// Insert attributes to form element from server and metadata of visual component
					ximpia.common.Form.doAttributes({
						djangoAttrs: settings.djangoAttrs,
						htmlAttrs: settings.htmlAttrs,
						excludeList: settings.excludeList,
						dataAttrs: dataAttrs,
						attrs: attrs,
						idElement: idInput
					});
					// Label
					if (!attrs.hasOwnProperty('hasLabel')) {
						attrs['hasLabel'] = true;
					}
					if (typeof dataAttrs != 'undefined' && dataAttrs.hasOwnProperty('label') && attrs['hasLabel'] == true) {
						if (attrs.hasOwnProperty('label')) {
							$("label[for=\"" + idInput + "\"]").text(attrs['label']);
						} else {
							$("label[for=\"" + idInput + "\"]").text(dataAttrs['label']);
						}
						if (attrs.info == true) {
							$("label[for=\"" + idInput + "\"]").addClass("info");
							// help_text
							if (dataAttrs.hasOwnProperty('helpText')) {
								$("label[for=\"" + idInput + "\"]").attr('data-xp-title', dataAttrs['helpText']);
							}
						}
					} else {
						if (attrs['hasLabel'] == true) {
							$("label[for=\"" + idInput + "\"]").text(attrs['label']);
						}
					}
					if (!attrs.hasOwnProperty('isCollapsible')) {
						attrs['isCollapsible'] = settings.isCollapsible;
					}
					if (attrs['isCollapsible'] == true) {
						var textarea = $("#" + idInput);
	        			var id = textarea.attr('id') + '_hidden';
	        			$('body').append('<div id="' + id + '"></div>');
						console.log('xpTextArea.render :: textarea...');
						console.log(textarea);      			
	        			textarea.css({
		            				'overflow':'hidden'
	        				})
	        				.bind('keyup',function(){
	        					//console.log('writing...');
	        					copyContent(textarea);
						//}
	        				});
	        				// Make sure all the content in the textarea is visible
	        				//alert(textarea.width());
	        				setCSS(textarea);
	        				copyContent(textarea);
							textarea.height($("#" + id).height());		
					//};									
					}
				}	
			}
		},
		disable: function() {
			/*var idInput = $(this).attr('id').split('_comp')[0];
			$("#" + idInput).attr('disable', 'disable');*/
			for (var i=0; i<$(this).length; i++) {
				// Get all option items and disable them
				$(this).find("input[data-xp-type='textarea']").each(function() {
					$(this).attr('disabled', true);
				})				
			}
		},
		enable: function() {
			for (var i=0; i<$(this).length; i++) {
				// Get all option items and disable them
				$(this).find("input[data-xp-type='textarea']").each(function() {
					$(this).attr('disabled', false);
				})				
			}
		},
		unrender: function() {
			for (var i=0; i<$(this).length; i++) {
				$(this).empty();
				$(this).removeAttr('data-xp-render');
			}
		}
        };
		
        if ( methods[method] ) {
            return methods[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));
        } else if ( typeof method === 'object' || ! method ) {
            return methods.init.apply( this, arguments );
        } else {
            $.error( 'Method ' +  method + ' does not exist on jQuery.xpTextArea' );
        }    		
	};
})(jQuery);
