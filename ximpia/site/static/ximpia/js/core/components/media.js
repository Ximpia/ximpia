/*
 * Renders into ``img`` html element.
 * 
 * ``src`` html attribute is generated using attributes ``file``, ``location`` and ``hostLocation``. Only required attribute is ``file``. You
 * can define ``src`` attribute with full path for images. 
 * 
 * ** HTML **
 * 
 * Using images location and default host location:
 * <div id="id_myImage_comp" data-xp-type="image" data-xp="{file: 'github-icon-source.jpg'}" > </div>
 * 
 * Using S3 host location.
 * <div id="id_myImage_comp" data-xp-type="image" data-xp="{file: 'github-icon-source.jpg', hostLocation: 'S3'}" > </div>
 * 
 * Using cloudfont host location:
 * <div id="id_myImage_comp" data-xp-type="image" data-xp="{file: 'github-icon-source.jpg', hostLocation: 'cloudfront'}" > </div>
 * 
 * Using src:
 * <div id="id_myImage_comp" data-xp-type="image" data-xp="{src: 'https://ximpia.s3.amazonaws.com/images/github-icon-source.jpg'}" > </div>
 * 
 * ** Attributes **
 * 
 * * ``file`` : Phisical file name with extension, like ``myphoto.png``. In case version attribute is defined, phisical file name will
 * 				be modified to include version in the url. In case src is defined, this field is not required.
 * * ``location`` [optional] : Location name. Locations are mapped into settings.js file. In case no location is defined, we use
 * 								``images`` location. Locations are mapped into paths.
 * * ``src`` [optional] : In case you want to define path instead of location. In case you have path, you don't need attributes
 * 							file, location or hostLocation.
 * * ``hostLocation`` [optional] : Host location mapping to use. You can define in settings alternate host location for your images, like
 * 									ximpia.settings.hostLocations['S3'] = 'https://ximpia.s3.amazonaws.com/'. In case not defined, will
 * 									use the default host location. This way for images can point to S3, local, cloudfront, etc...
 * * ``title`` [optional] : Tooltip to show when mouse is placed over image.
 * * ``version`` [optional] : Version to generate url for image versions. In case to include version you need no ``dimensions``attribute. 
 * 								Dimensions from version will be used.
 * * ``dimensions`` [optional] :List<width, height> : Dimensions for image, like [40,60] Dimensions will be converted to pixels (px)
 * 
 *
 */

(function($) {	

	$.fn.xpImage = function( method ) {  

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
		render : function(xpForm) {
			ximpia.console.log('image :: render...');
			//var data = ximpia.common.Browser.getFormDataFromSession(xpForm);
			//ximpia.console.log(data);
			for (var i=0; i<$(this).length; i++) {
				ximpia.console.log($(this)[i]);
				var element = $(this)[i]; 
				var idElement = $(element).attr('id').split('_comp')[0];
				var nameElement = idInput.split('id_')[1];
				var doRender = ximpia.common.Form.doRender(element, settings.reRender);
				alert(doRender);
				if (doRender == true) {
					ximpia.console.log('renderField :: id: ' + $(element).attr('id'));
				}
		}
        };
		
        if ( methods[method] ) {
            return methods[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));
        } else if ( typeof method === 'object' || ! method ) {
            return methods.init.apply( this, arguments );
        } else {
            $.error( 'Method ' +  method + ' does not exist on jQuery.xpImage' );
        }    
		
	};

})(jQuery);
