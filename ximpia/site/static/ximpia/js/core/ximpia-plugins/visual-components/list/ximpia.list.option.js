/*
 * Ximpia Visual Component Option: Radio button with fields coming from choices
 *
 */

(function($) {	

	$.fn.xpObjListOption = function( method ) {  

        // Settings		
        var settings = {
        	/*excudeListSelect: ['type','id','element','help_text','label','data-xp-val', 'value', 'choices','choicesId'],
        	excludeListLabel: ['type','id','element'],
        	excludeList: ['info','type','left'],
        	htmlAttrs: ['tabindex','value','name'],
        	djangoAttrs: ['type','id','info','help_text','label','element','left','xptype','choices'],
        	formData: {}*/
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
			/**
			 * Render for radio buttons
			 */
			// id_month_comp : choiceId:'months'
			ximpia.console.log('option ... render...');
			var data = JSON.parse(sessionStorage.getItem("xpForm"));
			for (var i=0; i<$(this).length; i++) {
				var element = $(this)[i];
				ximpia.console.log('element : ' + element); 
				var idBase = $(element).attr('id').split('_comp')[0];
				console.log('idBase : ' + idBase);
				var doRender = ximpia.common.Form.doRender(element, settings.reRender);
				if (doRender == true) {
					var name = idBase.split('id_')[1];
					var value = "";
					var choicesId = "";
					if (data.hasOwnProperty(name)) {
						value = data[name]['value'];
						choicesId = data[name]['choicesId']
					}					
					$.metadata.setType("attr", "data-xp");
					var attrs = $(element).metadata();
		        		// Choices
		        		ximpia.console.log('choiceId: ' + attrs['choiceId']);
		        		var choiceList = JSON.parse($('#id_choices').attr('value'))[choicesId];
		        		var htmlContent = "";
		        		if (attrs.alignment == 'vertical') {
		        			htmlContent = htmlContent + "<ul>";
		        		}
					var htmlContent = "<ul>";
					for (var j=0 ; i<choiceList.length; j++) {
						if (attrs.alignment == 'vertical') {
							htmlContent = htmlContent + "<li>";
						}
						if (choiceList[j][0] == value || j == 0) {
							if (attrs.type == 'radio') {
								htmlContent = htmlContent + "<input type=\"radio\" data-xp-type=\"input.option\" name=\"" + name + "\" value=\"" + choiceList[j][0] + "\" selected />" + choiceList[j][1];
							} else {
								htmlContent = htmlContent + "<input type=\"checkbox\" data-xp-type=\"input.checkOption\" name=\"" + name + "\" value=\"" + choiceList[j][0] + "\" checked />" + choiceList[j][1];
							}
						} else {
							if (attrs.type == 'radio') {
								htmlContent = htmlContent + "<input type=\"radio\" data-xp-type=\"input.option\" name=\"" + name + "\" value=\"" + choiceList[j][0] + "\" />" + choiceList[j][1];
							} else {
								htmlContent = htmlContent + "<input type=\"checkbox\" data-xp-type=\"input.checkOption\" name=\"" + name + "\" value=\"" + choiceList[j][0] + "\" />" + choiceList[j][1];
							}
						}
						if (attrs.alignment == 'vertical') {
							htmlContent = htmlContent + "</li>";
						}
					}
					if (attrs.alignment == 'vertical') {
						htmlContent = htmlContent + "</ul>";
					}
					// Assign html visual component div element
					$(element).html(htmlContent);
					// Set render, since we have rendered visual component
					$(element).attr('data-xp-render', JSON.stringify(true));
					// Trace
					ximpia.console.log(htmlContent);					
				}
			}
			$("input[data-xp-type='input.checkOption']").click() {
				$(this).xpObjectListOption("clickCheck");
			}
		},
		clickCheck: function() {
			/*
			 * When user clicks on the option checkbox, current clicked element is unchecked and new element checked
			 */
			// 
		}
        };
		
        if ( methods[method] ) {
            return methods[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));
        } else if ( typeof method === 'object' || ! method ) {
            return methods.init.apply( this, arguments );
        } else {
            $.error( 'Method ' +  method + ' does not exist on jQuery.xpObjListOption' );
        }    
		
	};

})(jQuery);
