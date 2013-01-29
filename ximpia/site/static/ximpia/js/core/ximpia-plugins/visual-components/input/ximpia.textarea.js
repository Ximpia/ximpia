/*
 * Ximpia Visual Component TextArea
 * 
 * TODO: Include the html for component
 *
 */

(function($) {	

	$.fn.xpObjTextArea = function( method ) {  

        // Settings		
        var settings = {
        	excudeListInput: ['type','id','element','help_text','label','left'],
        	excudeListInputSug: ['type','id','element','help_text','label','left'],
        	excludeListLabel: ['type','id','element'],
        	excludeList: ['info','type','left'],
		'maxLimit' : 144,
		'maxHeight' : 150
        };
                
        var setCSS = function(which){
        	// Init the div for the current textarea
        	var id = which.attr('id') + '_hidden';
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
        	var id = which.attr('id') + '_hidden';
        	theValue = $(which).val() || "";
        	theValue = theValue.replace(/\n/g,'<br />');
        	$("#" + id).html(theValue + '<br />');
        	$(which).height($("#" + id).height());						
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
			console.log('textarea render....');
			var data = ximpia.common.Browser.getFormDataFromSession(xpForm);
			//var data = JSON.parse(sessionStorage.getItem("xpForm"));
			console.log($(this));
			console.log('Elements : ' + $(this).length);
			for (var i=0; i<$(this).length; i++) {
				console.log($(this)[i]);
				var element = $(this)[i];
				var idInput = $(element).attr('id').split('_comp')[0];
				var nameInput = idInput.split('id_')[1];
				var doRender = ximpia.common.Form.doRender(element, settings.reRender);
				if (doRender == true) {
					$.metadata.setType("attr", "data-xp"); 
					var attrs = $(element).metadata();
					var dataAttrs = data[nameInput];
					console.log('idInput: ' + idInput);
					console.log('nameInput: ' + nameInput)
					console.log('*** text area data : dataAttrs ***');
					console.log(dataAttrs);
					console.log('*** text area data : attrs ***');
					console.log(attrs);
					var htmlContent = "";
					htmlContent += "<div><label for=\"" + idInput + "\"></label>: ";
					htmlContent += "<textarea id=\"" + idInput + "\"/> </div>";
					//htmlContent += "<td valign=\"bottom\" style=\"width: 30px\"><span id=\"\" class=\"textAreaCounter\" style=\" font-size:90%; position:relative; top: 7px\"></span></td></tr></table>";
					$(element).html(htmlContent);
					$(element).attr('data-xp-render', JSON.stringify(true));
					// Input
					for (attr in dataAttrs) {
						var exists = ximpia.common.ArrayUtil.hasKey(settings.excudeListInput, attr);
						if (exists == false) {
							$("#" + idInput).attr(attr, dataAttrs[attr]);
						}					
					}				
					// Label
					$("label[for=\"" + idInput + "\"]").text(dataAttrs['label']);
					if (attrs.info == true) {
						$("label[for=\"" + idInput + "\"]").addClass("info");
						// help_text
						if (dataAttrs.hasOwnProperty('help_text')) {
							$("label[for=\"" + idInput + "\"]").attr('data-xp-title', dataAttrs['help_text']);
						}
					}
					var textarea = $("#" + idInput);
        				var id = textarea.attr('id') + '_hidden';
        				$('body').append('<div id="' + id + '"></div>');
					console.log('textarea...');
					console.log(textarea);      			
        				textarea.css({
	            				'overflow':'hidden'
        				})
        				.bind('keyup',function(){
        					//console.log('writing...');
						var size = textarea.val().length;
                				if (size < settings.maxLimit) {
	                    				copyContent(textarea);
							if (textarea.hasClass('error')) {
								textarea.removeClass('error');
								textarea.addClass('valid');
							}
                				} else {
		                    			copyContent(textarea);
							textarea.addClass('error');
							if (textarea.hasClass('valid')) {
								textarea.removeClass('valid');
							}
                				}
					//}
        				});
        				// Make sure all the content in the textarea is visible
        				setCSS(textarea);
        				copyContent(textarea);
					textarea.height($("#" + id).height());		
				//};			
				}	
			}
		},
		disable: function() {
		}
        };
		
        if ( methods[method] ) {
            return methods[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));
        } else if ( typeof method === 'object' || ! method ) {
            return methods.init.apply( this, arguments );
        } else {
            $.error( 'Method ' +  method + ' does not exist on jQuery.xpObjInput' );
        }    		
	};
})(jQuery);
