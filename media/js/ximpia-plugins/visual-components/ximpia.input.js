/*
 * Ximpia Visual Component Input: Text, Password, etc...
 *
 */

(function($) {	

	$.fn.xpObjInput = function( method ) {  

        // Settings		
        var settings = {
        	excudeListInput: ['type','id','element','help_text','label','left'],
        	excudeListInputSug: ['type','id','element','help_text','label','left','suggest'],
        	excludeListLabel: ['type','id','element'],
        	excludeList: ['info','type','left','suggest']
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
		renderField: function(data) {
			for (var i=0; i<$(this).length; i++) {
				//console.log($(this)[i]);
				var element = $(this)[i]; 
				var idInput = $(element).attr('id').split('_comp')[0];
				var nameInput = idInput.split('id_')[1];
				$.metadata.setType("attr", "data-xp");
				var attrs = $(element).metadata();
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
				// Label				
				$("label[for=\"" + idInput + "\"]").text(dataAttrs['label']);
				if (attrs.info == true) {
					$("label[for=\"" + idInput + "\"]").addClass("info");
					// help_text
					if (dataAttrs.hasOwnProperty('help_text')) {
						$("label[for=\"" + idInput + "\"]").attr('data-xp-title', dataAttrs['help_text']);
					}
				}				
				//console.log($("#" + idInput));
			}
		},
		renderTextChoice: function(data) {
			console.log('renderTextChoice...');
			for (var i=0; i<$(this).length; i++) {
				//console.log($(this)[i]);
				var element = $(this)[i]; 
				var idInput = $(element).attr('id').split('_comp')[0];
				var nameInput = idInput.split('id_')[1];
				$.metadata.setType("attr", "data-xp");
				var attrs = $(element).metadata();
				//console.log('attrs...');
				//console.log(attrs)
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
				// Input
				for (attr in dataAttrs) {
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
					var exists = ximpia.common.ArrayUtil.hasKey(settings.excludeList, attr);
					if (exists == false) {
						$("#" + idInput).attr(attr, attrs[attr]);
					}
					
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
				//console.log($("#" + idInput));
				//console.log($("#" + idInput).attr('data-xp'));
				//$('#id_jobTitle').jsonSuggest({data: $('#id_jobTitle_data').attr('value'), maxHeight: 200, minCharacters:3});
				if (attrs.hasOwnProperty('suggest')) {
					//sugAttrs = $("#" + idInput).metadata();
					sugAttrs = JSON.parse($("#" + idInput).attr('data-xp'));
					//console.log('sugAttrs');
					//console.log(sugAttrs.data);
					$("#" + idInput).jsonSuggest({	data: sugAttrs.data, 
									maxHeight: sugAttrs.maxHeight, 
									minCharacters: sugAttrs.minCharacters
								});
				}
			}
		},
		disable: function() {
			var idInput = $(this).attr('id').split('_comp')[0];
			$("#" + idInput).attr('disable', 'disable');
		},
		enable: function() {
		},
		addHidden: function(data) {
			var list = Object.keys(data);
			for (key in list) {
				if (data[list[key]]['type'] == 'hidden') {
					$("#id_variables").append("<input type=\"hidden\" id=\"id_" + list[key] + "\" name=\"" + list[key] + "\" value=\"\" />");
					$("#id_" + list[key]).attr('value', data[list[key]]['value']);
				}				
			}
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
