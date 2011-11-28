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
			var data = JSON.parse(sessionStorage.getItem("xpForm"));
			//var container = $("#id_groupTags").xpContainer({limit: 10, 
									//doKey: true, 
									//args: {idText: 'id_organizationGroupTags', button: 'BtAddTag'}});
			//container.xpContainer('addTag');
			console.log('render fields...');
			//console.log($(this));
			for (var i=0; i<$(this).length; i++) {
				//console.log($(this)[i]);
				var element = $(this)[i];
				console.log('element : ' + element); 
				var idBase = $(element).attr('id').split('_comp')[0];
				console.log('idBase : ' + idBase);
				var name = idBase.split('id_')[1];
				var nameInput = name + 'Input';
				var nameList = name + 'ListValue';
				$.metadata.setType("attr", "data-xp");
				var attrs = $(element).metadata();
				var dataInputAttrs = data[nameInput];
				var dataListAttrs = data[nameList];
				console.log('attrs....');
				console.log(attrs);
				console.log('dataInputAttrs....');
				console.log(dataInputAttrs);
				console.log('dataListAttrs....');
				console.log(dataListAttrs);
				/*var type = 'text';
				if (attrs.hasOwnProperty('type')) {
					type = attrs.type;
				}*/
				// id, name, type
				var htmlContent = "";
				htmlContent = htmlContent + "<div id=\"" + idBase + 'Input_comp' + "\" data-xp-type=\"text.autocomplete\" data-xp=\"{info: true, left: 145}\" style=\"float: left\" ></div>";
				htmlContent = htmlContent + "<div style=\"float: left\"><a href=\"#\" class=\"buttonIcon buttonIconSmall\" onclick=\"return false;\" data-xp-type=\"button.field\" data-xp=\"{input: id_organizationGroupTags_comp}\" >Add</a></div>";
				htmlContent = htmlContent + "<div id=\"" + idBase + "Show\" class=\"listContainer\" style=\"width: 300px; margin-left: 15px; margin-top: 10px\" ></div>";
				htmlContent = htmlContent + "<input type=\"hidden\" name=\"" + nameList + "\" id=\"" + idBase + "ListValue\" value=\"\" />";
				$(element).html(htmlContent);
			}			
			
			// Bind click event to add button
			/*$("[data-xp-type='button.field']").click(function() {
			});*/
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
