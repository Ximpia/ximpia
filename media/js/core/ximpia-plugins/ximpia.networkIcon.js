/*
 * Ximpia Social Network Icon
 *
 */

(function($) {
	
	$.fn.xpSocialNetworkIcon = function( method ) {  

        // Settings		
        var settings = {
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
            click : function() {
				var width = 750;
				var height = 450;
                var wleft = (screen.width - width) / 2;
                var wtop = (screen.height - height) / 2;
				var dataId = $(this).attr('id') + '_data';
				var dataStr = $("#" + dataId).attr('value');
				// Errors ????
				var data = JSON.parse(dataStr);
				var windowUrl = data[0].windowUrl;
				window.open(windowUrl, "oauthWin", "width=" + width + "px, height=" + height + "px, top=" + wtop + "px, left=" + wleft + "px");
			},
            changeStatusOK : function() { 
			     var sId = $(this).attr('id');
				 var service = sId.split('_')[1].split('Icon')[0]
				 var sIdStatus = 'id_' + service + 'Status';
				 $("#" + sIdStatus).addClass('IconStatusOK');
				 $("#" + sIdStatus).removeClass('IconStatusERROR');
				 $("#" + sId).unbind('mouseover');
				 $("#" + sId).unbind('mouseout');
				 $("#" + sId).unbind('click');
				 $("#" + sId).removeClass('Icon');
				 $("#" + sId).addClass('IconUsed');
				 $("#" + sIdStatus).css('visibility', 'visible');
			},
            changeStatusERROR : function() {
                 var sId = $(this).attr('id');
                 var service = sId.split('_')[1].split('Icon')[0]
                 var sIdStatus = 'id_' + service + 'Status';
                 $("#" + sIdStatus).addClass('IconStatusERROR');
                 $("#" + sIdStatus).removeClass('IconStatusOK');
                 $("#" + sIdStatus).css('visibility', 'visible');
			}
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
