/*
 * Ximpia Social Network Icon
 *
 */

(function($) {
	
	$.fn.xpTagContainer = function( method ) {  

        // Settings		
        var settings = {
			'addLimit' : 10
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
            add : function(text) {
				var sId = $(this).attr('id');
				var idText = text.toLowerCase();
				var len = $(this).children().length;
				// Get list of objects
				// Generate hasTag, comparing obj.text to text
				//var obj = new GenericComponentData('id_groupTags_data');
				var dataDictList = JSON.parse($("#" + 'id_groupTags_data').attr('value'));
				var list = dataDictList[1].data;
				var hasTag = false;
				for (var i = 0; i<list.length ; i++) {
					alert(list[i].text + ' ' + text);
					if (list[i].text == text) {
						hasTag = true;
					}
				}
				alert(hasTag);
				var sTagId = sId + '_' + len;
				if (text != '' && len < settings.addLimit && hasTag == false) {
					var sHtml = '<div id="' + sTagId + '" class="tag"><div class="tagTextAdd">' + text + '</div><div class="tagSep">&nbsp;</div><div class="tagDel">X</div></div>';
					$(this).append(sHtml);
					var obj = new Object();
					obj.id = len+1;
					obj.text = text;
					dataDictList[1].data.push(obj);
				}
			},
        };
		
        if ( methods[method] ) {
            return methods[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));
        } else if ( typeof method === 'object' || ! method ) {
            return methods.init.apply( this, arguments );
        } else {
            $.error( 'Method ' +  method + ' does not exist on jQuery.xpSocialNetworkIcon' );
        }    
		
	};

})(jQuery);
