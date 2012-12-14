import httplib2
import urlparse
import oauth2
import simplejson as json
import types
import traceback
import os

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.http import Http404

from yacaptcha.models import Captcha

from ximpia.core.util import getClass
from models import context, ContextViewDecorator, ContextDecorator
from service import XpMsgException, ViewTmplDecorator, SearchService, TemplateService
from data import ViewDAO, ActionDAO

settings = getClass(os.getenv("DJANGO_SETTINGS_MODULE"))

# Logging
import logging.config
logging.config.dictConfig(settings.LOGGING)
logger = logging.getLogger(__name__)

def oauth20(request, service):
	"""Doc."""
	logger.debug( 'GET : ' + json.dumps(request.GET) )
	ContextDict = {
				'service': service,
				'status': '',
				'token': '',
				'tokenSecret': '',
				'errorMessage': ''
				}
	oauthVersion = settings.XIMPIA_CONSUMER_DICT[service][2]
	if oauthVersion == '2.0': 
		if request.GET.has_key('code'):
			code = request.GET['code']
			# Exchange code for access token
			logger.debug( settings.XIMPIA_CONSUMER_DICT[service][0] + '  ' + settings.XIMPIA_CONSUMER_DICT[service][1] )
			url = settings.XIMPIA_OAUTH_URL_DICT[service]['access'][0] + '?' + \
				'client_id=' + settings.XIMPIA_CONSUMER_DICT[service][0] + \
				'&redirect_uri=' + settings.XIMPIA_OAUTH2_REDIRECT + service + \
				'&client_secret=' + settings.XIMPIA_CONSUMER_DICT[service][1] + \
				'&code=' + code
			http = httplib2.Http()
			resp, content = http.request(url)
			if resp['status'] == '200':
				responseDict = dict(urlparse.parse_qsl(content))
				accessToken = responseDict['access_token']
				logger.debug( accessToken )
				ContextDict['status'] = 'OK'
				ContextDict['token'] = accessToken
				ContextDict['tokenSecret'] = ''
			else:
				# Show error
				ContextDict['status'] = 'ERROR'
		else:
			ContextDict['status'] = 'ERROR'
	else:
		ContextDict['status'] = 'ERROR'
	template = 'social_network/tags/networks/iconResponse.html'
	Result = render_to_response(template, ContextDict)
	return Result

def oauth(request, service):
	"""Oauth logic with all providers registered in settings"""
	logger.debug( 'GET : ' + json.dumps(request.GET) )
	# Think about methods in login: LinkedIn, parameters, etc...
	ContextDict = {
				'service': service,
				'status': '',
				'token': '',
				'tokenSecret': '',
				'errorMessage': ''
				}
	logger.debug( settings.XIMPIA_CONSUMER_DICT )
	oauthVersion = settings.XIMPIA_CONSUMER_DICT[service][2]
	if oauthVersion == '1.0':
		if len(request.GET.keys()) == 0:
			consumerTuple =  settings.XIMPIA_CONSUMER_DICT[service]
			consumer = oauth2.Consumer(consumerTuple[0], consumerTuple[1])
			client = oauth2.Client(consumer)
			resp, content = client.request(settings.XIMPIA_OAUTH_URL_DICT[service]['request'][0], settings.XIMPIA_OAUTH_URL_DICT[service]['request'][1])
			#logger.debug( json.dumps(resp) )
			if resp['status'] == '200':
				#logger.debug( json.dumps(content) )
				request_token = dict(urlparse.parse_qsl(content))
				logger.debug( request_token )
				request.session['request_token'] = request_token
				# Redirect to linkedin Url
				url = settings.XIMPIA_OAUTH_URL_DICT[service]['authorized'][0] + '?oauth_token=' + request_token['oauth_token']
				return HttpResponseRedirect(url)
			else:
				# should show message of error in connecting with network
				ContextDict['status'] = 'ERROR'
		else:
			# Callback : oauth_token and oauth_verifier
			logger.debug( 'callback...' )
			if request.GET.has_key('oauth_token') and request.GET.has_key('oauth_verifier'):
				#oauth_token = request.GET['oauth_token']
				oauth_verifier = request.GET['oauth_verifier']
				request_token = request.session['request_token']
				token = oauth2.Token(request_token['oauth_token'], request_token['oauth_token_secret'])
				token.set_verifier(oauth_verifier)
				consumerTuple =  settings.XIMPIA_CONSUMER_DICT[service]
				consumer = oauth2.Consumer(consumerTuple[0], consumerTuple[1])
				client = oauth2.Client(consumer, token)
				resp, content = client.request(settings.XIMPIA_OAUTH_URL_DICT[service]['access'][0], "POST")
				access_token = dict(urlparse.parse_qsl(content))
				logger.debug( 'access_token: ' + access_token )
				# Show web page... javascript logic and close window
				ContextDict['status'] = 'OK'
				ContextDict['token'] = access_token['oauth_token']
				ContextDict['tokenSecret'] = access_token['oauth_token_secret']
			else:
				# Show error message
				ContextDict['status'] = 'ERROR'
	else:
		# Show error
		ContextDict['status'] = 'ERROR'
	template = 'social_network/tags/networks/iconResponse.html'
	Result = render_to_response(template, ContextDict)
	return Result

