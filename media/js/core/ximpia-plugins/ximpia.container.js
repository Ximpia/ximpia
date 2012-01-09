/*
 * Container : Tags, Lists. User can add local data
 *
 */

(function($) {
	
	$.fn.xpContainer = function( method ) {  

        // Settings		
        var settings = {
			limit: 10,
			doKey: true,
			args: {}
        };
		
        var methods = {
            init : function( options ) { 
                return this.each(function() {        
                    // If options exist, lets merge them
                    // with our default settings
                    if ( options ) { 
                        settings = $.extend( settings, options );
						$(this).prop('settings', settings);
                    }
                });
			},
            addTag : function() {
				function doAdd(oArg) {
					var text = $('#' + oArg.idText).prop('value');
					var obj = new GenericComponentData(oArg.idData);
					var size = obj.getSize();
					var idTag = oArg.idContainer + '_' + size;
					var idTagClick = oArg.idContainer + '_click_' + size;
					var idTagDel = oArg.idContainer + '_del_' + size;
					var hasElement = obj.hasElement(text);
					var validate = false;
					if (text != '' && size < settings.limit && hasElement == false) {
						validate = true;
					}
					//alert(validate);
					if (validate == true) {
						var sHtml = '<div id="' + idTag + '" class="tag"><div id="' + idTagClick + '" class="tagTextAdd">' + text + '</div><div class="tagSep">&nbsp;</div><div id="' + idTagDel + '" class="tagDel">X</div></div>';
						$('#' + oArg.idContainer).append(sHtml);
						var tagObj = new Object();
						tagObj.id = size;
						tagObj.text = text;
						obj.addDataEnd(tagObj);
						$('#' + oArg.idText).prop('value', '');
						$('#' + oArg.idText).focus();
						// Delete Event
						$('#' + idTagDel).click(function() {
							deleteFromList($(this), oArg);
							$('#' + oArg.idText).focus();
						});
					}
				}
				settings = $(this).prop('settings');
				settings.args.idContainer = $(this).attr('id');
				settings.args.idData = $(this).attr('id') + '_data';
				if (settings.doKey == true) {
                	$("#" + settings.args.idText).keypress(function(e) {
	                    if (e.which == 13) {
							doAdd(settings.args);
                    	}
                	}); 					
				}
                $("#" + settings.args.button).click(function() {
					doAdd(settings.args);
                });
                $('#' + settings.args.idText).focus();
			}
        };
				
        if ( methods[method] ) {
            return methods[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));
        } else if ( typeof method === 'object' || ! method ) {
            return methods.init.apply( this, arguments );
        } else {
            $.error( 'Method ' +  method + ' does not exist on jQuery.xpContainer' );
        }    
		
	};

})(jQuery);
