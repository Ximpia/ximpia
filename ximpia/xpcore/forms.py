# coding: utf-8

import json
import logging

from django.core import serializers as _s
from django import forms
from django.forms import ValidationError
from django.utils.translation import ugettext as _
from django.conf import settings

from fields import CharField, CollectionField, MapField
from ximpia.util.js import Form as _jsf

import constants as K

from recaptcha.client import captcha

# Logging
logger = logging.getLogger(__name__)

class XBaseForm(forms.Form):
    
    """
    Core Form

    hidden list fields:
    Used to be serialzed lists in hidden fields. Now

    choices:
    It is kept, but built from choices information in fields. No need to include in form. 
    
    """

    ERROR_INVALID = 'invalid'
    _request = None
    _ctx = None
    _db = {}    
    entryFields = CollectionField()
    params = MapField({'viewMode': [K.UPDATE,K.DELETE]})
    choices = CollectionField()
    pkFields = CollectionField()
    errorMessages = CollectionField()
    okMessages = CollectionField()
    ERR_GEN_VALIDATION = CharField(initial= _('Error validating your data. Check errors marked in red'))
    msg_ok = CharField(initial= _(' '))
    siteMedia = CharField(initial= settings.MEDIA_URL)
    buttonConstants = CollectionField([('close', _('Close'))])
    action = CharField(initial='')
    app = CharField(initial='')
    viewNameSource = CharField(initial='')
    viewNameTarget = CharField(initial=' ')
    result = CharField(initial=' ')
    dbObjects = MapField()
    _errors = {}
    _kwargs = {}
    _args = {}
    _instances = {}
    def __init__(self, *args, **kwargs): 
        """
        Constructor for base form container
        Document instances
        Deletable instances??? : disable_deletes = ('', '')
        
        redis??? mongodb??
        We use django models to get data, but design should be universal, which would need to change the form fields. We need
        data reference (pk) and data key/value and db instance and field name universal for different data stores
        basic data we would need models which allow instance.field_name
        Ximpia models subclass data store type models: 0.3 will support relational and redis, we may add additional data stores later
        Design should be dynamic, so we don't have a static structure and we can map values from model (as data store changes schemas
        and data structures, we adapt without need to change models)
        
        **Arguments**
        
        **Methods** 
        
        **Returns**
        
        """
        self._kwargs = kwargs
        self._args = args
        self._errors = {}
        #logger.debug ( 'XBaseForm :: kwargs: ' + kwargs )
        if kwargs.has_key('ctx'):
            self._ctx = kwargs['ctx']
        #self.errors = {}
        #self.errors['invalid'] = []
        #logger.debug( 'kwargs : ' + kwargs )
        # TODO: Init all database model instances
        if kwargs.has_key('instances'):
            d = kwargs['instances']
            self._instances = d
            fields = self.base_fields.keys()
            for field_str in fields:
                field = self.base_fields[field_str]
                try:
                    instance_field_name = field.instance_field_name
                    # resolve instance in form related to instance in field by type
                    if field.instance:
                        db_resolved = self._resolve_db_instance(field) #@UnusedVariable
                        logger.debug('XBaseForm :: resolved instance: {}'.format(db_resolved))
                        # check if foreign key, should place pk as initial instead of model instance
                        is_fk = self._is_foreign_key(db_resolved, instance_field_name)
                        is_many_to_many = self._is_many_to_many(db_resolved, instance_field_name)
                        logger.debug('XBaseForm :: field: {} isForeignKey: {}'.format(instance_field_name, is_fk))
                        logger.debug('XBaseForm :: field: {} isManyToMany: {}'.format(instance_field_name, is_many_to_many))
                        if is_fk:
                            field.intital = getattr('db_resolved', instance_field_name + '_id')
                            field.instance = db_resolved
                        elif is_many_to_many:
                            #through = self._get_through(db_resolved, instance_field_name)
                            #logger.debug('XBaseForm :: Through: {}'.format(through)) 
                            logger.debug('XBaseForm :: Many data: {}'.format(getattr('db_resolved', instance_field_name + '.through.objects.all()')))
                            if field.values is not None:
                                data = getattr('db_resolved', instance_field_name + '.through.objects.values(* ' + field.values + ')')
                            else:
                                data = getattr('db_resolved', instance_field_name + '.through.objects.values(\'pk\')')
                            logger.debug('XBaseForm :: field name through: {}'.format(self._get_through_end_field(db_resolved, instance_field_name)))
                            field.initial = json.dumps(data)
                            field.instance = db_resolved
                        else:
                            field.initial = getattr('db_resolved', instance_field_name)
                            field.instance = db_resolved
                            logger.debug('XBaseForm :: {} = {}'.format(instance_field_name, field.initial))
                except AttributeError:
                    raise
            # Set instance too
        self._build_objects()
        if kwargs.has_key('ctx'):
            del kwargs['ctx']
        if kwargs.has_key('db_dict'):
            del kwargs['db_dict']
        if kwargs.has_key('instances'):
            del kwargs['instances']
        self._db = {}
        super(XBaseForm, self).__init__(*args, **kwargs)
    def _build_objects(self):
        """
        Build db instance json objects
        db objects should inform:
        - deletable, default True (instances)
        """
        if self._kwargs.has_key('instances'):
            d = {}
            for key in self._kwargs['instances']:
                # Get json object, parse, serialize fields object
                instance = self._kwargs['instances'][key]
                jsonObj = _s.serialize("json", [instance])
                logger.debug( 'XBaseForm._buildObjects :: jsonObj: {}'.format(jsonObj))
                obj = json.loads(jsonObj)[0]
                logger.debug( 'XBaseForm._buildObjects :: obj: {}'.format(obj))
                d[key] = {}
                d[key]['pk'] = obj['pk']
                d[key]['impl'] = str(instance.__class__).split("'")[1]
            self.dbObjects = d
    def _resolveDbInstance(self, field):
        """
        Resolves the instance for field from the instances dictionary sent to constructor instances argument:
        
        form = MyForm(instances={'dbInstance': myModelInstance}
        
        ** Attributes **
        
        * ``field ``:field : Form field
        
        ** Returns **
        
        The reseolved model instance
        """
        dbResolved = None
        for instanceKey in self._instances:
            instance = self._instances[instanceKey]
            if type(instance) == type(field.instance):
                dbResolved = instance
                break
        return dbResolved
    def _getInstanceName(self, instance):
        """
        Get model instance name
        """
        insTypeFields = str(type(instance)).split('.')
        instanceName = insTypeFields[len(insTypeFields)-1].split("'")[0]
        return instanceName
    def _isForeignKey(self, instance, instance_field_name):
        """
        Checks if field is foreign key
        
        ** Attributes **
        
        * ``instance``
        * ``instance_field_name``
        
        ** Returns**
        
        isFK:bool
        """
        isFK = False
        if eval('instance.__class__.__dict__.has_key(\'' + instance_field_name + '\')') and\
                 str(type(eval('instance.__class__.' + instance_field_name))) == "<class 'django.db.models.fields.related.ReverseSingleRelatedObjectDescriptor'>":
            isFK = True
        return isFK
    def _isManyToMany(self, instance, instance_field_name):
        """
        Checks if we have many to many relationship in form field
        """
        isManyToMany = False
        if eval('instance.__class__.__dict__.has_key(\'' + instance_field_name + '\')') and\
                 str(type(eval('instance.__class__.' + instance_field_name))) == "<class 'django.db.models.fields.related.ReverseManyRelatedObjectsDescriptor'>":
            isManyToMany = True
        return isManyToMany
    def _getThrough(self, instance, instance_field_name):
        """
        Checks if instance field has through relationship.
        """
        rel = instance.__class__._meta.get_field_by_name(instance_field_name)[0].rel
        if rel:
            try:
                through = rel.through
            except AttributeError:
                through = None
        else:
            through = None
        return through
    def _hasThrough(self, field):
        """
        Checks weather many to many relationship has a through attribute. If not, add() method exists for field.
        
        ** Attributes **
        
        * ``field``
        
        ** Returns **
        
        bool
        """
        check = True
        try:
            addMethod = field.add
            check = False
        except AttributeError:
            pass
        return check
    def _getThroughEndField(self, instance, instance_field_name):
        """
        Get end relationship through field name
        """
        fieldName = ''
        try:
            through = instance.__class__._meta.get_field_by_name(instance_field_name)[0].rel.through
            mainTo = instance.__class__._meta.get_field_by_name(instance_field_name)[0].rel.to
            for field in through._meta.fields:
                if field.rel:
                    relTo = field.rel.to
                    if relTo and relTo == mainTo:
                        # This is the field
                        fieldName = field.name
        except AttributeError:
            pass
        return fieldName
    def _getThroughFromField(self, instance, instance_field_name):
        """
        Get from relationship through field name. field name for origin relationship.
        """
        fieldName = ''
        try:
            through = instance.__class__._meta.get_field_by_name(instance_field_name)[0].rel.through
            origin = instance.__class__
            for field in through._meta.fields:
                if field.rel:
                    relTo = field.rel.to
                    if relTo and relTo == origin:
                        # This is the field
                        fieldName = field.name
        except AttributeError:
            pass
        return fieldName
    def set_view_mode(self, view_list):
        """Set view mode from ['update,'delete','read']. As CRUD. Save button will be create and update."""
        paramDict = json.loads(self.fields['params'].initial)
        paramDict['viewMode'] = view_list
        self.fields['params'].initial = json.dumps(paramDict)
    def set_view_mode_read(self):
        """Read only mode"""
        paramDict = json.loads(self.fields['params'].initial)
        paramDict['viewMode'] = ['read']
        self.fields['params'].initial = json.dumps(paramDict)
    def put_param(self, name, value):
        """Adds field to javascript array
        @param name: 
        @param value: """
        paramDict = json.loads(self.fields['params'].initial)
        paramDict[name] = value
        self.fields['params'].initial = json.dumps(paramDict)
    def put_param_list(self, **kwargs):
        """Put list of parameters. attribute set, like putParamList(myKey='', myOtherKey='')"""
        paramDict = json.loads(self.fields['params'].initial)
        for key in kwargs:
            paramDict[key] = kwargs[key]
        self.fields['params'].initial = json.dumps(paramDict)
    def get_param(self, name):
        """Get param value.
        @param name: Param name
        @return: value"""
        paramDict = json.loads(self.d('params'))
        if paramDict.has_key(name):
            value = paramDict[name]
        else:
            raise ValueError
        return value
    def get_param_dict(self, param_list):
        """Get dictionary of parameters for the list of parameters given"""
        paramDict = json.loads(self.fields['params'].initial)
        d = {}
        for field in param_list: 
            d[field] = paramDict[field]
        return d
    def get_param_list(self, param_list):
        """Get list of values from list of names given.
        @param paramList: List of fields (names)
        @return: list of values"""
        paramDict = json.loads(self.fields['params'].initial)
        l = []
        for field in param_list:
            l.append(paramDict[field])
        return l
    def has_param(self, name):
        """Checks if has key name
        @param name: 
        @return: boolean"""
        d = json.loads(self.fields['params'].initial)
        return d.has_key(name)
    def _get_field_value(self, field_name):
        """Get field value to be used in forms"""
        #field = eval("self.fields['" + fieldName + "']")
        value = self.data[field_name]
        return value
    def _validate_same_fields(self, tuple_list):
        """Validate same fields for list of tuples in form
        @param tupleList: Like ('password','passwordVerify')"""
        for myTuple in tuple_list:
            field1 = eval("self.fields['" + myTuple[0] + "']")
            field2 = eval("self.fields['" + myTuple[1] + "']")
            field1Value = self.data[myTuple[0]]
            field2Value = self.data[myTuple[1]]
            if field1Value != field2Value:
                if not self.errors.has_key('id_' + myTuple[0]):
                    self.errors['id_' + myTuple[0]] = []
                if not self._errors.has_key('id_' + myTuple[0]):
                    self._errors['id_' + myTuple[0]] = []
                self.errors['id_' + myTuple[0]].append(field1.label + _(' must be the same as ') + field2.label)
                self._errors['id_' + myTuple[0]].append(field1.label + _(' must be the same as ') + field2.label)

    def _validate_captcha(self):
        """Validate captcha"""
        if self._ctx.request.has_key('recaptcha_challenge_field'):
            logger.debug( 'XBaseForm :: _validateCapctha() ...' )
            captchaResponse = captcha.submit(self._ctx.request['recaptcha_challenge_field'],
                            self._ctx.request['recaptcha_response_field'], 
                            settings.RECAPTCHA_PRIVATE_KEY, 
                            self._ctx.meta['REMOTE_ADDR'])            
            if captchaResponse.is_valid == False:
                self.addInvalidError(_('Words introduced in Captcha do not correspond to image. You can reload for another image.'))
    def add_invalid_error(self, error):
        """Adds error to errors lists."""
        if not self.errors.has_key(self.ERROR_INVALID):
            self.errors[self.ERROR_INVALID] = []
        if not self._errors.has_key(self.ERROR_INVALID):
            self._errors[self.ERROR_INVALID] = []
        self.errors[self.ERROR_INVALID].append(error)    
        self._errors[self.ERROR_INVALID].append(error)
    def serialize_JSON(self):
        """Serialize the form into json. The form must be validated first."""
        return json.dumps(self.cleaned_data)
    def set_error_dict(self, errors):
        """Sets error dictionary"""
        self.errors = errors    
    def get_error_dict(self):
        """Get error dictionary"""
        return self.errors
    def has_invalid_errors(self):
        """Has the form invalid errors?"""
        bError = False
        #logger.debug( 'XBaseForm :: hasIvalidErrors :: errors: ' + self.errors.keys() )
        if len(self.errors.keys()) != 0:
            bError = True
        return bError
    def __getitem__(self, name):
        """Get item from object, like a dictionary. Can do form[fieldName]"""
        return self.d(name)
    def d(self, name):
        """Get cleaned data, after form has been validated"""
        value = ''
        try:
            if self.cleaned_data.has_key(name):
                value = self.cleaned_data[name]
        except AttributeError:
            pass
        return value
    def clean(self):
        """Common clean data."""
        self._xp_clean()
        return self.cleaned_data
    def _xp_clean(self):
        """Cleans form. Raises ValidationError in case errors found. Returns cleaned_data"""
        #logger.debug( 'XBaseForm :: hasInvalidErrors(): ' + self.hasInvalidErrors() )
        self._validate_captcha()
        if self.has_invalid_errors():
            raise ValidationError('Form Clean Validation Error')
        """logger.debug( 'self.cleaned_data : ' + self.cleaned_data )
        return self.cleaned_data"""
    def get_form_id(self):
        """Get form id"""
        return self._XP_FORM_ID
    def set_app(self, app):
        """Set application code to form."""
        self.base_fields['app'].initial = app
    def __buildForeignKey(self, js_data):
        """
        Build foreign key choices
        
        ** Attributes **
        
        * ``jsData`` : form data
        
        ** Returns **
        
        None
        """
        # append choices into id_choices        
        choicesStr = js_data['response']['form_' + self._XP_FORM_ID]['choices']['value']
        choices = _jsf.decodeArray(choicesStr)
        # Get fields from this form        
        for fieldName in self.fields:
            field = self.fields[fieldName]
            if str(type(field)).find('fields.OneListField') != -1:
                logger.debug('__buildForeignKey :: field: %s' % (fieldName) ) 
                choices[field.choicesId] = field.buildList()
        # Update new choices
        js_data['response']['form_' + self._XP_FORM_ID]['choices']['value'] = _jsf.encodeDict(choices)
    def __buildManyToMany(self, js_data):
        """
        Build many to many choices
        
        ** Attributes **
        
        * ``jsData`` : form data
        
        ** Returns **
        
        None
        """
        # append choices into id_choices        
        choicesStr = js_data['response']['form_' + self._XP_FORM_ID]['choices']['value']
        choices = _jsf.decodeArray(choicesStr)
        # Get fields from this form        
        for fieldName in self.fields:
            field = self.fields[fieldName]
            if str(type(field)).find('fields.ManyListField') != -1:
                #logger.debug('__buildForeignKey :: field: %s' % (fieldName) ) 
                choices[field.choicesId] = field.buildList()
        # Update new choices
        js_data['response']['form_' + self._XP_FORM_ID]['choices']['value'] = _jsf.encodeDict(choices)

    def save(self):
        """
        Saves the form.
        """        
        logger.debug('XBaseForm.save ...')
        logger.debug('XBaseForm.save :: form cleaned data: %s' % (self.cleaned_data) )
        fieldList = self.fields.keys()
        instances = {}
        manyList = []
        for field in fieldList:
            logger.debug('xBaseForm.save :: field: %s' % (field) )
            if self.fields[field].instance:
                fieldObj = self.fields[field]
                instanceName = self._getInstanceName(fieldObj.instance)
                if not instances.has_key(instanceName):
                    instances[instanceName] = fieldObj.instance
                isMany = self._isManyToMany(instances[instanceName], fieldObj.instance_field_name)
                isFK = self._isForeignKey(instances[instanceName], fieldObj.instance_field_name)
                logger.debug('XBaseForm.save :: isFK: %s' % (isFK) )
                logger.debug('XBaseForm.save :: isMany: %s' % (isMany) )
                logger.debug('XBaseForm.save :: instance db: %s' % (fieldObj.instance._state.db) )
                logger.debug('XBaseForm.save :: pk: %s' % (fieldObj.instance.pk) )
                if isFK:
                    logger.debug('XBaseForm.save :: %s = %s' % (fieldObj.instance_field_name, self.d(fieldObj.instance_field_name)) )
                    instances[instanceName].__setattr__(fieldObj.instance_field_name + '_id', self.d(fieldObj.instance_field_name) )
                else:
                    if not isMany:
                        logger.debug('XBaseForm.save :: %s = %s' % (fieldObj.instance_field_name, self.d(fieldObj.instance_field_name)) )
                        instances[instanceName].__setattr__(fieldObj.instance_field_name, self.d(fieldObj.instance_field_name))
                    else:
                        # Many To Many relationship logic
                        manyList.append(fieldObj)

        # Save model instances
        for instanceName in instances:
            if self._ctx.user:
                if instances[instanceName].pk:
                    instances[instanceName].userModifyId = self._ctx.user.id
                else:
                    instances[instanceName].userCreateId = self._ctx.user.id
            instances[instanceName].save()
        
        # TODO: Place this into method. In future, patterns for different many operations???
        for field in manyList:
            throughEndfield = self._getThroughEndField(field.instance, field.instance_field_name)
            nowValues = eval('field.instance.' + field.instance_field_name + '.through.objects.all()')
            #logger.debug('XBaseForm.save :: form attrs: %s' % (dir(self)) )
            #logger.debug('XBaseForm.save :: data: %s' % (self.data) )
            # self.d['tags'] = []
            # self.data['tags'] = ['1','2']
            logger.debug('XBaseForm.save :: field: %s nowValues: %s' % (field.instance_field_name, nowValues.values()) )
            manyField = eval('field.instance.' + field.instance_field_name)
            
            if self.d(field.instance_field_name) is None:
                visualList = []
            else:        
                if self.d(field.instance_field_name).find('{') == -1 and self.data.has_key(field.instance_field_name):
                    # checkbox
                    # Like [u'1',u'2'] : list of pk values
                    visualList = []
                    fieldValueList = self.data.getlist(field.instance_field_name)
                    # valueListStr :: [{'pk': '1'},{'pk': '2'}]
                    for fieldValue in fieldValueList:
                        visualList.append({'pk': fieldValue})
                else:
                    # Not checkbox
                    fieldValue = self.d(field.instance_field_name)
                    visualListStr = fieldValue.replace("'", '"')
                    visualListStr = fieldValue.replace("'", '"')
                    visualList = json.loads(visualListStr)            
            
            #visualListStr = fieldValue.replace("'", '"')
            #logger.debug('XBaseForm.save :: visualListStr: %s' % (visualListStr) )

            # visualListStr :: []
            #visualList = json.loads(visualListStr)
            logger.debug('xBaseForm.save :: visualList: %s' % (visualList) )
            visualDict = {}
            # origin <- through -> destination
            hasThrough = self._hasThrough(manyField)
            logger.debug('XBaseForm.save :: hasThrough: %s' % (hasThrough) )
            destinationModelClass = field.instance.__class__._meta.get_field_by_name(field.instance_field_name)[0].rel.to
            if hasThrough:
                throughModelClass = field.instance.__class__._meta.get_field_by_name(field.instance_field_name)[0].rel.through
            for visualObj in visualList:
                logger.debug('XBaseForm.save :: visualObj: %s' % (visualObj) )                
                originField = self._getThroughFromField(field.instance, field.instance_field_name)
                destinationField = self._getThroughEndField(field.instance, field.instance_field_name)
                if not visualObj.has_key('pk'):
                    # Not having pk, which means we need to create destination data and through data
                    logger.debug('XBaseForm.save :: Not having pk, which means we need to create destination data and through data')
                    # Create destination data
                    args = {}
                    for key in visualObj.keys():
                        if key.find('__') > 0:
                            args[key.split('__')[1]] = visualObj[key]
                    logger.debug('XBaseForm.save :: Creating destination table: %s' % (args) )
                    destination = destinationModelClass.objects.create( **args )
                    if not hasThrough:
                        # No through table
                        field.instance.add(destination)
                        visualDict[field.instance.through.objects.get( **args ).pk] = visualObj
                    else:
                        # Through table
                        # Insert to destiny table
                        # Insert to intermidiate table
                        args = { originField: field.instance, destinationField: destination }
                        # Add to args for values in visualObj
                        for key in visualObj.keys():
                            if key != 'pk' and key.find('__') == -1:
                                args[key] = visualObj[key]
                        logger.debug('XBaseForm.save :: Creating through table: %s' % (args) )
                        dbData = throughModelClass.objects.create( **args ) #@UnusedVariable
                        myPk = eval('dbData.' + throughEndfield + '_id')
                        visualDict[str(myPk)] = visualObj
                else:
                    # They have pk, either add to through table or insert into container visualDict                    
                    # TODO: We should have a more efficient way than filter every time???
                    logger.debug('XBaseForm.save :: Have pk...')
                    destination = destinationModelClass.objects.get(pk=visualObj['pk'])
                    args = { self._getThroughEndField(field.instance, field.instance_field_name) + '_id': visualObj['pk'] }
                    logger.debug('XBaseForm.save :: filter nowValues: %s' % (nowValues.filter( **args ).values()) )
                    if len(nowValues.filter( **args )) == 0:
                        # pk not added to through table, we add
                        logger.debug('XBaseForm.save :: pk not added to through table, we add')
                        if hasThrough:
                            args = { originField: field.instance, destinationField: destination }
                            # Add to args for values in visualObj
                            for key in visualObj.keys():
                                if key != 'pk' and key.find('__') == -1:
                                    args[key] = visualObj[key]
                            throughModelClass.objects.create( **args )
                            logger.debug('XBaseForm.save :: Created through table: %s' % (args) )
                        else:
                            field.instance.add(destination)
                    visualDict[visualObj['pk']] = visualObj
                                
            # nowValues[0]['meta_id']
            # mark for delete
            logger.debug('XBaseForm.save :: visualDict: %s' % (visualDict) )
            delList = []
            for obj in nowValues:
                # myPk is value pk for destination table, obj is through
                myPk = eval('obj.' + throughEndfield + '_id')
                if not visualDict.has_key(str(myPk)):
                    logger.debug('XBaseForm.save :: Mark for delete: %s' % (myPk) )
                    delList.append(myPk)
                # Do updates
                if visualDict.has_key(myPk):
                    visualObj = visualDict[myPk]
                    if visualObj.has_key('__doUpdate') and visualObj['__doUpdate'] == True:
                        # Will update from visual object attributes to through table
                        logger.debug('XBaseForm.save :: Will update model for pk: %s' % (myPk) )
                        attrs = visualObj.keys()
                        logger.debug('XBaseForm.save :: visualObj:%s' % (visualObj) )
                        for attr in attrs:
                            if attr.find('__') == -1:
                                obj.__setattr__(attr, visualObj[attr])
                        obj.save()
            
            # fieldMany = eval('field.instance.' + field.instance_field_name)
            # delete items in delList
            logger.debug('XBaseForm.save :: delList: %s' % (delList) )
            if len(delList) != 0:
                logger.debug('XBaseForm.save :: Deleting ... %s' % (delList) )
                logger.debug('XBaseForm.save :: Using: %s' % (field.instance._state.db) )
                delQuery = eval('field.instance.' + field.instance_field_name + '.through.objects.filter(' + throughEndfield + '__in=delList)')
                logger.debug('xBaseForm.save :: delQuery: %s' % (delQuery.values()) )
                delQuery.delete()
                logger.debug('XBaseForm.save :: Deleted completed' )
    
    def delete(self, is_real=False):
        """
        Deletes the reference model instance defined in the form.
        
        Get the pk from reference model in the form and calls delete()
        """
        pass
    
    def build_js_data(self, app, js_data):
        """Get javascript json data for this form"""
        js_data['response']['form_' + self._XP_FORM_ID] = {}
        #logger.debug( 'self.initial : ' + self.initial )
        fieldsDict = self.fields
        #logger.debug( 'base_fields: ' + self.base_fields )
        for fieldName in fieldsDict:
            oField = fieldsDict[fieldName]
            attrs = oField.attrs
            fieldTypeFields = str(type(oField)).split('.')
            attrs['fieldType'] = fieldTypeFields[len(fieldTypeFields)-1].split("'")[0]
            try:
                attrs['choices'] = oField.choices
            except AttributeError:
                pass
            attrs['name'] = fieldName
            #logger.debug( 'XBaseForm.buildJsData :: field initial: %s' % (oField.initial) )
            
            if oField.initial != None:
                try:
                    if attrs['fieldType'] == 'DateField' and oField.initial != None:
                        attrs['value'] = oField.initial.strftime('%m/%d/%Y')
                    elif attrs['fieldType'] == 'TimeField' and oField.initial != None:
                        attrs['value'] = oField.initial.strftime('%H:%M')
                    elif attrs['fieldType'] == 'DateTimeField' and oField.initial != None:
                        attrs['value'] = oField.initial.strftime('%m/%d/%Y %H:%M')
                    else:
                        attrs['value'] = oField.initial
                except AttributeError:
                    attrs['value'] = ''
            else:
                attrs['value'] = ''
            
            if attrs['label'] is not None:
                attrs['label'] = attrs['label'].replace('"', '')
            if attrs['helpText'] is not None:
                attrs['helpText'] = attrs['helpText'].replace('"', '')
            #logger.debug( 'XBaseForm.buildJsData :: field: %s' % (fieldName) )
            #logger.debug( attrs )
            js_data['response']['form_' + self._XP_FORM_ID][fieldName] = attrs
        # populate choices with foreign key fields: XpSelectField
        self.__buildForeignKey(js_data)
        self.__buildManyToMany(js_data)
        js_data['response']['form_' + self._XP_FORM_ID]['app']['value'] = app
    
    def disable_fields(self, fields):
        """
        Disable fields, will show them with ``readonly`` html attribute.
        
        ** Attributes **
        
        * ``fields``:List : fields to diable
        
        ** Returns **
        
        None
        """
        for field in fields:
            self.fields[field].widget.attrs['readonly'] = 'readonly'

