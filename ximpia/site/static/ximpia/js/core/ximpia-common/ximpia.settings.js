var ximpia = ximpia || {};
ximpia.settings = ximpia.settings || {};

/*
 * Settings => Move this later to settings.js file on production files, having settings for the frontend
 */
ximpia.settings.HOST = 'http://localhost:8000';
ximpia.settings.SITE_MEDIA_URL = ximpia.settings.HOST + '/static/';
ximpia.settings.STATIC_URL = ximpia.settings.HOST + '/static/';
//ximpia.settings.SITE_MEDIA_URL = 'https://ximpia.s3.amazonaws.com/';
//ximpia.settings.SITE_MEDIA_URL = 'https://d22von4i3krd3k.cloudfront.net/';
ximpia.settings.FACEBOOK_APP_ID = '180219935334975';
ximpia.settings.RECAPTCHA_PUBLIC_KEY = '6LePedYSAAAAALK44O_AfaYUR2NjYwJrKeGU5ESn';
ximpia.settings.LOG_LEVELS = ['debug', 'info', 'error', 'warn'];
ximpia.settings.DEBUG = true;
