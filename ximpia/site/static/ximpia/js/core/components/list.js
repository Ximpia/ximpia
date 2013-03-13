
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
 * * ``detailView``:string [optional] : View to display detail. hasLinkedRow must be true. Full path, like 'myProject.myApp.myView'
 * * ``detailType``:string [optional] [default:window] : Window type: window, popup.
 * * ``fields``:object<string> [optional]
 * * ``args``:object [optional] : Initial arguments. Object with arguments
 * * ``orderBy``:object [optional] : Order by fields, ascending with '-' sign before field name. Supports relationships, 
 * 									like 'field__value' 
 * * ``disablePaging``:boolean [optional] [default: false]
 * * ``caption``:string [optional]
 * * ``headComponents``:object [optional] : List of header components. Possible values: search|filter
 * * ``hasCheck``:boolean [optional] : Table has operations linked to row checks. User would check rows and click button to execute
 * 										actions on checked items.
 * * ``activateOnCheck``:object : List of components to activate when row check is clicked.
 * * ``onCheckClick``:string [optional] [default:enable] . Enable or render action components when user clicks on check.
 * * ``hasHeader``:boolean [optional] [default:true]
 * * ``pagingStyle``:string [optional] [default:more] : Possible values: more
 * * ``hasLinkRow``:boolean [optional] [default:false]
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
        	hasHeader: true,
        	onCheckClick: 'enable'
        };
        var variables = {
        	xpForm: null,
        	formId: null,
        	app: null
        };
        /*
         * Click on a row. Opens up a view with id selected
         */
        var clickItem = function() {
			ximpia.console.log('xpListData.clickItem...');
			var pageJx = ximpia.common.PageAjax();
			// app, params, view
			var params = {pk: $(this).parent().attr('data-xp-data-id')};
			var comp = ximpia.common.getParentComponent($(this));
			$.metadata.setType("attr", "data-xp");
			var attrs = $('#' + comp.attr('id')).metadata();
			if (attrs.hasOwnProperty('detailView')) {
				var fields = attrs.detailView.split('.');
				var detailView = fields[fields.length-1];
				var app = fields.slice(0,2).join('.');
				ximpia.console.log('xpListData :: view: ' + detailView + ' params: ' + JSON.stringify(params) 
						+ ' app: ' + app);
				ximpia.common.PageAjax.doFadeIn();
				var obj ={ view: detailView, params: JSON.stringify(params), app: app };
				if (attrs.hasOwnProperty('detailType')) {
					obj.winType = attrs.detailType;
				}
				pageJx.getView(obj);
			}
        };
        /*
         * Delete column ordering
         */
        var deleteOrder = function(evt, element) {
        	ximpia.console.log('xpListData.deleteOrder...');
			ximpia.console.log(evt);
			ximpia.console.log(element);
			evt.preventDefault();
			var index = $(element).parent().parent().index();
			var comp = ximpia.common.getParentComponent($(element));
			var compId = comp.attr('id');
			ximpia.console.log('xpListData.deleteOrder :: compId: ' + comp.attr('id'));
			var idInput = comp.attr('id').split('_comp')[0];
			var nameInput = idInput.split('id_')[1];
			$.metadata.setType("attr", "data-xp");
			var attrs = $('#' + compId).metadata();
			var hasLinkRow = false;
			if (attrs.hasOwnProperty('hasLinkRow')) {
				hasLinkRow = JSON.parse(attrs.hasLinkRow)
			}
			var fields = [];
			if (attrs.hasOwnProperty('fields')) {
				fields = attrs.fields;
			}
			var orderBy = JSON.parse($('#' + compId).attr('data-xp-order-by'));
			ximpia.console.log('xpListData.deleteOrder :: orderBy...');
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
			ximpia.console.log('xpListData.deleteOrder :: add: ' + hasOrderField);
			// must delete from orderBy and write to data-xp-order-by
			orderBy.splice(indexOrder, 1);
			ximpia.console.log('xpListData.deleteOrder :: orderBy after delete: ' + orderBy.length);
			$(comp).attr('data-xp-order-by', JSON.stringify(orderBy));
			// restore padding for text column
			var elementLink = $(element).parent().next().children('a');
			$(elementLink).css('padding','6px 10px');
			// must remove .grp-sortoptions
			$(element).parent().remove();
			// we search table data with updated orderBy
			$('#' + compId).attr('data-xp-order-by', JSON.stringify(orderBy));
			ximpia.console.log('xpListData.orderColumn :: orderBy...');
			ximpia.console.log(orderBy);
			var app = '';
			if (attrs.hasOwnProperty('app')) {
				app = attrs.app;
			} else {
				app = ximpia.common.Browser.getApp();
			}
			var hasCheck = false;
			if (attrs.hasOwnProperty('hasCheck')) {
				hasCheck = attrs.hasCheck;
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
					// Render new results under tbody
					html = '';
					for (var l=0; l<data.length; l++) {
						html += buildRow(data[l], nameInput, fields, l, hasCheck);
					}
					$('#' + compId + ' table.ui-list-data tbody').html(html);
					
					// Bind click row
					if (hasLinkRow == true) {
						$('#' + compId + ' table.ui-list-data tbody').addClass('has-link');
						$('#' + compId + ' table.ui-list-data tbody tr').click(clickItem);
					}
					
					$('#' + variables.formId).find("[data-xp-type='image']").xpImage('render', variables.xpForm);					
					
				}
			});
        };
        /*
         * Add delete control to column
         */
        var addDeleteCtrl = function(element, type) {
	 		var htmlCtrl = "<div class=\"grp-sortoptions\"><a class=\"grp-sortremove\" href=\"#\" title=\"Remove from sorting\"></a>";
            htmlCtrl += '<a href=\"#\" class=\"grp-toggle grp-' + type + '\" title=\"Toggle sorting\"></a></div>';
            $(element).parent().parent().prepend(htmlCtrl);
            $(element).parent().parent().addClass('sortable sorted ' + type);
            $(element).css('padding','6px 0px');
			// When click on sort image... 
			$('.grp-toggle').click(function(evt) {
				var elementTextLink = $(this).parent().next().children('a');
				orderColumn(evt, $(elementTextLink));
			});
			$('.grp-sortremove').click(function(evt) {
				deleteOrder(evt, $(this));
			});
        };
        /*
         * Order rows by column field
         */
        var orderColumn = function(evt, element) {
        	ximpia.console.log('xpListData.deleteOrder...');
			evt.preventDefault();
			ximpia.console.log(evt);
			ximpia.console.log(element);
			var index = $(element).parent().parent().index();
			ximpia.console.log('xpListData.orderColumn :: index: ' + index);
			var compId = $(element).attr('data-xp-element-id');
			var idInput = compId.split('_comp')[0];
			var idElement = compId;
			var nameInput = idInput.split('id_')[1];
			$.metadata.setType("attr", "data-xp");
			var attrs = $('#' + compId).metadata();
			if (attrs.hasOwnProperty('hasCheck')) {
				index = index - 1;
			}
			var hasLinkRow = false;
			if (attrs.hasOwnProperty('hasLinkRow')) {
				hasLinkRow = JSON.parse(attrs.hasLinkRow)
			}
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
				addDeleteCtrl(element, 'ascending');
			}
			$('#' + compId).attr('data-xp-order-by', JSON.stringify(orderBy));
			ximpia.console.log('xpListData.orderColumn :: orderBy...');
			ximpia.console.log(orderBy);
			var app = '';
			if (attrs.hasOwnProperty('app')) {
				app = attrs.app;
			} else {
				app = ximpia.common.Browser.getApp();
			}
			var hasCheck = false;
			if (attrs.hasOwnProperty('hasCheck')) {
				hasCheck = attrs.hasCheck;
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
					// Render new results under tbody
					html = '';
					for (var l=0; l<data.length; l++) {
						html += buildRow(data[l], nameInput, fields, l, hasCheck);
					}
					$('#' + compId + ' table.ui-list-data tbody').html(html);
					
					// Bind click row
					if (hasLinkRow == true) {
						$('#' + idElement + ' .ui-list-data tbody').addClass('has-link');
						$('#' + idElement + ' .ui-list-data tbody tr td.clickable').click(clickItem);
					}
					
					$('#' + variables.formId).find("[data-xp-type='image']").xpImage('render', variables.xpForm);
				}
			});
        };
        /*
         * Build table row html
         */
        var buildRow = function(row, nameInput, fields, index, hasCheck) {
			html = '<tr data-xp-data-id=\"' + row[0] + '\">';
			if (hasCheck == true) {
				html += '<td><input type=\"checkbox\" name=\"' + nameInput + '\" value=\"' + row[0] + '\" class=\"jxListDataCheck\" /></td>';
			}
			for (var i =0; i<row.length; i++) {
				// TODO: Do the row check
				var renderField = row[i];
				if (renderField == null) {
					renderField = '';
				} else if (typeof renderField == 'boolean') {
					var imgScope = nameInput + '_' + index;
					// TODO: Get image to show checked box and unchecked box (as image) checkbox disabled???
					if (renderField == true) {
						renderField = '<div id=\"id_exists_' + imgScope + '_comp\" data-xp-type=\"image\" data-xp=\"{imgClass: \'checkSmall\', title: \'Yes\'}\" > </div>';
					} else {
						renderField = '<div id=\"id_notExists_' + imgScope + '_comp\" data-xp-type=\"image\" data-xp=\"{imgClass: \'errorSmall\', title: \'No\'}\" > </div>';
						//renderField = '';
					}
				}
				if (fields.length == 0) {
					html += '<td>'+ renderField + '</td>';
				} else {
					if ((fields.length != 0 && i > 0 && !ximpia.common.ArrayUtil.hasKey(fields, 'id')) || 
								(fields.length != 0 && ximpia.common.ArrayUtil.hasKey(fields, 'id'))) {
						html += '<td class=\"clickable\">'+ renderField + '</td>';
					}
				}
				// TODO: Do the row ordering control at end of row: move row from one position to another
				// TODO: Group rows with + sign. Ability to move rows from one container to another, would open container and change parent
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
		/*
		 * Render data list table
		 */
		render : function(xpForm) {
			ximpia.console.log('xpListData :: render...');
			/*var data = ximpia.common.Browser.getFormDataFromSession(xpForm);
			ximpia.console.log(data);*/
			variables.xpForm = xpForm;
			variables.formId = ximpia.common.Browser.getForm(variables.xpForm);
			for (var i=0; i<$(this).length; i++) {
				ximpia.console.log($(this)[i]);
				var element = $(this)[i];
				var idElement = $(element).attr('id');
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
					variables.app = app;
					var dbClass = attrs.dbClass;
					var fields = [];
					if (attrs.hasOwnProperty('fields')) {
						fields = attrs.fields;
					}
					var compsActivateOnClick = [];
					if (attrs.hasOwnProperty('activateOnCheck')) {
						compsActivateOnClick = attrs.activateOnCheck;
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
					var hasLinkRow = false;
					if (attrs.hasOwnProperty('hasLinkRow')) {
						hasLinkRow = JSON.parse(attrs.hasLinkRow);
					}
					var hasCheck = false;
					if (attrs.hasOwnProperty('hasCheck')) {
						hasCheck = attrs.hasCheck;
					}
					var onCheckClick = settings.onCheckClick;
					if (attrs.hasOwnProperty('onCheckClick')) {
						onCheckClick = attrs.onCheckClick;
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
								var colSpan = headers.length;
								html += '<thead class="caption"><tr><td colspan="' + colSpan + '">' + attrs.caption + '</td></tr></thead>';
							}
							// thead
							if (hasHeader == true) {
								html += '<thead><tr>';
								ximpia.console.log('xpListData.render :: fields...');
								ximpia.console.log(fields);
								if (hasCheck == true) {
									html += '<th scope=\"col\"> <input type=\"checkbox\" name=\"' + nameInput + '_all\" class=\"jxListDataCheckAll\"  /> </th>';
								}
								for (var i=0; i<headers.length; i++) {
									if ((fields.length != 0 && i > 0) && !ximpia.common.ArrayUtil.hasKey(fields, 'id') || 
											fields.length == 0 || (fields.length != 0 && ximpia.common.ArrayUtil.hasKey(fields, 'id'))) {
										ximpia.console.log('xpListData.render :: header: ' + headers[i]);
										html += '<th scope=\"col\"><div class=\"ui-list-data-grp-text\"><a href=\"#\" title=\"';
										html += headers[i] + '\" class=\"jxColumnOrder\" data-xp-element-id=\"'
										html += $(element).attr('id') + '\" >' + headers[i] + '</a></div></th>';
									} 
								}
								html += '</tr></thead>';
							}
							
							// tbody
							html += '<tbody>';
							for (var l=0; l<data.length; l++) {
								html += buildRow(data[l], nameInput, fields, l, hasCheck);
							}
							html += '</tbody>';
							html += '</table>';
							// Insert into DOM, set render to true
							$(element).html(html);
							$(element).attr('data-xp-render', JSON.stringify(true));
							$(element).attr('data-xp-order-by', JSON.stringify(orderBy));
							
							if (hasHeader == true) {
								for (var i=0; i<headers.length; i++) {
									var type = 'ascending';
									if (ximpia.common.ArrayUtil.hasKey(orderBy, '-' + fields[i])) {
										type = 'descending';
									}
									if (orderBy.length != 0 && (ximpia.common.ArrayUtil.hasKey(orderBy, fields[i]) ||
											ximpia.common.ArrayUtil.hasKey(orderBy, '-' + fields[i]))) {
										var elementLink = $('#' + $(element).attr('id') + ' th a:contains("' + headers[i] + '")');
										ximpia.console.log('xpListData.render :: render Order ... elementLink...');
										ximpia.console.log(elementLink);
										addDeleteCtrl(elementLink, type);
									}
								}
							}							
							
							// Click on column for ordering
							$("#" + idElement + " .jxColumnOrder").click(function(evt) {
								orderColumn(evt, $(this));
							});
							
							// Bind click row
							if (hasLinkRow == true) {
								$('#' + idElement + ' .ui-list-data tbody').addClass('has-link');
								$('#' + idElement + ' .ui-list-data tbody tr td.clickable').click(clickItem);
							}
							
							// Disable buttons associated with activateOnCheck
							if (onCheckClick == 'enable') {
								// Enable / disable buttons when user clicks on check
								for (var i=0; i<compsActivateOnClick.length; i++) {
									$('#' + compsActivateOnClick[i]).xpButton('disable');
								}
							} else if (onCheckClick == 'render') {
								// Render buttons when user clicks on check
								// We unrender buttons associated with table...
								for (var i=0; i<compsActivateOnClick.length; i++) {
									$('#' + compsActivateOnClick[i]).xpButton('unrender');
								}
							}
							
							// Check all
							$('#' + idElement + ' .ui-list-data .jxListDataCheckAll').click(function() {
								// Check all rows in table
								// Send data to trigger
								$('#' + idElement + ' .ui-list-data').find('input[class=jxListDataCheck]').trigger('click', ['All']);
								// disable buttons if no checks
								var timeout = setTimeout(function() {
									if (onCheckClick == 'enable') {
										if (!$('#' + idElement + ' .jxListDataCheck').is(':checked')) {
											// disable
											for (var i=0; i<compsActivateOnClick.length; i++) {
												$('#' + compsActivateOnClick[i]).xpButton('disable');
											}
										} else {
											// enable
											for (var i=0; i<compsActivateOnClick.length; i++) {
												$('#' + compsActivateOnClick[i]).xpButton('enable');
											}
										}
									} else {
										if (!$('#' + idElement + ' .jxListDataCheck').is(':checked')) {
											// unrender
											for (var i=0; i<compsActivateOnClick.length; i++) {
												$('#' + compsActivateOnClick[i]).xpButton('unrender');
											}
										} else {
											// render
											for (var i=0; i<compsActivateOnClick.length; i++) {
												$('#' + compsActivateOnClick[i]).xpButton('render');
											}
										}
									}
								}, 100);
							});
														
							// Check click bind
							$('#' + idElement + ' .jxListDataCheck').click(function(evt, defaultInputValue) {
								ximpia.console.log(evt);
								ximpia.console.log(defaultInputValue + ' ' + typeof defaultInputValue);
								if (defaultInputValue != 'All') {
									if (onCheckClick == 'enable') {
										// Better ways to toggle???
										if (compsActivateOnClick.length > 0 && $('#' + idElement + ' .jxListDataCheck').is(':checked')) {
											// enable
											for (var i=0; i<compsActivateOnClick.length; i++) {
												$('#' + compsActivateOnClick[i]).xpButton('enable');
											}
										} else if (compsActivateOnClick.length > 0) {
											// disable
											for (var i=0; i<compsActivateOnClick.length; i++) {
												$('#' + compsActivateOnClick[i]).xpButton('disable');
											}
										}									
									} else if (onCheckClick == 'render') {
										// I render buttons associated with check
										if (compsActivateOnClick.length > 0 && $('#' + idElement + ' .jxListDataCheck').is(':checked')) {
											// render
											for (var i=0; i<compsActivateOnClick.length; i++) {
												$('#' + compsActivateOnClick[i]).xpButton('render');
											}
										} else if (compsActivateOnClick.length > 0) {
											// unrender
											for (var i=0; i<compsActivateOnClick.length; i++) {
												$('#' + compsActivateOnClick[i]).xpButton('unrender');
											}
										}
									}									
								}
							});
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