class DefaultForm(XBaseForm):
    _XP_FORM_ID = 'default'
    errorMessages = CollectionField()
    okMessages = CollectionField()

'''class AppRegex(object):
    """Doc.
    @deprecated: """
    # Any text
    string = re.compile('\w+', re.L)
    # text field, like 
    textField = re.compile("^(\w*)\s?(\s?\w+)*$", re.L)
    # Domain
    domain = re.compile("^([a-z0-9]([-a-z0-9]*[a-z0-9])?\\.)+((a[cdefgilmnoqrstuwxz]|aero|arpa)|(b[abdefghijmnorstvwyz]|biz)|(c[acdfghiklmnorsuvxyz]|cat|com|coop)|d[ejkmoz]|(e[ceghrstu]|edu)|f[ijkmor]|(g[abdefghilmnpqrstuwy]|gov)|h[kmnrtu]|(i[delmnoqrst]|info|int)|(j[emop]|jobs)|k[eghimnprwyz]|l[abcikrstuvy]|(m[acdghklmnopqrstuvwxyz]|mil|mobi|museum)|(n[acefgilopruz]|name|net)|(om|org)|(p[aefghklmnrstwy]|pro)|qa|r[eouw]|s[abcdeghijklmnortvyz]|(t[cdfghjklmnoprtvwz]|travel)|u[agkmsyz]|v[aceginu]|w[fs]|y[etu]|z[amw])$", re.L)
    # currency, like 23.23, 34.5
    currency = re.compile('^[0-9]*\.?|\,?[0-9]{0,2}$')
    # id, like 87262562
    id = re.compile('^[1-9]+[0-9]*$')
    # user id
    userId = re.compile('^[a-zA-Z0-9_.]+')
    # password
    password = re.compile('^\w+')
    # captcha
    captcha = re.compile('^\w{6}$')
    # Email
    email = re.compile('^([\w.])+\@([a-z0-9]([-a-z0-9]*[a-z0-9])?\\.)+((a[cdefgilmnoqrstuwxz]|aero|arpa)|(b[abdefghijmnorstvwyz]|biz)|(c[acdfghiklmnorsuvxyz]|cat|com|coop)|d[ejkmoz]|(e[ceghrstu]|edu)|f[ijkmor]|(g[abdefghilmnpqrstuwy]|gov)|h[kmnrtu]|(i[delmnoqrst]|info|int)|(j[emop]|jobs)|k[eghimnprwyz]|l[abcikrstuvy]|(m[acdghklmnopqrstuvwxyz]|mil|mobi|museum)|(n[acefgilopruz]|name|net)|(om|org)|(p[aefghklmnrstwy]|pro)|qa|r[eouw]|s[abcdeghijklmnortvyz]|(t[cdfghjklmnoprtvwz]|travel)|u[agkmsyz]|v[aceginu]|w[fs]|y[etu]|z[amw])')'''
