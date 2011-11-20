/*
 * List of fields. Fields can be added, deleted. Will represent the many-to-many relationships in models
 *
 */

(function($) {	

	$.fn.xpObjListField = function( method ) {  

        // Settings		
        var settings = {
        	excudeListSelect: ['type','id','element','help_text','label','data-xp-val', 'value', 'choices','choicesId'],
        	excludeListLabel: ['type','id','element'],
        	excludeList: ['info','type'],
        	formData: {},
        	limit: 20
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
		render: function() {			
			//var container = $("#id_groupTags").xpContainer({limit: 10, 
									//doKey: true, 
									//args: {idText: 'id_organizationGroupTags', button: 'BtAddTag'}});
			//container.xpContainer('addTag');
			console.log('render fields...');
			
			
			
			
			// Bind click event to add button
			$("[data-xp-type='button.field']").click(function() {
			});
		},
		add: function() {
		},
		remove: function() {
			// Probably we will not need it
		}
        };
		
        if ( methods[method] ) {
            return methods[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));
        } else if ( typeof method === 'object' || ! method ) {
            return methods.init.apply( this, arguments );
        } else {
            $.error( 'Method ' +  method + ' does not exist on jQuery.xpObjListField' );
        }    
		
	};

})(jQuery);
