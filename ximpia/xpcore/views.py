# coding: utf-8

import httplib2
import urlparse
import oauth2
import json
import types
import traceback
import os
import datetime
import copy

from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.utils.translation import ugettext as _
from django.http import Http404 

from ximpia.xpcore.util import get_class, AttrDict
from models import context, context_view, ctx, JsResultDict
from service import XpMsgException, view_tmpl, SearchService, TemplateService, CommonService
from data import ViewDAO, ActionDAO, ApplicationDAO

from ximpia.xpsite import constants as KSite
from ximpia.xpsite.models import Setting

settings = get_class(os.getenv("DJANGO_SETTINGS_MODULE"))

# Logging
import logging.config
logging.config.dictConfig(settings.LOGGING)
logger = logging.getLogger(__name__)

def __showView(view, viewAttrs, ctx):
    """Show view. Returns classPath for service class, method and service operation attributes

    ** Attributes **

    * ``view``
    * ``viewAttrs``
    * ``ctx``

    ** Returns **

    * ``(classPath, method, viewAttrTuple):Tuple
    """
    ctx.viewNameSource = view.name
    ctx.path = '/apps/' + view.application.slug + '/' + view.slug
    impl = view.implementation
    # Parse method and class path
    implFields = impl.split('.')
    method = implFields[len(implFields)-1]
    classPath = ".".join(implFields[:-1])
    if viewAttrs.find('/') != -1:
        viewAttrTuple = viewAttrs.split('/')
    else:
        if len(viewAttrs) == 0:
            viewAttrTuple = []
        else:
            viewAttrTuple = [viewAttrs]
    return (classPath, method, viewAttrTuple)

def oauth20(request, service):
    """Doc."""
    logger.debug( 'GET : %s' % (json.dumps(request.GET)) )
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
    logger.debug( 'GET : %s' % (json.dumps(request.GET)) )
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
                logger.debug( 'access_token: %s' % (access_token) )
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
def jxSuggestList(request, **args):
    """Suggest search list"""
    # init
    ctx = args['ctx']
    # Do
    resultList = []
    if request.REQUEST.has_key('dbClass'):
        dbClass = request.REQUEST['dbClass']
        app = request.REQUEST['app']
        logger.debug('jxSuggestList :: search: %s' % (request.REQUEST['search']) )
        logger.debug('jxSuggestList :: path dbClass: %s' % (app + '.data.' + dbClass) )
        cls = get_class( app + '.data.' + dbClass)
        obj = cls(args['ctx']) #@UnusedVariable
        obj.request = request
        params = {}
        if request.REQUEST.has_key('params'):
            params = json.loads(request.REQUEST['params']);
        searchField = request.REQUEST['searchField']
        params[searchField + '__istartswith'] = request.REQUEST['search']
        logger.debug('jxSuggestList :: params: %s' % (params) )
        fields = eval('obj.search')(**params)
        logger.debug('jxSuggestList :: fields: %s' % (fields) )
        fieldValue = None
        if request.REQUEST.has_key('fieldValue'):
            fieldValue = request.REQUEST['fieldValue']
        extraFields = None
        if request.REQUEST.has_key('extraFields'):
            extraFields = json.loads(request.REQUEST['extraFields'])
            logger.debug('jxSuggestList :: extrafields: %s' % (extraFields) )
        for entity in fields:
            dd = {}
            dd['id'] = entity.id
            if fieldValue is None:
                dd['text'] = str(entity)
            else:
                dd['text'] = eval('entity.' + fieldValue)
            if extraFields is not None:
                extraDict = {}
                for extraField in extraFields:
                    extraDict[extraField] = eval('entity.' + extraField)
                dd['extra'] = extraDict
            resultList.append(dd)
    logger.debug('jxSuggestList :: resultList: %s' % (resultList) )
    return HttpResponse(json.dumps(resultList))

