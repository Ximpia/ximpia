# coding: utf-8

import random
import os
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User

from models import XpMsgException, CoreParam, Application, Action
from models import Menu, MenuParam, View, Workflow, Param, WFParamValue, WorkflowData, ServiceMenu
from models import WorkflowView, ViewMenu, SearchIndex, SearchIndexParam, Word, SearchIndexWord, XpTemplate, ViewTmpl, ServiceMenuCondition
from models import ViewMenuCondition, ApplicationMedia
from models import Context, JsResultDict

from ximpia.xpsite.models import Setting

# Settings
from ximpia.xpcore.util import get_class
settings = get_class(os.getenv("DJANGO_SETTINGS_MODULE"))

# Logging
import logging.config
logging.config.dictConfig(settings.LOGGING)
logger = logging.getLogger(__name__)

class CommonDAO(object):    

    _numberMatches = 0
    _ctx = None
    model = None
    _relatedFields = ()
    _relatedDepth = None

    def __init__(self, ctx, related_fields=(), related_depth=None, number_matches=100):
        """@param ctx: Context: 
        @param related_fields: tuple containing the fields to fetch data in the same query
        @param related_depth: Number of depth relationships to follow. The higher the number, the bigger the query
        @param number_matches: Number of rows for queries that support paging
        """
        self._ctx = ctx
        self._relatedFields = related_fields
        self._relatedDepth = related_depth
        self._numberMatches = number_matches 
        if related_depth != None and len(related_fields) != 0:
            raise XpMsgException(None, _('relatedFields and relatedDepth cannot be combined. One of them must only be informed.'))
    
    def _processRelated(self):
        """Process related objects using fields and depth, class attributes _relatedFields and _relatedDepth"""
        if len(self._relatedFields) != 0 or self._relatedDepth != None:
            if len(self._relatedFields) != 0:
                dbObj = self.model.objects.select_related(self._relatedFields)
            elif self._relatedDepth != None:
                dbObj = self.model.objects.select_related(depth=self._relatedDepth)
        else:
            dbObj = self.model.objects
        return dbObj
        
    def _cleanDict(self, dd):
        """Clean dict removing xpXXX fields.
        @param dict: Dictionary
        @return: dictNew : New dictionary without xpXXX fields"""
        fields = dd.keys()
        dictNew = {}
        for sKey in fields:
            if sKey.find('xp') == 0:
                pass
            else:
                dictNew[sKey] = dd[sKey]
        return dictNew
    
    def _getPagingStartEnd(self, page, numberMatches):
        """Get tuple (iStart, iEnd)"""
        iStart = (page-1)*numberMatches
        iEnd = iStart+numberMatches
        values = (iStart, iEnd)
        return values
    
    def _getCtx(self):
        """Get context"""
        return self._ctx

    def _doManyById(self, model, idList, field):
        """Does request for map for list of ids (one query). Then processes map and adds to object obtained objects.
        @param idList: List
        @param object: Model"""
        xpDict = self.getMap(idList, userModel=model)
        for idTarget in xpDict.keys():
            addModel = xpDict[idTarget]
            field.add(addModel)
    
    def _doManyByName(self, model, nameList, field):
        """Does request for map for list of ids (one query). Then processes map and adds to object obtained objects.
        @param idList: List
        @param object: Model"""
        for value in nameList:
            fields = model.objects.get_or_create(name=value)
            nameModel = fields[0]
            field.add(nameModel)
    
    def _resolveDbName(self):
        """Resolves the db name to use. Supports multiple masters and multiple slaves. Views use slaves. Actions use masters.
        Data about view or action is obtained from the context."""
        #TODO: Include application mapping with settings variable XIMPIA_DATABASE_APPS = {}
        # Build master and slave lists
        if self._ctx.dbName == None:
            dbList = settings.DATABASES.keys()
            dbListMaster = []
            dbListSlave = []
            for dbNameI in dbList:
                if dbNameI == 'default' or dbNameI.find('master') == 0:
                    dbListMaster.append(dbNameI)
                elif dbNameI.find('slave') == 0:
                    dbListSlave.append(dbNameI)
            dbName = ''
            if self._ctx.isView == True:
                if len(dbListSlave) != 0:
                    dbName = random.choice(dbListSlave)
                else:
                    dbName = 'default'
            elif self._ctx.isAction == True:
                dbName = random.choice(dbListMaster)
        else:
            dbName = self._ctx.dbName
        logger.debug('CommonDAO :: dbName: %s view: %s' % (dbName, self._ctx.viewNameSource) )
        return dbName
    
    def _getSetting(self, settingName):
        """
        Get setting model instance.
        
        ** Attributes ** 
        
        * ``settingName``:String : Setting name
        
        ** Returns **
        
        models.site.Setting model instance
        """
        setting = Setting.objects.get(name__name=settingName).value
        return setting
    
    def get_map(self, id_list):
        """Get object map for a list of ids 
        @param idList: 
        @param bFull: boolean : Follows all foreign keys
        @return: Dict[id]: object"""
        dd = {}
        if len(id_list) != 0:
            dbObj = self._processRelated()
            fields = dbObj.using(self._resolveDbName()).filter(id__in=id_list)
            for obj in fields:
                dd[obj.id] = obj
        return dd
    
    def get_by_id(self, field_id):
        """Get model object by id
        @param field_id: Object id
        @return: Model object"""
        try:
            dbObj = self._processRelated()
            obj = dbObj.using(self._resolveDbName()).get(id=field_id)
        except Exception as e:
            raise XpMsgException(e, _('Error in get object by id ') + str(field_id) + _(' in model ') + str(self.model), 
                                origin='data')
        return obj
    
    def check(self, **qs_args):
        """Checks if object exists
        @param qs_args: query arguments
        @return: Boolean"""
        try:
            dbObj = self.model.objects
            exists = dbObj.using(self._resolveDbName()).filter(**qs_args).exists()
        except Exception as e:
            raise XpMsgException(e, _('Error in check object. Args: ') + str(qs_args) + _(' in model ') + str(self.model), 
                                origin='data')
        return exists
    
    def get(self, **qs_args):
        """Get object
        @param qs_args: query arguments
        @return: Model Object"""
        try:
            logger.debug('dbName:' + self._resolveDbName())
            dbObj = self._processRelated()
            data = dbObj.using(self._resolveDbName()).get(**qs_args)
        except Exception as e:
            raise XpMsgException(e, _('Error in get object. Args: ') + str(qs_args) + _(' in model ') + str(self.model), 
                                origin='data')
        return data    

    def save(self):
        """Save database object, either insert or update"""
        try:
            self.model.save(using=self._resolveDbName())
        except Exception as e:
            raise XpMsgException(e, _('Error in save model ') + str(self.model), 
                                origin='data')
        return self.model
    
    def search(self, *qs_tuple, **qs_args):
        """Search model using filter. Support for related objects as FK to model"""
        #try:
        dbObj = self._processRelated()
        filterList = dbObj.using(self._resolveDbName()).filter(*qs_tuple, **qs_args)
        """except Exception as e:
            raise XpMsgException(e, _('Error in search operation. qs_tuple: ') + str(qs_tuple) + ' . Args: ' + str(qs_args) + _(' in model ') + str(self.model), 
                                origin='data')"""
        return filterList
    
    def create(self, **qs_args):
        """Create object
        @param qs_args: Query arguments
        @return: Data Object"""
        try:
            dbObj = self.model.objects
            data = dbObj.using(self._resolveDbName()).create(**qs_args)
        except Exception as e:
            raise XpMsgException(e, _('Error in create object. Args: ') + str(qs_args) + _(' in model ') + str(self.model), 
                                origin='data')
        return data
    
    def get_create(self, **qs_args):
        """Get or create object. If exists, gets the current value. If does not exist, creates data.
        @param qs_args: Query arguments
        @return: tuple (Data Object, bCreated)"""
        try:
            dbObj = self.model.objects
            xpTuple = dbObj.using(self._resolveDbName()).get_or_create(**qs_args)
        except Exception as e:
            raise XpMsgException(e, _('Error in get or create object. Args: ') + str(qs_args) + _(' in model ') + str(self.model), 
                                origin='data')
        return xpTuple
    
    def delete_by_id(self, pk, is_real=False):
        """Delete model object by id
        @param id: Object id
        @return: Model object"""
        try:
            if is_real == False:
                xpObject = self.model.objects.using(self._resolveDbName()).get(id=pk)
                xpObject.isDeleted = True
                xpObject.save(using=self._resolveDbName())
            else:
                xpObject = self.model.objects_del.using(self._resolveDbName()).get(id=pk)
                xpObject.delete()
        except Exception as e:
            raise XpMsgException(e, _('Error delete object by id ') + str(pk), 
                                origin='data')
        return xpObject
    
    def delete_if_exists(self, is_real=False, **qs_args):
        """Delete row in case item exists.If does not exist, catches a DoesNotExist exception
        @param qs_args: query arguments"""
        try:
            dbObj = self.model.objects
            try:
                if is_real == False:
                    dbObj = self.model.objects.using(self._resolveDbName()).get(**qs_args)
                    dbObj.isDeleted = True
                    dbObj.save(using=self._resolveDbName())
                else:
                    dbObj = self.model.objects_del.using(self._resolveDbName()).get(**qs_args)
                    dbObj.delete()
            except self.model.DoesNotExist:
                pass    
        except Exception as e:
            raise XpMsgException(e, _('Error delete object. Args ') + str(qs_args) + _(' in model ') + str(self.model), 
                                origin='data')
    
    def delete(self, is_real=False, **qs_args):
        """Delete row. In case does not exist, throws model.DoesNotExist
        @param qs_args: query arguments"""
        try:                        
            if is_real == False:
                dbObj = self.model.objects.using(self._resolveDbName()).get(**qs_args)
                dbObj.isDeleted = True
                dbObj.save(using=self._resolveDbName())
            else:
                dbObj = self.model.objects_del.using(self._resolveDbName()).get(**qs_args)
                dbObj.delete()
            #dbObj.using(self._resolveDbName()).get(**qs_args).delete()
        except Exception as e:
            raise XpMsgException(e, _('Error delete object. Args ') + str(qs_args) + _(' in model ') + str(self.model), 
                                origin='data')
    
    def filter_data(self, **args_dict):
        """Search a model table with ordering support and paging
        @param xpNumberMatches: Number of matches
        @param xpPage: Page
        @param xpOrderBy: Tuple of fields to order by
        @return: list : List of model objects"""
        try:
            iNumberMatches = self._numberMatches
            if args_dict.has_key('xpNumberMatches'):
                iNumberMatches = args_dict['xpNumberMatches']
            page = 1
            if args_dict.has_key('xpPage'):
                page = int(args_dict['xpPage'])
            iStart, iEnd = self._getPagingStartEnd(page, iNumberMatches)
            orderByTuple = ()
            if args_dict.has_key('xpOrderBy'):
                orderByTuple = args_dict['xpOrderBy']
            ArgsDict = self._cleanDict(args_dict)
            dbObj = self._processRelated()
            if len(orderByTuple) != 0:
                dbObj = self.model.objects.order_by(*orderByTuple)
            logger.debug( self._resolveDbName() )
            xpList = dbObj.using(self._resolveDbName()).filter(**ArgsDict)[iStart:iEnd]
        except Exception as e:
            raise XpMsgException(e, _('Error in search table model ') + str(self.model), 
                                origin='data')
        return xpList
        
    def get_all(self):
        """Get all rows from table
        @param bFull: boolean : Follows all foreign keys
        @return: list"""
        try:
            dbObj = self._processRelated()
            xpList = dbObj.using(self._resolveDbName()).all()
        except Exception as e:
            raise XpMsgException(e, _('Error in getting all fields from ') + str(self.model), 
                                origin='data')
        return xpList
    
    def search_fields(self, fields, page_start=1, page_end=None, number_results=None, order_by=[], **args):
        """
        Search table with paging, ordering for set of fields. listMap allows mapping from keys to model fields.
        
        ** Attributes **
        
        * ``fields``:tuple<str>
        * ``page_start``:int [optional] [default:1]
        * ``page_end``:int [optional]
        * ``number_results``:int [optional] [default:from settings]
        * ``order_by``:tuple<str> [optional] [default:[]]
        
        ** Returns **
        
        Returns the query set with values(*fields).
        
        xpList:ValuesQueryset
        """
        try:
            logger.debug('CommonDAO.searchFields :: pageStart: %s pageEnd: %s' % (page_start, page_end) )
            logger.debug('CommonDAO.searchFields :: numberResults: %s disablePaging: %s' % (number_results, args['disable_paging']) )
            if (args.has_key('disablePaging') and not args['disablePaging']) or not args.has_key('disablePaging'):
                iStart = (page_start-1)*number_results
                if page_end is None:
                    iEnd = iStart+number_results
                else:
                    iEnd = iStart + number_results*(page_end-page_start+1)
                logger.debug('CommonDAO.searchFields :: iStart: %s iEnd: %s' % (iStart, iEnd) )
            dbObj = self._processRelated()
            """if len(orderBy) != 0:
                dbObj = self.model.objects.order_by(*orderBy)"""
            logger.debug( self._resolveDbName() )
            logger.debug('CommonDAO.searchFields :: args: %s' % (args) )
            if (args.has_key('disablePaging') and not args['disablePaging']) or not args.has_key('disablePaging'):
                logger.debug('CommonDAO.searchField:: iStart: %s iEnd: %s' % (iStart, iEnd) )
                if args.has_key('disable_paging'):
                    del args['disable_paging']
                if len(order_by) == 0:
                    xpList = dbObj.using(self._resolveDbName()).filter(**args)[iStart:iEnd].values_list(*fields)
                else:
                    xpList = dbObj.using(self._resolveDbName()).filter(**args).order_by(*order_by)[iStart:iEnd].values_list(*fields)
            else:
                logger.debug('CommonDAO.searchField:: Have no paging, we get all the data...')
                if args.has_key('disable_paging'):
                    del args['disable_paging']                
                if len(order_by) == 0:
                    xpList = dbObj.using(self._resolveDbName()).filter(**args).values_list(*fields)
                else:
                    xpList = dbObj.using(self._resolveDbName()).filter(**args).order_by(*order_by).values_list(*fields)
            """if len(orderBy) != 0:
                xpList.orderBy(*orderBy)"""
            return xpList
        except Exception as e:
            raise XpMsgException(e, _('Error in searching fields in model ') + str(self.model), origin='data')

    ctx = property(_getCtx, None)

