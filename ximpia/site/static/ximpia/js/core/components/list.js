
/*
 * 
 * Copyright (c) 2013 Ximpia, Inc, All rights reserved
 * This Source Code Form is subject to the terms of the Mozilla Public License, 
 * v. 2.0. If a copy of the MPL was not distributed with this file, You can obtain 
 * one at http://mozilla.org/MPL/2.0/.
 * 
 */

/*
 * List of content elements
 *  
 */

(function($) {	

	$.fn.xpListContent = function( method ) {  

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
		render : function() {
			
		}
        };
		
        if ( methods[method] ) {
            return methods[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));
        } else if ( typeof method === 'object' || ! method ) {
            return methods.init.apply( this, arguments );
        } else {
            $.error( 'Method ' +  method + ' does not exist on jQuery.xpListContent' );
        }    
		
	};

})(jQuery);

/*
 * Tabular data
 * 
 * 
 * * HTML **
 * 
 * <div id="id_myList_comp" data-xp-type="list.data" data-xp="{dbClass: 'MyDAO', linkFields: ['name'], fields: ['name','value']}" > </div>
 * 
 * ** Attributes **
 *
 * * ``dbClass``:string
 * * ``app``:string [optional]
 * * ``method``:string [optional] [default:searchFields] : Data method to execute
 * * ``detailView``:string [optional] : View to display detail. hasLinkedRow must be true.
 * * ``fields``:object<string> [optional]
 * * ``args``:object [optional] : Initial arguments. Object with arguments
 * * ``orderBy``:object [optional] : Order by fields, ascending with '-' sign before field name. Supports relationships, 
 * 									like 'field__value' 
 * * ``disablePaging``:boolean [optional] [default: false]
 * * ``caption``:string [optional]
 * * ``headComponents``:object [optional] : List of header components. Possible values: search|filter
 * * ``hasCheck``:boolean [optional]
 * * ``hasSorting``:boolean [optional]
 * * ``hasHeader``:boolean [optional] [default:true]
 * * ``orderField``:string [optional]
 * * ``pagingStyle``:string [optional] [default:more] : Possible values: more
 * * ``hasLinkedRow``:boolean [optional] [default:false]
 * 
 * ** Build Attributes **
 * 
 * * ``pageStart``
 * * ``pageEnd``
 * 
 * ** Interfaces **
 * 
 * IList 
 *  
 */