def reloadCaptcha(request):
	"""Reload captcha
	@param request: """
	Captcha(request).create()
	Result = HttpResponse('OK')
	return Result

def checkCaptcha(request, value):
	"""Checks that value is the same as stored in captcha for user session. Returns True/False in json
	@param request: 
	@param value: Text inputed by user
	@return: json True/False"""
	captcha = Captcha(request).get()
	check = False
	if captcha == value:
		check = True
	jsonCheck = json.dumps(check)
	return jsonCheck

@context
def jxJSON(request, **ArgsDict):
	"""Sequence of actions are executed. Returns either OK or ERROR. jsonData has list of fields action,argsTuple, argsDict."""
	# init
	ctx = ArgsDict['ctx']
	# Option 1 : Map method, argsTuple, argsDict
	if request.POST.has_key('jsonData'):
		try:
			data = json.loads(request.POST['jsonData'])['jsonDataList']
			for fields in data:
				action, parameterList, parameterDict = fields
				resultTmp = eval(action)(*parameterList, **parameterDict)
				if type(resultTmp) == types.ListType:
					listResult = []
					for entity in resultTmp:
						dd = entity.values()
						listResult.append(dd)
					ctx.rs['status'] = 'OK'
					ctx.rs['response'] = listResult
				else:
					entity = resultTmp
					ctx.rs['status'] = 'OK'
					ctx.rs['response'] = entity.values()
		except:
			ctx.rs['status'] = 'ERROR'
	else:
		ctx.rs['status'] = 'ERROR'
	response = json.dumps(ctx.rs)
	return HttpResponse(response)

@context
def jxSuggestList(request, **ArgsDict):
	"""Suggest search list"""
	# init
	ctx = ArgsDict['ctx']
	# Do
	resultList = []
	if request.REQUEST.has_key('dbClass'):
		dbClass = request.REQUEST['dbClass'];
		params = json.loads(request.REQUEST['params']);
		params[params['text']] = request.REQUEST['search'];
		del params['text']
		obj = eval(dbClass)(ctx) #@UnusedVariable
		fields = eval('obj.filter')(*[], **params)
		for entity in fields:
			dd = {}
			dd['id'] = entity.id
			dd['text'] = entity.getText()
			resultList.append(dd) 
	return HttpResponse(json.dumps(resultList))

@context
def searchHeader(request, **args):
	"""Search ximpia for views and actions."""
	try:
		logger.debug( 'searchHeader...' )
		logger.debug( 'search: ' + request.REQUEST['search'] )
		# What are params in jxSuggestList?????
		ctx = args['ctx']
		searchObj = SearchService(ctx)
		results = searchObj.search(request.REQUEST['search'])
		logger.debug( 'results: ' + json.dumps(results) )
	except:
		traceback.print_exc()
	return HttpResponse(json.dumps(results))

def jxTemplate(request, app, mode, tmplName):
	"""
	
	Get ximpia template
	
	**Attributes**
	
	* ``app``:String : Application
	* ``mode``:String : Mode: window, popup
	* ``tmplName``:String : Template name
	
	** Returns **
	
	* ``template``:HttpResponse	
	
	"""
	
	service = TemplateService(None)
	tmpl = service.get(app, mode, tmplName)
	
	"""tmpl = cache.get('tmpl/' + app + '/' + mode + '/' + tmplName)
	if not tmpl:
		package, module = app.split('.')
		m = getClass(package + '.' + module)
		path = m.__file__.split('__init__')[0] + '/xp_templates/' + mode + '/' + tmplName + '.html'
		f = open(path)
		tmpl = f.read()
		f.close()
		cache.set('tmpl/' + app + '/' + mode + '/' + tmplName, tmpl)"""

	return HttpResponse(tmpl)

