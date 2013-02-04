/** * Render external objects using javascript: Used for facebook login button, recaptcha, etc... * */(function($) {		$.fn.xpRenderExt = function( method ) {          // Settings		        var settings = {        	reRender: false        };                var methods = {		init : function( options ) {                 	return this.each(function() {                    		// If options exist, lets merge them                    		// with our default settings                    		if ( options ) {	                        	$.extend( settings, options );                    		}                	});		},		render : function( xpForm ) {			/**			 * Render javascript functions			 */			for (var i=0; i<$(this).length; i++) {				var element = $(this)[i];				if (typeof $(element).attr('data-xp-render') == 'undefined') {					ximpia.console.log('plugin renderext :: data-xp-render => blank ' + $(element).attr('id'));					$(element).attr('data-xp-render', '');				}				var doRender = ximpia.common.Form.doRender(element, settings.reRender);				if (doRender == true) {					$.metadata.setType("attr", "data-xp");					var attrs = $(element).metadata();					attrs.element = $(element);					eval(attrs.functionName)(attrs, function(attrs) {						$(attrs.element).attr('data-xp-render', JSON.stringify(true));						ximpia.console.log('plugin renderext :: render true ' + $(attrs.element).attr('id'));						ximpia.console.log(attrs);					});				}			}		}        };		        if ( methods[method] ) {            return methods[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));        } else if ( typeof method === 'object' || ! method ) {            return methods.init.apply( this, arguments );        } else {            $.error( 'Method ' +  method + ' does not exist on jQuery.xpObjRenderExt' );        }    			};})(jQuery);