@context
def jxSearchHeader(request, **args):
    """Search ximpia for views and actions."""
    try:
        logger.debug( 'searchHeader...' )
        logger.debug( 'search: %s' % (request.REQUEST['search']) )
        # What are params in jxSuggestList?????
        ctx = args['ctx']
        searchObj = SearchService(ctx)
        results = searchObj.search(request.REQUEST['search'])
        logger.debug( 'results: %s' % (json.dumps(results)) )
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

    return HttpResponse(tmpl)

def jxAppTemplate(request, app):
    """

    Get ximpia application template

    **Attributes**

    * ``app``:String : Application

    ** Returns **

    * ``template``:HttpResponse

    """

    service = TemplateService(None)
    tmpl = service.get_app(app)

    return HttpResponse(tmpl)

@context
def jxDataQuery(request, **args):
    """
    Execute data queries for lists with ordering, page and filters.

    ** Attributes **

    * ``request``
    * ``args``

    ** Html Attributes **

    * ``dbClass``:str : Data class name (DAO)
    * ``fields``:list<str> [optional]
    * ``pageStart``:str [optional] [default:1] : Start page number
    * ``pageEnd``:str [optional] : End page number
    * ``orderBy``:tuple<str> [optional]
    * ``method``:str [optional] [default:searchFields]
    * ``args``:dict<str,str> [optional]
    * ``hasOrdering``:bool [optional]
    * ``orderField``:str [optional]

    ** Returns **

    result
    """
    logger.debug( 'jxDataQuery...' )
    logger.debug('jxDataQuery :: args: %s' % (args) )
    logger.debug('jxDataQuery :: REQUEST: %s' % (request.REQUEST) )
    if not request.REQUEST.has_key('dbClass') or not request.REQUEST.has_key('app'):
        raise XpMsgException(AttributeError, _('app and dbClass must be defined.'))
    dbClass = request.REQUEST['dbClass']
    dbApplication = ApplicationDAO(args['ctx'])
    app = request.REQUEST['app']
    application = dbApplication.get(name=app)
    # app: ximpia_site.web, MyDAO => ximpia_site.web.data.MyDAO
    classPath = app + '.data.' + dbClass
    cls = get_class( classPath )
    obj = cls(args['ctx']) #@UnusedVariable
    obj.request = request
    logger.debug('jxDataQuery :: obj: %s' % (obj) )
    # fields
    fields = []
    if request.REQUEST.has_key('fields'):
        fields = json.loads(request.REQUEST['fields'])
    dbArgs = {}
    meta = AttrDict()
    # disablePaging
    dbArgs['disable_paging'] = False
    if request.REQUEST.has_key('disablePaging'):
        dbArgs['disable_paging'] = json.loads(request.REQUEST['disablePaging'])
    if not dbArgs['disable_paging']:
        if request.REQUEST.has_key('pageStart'):
            dbArgs['page_start'] = int(request.REQUEST['pageStart'])
        else:
            dbArgs['page_start'] = 1
        logger.debug('jxDataQuery :: pageStart: %s' % (dbArgs['page_start']) )
    # pageEnd
    if request.REQUEST.has_key('pageEnd') and not dbArgs['disable_paging']:
        dbArgs['page_end'] = int(request.REQUEST['pageEnd'])
    # orderBy
    if request.REQUEST.has_key('orderBy'):
        dbArgs['order_by'] = json.loads(request.REQUEST['orderBy'])
    # args
    if request.REQUEST.has_key('args'):
        requestArgs = json.loads(request.REQUEST['args'])
        for requestArg in requestArgs:
            try:
                dbArgs[requestArg] = json.loads(requestArgs[requestArg])
            except ValueError:
                dbArgs[requestArg] = requestArgs[requestArg]
    # numberResults
    if request.REQUEST.has_key('numberResults'):
        dbArgs['number_results'] = int(request.REQUEST['numberResults'])
    else:
        # Get number results from settings
        dbArgs['number_results'] = int(Setting.objects.get(name__name=KSite.SET_NUMBER_RESULTS_LIST).value)
    logger.debug('jxDataQuery :: numberResults: %s' % (dbArgs['number_results']) )

    # hasOrdering
    if request.REQUEST.has_key('hasOrdering') and request.REQUEST['hasOrdering'] == 'true':
        if request.REQUEST.has_key('orderField'):
            fields.append(request.REQUEST['orderField'])
        else:
            fields.append('order')
    # hasHeader
    hasHeader = False
    if request.REQUEST.has_key('hasHeader'):
        hasHeader = json.loads(request.REQUEST['hasHeader'])
    logger.debug('jxDataQuery :: hasHeader: %s' % (hasHeader) )
    if 'id' not in fields and len(fields) != 0:
        fields.insert(0, 'id')
    logger.debug('jxDataQuery :: fields: %s' % (fields) )
    logger.debug('jxDataQuery :: dbArgs: %s' % (dbArgs) )

    """dbArgs['disablePaging'] = False
    dbArgs['pageStart'] = 1
    dbArgs['pageEnd'] = 1
    dbArgs['numberResults'] = 2"""

    if request.REQUEST.has_key('method'):
        dataListTmp = eval('obj.' + request.REQUEST['method'])(fields, **dbArgs)
    else:
        dataListTmp = obj.search_fields(fields, **dbArgs)
    # numberPages
    if dbArgs['disable_paging'] is not True:
        dbArgsPages = copy.copy(dbArgs)
        if dbArgsPages.has_key('page_start'):
            del dbArgsPages['page_start']
        if dbArgsPages.has_key('page_end'):
            del dbArgsPages['page_end']
        if request.REQUEST.has_key('method'):
            """dataListTmp = eval('obj.' + request.REQUEST['method'])(fields, **dbArgsPages)
            logger.debug('jxDataQuery :: type dataListTmp: %s' % (type(dataListTmp)) )
            meta.numberPages = dataListTmp.count()/numberResults"""
            pass
        else:
            if dbArgsPages.has_key('disable_paging'):
                del dbArgsPages['disable_paging']
            if dbArgsPages.has_key('number_results'):
                numberResults = dbArgsPages['number_results']
                del dbArgsPages['number_results']
            if dbArgsPages.has_key('page_start'): del dbArgsPages['page_start']
            if dbArgsPages.has_key('page_end'): del dbArgsPages['page_end']
            if dbArgsPages.has_key('order_by'): del dbArgsPages['order_by']
            meta.numberPages = int(round(float(obj._model.objects.filter(**dbArgsPages).count())/float(numberResults)))
    else:
        meta.numberPages = 1

    meta.pageStart = 1
    if dbArgs.has_key('page_start'):
        meta.pageStart = dbArgs['page_start']
    if dbArgs.has_key('page_end'):
        meta.pageEnd = dbArgs['page_end']
    else:
        meta.pageEnd = meta.pageStart
    #logger.debug('jxDataQuery :: dataListTmp: %s' % (dataListTmp) )
    dataList = []
    for dbFields in dataListTmp:
        ll = []
        for dbField in dbFields:
            if type(dbField) == datetime.date:
                ll.append(dbField.strftime('%m/%d/%Y'))
            elif type(dbField) == datetime.datetime:
                ll.append(dbField.strftime('%m/%d/%Y %H:%M'))
            elif type(dbField) == datetime.time:
                ll.append(dbField.strftime('%H:%M'))
            else:
                ll.append(dbField)
        dataList.append(ll)
    logger.debug('jxDataQuery :: dataList: %s' % (dataList) )
    # headers
    headers = []
    if hasHeader:
        modelFields = obj._model._meta.fields
        logger.debug('jxDataQuery :: modelFields: %s' % (modelFields) )
        if len(fields) == 0:
            # get all model fields from table and add to headers
            for modelField in modelFields:
                headers.append(modelField.verbose_name)
        else:
            # Get model fields with max level 3: field__field__field
            for field in fields:
                if field.count('__') == 0:
                    headerField = obj._model._meta.get_field_by_name(field)[0].verbose_name
                    logger.debug('jxDataQuery :: headerField: %s' % (headerField) )
                    headers.append(headerField)
                elif field.count('__') == 1:
                    fieldFrom, fieldTo = field.split('__')
                    logger.debug('jxDataQuery :: fieldFrom: %s fieldTo: %s' % (fieldFrom, fieldTo) )
                    """relField = obj._model._meta.get_field_by_name(fieldFrom)[0]\
                        .rel.to._meta.get_field_by_name(fieldTo)[0]"""
                    # 03/07/2013 : We get header name from fk verbose name and not linked to verbose name
                    relField = obj._model._meta.get_field_by_name(fieldFrom)[0]
                    if type(relField.verbose_name) == types.UnicodeType:
                        headerField = relField.verbose_name
                    else:
                        headerField = relField.name
                    logger.debug('jxDataQuery :: headerField: %s' % (headerField) )
                    headers.append(headerField)
                elif field.count('__') == 2:
                    fieldFrom, fieldTo1, fieldTo2 = field.split('__')
                    logger.debug('jxDataQuery :: fieldFrom: %s fieldTo: %s' % (fieldFrom, fieldTo1, fieldTo2) )
                    """relField = obj._model._meta.get_field_by_name(fieldFrom)[0]\
                        .rel.to._meta.get_field_by_name(fieldTo1)[0]\
                        .rel.to._meta.get_field_by_name(fieldTo2)[0]"""
                    # 03/07/2013 : We get header name from fk verbose name and not linked to verbose name
                    relField = obj._model._meta.get_field_by_name(fieldFrom)[0]
                    if type(relField.verbose_name) == types.UnicodeType:
                        headerField = relField.verbose_name
                    else:
                        headerField = relField.name
                    logger.debug('jxDataQuery :: headerField: %s' % (headerField) )
                    headers.append(headerField)
    logger.debug('jxDataQuery :: headers: %s' % (headers) )
    results = {'headers': headers, 'data': dataList, 'meta': meta}
    logger.debug('jxDataQuery :: results: %s' % (results) )
    return HttpResponse(json.dumps(results))

