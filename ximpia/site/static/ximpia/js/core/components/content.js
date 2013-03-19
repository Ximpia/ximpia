
/*
 * 
 * 
 * Copyright 2013 Ximpia, Inc
 * 
 *    Licensed under the Apache License, Version 2.0 (the "License");
 *    you may not use this file except in compliance with the License.
 *    You may obtain a copy of the License at
 * 
 *        http://www.apache.org/licenses/LICENSE-2.0
 * 
 *    Unless required by applicable law or agreed to in writing, software
 *    distributed under the License is distributed on an "AS IS" BASIS,
 *    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *    See the License for the specific language governing permissions and
 *    limitations under the License. 
 * 
 * 
 */

/*
 * Content
 * 
 * ** HTML **
 * 
 * <a href="{{object.url}}" title="{{object.title}}" data-xp-type="content" >{{object.title}}</a>
 * 
 * 
 * ** Methods **
 * 
 * * render
 *  
 */

(function($) {	

	$.fn.xpContent = function( method ) {  

        // Settings		
        var settings = {
        };
        var vars = {
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
		/*
		 * Render content
		 */
		render : function() {		
			ximpia.console.log('xpContent :: render...');
			for (var i=0; i<$(this).length; i++) {
				ximpia.console.log($(this)[i]);
				vars.element = $(this)[i];
				vars.doRender = ximpia.common.Form.doRender(vars.element, settings.reRender);
				if (vars.doRender == true) {
					// Process content
					ximpia.console.log('xpContent :: content: '+ $(vars.element).html());
					$(vars.element).html(ximpia.common.Content.replaceFields($(vars.element).html()));
					ximpia.console.log('xpContent :: content new: '+ $(vars.element).html());
					// Process attributes
					var attrs = vars.element.attributes;
					for (var j=0; j<Object.keys(attrs).length; j++) {
						ximpia.console.log('xpContent :: attr: '+ attrs[j]);						
						if (typeof attrs[j] != 'undefined') {
							ximpia.console.log('xpContent :: attr value: '+ attrs[j].value);
							attrs[j].value = ximpia.common.Content.replaceFields(attrs[j].value);
							ximpia.console.log('xpContent :: attr new value: '+ attrs[j].value);
						}
					}
					$(vars.element).attr('data-xp-render', JSON.stringify(true));
				}
			}
		}
        };
		
        if ( methods[method] ) {
            return methods[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));
        } else if ( typeof method === 'object' || ! method ) {
            return methods.init.apply( this, arguments );
        } else {
            $.error( 'Method ' +  method + ' does not exist on jQuery.xpContent' );
        }    
		
	};

})(jQuery);
