import facebook
import oauth2
import urlparse
import simplejson as json
import httplib2
import types
import time
import imp

from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpRequest, HttpResponseServerError, HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import Context, loader, Template, RequestContext
from django.core.urlresolvers import reverse
from django.core.context_processors import auth, csrf
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User, Group
from django.utils import translation
from django.utils.translation import ugettext as _

#from models import Invitation
from ximpia.core.models import context, Context, XpTemplate, getResultOK, Context as Ctx, JsResultDict, XpMsgException
#from choices import Choices
#from constants import Constants
#from messages import MsgSignup
#from data import *
#from choices import Choices
import forms
#from constants import Constants

from data import UserDAO
from models import Invitation

#from ximpia import util
from ximpia.util.http import Request
from ximpia.util.content import getContentRelaseDict

from ximpia import settings
from yacaptcha.models import Captcha

from business import SignupBusiness, LoginBusiness
#from data import UserDAO
#from constants import Constants
#from sqlalchemy.util import deprecated

from constants import Constants as K

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
		for tuple in nameList:
			name, value = tuple
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
			result = eval(action)(request, form)
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
		list = json.loads(request.POST['jsonData'])
		if len(list) == 1:
			action, parameterList, parameterDict = list[0]
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
			list = json.loads(request.POST['jsonData'])
			for tuple in list:
				action, parameterList, parameterDict = tuple
				result = eval(action)(parameterList, parameterDict)
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
			list = json.loads(request.POST['jsonData'])['jsonDataList']
			for tuple in list:
				action, parameterList, parameterDict = tuple
				resultTmp = eval(action)(*parameterList, **parameterDict)
				if type(resultTmp) == types.ListType:
					listResult = []
					for entity in resultTmp:
						dict = entity.values()
						listResult.append(dict)
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
	print 'jxBusiness...'
	ctx = argsDict['ctx']
	print request.REQUEST.items()
	if request.REQUEST.has_key('bsClass') and request.is_ajax() == True:
		bsClass = request.REQUEST['bsClass'];
		method = request.REQUEST['method']
		if method.find('_') == -1 or method.find('__') == -1: 
			obj = eval(bsClass)(ctx)
			result = eval('obj.' + method)()
		else:
			print 'private methods...'
			raise Http404
	else:
		print 'Unvalid business request'
		raise Http404
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
		list = eval('obj.filter')(*[], **params)
		for entity in list:
			dict = {}
			dict['id'] = entity.id
			dict['text'] = entity.getText()
			resultList.append(dict) 
	return HttpResponse(json.dumps(resultList))


######################################################################
# Signup
######################################################################

def __buildResultDict():
	dict = {}
	dict['status'] = ''
	dict['errors'] = []
	dict['response'] = ''
	return dict

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

@Context
def signup(request, invitationCode=None, **argsDict):
	"""Sign up professional account"""
	# init
	ctx = argsDict['ctx']
	dbUser = UserDAO(ctx)
	# start
	signup = SignupBusiness(ctx)
	if request.method == 'POST':
		# POST
		ctx['form'] = forms.UserSignupForm(ctx['post'])
		ctx['captcha'] = Captcha(request).get()
		bForm = ctx['form'].is_valid()
		print 'bForm : ', bForm, ctx['form'].errors, ctx['form']._errors
		signup = SignupBusiness(ctx)
		try:
			result = signup.doUser(ctx)
		except XpMsgException:
			errorDict = signup.getErrors()
			if len(errorDict) != 0:
				result = signup.buildJSONResult(signup.getErrorResultDict(errorDict))
			else:
				raise
		print result
	else:
		#signup.doGet()
		try:
			affiliateId = Request.getReqParams(request, ['aid:int'])[0]
			invitation = dbUser.getInvitation(invitationCode, status=K.PENDING)
			ctx['form'] = forms.UserSignupForm(instances = {'dbInvitation': invitation})
			jsData = getResultOK({})
			ctx['form'].buildJsData(jsData)
			jsData['response']['affiliateId'] = affiliateId
			#print invitation.invitationCode, jsData['response']['form_signup']['invitationCode']
			result = signup.buildJSONResult(jsData)
			#print 'keys : ', jsData['response']['form_signup'].keys()
			#print result
		except Invitation.DoesNotExist:
			raise Http404
	return result

