
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
 * ** Html **
 * 
 * <div id="id_myList_comp" type="list.content" data-xp="{dbClass: 'MyDAO'}"> </div>
 * 
 * ** Attributes **
 *
 * * ``dbClass``:string
 * * ``app``:string [optional]
 * * ``method``:string [optional] [default:searchFields] : Data method to execute
 * * ``detailView``:object [optional] <viewPath, winType>: View to display detail. hasLinkedRow must be true. Full path, 
 * 															like 'myProject.myApp.myView'. winType can be ``window``or ``popup``
 * * ``detailType``:string [optional] [default:window] : Window type: window, popup.
 * * ``fields``:object<string> [optional]
 * * ``args``:object [optional] : Initial arguments. Object with arguments
 * * ``orderBy``:object [optional] : Order by fields, ascending with '-' sign before field name. Supports relationships, 
 * 									like 'field__value' 
 * * ``disablePaging``:boolean [optional] [default: false]
 * * ``hasCheck``:boolean [optional] : Table has operations linked to row checks. User would check rows and click button to execute
 * 										actions on checked items.
 * * ``activateOnCheck``:object : List of components to activate when row check is clicked.
 * * ``onCheckClick``:string [optional] [default:enable] . Enable or render action components when user clicks on check.
 * * ``pagingStyle``:string [optional] [default:more] : Possible values: more
 * * ``hasLinkRow``:boolean [optional] [default:false]
 * 
 * ** Interfaces **
 * 
 * * ``IList``
 * 
 * ** Methods **
 * 
 * * ``render``(xpForm:string)
 * * ``insertRows``(xpForm:string, result:object)
 *  
 */