@context
def jxDataSwitchOrder(request, **args):
    """
    Change order in a data table

    ** Attributes **

    * ``request``
    * ``args``

    ** Html Attributes **

    * ``dbClass``:str
    * ``orderCurrent``:str ????
    * ``orderNew``:str
    * ``pk``

    """
    logger.debug('jxDataSwitchOrder...')
    # TODO: Hit master for this operation
    # get current order
    # get list fields from current order to new order
    # new order higher or lower than current order?
    orderCurrent = int(request.REQUEST['orderCurrent'])
    orderNew = int(request.REQUEST['orderCurrent'])
    pk = request.REQUEST['pk']
    dbClass = request.REQUEST['dbClass']
    orderField = 'order'
    if request.REQUEST.has_key('orderField'):
        orderField = request.REQUEST['orderField']
    logger.debug('jxDataSwitchOrder :: pk: %s orderCurrent: %s orderNew: %s dbClass: %s' % (pk, orderCurrent, orderNew, dbClass) )
    dbApplication = ApplicationDAO(args['ctx'])
    app = request.REQUEST['app']
    application = dbApplication.get(name=app)
    # app: ximpia_site.web, MyDAO => ximpia_site.web.data.MyDAO
    classPath = app + '.data.' + dbClass
    cls = get_class( classPath )
    obj = cls(args['ctx']) #@UnusedVariable 
    item = obj.get(pk=pk)
    logger.debug('jxDataSwitchOrder :: change order : %s -> %s' % (orderCurrent, orderNew) )
    item.__setattr__(orderField, orderNew)
    orderDbCurrent = eval('item.' + orderField)
    logger.debug('jxDataSwitchOrder :: orderDbCurrent: %s' % (orderDbCurrent) )
    if orderCurrent != orderDbCurrent:
        raise XpMsgException(None, _('Sorting error. Please retry later. Thanks'))
    if orderNew > orderCurrent:
        # Moving down the list
        logger.debug('jxDataSwitchOrder :: Moving down the list...')
        itemsToUpdate = obj.objects.filter(order__gt = orderCurrent, order__lte = orderNew).values()
        logger.debug('jxDataSwitchOrder :: itemsToUpdate. %s' % (itemsToUpdate))
        for itemToUpdate in itemsToUpdate:
            logger.debug('jxDataSwitchOrder :: Move down: %s -> %s' % (itemToUpdate[orderField], itemToUpdate[orderField]-1) )
            itemToUpdate[orderField] -= 1
            itemToUpdate.save()
    else:
        # Moving up the list
        logger.debug('jxDataSwitchOrder :: Moving up the list...')
        itemsToUpdate = obj.objects.filter(order__gt = orderNew, order__lt = orderCurrent).values()
        logger.debug('jxDataSwitchOrder :: itemsToUpdate. %s' % (itemsToUpdate))
        for itemToUpdate in itemsToUpdate:
            logger.debug('jxDataSwitchOrder :: Move up: %s -> %s' % (itemToUpdate[orderField], itemToUpdate[orderField]+1) )
            itemToUpdate[orderField] += 1
            itemToUpdate.save()
    logger.debug('jxDataSwitchOrder :: finished!!!')
    return HttpResponse(json.dumps('OK'))

