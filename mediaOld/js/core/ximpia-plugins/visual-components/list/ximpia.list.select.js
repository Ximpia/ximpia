/*
 * Ximpia Visual Component Input: Text, Password, etc...
 *
 */

(function($) {	

	$.fn.xpObjListSelect = function( method ) {  

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
					var dataAttrs = data[nameInput];
					console.log('XpObjListSelect...');
					console.log(dataAttrs);
					console.log(attrs);
					var type = 'text';
					var value = "";
					var choicesId = "";
					if (dataAttrs.hasOwnProperty('choicesId')) {
						choicesId = dataAttrs['choicesId'];
					}
					if (attrs.hasOwnProperty('type')) {
						type = attrs.type;
					}
					// id, name, type
					var htmlContent = "";
					if (attrs.hasOwnProperty('left')) {
						htmlContent = "<div style=\"width: " + attrs['left'] + "px; float: left; border: 0px solid\"><label for=\"" + idInput + "\"></label>:</div> <div id=\"" + idField + "\" style=\"float: left; margin-top: 7px; margin-left: 3px\" ></div>";
					} else {
						htmlContent = "<div style=\"float: left; border: 0px solid\"><label for=\"" + idInput + "\"></label>:</div> <div id=\"" + idField + "\" style=\"float: left; margin-top: 7px; margin-left: 3px\" ></div>";
					}
					console.log(htmlContent);
					$(element).html(htmlContent);
					$(element).attr('data-xp-render', JSON.stringify(true));
					// Plugin
					//var countryList = JSON.parse(JSON.parse($('#id_' + myForm + '_choices').attr('value')))[choicesId];
					var countryList = JSON.parse($('#id_' + myForm + '_choices').attr('value'))[choicesId];
					var results = {'results': []};
					for (j in countryList) {
						results['results'][j] = {'id': countryList[j][0], 'name': countryList[j][1]}
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
					//fb.setValue('es', 'Spain');
					// Input
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
					$("label[for=\"" + idInput + "\"]").text(dataAttrs['label']);
					if (attrs.info == true) {
						$("label[for=\"" + idInput + "\"]").addClass("info");
						// help_text
						if (dataAttrs.hasOwnProperty('help_text')) {
							$("label[for=\"" + idInput + "\"]").attr('data-xp-title', dataAttrs['help_text']);
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
		setValue: function(code) {
			var data = JSON.parse(localStorage.getItem("xpForm"));			
			var idField = $(this).attr('id').split('_comp')[0] + '_field';
        		var id = '#' + idField.split('_field')[0];
        		var nameField = idField.split('_field')[0].split('id_')[1];
        		var field = data[nameField];
        		var choicesId = field['choicesId'];
        		var countryList = ximpia.common.Choices.get(choicesId);
			var value = ximpia.common.List.getValueFromList(code, countryList);
        		$(id).val(code).removeClass('watermark');
        		$(id + '_input').val(value).removeClass('watermark');			
		}	
        };
		
        if ( methods[method] ) {
            return methods[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));
        } else if ( typeof method === 'object' || ! method ) {
            return methods.init.apply( this, arguments );
        } else {
            $.error( 'Method ' +  method + ' does not exist on jQuery.xpObjListSelect' );
        }    
		
	};

})(jQuery);
