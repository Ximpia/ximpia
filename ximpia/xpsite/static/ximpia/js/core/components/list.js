
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
 * list Constants
 */

ximpia.constants.list = ximpia.constants.list || {};

ximpia.constants.list.REPLACE = 'replace';
ximpia.constants.list.APPEND = 'append';


/*
 * List of content elements
 * 
 * ** Html **
 * 
 * You include a div for the component definition and html inside this div can be any html element that will
 * be repeated for each row in the list. You include data with {{}} notation. Response context has elements for lists
 * with ``list_myList``where myList relates to ``id_myList_comp``. This way you don't have to repeat {{list_myList.data.myField}} and only
 * need to include {{data.myField}}. You can include list values, header values and meta values for the list.
 * 
 * You can include any element in three positions: jxListContentHeader, jxListContentBody and jxListContentFoot. Body position will incude
 * the rows to be repeated in the list with values. Header will include content before list and foot includes any content you need at end
 * of list.
 * 
 * <div id="id_myList_comp" type="list.content" data-xp="{dbClass: 'MyDAO', fields: ['myField']}"> 
 * 
 * <$htmlElement class="jxListContentHeader">
 * Here go the results...
 * </$htmlElement>
 * 
 * <$htmlElement class="jxListContentBody">
 * {{header.myField}}: {{data.myField}}
 * </$htmlElement>
 * 
 * <$htmlElement class="jxListContentFoot">
 * numberPages: {{meta.numberPages}}
 * </$htmlElement>
 * 
 * </div>
 * 
 * ** Attributes **
 *
 * * ``dbClass``:string
 * * ``app``:string [optional]
 * * ``method``:string [optional] [default:searchFields] : Data method to execute
 * * ``fields``:object<string>
 * * ``args``:object [optional] : Initial arguments. Object with arguments
 * * ``orderBy``:object [optional] : Order by fields, ascending with '-' sign before field name. Supports relationships, 
 * 									like 'field__value' 
 * * ``disablePaging``:boolean [optional] [default: false]
 * * ``pagingStyle``:string [optional] [default:more] : Possible values: more
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
        var vars = {        	
        };
        var constants = {
        	TMPL_LIST_HEADER: 'xpListHeader',
        	TMPL_LIST_BODY: 'xpListBody',
        	TMPL_LIST_FOOT: 'xpListFoot'
        };
        
        /*
         * Init variables from attributes
         */
        var _initVars = function() {
			vars.app = ximpia.common.Util.initVariable('app', ximpia.common.Browser.getApp(), vars.attrs);
			vars.dbClass = vars.attrs.dbClass;
			vars.fields = ximpia.common.Util.initVariable('fields', [], vars.attrs);
			vars.compsActivateOnClick = ximpia.common.Util.initVariable('activateOnCheck', [], vars.attrs);
			vars.orderBy = ximpia.common.Util.initVariable('orderBy', [], vars.attrs);
			vars.hasLinkRow = JSON.parse(ximpia.common.Util.initVariable('hasLinkRow', false, vars.attrs));
			vars.hasCheck = ximpia.common.Util.initVariable('hasCheck', false, vars.attrs);
			vars.onCheckClick = ximpia.common.Util.initVariable('onCheckClick', settings.onCheckClick, vars.attrs);
        };
        /*
         * Build item html
         * 
         * ** Returns **
         * 
         * Returns the html for items
         * 
         */
        var _buildItemHtml = function() {
			var html = '';			
			for (var l=0; l<vars.data.length; l++) {
				var index = 1;
				if (!ximpia.common.ArrayUtil.hasKey(vars.fields, 'id')) {
					vars.fields.splice(0, 0, 'id');
				}
				var mapData = ximpia.common.List.getMapByKeyList(vars.fields, vars.data[l])
				var mapHeader = ximpia.common.List.getMapByKeyList(vars.fields, vars.headers)
				ximpia.console.log('xpListContent._buildItemHtml :: mapData...');
				ximpia.console.log(mapData);
				ximpia.console.log('xpListContent._buildItemHtml :: mapHeader...');
				ximpia.console.log(mapHeader);
				// Insert data and headers into response object
				vars.resp.listObj.data = mapData;
				vars.resp.listObj.headers = mapHeader;
				// meta				
				ximpia.console.log('xpListContent._buildItemHtml :: listObj...');
				ximpia.console.log(vars.resp.listObj);
				html += ximpia.common.Content.replaceFields(vars.templateBodyHtml, vars.resp.listObj);
			}
			return html;			        	
        }
        /*
         * Build component html
         */
        var _buildHtml = function() {
        	// Process content template...			
			// Get body
			// Get header
			// Get foot
			vars.templateBodyHtml = '';
			vars.templateHeaderHtml = '';
			vars.templateFootHtml = '';			
			$(vars.element).children('.jxListContentHeader').each(function() {
				vars.templateHeaderHtml += $(this)[0].outerHTML;
				var headerData = $(vars.element).data(constants.TMPL_LIST_HEADER) || '';
				$(vars.element).data(constants.TMPL_LIST_HEADER, headerData += $(this)[0].outerHTML);
				$(this).remove();
			});
			$(vars.element).children('.jxListContentBody').each(function() {
				vars.templateBodyHtml += $(this)[0].outerHTML;
				var bodyData = $(vars.element).data(constants.TMPL_LIST_BODY) || '';
				$(vars.element).data(constants.TMPL_LIST_BODY, bodyData += $(this)[0].outerHTML);
				$(this).remove();
			});
			$(vars.element).children('.jxListContentFoot').each(function() {
				vars.templateFootHtml += $(this)[0].outerHTML;
				var footData = $(vars.element).data(constants.TMPL_LIST_FOOT) || '';
				$(vars.element).data(constants.TMPL_LIST_FOOT, footData += $(this)[0].outerHTML);
				$(this).remove();
			});
			// resp
			vars.resp = ximpia.common.Browser.getResponse();
			vars.resp.listObj = {};
			vars.resp.listObj.meta = vars.meta;
			// Header
			$(vars.element).append(ximpia.common.Content.replaceFields(vars.templateHeaderHtml, vars.resp.listObj));
			// Item html			
			var html = _buildItemHtml();
			$(vars.element).append(html);			
			// Include component attributes for render and order
			$(vars.element).attr('data-xp-render', JSON.stringify(true))
							.attr('data-xp-order-by', JSON.stringify(vars.orderBy));			
			// Foot
			$(vars.element).append(ximpia.common.Content.replaceFields(vars.templateFootHtml, vars.resp.listObj));
        };
        /*
         * Do persistence when a new view is triggered and user clicks on back button, paging and order has persistence
         */
        var _doPersistence = function() {
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
        }
        
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
			ximpia.console.log('xpListContent :: render...');
			vars.xpForm = xpForm;
			vars.formId = ximpia.common.Browser.getForm(vars.xpForm);
			for (var i=0; i<$(this).length; i++) {
				ximpia.console.log($(this)[i]);
				vars.element = $(this)[i];
				vars.idElement = $(vars.element).attr('id');
				vars.idInput = $(vars.element).attr('id');
				vars.nameInput = vars.idInput;
				vars.doRender = ximpia.common.Form.doRender(vars.element, settings.reRender);
				if (vars.doRender == true) {
					ximpia.console.log('xpListContent.render :: id: ' + $(vars.element).attr('id'));
					ximpia.console.log('xpListContent.render :: nameInput: ' + vars.nameInput);
					$.metadata.setType("attr", "data-xp");
					vars.attrs = $(vars.element).metadata();
					// init vars
					_initVars();
					ximpia.console.log('xpListContent.render :: attrs...');
					ximpia.console.log(vars.attrs);
					// Persistence
					_doPersistence();
					vars.attrs.hasHeader = true;
					ximpia.common.JxDataQuery.search(vars.app, vars.dbClass, vars.attrs, function(result) {
						// data and headers
						// data: [{},{}]
						// headers : ['','','']						
						vars.data = result.data;
						vars.headers = result.headers;
						vars.meta = result.meta;
						if (vars.meta.hasOwnProperty('pageStart')) $(vars.element).attr('data-xp-page-start',vars.meta.pageStart);
						if (vars.meta.hasOwnProperty('pageEnd')) $(vars.element).attr('data-xp-page-end',vars.meta.pageEnd);
						ximpia.console.log('xpListContent.render :: result data...');
						ximpia.console.log(vars.data);
						ximpia.console.log('xpListContent.render :: result headers: ' + vars.headers);
						// Reset sessionStorage for pageStart, pageEnd, orderBy
						if (vars.data.length > 0) {
							_buildHtml();							
						}
					});
				}
			}
		},
		/*
		 * Insert rows into list
		 * 
		 * ** Attributes **
		 * 
		 * * ``xpForm``:string
		 * * ``result``:object
		 * * ``mode``:string : Insertion mode: 'append' or 'replace'
		 * * ``args``:object : Arguments
		 * 		* ``pagingCompId``:string : Paging component id. Will remove this when no more paging available
		 * 
		 */
		insertRows : function(xpForm, result, mode, args) {
			ximpia.console.log(result);
			vars.xpForm = xpForm;
			vars.formId = ximpia.common.Browser.getForm(vars.xpForm);
			vars.element = $(this);
			vars.idElement = $(vars.element).attr('id');
			vars.idInput = $(vars.element).attr('id');
			vars.nameInput = vars.idInput;
			$.metadata.setType("attr", "data-xp");
			vars.attrs = $(vars.element).metadata();
			// init vars
			_initVars();
			vars.attrs.hasHeader = true;
			vars.data = result.data;
			vars.headers = result.headers;
			vars.meta = result.meta;
			// resp
			vars.resp = ximpia.common.Browser.getResponse();
			vars.resp.listObj = {};
			vars.resp.listObj.meta = vars.meta;
			if (vars.meta.hasOwnProperty('pageEnd')) $(vars.element).attr('data-xp-page-end', vars.meta.pageEnd);
			ximpia.console.log('xpListContent.render :: result data...');
			ximpia.console.log(vars.data);
			ximpia.console.log('xpListContent.render :: result headers: ' + vars.headers);			
			if (vars.data.length > 0) {				
				// Get body template...
				vars.templateBodyHtml = $(this).data(constants.TMPL_LIST_BODY);
				
				// Remove paging content in case last page
				if (vars.meta.numberPages == vars.meta.pageEnd) {
					$('#' + args.pagingCompId).remove();
				}
				var html = _buildItemHtml();
				if ($(vars.element).find('.jxListContentFoot')) {
					// foot? -> Append after last .jxListContentBody
					$('.jxListContentBody:last').after(html);
				} else {
					// else -> append to element
					$(vars.element).append(html);
				}					
			}			
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
 * * ``pagingStyle``:string [optional] [default:more] : Possible values: more, bullet
 * * ``pagingMoreText``:string [optional] [default:More Results...] : More paging text
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
        	onCheckClick: 'enable',
        	pageMoreText: 'More Results...'
        };
        var vars = {
        };
                
        var constants = {
        	ATTR_APP: 'app',
        	ATTR_METHOD: 'method',
        	ATTR_DETAIL_VIEW: 'detailView',
        	ATTR_DETAIL_TYPE: 'detailType',
        	ATTR_FIELDS: 'fields',
        	ATTR_ARGS: 'args',
        	ATTR_ORDER_BY: 'orderBy',
        	ATTR_DISABLE_PAGING: 'disablePaging',
        	ATTR_CAPTION: 'caption',
        	ATTR_HEAD_COMPONENTS: 'headComponents',
        	ATTR_HAS_CHECK: 'hasCheck',
        	ATTR_ACTIVATE_ON_CHECK: 'activateOnCheck',
        	ATTR_ON_CHECK_CLICK: 'onCheckClick',
        	ATTR_HAS_HEADER: 'hasHeader',
        	ATTR_PAGING_STYLE: 'pagingStyle',
        	ATTR_HAS_LINK_ROW: 'hasLinkRow',
        	ATTR_PAGING_MORE_TEXT: 'pagingMoreText',
        	PAGE_MORE: 'more',
        	PAGE_BULLET: 'bullet',
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
				var app = pathFields.slice(0,pathFields.length-1).join('.');
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
			vars.attrs[constants.ATTR_PAGING_STYLE] = ximpia.common.Util.initVariable(constants.ATTR_PAGING_STYLE, 
				settings.pagingStyle, vars.attrs);
			vars.attrs[constants.ATTR_PAGING_MORE_TEXT] = ximpia.common.Util.initVariable(constants.ATTR_PAGING_MORE_TEXT, 
				settings.pageMoreText, vars.attrs);
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
			vars.idInput = vars.comp.attr('id');
			vars.nameInput = vars.idInput;
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
					
					ximpia.common.PageAjax.doRenderListRows(vars.xpForm);
					
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
			ximpia.console.log('xpListData.orderColumn :: index: ' + vars.index);
			vars.compId = $(element).attr('data-xp-element-id');
			vars.idInput = vars.compId;
			vars.idElement = vars.compId;
			vars.nameInput = vars.idInput;
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
					
					ximpia.common.PageAjax.doRenderListRows(vars.xpForm);
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
						renderField = '<div id=\"id_exists_' + imgScope + '\" data-xp-type=\"image\" data-xp=\"{imgClass: \'checkSmall\', title: \'Yes\'}\" > </div>';
					} else {
						renderField = '<div id=\"id_notExists_' + imgScope + '\" data-xp-type=\"image\" data-xp=\"{imgClass: \'errorSmall\', title: \'No\'}\" > </div>';
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
			vars.xpForm = xpForm;
			vars.formId = ximpia.common.Browser.getForm(vars.xpForm);
			for (var i=0; i<$(this).length; i++) {
				ximpia.console.log($(this)[i]);
				vars.element = $(this)[i];
				vars.idElement = $(vars.element).attr('id');
				vars.idInput = $(vars.element).attr('id');
				vars.nameInput = vars.idInput;
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
						// data and headers
						// data: [{},{}]
						// headers : ['','','']
						//ximpia.common.Browser.setObject('list_' + vars.nameInput, result);
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
										html += headers[i] + '\" class=\"jxColumnOrder\" data-xp-element-id=\"';
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
							if (meta.numberPages > meta.pageEnd && vars.attrs.hasOwnProperty(constants.ATTR_PAGING_STYLE)) {
								var footerColspan = headers.length;
								if (vars.hasCheck) footerColspan = headers.length + 1;
								var pageAttrsStr = $(vars.element).attr('data-xp');
								if (vars.attrs[constants.ATTR_PAGING_STYLE] == constants.PAGE_MORE) {
									html += '<tfoot class=\"paging\"><tr><td colspan=\"' + footerColspan + '\">';
									html += '<div id=\"id_' + vars.nameInput + '_paging\" data-xp-type=\"paging.' + 
											vars.attrs[constants.ATTR_PAGING_STYLE] + '\" data-xp=\"' + 
											'{compId: \'' + vars.idElement + '\'}' + '\" >' + vars.attrs[constants.ATTR_PAGING_MORE_TEXT] + 
											'</div>';
								} else if (vars.attrs[constants.ATTR_PAGING_STYLE] == constants.PAGE_BULLET) {
									html += '<tfoot class=\"paging-bullet\"><tr><td colspan=\"' + footerColspan + '\">';
									html += '<div id=\"id_' + vars.nameInput + '_paging\" data-xp-type=\"paging.' + 
											vars.attrs[constants.ATTR_PAGING_STYLE] + '\" data-xp=\"' + 
											'{compId: \'' + vars.idElement + '\', ' + 
											'numberPages: ' + meta.numberPages + ', ' + 
											'numberResources: ' + vars.attrs.numberResults + '}' + '\" > </div>';
								}
								html += '</td></tr></tfoot>';
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
		 * ``mode``:string : Insertion mode: 'append' or 'replace'
		 * ``args``:object
		 * 
		 */
		insertRows : function(xpForm, result, mode, args) {
			ximpia.console.log(result);
			vars.xpForm = xpForm;
			vars.formId = ximpia.common.Browser.getForm(vars.xpForm);
			vars.element = $(this);
			vars.idElement = $(vars.element).attr('id');
			vars.idInput = $(vars.element).attr('id');
			vars.nameInput = vars.idInput;
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
				if (meta.numberPages == meta.pageEnd && mode == ximpia.constants.list.APPEND) {
					$('#' + vars.idElement + ' tfoot').empty();
				}
				
				// Insert into DOM, set render to true
				if (mode == ximpia.constants.list.APPEND) {
					$('#' + $(vars.element).attr('id') + ' tbody').append(html);
				} else if (mode == ximpia.constants.list.REPLACE) {
					$('#' + $(vars.element).attr('id') + ' tbody').html(html);
				}
				ximpia.common.PageAjax.doRenderListRows(vars.xpForm);
				// Bind click row
				if (vars.hasLinkRow == true) {
					$('#' + vars.idElement + ' .ui-list-data tbody').addClass('has-link');
					$('#' + vars.idElement + ' .ui-list-data tbody tr td.clickable').click(clickItem);
				}
				// Check click bind
				// TODO: Place into a common method
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
 * ** Html **
 * 
 * ** Attributes **
 * 
 * * ``compId``
 * 
 * ** Interfaces **
 * 
 * IPage
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
			ximpia.console.log('xpPagingMore :: render...');
			vars.xpForm = xpForm;
			vars.formId = ximpia.common.Browser.getForm(vars.xpForm);
			for (var i=0; i<$(this).length; i++) {
				ximpia.console.log($(this)[i]);
				vars.element = $(this)[i];
				vars.idElement = $(vars.element).attr('id');
				vars.idInput = $(vars.element).attr('id');
				vars.nameInput = vars.idInput;
				vars.doRender = ximpia.common.Form.doRender(vars.element, settings.reRender);
				if (vars.doRender == true) {
					ximpia.console.log('xpPagingMore.render :: id: ' + $(vars.element).attr('id'));
					ximpia.console.log('xpPagingMore.render :: nameInput: ' + vars.nameInput);
					$(vars.element).attr('data-xp-render', JSON.stringify(true));
					$('#' + vars.idElement).click(function(evt) {
						// Get variables from linked component: app, dbClass, attrs, etc...
						$.metadata.setType("attr", "data-xp");
						vars.attrs = $(this).metadata();
						vars.listCompId = vars.attrs.compId;
						vars.listComp = $('#' + vars.listCompId);
						// Reference component attributes...
						vars.attrs = $(vars.listComp).metadata();
						// initVars
						initVars();
						vars.pageStart = parseInt($(vars.listComp).attr('data-xp-page-start'));
						vars.pageEnd = parseInt($(vars.listComp).attr('data-xp-page-end'))+1 || vars.pageStart + 1;
						vars.attrs.pageStart = vars.pageEnd;
						vars.attrs.hasHeader = true;
						// Send query
						ximpia.common.JxDataQuery.search(vars.app, vars.dbClass, vars.attrs, function(result) {
							var data = result.data;
							var headers = result.headers;
							var meta = result.meta;
							// inject result into listData or listContent
							if (vars.listComp.attr('data-xp-type') == 'list.data') {
								$(vars.listComp).xpListData('insertRows', vars.xpForm, result, ximpia.constants.list.APPEND);
							} else if (vars.listComp.attr('data-xp-type') == 'list.content') {
								$(vars.listComp).xpListContent('insertRows', vars.xpForm, result, ximpia.constants.list.APPEND, 
														{
															pagingCompId: vars.idElement
														});
							}
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

/*
 * Bullet paging component which displays current page, next n (customized, default 5) pages with ability to jump to pages.  
 * 
 * Current page has filled bullet. When mouse goes over, shows number of resources to fetch (1-10).
 * 
 * ** Html **
 * 
 * ** Attributes **
 * 
 * * ``compId``:string : Id for list component
 * * ``numberPages``:number : Number of pages for list
 * * ``numberResources``:number : Number of resources in the list, used to display result pointers in page links (1-10, etc...)
 * 
 * ** Interfaces **
 * 
 * IPage
 *  
 */

(function($) {	

	$.fn.xpPagingBullet = function( method ) {  

        // Settings		
        var settings = {
        	numberPagesDisplayMax: 20
        };
        var vars = {
        };
        var constants = {        	
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
			ximpia.console.log('xpPagingMore :: render...');
			vars.xpForm = xpForm;
			vars.formId = ximpia.common.Browser.getForm(vars.xpForm);
			for (var i=0; i<$(this).length; i++) {
				ximpia.console.log($(this)[i]);
				vars.element = $(this)[i];
				vars.idElement = $(vars.element).attr('id');
				vars.idInput = $(vars.element).attr('id');
				vars.nameInput = vars.idInput;
				vars.doRender = ximpia.common.Form.doRender(vars.element, settings.reRender);
				if (vars.doRender == true) {
					$.metadata.setType("attr", "data-xp");
					vars.attrs = $(vars.element).metadata();
					ximpia.console.log('xpPagingBullet.render :: id: ' + $(vars.element).attr('id'));
					ximpia.console.log('xpPagingBullet.render :: nameInput: ' + vars.nameInput);					
					var html = '<nav class="ui-list-paging-bullet" ><ul>';
					var maxPages = settings.numberPagesDisplayMax;
					if (parseInt(vars.attrs.numberPages) < maxPages) {
						maxPages = parseInt(vars.attrs.numberPages);
					}
					for (var i=1; i<=maxPages; i++) {
						if (i == 1) {
							html += '<li><a class="bubble active" href="#" title="1-' + vars.attrs.numberResources + 
									'" data-xp="{page: 1}" > </a></li>';
						} else {
							html += '<li><a class="bubble" href="#" title="' + ((i-1)*parseInt(vars.attrs.numberResources)+1) + 
									'-' + i*parseInt(vars.attrs.numberResources) + 
									'" data-xp="{page: ' + i + '}" ></a></li>';
						}						
					}
					html += '</ul></nav>';
					$(vars.element).html(html); 
					$(vars.element).attr('data-xp-render', JSON.stringify(true));
					$('#' + vars.idElement + ' a').click(function(evt) {
						evt.preventDefault();
						// Get variables from linked component: app, dbClass, attrs, etc...
						vars.pagingComp = ximpia.common.getParentComponent($(this), {type: 'paging.bullet'});
						$.metadata.setType("attr", "data-xp");
						vars.attrs = $(vars.pagingComp).metadata();
						vars.listCompId = vars.attrs.compId;
						vars.listComp = $('#' + vars.listCompId);
						// Reference component attributes...
						vars.attrs = $(vars.listComp).metadata();
						// initVars
						initVars();
						vars.pageStart = $(this).metadata().page;
						vars.pageEnd = vars.pageStart;
						vars.attrs.pageStart = vars.pageEnd;
						vars.attrs.pageEnd = vars.pageEnd;
						vars.attrs.hasHeader = true;
						vars.element = $(this);
						// Send query
						ximpia.common.JxDataQuery.search(vars.app, vars.dbClass, vars.attrs, function(result) {
							var data = result.data;
							var headers = result.headers;
							var meta = result.meta;
							// inject result into listData or listContent
							if (vars.listComp.attr('data-xp-type') == 'list.data') {
								$(vars.listComp).xpListData('insertRows', vars.xpForm, result, ximpia.constants.list.REPLACE);
							} else if (vars.listComp.attr('data-xp-type') == 'list.content') {
								$(vars.listComp).xpListContent('insertRows', vars.xpForm, result, ximpia.constants.list.REPLACE, 
														{
															pagingCompId: vars.idElement
														});
							}
							// Process removal of page depending of number pages
							// Make requested page as active and remove old active
							// Remove active link
							ximpia.common.getParentComponent($(vars.element)).find('.active').removeClass('active');
							// Make active selected page
							$(vars.element).addClass('active');
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
            $.error( 'Method ' +  method + ' does not exist on jQuery.xpPagingBullet' );
        }    
		
	};

})(jQuery);
