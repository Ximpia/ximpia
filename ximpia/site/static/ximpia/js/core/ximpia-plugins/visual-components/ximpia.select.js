/*
 * Ximpia Visual Component Input: Text, Password, etc...
 *
 */

(function($) {	

	$.fn.xpObjSelect = function( method ) {  

        // Settings		
        var settings = {
        	excudeListSelect: ['type','id','element','help_text','label','data-xp-val', 'value', 'choices','choicesId'],
        	excludeListLabel: ['type','id','element'],
        	excludeList: ['info','type']
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
		render: function(data) {
			for (var i=0; i<$(this).length; i++) {
				//console.log($(this)[i]);
				var element = $(this)[i]; 
				var idInput = $(element).attr('id').split('_comp')[0];
				var doRender = ximpia.common.Form.doRender(element, settings.reRender);
				if (doRender == true) {
					var nameInput = idInput.split('id_')[1];
					$.metadata.setType("attr", "data-xp");
					var attrs = $(element).metadata();
					var dataAttrs = data[nameInput];
					//console.log(dataAttrs);
					var type = 'text';
					var value = "";
					if (attrs.hasOwnProperty('type')) {
						type = attrs.type;
					}
					// id, name, type
					var htmlContent = "";
					if (attrs.hasOwnProperty('left')) {
						htmlContent = "<div style=\"width: " + attrs['left'] + "px; float: left; border: 0px solid\"><label for=\"" + idInput + "\"></label>:</div> <div style=\"border: 0px solid; float: left\"><select id=\"" + idInput + "\" data-xp-class=\"combobox\"  ></select></div>";
					} else {
						htmlContent = "<div style=\"float: left; border: 0px solid\"><label for=\"" + idInput + "\"></label>:</div> <div style=\"border: 0px solid; float: left; margin-left: 5px \"><select id=\"" + idInput + "\" data-xp-class=\"combobox\" ></select></div>";
					}
					$(element).html(htmlContent);
					$(element).attr('data-xp-render', JSON.stringify(true));				
					// Input
					for (attr in dataAttrs) {
						var exists = ximpia.common.ArrayUtil.hasKey(settings.excudeListSelect, attr);
						if (exists == false) {
							value = dataAttrs[attr];
							/*if (attr == 'class') {
								value = value + ' scroll';
							}
							console.log(attr + ' - ' + value);*/
							$("#" + idInput).attr(attr, value);
						}					
					}
					for (attr in attrs) {
						var exists = ximpia.common.ArrayUtil.hasKey(settings.excludeList, attr);
						if (exists == false) {
							value = attrs[attr];
							/*if (attr == 'class') {
								value = value + 'scroll';
							}*/
							$("#" + idInput).attr(attr, value);
						}					
					}				
					// Choices
					var choicesId = dataAttrs['choicesId'];
					var choices = JSON.parse($("#id_choices").attr('value'))[choicesId];
					/*console.log('choices...');
					console.log('choicesId : ' + choicesId);
					console.log(choices)*/
					for (choiceIndex in choices) {
						var htmlSelect = "<option value=\"" + choices[choiceIndex][0] + "\">" + choices[choiceIndex][1] + "</option>";
						$("#" + idInput).append(htmlSelect);
					}
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
				}				
			}
		},
		disable: function() {
			var idInput = $(this).attr('id').split('_comp')[0];
			$("#" + idInput).attr('disable', 'disable');
		},
		enable: function() {
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