@ctx()
@transaction.commit_on_success
def jxService(request, **args):
    """Excutes the business class: bsClass, method {bsClass: '', method: ''}
    @param request: Request
    @param result: Result"""
    logger.debug( 'jxService...' )
    #raw_input('Continue???')
    #time.sleep(1.5)
    logger.debug( json.dumps(request.REQUEST.items()) )
    request.session.set_test_cookie()
    request.session.delete_test_cookie()
    #logger.debug( 'session: %s' % (json.dumps(request.session.items())) )
    #logger.debug( 'session: %s' % json.dumps(request.session.items()) + ' ' + json.dumps(request.session.session_key) )
    if (request.REQUEST.has_key('view') or request.REQUEST.has_key('action')) and request.is_ajax() is True:
        viewAttrs = {}
        dbApplication = ApplicationDAO(args['ctx'])
        app = request.REQUEST['app']
        application = dbApplication.get(name=app)
        if request.REQUEST.has_key('view'):
            view = request.REQUEST['view']
            logger.debug( 'view: %s' % (view) )
            dbView = ViewDAO(args['ctx'])
            viewObj = dbView.get(application__name=app, name=view)
            args['ctx'].viewAuth = viewObj.hasAuth
            impl = viewObj.implementation
            # view attributes
            viewAttrs = json.loads(request.REQUEST['params'])
            args['ctx'].viewNameSource = view
            args['ctx'].path = '/apps/' + application.slug + '/' + viewObj.slug
        elif request.REQUEST.has_key('action'):
            action = request.REQUEST['action']
            logger.debug( 'action: %s' % (action) )
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
            args['ctx'].path = '/apps/' + application.slug + '/do/' + actionObj.slug
        implFields = impl.split('.')
        method = implFields[len(implFields)-1]
        classPath = ".".join(implFields[:-1])
        logger.debug('classPath: %s' % (classPath) )
        if method.find('_') == -1 or method.find('__') == -1:
            cls = get_class(classPath)
            obj = cls(args['ctx'])
            super(cls, obj).__init__(args['ctx'])
            obj.request = request
            if (len(viewAttrs) == 0):
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