@ContextDecorator()
def jxService(request, **args):
	"""Excutes the business class: bsClass, method {bsClass: '', method: ''}
	@param request: Request
	@param result: Result"""
	print 'holaaaaaaaaaaaaaaa'
	print 'args: ', args
	logger.debug( 'jxService...' )
	logger.debug( json.dumps(request.REQUEST.items()) )
	request.session.set_test_cookie()
	request.session.delete_test_cookie()
	logger.debug( 'session: ' + json.dumps(request.session.items()) )
	#logger.debug( 'session: %s' % json.dumps(request.session.items()) + ' ' + json.dumps(request.session.session_key) )
	if (request.REQUEST.has_key('view') or request.REQUEST.has_key('action')) and request.is_ajax() == True:
		viewAttrs = {}
		if request.REQUEST.has_key('view'):
			app = request.REQUEST['app']
			view = request.REQUEST['view']
			logger.debug( 'view: ' + view )
			dbView = ViewDAO(args['ctx'])
			impl = dbView.get(application__name=app, name=view).implementation
			# view attributes 
			viewAttrs = json.loads(request.REQUEST['params'])
			args['ctx'].viewNameSource = view
		elif request.REQUEST.has_key('action'):
			app = request.REQUEST['app']
			action = request.REQUEST['action']
			logger.debug( 'action: ' + action )
			dbAction = ActionDAO(args['ctx'])
			dbView = ViewDAO(args['ctx'])
			actionObj = dbAction.get(application__name=app, name=action)
			#if args['ctx'].has_key('viewNameSource') and len(args['ctx']['viewNameSource']) != 0:
			if len(args['ctx'].viewNameSource) != 0:
				# Get view name and check its application code with application code of action
				logger.debug( 'viewNameSource: %s' % (args['ctx'].viewNameSource) )
				viewObj = dbView.get(application__name=app, name=args['ctx'].viewNameSource)
				if actionObj.application.name != viewObj.application.name:
					raise XpMsgException(None, _('Action is not in same application as view source'))
			impl = actionObj.implementation
		implFields = impl.split('.')
		method = implFields[len(implFields)-1]
		classPath = ".".join(implFields[:-1])
		logger.debug('classPath: ' + classPath)
		if method.find('_') == -1 or method.find('__') == -1:
			cls = getClass( classPath ) 
			obj = cls(args['ctx']) #@UnusedVariable
			if (len(viewAttrs) == 0) :
				result = eval('obj.' + method)()
			else:
				result = eval('obj.' + method)(**viewAttrs)
		else:
			logger.debug( 'private methods...' )
			raise Http404
	else:
		logger.debug( 'Unvalid business request' )
		raise Http404
	return result

@ContextViewDecorator()
@ViewTmplDecorator()
def showView(request, app, viewName, viewAttrs, **args):
	"""Show url view. Application code and view name are parsed from the url.
	@param request: Request
	@param app: Application code
	@param viewName: View name
	@return: result"""
	# Get view from viewName
	logger.debug( 'core showView :: context: ' + json.dumps(args['ctx']) )
	db = ViewDAO(args['ctx'])
	#view = db.get(name=viewName)
	view = db.get(application__name=app, name=viewName)
	impl = view.implementation
	# Parse method and class path
	implFields = impl.split('.')
	method = implFields[len(implFields)-1]
	classPath = ".".join(implFields[:-1])
	if viewAttrs.find('-') != -1:
		viewAttrTuple = viewAttrs.split('-')
	else:
		if len(viewAttrs) == 0:
			viewAttrTuple = []
		else:
			viewAttrTuple = [viewAttrs]
	# Instance and call method for view, get result
	if method.find('_') == -1 or method.find('__') == -1:
		cls = getClass( classPath )
		obj = cls(args['ctx']) #@UnusedVariable
		if (len(viewAttrTuple) == 0):	
			result = eval('obj.' + method)()
		else:
			result = eval('obj.' + method)(*viewAttrTuple)
	else:
		logger.debug( 'core :: showView :: private methods...' )
		raise Http404
	return result

@ContextViewDecorator(mode='action')
@ViewTmplDecorator()
def execActionMsg(request, app, actionName, actionAttrs, **args):
	"""Executes an action and shows a message of result of action."""
	db = ActionDAO(args['ctx'])
	action = db.get(application__name=app, name=actionName)
	impl = action.implementation
	implFields = impl.split('.')
	method = implFields[len(implFields)-1] 
	classPath = ".".join(implFields[:-1])
	if actionAttrs.find('-') != -1:
		actionAttrTuple = actionAttrs.split('-')
	else:
		if len(actionAttrs) == 0:
			actionAttrTuple = []
		else:
			actionAttrTuple = [actionAttrs]
	# Instance and call method for view, get result
	if method.find('_') == -1 or method.find('__') == -1:
		cls = getClass( classPath )
		obj = cls(args['ctx']) #@UnusedVariable
		if (len(actionAttrTuple) == 0):	
			result = eval('obj.' + method)()
		else:
			result = eval('obj.' + method)(*actionAttrTuple)
	else:
		logger.debug( 'core :: execAction :: private methods...' )
		raise Http404
	return result