(function($) {	

	$.fn.xpListContent = function( method ) {  

        // Settings		
        var settings = {
        	pagingStyle: 'more',
        	hasLinkedRow: false,
        	onCheckClick: 'enable'
        };
        var vars = {};
        
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
		 * Render list
		 * 
		 * ** Attributes **
		 * 
		 * * ``xpForm``:string
		 */
		render : function(xpForm) {			
		},
		/*
		 * Insert rows into list
		 * 
		 * ** Attributes **
		 * 
		 * * ``xpForm``:string
		 * * ``result``:object
		 * 
		 */
		insertRows : function(xpForm, result)
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
 * <div id="id_myList_comp" data-xp-type="list.data" data-xp="{dbClass: 'MyDAO', fields: ['name','value']}" > </div>
 * 
 * ** Attributes **
 *
 * * ``dbClass``:string
 * * ``app``:string [optional]
 * * ``method``:string [optional] [default:searchFields] : Data method to execute
 * * ``detailView``:object [optional] <viewPath, winType>: View to display detail. hasLinkedRow must be true. Full path, 
 * 															like 'myProject.myApp.myView'. winType can be ``window``or ``popup``
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
 * ** Methods **
 * 
 * * ``render``(xpForm:string)
 * * ``insertRows``(xpForm:string, result:object) : Result contains keys data, headers and meta for list result
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
        var vars = {
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
				var fields = attrs.detailView;
				var detailView = fields[0];
				var detailType = fields[1];
				// write into sessionStorage pageStart, pageEnd, orderBy and args for table...
				if (detailType == 'window') {
					ximpia.common.Browser.setObject('list', $(comp).attr('id'));
					if ($(comp).attr('data-xp-page-start')) {
						ximpia.common.Browser.setObject('list-pageStart', parseInt($(comp).attr('data-xp-page-start')));
					}
					if ($(comp).attr('data-xp-page-end')) {
						ximpia.common.Browser.setObject('list-pageEnd', parseInt($(comp).attr('data-xp-page-end')));
					}
					if ($(comp).attr('data-xp-order-by')) {
						ximpia.common.Browser.setObject('list-orderBy', $(comp).attr('data-xp-order-by'));
					}				
				}
				var pathFields = detailView.split('.');
				var detailView = pathFields[pathFields.length-1];
				var app = pathFields.slice(0,2).join('.');
				ximpia.console.log('xpListData :: view: ' + detailView + ' params: ' + JSON.stringify(params) 
						+ ' app: ' + app);
				if (detailType == 'window') {
					ximpia.common.PageAjax.doFadeIn();
				}
				var obj ={ view: detailView, params: JSON.stringify(params), app: app, winType: detailType };
				pageJx.getView(obj);
			}
        };
        /*
         * Init variables from attributes
         */
        var initVars = function() {
			vars.app = ximpia.common.Util.initVariable('app', ximpia.common.Browser.getApp(), vars.attrs);
			vars.dbClass = vars.attrs.dbClass;
			vars.fields = ximpia.common.Util.initVariable('fields', [], vars.attrs);
			vars.compsActivateOnClick = ximpia.common.Util.initVariable('activateOnCheck', [], vars.attrs);
			vars.hasHeader = ximpia.common.Util.initVariable('hasHeader', settings.hasHeader, vars.attrs);
			if (!vars.attrs.hasOwnProperty('hasHeader')) vars.attrs.hasHeader = vars.hasHeader;
			vars.orderBy = ximpia.common.Util.initVariable('orderBy', [], vars.attrs);
			vars.hasLinkRow = JSON.parse(ximpia.common.Util.initVariable('hasLinkRow', false, vars.attrs));
			vars.hasCheck = ximpia.common.Util.initVariable('hasCheck', false, vars.attrs);
			vars.onCheckClick = ximpia.common.Util.initVariable('onCheckClick', settings.onCheckClick, vars.attrs);
        };
        /*
         * Delete column ordering
         */
        var deleteOrder = function(evt, element) {
        	ximpia.console.log('xpListData.deleteOrder...');
			ximpia.console.log(evt);
			ximpia.console.log(element);
			evt.preventDefault();
			vars.index = $(element).parent().parent().index();
			vars.comp = ximpia.common.getParentComponent($(element));
			vars.compId = vars.comp.attr('id');
			ximpia.console.log('xpListData.deleteOrder :: compId: ' + vars.comp.attr('id'));
			vars.idInput = vars.comp.attr('id').split('_comp')[0];
			vars.nameInput = vars.idInput.split('id_')[1];
			$.metadata.setType("attr", "data-xp");
			vars.attrs = $('#' + vars.compId).metadata();
			vars.orderBy = JSON.parse($('#' + vars.compId).attr('data-xp-order-by'));
			ximpia.console.log('xpListData.deleteOrder :: orderBy...');
			ximpia.console.log(vars.orderBy);
			var myField = vars.attrs.fields[vars.index];
			var hasOrderField = false;
			var indexOrder = -1;
			// hasOrderField, indexOrder
			for (var i=0; i<vars.orderBy.length; i++) {
				var targetFieldTmp = vars.orderBy[i];
				if (vars.orderBy[i][0] == '-') {
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
			vars.orderBy.splice(indexOrder, 1);
			ximpia.console.log('xpListData.deleteOrder :: orderBy after delete: ' + vars.orderBy.length);
			$(vars.comp).attr('data-xp-order-by', JSON.stringify(vars.orderBy));
			// restore padding for text column
			var elementLink = $(element).parent().next().children('a');
			$(elementLink).css('padding','6px 10px');
			// must remove .grp-sortoptions
			$(element).parent().remove();
			// we search table data with updated orderBy
			$('#' + vars.compId).attr('data-xp-order-by', JSON.stringify(vars.orderBy));
			ximpia.console.log('xpListData.orderColumn :: orderBy...');
			ximpia.console.log(vars.orderBy);
			// init vars
			initVars();
			vars.attrs.orderBy = vars.orderBy;
			vars.attrs.pageStart = parseInt($('#' + vars.compId).attr('data-xp-page-start'));
			vars.attrs.pageEnd = parseInt($('#' + vars.compId).attr('data-xp-page-end'));
			ximpia.common.JxDataQuery.search(vars.app, vars.dbClass, vars.attrs, function(result) {
				var data = result.data;
				var headers = result.headers;
				var meta = result.meta;
				ximpia.console.log('xpListData.render :: result data...');
				ximpia.console.log(data);
				ximpia.console.log('xpListData.render :: result headers: ' + headers);
				if (data.length > 0) {
					// Render new results under tbody
					html = '';
					for (var l=0; l<data.length; l++) {
						html += buildRow(l, data[l]);
					}
					$('#' + vars.compId + ' table.ui-list-data tbody').html(html);
					
					// Bind click row
					if (vars.hasLinkRow == true) {
						$('#' + vars.compId + ' .ui-list-data tbody').addClass('has-link');
						$('#' + vars.compId + ' .ui-list-data tbody tr td.clickable').click(clickItem);						
					}
					
					// Check click bind
					$('#' + vars.compId + ' .jxListDataCheck').click(function(evt, defaultInputValue) {
						ximpia.console.log(evt);
						ximpia.console.log(defaultInputValue + ' ' + typeof defaultInputValue);
						if (defaultInputValue != 'All') {
							if (vars.onCheckClick == 'enable') {
								// Better ways to toggle???
								if (vars.compsActivateOnClick.length > 0 && $('#' + vars.compId + ' .jxListDataCheck').is(':checked')) {
									// enable
									for (var i=0; i<vars.compsActivateOnClick.length; i++) {
										$('#' + vars.compsActivateOnClick[i]).xpButton('enable');
									}
								} else if (vars.compsActivateOnClick.length > 0) {
									// disable
									for (var i=0; i<vars.compsActivateOnClick.length; i++) {
										$('#' + vars.compsActivateOnClick[i]).xpButton('disable');
									}
								}									
							} else if (vars.onCheckClick == 'render') {
								// I render buttons associated with check
								if (vars.compsActivateOnClick.length > 0 && $('#' + vars.compId + ' .jxListDataCheck').is(':checked')) {
									// render
									for (var i=0; i<vars.compsActivateOnClick.length; i++) {
										$('#' + vars.compsActivateOnClick[i]).xpButton('render');
									}
								} else if (vars.compsActivateOnClick.length > 0) {
									// unrender
									for (var i=0; i<vars.compsActivateOnClick.length; i++) {
										$('#' + vars.compsActivateOnClick[i]).xpButton('unrender');
									}
								}
							}									
						}
					});
					
					$('#' + vars.formId).find("[data-xp-type='image']").xpImage('render', vars.xpForm);					
					
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
			vars.index = $(element).parent().parent().index();
			ximpia.console.log('xpListData.orderColumn :: index: ' + index);
			vars.compId = $(element).attr('data-xp-element-id');
			vars.idInput = vars.compId.split('_comp')[0];
			vars.idElement = vars.compId;
			vars.nameInput = vars.idInput.split('id_')[1];
			$.metadata.setType("attr", "data-xp");
			vars.attrs = $('#' + vars.compId).metadata();
			// init vars
			initVars();
			if (vars.attrs.hasOwnProperty('hasCheck')) {
				vars.index = vars.index - 1;
			}
			vars.orderBy = JSON.parse($('#' + vars.compId).attr('data-xp-order-by'));
			ximpia.console.log('xpListData.orderColumn :: orderBy...');
			ximpia.console.log(vars.orderBy);
			var myField = vars.attrs.fields[vars.index];
			var hasOrderField = false;
			var indexOrder = -1;
			// hasOrderField, indexOrder
			for (var i=0; i<vars.orderBy.length; i++) {
				var targetFieldTmp = vars.orderBy[i];
				if (vars.orderBy[i][0] == '-') {
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
				if (vars.orderBy[indexOrder].search('\\-') == -1) {
					vars.orderBy[indexOrder] = '-' + vars.orderBy[indexOrder];
					$(element).parent().parent().removeClass('ascending');
					$(element).parent().parent().addClass('descending');
					$(element).parent().prev().children('.grp-ascending').removeClass('grp-ascending').addClass('grp-descending');
				} else {
					vars.orderBy[indexOrder] = vars.orderBy[indexOrder].slice(1);
					$(element).parent().parent().removeClass('descending');
					$(element).parent().parent().addClass('ascending');
					$(element).parent().prev().children('.grp-descending').removeClass('grp-descending').addClass('grp-ascending');
				}
			} else {
				// i dont have field in order by, add to orderBy ascensing
				vars.orderBy.push(myField);
				// I add delete order and asc / desc control
				addDeleteCtrl(element, 'ascending');
			}
			$('#' + vars.compId).attr('data-xp-order-by', JSON.stringify(vars.orderBy));
			ximpia.console.log('xpListData.orderColumn :: orderBy...');
			ximpia.console.log(vars.orderBy);
			vars.attrs.orderBy = vars.orderBy;
			vars.attrs.pageStart = parseInt($('#' + vars.compId).attr('data-xp-page-start'));
			vars.attrs.pageEnd = parseInt($('#' + vars.compId).attr('data-xp-page-end'));
			ximpia.common.JxDataQuery.search(vars.app, vars.dbClass, vars.attrs, function(result) {
				var data = result.data;
				var headers = result.headers;
				var meta = result.meta;
				ximpia.console.log('xpListData.render :: result data...');
				ximpia.console.log(data);
				ximpia.console.log('xpListData.render :: result headers: ' + headers);
				if (data.length > 0) {
					// Render new results under tbody
					html = '';
					for (var l=0; l<data.length; l++) {
						html += buildRow(l, data[l]);
					}
					$('#' + vars.compId + ' table.ui-list-data tbody').html(html);
					
					// Bind click row
					if (vars.hasLinkRow == true) {
						$('#' + vars.idElement + ' .ui-list-data tbody').addClass('has-link');
						$('#' + vars.idElement + ' .ui-list-data tbody tr td.clickable').click(clickItem);
					}
					
					// Check click bind
					$('#' + vars.idElement + ' .jxListDataCheck').click(function(evt, defaultInputValue) {
						ximpia.console.log(evt);
						ximpia.console.log(defaultInputValue + ' ' + typeof defaultInputValue);
						if (defaultInputValue != 'All') {
							if (vars.onCheckClick == 'enable') {
								// Better ways to toggle???
								if (vars.compsActivateOnClick.length > 0 && $('#' + vars.idElement + ' .jxListDataCheck').is(':checked')) {
									// enable
									for (var i=0; i<vars.compsActivateOnClick.length; i++) {
										$('#' + vars.compsActivateOnClick[i]).xpButton('enable');
									}
								} else if (vars.compsActivateOnClick.length > 0) {
									// disable
									for (var i=0; i<vars.compsActivateOnClick.length; i++) {
										$('#' + vars.compsActivateOnClick[i]).xpButton('disable');
									}
								}									
							} else if (vars.onCheckClick == 'render') {
								// I render buttons associated with check
								if (vars.compsActivateOnClick.length > 0 && $('#' + vars.idElement + ' .jxListDataCheck').is(':checked')) {
									// render
									for (var i=0; i<vars.compsActivateOnClick.length; i++) {
										$('#' + vars.compsActivateOnClick[i]).xpButton('render');
									}
								} else if (vars.compsActivateOnClick.length > 0) {
									// unrender
									for (var i=0; i<vars.compsActivateOnClick.length; i++) {
										$('#' + vars.compsActivateOnClick[i]).xpButton('unrender');
									}
								}
							}									
						}
					});
					
					$('#' + vars.formId).find("[data-xp-type='image']").xpImage('render', vars.xpForm);
				}
			});
        };
        /*
         * Build table row html
         */
        var buildRow = function(index, row) {
			html = '<tr data-xp-data-id=\"' + row[0] + '\">';
			if (vars.hasCheck == true) {
				html += '<td><input type=\"checkbox\" name=\"' + vars.nameInput + '\" value=\"' + row[0] + '\" class=\"jxListDataCheck\" /></td>';
			}
			for (var i =0; i<row.length; i++) {
				// TODO: Do the row check
				var renderField = row[i];
				if (renderField == null) {
					renderField = '';
				} else if (typeof renderField == 'boolean') {
					var imgScope = vars.nameInput + '_' + row[0] + '_' + i;
					// TODO: Get image to show checked box and unchecked box (as image) checkbox disabled???
					if (renderField == true) {
						renderField = '<div id=\"id_exists_' + imgScope + '_comp\" data-xp-type=\"image\" data-xp=\"{imgClass: \'checkSmall\', title: \'Yes\'}\" > </div>';
					} else {
						renderField = '<div id=\"id_notExists_' + imgScope + '_comp\" data-xp-type=\"image\" data-xp=\"{imgClass: \'errorSmall\', title: \'No\'}\" > </div>';
						//renderField = '';
					}
				}
				if (vars.fields.length == 0) {
					html += '<td>'+ renderField + '</td>';
				} else {
					if ((vars.fields.length != 0 && i > 0 && !ximpia.common.ArrayUtil.hasKey(vars.fields, 'id')) || 
								(vars.fields.length != 0 && ximpia.common.ArrayUtil.hasKey(vars.fields, 'id'))) {
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
			ximpia.console.log($(this));
			ximpia.console.log(this);
			/*var data = ximpia.common.Browser.getFormDataFromSession(xpForm);
			ximpia.console.log(data);*/
			vars.xpForm = xpForm;
			vars.formId = ximpia.common.Browser.getForm(vars.xpForm);
			for (var i=0; i<$(this).length; i++) {
				ximpia.console.log($(this)[i]);
				vars.element = $(this)[i];
				vars.idElement = $(vars.element).attr('id');
				vars.idInput = $(vars.element).attr('id').split('_comp')[0];
				vars.nameInput = vars.idInput.split('id_')[1];
				vars.doRender = ximpia.common.Form.doRender(vars.element, settings.reRender);
				if (vars.doRender == true) {
					ximpia.console.log('xpListData.render :: id: ' + $(vars.element).attr('id'));
					ximpia.console.log('xpListData.render :: nameInput: ' + vars.nameInput);
					$.metadata.setType("attr", "data-xp");
					vars.attrs = $(vars.element).metadata();
					// init vars
					initVars();
					ximpia.console.log('xpListData.render :: attrs...');
					ximpia.console.log(vars.attrs);
					// sessionStorage
					// TODO: Place this into a common method
					var sessionList = ximpia.common.Browser.getObject('list');
					if (sessionList == vars.idElement) {
						var sessionPageStart = ximpia.common.Browser.getObject('list-pageStart');
						var sessionPageEnd = ximpia.common.Browser.getObject('list-pageEnd');
						var sessionOrderBy = ximpia.common.Browser.getObject('list-orderBy');
						if (sessionPageStart != null) {
							vars.attrs.pageStart = sessionPageStart;
							$('#' + vars.idElement).attr('data-xp-page-start', sessionPageStart);
						}
						if (sessionPageEnd != null) {
							vars.attrs.pageEnd = sessionPageEnd;
							$('#' + vars.idElement).attr('data-xp-page-end', sessionPageEnd);
						}
						if (sessionOrderBy != null) {
							vars.attrs.orderBy = vars.orderBy = JSON.parse(sessionOrderBy); 
							$('#' + vars.idElement).attr('data-xp-order-by', vars.attrs.orderBy);
						}
						ximpia.common.Browser.deleteObject('list');
						ximpia.common.Browser.deleteObject('list-pageStart');
						ximpia.common.Browser.deleteObject('list-pageEnd');
						ximpia.common.Browser.deleteObject('list-orderBy');
					}
					ximpia.common.JxDataQuery.search(vars.app, vars.dbClass, vars.attrs, function(result) {
						// TODO: Insert this into insertRows private method
						// data and headers
						// data: [{},{}]
						// headers : ['','','']
						var data = result.data;
						var headers = result.headers;
						var meta = result.meta;
						if (meta.hasOwnProperty('pageStart')) $(vars.element).attr('data-xp-page-start',meta.pageStart);
						if (meta.hasOwnProperty('pageEnd')) $(vars.element).attr('data-xp-page-end',meta.pageEnd);
						ximpia.console.log('xpListData.render :: result data...');
						ximpia.console.log(data);
						ximpia.console.log('xpListData.render :: result headers: ' + headers);
						// Reset sessionStorage for pageStart, pageEnd, orderBy
						if (data.length > 0) {
							// we got valid response
							var headerMap = {};
							// Include filters, orderBy persistence in table element????
							var html = '<table class=\"ui-list-data\" cellspacing=\"0\">';
							// We build table
							// caption
							if (vars.attrs.hasOwnProperty('caption')) {
								var colSpan = headers.length;
								html += '<thead class="caption"><tr><td colspan="' + colSpan + '">' + vars.attrs.caption + '</td></tr></thead>';
							}
							// thead
							if (vars.hasHeader == true) {
								html += '<thead><tr>';
								ximpia.console.log('xpListData.render :: fields...');
								ximpia.console.log(vars.fields);
								if (vars.hasCheck == true) {
									html += '<th scope=\"col\"> <input type=\"checkbox\" name=\"' + vars.nameInput + '_all\" class=\"jxListDataCheckAll\"  /> </th>';
								}
								for (var i=0; i<headers.length; i++) {
									if ((vars.fields.length != 0 && i > 0) && !ximpia.common.ArrayUtil.hasKey(vars.fields, 'id') || 
											vars.fields.length == 0 || (vars.fields.length != 0 && 
												ximpia.common.ArrayUtil.hasKey(vars.fields, 'id'))) {
										ximpia.console.log('xpListData.render :: header: ' + headers[i]);
										html += '<th scope=\"col\"><div class=\"ui-list-data-grp-text\"><a href=\"#\" title=\"';
										html += headers[i] + '\" class=\"jxColumnOrder\" data-xp-element-id=\"'
										html += $(vars.element).attr('id') + '\" >' + headers[i] + '</a></div></th>';
									} 
								}
								html += '</tr></thead>';
							}
							
							// tbody
							html += '<tbody>';
							for (var l=0; l<data.length; l++) {
								html += buildRow(l, data[l]);
							}
							html += '</tbody>';
							
							if (meta.numberPages > meta.pageEnd) {
								var footerColspan = headers.length;
								if (vars.hasCheck) footerColspan = headers.length + 1;
								var pageAttrsStr = $(vars.element).attr('data-xp');
								html += '<tfoot class=\"paging\"><tr><td colspan=\"' + footerColspan + '\">' + 
										'<div id=\"id_' + vars.nameInput + '_paging_comp\" data-xp-type=\"paging.more\" data-xp=\"' + 
												'{listDataId: \'' + vars.idElement + '\'}' + '\" >More Results...</div>' +
										'</td></tr></tfoot>';
							}
							
							html += '</table>';
							// Insert into DOM, set render to true
							$(vars.element).html(html);
							$(vars.element).attr('data-xp-render', JSON.stringify(true));
							$(vars.element).attr('data-xp-order-by', JSON.stringify(vars.orderBy));
							
							if (vars.hasHeader == true) {
								for (var i=0; i<headers.length; i++) {
									var type = 'ascending';
									if (ximpia.common.ArrayUtil.hasKey(vars.orderBy, '-' + vars.fields[i])) {
										type = 'descending';
									}
									if (vars.orderBy.length != 0 && (ximpia.common.ArrayUtil.hasKey(vars.orderBy, vars.fields[i]) ||
											ximpia.common.ArrayUtil.hasKey(vars.orderBy, '-' + vars.fields[i]))) {
										var elementLink = $('#' + $(vars.element).attr('id') + ' th a:contains("' + headers[i] + '")');
										ximpia.console.log('xpListData.render :: render Order ... elementLink...');
										ximpia.console.log(elementLink);
										addDeleteCtrl(elementLink, type);
									}
								}
							}							
							
							// Click on column for ordering
							$("#" + vars.idElement + " .jxColumnOrder").click(function(evt) {
								orderColumn(evt, $(this));
							});
							
							// Bind click row
							if (vars.hasLinkRow == true) {
								$('#' + vars.idElement + ' .ui-list-data tbody').addClass('has-link');
								$('#' + vars.idElement + ' .ui-list-data tbody tr td.clickable').click(clickItem);
							}
							
							// Disable buttons associated with activateOnCheck
							if (vars.onCheckClick == 'enable') {
								// Enable / disable buttons when user clicks on check
								for (var i=0; i<vars.compsActivateOnClick.length; i++) {
									$('#' + vars.compsActivateOnClick[i]).xpButton('disable');
								}
							} else if (vars.onCheckClick == 'render') {
								// Render buttons when user clicks on check
								// We unrender buttons associated with table...
								for (var i=0; i<vars.compsActivateOnClick.length; i++) {
									$('#' + vars.compsActivateOnClick[i]).xpButton('unrender');
								}
							}
							
							// Check all
							$('#' + vars.idElement + ' .ui-list-data .jxListDataCheckAll').click(function() {
								// Check all rows in table
								// Send data to trigger
								$('#' + vars.idElement + ' .ui-list-data').find('input[class=jxListDataCheck]').trigger('click', ['All']);
								// disable buttons if no checks
								var timeout = setTimeout(function() {
									if (vars.onCheckClick == 'enable') {
										if (!$('#' + vars.idElement + ' .jxListDataCheck').is(':checked')) {
											// disable
											for (var i=0; i<vars.compsActivateOnClick.length; i++) {
												$('#' + vars.compsActivateOnClick[i]).xpButton('disable');
											}
										} else {
											// enable
											for (var i=0; i<vars.compsActivateOnClick.length; i++) {
												$('#' + vars.compsActivateOnClick[i]).xpButton('enable');
											}
										}
									} else {
										if (!$('#' + vars.idElement + ' .jxListDataCheck').is(':checked')) {
											// unrender
											for (var i=0; i<vars.compsActivateOnClick.length; i++) {
												$('#' + vars.compsActivateOnClick[i]).xpButton('unrender');
											}
										} else {
											// render
											for (var i=0; i<vars.compsActivateOnClick.length; i++) {
												$('#' + vars.compsActivateOnClick[i]).xpButton('render');
											}
										}
									}
								}, 100);
							});
														
							// Check click bind
							$('#' + vars.idElement + ' .jxListDataCheck').click(function(evt, defaultInputValue) {
								ximpia.console.log(evt);
								ximpia.console.log(defaultInputValue + ' ' + typeof defaultInputValue);
								if (defaultInputValue != 'All') {
									if (vars.onCheckClick == 'enable') {
										// Better ways to toggle???
										if (vars.compsActivateOnClick.length > 0 && $('#' + vars.idElement + ' .jxListDataCheck').is(':checked')) {
											// enable
											for (var i=0; i<vars.compsActivateOnClick.length; i++) {
												$('#' + vars.compsActivateOnClick[i]).xpButton('enable');
											}
										} else if (vars.compsActivateOnClick.length > 0) {
											// disable
											for (var i=0; i<vars.compsActivateOnClick.length; i++) {
												$('#' + vars.compsActivateOnClick[i]).xpButton('disable');
											}
										}									
									} else if (vars.onCheckClick == 'render') {
										// I render buttons associated with check
										if (vars.compsActivateOnClick.length > 0 && $('#' + vars.idElement + ' .jxListDataCheck').is(':checked')) {
											// render
											for (var i=0; i<vars.compsActivateOnClick.length; i++) {
												$('#' + vars.compsActivateOnClick[i]).xpButton('render');
											}
										} else if (vars.compsActivateOnClick.length > 0) {
											// unrender
											for (var i=0; i<vars.compsActivateOnClick.length; i++) {
												$('#' + vars.compsActivateOnClick[i]).xpButton('unrender');
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
		/*
		 * Insert rows into table
		 * 
		 * ** Attributes **
		 * 
		 * * ``xpForm``:string
		 * * ``result``object : Contains keys ``data``, ``headers``and ``meta``. Data has list items. Headers contains the table header
		 * 						information and meta contains data related to query like pageStart and pageEnd.
		 */
		insertRows : function(xpForm, result) {
			ximpia.console.log(result);
			vars.xpForm = xpForm;
			vars.formId = ximpia.common.Browser.getForm(vars.xpForm);
			vars.element = $(this);
			vars.idElement = $(vars.element).attr('id');
			vars.idInput = $(vars.element).attr('id').split('_comp')[0];
			vars.nameInput = vars.idInput.split('id_')[1];
			$.metadata.setType("attr", "data-xp");
			vars.attrs = $(vars.element).metadata();
			// init vars
			initVars();
			var data = result.data;
			var headers = result.headers;
			var meta = result.meta;
			if (meta.hasOwnProperty('pageEnd')) $(vars.element).attr('data-xp-page-end', meta.pageEnd);
			ximpia.console.log('xpListData.render :: result data...');
			ximpia.console.log(data);
			ximpia.console.log('xpListData.render :: result headers: ' + headers);
			if (data.length > 0) {
				// we got valid response
				
				// tbody
				html = '';
				for (var l=0; l<data.length; l++) {
					html += buildRow(l, data[l]);
				}
				
				// Remove paging content in case last page
				if (meta.numberPages == meta.pageEnd) {
					$('#' + vars.idElement + ' tfoot').empty();
				}
				
				// Insert into DOM, set render to true
				$('#' + $(vars.element).attr('id') + ' tbody').append(html);
				
				$('#' + vars.formId).find("[data-xp-type='image']").xpImage('render', vars.xpForm);
				
				// Bind click row
				if (vars.hasLinkRow == true) {
					$('#' + vars.idElement + ' .ui-list-data tbody').addClass('has-link');
					$('#' + vars.idElement + ' .ui-list-data tbody tr td.clickable').click(clickItem);
				}
				
				// Check click bind
				$('#' + vars.idElement + ' .jxListDataCheck').click(function(evt, defaultInputValue) {
					ximpia.console.log(evt);
					ximpia.console.log(defaultInputValue + ' ' + typeof defaultInputValue);
					if (defaultInputValue != 'All') {
						if (vars.onCheckClick == 'enable') {
							// Better ways to toggle???
							if (vars.compsActivateOnClick.length > 0 && $('#' + vars.idElement + ' .jxListDataCheck').is(':checked')) {
								// enable
								for (var i=0; i<vars.compsActivateOnClick.length; i++) {
									$('#' + vars.compsActivateOnClick[i]).xpButton('enable');
								}
							} else if (vars.compsActivateOnClick.length > 0) {
								// disable
								for (var i=0; i<vars.compsActivateOnClick.length; i++) {
									$('#' + vars.compsActivateOnClick[i]).xpButton('disable');
								}
							}									
						} else if (vars.onCheckClick == 'render') {
							// I render buttons associated with check
							if (vars.compsActivateOnClick.length > 0 && $('#' + vars.idElement + ' .jxListDataCheck').is(':checked')) {
								// render
								for (var i=0; i<vars.compsActivateOnClick.length; i++) {
									$('#' + vars.compsActivateOnClick[i]).xpButton('render');
								}
							} else if (vars.compsActivateOnClick.length > 0) {
								// unrender
								for (var i=0; i<vars.compsActivateOnClick.length; i++) {
									$('#' + vars.compsActivateOnClick[i]).xpButton('unrender');
								}
							}
						}									
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
            $.error( 'Method ' +  method + ' does not exist on jQuery.xpListData' );
        }    
		
	};

})(jQuery);

/*
 * More paging component
 *  
 */

(function($) {	

	$.fn.xpPagingMore = function( method ) {  

        // Settings		
        var settings = {
        };
        var vars = {
        };
        var initVars = function() {
			vars.app = ximpia.common.Util.initVariable('app', ximpia.common.Browser.getApp(), vars.attrs);
			vars.dbClass = vars.attrs.dbClass;
			vars.fields = ximpia.common.Util.initVariable('fields', [], vars.attrs);
			vars.compsActivateOnClick = ximpia.common.Util.initVariable('activateOnCheck', [], vars.attrs);
			vars.hasHeader = ximpia.common.Util.initVariable('hasHeader', settings.hasHeader, vars.attrs);
			if (!vars.attrs.hasOwnProperty('hasHeader')) vars.attrs.hasHeader = vars.hasHeader;
			vars.orderBy = ximpia.common.Util.initVariable('orderBy', [], vars.attrs);
			vars.hasLinkRow = JSON.parse(ximpia.common.Util.initVariable('hasLinkRow', false, vars.attrs));
			vars.hasCheck = ximpia.common.Util.initVariable('hasCheck', false, vars.attrs);
			vars.onCheckClick = ximpia.common.Util.initVariable('onCheckClick', settings.onCheckClick, vars.attrs);        	
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
			// Render paging more...
			ximpia.console.log('xpListData :: render...');
			vars.xpForm = xpForm;
			vars.formId = ximpia.common.Browser.getForm(vars.xpForm);
			for (var i=0; i<$(this).length; i++) {
				ximpia.console.log($(this)[i]);
				vars.element = $(this)[i];
				vars.idElement = $(vars.element).attr('id');
				vars.idInput = $(vars.element).attr('id').split('_comp')[0];
				vars.nameInput = vars.idInput.split('id_')[1];
				vars.doRender = ximpia.common.Form.doRender(vars.element, settings.reRender);
				if (vars.doRender == true) {
					ximpia.console.log('xpListData.render :: id: ' + $(vars.element).attr('id'));
					ximpia.console.log('xpListData.render :: nameInput: ' + vars.nameInput);
					$.metadata.setType("attr", "data-xp");
					vars.attrs = $($(this)).metadata();
					vars.listCompId = '';
					if (vars.attrs.hasOwnProperty('listDataId')) {
						vars.listCompId = vars.attrs.listDataId;
					}
					vars.listComp = $('#' + vars.listCompId);
					vars.listCompAttrs = $(vars.listComp).metadata();
					vars.attrs = vars.listCompAttrs;
					// initVars
					initVars();
					$('#' + vars.idElement).click(function() {
						vars.pageStart = parseInt($(vars.listComp).attr('data-xp-page-start'));
						vars.pageEnd = parseInt($(vars.listComp).attr('data-xp-page-end'))+1 || vars.pageStart + 1;
						// Send query
						vars.attrs.pageStart = vars.pageEnd;
						ximpia.common.JxDataQuery.search(vars.app, vars.dbClass, vars.attrs, function(result) {
							// data and headers
							// data: [{},{}]
							// headers : ['','','']
							var data = result.data;
							var headers = result.headers;
							var meta = result.meta;
							// inyect result into listData or listContent???
							$(vars.listComp).xpListData('insertRows', vars.xpForm, result);
						});
					});
				}
			}
		}
        };
		
        if ( methods[method] ) {
            return methods[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));
        } else if ( typeof method === 'object' || ! method ) {
            return methods.init.apply( this, arguments );
        } else {
            $.error( 'Method ' +  method + ' does not exist on jQuery.xpPagingMore' );
        }    
		
	};

})(jQuery);
