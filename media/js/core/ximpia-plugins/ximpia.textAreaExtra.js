/*
 * Ximpia TextArea Extra
 *
 */

(function($) {
	
	$.fn.xpTextAreaExtra = function( options ) {  

        // Settings
        var settings = {
			'maxLimit' : 144,
			'maxHeight' : 150,
        };		
	   
        if ( options ) { 
            $.extend( settings, options );
        }

        var setCSS = function(which){
            // Init the div for the current textarea
            $("#" + id).css({
                'position':'absolute',
                'top': -10000,
                'left': -10000,
                'width': $(which).width()-20,
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
            theValue = $(which).attr('value') || "";
            theValue = theValue.replace(/\n/g,'<br />');
            $("#" + id).html(theValue + '<br />');
			$(which).height($("#" + id).height());						
        };              

        var id = $(this).attr('id') + '_hidden';
        $('body').append('<div id="' + id + '"></div>');
        $(this).css({
            'overflow':'hidden'
        })
        .bind('keyup',function(){
			var size = $(this).attr('value').length;
            //var height = $(this).css('height');
            //var iHeight = parseInt(height.split('px')[0]);
			//if ($(this).height() < settings.maxHeight) {
                if (size < settings.maxLimit) {
                    copyContent($(this));
					if ($(this).hasClass('error')) {
						$(this).removeClass('error');
						$(this).addClass('valid');
					}
                } else {
                    copyContent($(this));
					$(this).addClass('error');
					if ($(this).hasClass('valid')) {
						$(this).removeClass('valid');
					}
                }
			//}
        });
        // Make sure all the content in the textarea is visible
        setCSS(this);
        copyContent($(this));
	$(this).height($("#" + id).height());		
        /*if ($(this).height() > settings.maxHeight) {
                $(this).css({
                    'overflow-y': 'scroll',
                    'height': settings.maxHeight
                });
        } else {
			$(this).height($("#" + id).height());
		}*/
	};
})(jQuery);
