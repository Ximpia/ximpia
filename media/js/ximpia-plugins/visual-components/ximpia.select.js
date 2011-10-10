/*
 * Ximpia Visual Component Input: Text, Password, etc...
 *
 */

(function($) {	

	$.fn.xpObjSelect = function( method ) {  

        // Settings		
        var settings = {
        	excudeListSelect: ['type','id','element','help_text','label','data-xp-val', 'value', 'choices'],
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
					htmlContent = "<div style=\"width: " + attrs['left'] + "px; float: left\"><label for=\"" + idInput + "\"></label>:</div> <select id=\"" + idInput + "\" ></select>";
				} else {
					htmlContent = "<label for=\"" + idInput + "\"></label>: <select id=\"" + idInput + "\" ></select>";
				}
				$(element).html(htmlContent);				
				// Input
				for (attr in dataAttrs) {
					var exists = ximpia.common.ArrayUtil.hasKey(settings.excudeListSelect, attr);
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
				// Choices
				for (choiceIndex in dataAttrs.choices) {
					var htmlSelect = "<option value=\"" + dataAttrs.choices[choiceIndex][0] + "\">" + dataAttrs.choices[choiceIndex][1] + "</option>";
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
				//console.log($("#" + idInput));				
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