@ctx()
@transaction.commit_on_success
def jxSave(request, **args):
    """
    Save register. Operation executed when clicking on "Save" button on forms. Saves all instances related to forms, included
    many to many relationships.

    ** Attributes **

    * ``request``
    * ``**args``
    """
    logger.debug( 'jxSave...' )
    logger.debug( json.dumps(request.REQUEST.items()) )
    request.session.set_test_cookie()
    request.session.delete_test_cookie()
    if (request.REQUEST.has_key('action')) and request.is_ajax() == True:
        action = request.REQUEST['action']
        logger.debug( 'action: %s' % (action) )
        if action == 'save':
            # resolve form, set to args['ctx'].form
            logger.debug('jxSave :: form: %s' % (request.REQUEST['form']) )
            formId = request.REQUEST['form']
            app = request.REQUEST['app']
            formModule = getattr(getattr(__import__(app.split('.')[0]), app.split('.')[1]), 'forms')
            classes = dir(formModule)
            resolvedForm = None
            for myClass in classes:
                try:
                    formIdTarget = eval('formModule.' + myClass + '._XP_FORM_ID')
                    if formIdTarget == formId:
                        resolvedForm = eval('formModule.' + myClass)
                except AttributeError:
                    pass
            logger.debug('jxSave :: resolvedForm: %s' % (resolvedForm) )
            # Instantiate form, validate form
            logger.debug('jxSave :: post: %s' % (args['ctx'].post) )
            # instantiate form for create and update with db instances dbObjects from form
            # dbObjects : pk, model
            instances = {}
            dbObjects = json.loads(args['ctx'].post['dbObjects'].replace("'", '"'))
            logger.debug('jxSave :: dbObjects: %s' % (dbObjects) )
            # TODO: In case we support more masters than 'default', resolve appropiate master db name
            for key in dbObjects:
                # Get instance model by pk
                impl = dbObjects[key]['impl']
                cls = get_class( impl )
                instances[key] = cls.objects.using('default').get(pk=dbObjects[key]['pk'])
            logger.debug('jxSave :: instances. %s' % (instances) )
            if len(instances) == 0:
                args['ctx'].form = resolvedForm(args['ctx'].post, ctx=args['ctx'])
            else:
                args['ctx'].form = resolvedForm(args['ctx'].post, ctx=args['ctx'], instances=instances)
            logger.debug('jxSave :: instantiated form')
            args['ctx'].jsData = JsResultDict()
            isFormValid = args['ctx'].form.is_valid()
            #isFormValid = False
            logger.debug('jxSave :: isFormValid: %s' % (isFormValid) )
            obj = CommonService(args['ctx'])
            obj.request = request
            if isFormValid == True:
                obj._setMainForm(args['ctx'].form)
                result = obj.save()
            else:
                if settings.DEBUG == True:
                    logger.debug( 'Validation error!!!!!' )
                    logger.debug( args['ctx'].form.errors )
                    if args['ctx'].form.errors.has_key('invalid'):
                        logger.debug( args['ctx'].form.errors['invalid'] )
                    traceback.print_exc()
                if args['ctx'].form.errors.has_key('invalid'):
                    errorDict = {'': args['ctx'].form.errors['invalid'][0]}
                    logger.debug( 'errorDict: %s' % (errorDict) )
                    result = obj._buildJSONResult(obj._getErrorResultDict(errorDict, pageError=True))
                else:
                    # Build errordict
                    errorDict = {}
                    for field in args['ctx'].form.errors:
                        if field != '__all__':
                            errorDict[field] = args['ctx'].form.errors[field][0]
                    logger.debug( 'errorDict: %s' % (errorDict) )
                    result = obj._buildJSONResult(obj._getErrorResultDict(errorDict, pageError=False))
                return result
        else:
            logger.debug( 'Invalid action name. Only save is allowed' )
            raise Http404
    else:
        logger.debug( 'Unvalid business request' )
        raise Http404
    return result

