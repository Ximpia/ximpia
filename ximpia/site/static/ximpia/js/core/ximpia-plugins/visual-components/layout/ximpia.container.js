/*
 * Container
 * 
 * Group set of visual components in a block.
 * 
 * Supports conditions. You can place your visual objects inside containers to force condition for rendering.
 * 
 * Conditions are defined in the view definitions with attribute ``data-xp-cond-rules``, like:
 * 
 * ```
 * <div 	id="id_view" 
 * 		data-xp="{viewName: 'signup'}" 
 * 		data-xp-cond-rules="{hasUserAuth: 'settings.SIGNUP_USER_PASSWORD == true', hasNetAuth: 'settings.SIGNUP_SOCIAL_NETWORK == true', socialNetLogged: 'socialNetLogged == true'}" >
 * </div>```
 * 
 * Then we define condition for the container, like:
 * 
 *  ```<div id="id_passwordAuth" data-xp-type="container" data-xp-cond="{conditions: [{condition: 'socialNetLogged', render: false}]}" >
 *  ...your objects...
 *  </div>```
 * 
 * ** Attributes**
 * 
 * * ``data-xp-type`` : container
 * * ``data-xp-cond``:ListType : Condition objects, like [{}, {}, ...] First matched condition will execute action
 * 		* ``conditions``:ListType : List of conditions:
 * 			* ``condition`` : condition key from ``data-xp-cond-rules``
 * 			* ``action`` : Supported values: 'render'
 * 			* ``value``:Boolean : true / false
 * 
 */

(function($) {	

	$.fn.xpObjContainer = function( method ) {  

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
		render: function(xpForm) {
			ximpia.console.log('xpObjContainer :: render...');
			var data = ximpia.common.Browser.getFormDataFromSession(xpForm);
			ximpia.console.log(data);
			// Get condition rules and Eval conditions and built evals 
			$.metadata.setType("attr", "data-xp-cond-rules");
			var conditionRules = $("#id_view").metadata();
			var evals = {};
			for (conditionRule in conditionRules) {
				var checkCondition = ximpia.common.Condition.eval(conditionRules[conditionRule]);
				evals[conditionRule] = checkCondition;
			}
			ximpia.console.log('xpObjContainer :: evals...');
			ximpia.console.log(evals);
			for (var i=0; i<$(this).length; i++) {
				var element = $(this)[i];
				ximpia.console.log('xpObjContainer :: Element ' + $(element).attr('id'));
				var idInput = $(element).attr('id').split('_comp')[0];
				var doRender = ximpia.common.Form.doRender(element, settings.reRender);
				if (doRender == true) {
					// Will set render to false to all components inside
					// data-xp-render
					ximpia.console.log('xpObjContainer :: doRender: ' + doRender);
					var nameInput = idInput.split('id_')[1];
					$.metadata.setType("attr", "data-xp-cond");
					var conditions = $(element).metadata();
					ximpia.console.log('xpObjContainer :: conditions...');
					ximpia.console.log(conditions);
					if (conditions.hasOwnProperty('conditions')) {
						for (var c=0; c<conditions['conditions'].length; c++) {
							var condition = conditions['conditions'][c];
							ximpia.console.log('xpObjContainer :: condition: ' + condition);
							if (condition.action == 'render') { 
								if (condition.value == true && evals[condition.condition] == true) {
									$(element).css('display', 'block');
								} else {
									$(element).css('display', 'none');
								}
							}
						}
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
            $.error( 'Method ' +  method + ' does not exist on jQuery.xpObjContainer' );
        }
	};

})(jQuery);
