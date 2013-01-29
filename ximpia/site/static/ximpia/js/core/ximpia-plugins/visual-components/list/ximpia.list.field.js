/*
 * List of fields. Fields can be added, deleted. Will represent the many-to-many relationships in models
 * 
 * TODO: Include the html for component
 *
 */

(function($) {	

	$.fn.xpObjListField = function( method ) {  

        // Settings		
        var settings = {
        	excudeListSelect: ['type','id','element','help_text','label','data-xp-val', 'value', 'choices','choicesId'],
        	excludeListLabel: ['type','id','element'],
        	excludeList: ['info','type']
        };
        
        var addField = function(inputField, feedType, choicesId) {
        	ximpia.console.log('addField...');
        	ximpia.console.log('inputField: ' + inputField + ' feedType: ' + feedType);
        	var inputDataId = inputField.split('_comp')[0];
        	if (feedType == 'input') {
        		var idBase = inputField.split('Input_comp')[0];
			var data = $("#" + inputDataId).prop('value');
			var dataId = data
        	} else if (feedType == 'select') {
        		var idBase = inputField.split('Select_comp')[0];
        		var dataId = $("#" + inputDataId).prop('value');
        		// Get from choices data
        		var choiceList = JSON.parse($('#id_choices').attr('value'))[choicesId];
        		for (j in choiceList) {
        			if (choiceList[j][0] == dataId) {
        				data = choiceList[j][1];
        			}
        		}
        	}				
		ximpia.console.log('data: ' + data + ' dataId: ' + dataId)	
		var idBaseList = idBase + 'ListValue';
		ximpia.console.log('idBaseList: ' + idBaseList);
		var obj = new ximpia.visual.GenericComponentData();
		obj.init(idBaseList);
		var hasElement = obj.hasElement(dataId);
		var size = obj.getSize();
		var idTag = idBase + '_' + size;
		var idTagClick = idBase + '_click_' + size;
		var idTagDel = idBase + '_del_' + size;
		validate = false;
		if (dataId != '' && size < settings.limit && hasElement == false) {
			validate = true;
		}
		ximpia.console.log('validate: ' + validate);				
		if (validate == true) {
			var sHtml = '<div id="' + idTag + '" class="listField"><div id="' + idTagClick + '" class="listFieldText">' + data + '</div><div class="listFieldSep">&nbsp;</div><div id="' + idTagDel + '" class="listFieldDel">X</div></div>';
			ximpia.console.log(sHtml);
			$('#' + idBase + 'Show').append(sHtml);
			var tagObj = new Object();
			tagObj.id = size;
			tagObj.text = dataId;
			obj.addDataEnd(tagObj);
			if (feedType == 'input') {
				$('#' + inputDataId).prop('value', '');
				$('#' + inputDataId).focus();
			} else if (feedType == 'select') {
				$('#' + idBase + 'Select_input').prop('value', '');
			}

			// Remove Field Bind
			$('#' + idTagDel).click(function() {
				var idElementDel = $(this).attr('id');
        			var idElement = idElementDel.replace('_del','');
        			var list = idElement.split('_');
				var index = list[list.length-1];
        			$('#' + idElement).remove();
        			obj.deleteData(index);
        			// Logic when field is deleted
        			// TODO: Define how to call to logic, n function with arguments, etc....
        			/*if (oArg.callBack) {
	        			oArg.callBack(oArg);
        			}*/
				$('#' + inputDataId).focus();
			});
		} else if (size >= settings.limit) {
			// TODO: Show a fancy messahe window
			alert('Can´t include more fields to the list');
		}
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
			
			/*
			 * {	limit: 10, 
			 * 	doKey: true, 
			 * 	args: {
			 * 		idText: 'id_organizationGroupTags', 
			 * 		button: 'BtAddTag'
			 * 		}
			 * 	}
			 */
			
			ximpia.console.log('render fields...');
			//ximpia.console.log($(this));
			for (var i=0; i<$(this).length; i++) {
				//ximpia.console.log($(this)[i]);
				var element = $(this)[i];
				ximpia.console.log('element : ' + element); 
				var idBase = $(element).attr('id').split('_comp')[0];
				ximpia.console.log('idBase : ' + idBase);
				var doRender = ximpia.common.Form.doRender(element, settings.reRender);
				if (doRender == true) {
					var name = idBase.split('id_')[1];
					var nameInput = name + 'Input';
					var nameSelect = name + 'Select';
					var nameList = name + 'ListValue';
					$.metadata.setType("attr", "data-xp");
					var attrs = $(element).metadata();
					var dataInputAttrs = data[nameInput];
					var dataSelectAttrs = data[nameSelect];
					var dataListAttrs = data[nameList];
					ximpia.console.log('attrs....');
					ximpia.console.log(attrs);
					ximpia.console.log('dataInputAttrs....');
					ximpia.console.log(dataInputAttrs);
					ximpia.console.log('dataInputAttrs....');
					ximpia.console.log(dataSelectAttrs);
					ximpia.console.log('dataSelectAttrs....');
					ximpia.console.log(dataListAttrs);
					/*var type = 'text';
					if (attrs.hasOwnProperty('type')) {
						type = attrs.type;
					}*/
					// id, name, type
					var inType = attrs.inType;
					if (inType == "input") {
						var htmlContent = "";
						htmlContent = htmlContent + "<div id=\"" + idBase + 'Input_comp' + "\" data-xp-type=\"text.autocomplete\" data-xp=\"{info: true, left: 145}\" style=\"float: left\" data-xp-related=\"list.field\" ></div>";
						htmlContent = htmlContent + "<div style=\"float: left\"><a href=\"#\" class=\"buttonIcon buttonIconSmall\" onclick=\"return false;\" data-xp-type=\"button.field\" data-xp=\"{input: " + idBase + "Input_comp, type: 'input'}\" >Add</a></div>";
						htmlContent = htmlContent + "<div id=\"" + idBase + "Show\" class=\"listContainer\" style=\"width: 300px; margin-left: 15px; margin-top: 4px\" ></div><div style='clear:both'></div>";
						htmlContent = htmlContent + "<input type=\"hidden\" name=\"" + nameList + "\" id=\"" + idBase + "ListValue\" value=\"\" />";
					} else if (inType == "select") {
						var htmlContent = "";
						htmlContent = htmlContent + "<div id=\"" + idBase + 'Select_comp' + "\" data-xp-type=\"list.select\" data-xp=\"{left: 85, info: true}\" style=\"float: left\" data-xp-related=\"list.field\" ></div>";
						htmlContent = htmlContent + "<div style=\"float: left\"><a href=\"#\" class=\"buttonIcon buttonIconSmall\" onclick=\"return false;\" data-xp-type=\"button.field\" data-xp=\"{input: " + idBase + "Select_comp, type: 'select', choicesId: '" + dataSelectAttrs.choicesId + "'}\" >Add</a></div>";
						htmlContent = htmlContent + "<div id=\"" + idBase + "Show\" class=\"listContainer\" style=\"width: 300px; margin-left: 15px; margin-top: 4px\" ></div><div style='clear:both'></div>";
						htmlContent = htmlContent + "<input type=\"hidden\" name=\"" + nameList + "\" id=\"" + idBase + "ListValue\" value=\"\" />";
					}
					$(element).html(htmlContent);
					$(element).attr('data-xp-render', JSON.stringify(true));
					$(element).css('clear', 'both');
					ximpia.console.log('field list html...');
					ximpia.console.log(htmlContent);
				}				
			}			
			// Bind click event to add button
			$("[data-xp-type='button.field']").click(function() {
				var attrsButton = $(this).metadata();
				var inputField = attrsButton['input'].id;
				ximpia.console.log('inputField: ' + inputField);
				var feedType = attrsButton['type'];
				ximpia.console.log('feedType: ' + feedType);
				var choicesId = "";
				if (attrsButton.hasOwnProperty('choicesId')) {
					choicesId = attrsButton['choicesId'];
					ximpia.console.log('choicesId: ' + choicesId);
				}
				addField(inputField, feedType, choicesId);
			});
		},
		bindKeyPress: function() {
			for (var i=0; i<$(this).length; i++) {
				var element = $(this)[i];
				$(element).keypress(function(e) {
					if (e.which == 13) {
						var inputField = e.currentTarget.id + '_comp';
						ximpia.console.log('inputField: ' + inputField);
                				addField(inputField, 'input');
					}
				});
			}			
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
