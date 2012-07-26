import httplib2
import urlparse
import oauth2
import simplejson as json
import types
import traceback

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.http import Http404

from yacaptcha.models import Captcha

from ximpia.core.util import getClass
from models import context, ContextViewDecorator, ContextDecorator
from business import Search, ViewDecorator, XpMsgException
from data import ViewDAO, ActionDAO
import constants as K

from ximpia import settings

def oauth20(request, service):
	"""Doc."""
	print 'GET : ', request.GET
	ContextDict = {
				'service': service,
				'status': '',
				'token': '',
				'tokenSecret': '',
				'errorMessage': ''
				}
	oauthVersion = settings.CONSUMER_DICT[service][2]
	if oauthVersion == '2.0': 
		if request.GET.has_key('code'):
			code = request.GET['code']
			# Exchange code for access token
			print settings.CONSUMER_DICT[service][0] + '  ' + settings.CONSUMER_DICT[service][1]
			url = settings.OAUTH_URL_DICT[service]['access'][0] + '?' + \
				'client_id=' + settings.CONSUMER_DICT[service][0] + \
				'&redirect_uri=' + settings.OAUTH2_REDIRECT + service + \
				'&client_secret=' + settings.CONSUMER_DICT[service][1] + \
				'&code=' + code
			http = httplib2.Http()
			resp, content = http.request(url)
			if resp['status'] == '200':
				responseDict = dict(urlparse.parse_qsl(content))
				accessToken = responseDict['access_token']
				print accessToken
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
	print 'GET : ', request.GET
	# Think about methods in login: LinkedIn, parameters, etc...
	ContextDict = {
				'service': service,
				'status': '',
				'token': '',
				'tokenSecret': '',
				'errorMessage': ''
				}
	print settings.CONSUMER_DICT
	oauthVersion = settings.CONSUMER_DICT[service][2]
	if oauthVersion == '1.0':
		if len(request.GET.keys()) == 0:
			consumerTuple =  settings.CONSUMER_DICT[service]
			consumer = oauth2.Consumer(consumerTuple[0], consumerTuple[1])
			client = oauth2.Client(consumer)
			resp, content = client.request(settings.OAUTH_URL_DICT[service]['request'][0], settings.OAUTH_URL_DICT[service]['request'][1])
			#print resp
			if resp['status'] == '200':
				#print content
				request_token = dict(urlparse.parse_qsl(content))
				print request_token
				request.session['request_token'] = request_token
				# Redirect to linkedin Url
				url = settings.OAUTH_URL_DICT[service]['authorized'][0] + '?oauth_token=' + request_token['oauth_token']
				return HttpResponseRedirect(url)
			else:
				# should show message of error in connecting with network
				ContextDict['status'] = 'ERROR'
		else:
			# Callback : oauth_token and oauth_verifier
			print 'callback...'
			if request.GET.has_key('oauth_token') and request.GET.has_key('oauth_verifier'):
				#oauth_token = request.GET['oauth_token']
				oauth_verifier = request.GET['oauth_verifier']
				request_token = request.session['request_token']
				token = oauth2.Token(request_token['oauth_token'], request_token['oauth_token_secret'])
				token.set_verifier(oauth_verifier)
				consumerTuple =  settings.CONSUMER_DICT[service]
				consumer = oauth2.Consumer(consumerTuple[0], consumerTuple[1])
				client = oauth2.Client(consumer, token)
				resp, content = client.request(settings.OAUTH_URL_DICT[service]['access'][0], "POST")
				access_token = dict(urlparse.parse_qsl(content))
				print 'access_token', access_token
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
		print 'searchHeader...'
		print 'search: ', request.REQUEST['search']
		# What are params in jxSuggestList?????
		ctx = args['ctx']
		searchObj = Search(ctx)
		results = searchObj.search(request.REQUEST['search'])
		print 'results: ', results
	except:
		traceback.print_exc()
	return HttpResponse(json.dumps(results))