class CoreParameterDAO(CommonDAO):
    model = CoreParam

class ApplicationDAO(CommonDAO):
    model = Application

class ApplicationMediaDAO(CommonDAO):
    model = ApplicationMedia

class ActionDAO(CommonDAO):
    model = Action

class MenuDAO(CommonDAO):
    model = Menu

class ViewMenuDAO(CommonDAO):
    model = ViewMenu

class ServiceMenuDAO(CommonDAO):
    model = ServiceMenu

class MenuParamDAO(CommonDAO):
    model = MenuParam

class ViewDAO(CommonDAO):
    model = View

class WorkflowDAO(CommonDAO):
    model = Workflow

class WorkflowDataDAO(CommonDAO):
    model = WorkflowData

class ParamDAO(CommonDAO):
    model = Param

class WFParamValueDAO(CommonDAO):
    model = WFParamValue

class WorkflowViewDAO(CommonDAO):
    model = WorkflowView

class SearchIndexDAO(CommonDAO):
    model = SearchIndex

class SearchIndexParamDAO(CommonDAO):
    model = SearchIndexParam

class WordDAO(CommonDAO):
    model = Word

class SearchIndexWordDAO(CommonDAO):
    model = SearchIndexWord

class TemplateDAO(CommonDAO):
    model = XpTemplate

class ViewTmplDAO(CommonDAO):
    model = ViewTmpl

class ServiceMenuConditionDAO(CommonDAO):
    model = ServiceMenuCondition

class ViewMenuConditionDAO(CommonDAO):
    model = ViewMenuCondition