(function($) {	

	$.fn.xpListData = function( method ) {  

        // Settings		
        var settings = {
        	pagingStyle: 'more',
        	hasLinkedRow: false,
        	hasHeader: true
        };
        var variables = {
        	xpForm: null,
        	formId: null
        };
        /*
         * Click on a row. Opens up a view with id selected
         */
        var clickItem = function() {
        	alert($(this).attr('data-xp-data-id'));
        };
        /*
         * Delete column ordering
         */
        var deleteOrder = function(evt, element) {
        	
        };
        /*
         * Order rows by column field
         */
        var orderColumn = function(evt, element) {
			evt.preventDefault();
			ximpia.console.log(evt);
			ximpia.console.log(element);
			var index = $(element).parent().parent().index();
			ximpia.console.log('xpListData.orderColumn :: index: ' + index);
			var compId = $(element).attr('data-xp-element-id');
			var idInput = compId.split('_comp')[0];
			var nameInput = idInput.split('id_')[1];
			$.metadata.setType("attr", "data-xp");
			var attrs = $('#' + compId).metadata();
			var fields = [];
			if (attrs.hasOwnProperty('fields')) {
				fields = attrs.fields;
			}
			var orderBy = JSON.parse($('#' + compId).attr('data-xp-order-by'));
			ximpia.console.log('xpListData.orderColumn :: orderBy...');
			ximpia.console.log(orderBy);
			var myField = attrs.fields[index];
			var hasOrderField = false;
			var indexOrder = -1;
			// hasOrderField, indexOrder
			for (var i=0; i<orderBy.length; i++) {
				var targetFieldTmp = orderBy[i];
				if (orderBy[i][0] == '-') {
					var targetField = targetFieldTmp.slice(1);
				} else {
					var targetField = targetFieldTmp;
				}
				if (targetField == myField) {
					hasOrderField = true;
					indexOrder = i;
				}
			}
			ximpia.console.log('xpListData.orderColumn :: hasOrderField: ' + hasOrderField);
			if (hasOrderField) {
				// I have order field in orderBy, change ascending or descending
				if (orderBy[indexOrder].search('\\-') == -1) {
					orderBy[indexOrder] = '-' + orderBy[indexOrder];
					$(element).parent().parent().removeClass('ascending');
					$(element).parent().parent().addClass('descending');
					$(element).parent().prev().children('.grp-ascending').removeClass('grp-ascending').addClass('grp-descending');
				} else {
					orderBy[indexOrder] = orderBy[indexOrder].slice(1);
					$(element).parent().parent().removeClass('descending');
					$(element).parent().parent().addClass('ascending');
					$(element).parent().prev().children('.grp-descending').removeClass('grp-descending').addClass('grp-ascending');
				}
			} else {
				// i dont have field in order by, add to orderBy ascensing
				orderBy.push(myField);
				// I add delete order and asc / desc control
		 		var htmlCtrl = "<div class=\"grp-sortoptions\"><a class=\"grp-sortremove\" href=\"#\" title=\"Remove from sorting\"></a><a href=\"#\" class=\"grp-toggle grp-ascending\" title=\"Toggle sorting\"></a></div>";
                $(element).parent().parent().prepend(htmlCtrl);
                $(element).parent().parent().addClass('sortable sorted ascending');
                $(element).css('padding','6px 0px');
			}
							/*$('.grp-toggle.jxColumnOrder').click(function(evt) {
								orderColumn(evt, $(this));
							});*/
			$('#' + compId).attr('data-xp-order-by', JSON.stringify(orderBy));
			ximpia.console.log('xpListData.orderColumn :: orderBy...');
			ximpia.console.log(orderBy);
			var app = '';
			if (attrs.hasOwnProperty('app')) {
				app = attrs.app;
			} else {
				app = ximpia.common.Browser.getApp();
			}
			var dbClass = attrs.dbClass;
			attrs.orderBy = orderBy;
			ximpia.common.JxDataQuery.search(app, dbClass, attrs, function(result) {
				var data = result.data;
				var headers = result.headers;
				ximpia.console.log('xpListData.render :: result data...');
				ximpia.console.log(data);
				ximpia.console.log('xpListData.render :: result headers: ' + headers);
				if (data.length > 0) {
					// Remove results
					$('#' + compId + ' table.ui-list-data tbody').empty();
					// Render new results under tbody
					html = '';
					for (var l=0; l<data.length; l++) {
						html += buildRow(data[l], nameInput, fields, l);
					}
					$('#' + compId + ' table.ui-list-data tbody').html(html);
					
					// Bind click row
					$('.ui-list-data tbody tr').click(clickItem);
					
					$('#' + variables.formId).find("[data-xp-type='image']").xpImage('render', variables.xpForm);					
				}
			});			
			

			
        };
        /*
         * 
         */
        var buildRow = function(row, nameInput, fields, index) {
			html = '<tr data-xp-data-id=\"' + row[0] + '\">';
			for (var i =0; i<row.length; i++) {
				// TODO: Do the row check
				var renderField = row[i];
				if (renderField == null) {
					renderField = '';
				} else if (typeof renderField == 'boolean') {
					var imgScope = nameInput + '_' + index;
					if (renderField == true) {
						renderField = '<div id=\"id_exists_' + imgScope + '_comp\" data-xp-type=\"image\" data-xp=\"{imgClass: \'checkSmall\', title: \'Yes\'}\" > </div>';
					} else {
						//renderField = '<div id=\"id_notExists_' + imgScope + '_comp\" data-xp-type=\"image\" data-xp=\"{imgClass: \'errorSmall\', title: \'No\'}\" > </div>';
						renderField = '';
					}
				}
				if (fields.length == 0) {
					html += '<td>'+ renderField + '</td>';
				} else {
					if ((fields.length != 0 && i > 0 && !ximpia.common.ArrayUtil.hasKey(fields, 'id')) || 
								(fields.length != 0 && ximpia.common.ArrayUtil.hasKey(fields, 'id'))) {
						html += '<td>'+ renderField + '</td>';
					}
				}
				// TODO: Do the row ordering control at end of row
			}
			html += '</tr>';
			return html;
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
			ximpia.console.log('xpListData :: render...');
			/*var data = ximpia.common.Browser.getFormDataFromSession(xpForm);
			ximpia.console.log(data);*/
			variables.xpForm = xpForm;
			variables.formId = ximpia.common.Browser.getForm(variables.xpForm);
			for (var i=0; i<$(this).length; i++) {
				ximpia.console.log($(this)[i]);
				var element = $(this)[i];
				var idInput = $(element).attr('id').split('_comp')[0];
				var nameInput = idInput.split('id_')[1];
				var doRender = ximpia.common.Form.doRender(element, settings.reRender);
				if (doRender == true) {
					ximpia.console.log('xpListData.render :: id: ' + $(element).attr('id'));
					ximpia.console.log('xpListData.render :: nameInput: ' + nameInput);
					$.metadata.setType("attr", "data-xp");
					var attrs = $(element).metadata();
					var app = '';
					if (attrs.hasOwnProperty('app')) {
						app = attrs.app;
					} else {
						app = ximpia.common.Browser.getApp();
					}
					var dbClass = attrs.dbClass;
					var fields = [];
					if (attrs.hasOwnProperty('fields')) {
						fields = attrs.fields;
					}
					var hasHeader = settings.hasHeader;
					if (attrs.hasOwnProperty('hasHeader')) {
						var hasHeader = attrs.hasHeader;
					} else {
						attrs.hasHeader = hasHeader;
					}
					var orderBy = [];
					if (attrs.hasOwnProperty('orderBy')) {
						orderBy = attrs.orderBy;
					}
					ximpia.console.log('xpListData.render :: attrs...');
					ximpia.console.log(attrs);
					ximpia.common.JxDataQuery.search(app, dbClass, attrs, function(result) {
						// data and headers
						// data: [{},{}]
						// headers : ['','','']
						var data = result.data;
						var headers = result.headers;
						ximpia.console.log('xpListData.render :: result data...');
						ximpia.console.log(data);
						ximpia.console.log('xpListData.render :: result headers: ' + headers);
						if (data.length > 0) {
							// we got valid response
							var headerMap = {};
							// Include filters, orderBy persistence in table element????
							var html = '<table class=\"ui-list-data\" cellspacing=\"0\">';
							// We build table
							// caption
							if (attrs.hasOwnProperty('caption')) {
								html += '<caption>' + attrs.caption + '</caption>';
							}
							// thead
							if (hasHeader == true) {
								html += '<thead><tr>';
								ximpia.console.log('xpListData.render :: fields...');
								ximpia.console.log(fields);
								for (var i=0; i<headers.length; i++) {
									if ((fields.length != 0 && i > 0) && !ximpia.common.ArrayUtil.hasKey(fields, 'id') || 
											fields.length == 0 || (fields.length != 0 && ximpia.common.ArrayUtil.hasKey(fields, 'id'))) {
										ximpia.console.log('xpListData.render :: header: ' + headers[i]);
										html += '<th scope=\"col\"><div class=\"ui-list-data-grp-text\"><a href=\"#\" title=\"' + headers[i] + '\" class=\"jxColumnOrder\" data-xp-element-id=\"' + $(element).attr('id') + '\" >' + headers[i] + '</a></div></th>';
									}
								}
								html += '</tr></thead>';
							}
							
							// tbody
							html += '<tbody>';
							for (var l=0; l<data.length; l++) {
								html += buildRow(data[l], nameInput, fields, l);
							}
							html += '</tbody>';
							html += '</table>';
							// Insert into DOM, set render to true
							$(element).html(html);
							$(element).attr('data-xp-render', JSON.stringify(true));
							$(element).attr('data-xp-order-by', JSON.stringify(orderBy));
							
							$(".jxColumnOrder").click(function(evt) {
								orderColumn(evt, $(this));
							});
							
							// Bind click row
							var hasLinkRow = JSON.parse(attrs.hasLinkRow) || false;
							if (hasLinkRow == true) {
								$('.ui-list-data tbody').addClass('has-link');
								$('.ui-list-data tbody tr').click(clickItem);
							}
							
							// TODO: Bind the delete order
							
						}
					});
				}
			}
		},
		clickItem : function(xpForm) {
		}
        };
		
        if ( methods[method] ) {
            return methods[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));
        } else if ( typeof method === 'object' || ! method ) {
            return methods.init.apply( this, arguments );
        } else {
            $.error( 'Method ' +  method + ' does not exist on jQuery.xpListData' );
        }    
		
	};

})(jQuery);


