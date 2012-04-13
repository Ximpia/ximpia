import oauth2
import urlparse
import simplejson as json
import httplib2
import types
import traceback

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import login, authenticate
from django.utils import translation
from django.utils.translation import ugettext as _

from ximpia.core.models import context, Context
from ximpia.core.data import ActionDAO, ViewDAO

from business import SignupView, LoginView
from business import SignupAction, LoginAction
from constants import Constants as K
import forms

from ximpia.util.http import Request
from ximpia.util.content import getContentRelaseDict

from ximpia import settings
from yacaptcha.models import Captcha

def test(request):
	return HttpResponse("OK")

def staticContent(request, templateName='index', **argsDict):
	"""Deliver static content. Allows passing variables through optional argsDict."""
	print 'templateName : ', templateName
	lang = translation.get_language()
	# template
	template = 'social_network' + '/' + templateName + '.html'
	# Show html
	"""ContextDict = { 
				'rel_d': util.content.getContentRelaseDict(request.session.theme)
				}"""
	ContextDict = {
				'request': request,
				'lang': lang
				}
	if len(argsDict) != 0:
		nameList = argsDict.items()
		for fields in nameList:
			name, value = fields
			ContextDict[name] = value
	Result = render_to_response(template, ContextDict)
	return Result

def formContent(request, templateName):
	"""Delivers form content. Supports either GET and POST methods. When GET is received, we show blank form. When POST is received
	we call business action (bsAction)."""
	lang = request.session.lang
	template = 'social_network' + '/' + lang + '/' + templateName + '.html'
	ContextDict = {
				'lang': lang, 
				'rel_d': getContentRelaseDict(request.session.theme)
				}
	if request.method == 'POST':
		form = forms.FrmUserSignup(request.POST)
		check = form.isValid()
		ContextDict['form'] = form
		if check:
			action = request.POST['bsAction']
			eval(action)(request, form)
			ContextDict['message'] = _('OK, we did it.')
		else:
			ContextDict['message'] = _('There was an error in processing the action. Please check your data and try again.')
	else:
		form = forms.FrmOrganizationSignup()
		ContextDict['form'] = form
	Result = render_to_response(template, ContextDict)
	return Result

def doLogin(request):
	"""Perform login action. Returns OK or ERROR_AUTH"""
	sPassword = request.POST['password']
	sUser = request.POST['ximpiaId']
	user = authenticate(username=sUser, password=sPassword)
	if user:
		login(request, user)
		code = 'OK'
	else:
		code = 'ERROR_AUTH'
	return HttpResponse(code)


###############################################################
#  AJAX
###############################################################

def jxContent(request, templateName):
	"""AJAX html content. jsonData must have only one field. It calls the business action and renders response in html template."""
	lang = request.session.lang
	try:
		fields = json.loads(request.POST['jsonData'])
		if len(fields) == 1:
			action, parameterList, parameterDict = fields[0]
			result = eval(action)(parameterList, parameterDict)
			template = 'social_network' + '/' + lang + '/' + templateName + '.html'
			ContextDict = {
				'result': result,
				'lang': lang, 
				'rel_d': getContentRelaseDict(request.session.theme)
				}
			Result = render_to_response(template, ContextDict)
		else:
			Result = 'ERROR'
	except:
		Result = 'ERROR'
	return Result

def jxAction(request):
	"""Sequence of actions are executed. Returns either OK or ERROR. jsonData has list of fields action,argsTuple, argsDict."""
	if request.POST.has_key('jsonData'):
		try:
			data = json.loads(request.POST['jsonData'])
			for fields in data:
				action, parameterList, parameterDict = fields
				eval(action)(parameterList, parameterDict)
				code = 'OK'
		except:
			code = 'ERROR'
	else:
		code = 'ERROR'
	return HttpResponse(code)

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

@Context
def jxBusiness(request, *argsTuple, **argsDict):
	"""Excutes the business class: bsClass, method {bsClass: '', method: ''}
	@param request: Request
	@param result: Result"""
	try:
		print 'jxBusiness...'
		ctx = argsDict['ctx']
		print request.REQUEST.items()
		if (request.REQUEST.has_key('view') or request.REQUEST.has_key('action')) and request.is_ajax() == True:
			#bsClass = request.REQUEST['bsClass'];
			#method = request.REQUEST['method']
			if request.REQUEST.has_key('view'):
				view = request.REQUEST['view']
				print 'view: ', view
				dbView = ViewDAO(ctx)
				impl = dbView.get(application__code=K.APP, name=view).implementation
			elif request.REQUEST.has_key('action'):
				action = request.REQUEST['action']
				print 'action: ', action
				dbAction = ActionDAO(ctx)
				impl = dbAction.get(application__code=K.APP, name=action).implementation
			print 'Implementation: ', impl
			implFields = impl.split('.')
			method = implFields[len(implFields)-1]
			bsClass = implFields[len(implFields)-2]
			print 'method: ', method, type(method)
			print 'class: ', bsClass, type(bsClass)
			if method.find('_') == -1 or method.find('__') == -1: 
				obj = eval(bsClass)(ctx)
				result = eval('obj.' + method)()
			else:
				print 'private methods...'
				raise Http404
		else:
			print 'Unvalid business request'
			raise Http404
	except Exception as e:
		if settings.DEBUG == True:
			traceback.print_exc()
		raise
	return result

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
		obj = eval(dbClass)(ctx)
		fields = eval('obj.filter')(*[], **params)
		for entity in fields:
			dd = {}
			dd['id'] = entity.id
			dd['text'] = entity.getText()
			resultList.append(dd) 
	return HttpResponse(json.dumps(resultList))


######################################################################
# Signup
######################################################################

def __buildResultDict():
	dd = {}
	dd['status'] = ''
	dd['errors'] = []
	dd['response'] = ''
	return dd

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

# ===========================================================================================================


# *******************************
# ****     Server Content     ***
# *******************************

@Context
def changePassword(request, ximpiaId, reminderId, **argsDict):
	"""View to show change password form. User will enter new password and click save. New password then would be saved
	and user logged in"""
	print 'changePassword...'
	login = LoginView(argsDict['ctx'])
	login.showNewPassword(ximpiaId, reminderId)
	result = render_to_response('social_network/login/changePassword.html', RequestContext(request, argsDict['ctx']))
	return result

@Context
def signupUser(request, invitationCode, **argsDict):
	"""Signup user with invitation."""
	print 'signupUser...'
	affiliateId = Request.getReqParams(request, ['aid:int'])[0]
	signup = SignupView(argsDict['ctx'])
	signup.showSignupUser(invitationCode, affiliateId)
	result = render_to_response('social_network/signup/signupUser.html', RequestContext(request, argsDict['ctx']))
	return result
