// jQuery Context Menu Plugin
//
// Version 1.01
//
// Cory S.N. LaViska
// A Beautiful Site (http://abeautifulsite.net/)
//
// More info: http://abeautifulsite.net/2008/09/jquery-context-menu-plugin/
//
// Terms of Use
//
// This plugin is dual-licensed under the GNU General Public License
//   and the MIT License and is copyright A Beautiful Site, LLC.
//
if(jQuery)( function() {
	$.extend($.fn, {
		
		contextMenu: function(o, callback) {
			// Defaults
			if (o.doAllways == undefined) o.doAllways = true;
			if (o.align == undefined) o.align = 'left';
			if( o.menu == undefined ) return false;
			if( o.inSpeed == undefined ) o.inSpeed = 200;
			if( o.outSpeed == undefined ) o.outSpeed = 200;
			// 0 needs to be -1 for expected results (no fade)
			if( o.inSpeed == 0 ) o.inSpeed = -1;
			if( o.outSpeed == 0 ) o.outSpeed = -1;
			// Loop each context menu
			$(this).each( function() {
				var el = $(this);
				var offset = $(el).offset();
				var showMenu = false;
				// Add contextMenu class
				$('#' + o.menu).addClass('contextMenu');
				// Simulate a true right click
				$(this).click( function(e) {
					var evt = e;
					//var doAllways = true;
					//ximpia.console.log('contextMenu :: event: ');
					//ximpia.console.log(evt);
					evt.stopPropagation();
					//$(this).mouseup( function(e) {
						e.stopPropagation();
						var srcElement = $(this);
						//$(this).unbind('mouseup');
						if ( o.doAllways == true) {
							showMenu = true;
						} else {
							if( evt.button == 2 ) {
								showMenu = true;
							}
						}
						// Get this context menu
						var menu = $('#' + o.menu);
						if ($(menu).css('display') == 'block') {
							showMenu = false;
						}						
						
						//ximpia.console.log('contextMenu :: showMenu: ' + showMenu);
						
						if( showMenu == true ) {
							// Hide context menus that may be showing
							$(".contextMenu").hide();
							//$(menu).find('li.hover').removeClass('hover');
							//$(menu).find('li a').unbind('click');
							
							if( $(el).hasClass('disabled') ) return false;
							
							// Detect mouse position
							var d = {}, x, y;
							if( self.innerHeight ) {
								d.pageYOffset = self.pageYOffset;
								d.pageXOffset = self.pageXOffset;
								d.innerHeight = self.innerHeight;
								d.innerWidth = self.innerWidth;
							} else if( document.documentElement &&
								document.documentElement.clientHeight ) {
								d.pageYOffset = document.documentElement.scrollTop;
								d.pageXOffset = document.documentElement.scrollLeft;
								d.innerHeight = document.documentElement.clientHeight;
								d.innerWidth = document.documentElement.clientWidth;
							} else if( document.body ) {
								d.pageYOffset = document.body.scrollTop;
								d.pageXOffset = document.body.scrollLeft;
								d.innerHeight = document.body.clientHeight;
								d.innerWidth = document.body.clientWidth;
							}
							(e.pageX) ? x = e.pageX : x = e.clientX + d.scrollLeft;
							(e.pageY) ? y = e.pageY : y = e.clientY + d.scrollTop;
							
							if (o.alignElement != undefined && o.alignElement == true) {
								if (o.align == 'left') {
									x = offset.left;
								}
							}
							if (o.isCombo == true) {
								// Menu is positioned aligned from previous element when isCombo is true
								//ximpia.console.log('contextMenu :: isCombo: ' + o.isCombo);
								// Get width of previous element
								var offsetPrev = $(this).prev().offset();
								//ximpia.console.log($(this).prev().offset());
								x = offsetPrev.left;
							}
							y = offset.top + parseInt(srcElement.css('height').split('px')[0]) + 3;
							if (o.paddingTop != undefined) {
								y = y + o.paddingTop;
							}
							
							// Show the menu
							$(document).unbind('click');
							//ximpia.console.log('contextMenu :: menu displayed?: ' + $(menu).css('display'));
							$(menu).css({ top: y, left: x }).slideDown(o.inSpeed);
							
							// Hover events
							$(menu).find('a').mouseover( function() {
								$(menu).find('li.hover').removeClass('hover');
								$(this).parent().addClass('hover');
							}).mouseout( function() {
								$(menu).find('li.hover').removeClass('hover');
							});
							
							// Keyboard
							$(document).keydown( function(e) {
								//ximpia.console.log('contextMenu :: key: ' + e.keyCode);
								switch( e.keyCode ) {
									case 38: // up
										if( $(menu).find('li.hover').size() == 0 ) {
											$(menu).find('li:last').addClass('hover');
										} else {
											$(menu).find('li.hover').removeClass('hover').prevAll('li:not(.disabled)').eq(0).addClass('hover');
											if( $(menu).find('li.hover').size() == 0 ) $(menu).find('li:last').addClass('hover');
										}
									break;
									case 40: // down
										if( $(menu).find('li.hover').size() == 0 ) {
											$(menu).find('li:first').addClass('hover');
										} else {
											$(menu).find('li.hover').removeClass('hover').nextAll('li:not(.disabled)').eq(0).addClass('hover');
											if( $(menu).find('li.hover').size() == 0 ) $(menu).find('li:first').addClass('hover');
										}
									break;
									case 13: // enter
										//$(menu).find('li.hover a').trigger('click');
										//alert('click!!!');
										//ximpia.console.log('Will try to click on hover items...');
									break;
									case 27: // esc
										$(document).trigger('click');
									break
								}
							});
							
							// When items are selected
							$('#' + o.menu).find('a').unbind('click');
							$('#' + o.menu).find('li:not(.disabled) a').click( function() {
								$(document).unbind('click').unbind('keypress');
								$(".contextMenu").hide();
								// Callback
								if( callback ) callback( $(this).attr('href').substr(1), $(srcElement), {x: x - offset.left, y: y - offset.top, docX: x, docY: y} );
								return false;
							});
							
							// Hide bindings
							setTimeout( function() { // Delay for Mozilla
								$(document).click( function() {
									$(document).unbind('click').unbind('keypress');
									$(menu).slideUp(o.outSpeed);
									return false;
								});
							}, 0);
						} else {
							// show menu is false
							$(menu).find('li.hover').removeClass('hover');
							$(menu).slideUp(o.outSpeed);
						}
					//});
				});
				
				// Disable text selection
				if( $.browser.mozilla ) {
					$('#' + o.menu).each( function() { $(this).css({ 'MozUserSelect' : 'none' }); });
				} else if( $.browser.msie ) {
					$('#' + o.menu).each( function() { $(this).bind('selectstart.disableTextSelect', function() { return false; }); });
				} else {
					$('#' + o.menu).each(function() { $(this).bind('mousedown.disableTextSelect', function() { return false; }); });
				}
				// Disable browser context menu (requires both selectors to work in IE/Safari + FF/Chrome)
				$(el).add($('UL.contextMenu')).bind('contextmenu', function() { return false; });
				
			});
			return $(this);
		},
		
		// Disable context menu items on the fly
		disableContextMenuItems: function(o) {
			if( o == undefined ) {
				// Disable all
				$(this).find('li').addClass('disabled');
				return( $(this) );
			}
			$(this).each( function() {
				if( o != undefined ) {
					var d = o.split(',');
					for( var i = 0; i < d.length; i++ ) {
						$(this).find('a[href="' + d[i] + '"]').parent().addClass('disabled');
						
					}
				}
			});
			return( $(this) );
		},
		
		// Enable context menu items on the fly
		enableContextMenuItems: function(o) {
			if( o == undefined ) {
				// Enable all
				$(this).find('li.disabled').removeClass('disabled');
				return( $(this) );
			}
			$(this).each( function() {
				if( o != undefined ) {
					var d = o.split(',');
					for( var i = 0; i < d.length; i++ ) {
						$(this).find('a[href="' + d[i] + '"]').parent().removeClass('disabled');
						
					}
				}
			});
			return( $(this) );
		},
		
		// Disable context menu(s)
		disableContextMenu: function() {
			$(this).each( function() {
				$(this).addClass('disabled');
			});
			return( $(this) );
		},
		
		// Enable context menu(s)
		enableContextMenu: function() {
			$(this).each( function() {
				$(this).removeClass('disabled');
			});
			return( $(this) );
		},
		
		// Destroy context menu(s)
		destroyContextMenu: function() {
			// Destroy specified context menus
			$(this).each( function() {
				// Disable action
				$(this).unbind('mousedown').unbind('mouseup');
			});
			return( $(this) );
		}
		
	});
})(jQuery);