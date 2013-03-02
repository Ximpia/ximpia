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
 * * ``title`` : Tooltip to show when mouse is placed over image.
 * * ``version`` [optional] : Version to generate url for image versions. In case to include version you need no ``dimensions``attribute. 
 * 								Dimensions from version will be used.
 * 
 *
 */


(function($) {	

	$.fn.xpImage = function( method ) {  

        // Settings		
        var settings = {
        	htmlAttrs: ['tabindex','readonly','maxlength','class','value','name','autocomplete','size','style'],
        };
        var templates = {
        	main: '<img id="{{id}}" src="{{src}}" />'
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
			for (var i=0; i<$(this).length; i++) {
				ximpia.console.log($(this)[i]);
				var element = $(this)[i]; 
				var idElement = $(element).attr('id').split('_comp')[0];
				var nameElement = idElement.split('id_')[1];
				var doRender = ximpia.common.Form.doRender(element, settings.reRender);
				if (doRender == true) {
					ximpia.console.log('renderField :: id: ' + $(element).attr('id'));
					$.metadata.setType("attr", "data-xp");
					var attrs = $(element).metadata();
					ximpia.console.log('xpImage :: attrs...')
					ximpia.console.log(attrs);
					$(element).html("<img id=\"" + idElement + "\" />");
					// Build src
					if (attrs.hasOwnProperty('src')) {
						$('#' + idElement).attr('src', attrs.src);
					} else {
						var src="";
						if (attrs.hasOwnProperty('hostLocation') && 
								ximpia.settings.static.hostLocations.hasOwnProperty(attrs['hostLocation'])) {
							src += ximpia.settings.static.hostLocations[attrs['hostLocation']];
						} else {
							src += ximpia.settings.static.hostLocations['default'];
						}
						if (attrs.hasOwnProperty('location') && ximpia.settings.static.locations.hasOwnProperty(attrs['locations'])) {
							src += ximpia.settings.static.locations[attrs['locations']];
						} else {
							src += ximpia.settings.static.locations['images'];
						}
						if (attrs.hasOwnProperty('version')) {
							var fileFields = attrs['file'].split('.');
							var fileName = fileFields.slice(0, fileFields.length-1).join('.');
							src += fileName + '_' + attrs['version'] + '.' + fileFields[fileFields.length-1];
						} else {
							src += attrs['file'];							
						}
						$('#' + idElement).attr('src', src);
					}
					// Build title
					if (attrs.hasOwnProperty('title')) {
						$('#' + idElement).attr('title', attrs.title);
						$('#' + idElement).attr('alt', attrs.title);
					} else {
						$('#' + idElement).attr('title', 'Image');
						$('#' + idElement).attr('alt', 'Image');
					}
					// Process attributes					
					var dataAttrs = {};
					ximpia.common.Form.doAttributes({
						djangoAttrs: [],
						htmlAttrs: settings.htmlAttrs,
						excludeList: [],
						dataAttrs: dataAttrs,
						attrs: attrs,
						idElement: idElement
					});
					// Dimensions for version in case no defined by styles
					if ((attrs.hasOwnProperty('style') && attrs['style'].indexOf('width') == -1 && attrs.hasOwnProperty('version')) ||
							(!attrs.hasOwnProperty('style') && attrs.hasOwnProperty('version'))) {
						$('#' + idElement).css('width', ximpia.settings.imageVersions[attrs['version']].width + 'px');
					}
				}
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