@ctx()
@transaction.commit_on_success
def jxDelete(request, **args):
    """
    Deletes registers associated to form. In case more than one instance associated to form, button must define instances to delete.

    This operation is executed when "Delete" button is clicked on forms.

    Deletes the register by pk: dbInstance.objects.get(pk=myPk).delete()

    ** Attributes **

    * ``request``
    * ``**args``
    """
    logger.debug('jxDelete ...')
    logger.debug('jxDelete :: args: %s' % (args) )
    request.session.set_test_cookie()
    request.session.delete_test_cookie()
    if (request.REQUEST.has_key('action')) and request.is_ajax() == True:
        action = request.REQUEST['action']
        logger.debug( 'action: %s' % (action) )
        if action == 'delete':
            # resolve form, set to args['ctx'].form
            logger.debug('jxDelete :: form: %s' % (request.REQUEST['form']) )
            formId = request.REQUEST['form']
            app = request.REQUEST['app']
            formModule = getattr(getattr(__import__(app.split('.')[0]), app.split('.')[1]), 'forms')
            classes = dir(formModule)
            resolvedForm = None
            for myClass in classes:
                try:
                    formIdTarget = eval('formModule.' + myClass + '._XP_FORM_ID')
                    if formIdTarget == formId:
                        resolvedForm = eval('formModule.' + myClass)
                except AttributeError:
                    pass
            logger.debug('jxDelete :: resolvedForm: %s' % (resolvedForm) )
            args['ctx'].form = resolvedForm(args['ctx'].post, ctx=args['ctx'])
            args['ctx'].jsData = JsResultDict()
            # Instantiate form, validate form
            logger.debug('jxDelete :: post: %s' % (args['ctx'].post) )
            # instantiate form for create and update with db instances dbObjects from form
            # dbObjects : pk, model
            obj = CommonService(args['ctx'])
            obj._setMainForm(args['ctx'].form)
            obj.request = request
            result = obj.delete()
        else:
            logger.debug( 'Invalid action name. Only save is allowed' )
            raise Http404
    else:
        logger.debug( 'Unvalid business request' )
        raise Http404
    return result

