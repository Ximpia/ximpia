var ximpia = ximpia || {};
ximpia.settings = ximpia.settings || {};

/*
 * Settings => Move this later to settings.js file on production files, having settings for the frontend
 */
ximpia.settings.THEME = 'base';
ximpia.settings.HOST = 'http://localhost:8000';
ximpia.settings.SITE_MEDIA_URL = ximpia.settings.HOST + '/static/';
ximpia.settings.STATIC_URL = ximpia.settings.HOST + '/static/';
//ximpia.settings.SITE_MEDIA_URL = 'https://ximpia.s3.amazonaws.com/';
//ximpia.settings.SITE_MEDIA_URL = 'https://d22von4i3krd3k.cloudfront.net/';
ximpia.settings.FACEBOOK_APP_ID = '180219935334975';
ximpia.settings.RECAPTCHA_PUBLIC_KEY = '6LePedYSAAAAALK44O_AfaYUR2NjYwJrKeGU5ESn';
ximpia.settings.LOG_LEVELS = ['debug', 'info', 'error', 'warn'];
ximpia.settings.DEBUG = true;

/*
 * Automplete
 */
ximpia.settings.COMPLETE_MAX_HEIGHT = 200
ximpia.settings.COMPLETE_MIN_CHARACTERS = 3
ximpia.settings.LABEL_WIDTH = 'auto'

/*
 * Tooltip
 */
ximpia.settings.IMAGE_TOOLTIP = true;

/*
 * Static Locations
 */
ximpia.settings.static = ximpia.settings.media || {};
ximpia.settings.static.locations = {};
ximpia.settings.static.locations['default'] = '';
ximpia.settings.static.locations['images'] = 'images/';
ximpia.settings.static.hostLocations = {};
ximpia.settings.static.hostLocations['default'] = ximpia.settings.STATIC_URL;
ximpia.settings.static.hostLocations['S3'] = 'https://ximpia.s3.amazonaws.com/';
ximpia.settings.static.hostLocations['cloudfront'] = 'https://d22von4i3krd3k.cloudfront.net/';

/*
 * Image versions
 *  
 */
ximpia.settings.imageVersions = ximpia.settings.imageVersions || {};
ximpia.settings.imageVersions.mini = {verboseName: 'Mini', width: 24, height: 24};
ximpia.settings.imageVersions.thumbnail = {verboseName: 'Thumbnail', width: 60, height: 60};
ximpia.settings.imageVersions.small = {verboseName: 'Small', width: 140};
ximpia.settings.imageVersions.medium = {verboseName: 'Medium', width: 300};
ximpia.settings.imageVersions.big = {verboseName: 'Big', width: 460};
ximpia.settings.imageVersions.large = {verboseName: 'Large', width: 680};
/*
 * PageButton
 */
ximpia.settings.pagebutton = ximpia.settings.pagebutton || {};
ximpia.settings.pagebutton.msg = ximpia.settings.pagebutton.msg || {};
ximpia.settings.pagebutton.msg.slideTimeout = 1500;
