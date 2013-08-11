# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Param'
        db.create_table('CORE_PARAM', (
            ('dateCreate', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_column='DATE_CREATE', blank=True)),
            ('dateModify', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, db_column='DATE_MODIFY', blank=True)),
            ('userCreateId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_CREATE_ID', blank=True)),
            ('userModifyId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_MODIFY_ID', blank=True)),
            ('isDeleted', self.gf('django.db.models.fields.BooleanField')(default=False, db_column='IS_DELETED')),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column='ID_CORE_PARAM')),
            ('application', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Application'], db_column='ID_APPLICATION')),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=15, db_column='NAME')),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=30, db_column='TITLE')),
            ('paramType', self.gf('django.db.models.fields.CharField')(max_length=10, db_column='PARAM_TYPE')),
            ('isView', self.gf('django.db.models.fields.BooleanField')(default=False, db_column='IS_VIEW')),
            ('isWorkflow', self.gf('django.db.models.fields.BooleanField')(default=False, db_column='IS_WORKFLOW')),
        ))
        db.send_create_signal(u'core', ['Param'])

        # Adding unique constraint on 'Param', fields ['application', 'name']
        db.create_unique('CORE_PARAM', ['ID_APPLICATION', 'NAME'])

        # Adding model 'Condition'
        db.create_table('CORE_CONDITION', (
            ('dateCreate', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_column='DATE_CREATE', blank=True)),
            ('dateModify', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, db_column='DATE_MODIFY', blank=True)),
            ('userCreateId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_CREATE_ID', blank=True)),
            ('userModifyId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_MODIFY_ID', blank=True)),
            ('isDeleted', self.gf('django.db.models.fields.BooleanField')(default=False, db_column='IS_DELETED')),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column='ID_CORE_CONDITION')),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30, db_column='NAME')),
            ('rule', self.gf('django.db.models.fields.CharField')(max_length=255, db_column='RULE')),
        ))
        db.send_create_signal(u'core', ['Condition'])

        # Adding model 'CoreParam'
        db.create_table('CORE_PARAMETER', (
            ('dateCreate', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_column='DATE_CREATE', blank=True)),
            ('dateModify', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, db_column='DATE_MODIFY', blank=True)),
            ('userCreateId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_CREATE_ID', blank=True)),
            ('userModifyId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_MODIFY_ID', blank=True)),
            ('isDeleted', self.gf('django.db.models.fields.BooleanField')(default=False, db_column='IS_DELETED')),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column='ID_CORE_PARAMETER')),
            ('mode', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, db_column='MODE', blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20, db_column='NAME')),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, db_column='VALUE', blank=True)),
            ('paramType', self.gf('django.db.models.fields.CharField')(default='string', max_length=10, db_column='PARAM_TYPE')),
        ))
        db.send_create_signal(u'core', ['CoreParam'])

        # Adding model 'MetaKey'
        db.create_table('CORE_META_KEY', (
            ('dateCreate', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_column='DATE_CREATE', blank=True)),
            ('dateModify', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, db_column='DATE_MODIFY', blank=True)),
            ('userCreateId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_CREATE_ID', blank=True)),
            ('userModifyId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_MODIFY_ID', blank=True)),
            ('isDeleted', self.gf('django.db.models.fields.BooleanField')(default=False, db_column='IS_DELETED')),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column='ID_CORE_META_KEY')),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, db_column='NAME')),
            ('keyType', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.CoreParam'], db_column='ID_META_TYPE')),
        ))
        db.send_create_signal(u'core', ['MetaKey'])

        # Adding model 'Application'
        db.create_table('CORE_APPLICATION', (
            ('dateCreate', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_column='DATE_CREATE', blank=True)),
            ('dateModify', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, db_column='DATE_MODIFY', blank=True)),
            ('userCreateId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_CREATE_ID', blank=True)),
            ('userModifyId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_MODIFY_ID', blank=True)),
            ('isDeleted', self.gf('django.db.models.fields.BooleanField')(default=False, db_column='IS_DELETED')),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column='ID_CORE_APPLICATION')),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=30, db_column='SLUG')),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=30, db_column='TITLE')),
            ('developer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, db_column='ID_DEVELOPER', blank=True)),
            ('accessGroup', self.gf('django.db.models.fields.related.ForeignKey')(related_name='app_access', db_column='ID_GROUP', to=orm['site.Group'])),
            ('developerOrg', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='app_dev_org', null=True, db_column='ID_DEVELOPER_ORG', to=orm['site.Group'])),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Application'], null=True, db_column='ID_PARENT', blank=True)),
            ('isSubscription', self.gf('django.db.models.fields.BooleanField')(default=False, db_column='IS_SUBSCRIPTION')),
            ('isPrivate', self.gf('django.db.models.fields.BooleanField')(default=False, db_column='IS_PRIVATE')),
            ('isAdmin', self.gf('django.db.models.fields.BooleanField')(default=False, db_column='IS_ADMIN')),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['site.Category'], null=True, db_column='ID_CATEGORY', blank=True)),
        ))
        db.send_create_signal(u'core', ['Application'])

        # Adding model 'ApplicationTag'
        db.create_table('CORE_APPLICATION_TAG', (
            ('dateCreate', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_column='DATE_CREATE', blank=True)),
            ('dateModify', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, db_column='DATE_MODIFY', blank=True)),
            ('userCreateId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_CREATE_ID', blank=True)),
            ('userModifyId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_MODIFY_ID', blank=True)),
            ('isDeleted', self.gf('django.db.models.fields.BooleanField')(default=False, db_column='IS_DELETED')),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column='ID_CORE_APPLICATION_TAG')),
            ('application', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Application'], db_column='ID_VIEW')),
            ('tag', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['site.Tag'], db_column='ID_TAG')),
        ))
        db.send_create_signal(u'core', ['ApplicationTag'])

        # Adding model 'ApplicationMedia'
        db.create_table('CORE_APPLICATION_MEDIA', (
            ('dateCreate', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_column='DATE_CREATE', blank=True)),
            ('dateModify', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, db_column='DATE_MODIFY', blank=True)),
            ('userCreateId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_CREATE_ID', blank=True)),
            ('userModifyId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_MODIFY_ID', blank=True)),
            ('isDeleted', self.gf('django.db.models.fields.BooleanField')(default=False, db_column='IS_DELETED')),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column='ID_CORE_APPLICATION_MEDIA')),
            ('application', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Application'], db_column='ID_APPLICATION')),
            ('image', self.gf('filebrowser.fields.FileBrowseField')(max_length=200, null=True, db_column='IMAGE', blank=True)),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.CoreParam'], db_column='ID_TYPE')),
            ('menuOrder', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1, db_column='MENU_ORDER')),
        ))
        db.send_create_signal(u'core', ['ApplicationMedia'])

        # Adding model 'ApplicationMeta'
        db.create_table('CORE_APPLICATION_META', (
            ('dateCreate', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_column='DATE_CREATE', blank=True)),
            ('dateModify', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, db_column='DATE_MODIFY', blank=True)),
            ('userCreateId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_CREATE_ID', blank=True)),
            ('userModifyId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_MODIFY_ID', blank=True)),
            ('isDeleted', self.gf('django.db.models.fields.BooleanField')(default=False, db_column='IS_DELETED')),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column='ID_CORE_APPLICATION_META')),
            ('application', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Application'], db_column='ID_APPLICATION')),
            ('meta', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.MetaKey'], db_column='ID_META')),
            ('value', self.gf('django.db.models.fields.TextField')(db_column='VALUE')),
        ))
        db.send_create_signal(u'core', ['ApplicationMeta'])

        # Adding model 'SearchIndex'
        db.create_table('CORE_SEARCH_INDEX', (
            ('dateCreate', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_column='DATE_CREATE', blank=True)),
            ('dateModify', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, db_column='DATE_MODIFY', blank=True)),
            ('userCreateId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_CREATE_ID', blank=True)),
            ('userModifyId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_MODIFY_ID', blank=True)),
            ('isDeleted', self.gf('django.db.models.fields.BooleanField')(default=False, db_column='IS_DELETED')),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column='ID_CORE_SEARCH_INDEX')),
            ('application', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Application'], db_column='ID_APPLICATION')),
            ('view', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='index_view', null=True, db_column='ID_VIEW', to=orm['core.View'])),
            ('action', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='index_action', null=True, db_column='ID_ACTION', to=orm['core.Action'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=70, db_column='TITLE')),
        ))
        db.send_create_signal(u'core', ['SearchIndex'])

        # Adding unique constraint on 'SearchIndex', fields ['view', 'action']
        db.create_unique('CORE_SEARCH_INDEX', ['ID_VIEW', 'ID_ACTION'])

        # Adding model 'Word'
        db.create_table('CORE_WORD', (
            ('dateCreate', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_column='DATE_CREATE', blank=True)),
            ('dateModify', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, db_column='DATE_MODIFY', blank=True)),
            ('userCreateId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_CREATE_ID', blank=True)),
            ('userModifyId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_MODIFY_ID', blank=True)),
            ('isDeleted', self.gf('django.db.models.fields.BooleanField')(default=False, db_column='IS_DELETED')),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column='ID_CORE_WORD')),
            ('word', self.gf('django.db.models.fields.CharField')(max_length=20, db_column='WORD', db_index=True)),
        ))
        db.send_create_signal(u'core', ['Word'])

        # Adding model 'SearchIndexWord'
        db.create_table('CORE_SEARCH_INDEX_WORD', (
            ('dateCreate', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_column='DATE_CREATE', blank=True)),
            ('dateModify', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, db_column='DATE_MODIFY', blank=True)),
            ('userCreateId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_CREATE_ID', blank=True)),
            ('userModifyId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_MODIFY_ID', blank=True)),
            ('isDeleted', self.gf('django.db.models.fields.BooleanField')(default=False, db_column='IS_DELETED')),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column='ID_CORE_SEARCH_INDEX_WORD')),
            ('index', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.SearchIndex'], db_column='ID_INDEX')),
            ('word', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Word'], db_column='ID_WORD')),
        ))
        db.send_create_signal(u'core', ['SearchIndexWord'])

        # Adding model 'SearchIndexParam'
        db.create_table('CORE_INDEX_PARAM', (
            ('dateCreate', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_column='DATE_CREATE', blank=True)),
            ('dateModify', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, db_column='DATE_MODIFY', blank=True)),
            ('userCreateId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_CREATE_ID', blank=True)),
            ('userModifyId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_MODIFY_ID', blank=True)),
            ('isDeleted', self.gf('django.db.models.fields.BooleanField')(default=False, db_column='IS_DELETED')),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column='ID_CORE_INDEX_PARAM')),
            ('searchIndex', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.SearchIndex'], db_column='ID_SEARCH_INDEX')),
            ('name', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Param'], db_column='ID_NAME')),
            ('operator', self.gf('django.db.models.fields.CharField')(max_length=10, db_column='OPERATOR')),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=20, db_column='VALUE')),
        ))
        db.send_create_signal(u'core', ['SearchIndexParam'])

        # Adding model 'Service'
        db.create_table('CORE_SERVICE', (
            ('dateCreate', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_column='DATE_CREATE', blank=True)),
            ('dateModify', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, db_column='DATE_MODIFY', blank=True)),
            ('userCreateId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_CREATE_ID', blank=True)),
            ('userModifyId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_MODIFY_ID', blank=True)),
            ('isDeleted', self.gf('django.db.models.fields.BooleanField')(default=False, db_column='IS_DELETED')),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column='ID_CORE_SERVICE')),
            ('application', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Application'], db_column='ID_APPLICATION')),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30, db_column='NAME')),
            ('implementation', self.gf('django.db.models.fields.CharField')(max_length=100, db_column='IMPLEMENTATION')),
        ))
        db.send_create_signal(u'core', ['Service'])

        # Adding unique constraint on 'Service', fields ['application', 'name']
        db.create_unique('CORE_SERVICE', ['ID_APPLICATION', 'NAME'])

        # Adding model 'View'
        db.create_table('CORE_VIEW', (
            ('dateCreate', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_column='DATE_CREATE', blank=True)),
            ('dateModify', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, db_column='DATE_MODIFY', blank=True)),
            ('userCreateId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_CREATE_ID', blank=True)),
            ('userModifyId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_MODIFY_ID', blank=True)),
            ('isDeleted', self.gf('django.db.models.fields.BooleanField')(default=False, db_column='IS_DELETED')),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column='ID_CORE_VIEW')),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='view_parent', null=True, db_column='ID_PARENT', to=orm['core.View'])),
            ('application', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Application'], db_column='ID_APPLICATION')),
            ('service', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Service'], db_column='ID_SERVICE')),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30, db_column='NAME')),
            ('implementation', self.gf('django.db.models.fields.CharField')(max_length=100, db_column='IMPLEMENTATION')),
            ('winType', self.gf('django.db.models.fields.CharField')(default='window', max_length=20, db_column='WIN_TYPE')),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_column='SLUG')),
            ('hasAuth', self.gf('django.db.models.fields.BooleanField')(default=False, db_column='HAS_AUTH')),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['site.Category'], null=True, db_column='ID_CATEGORY', blank=True)),
            ('image', self.gf('filebrowser.fields.FileBrowseField')(max_length=200, null=True, db_column='IMAGE', blank=True)),
        ))
        db.send_create_signal(u'core', ['View'])

        # Adding unique constraint on 'View', fields ['application', 'name']
        db.create_unique('CORE_VIEW', ['ID_APPLICATION', 'NAME'])

        # Adding model 'ViewAccessGroup'
        db.create_table('CORE_VIEW_ACCESS_GROUP', (
            ('dateCreate', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_column='DATE_CREATE', blank=True)),
            ('dateModify', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, db_column='DATE_MODIFY', blank=True)),
            ('userCreateId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_CREATE_ID', blank=True)),
            ('userModifyId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_MODIFY_ID', blank=True)),
            ('isDeleted', self.gf('django.db.models.fields.BooleanField')(default=False, db_column='IS_DELETED')),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column='ID_SITE_GROUP_CHANNEL_ACCESS')),
            ('view', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.View'], db_column='ID_VIEW')),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['site.Group'], db_column='ID_GROUP')),
        ))
        db.send_create_signal(u'core', ['ViewAccessGroup'])

        # Adding model 'ViewTag'
        db.create_table('CORE_VIEW_TAG', (
            ('dateCreate', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_column='DATE_CREATE', blank=True)),
            ('dateModify', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, db_column='DATE_MODIFY', blank=True)),
            ('userCreateId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_CREATE_ID', blank=True)),
            ('userModifyId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_MODIFY_ID', blank=True)),
            ('isDeleted', self.gf('django.db.models.fields.BooleanField')(default=False, db_column='IS_DELETED')),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column='ID_CORE_VIEW_TAG')),
            ('view', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.View'], db_column='ID_VIEW')),
            ('tag', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['site.Tag'], db_column='ID_TAG')),
        ))
        db.send_create_signal(u'core', ['ViewTag'])

        # Adding model 'Action'
        db.create_table('CORE_ACTION', (
            ('dateCreate', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_column='DATE_CREATE', blank=True)),
            ('dateModify', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, db_column='DATE_MODIFY', blank=True)),
            ('userCreateId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_CREATE_ID', blank=True)),
            ('userModifyId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_MODIFY_ID', blank=True)),
            ('isDeleted', self.gf('django.db.models.fields.BooleanField')(default=False, db_column='IS_DELETED')),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column='ID_CORE_ACTION')),
            ('application', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Application'], db_column='ID_APPLICATION')),
            ('service', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Service'], db_column='ID_SERVICE')),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30, db_column='NAME')),
            ('implementation', self.gf('django.db.models.fields.CharField')(max_length=100, db_column='IMPLEMENTATION')),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_column='SLUG')),
            ('hasAuth', self.gf('django.db.models.fields.BooleanField')(default=False, db_column='HAS_AUTH')),
            ('image', self.gf('filebrowser.fields.FileBrowseField')(max_length=200, null=True, db_column='IMAGE', blank=True)),
        ))
        db.send_create_signal(u'core', ['Action'])

        # Adding unique constraint on 'Action', fields ['application', 'name']
        db.create_unique('CORE_ACTION', ['ID_APPLICATION', 'NAME'])

        # Adding model 'ActionAccessGroup'
        db.create_table('CORE_ACTION_ACCESS_GROUP', (
            ('dateCreate', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_column='DATE_CREATE', blank=True)),
            ('dateModify', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, db_column='DATE_MODIFY', blank=True)),
            ('userCreateId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_CREATE_ID', blank=True)),
            ('userModifyId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_MODIFY_ID', blank=True)),
            ('isDeleted', self.gf('django.db.models.fields.BooleanField')(default=False, db_column='IS_DELETED')),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column='ID_SITE_GROUP_CHANNEL_ACCESS')),
            ('action', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Action'], db_column='ID_ACTION')),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['site.Group'], db_column='ID_GROUP')),
        ))
        db.send_create_signal(u'core', ['ActionAccessGroup'])

        # Adding model 'Menu'
        db.create_table('CORE_MENU', (
            ('dateCreate', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_column='DATE_CREATE', blank=True)),
            ('dateModify', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, db_column='DATE_MODIFY', blank=True)),
            ('userCreateId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_CREATE_ID', blank=True)),
            ('userModifyId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_MODIFY_ID', blank=True)),
            ('isDeleted', self.gf('django.db.models.fields.BooleanField')(default=False, db_column='IS_DELETED')),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column='ID_CORE_MENU')),
            ('application', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Application'], db_column='ID_APPLICATION')),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20, db_column='NAME')),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, db_column='TITLE', blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, db_column='DESCRIPTION', blank=True)),
            ('icon', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.CoreParam'], null=True, db_column='ID_ICON', blank=True)),
            ('view', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='menu_view', null=True, db_column='ID_VIEW', to=orm['core.View'])),
            ('action', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='menu_action', null=True, db_column='ID_ACTION', to=orm['core.Action'])),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, db_column='URL', blank=True)),
            ('urlTarget', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, db_column='URL_TARGET', blank=True)),
            ('language', self.gf('django.db.models.fields.CharField')(default='en', max_length=2, db_column='LANGUAGE')),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=2, null=True, db_column='COUNTRY', blank=True)),
            ('device', self.gf('django.db.models.fields.CharField')(default='PC', max_length=10, db_column='DEVICE')),
        ))
        db.send_create_signal(u'core', ['Menu'])

        # Adding model 'ViewMenu'
        db.create_table('CORE_VIEW_MENU', (
            ('dateCreate', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_column='DATE_CREATE', blank=True)),
            ('dateModify', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, db_column='DATE_MODIFY', blank=True)),
            ('userCreateId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_CREATE_ID', blank=True)),
            ('userModifyId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_MODIFY_ID', blank=True)),
            ('isDeleted', self.gf('django.db.models.fields.BooleanField')(default=False, db_column='IS_DELETED')),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column='ID_CORE_VIEW_MENU')),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.ViewMenu'], null=True, db_column='ID_PARENT', blank=True)),
            ('view', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.View'], null=True, db_column='ID_VIEW', blank=True)),
            ('menu', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Menu'], db_column='ID_MENU')),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=10, db_column='ORDER')),
            ('hasSeparator', self.gf('django.db.models.fields.BooleanField')(default=False, db_column='HAS_SEPARATOR')),
            ('zone', self.gf('django.db.models.fields.CharField')(max_length=10, db_column='ZONE')),
        ))
        db.send_create_signal(u'core', ['ViewMenu'])

        # Adding unique constraint on 'ViewMenu', fields ['menu', 'view']
        db.create_unique('CORE_VIEW_MENU', ['ID_MENU', 'ID_VIEW'])

        # Adding model 'ViewMenuCondition'
        db.create_table('CORE_VIEW_MENU_CONDITION', (
            ('dateCreate', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_column='DATE_CREATE', blank=True)),
            ('dateModify', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, db_column='DATE_MODIFY', blank=True)),
            ('userCreateId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_CREATE_ID', blank=True)),
            ('userModifyId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_MODIFY_ID', blank=True)),
            ('isDeleted', self.gf('django.db.models.fields.BooleanField')(default=False, db_column='IS_DELETED')),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column='ID_CORE_VIEW_MENU_CONDITION')),
            ('condition', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Condition'], null=True, db_column='ID_CORE_CONDITION', blank=True)),
            ('viewMenu', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.ViewMenu'], db_column='ID_CORE_VIEW_MENU')),
            ('action', self.gf('django.db.models.fields.CharField')(default='render', max_length=20, db_column='ACTION')),
            ('value', self.gf('django.db.models.fields.BooleanField')(default=True, db_column='VALUE')),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=10, db_column='ORDER')),
        ))
        db.send_create_signal(u'core', ['ViewMenuCondition'])

        # Adding model 'ServiceMenu'
        db.create_table('CORE_SERVICE_MENU', (
            ('dateCreate', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_column='DATE_CREATE', blank=True)),
            ('dateModify', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, db_column='DATE_MODIFY', blank=True)),
            ('userCreateId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_CREATE_ID', blank=True)),
            ('userModifyId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_MODIFY_ID', blank=True)),
            ('isDeleted', self.gf('django.db.models.fields.BooleanField')(default=False, db_column='IS_DELETED')),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column='ID_CORE_SERVICE_MENU')),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.ServiceMenu'], null=True, db_column='ID_PARENT', blank=True)),
            ('service', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Service'], db_column='ID_SERVICE')),
            ('menu', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Menu'], db_column='ID_MENU')),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=10, db_column='ORDER')),
            ('hasSeparator', self.gf('django.db.models.fields.BooleanField')(default=False, db_column='HAS_SEPARATOR')),
            ('zone', self.gf('django.db.models.fields.CharField')(max_length=10, db_column='ZONE')),
        ))
        db.send_create_signal(u'core', ['ServiceMenu'])

        # Adding model 'ServiceMenuCondition'
        db.create_table('CORE_SERVICE_MENU_CONDITION', (
            ('dateCreate', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_column='DATE_CREATE', blank=True)),
            ('dateModify', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, db_column='DATE_MODIFY', blank=True)),
            ('userCreateId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_CREATE_ID', blank=True)),
            ('userModifyId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_MODIFY_ID', blank=True)),
            ('isDeleted', self.gf('django.db.models.fields.BooleanField')(default=False, db_column='IS_DELETED')),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column='ID_CORE_SERVICE_MENU_CONDITION')),
            ('condition', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Condition'], null=True, db_column='ID_CORE_CONDITION', blank=True)),
            ('serviceMenu', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.ServiceMenu'], db_column='ID_CORE_SERVICE_MENU')),
            ('action', self.gf('django.db.models.fields.CharField')(default='render', max_length=20, db_column='ACTION')),
            ('value', self.gf('django.db.models.fields.BooleanField')(default=True, db_column='VALUE')),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=10, db_column='ORDER')),
        ))
        db.send_create_signal(u'core', ['ServiceMenuCondition'])

        # Adding model 'MenuParam'
        db.create_table('CORE_MENU_PARAM', (
            ('dateCreate', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_column='DATE_CREATE', blank=True)),
            ('dateModify', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, db_column='DATE_MODIFY', blank=True)),
            ('userCreateId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_CREATE_ID', blank=True)),
            ('userModifyId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_MODIFY_ID', blank=True)),
            ('isDeleted', self.gf('django.db.models.fields.BooleanField')(default=False, db_column='IS_DELETED')),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column='ID_CORE_MENU_PARAM')),
            ('menu', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Menu'], db_column='ID_MENU')),
            ('name', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Param'], db_column='ID_NAME')),
            ('operator', self.gf('django.db.models.fields.CharField')(max_length=10, db_column='OPERATOR')),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=20, db_column='VALUE')),
        ))
        db.send_create_signal(u'core', ['MenuParam'])

        # Adding model 'ViewMeta'
        db.create_table('CORE_VIEW_META', (
            ('dateCreate', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_column='DATE_CREATE', blank=True)),
            ('dateModify', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, db_column='DATE_MODIFY', blank=True)),
            ('userCreateId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_CREATE_ID', blank=True)),
            ('userModifyId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_MODIFY_ID', blank=True)),
            ('isDeleted', self.gf('django.db.models.fields.BooleanField')(default=False, db_column='IS_DELETED')),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column='ID_CORE_VIEW_META')),
            ('view', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.View'], db_column='ID_VIEW')),
            ('meta', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.MetaKey'], db_column='ID_META')),
            ('value', self.gf('django.db.models.fields.TextField')(db_column='VALUE')),
        ))
        db.send_create_signal(u'core', ['ViewMeta'])

        # Adding model 'ViewTmpl'
        db.create_table('CORE_VIEW_TMPL', (
            ('dateCreate', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_column='DATE_CREATE', blank=True)),
            ('dateModify', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, db_column='DATE_MODIFY', blank=True)),
            ('userCreateId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_CREATE_ID', blank=True)),
            ('userModifyId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_MODIFY_ID', blank=True)),
            ('isDeleted', self.gf('django.db.models.fields.BooleanField')(default=False, db_column='IS_DELETED')),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column='ID_CORE_VIEW_TMPL')),
            ('view', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.View'], db_column='ID_VIEW')),
            ('template', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.XpTemplate'], db_column='ID_TEMPLATE')),
        ))
        db.send_create_signal(u'core', ['ViewTmpl'])

        # Adding model 'XpTemplate'
        db.create_table('CORE_TEMPLATE', (
            ('dateCreate', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_column='DATE_CREATE', blank=True)),
            ('dateModify', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, db_column='DATE_MODIFY', blank=True)),
            ('userCreateId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_CREATE_ID', blank=True)),
            ('userModifyId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_MODIFY_ID', blank=True)),
            ('isDeleted', self.gf('django.db.models.fields.BooleanField')(default=False, db_column='IS_DELETED')),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column='ID_CORE_TEMPLATE')),
            ('application', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Application'], db_column='ID_APPLICATION')),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50, db_column='NAME')),
            ('alias', self.gf('django.db.models.fields.CharField')(max_length=20, db_column='ALIAS')),
            ('language', self.gf('django.db.models.fields.CharField')(default='en', max_length=2, db_column='LANGUAGE')),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=2, null=True, db_column='COUNTRY', blank=True)),
            ('winType', self.gf('django.db.models.fields.CharField')(default='window', max_length=20, db_column='WIN_TYPE')),
            ('device', self.gf('django.db.models.fields.CharField')(default='PC', max_length=10, db_column='DEVICE')),
        ))
        db.send_create_signal(u'core', ['XpTemplate'])

        # Adding unique constraint on 'XpTemplate', fields ['application', 'name']
        db.create_unique('CORE_TEMPLATE', ['ID_APPLICATION', 'NAME'])

        # Adding model 'Workflow'
        db.create_table('CORE_WORKFLOW', (
            ('dateCreate', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_column='DATE_CREATE', blank=True)),
            ('dateModify', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, db_column='DATE_MODIFY', blank=True)),
            ('userCreateId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_CREATE_ID', blank=True)),
            ('userModifyId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_MODIFY_ID', blank=True)),
            ('isDeleted', self.gf('django.db.models.fields.BooleanField')(default=False, db_column='IS_DELETED')),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column='ID_CORE_WORKFLOW')),
            ('application', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Application'], db_column='ID_APPLICATION')),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=15, db_column='CODE', db_index=True)),
            ('resetStart', self.gf('django.db.models.fields.BooleanField')(default=False, db_column='RESET_START')),
            ('deleteOnEnd', self.gf('django.db.models.fields.BooleanField')(default=False, db_column='DELETE_ON_END')),
            ('jumpToView', self.gf('django.db.models.fields.BooleanField')(default=True, db_column='JUMP_TO_VIEW')),
        ))
        db.send_create_signal(u'core', ['Workflow'])

        # Adding model 'WorkflowView'
        db.create_table('CORE_WORKFLOW_VIEW', (
            ('dateCreate', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_column='DATE_CREATE', blank=True)),
            ('dateModify', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, db_column='DATE_MODIFY', blank=True)),
            ('userCreateId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_CREATE_ID', blank=True)),
            ('userModifyId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_MODIFY_ID', blank=True)),
            ('isDeleted', self.gf('django.db.models.fields.BooleanField')(default=False, db_column='IS_DELETED')),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column='ID_CORE_WORKFLOW_VIEW')),
            ('flow', self.gf('django.db.models.fields.related.ForeignKey')(related_name='flowView', db_column='ID_FLOW', to=orm['core.Workflow'])),
            ('viewSource', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='flowViewSource', null=True, db_column='ID_VIEW_SOURCE', to=orm['core.View'])),
            ('viewTarget', self.gf('django.db.models.fields.related.ForeignKey')(related_name='flowViewTarget', db_column='ID_VIEW_TARGET', to=orm['core.View'])),
            ('action', self.gf('django.db.models.fields.related.ForeignKey')(related_name='wf_action', db_column='ID_ACTION', to=orm['core.Action'])),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=10, db_column='ORDER')),
        ))
        db.send_create_signal(u'core', ['WorkflowView'])

        # Adding model 'ViewParamValue'
        db.create_table('CORE_VIEW_PARAM_VALUE', (
            ('dateCreate', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_column='DATE_CREATE', blank=True)),
            ('dateModify', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, db_column='DATE_MODIFY', blank=True)),
            ('userCreateId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_CREATE_ID', blank=True)),
            ('userModifyId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_MODIFY_ID', blank=True)),
            ('isDeleted', self.gf('django.db.models.fields.BooleanField')(default=False, db_column='IS_DELETED')),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column='ID_CORE_VIEW_PARAM_VALUE')),
            ('view', self.gf('django.db.models.fields.related.ForeignKey')(related_name='viewParam', db_column='ID_VIEW', to=orm['core.View'])),
            ('name', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Param'], db_column='ID_NAME')),
            ('operator', self.gf('django.db.models.fields.CharField')(max_length=10, db_column='OPERATOR')),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=20, db_column='VALUE')),
        ))
        db.send_create_signal(u'core', ['ViewParamValue'])

        # Adding model 'WorkflowData'
        db.create_table('CORE_WORKFLOW_DATA', (
            ('dateCreate', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_column='DATE_CREATE', blank=True)),
            ('dateModify', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, db_column='DATE_MODIFY', blank=True)),
            ('userCreateId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_CREATE_ID', blank=True)),
            ('userModifyId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_MODIFY_ID', blank=True)),
            ('isDeleted', self.gf('django.db.models.fields.BooleanField')(default=False, db_column='IS_DELETED')),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column='ID_CORE_WORKFLOW_DATA')),
            ('userId', self.gf('django.db.models.fields.CharField')(max_length=40, db_column='USER_ID')),
            ('flow', self.gf('django.db.models.fields.related.ForeignKey')(related_name='flowData', db_column='ID_FLOW', to=orm['core.Workflow'])),
            ('view', self.gf('django.db.models.fields.related.ForeignKey')(related_name='viewFlowData', db_column='ID_VIEW', to=orm['core.View'])),
            ('data', self.gf('django.db.models.fields.TextField')(default='eyJkYXRhIjoge30sICJ2aWV3TmFtZSI6ICIifQ==\n', db_column='DATA')),
        ))
        db.send_create_signal(u'core', ['WorkflowData'])

        # Adding unique constraint on 'WorkflowData', fields ['userId', 'flow']
        db.create_unique('CORE_WORKFLOW_DATA', ['USER_ID', 'ID_FLOW'])

        # Adding model 'WFParamValue'
        db.create_table('CORE_WORKFLOW_PARAM_VALUE', (
            ('dateCreate', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_column='DATE_CREATE', blank=True)),
            ('dateModify', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, db_column='DATE_MODIFY', blank=True)),
            ('userCreateId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_CREATE_ID', blank=True)),
            ('userModifyId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_MODIFY_ID', blank=True)),
            ('isDeleted', self.gf('django.db.models.fields.BooleanField')(default=False, db_column='IS_DELETED')),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column='ID_CORE_WORKFLOW_PARAM_VALUE')),
            ('flowView', self.gf('django.db.models.fields.related.ForeignKey')(related_name='flowViewParamValue', db_column='ID_FLOW_VIEW', to=orm['core.WorkflowView'])),
            ('name', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Param'], db_column='ID_NAME')),
            ('operator', self.gf('django.db.models.fields.CharField')(max_length=10, db_column='OPERATOR')),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=20, db_column='VALUE')),
        ))
        db.send_create_signal(u'core', ['WFParamValue'])

        # Adding model 'Setting'
        db.create_table('CORE_SETTING', (
            ('dateCreate', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_column='DATE_CREATE', blank=True)),
            ('dateModify', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, db_column='DATE_MODIFY', blank=True)),
            ('userCreateId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_CREATE_ID', blank=True)),
            ('userModifyId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_MODIFY_ID', blank=True)),
            ('isDeleted', self.gf('django.db.models.fields.BooleanField')(default=False, db_column='IS_DELETED')),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column='ID_CORE_SETTING')),
            ('application', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='core_setting_app', null=True, db_column='ID_CORE_APPLICATION', to=orm['core.Application'])),
            ('name', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.MetaKey'], db_column='ID_META')),
            ('value', self.gf('django.db.models.fields.TextField')(db_column='VALUE')),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255, db_column='DESCRIPTION')),
            ('mustAutoload', self.gf('django.db.models.fields.BooleanField')(default=False, db_column='MUST_AUTOLOAD')),
        ))
        db.send_create_signal(u'core', ['Setting'])


    def backwards(self, orm):
        # Removing unique constraint on 'WorkflowData', fields ['userId', 'flow']
        db.delete_unique('CORE_WORKFLOW_DATA', ['USER_ID', 'ID_FLOW'])

        # Removing unique constraint on 'XpTemplate', fields ['application', 'name']
        db.delete_unique('CORE_TEMPLATE', ['ID_APPLICATION', 'NAME'])

        # Removing unique constraint on 'ViewMenu', fields ['menu', 'view']
        db.delete_unique('CORE_VIEW_MENU', ['ID_MENU', 'ID_VIEW'])

        # Removing unique constraint on 'Action', fields ['application', 'name']
        db.delete_unique('CORE_ACTION', ['ID_APPLICATION', 'NAME'])

        # Removing unique constraint on 'View', fields ['application', 'name']
        db.delete_unique('CORE_VIEW', ['ID_APPLICATION', 'NAME'])

        # Removing unique constraint on 'Service', fields ['application', 'name']
        db.delete_unique('CORE_SERVICE', ['ID_APPLICATION', 'NAME'])

        # Removing unique constraint on 'SearchIndex', fields ['view', 'action']
        db.delete_unique('CORE_SEARCH_INDEX', ['ID_VIEW', 'ID_ACTION'])

        # Removing unique constraint on 'Param', fields ['application', 'name']
        db.delete_unique('CORE_PARAM', ['ID_APPLICATION', 'NAME'])

        # Deleting model 'Param'
        db.delete_table('CORE_PARAM')

        # Deleting model 'Condition'
        db.delete_table('CORE_CONDITION')

        # Deleting model 'CoreParam'
        db.delete_table('CORE_PARAMETER')

        # Deleting model 'MetaKey'
        db.delete_table('CORE_META_KEY')

        # Deleting model 'Application'
        db.delete_table('CORE_APPLICATION')

        # Deleting model 'ApplicationTag'
        db.delete_table('CORE_APPLICATION_TAG')

        # Deleting model 'ApplicationMedia'
        db.delete_table('CORE_APPLICATION_MEDIA')

        # Deleting model 'ApplicationMeta'
        db.delete_table('CORE_APPLICATION_META')

        # Deleting model 'SearchIndex'
        db.delete_table('CORE_SEARCH_INDEX')

        # Deleting model 'Word'
        db.delete_table('CORE_WORD')

        # Deleting model 'SearchIndexWord'
        db.delete_table('CORE_SEARCH_INDEX_WORD')

        # Deleting model 'SearchIndexParam'
        db.delete_table('CORE_INDEX_PARAM')

        # Deleting model 'Service'
        db.delete_table('CORE_SERVICE')

        # Deleting model 'View'
        db.delete_table('CORE_VIEW')

        # Deleting model 'ViewAccessGroup'
        db.delete_table('CORE_VIEW_ACCESS_GROUP')

        # Deleting model 'ViewTag'
        db.delete_table('CORE_VIEW_TAG')

        # Deleting model 'Action'
        db.delete_table('CORE_ACTION')

        # Deleting model 'ActionAccessGroup'
        db.delete_table('CORE_ACTION_ACCESS_GROUP')

        # Deleting model 'Menu'
        db.delete_table('CORE_MENU')

        # Deleting model 'ViewMenu'
        db.delete_table('CORE_VIEW_MENU')

        # Deleting model 'ViewMenuCondition'
        db.delete_table('CORE_VIEW_MENU_CONDITION')

        # Deleting model 'ServiceMenu'
        db.delete_table('CORE_SERVICE_MENU')

        # Deleting model 'ServiceMenuCondition'
        db.delete_table('CORE_SERVICE_MENU_CONDITION')

        # Deleting model 'MenuParam'
        db.delete_table('CORE_MENU_PARAM')

        # Deleting model 'ViewMeta'
        db.delete_table('CORE_VIEW_META')

        # Deleting model 'ViewTmpl'
        db.delete_table('CORE_VIEW_TMPL')

        # Deleting model 'XpTemplate'
        db.delete_table('CORE_TEMPLATE')

        # Deleting model 'Workflow'
        db.delete_table('CORE_WORKFLOW')

        # Deleting model 'WorkflowView'
        db.delete_table('CORE_WORKFLOW_VIEW')

        # Deleting model 'ViewParamValue'
        db.delete_table('CORE_VIEW_PARAM_VALUE')

        # Deleting model 'WorkflowData'
        db.delete_table('CORE_WORKFLOW_DATA')

        # Deleting model 'WFParamValue'
        db.delete_table('CORE_WORKFLOW_PARAM_VALUE')

        # Deleting model 'Setting'
        db.delete_table('CORE_SETTING')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'core.action': {
            'Meta': {'unique_together': "(('application', 'name'),)", 'object_name': 'Action', 'db_table': "'CORE_ACTION'"},
            'accessGroups': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'action_access'", 'symmetrical': 'False', 'through': u"orm['core.ActionAccessGroup']", 'to': u"orm['site.Group']"}),
            'application': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Application']", 'db_column': "'ID_APPLICATION'"}),
            'dateCreate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'DATE_CREATE'", 'blank': 'True'}),
            'dateModify': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'DATE_MODIFY'", 'blank': 'True'}),
            'hasAuth': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'HAS_AUTH'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'ID_CORE_ACTION'"}),
            'image': ('filebrowser.fields.FileBrowseField', [], {'max_length': '200', 'null': 'True', 'db_column': "'IMAGE'", 'blank': 'True'}),
            'implementation': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'IMPLEMENTATION'"}),
            'isDeleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'IS_DELETED'"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'db_column': "'NAME'"}),
            'service': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Service']", 'db_column': "'ID_SERVICE'"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_column': "'SLUG'"}),
            'userCreateId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_CREATE_ID'", 'blank': 'True'}),
            'userModifyId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_MODIFY_ID'", 'blank': 'True'})
        },
        u'core.actionaccessgroup': {
            'Meta': {'object_name': 'ActionAccessGroup', 'db_table': "'CORE_ACTION_ACCESS_GROUP'"},
            'action': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Action']", 'db_column': "'ID_ACTION'"}),
            'dateCreate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'DATE_CREATE'", 'blank': 'True'}),
            'dateModify': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'DATE_MODIFY'", 'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['site.Group']", 'db_column': "'ID_GROUP'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'ID_SITE_GROUP_CHANNEL_ACCESS'"}),
            'isDeleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'IS_DELETED'"}),
            'userCreateId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_CREATE_ID'", 'blank': 'True'}),
            'userModifyId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_MODIFY_ID'", 'blank': 'True'})
        },
        u'core.application': {
            'Meta': {'object_name': 'Application', 'db_table': "'CORE_APPLICATION'"},
            'accessGroup': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'app_access'", 'db_column': "'ID_GROUP'", 'to': u"orm['site.Group']"}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['site.Category']", 'null': 'True', 'db_column': "'ID_CATEGORY'", 'blank': 'True'}),
            'dateCreate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'DATE_CREATE'", 'blank': 'True'}),
            'dateModify': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'DATE_MODIFY'", 'blank': 'True'}),
            'developer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'db_column': "'ID_DEVELOPER'", 'blank': 'True'}),
            'developerOrg': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'app_dev_org'", 'null': 'True', 'db_column': "'ID_DEVELOPER_ORG'", 'to': u"orm['site.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'ID_CORE_APPLICATION'"}),
            'isAdmin': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'IS_ADMIN'"}),
            'isDeleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'IS_DELETED'"}),
            'isPrivate': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'IS_PRIVATE'"}),
            'isSubscription': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'IS_SUBSCRIPTION'"}),
            'meta': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'app_meta'", 'symmetrical': 'False', 'through': u"orm['core.ApplicationMeta']", 'to': u"orm['core.MetaKey']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Application']", 'null': 'True', 'db_column': "'ID_PARENT'", 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '30', 'db_column': "'SLUG'"}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'application_tags'", 'to': u"orm['site.Tag']", 'through': u"orm['core.ApplicationTag']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '30', 'db_column': "'TITLE'"}),
            'userCreateId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_CREATE_ID'", 'blank': 'True'}),
            'userModifyId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_MODIFY_ID'", 'blank': 'True'})
        },
        u'core.applicationmedia': {
            'Meta': {'object_name': 'ApplicationMedia', 'db_table': "'CORE_APPLICATION_MEDIA'"},
            'application': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Application']", 'db_column': "'ID_APPLICATION'"}),
            'dateCreate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'DATE_CREATE'", 'blank': 'True'}),
            'dateModify': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'DATE_MODIFY'", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'ID_CORE_APPLICATION_MEDIA'"}),
            'image': ('filebrowser.fields.FileBrowseField', [], {'max_length': '200', 'null': 'True', 'db_column': "'IMAGE'", 'blank': 'True'}),
            'isDeleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'IS_DELETED'"}),
            'menuOrder': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1', 'db_column': "'MENU_ORDER'"}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.CoreParam']", 'db_column': "'ID_TYPE'"}),
            'userCreateId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_CREATE_ID'", 'blank': 'True'}),
            'userModifyId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_MODIFY_ID'", 'blank': 'True'})
        },
        u'core.applicationmeta': {
            'Meta': {'object_name': 'ApplicationMeta', 'db_table': "'CORE_APPLICATION_META'"},
            'application': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Application']", 'db_column': "'ID_APPLICATION'"}),
            'dateCreate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'DATE_CREATE'", 'blank': 'True'}),
            'dateModify': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'DATE_MODIFY'", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'ID_CORE_APPLICATION_META'"}),
            'isDeleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'IS_DELETED'"}),
            'meta': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.MetaKey']", 'db_column': "'ID_META'"}),
            'userCreateId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_CREATE_ID'", 'blank': 'True'}),
            'userModifyId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_MODIFY_ID'", 'blank': 'True'}),
            'value': ('django.db.models.fields.TextField', [], {'db_column': "'VALUE'"})
        },
        u'core.applicationtag': {
            'Meta': {'object_name': 'ApplicationTag', 'db_table': "'CORE_APPLICATION_TAG'"},
            'application': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Application']", 'db_column': "'ID_VIEW'"}),
            'dateCreate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'DATE_CREATE'", 'blank': 'True'}),
            'dateModify': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'DATE_MODIFY'", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'ID_CORE_APPLICATION_TAG'"}),
            'isDeleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'IS_DELETED'"}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['site.Tag']", 'db_column': "'ID_TAG'"}),
            'userCreateId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_CREATE_ID'", 'blank': 'True'}),
            'userModifyId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_MODIFY_ID'", 'blank': 'True'})
        },
        u'core.condition': {
            'Meta': {'object_name': 'Condition', 'db_table': "'CORE_CONDITION'"},
            'dateCreate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'DATE_CREATE'", 'blank': 'True'}),
            'dateModify': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'DATE_MODIFY'", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'ID_CORE_CONDITION'"}),
            'isDeleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'IS_DELETED'"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'db_column': "'NAME'"}),
            'rule': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_column': "'RULE'"}),
            'userCreateId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_CREATE_ID'", 'blank': 'True'}),
            'userModifyId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_MODIFY_ID'", 'blank': 'True'})
        },
        u'core.coreparam': {
            'Meta': {'object_name': 'CoreParam', 'db_table': "'CORE_PARAMETER'"},
            'dateCreate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'DATE_CREATE'", 'blank': 'True'}),
            'dateModify': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'DATE_MODIFY'", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'ID_CORE_PARAMETER'"}),
            'isDeleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'IS_DELETED'"}),
            'mode': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'db_column': "'MODE'", 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20', 'db_column': "'NAME'"}),
            'paramType': ('django.db.models.fields.CharField', [], {'default': "'string'", 'max_length': '10', 'db_column': "'PARAM_TYPE'"}),
            'userCreateId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_CREATE_ID'", 'blank': 'True'}),
            'userModifyId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_MODIFY_ID'", 'blank': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'db_column': "'VALUE'", 'blank': 'True'})
        },
        u'core.menu': {
            'Meta': {'object_name': 'Menu', 'db_table': "'CORE_MENU'"},
            'action': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'menu_action'", 'null': 'True', 'db_column': "'ID_ACTION'", 'to': u"orm['core.Action']"}),
            'application': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Application']", 'db_column': "'ID_APPLICATION'"}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'db_column': "'COUNTRY'", 'blank': 'True'}),
            'dateCreate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'DATE_CREATE'", 'blank': 'True'}),
            'dateModify': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'DATE_MODIFY'", 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'db_column': "'DESCRIPTION'", 'blank': 'True'}),
            'device': ('django.db.models.fields.CharField', [], {'default': "'PC'", 'max_length': '10', 'db_column': "'DEVICE'"}),
            'icon': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.CoreParam']", 'null': 'True', 'db_column': "'ID_ICON'", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'ID_CORE_MENU'"}),
            'isDeleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'IS_DELETED'"}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'en'", 'max_length': '2', 'db_column': "'LANGUAGE'"}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20', 'db_column': "'NAME'"}),
            'params': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'menu_params'", 'to': u"orm['core.Param']", 'through': u"orm['core.MenuParam']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'db_column': "'TITLE'", 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'db_column': "'URL'", 'blank': 'True'}),
            'urlTarget': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'db_column': "'URL_TARGET'", 'blank': 'True'}),
            'userCreateId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_CREATE_ID'", 'blank': 'True'}),
            'userModifyId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_MODIFY_ID'", 'blank': 'True'}),
            'view': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'menu_view'", 'null': 'True', 'db_column': "'ID_VIEW'", 'to': u"orm['core.View']"})
        },
        u'core.menuparam': {
            'Meta': {'object_name': 'MenuParam', 'db_table': "'CORE_MENU_PARAM'"},
            'dateCreate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'DATE_CREATE'", 'blank': 'True'}),
            'dateModify': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'DATE_MODIFY'", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'ID_CORE_MENU_PARAM'"}),
            'isDeleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'IS_DELETED'"}),
            'menu': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Menu']", 'db_column': "'ID_MENU'"}),
            'name': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Param']", 'db_column': "'ID_NAME'"}),
            'operator': ('django.db.models.fields.CharField', [], {'max_length': '10', 'db_column': "'OPERATOR'"}),
            'userCreateId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_CREATE_ID'", 'blank': 'True'}),
            'userModifyId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_MODIFY_ID'", 'blank': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '20', 'db_column': "'VALUE'"})
        },
        u'core.metakey': {
            'Meta': {'ordering': "['name']", 'object_name': 'MetaKey', 'db_table': "'CORE_META_KEY'"},
            'dateCreate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'DATE_CREATE'", 'blank': 'True'}),
            'dateModify': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'DATE_MODIFY'", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'ID_CORE_META_KEY'"}),
            'isDeleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'IS_DELETED'"}),
            'keyType': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.CoreParam']", 'db_column': "'ID_META_TYPE'"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'NAME'"}),
            'userCreateId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_CREATE_ID'", 'blank': 'True'}),
            'userModifyId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_MODIFY_ID'", 'blank': 'True'})
        },
        u'core.param': {
            'Meta': {'unique_together': "(('application', 'name'),)", 'object_name': 'Param', 'db_table': "'CORE_PARAM'"},
            'application': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Application']", 'db_column': "'ID_APPLICATION'"}),
            'dateCreate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'DATE_CREATE'", 'blank': 'True'}),
            'dateModify': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'DATE_MODIFY'", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'ID_CORE_PARAM'"}),
            'isDeleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'IS_DELETED'"}),
            'isView': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'IS_VIEW'"}),
            'isWorkflow': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'IS_WORKFLOW'"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_column': "'NAME'"}),
            'paramType': ('django.db.models.fields.CharField', [], {'max_length': '10', 'db_column': "'PARAM_TYPE'"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '30', 'db_column': "'TITLE'"}),
            'userCreateId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_CREATE_ID'", 'blank': 'True'}),
            'userModifyId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_MODIFY_ID'", 'blank': 'True'})
        },
        u'core.searchindex': {
            'Meta': {'unique_together': "(('view', 'action'),)", 'object_name': 'SearchIndex', 'db_table': "'CORE_SEARCH_INDEX'"},
            'action': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'index_action'", 'null': 'True', 'db_column': "'ID_ACTION'", 'to': u"orm['core.Action']"}),
            'application': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Application']", 'db_column': "'ID_APPLICATION'"}),
            'dateCreate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'DATE_CREATE'", 'blank': 'True'}),
            'dateModify': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'DATE_MODIFY'", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'ID_CORE_SEARCH_INDEX'"}),
            'isDeleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'IS_DELETED'"}),
            'params': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'index_params'", 'to': u"orm['core.Param']", 'through': u"orm['core.SearchIndexParam']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '70', 'db_column': "'TITLE'"}),
            'userCreateId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_CREATE_ID'", 'blank': 'True'}),
            'userModifyId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_MODIFY_ID'", 'blank': 'True'}),
            'view': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'index_view'", 'null': 'True', 'db_column': "'ID_VIEW'", 'to': u"orm['core.View']"}),
            'words': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'index_words'", 'symmetrical': 'False', 'through': u"orm['core.SearchIndexWord']", 'to': u"orm['core.Word']"})
        },
        u'core.searchindexparam': {
            'Meta': {'object_name': 'SearchIndexParam', 'db_table': "'CORE_INDEX_PARAM'"},
            'dateCreate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'DATE_CREATE'", 'blank': 'True'}),
            'dateModify': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'DATE_MODIFY'", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'ID_CORE_INDEX_PARAM'"}),
            'isDeleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'IS_DELETED'"}),
            'name': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Param']", 'db_column': "'ID_NAME'"}),
            'operator': ('django.db.models.fields.CharField', [], {'max_length': '10', 'db_column': "'OPERATOR'"}),
            'searchIndex': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.SearchIndex']", 'db_column': "'ID_SEARCH_INDEX'"}),
            'userCreateId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_CREATE_ID'", 'blank': 'True'}),
            'userModifyId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_MODIFY_ID'", 'blank': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '20', 'db_column': "'VALUE'"})
        },
        u'core.searchindexword': {
            'Meta': {'object_name': 'SearchIndexWord', 'db_table': "'CORE_SEARCH_INDEX_WORD'"},
            'dateCreate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'DATE_CREATE'", 'blank': 'True'}),
            'dateModify': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'DATE_MODIFY'", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'ID_CORE_SEARCH_INDEX_WORD'"}),
            'index': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.SearchIndex']", 'db_column': "'ID_INDEX'"}),
            'isDeleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'IS_DELETED'"}),
            'userCreateId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_CREATE_ID'", 'blank': 'True'}),
            'userModifyId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_MODIFY_ID'", 'blank': 'True'}),
            'word': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Word']", 'db_column': "'ID_WORD'"})
        },
        u'core.service': {
            'Meta': {'unique_together': "(('application', 'name'),)", 'object_name': 'Service', 'db_table': "'CORE_SERVICE'"},
            'application': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Application']", 'db_column': "'ID_APPLICATION'"}),
            'dateCreate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'DATE_CREATE'", 'blank': 'True'}),
            'dateModify': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'DATE_MODIFY'", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'ID_CORE_SERVICE'"}),
            'implementation': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'IMPLEMENTATION'"}),
            'isDeleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'IS_DELETED'"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'db_column': "'NAME'"}),
            'userCreateId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_CREATE_ID'", 'blank': 'True'}),
            'userModifyId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_MODIFY_ID'", 'blank': 'True'})
        },
        u'core.servicemenu': {
            'Meta': {'object_name': 'ServiceMenu', 'db_table': "'CORE_SERVICE_MENU'"},
            'conditions': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'servicemenu_conditions'", 'to': u"orm['core.Condition']", 'through': u"orm['core.ServiceMenuCondition']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'dateCreate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'DATE_CREATE'", 'blank': 'True'}),
            'dateModify': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'DATE_MODIFY'", 'blank': 'True'}),
            'hasSeparator': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'HAS_SEPARATOR'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'ID_CORE_SERVICE_MENU'"}),
            'isDeleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'IS_DELETED'"}),
            'menu': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Menu']", 'db_column': "'ID_MENU'"}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '10', 'db_column': "'ORDER'"}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.ServiceMenu']", 'null': 'True', 'db_column': "'ID_PARENT'", 'blank': 'True'}),
            'service': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Service']", 'db_column': "'ID_SERVICE'"}),
            'userCreateId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_CREATE_ID'", 'blank': 'True'}),
            'userModifyId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_MODIFY_ID'", 'blank': 'True'}),
            'zone': ('django.db.models.fields.CharField', [], {'max_length': '10', 'db_column': "'ZONE'"})
        },
        u'core.servicemenucondition': {
            'Meta': {'object_name': 'ServiceMenuCondition', 'db_table': "'CORE_SERVICE_MENU_CONDITION'"},
            'action': ('django.db.models.fields.CharField', [], {'default': "'render'", 'max_length': '20', 'db_column': "'ACTION'"}),
            'condition': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Condition']", 'null': 'True', 'db_column': "'ID_CORE_CONDITION'", 'blank': 'True'}),
            'dateCreate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'DATE_CREATE'", 'blank': 'True'}),
            'dateModify': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'DATE_MODIFY'", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'ID_CORE_SERVICE_MENU_CONDITION'"}),
            'isDeleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'IS_DELETED'"}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '10', 'db_column': "'ORDER'"}),
            'serviceMenu': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.ServiceMenu']", 'db_column': "'ID_CORE_SERVICE_MENU'"}),
            'userCreateId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_CREATE_ID'", 'blank': 'True'}),
            'userModifyId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_MODIFY_ID'", 'blank': 'True'}),
            'value': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_column': "'VALUE'"})
        },
        u'core.setting': {
            'Meta': {'object_name': 'Setting', 'db_table': "'CORE_SETTING'"},
            'application': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'core_setting_app'", 'null': 'True', 'db_column': "'ID_CORE_APPLICATION'", 'to': u"orm['core.Application']"}),
            'dateCreate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'DATE_CREATE'", 'blank': 'True'}),
            'dateModify': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'DATE_MODIFY'", 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_column': "'DESCRIPTION'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'ID_CORE_SETTING'"}),
            'isDeleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'IS_DELETED'"}),
            'mustAutoload': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'MUST_AUTOLOAD'"}),
            'name': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.MetaKey']", 'db_column': "'ID_META'"}),
            'userCreateId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_CREATE_ID'", 'blank': 'True'}),
            'userModifyId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_MODIFY_ID'", 'blank': 'True'}),
            'value': ('django.db.models.fields.TextField', [], {'db_column': "'VALUE'"})
        },
        u'core.view': {
            'Meta': {'unique_together': "(('application', 'name'),)", 'object_name': 'View', 'db_table': "'CORE_VIEW'"},
            'accessGroups': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'view_access'", 'symmetrical': 'False', 'through': u"orm['core.ViewAccessGroup']", 'to': u"orm['site.Group']"}),
            'application': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Application']", 'db_column': "'ID_APPLICATION'"}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['site.Category']", 'null': 'True', 'db_column': "'ID_CATEGORY'", 'blank': 'True'}),
            'dateCreate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'DATE_CREATE'", 'blank': 'True'}),
            'dateModify': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'DATE_MODIFY'", 'blank': 'True'}),
            'hasAuth': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'HAS_AUTH'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'ID_CORE_VIEW'"}),
            'image': ('filebrowser.fields.FileBrowseField', [], {'max_length': '200', 'null': 'True', 'db_column': "'IMAGE'", 'blank': 'True'}),
            'implementation': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'IMPLEMENTATION'"}),
            'isDeleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'IS_DELETED'"}),
            'menus': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'view_menus'", 'symmetrical': 'False', 'through': u"orm['core.ViewMenu']", 'to': u"orm['core.Menu']"}),
            'meta': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'view_meta'", 'symmetrical': 'False', 'through': u"orm['core.ViewMeta']", 'to': u"orm['core.MetaKey']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'db_column': "'NAME'"}),
            'params': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'view_params'", 'to': u"orm['core.Param']", 'through': u"orm['core.ViewParamValue']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'view_parent'", 'null': 'True', 'db_column': "'ID_PARENT'", 'to': u"orm['core.View']"}),
            'service': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Service']", 'db_column': "'ID_SERVICE'"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_column': "'SLUG'"}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'view_tags'", 'to': u"orm['site.Tag']", 'through': u"orm['core.ViewTag']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'templates': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'view_templates'", 'symmetrical': 'False', 'through': u"orm['core.ViewTmpl']", 'to': u"orm['core.XpTemplate']"}),
            'userCreateId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_CREATE_ID'", 'blank': 'True'}),
            'userModifyId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_MODIFY_ID'", 'blank': 'True'}),
            'winType': ('django.db.models.fields.CharField', [], {'default': "'window'", 'max_length': '20', 'db_column': "'WIN_TYPE'"})
        },
        u'core.viewaccessgroup': {
            'Meta': {'object_name': 'ViewAccessGroup', 'db_table': "'CORE_VIEW_ACCESS_GROUP'"},
            'dateCreate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'DATE_CREATE'", 'blank': 'True'}),
            'dateModify': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'DATE_MODIFY'", 'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['site.Group']", 'db_column': "'ID_GROUP'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'ID_SITE_GROUP_CHANNEL_ACCESS'"}),
            'isDeleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'IS_DELETED'"}),
            'userCreateId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_CREATE_ID'", 'blank': 'True'}),
            'userModifyId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_MODIFY_ID'", 'blank': 'True'}),
            'view': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.View']", 'db_column': "'ID_VIEW'"})
        },
        u'core.viewmenu': {
            'Meta': {'unique_together': "(('menu', 'view'),)", 'object_name': 'ViewMenu', 'db_table': "'CORE_VIEW_MENU'"},
            'conditions': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'viewmenu_conditions'", 'to': u"orm['core.Condition']", 'through': u"orm['core.ViewMenuCondition']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'dateCreate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'DATE_CREATE'", 'blank': 'True'}),
            'dateModify': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'DATE_MODIFY'", 'blank': 'True'}),
            'hasSeparator': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'HAS_SEPARATOR'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'ID_CORE_VIEW_MENU'"}),
            'isDeleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'IS_DELETED'"}),
            'menu': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Menu']", 'db_column': "'ID_MENU'"}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '10', 'db_column': "'ORDER'"}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.ViewMenu']", 'null': 'True', 'db_column': "'ID_PARENT'", 'blank': 'True'}),
            'userCreateId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_CREATE_ID'", 'blank': 'True'}),
            'userModifyId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_MODIFY_ID'", 'blank': 'True'}),
            'view': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.View']", 'null': 'True', 'db_column': "'ID_VIEW'", 'blank': 'True'}),
            'zone': ('django.db.models.fields.CharField', [], {'max_length': '10', 'db_column': "'ZONE'"})
        },
        u'core.viewmenucondition': {
            'Meta': {'object_name': 'ViewMenuCondition', 'db_table': "'CORE_VIEW_MENU_CONDITION'"},
            'action': ('django.db.models.fields.CharField', [], {'default': "'render'", 'max_length': '20', 'db_column': "'ACTION'"}),
            'condition': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Condition']", 'null': 'True', 'db_column': "'ID_CORE_CONDITION'", 'blank': 'True'}),
            'dateCreate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'DATE_CREATE'", 'blank': 'True'}),
            'dateModify': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'DATE_MODIFY'", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'ID_CORE_VIEW_MENU_CONDITION'"}),
            'isDeleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'IS_DELETED'"}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '10', 'db_column': "'ORDER'"}),
            'userCreateId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_CREATE_ID'", 'blank': 'True'}),
            'userModifyId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_MODIFY_ID'", 'blank': 'True'}),
            'value': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_column': "'VALUE'"}),
            'viewMenu': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.ViewMenu']", 'db_column': "'ID_CORE_VIEW_MENU'"})
        },
        u'core.viewmeta': {
            'Meta': {'object_name': 'ViewMeta', 'db_table': "'CORE_VIEW_META'"},
            'dateCreate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'DATE_CREATE'", 'blank': 'True'}),
            'dateModify': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'DATE_MODIFY'", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'ID_CORE_VIEW_META'"}),
            'isDeleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'IS_DELETED'"}),
            'meta': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.MetaKey']", 'db_column': "'ID_META'"}),
            'userCreateId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_CREATE_ID'", 'blank': 'True'}),
            'userModifyId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_MODIFY_ID'", 'blank': 'True'}),
            'value': ('django.db.models.fields.TextField', [], {'db_column': "'VALUE'"}),
            'view': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.View']", 'db_column': "'ID_VIEW'"})
        },
        u'core.viewparamvalue': {
            'Meta': {'object_name': 'ViewParamValue', 'db_table': "'CORE_VIEW_PARAM_VALUE'"},
            'dateCreate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'DATE_CREATE'", 'blank': 'True'}),
            'dateModify': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'DATE_MODIFY'", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'ID_CORE_VIEW_PARAM_VALUE'"}),
            'isDeleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'IS_DELETED'"}),
            'name': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Param']", 'db_column': "'ID_NAME'"}),
            'operator': ('django.db.models.fields.CharField', [], {'max_length': '10', 'db_column': "'OPERATOR'"}),
            'userCreateId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_CREATE_ID'", 'blank': 'True'}),
            'userModifyId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_MODIFY_ID'", 'blank': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '20', 'db_column': "'VALUE'"}),
            'view': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'viewParam'", 'db_column': "'ID_VIEW'", 'to': u"orm['core.View']"})
        },
        u'core.viewtag': {
            'Meta': {'object_name': 'ViewTag', 'db_table': "'CORE_VIEW_TAG'"},
            'dateCreate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'DATE_CREATE'", 'blank': 'True'}),
            'dateModify': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'DATE_MODIFY'", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'ID_CORE_VIEW_TAG'"}),
            'isDeleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'IS_DELETED'"}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['site.Tag']", 'db_column': "'ID_TAG'"}),
            'userCreateId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_CREATE_ID'", 'blank': 'True'}),
            'userModifyId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_MODIFY_ID'", 'blank': 'True'}),
            'view': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.View']", 'db_column': "'ID_VIEW'"})
        },
        u'core.viewtmpl': {
            'Meta': {'object_name': 'ViewTmpl', 'db_table': "'CORE_VIEW_TMPL'"},
            'dateCreate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'DATE_CREATE'", 'blank': 'True'}),
            'dateModify': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'DATE_MODIFY'", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'ID_CORE_VIEW_TMPL'"}),
            'isDeleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'IS_DELETED'"}),
            'template': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.XpTemplate']", 'db_column': "'ID_TEMPLATE'"}),
            'userCreateId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_CREATE_ID'", 'blank': 'True'}),
            'userModifyId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_MODIFY_ID'", 'blank': 'True'}),
            'view': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.View']", 'db_column': "'ID_VIEW'"})
        },
        u'core.wfparamvalue': {
            'Meta': {'object_name': 'WFParamValue', 'db_table': "'CORE_WORKFLOW_PARAM_VALUE'"},
            'dateCreate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'DATE_CREATE'", 'blank': 'True'}),
            'dateModify': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'DATE_MODIFY'", 'blank': 'True'}),
            'flowView': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'flowViewParamValue'", 'db_column': "'ID_FLOW_VIEW'", 'to': u"orm['core.WorkflowView']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'ID_CORE_WORKFLOW_PARAM_VALUE'"}),
            'isDeleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'IS_DELETED'"}),
            'name': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Param']", 'db_column': "'ID_NAME'"}),
            'operator': ('django.db.models.fields.CharField', [], {'max_length': '10', 'db_column': "'OPERATOR'"}),
            'userCreateId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_CREATE_ID'", 'blank': 'True'}),
            'userModifyId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_MODIFY_ID'", 'blank': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '20', 'db_column': "'VALUE'"})
        },
        u'core.word': {
            'Meta': {'object_name': 'Word', 'db_table': "'CORE_WORD'"},
            'dateCreate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'DATE_CREATE'", 'blank': 'True'}),
            'dateModify': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'DATE_MODIFY'", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'ID_CORE_WORD'"}),
            'isDeleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'IS_DELETED'"}),
            'userCreateId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_CREATE_ID'", 'blank': 'True'}),
            'userModifyId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_MODIFY_ID'", 'blank': 'True'}),
            'word': ('django.db.models.fields.CharField', [], {'max_length': '20', 'db_column': "'WORD'", 'db_index': 'True'})
        },
        u'core.workflow': {
            'Meta': {'object_name': 'Workflow', 'db_table': "'CORE_WORKFLOW'"},
            'application': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Application']", 'db_column': "'ID_APPLICATION'"}),
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '15', 'db_column': "'CODE'", 'db_index': 'True'}),
            'dateCreate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'DATE_CREATE'", 'blank': 'True'}),
            'dateModify': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'DATE_MODIFY'", 'blank': 'True'}),
            'deleteOnEnd': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'DELETE_ON_END'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'ID_CORE_WORKFLOW'"}),
            'isDeleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'IS_DELETED'"}),
            'jumpToView': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_column': "'JUMP_TO_VIEW'"}),
            'resetStart': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'RESET_START'"}),
            'userCreateId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_CREATE_ID'", 'blank': 'True'}),
            'userModifyId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_MODIFY_ID'", 'blank': 'True'})
        },
        u'core.workflowdata': {
            'Meta': {'unique_together': "(('userId', 'flow'),)", 'object_name': 'WorkflowData', 'db_table': "'CORE_WORKFLOW_DATA'"},
            'data': ('django.db.models.fields.TextField', [], {'default': "'eyJkYXRhIjoge30sICJ2aWV3TmFtZSI6ICIifQ==\\n'", 'db_column': "'DATA'"}),
            'dateCreate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'DATE_CREATE'", 'blank': 'True'}),
            'dateModify': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'DATE_MODIFY'", 'blank': 'True'}),
            'flow': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'flowData'", 'db_column': "'ID_FLOW'", 'to': u"orm['core.Workflow']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'ID_CORE_WORKFLOW_DATA'"}),
            'isDeleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'IS_DELETED'"}),
            'userCreateId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_CREATE_ID'", 'blank': 'True'}),
            'userId': ('django.db.models.fields.CharField', [], {'max_length': '40', 'db_column': "'USER_ID'"}),
            'userModifyId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_MODIFY_ID'", 'blank': 'True'}),
            'view': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'viewFlowData'", 'db_column': "'ID_VIEW'", 'to': u"orm['core.View']"})
        },
        u'core.workflowview': {
            'Meta': {'object_name': 'WorkflowView', 'db_table': "'CORE_WORKFLOW_VIEW'"},
            'action': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'wf_action'", 'db_column': "'ID_ACTION'", 'to': u"orm['core.Action']"}),
            'dateCreate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'DATE_CREATE'", 'blank': 'True'}),
            'dateModify': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'DATE_MODIFY'", 'blank': 'True'}),
            'flow': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'flowView'", 'db_column': "'ID_FLOW'", 'to': u"orm['core.Workflow']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'ID_CORE_WORKFLOW_VIEW'"}),
            'isDeleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'IS_DELETED'"}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '10', 'db_column': "'ORDER'"}),
            'params': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'flowView_params'", 'to': u"orm['core.Param']", 'through': u"orm['core.WFParamValue']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'userCreateId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_CREATE_ID'", 'blank': 'True'}),
            'userModifyId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_MODIFY_ID'", 'blank': 'True'}),
            'viewSource': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'flowViewSource'", 'null': 'True', 'db_column': "'ID_VIEW_SOURCE'", 'to': u"orm['core.View']"}),
            'viewTarget': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'flowViewTarget'", 'db_column': "'ID_VIEW_TARGET'", 'to': u"orm['core.View']"})
        },
        u'core.xptemplate': {
            'Meta': {'unique_together': "(('application', 'name'),)", 'object_name': 'XpTemplate', 'db_table': "'CORE_TEMPLATE'"},
            'alias': ('django.db.models.fields.CharField', [], {'max_length': '20', 'db_column': "'ALIAS'"}),
            'application': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Application']", 'db_column': "'ID_APPLICATION'"}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'db_column': "'COUNTRY'", 'blank': 'True'}),
            'dateCreate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'DATE_CREATE'", 'blank': 'True'}),
            'dateModify': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'DATE_MODIFY'", 'blank': 'True'}),
            'device': ('django.db.models.fields.CharField', [], {'default': "'PC'", 'max_length': '10', 'db_column': "'DEVICE'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'ID_CORE_TEMPLATE'"}),
            'isDeleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'IS_DELETED'"}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'en'", 'max_length': '2', 'db_column': "'LANGUAGE'"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_column': "'NAME'"}),
            'userCreateId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_CREATE_ID'", 'blank': 'True'}),
            'userModifyId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_MODIFY_ID'", 'blank': 'True'}),
            'winType': ('django.db.models.fields.CharField', [], {'default': "'window'", 'max_length': '20', 'db_column': "'WIN_TYPE'"})
        },
        u'site.category': {
            'Meta': {'object_name': 'Category', 'db_table': "'SITE_CATEGORY'"},
            'dateCreate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'DATE_CREATE'", 'blank': 'True'}),
            'dateModify': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'DATE_MODIFY'", 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'DESCRIPTION'", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'ID_SITE_CATEGORY'"}),
            'image': ('filebrowser.fields.FileBrowseField', [], {'max_length': '200', 'null': 'True', 'db_column': "'IMAGE'", 'blank': 'True'}),
            'isDeleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'IS_DELETED'"}),
            'isPublic': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_column': "'IS_PUBLIC'"}),
            'isPublished': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'IS_PUBLISHED'"}),
            'menuOrder': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1', 'db_column': "'MENU_ORDER'"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '55', 'db_column': "'NAME'"}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'category_parent'", 'null': 'True', 'db_column': "'ID_PARENT'", 'to': u"orm['site.Category']"}),
            'popularity': ('django.db.models.fields.IntegerField', [], {'default': '1', 'null': 'True', 'db_column': "'POPULARITY'", 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '200', 'db_column': "'SLUG'"}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['site.Param']", 'db_column': "'ID_SITE_PARAMETER'"}),
            'userCreateId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_CREATE_ID'", 'blank': 'True'}),
            'userModifyId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_MODIFY_ID'", 'blank': 'True'})
        },
        u'site.group': {
            'Meta': {'object_name': 'Group', 'db_table': "'SITE_GROUP'"},
            'accessGroups': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'group_access'", 'symmetrical': 'False', 'through': u"orm['site.GroupAccess']", 'to': u"orm['site.Group']"}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['site.Category']", 'db_column': "'ID_CATEGORY'"}),
            'dateCreate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'DATE_CREATE'", 'blank': 'True'}),
            'dateModify': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'DATE_MODIFY'", 'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.Group']", 'unique': 'True', 'db_column': "'ID_GROUP_SYS'"}),
            'groupNameId': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'db_column': "'GROUP_NAME_ID'", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'ID_SITE_GROUP'"}),
            'isDeleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'IS_DELETED'"}),
            'isPublic': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_column': "'IS_PUBLIC'"}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'groupchannel_parent'", 'null': 'True', 'db_column': "'ID_PARENT'", 'to': u"orm['site.Group']"}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'groupchannel_tags'", 'to': u"orm['site.Tag']", 'through': u"orm['site.GroupTag']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'userCreateId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_CREATE_ID'", 'blank': 'True'}),
            'userModifyId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_MODIFY_ID'", 'blank': 'True'})
        },
        u'site.groupaccess': {
            'Meta': {'object_name': 'GroupAccess', 'db_table': "'SITE_GROUP_ACCESS'"},
            'dateCreate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'DATE_CREATE'", 'blank': 'True'}),
            'dateModify': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'DATE_MODIFY'", 'blank': 'True'}),
            'groupFrom': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'groupaccess_from'", 'db_column': "'ID_GROUP_FROM'", 'to': u"orm['site.Group']"}),
            'groupTo': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'groupaccess_to'", 'db_column': "'ID_GROUP_TO'", 'to': u"orm['site.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'ID_SITE_GROUP_ACCESS'"}),
            'isDeleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'IS_DELETED'"}),
            'userCreateId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_CREATE_ID'", 'blank': 'True'}),
            'userModifyId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_MODIFY_ID'", 'blank': 'True'})
        },
        u'site.grouptag': {
            'Meta': {'object_name': 'GroupTag', 'db_table': "'SITE_GROUP_TAG'"},
            'dateCreate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'DATE_CREATE'", 'blank': 'True'}),
            'dateModify': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'DATE_MODIFY'", 'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['site.Group']", 'db_column': "'ID_GROUP'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'ID_SITE_GROUP_TAG'"}),
            'isDeleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'IS_DELETED'"}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['site.Tag']", 'db_column': "'ID_TAG'"}),
            'userCreateId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_CREATE_ID'", 'blank': 'True'}),
            'userModifyId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_MODIFY_ID'", 'blank': 'True'})
        },
        u'site.param': {
            'Meta': {'object_name': 'Param', 'db_table': "'SITE_PARAMETER'"},
            'dateCreate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'DATE_CREATE'", 'blank': 'True'}),
            'dateModify': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'DATE_MODIFY'", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'ID_SITE_PARAMETER'"}),
            'isDeleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'IS_DELETED'"}),
            'mode': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'db_column': "'MODE'", 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20', 'db_column': "'NAME'"}),
            'paramType': ('django.db.models.fields.CharField', [], {'default': "'string'", 'max_length': '10', 'db_column': "'PARAM_TYPE'"}),
            'userCreateId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_CREATE_ID'", 'blank': 'True'}),
            'userModifyId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_MODIFY_ID'", 'blank': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'db_column': "'VALUE'", 'blank': 'True'})
        },
        u'site.tag': {
            'Meta': {'ordering': "['-popularity']", 'object_name': 'Tag', 'db_table': "'SITE_TAG'"},
            'dateCreate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'DATE_CREATE'", 'blank': 'True'}),
            'dateModify': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'DATE_MODIFY'", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'ID_SITE_TAG'"}),
            'isDeleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'IS_DELETED'"}),
            'isPublic': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_column': "'IS_PUBLIC'"}),
            'mode': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tag_mode'", 'db_column': "'ID_MODE'", 'to': u"orm['site.TagMode']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'db_column': "'NAME'"}),
            'popularity': ('django.db.models.fields.IntegerField', [], {'default': '1', 'null': 'True', 'db_column': "'POPULARITY'", 'blank': 'True'}),
            'userCreateId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_CREATE_ID'", 'blank': 'True'}),
            'userModifyId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_MODIFY_ID'", 'blank': 'True'})
        },
        u'site.tagmode': {
            'Meta': {'object_name': 'TagMode', 'db_table': "'SITE_TAG_MODE'"},
            'dateCreate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'DATE_CREATE'", 'blank': 'True'}),
            'dateModify': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'DATE_MODIFY'", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'ID_SITE_TAG_MODE'"}),
            'isDeleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'IS_DELETED'"}),
            'isPublic': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_column': "'IS_PUBLIC'"}),
            'mode': ('django.db.models.fields.CharField', [], {'max_length': '30', 'db_column': "'MODE'"}),
            'userCreateId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_CREATE_ID'", 'blank': 'True'}),
            'userModifyId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_MODIFY_ID'", 'blank': 'True'})
        }
    }

    complete_apps = ['core']