@ContextDecorator()
def jxBusiness(request, **args):
	"""Excutes the business class: bsClass, method {bsClass: '', method: ''}
	@param request: Request
	@param result: Result"""
	print 'jxBusiness...'
	print request.REQUEST.items()
	request.session.set_test_cookie()
	request.session.delete_test_cookie()
	print 'session: ', request.session.items()
	#print 'session: ', request.session.items(), request.session.session_key
	if (request.REQUEST.has_key('view') or request.REQUEST.has_key('action')) and request.is_ajax() == True:
		viewAttrs = {}
		if request.REQUEST.has_key('view'):
			app = request.REQUEST['app']
			view = request.REQUEST['view']
			print 'view: ', view
			dbView = ViewDAO(args['ctx'])
			impl = dbView.get(application__code=app, name=view).implementation
			# view attributes 
			viewAttrs = json.loads(request.REQUEST['params'])
			args['ctx']['viewNameSource'] = view
		elif request.REQUEST.has_key('action'):
			app = request.REQUEST['app']
			action = request.REQUEST['action']
			print 'action: ', action
			dbAction = ActionDAO(args['ctx'])
			dbView = ViewDAO(args['ctx'])
			actionObj = dbAction.get(application__code=app, name=action)
			if args['ctx'].has_key('viewNameSource') and len(args['ctx']['viewNameSource']) != 0:
				# Get view name and check its application code with application code of action
				print 'viewNameSource', args['ctx']['viewNameSource']
				viewObj = dbView.get(application__code=app, name=args['ctx']['viewNameSource'])
				if actionObj.application.code != viewObj.application.code:
					raise XpMsgException(None, _('Action is not in same application as view source'))
			impl = actionObj.implementation
		implFields = impl.split('.')
		method = implFields[len(implFields)-1]
		classPath = ".".join(implFields[:-1])
		if method.find('_') == -1 or method.find('__') == -1:
			cls = getClass( classPath ) 
			obj = cls(args['ctx']) #@UnusedVariable
			if (len(viewAttrs) == 0) :
				result = eval('obj.' + method)()
			else:
				result = eval('obj.' + method)(**viewAttrs)
		else:
			print 'private methods...'
			raise Http404
	else:
		print 'Unvalid business request'
		raise Http404
	return result

@ContextViewDecorator()
@ViewDecorator()
def showView(request, app, viewName, viewAttrs, **args):
	"""Show url view. Application code and view name are parsed from the url.
	@param request: Request
	@param app: Application code
	@param viewName: View name
	@return: result"""
	# Get view from viewName
	print 'showView :: app: ', app
	print 'showView :: viewName: ', viewName
	print 'showView :: viewAttrs: ', viewAttrs
	print 'context: ', args['ctx']
	db = ViewDAO(args['ctx'])
	#view = db.get(name=viewName)
	view = db.get(application__code=app, name=viewName)
	impl = view.implementation
	print 'impl: ', impl
	# Parse method and class path
	implFields = impl.split('.')
	method = implFields[len(implFields)-1]
	classPath = ".".join(implFields[:-1])
	print 'method: ', method
	print 'classPath: ', classPath
	if viewAttrs.find('-') != -1:
		viewAttrTuple = viewAttrs.split('-')
	else:
		if len(viewAttrs) == 0:
			viewAttrTuple = []
		else:
			viewAttrTuple = [viewAttrs]
	print 'viewAttrTuple: ', viewAttrTuple
	# Instance and call method for view, get result
	if method.find('_') == -1 or method.find('__') == -1:
		cls = getClass( classPath )
		obj = cls(args['ctx']) #@UnusedVariable
		if (len(viewAttrTuple) == 0):	
			result = eval('obj.' + method)()
		else:
			result = eval('obj.' + method)(*viewAttrTuple)
	else:
		print 'private methods...'
		raise Http404
	return result