@context_view()
@view_tmpl()
def showView(request, appSlug, viewSlug, viewAttrs, **args):
    """
    Show url view. Application code and view name are parsed from the url.

    **Required Attributes**

    **Optional Attributes**

    **Returns**

    """
    #logger.debug( 'xpcore showView :: context: %s' % (json.dumps(args['ctx'])) )
    dbApplication = ApplicationDAO(args['ctx'])
    application = dbApplication.get(slug=appSlug)
    db = ViewDAO(args['ctx'])
    view = db.get(application=application, slug=viewSlug)
    args['ctx'].viewAuth = view.hasAuth
    classPath, method, viewAttrTuple = __showView(view, viewAttrs, args['ctx'])
    if method.find('_') == -1 or method.find('__') == -1:
        logger.debug('showView :: classPath: %s method: %s viewAttrTuple: %s' % (classPath, method, viewAttrTuple))
        cls = get_class( classPath ) 
        obj = cls(args['ctx'])
        super(cls, obj).__init__(args['ctx'])
        obj.request = request
        if (len(viewAttrTuple) == 0):
            result = eval('obj.' + method)()
        else:
            result = eval('obj.' + method)(*viewAttrTuple)
    else:
        logger.debug( 'xpcore :: showView :: private methods...' )
        raise Http404
    return result

@transaction.commit_on_success
@context_view(mode='action')
@view_tmpl()
def execActionMsg(request, appSlug, actionSlug, actionAttrs, **args):
    """
    Executes an action and shows a message of result of action.
    """
    logger.debug('appslug: %s actionslug: %s actionAttrs: %s' % (appSlug, actionSlug, actionAttrs) )
    dbApplication = ApplicationDAO(args['ctx'])
    application = dbApplication.get(slug=appSlug)
    db = ActionDAO(args['ctx'])
    action = db.get(application=application, slug=actionSlug)
    impl = action.implementation
    implFields = impl.split('.')
    method = implFields[len(implFields)-1]
    classPath = ".".join(implFields[:-1])
    args['ctx'].path = '/apps/' + application.slug + '/' + action.slug
    if actionAttrs.find('/') != -1:
        actionAttrTuple = actionAttrs.split('/')
    else:
        if len(actionAttrs) == 0:
            actionAttrTuple = []
        else:
            actionAttrTuple = [actionAttrs]
    # Instance and call method for view, get result
    if method.find('_') == -1 or method.find('__') == -1:
        cls = get_class( classPath )
        obj = cls(args['ctx'])
        super(cls, obj).__init__(args['ctx'])
        obj.request = request
        if (len(actionAttrTuple) == 0):
            result = eval('obj.' + method)()
        else:
            result = eval('obj.' + method)(*actionAttrTuple)
    else:
        logger.debug( 'xpcore :: execAction :: private methods...' )
        raise Http404
    return result