@Context
@XpTemplate({'main': 'social_network/signup/signupOrganization.html'})
def signupOrganization(request, invitationCode=None, **argsDict):
	"""Sign up professional account"""
	# init
	ctx = argsDict['ctx']
	tmplDict = argsDict['tmplDict']
	dbUser = UserDAO(ctx)
	# start
	print 'invitationCode:', invitationCode
	bFacebookLogin = False 
	ctx['auth'] = {'facebook': False}
	if request.COOKIES.has_key(settings.FACEBOOK_APP_COOKIE):
		ctx['auth']['facebook'] = True
		bFacebookLogin = True	
	if request.method == 'POST':
		# POST
		form = forms.FrmOrganizationSignup(request.POST)
		captcha=Captcha(request).get()
		# Business
		signup = SignupBusiness(ctx, request)
		result = signup.doOrganization(form, captcha, bFacebookLogin)
		print result
	else:
		# GET
		#template = 'social_network/signup/signupOrganization.html'
		try:
			affiliateId = Request.getReqParams(request, ['aid:int'])[0]
			print 'affiliateId : ', affiliateId
			invitation = dbUser.getInvitation(invitationCode, status=K.PENDING)
			if settings.PRIVATE_BETA == True and affiliateId == None:
				ctx['showInvitation'] = True
			else:
				ctx['showInvitation'] = False
			# Captcha
			Captcha(request).create()
			# Facebook
			profileDict = {}
			fbAccessToken = ''
			if bFacebookLogin:
				fbUserDict = facebook.get_user_from_cookie(request.COOKIES, settings.FACEBOOK_APP_ID, settings.FACE_APP_SECRET)
				fbAccessToken = fbUserDict['access_token']
				graph = facebook.GraphAPI(fbAccessToken)
				profileDict = graph.get_object("me");				
				ctx['auth']['facebook'] = True
			ctx['form'] = forms.OrganizationSignupForm()
			#ctx['form'].buildInitialShow(invitationCode, invitation, profileDict, fbAccessToken)		
			ctx['affiliateId'] = affiliateId
			result = render_to_response(tmplDict['main'], RequestContext(request, ctx))
		except Invitation.DoesNotExist, facebook.GraphAPIError:
			raise Http404
	return result

@Context
def activateAccount(request, user, activationCode, **argsDict):
	"""Activate account, either professional or organization"""
	# init
	ctx = argsDict['ctx']
	# start
	signup = SignupBusiness(ctx)
	resultDict = signup.activateAccount(user, activationCode)
	if resultDict['status'] == 'OK':
		# login user
		# Redirect to Ximpia home
		result = HttpResponse('OK')
	else:
		# assume spammer
		raise Http404
	return result


# ===========================================================================================================


# *******************************
# ****     Server Content     ***
# *******************************

@Context
def changePassword(request, userAccount, **argsDict):
	"""View to show change password form. User will enter new password and click save. New password then would be saved
	and user logged in"""
	print 'changePassword...'
	login = LoginBusiness(argsDict['ctx'])
	login.showNewPassword(userAccount)
	result = render_to_response('social_network/login/changePassword.html', RequestContext(request, argsDict['ctx']))
	return result

@Context
def signupUser(request, invitationCode, **argsDict):
	"""Signup user with invitation."""
	print 'signupUser...'
	affiliateId = Request.getReqParams(request, ['aid:int'])[0]
	signup = SignupBusiness(argsDict['ctx'])
	signup.showSignupUser(invitationCode, affiliateId)
	result = render_to_response('social_network/signup/signupUser.html', RequestContext(request, argsDict['ctx']))
	return result
