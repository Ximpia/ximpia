# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ServiceMeta'
        db.create_table('CORE_SERVICE_META', (
            ('dateCreate', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_column='DATE_CREATE', blank=True)),
            ('dateModify', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, db_column='DATE_MODIFY', blank=True)),
            ('userCreateId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_CREATE_ID', blank=True)),
            ('userModifyId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_MODIFY_ID', blank=True)),
            ('isDeleted', self.gf('django.db.models.fields.BooleanField')(default=False, db_column='IS_DELETED')),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column='ID_CORE_SERVICE_META')),
            ('service', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['xpcore.Service'], db_column='ID_SERVICE')),
            ('meta', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['xpcore.MetaKey'], db_column='ID_META')),
            ('value', self.gf('django.db.models.fields.TextField')(db_column='VALUE')),
        ))
        db.send_create_signal(u'xpcore', ['ServiceMeta'])

        # Adding model 'WorkflowMeta'
        db.create_table('CORE_WORKFLOW_META', (
            ('dateCreate', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_column='DATE_CREATE', blank=True)),
            ('dateModify', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, db_column='DATE_MODIFY', blank=True)),
            ('userCreateId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_CREATE_ID', blank=True)),
            ('userModifyId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_MODIFY_ID', blank=True)),
            ('isDeleted', self.gf('django.db.models.fields.BooleanField')(default=False, db_column='IS_DELETED')),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column='ID_CORE_WORKFLOW_META')),
            ('workflow', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['xpcore.Workflow'], db_column='ID_WORKFLOW')),
            ('meta', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['xpcore.MetaKey'], db_column='ID_META')),
            ('value', self.gf('django.db.models.fields.TextField')(db_column='VALUE')),
        ))
        db.send_create_signal(u'xpcore', ['WorkflowMeta'])

        # Adding field 'Application.isActive'
        db.add_column('CORE_APPLICATION', 'isActive',
                      self.gf('django.db.models.fields.BooleanField')(default=True, db_column='IS_ACTIVE'),
                      keep_default=False)

        # Adding field 'Service.isActive'
        db.add_column('CORE_SERVICE', 'isActive',
                      self.gf('django.db.models.fields.BooleanField')(default=True, db_column='IS_ACTIVE'),
                      keep_default=False)

        # Deleting field 'Workflow.jumpToView'
        db.delete_column('CORE_WORKFLOW', 'JUMP_TO_VIEW')

        # Deleting field 'Workflow.resetStart'
        db.delete_column('CORE_WORKFLOW', 'RESET_START')

        # Deleting field 'Workflow.deleteOnEnd'
        db.delete_column('CORE_WORKFLOW', 'DELETE_ON_END')


        # Changing field 'WorkflowView.action'
        db.alter_column('CORE_WORKFLOW_VIEW', 'ID_ACTION', self.gf('django.db.models.fields.related.ForeignKey')(null=True, db_column='ID_ACTION', to=orm['xpcore.Action']))


    def backwards(self, orm):
        # Deleting model 'ServiceMeta'
        db.delete_table('CORE_SERVICE_META')

        # Deleting model 'WorkflowMeta'
        db.delete_table('CORE_WORKFLOW_META')

        # Deleting field 'Application.isActive'
        db.delete_column('CORE_APPLICATION', 'IS_ACTIVE')

        # Deleting field 'Service.isActive'
        db.delete_column('CORE_SERVICE', 'IS_ACTIVE')

        # Adding field 'Workflow.jumpToView'
        db.add_column('CORE_WORKFLOW', 'jumpToView',
                      self.gf('django.db.models.fields.BooleanField')(default=True, db_column='JUMP_TO_VIEW'),
                      keep_default=False)

        # Adding field 'Workflow.resetStart'
        db.add_column('CORE_WORKFLOW', 'resetStart',
                      self.gf('django.db.models.fields.BooleanField')(default=False, db_column='RESET_START'),
                      keep_default=False)

        # Adding field 'Workflow.deleteOnEnd'
        db.add_column('CORE_WORKFLOW', 'deleteOnEnd',
                      self.gf('django.db.models.fields.BooleanField')(default=False, db_column='DELETE_ON_END'),
                      keep_default=False)


        # Changing field 'WorkflowView.action'
        db.alter_column('CORE_WORKFLOW_VIEW', 'ID_ACTION', self.gf('django.db.models.fields.related.ForeignKey')(default='', db_column='ID_ACTION', to=orm['xpcore.Action']))


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
        u'xpcore.action': {
            'Meta': {'unique_together': "(('application', 'name'),)", 'object_name': 'Action', 'db_table': "'CORE_ACTION'"},
            'accessGroups': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'action_access'", 'symmetrical': 'False', 'through': u"orm['xpcore.ActionAccessGroup']", 'to': u"orm['xpsite.Group']"}),
            'application': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['xpcore.Application']", 'db_column': "'ID_APPLICATION'"}),
            'dateCreate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'DATE_CREATE'", 'blank': 'True'}),
            'dateModify': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'DATE_MODIFY'", 'blank': 'True'}),
            'hasAuth': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'HAS_AUTH'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'ID_CORE_ACTION'"}),
            'image': ('filebrowser.fields.FileBrowseField', [], {'max_length': '200', 'null': 'True', 'db_column': "'IMAGE'", 'blank': 'True'}),
            'implementation': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'IMPLEMENTATION'"}),
            'isDeleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'IS_DELETED'"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'db_column': "'NAME'"}),
            'service': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['xpcore.Service']", 'db_column': "'ID_SERVICE'"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_column': "'SLUG'"}),
            'userCreateId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_CREATE_ID'", 'blank': 'True'}),
            'userModifyId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_MODIFY_ID'", 'blank': 'True'})
        },
        u'xpcore.actionaccessgroup': {
            'Meta': {'object_name': 'ActionAccessGroup', 'db_table': "'CORE_ACTION_ACCESS_GROUP'"},
            'action': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['xpcore.Action']", 'db_column': "'ID_ACTION'"}),
            'dateCreate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'DATE_CREATE'", 'blank': 'True'}),
            'dateModify': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'DATE_MODIFY'", 'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['xpsite.Group']", 'db_column': "'ID_GROUP'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'ID_SITE_GROUP_CHANNEL_ACCESS'"}),
            'isDeleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'IS_DELETED'"}),
            'userCreateId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_CREATE_ID'", 'blank': 'True'}),
            'userModifyId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_MODIFY_ID'", 'blank': 'True'})
        },
        u'xpcore.application': {
            'Meta': {'object_name': 'Application', 'db_table': "'CORE_APPLICATION'"},
            'accessGroup': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'app_access'", 'db_column': "'ID_GROUP'", 'to': u"orm['xpsite.Group']"}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['xpsite.Category']", 'null': 'True', 'db_column': "'ID_CATEGORY'", 'blank': 'True'}),
            'dateCreate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'DATE_CREATE'", 'blank': 'True'}),
            'dateModify': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'DATE_MODIFY'", 'blank': 'True'}),
            'developer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'db_column': "'ID_DEVELOPER'", 'blank': 'True'}),
            'developerOrg': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'app_dev_org'", 'null': 'True', 'db_column': "'ID_DEVELOPER_ORG'", 'to': u"orm['xpsite.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'ID_CORE_APPLICATION'"}),
            'isActive': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_column': "'IS_ACTIVE'"}),
            'isAdmin': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'IS_ADMIN'"}),
            'isDeleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'IS_DELETED'"}),
            'isPrivate': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'IS_PRIVATE'"}),
            'isSubscription': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'IS_SUBSCRIPTION'"}),
            'meta': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'app_meta'", 'symmetrical': 'False', 'through': u"orm['xpcore.ApplicationMeta']", 'to': u"orm['xpcore.MetaKey']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['xpcore.Application']", 'null': 'True', 'db_column': "'ID_PARENT'", 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '30', 'db_column': "'SLUG'"}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'application_tags'", 'to': u"orm['xpsite.Tag']", 'through': u"orm['xpcore.ApplicationTag']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '30', 'db_column': "'TITLE'"}),
            'userCreateId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_CREATE_ID'", 'blank': 'True'}),
            'userModifyId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_MODIFY_ID'", 'blank': 'True'})
        },
        u'xpcore.applicationmedia': {
            'Meta': {'object_name': 'ApplicationMedia', 'db_table': "'CORE_APPLICATION_MEDIA'"},
            'application': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['xpcore.Application']", 'db_column': "'ID_APPLICATION'"}),
            'dateCreate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'DATE_CREATE'", 'blank': 'True'}),
            'dateModify': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'DATE_MODIFY'", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'ID_CORE_APPLICATION_MEDIA'"}),
            'image': ('filebrowser.fields.FileBrowseField', [], {'max_length': '200', 'null': 'True', 'db_column': "'IMAGE'", 'blank': 'True'}),
            'isDeleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'IS_DELETED'"}),
            'menuOrder': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1', 'db_column': "'MENU_ORDER'"}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['xpcore.CoreParam']", 'db_column': "'ID_TYPE'"}),
            'userCreateId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_CREATE_ID'", 'blank': 'True'}),
            'userModifyId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_MODIFY_ID'", 'blank': 'True'})
        },
        u'xpcore.applicationmeta': {
            'Meta': {'object_name': 'ApplicationMeta', 'db_table': "'CORE_APPLICATION_META'"},
            'application': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['xpcore.Application']", 'db_column': "'ID_APPLICATION'"}),
            'dateCreate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'DATE_CREATE'", 'blank': 'True'}),
            'dateModify': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'DATE_MODIFY'", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'ID_CORE_APPLICATION_META'"}),
            'isDeleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'IS_DELETED'"}),
            'meta': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['xpcore.MetaKey']", 'db_column': "'ID_META'"}),
            'userCreateId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_CREATE_ID'", 'blank': 'True'}),
            'userModifyId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_MODIFY_ID'", 'blank': 'True'}),
            'value': ('django.db.models.fields.TextField', [], {'db_column': "'VALUE'"})
        },
        u'xpcore.applicationtag': {
            'Meta': {'object_name': 'ApplicationTag', 'db_table': "'CORE_APPLICATION_TAG'"},
            'application': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['xpcore.Application']", 'db_column': "'ID_VIEW'"}),
            'dateCreate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'DATE_CREATE'", 'blank': 'True'}),
            'dateModify': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'DATE_MODIFY'", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'ID_CORE_APPLICATION_TAG'"}),
            'isDeleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'IS_DELETED'"}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['xpsite.Tag']", 'db_column': "'ID_TAG'"}),
            'userCreateId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_CREATE_ID'", 'blank': 'True'}),
            'userModifyId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_MODIFY_ID'", 'blank': 'True'})
        },
        u'xpcore.condition': {
            'Meta': {'object_name': 'Condition', 'db_table': "'CORE_CONDITION'"},
            'dateCreate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'DATE_CREATE'", 'blank': 'True'}),
            'dateModify': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'DATE_MODIFY'", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'ID_CORE_CONDITION'"}),
            'isDeleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'IS_DELETED'"}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30', 'db_column': "'NAME'"}),
            'rule': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_column': "'RULE'"}),
            'userCreateId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_CREATE_ID'", 'blank': 'True'}),
            'userModifyId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_MODIFY_ID'", 'blank': 'True'})
        },
        u'xpcore.coreparam': {
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
        u'xpcore.menu': {
            'Meta': {'object_name': 'Menu', 'db_table': "'CORE_MENU'"},
            'action': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'menu_action'", 'null': 'True', 'db_column': "'ID_ACTION'", 'to': u"orm['xpcore.Action']"}),
            'application': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['xpcore.Application']", 'db_column': "'ID_APPLICATION'"}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'db_column': "'COUNTRY'", 'blank': 'True'}),
            'dateCreate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'DATE_CREATE'", 'blank': 'True'}),
            'dateModify': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'DATE_MODIFY'", 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'db_column': "'DESCRIPTION'", 'blank': 'True'}),
            'device': ('django.db.models.fields.CharField', [], {'default': "'PC'", 'max_length': '10', 'db_column': "'DEVICE'"}),
            'icon': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['xpcore.CoreParam']", 'null': 'True', 'db_column': "'ID_ICON'", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'ID_CORE_MENU'"}),
            'isDeleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'IS_DELETED'"}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'en'", 'max_length': '2', 'db_column': "'LANGUAGE'"}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20', 'db_column': "'NAME'"}),
            'params': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'menu_params'", 'to': u"orm['xpcore.Param']", 'through': u"orm['xpcore.MenuParam']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'db_column': "'TITLE'", 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'db_column': "'URL'", 'blank': 'True'}),
            'urlTarget': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'db_column': "'URL_TARGET'", 'blank': 'True'}),
            'userCreateId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_CREATE_ID'", 'blank': 'True'}),
            'userModifyId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_MODIFY_ID'", 'blank': 'True'}),
            'view': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'menu_view'", 'null': 'True', 'db_column': "'ID_VIEW'", 'to': u"orm['xpcore.View']"})
        },
        u'xpcore.menuparam': {
            'Meta': {'object_name': 'MenuParam', 'db_table': "'CORE_MENU_PARAM'"},
            'dateCreate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'DATE_CREATE'", 'blank': 'True'}),
            'dateModify': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'DATE_MODIFY'", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'ID_CORE_MENU_PARAM'"}),
            'isDeleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'IS_DELETED'"}),
            'menu': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['xpcore.Menu']", 'db_column': "'ID_MENU'"}),
            'name': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['xpcore.Param']", 'db_column': "'ID_NAME'"}),
            'operator': ('django.db.models.fields.CharField', [], {'max_length': '10', 'db_column': "'OPERATOR'"}),
            'userCreateId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_CREATE_ID'", 'blank': 'True'}),
            'userModifyId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_MODIFY_ID'", 'blank': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '20', 'db_column': "'VALUE'"})
        },
        u'xpcore.metakey': {
            'Meta': {'ordering': "['name']", 'object_name': 'MetaKey', 'db_table': "'CORE_META_KEY'"},
            'dateCreate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'DATE_CREATE'", 'blank': 'True'}),
            'dateModify': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'DATE_MODIFY'", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'ID_CORE_META_KEY'"}),
            'isDeleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'IS_DELETED'"}),
            'keyType': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['xpcore.CoreParam']", 'db_column': "'ID_META_TYPE'"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'NAME'"}),
            'userCreateId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_CREATE_ID'", 'blank': 'True'}),
            'userModifyId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_MODIFY_ID'", 'blank': 'True'})
        },
        u'xpcore.param': {
            'Meta': {'unique_together': "(('application', 'name'),)", 'object_name': 'Param', 'db_table': "'CORE_PARAM'"},
            'application': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['xpcore.Application']", 'db_column': "'ID_APPLICATION'"}),
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
        u'xpcore.searchindex': {
            'Meta': {'unique_together': "(('view', 'action'),)", 'object_name': 'SearchIndex', 'db_table': "'CORE_SEARCH_INDEX'"},
            'action': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'index_action'", 'null': 'True', 'db_column': "'ID_ACTION'", 'to': u"orm['xpcore.Action']"}),
            'application': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['xpcore.Application']", 'db_column': "'ID_APPLICATION'"}),
            'dateCreate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'DATE_CREATE'", 'blank': 'True'}),
            'dateModify': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'DATE_MODIFY'", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'ID_CORE_SEARCH_INDEX'"}),
            'isDeleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'IS_DELETED'"}),
            'params': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'index_params'", 'to': u"orm['xpcore.Param']", 'through': u"orm['xpcore.SearchIndexParam']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '70', 'db_column': "'TITLE'"}),
            'userCreateId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_CREATE_ID'", 'blank': 'True'}),
            'userModifyId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_MODIFY_ID'", 'blank': 'True'}),
            'view': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'index_view'", 'null': 'True', 'db_column': "'ID_VIEW'", 'to': u"orm['xpcore.View']"}),
            'words': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'index_words'", 'symmetrical': 'False', 'through': u"orm['xpcore.SearchIndexWord']", 'to': u"orm['xpcore.Word']"})
        },
        u'xpcore.searchindexparam': {
            'Meta': {'object_name': 'SearchIndexParam', 'db_table': "'CORE_INDEX_PARAM'"},
            'dateCreate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'DATE_CREATE'", 'blank': 'True'}),
            'dateModify': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'DATE_MODIFY'", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'ID_CORE_INDEX_PARAM'"}),
            'isDeleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'IS_DELETED'"}),
            'name': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['xpcore.Param']", 'db_column': "'ID_NAME'"}),
            'operator': ('django.db.models.fields.CharField', [], {'max_length': '10', 'db_column': "'OPERATOR'"}),
            'searchIndex': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['xpcore.SearchIndex']", 'db_column': "'ID_SEARCH_INDEX'"}),
            'userCreateId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_CREATE_ID'", 'blank': 'True'}),
            'userModifyId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_MODIFY_ID'", 'blank': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '20', 'db_column': "'VALUE'"})
        },
        u'xpcore.searchindexword': {
            'Meta': {'object_name': 'SearchIndexWord', 'db_table': "'CORE_SEARCH_INDEX_WORD'"},
            'dateCreate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'DATE_CREATE'", 'blank': 'True'}),
            'dateModify': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'DATE_MODIFY'", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'ID_CORE_SEARCH_INDEX_WORD'"}),
            'index': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['xpcore.SearchIndex']", 'db_column': "'ID_INDEX'"}),
            'isDeleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'IS_DELETED'"}),
            'userCreateId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_CREATE_ID'", 'blank': 'True'}),
            'userModifyId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_MODIFY_ID'", 'blank': 'True'}),
            'word': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['xpcore.Word']", 'db_column': "'ID_WORD'"})
        },
        u'xpcore.service': {
            'Meta': {'unique_together': "(('application', 'name'),)", 'object_name': 'Service', 'db_table': "'CORE_SERVICE'"},
            'application': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['xpcore.Application']", 'db_column': "'ID_APPLICATION'"}),
            'dateCreate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'DATE_CREATE'", 'blank': 'True'}),
            'dateModify': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'DATE_MODIFY'", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'ID_CORE_SERVICE'"}),
            'implementation': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'IMPLEMENTATION'"}),
            'isActive': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_column': "'IS_ACTIVE'"}),
            'isDeleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'IS_DELETED'"}),
            'meta': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'service_meta'", 'symmetrical': 'False', 'through': u"orm['xpcore.ServiceMeta']", 'to': u"orm['xpcore.MetaKey']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'db_column': "'NAME'"}),
            'userCreateId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_CREATE_ID'", 'blank': 'True'}),
            'userModifyId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_MODIFY_ID'", 'blank': 'True'})
        },
        u'xpcore.servicemenu': {
            'Meta': {'object_name': 'ServiceMenu', 'db_table': "'CORE_SERVICE_MENU'"},
            'conditions': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'servicemenu_conditions'", 'to': u"orm['xpcore.Condition']", 'through': u"orm['xpcore.ServiceMenuCondition']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'dateCreate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'DATE_CREATE'", 'blank': 'True'}),
            'dateModify': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'DATE_MODIFY'", 'blank': 'True'}),
            'hasSeparator': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'HAS_SEPARATOR'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'ID_CORE_SERVICE_MENU'"}),
            'isDeleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'IS_DELETED'"}),
            'menu': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['xpcore.Menu']", 'db_column': "'ID_MENU'"}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '10', 'db_column': "'ORDER'"}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['xpcore.ServiceMenu']", 'null': 'True', 'db_column': "'ID_PARENT'", 'blank': 'True'}),
            'service': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['xpcore.Service']", 'db_column': "'ID_SERVICE'"}),
            'userCreateId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_CREATE_ID'", 'blank': 'True'}),
            'userModifyId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_MODIFY_ID'", 'blank': 'True'}),
            'zone': ('django.db.models.fields.CharField', [], {'max_length': '10', 'db_column': "'ZONE'"})
        },
        u'xpcore.servicemenucondition': {
            'Meta': {'object_name': 'ServiceMenuCondition', 'db_table': "'CORE_SERVICE_MENU_CONDITION'"},
            'action': ('django.db.models.fields.CharField', [], {'default': "'render'", 'max_length': '20', 'db_column': "'ACTION'"}),
            'condition': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['xpcore.Condition']", 'null': 'True', 'db_column': "'ID_CORE_CONDITION'", 'blank': 'True'}),
            'dateCreate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'DATE_CREATE'", 'blank': 'True'}),
            'dateModify': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'DATE_MODIFY'", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'ID_CORE_SERVICE_MENU_CONDITION'"}),
            'isDeleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'IS_DELETED'"}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '10', 'db_column': "'ORDER'"}),
            'serviceMenu': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['xpcore.ServiceMenu']", 'db_column': "'ID_CORE_SERVICE_MENU'"}),
            'userCreateId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_CREATE_ID'", 'blank': 'True'}),
            'userModifyId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_MODIFY_ID'", 'blank': 'True'}),
            'value': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_column': "'VALUE'"})
        },
        u'xpcore.servicemeta': {
            'Meta': {'object_name': 'ServiceMeta', 'db_table': "'CORE_SERVICE_META'"},
            'dateCreate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'DATE_CREATE'", 'blank': 'True'}),
            'dateModify': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'DATE_MODIFY'", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'ID_CORE_SERVICE_META'"}),
            'isDeleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'IS_DELETED'"}),
            'meta': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['xpcore.MetaKey']", 'db_column': "'ID_META'"}),
            'service': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['xpcore.Service']", 'db_column': "'ID_SERVICE'"}),
            'userCreateId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_CREATE_ID'", 'blank': 'True'}),
            'userModifyId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_MODIFY_ID'", 'blank': 'True'}),
            'value': ('django.db.models.fields.TextField', [], {'db_column': "'VALUE'"})
        },
        u'xpcore.setting': {
            'Meta': {'object_name': 'Setting', 'db_table': "'CORE_SETTING'"},
            'application': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'xpcore.setting_app'", 'null': 'True', 'db_column': "'ID_CORE_APPLICATION'", 'to': u"orm['xpcore.Application']"}),
            'dateCreate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'DATE_CREATE'", 'blank': 'True'}),
            'dateModify': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'DATE_MODIFY'", 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_column': "'DESCRIPTION'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'ID_CORE_SETTING'"}),
            'isDeleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'IS_DELETED'"}),
            'mustAutoload': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'MUST_AUTOLOAD'"}),
            'name': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['xpcore.MetaKey']", 'db_column': "'ID_META'"}),
            'userCreateId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_CREATE_ID'", 'blank': 'True'}),
            'userModifyId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_MODIFY_ID'", 'blank': 'True'}),
            'value': ('django.db.models.fields.TextField', [], {'db_column': "'VALUE'"})
        },
        u'xpcore.view': {
            'Meta': {'unique_together': "(('application', 'name'),)", 'object_name': 'View', 'db_table': "'CORE_VIEW'"},
            'accessGroups': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'view_access'", 'symmetrical': 'False', 'through': u"orm['xpcore.ViewAccessGroup']", 'to': u"orm['xpsite.Group']"}),
            'application': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['xpcore.Application']", 'db_column': "'ID_APPLICATION'"}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['xpsite.Category']", 'null': 'True', 'db_column': "'ID_CATEGORY'", 'blank': 'True'}),
            'dateCreate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'DATE_CREATE'", 'blank': 'True'}),
            'dateModify': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'DATE_MODIFY'", 'blank': 'True'}),
            'hasAuth': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'HAS_AUTH'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'ID_CORE_VIEW'"}),
            'image': ('filebrowser.fields.FileBrowseField', [], {'max_length': '200', 'null': 'True', 'db_column': "'IMAGE'", 'blank': 'True'}),
            'implementation': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'IMPLEMENTATION'"}),
            'isDeleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'IS_DELETED'"}),
            'menus': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'view_menus'", 'symmetrical': 'False', 'through': u"orm['xpcore.ViewMenu']", 'to': u"orm['xpcore.Menu']"}),
            'meta': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'view_meta'", 'symmetrical': 'False', 'through': u"orm['xpcore.ViewMeta']", 'to': u"orm['xpcore.MetaKey']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'db_column': "'NAME'"}),
            'params': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'view_params'", 'to': u"orm['xpcore.Param']", 'through': u"orm['xpcore.ViewParamValue']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'view_parent'", 'null': 'True', 'db_column': "'ID_PARENT'", 'to': u"orm['xpcore.View']"}),
            'service': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['xpcore.Service']", 'db_column': "'ID_SERVICE'"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_column': "'SLUG'"}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'view_tags'", 'to': u"orm['xpsite.Tag']", 'through': u"orm['xpcore.ViewTag']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'templates': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'view_templates'", 'symmetrical': 'False', 'through': u"orm['xpcore.ViewTmpl']", 'to': u"orm['xpcore.XpTemplate']"}),
            'userCreateId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_CREATE_ID'", 'blank': 'True'}),
            'userModifyId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_MODIFY_ID'", 'blank': 'True'}),
            'winType': ('django.db.models.fields.CharField', [], {'default': "'window'", 'max_length': '20', 'db_column': "'WIN_TYPE'"})
        },
        u'xpcore.viewaccessgroup': {
            'Meta': {'object_name': 'ViewAccessGroup', 'db_table': "'CORE_VIEW_ACCESS_GROUP'"},
            'dateCreate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'DATE_CREATE'", 'blank': 'True'}),
            'dateModify': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'DATE_MODIFY'", 'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['xpsite.Group']", 'db_column': "'ID_GROUP'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'ID_SITE_GROUP_CHANNEL_ACCESS'"}),
            'isDeleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'IS_DELETED'"}),
            'userCreateId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_CREATE_ID'", 'blank': 'True'}),
            'userModifyId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_MODIFY_ID'", 'blank': 'True'}),
            'view': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['xpcore.View']", 'db_column': "'ID_VIEW'"})
        },
        u'xpcore.viewmenu': {
            'Meta': {'unique_together': "(('menu', 'view'),)", 'object_name': 'ViewMenu', 'db_table': "'CORE_VIEW_MENU'"},
            'conditions': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'viewmenu_conditions'", 'to': u"orm['xpcore.Condition']", 'through': u"orm['xpcore.ViewMenuCondition']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'dateCreate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'DATE_CREATE'", 'blank': 'True'}),
            'dateModify': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'DATE_MODIFY'", 'blank': 'True'}),
            'hasSeparator': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'HAS_SEPARATOR'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'ID_CORE_VIEW_MENU'"}),
            'isDeleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'IS_DELETED'"}),
            'menu': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['xpcore.Menu']", 'db_column': "'ID_MENU'"}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '10', 'db_column': "'ORDER'"}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['xpcore.ViewMenu']", 'null': 'True', 'db_column': "'ID_PARENT'", 'blank': 'True'}),
            'userCreateId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_CREATE_ID'", 'blank': 'True'}),
            'userModifyId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_MODIFY_ID'", 'blank': 'True'}),
            'view': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['xpcore.View']", 'null': 'True', 'db_column': "'ID_VIEW'", 'blank': 'True'}),
            'zone': ('django.db.models.fields.CharField', [], {'max_length': '10', 'db_column': "'ZONE'"})
        },
        u'xpcore.viewmenucondition': {
            'Meta': {'object_name': 'ViewMenuCondition', 'db_table': "'CORE_VIEW_MENU_CONDITION'"},
            'action': ('django.db.models.fields.CharField', [], {'default': "'render'", 'max_length': '20', 'db_column': "'ACTION'"}),
            'condition': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['xpcore.Condition']", 'null': 'True', 'db_column': "'ID_CORE_CONDITION'", 'blank': 'True'}),
            'dateCreate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'DATE_CREATE'", 'blank': 'True'}),
            'dateModify': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'DATE_MODIFY'", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'ID_CORE_VIEW_MENU_CONDITION'"}),
            'isDeleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'IS_DELETED'"}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '10', 'db_column': "'ORDER'"}),
            'userCreateId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_CREATE_ID'", 'blank': 'True'}),
            'userModifyId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_MODIFY_ID'", 'blank': 'True'}),
            'value': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_column': "'VALUE'"}),
            'viewMenu': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['xpcore.ViewMenu']", 'db_column': "'ID_CORE_VIEW_MENU'"})
        },
        u'xpcore.viewmeta': {
            'Meta': {'object_name': 'ViewMeta', 'db_table': "'CORE_VIEW_META'"},
            'dateCreate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'DATE_CREATE'", 'blank': 'True'}),
            'dateModify': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'DATE_MODIFY'", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'ID_CORE_VIEW_META'"}),
            'isDeleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'IS_DELETED'"}),
            'meta': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['xpcore.MetaKey']", 'db_column': "'ID_META'"}),
            'userCreateId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_CREATE_ID'", 'blank': 'True'}),
            'userModifyId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_MODIFY_ID'", 'blank': 'True'}),
            'value': ('django.db.models.fields.TextField', [], {'db_column': "'VALUE'"}),
            'view': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['xpcore.View']", 'db_column': "'ID_VIEW'"})
        },
        u'xpcore.viewparamvalue': {
            'Meta': {'object_name': 'ViewParamValue', 'db_table': "'CORE_VIEW_PARAM_VALUE'"},
            'dateCreate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'DATE_CREATE'", 'blank': 'True'}),
            'dateModify': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'DATE_MODIFY'", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'ID_CORE_VIEW_PARAM_VALUE'"}),
            'isDeleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'IS_DELETED'"}),
            'name': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['xpcore.Param']", 'db_column': "'ID_NAME'"}),
            'operator': ('django.db.models.fields.CharField', [], {'max_length': '10', 'db_column': "'OPERATOR'"}),
            'userCreateId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_CREATE_ID'", 'blank': 'True'}),
            'userModifyId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_MODIFY_ID'", 'blank': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '20', 'db_column': "'VALUE'"}),
            'view': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'viewParam'", 'db_column': "'ID_VIEW'", 'to': u"orm['xpcore.View']"})
        },
        u'xpcore.viewtag': {
            'Meta': {'object_name': 'ViewTag', 'db_table': "'CORE_VIEW_TAG'"},
            'dateCreate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'DATE_CREATE'", 'blank': 'True'}),
            'dateModify': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'DATE_MODIFY'", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'ID_CORE_VIEW_TAG'"}),
            'isDeleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'IS_DELETED'"}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['xpsite.Tag']", 'db_column': "'ID_TAG'"}),
            'userCreateId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_CREATE_ID'", 'blank': 'True'}),
            'userModifyId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_MODIFY_ID'", 'blank': 'True'}),
            'view': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['xpcore.View']", 'db_column': "'ID_VIEW'"})
        },
        u'xpcore.viewtmpl': {
            'Meta': {'object_name': 'ViewTmpl', 'db_table': "'CORE_VIEW_TMPL'"},
            'dateCreate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'DATE_CREATE'", 'blank': 'True'}),
            'dateModify': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'DATE_MODIFY'", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'ID_CORE_VIEW_TMPL'"}),
            'isDeleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'IS_DELETED'"}),
            'template': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['xpcore.XpTemplate']", 'db_column': "'ID_TEMPLATE'"}),
            'userCreateId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_CREATE_ID'", 'blank': 'True'}),
            'userModifyId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_MODIFY_ID'", 'blank': 'True'}),
            'view': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['xpcore.View']", 'db_column': "'ID_VIEW'"})
        },
        u'xpcore.wfparamvalue': {
            'Meta': {'object_name': 'WFParamValue', 'db_table': "'CORE_WORKFLOW_PARAM_VALUE'"},
            'dateCreate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'DATE_CREATE'", 'blank': 'True'}),
            'dateModify': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'DATE_MODIFY'", 'blank': 'True'}),
            'flowView': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'flowViewParamValue'", 'db_column': "'ID_FLOW_VIEW'", 'to': u"orm['xpcore.WorkflowView']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'ID_CORE_WORKFLOW_PARAM_VALUE'"}),
            'isDeleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'IS_DELETED'"}),
            'name': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['xpcore.Param']", 'db_column': "'ID_NAME'"}),
            'operator': ('django.db.models.fields.CharField', [], {'max_length': '10', 'db_column': "'OPERATOR'"}),
            'userCreateId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_CREATE_ID'", 'blank': 'True'}),
            'userModifyId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_MODIFY_ID'", 'blank': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '20', 'db_column': "'VALUE'"})
        },
        u'xpcore.word': {
            'Meta': {'object_name': 'Word', 'db_table': "'CORE_WORD'"},
            'dateCreate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'DATE_CREATE'", 'blank': 'True'}),
            'dateModify': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'DATE_MODIFY'", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'ID_CORE_WORD'"}),
            'isDeleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'IS_DELETED'"}),
            'userCreateId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_CREATE_ID'", 'blank': 'True'}),
            'userModifyId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_MODIFY_ID'", 'blank': 'True'}),
            'word': ('django.db.models.fields.CharField', [], {'max_length': '20', 'db_column': "'WORD'", 'db_index': 'True'})
        },
        u'xpcore.workflow': {
            'Meta': {'object_name': 'Workflow', 'db_table': "'CORE_WORKFLOW'"},
            'application': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['xpcore.Application']", 'db_column': "'ID_APPLICATION'"}),
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '15', 'db_column': "'CODE'", 'db_index': 'True'}),
            'dateCreate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'DATE_CREATE'", 'blank': 'True'}),
            'dateModify': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'DATE_MODIFY'", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'ID_CORE_WORKFLOW'"}),
            'isDeleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'IS_DELETED'"}),
            'meta': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'wf_meta'", 'symmetrical': 'False', 'through': u"orm['xpcore.WorkflowMeta']", 'to': u"orm['xpcore.MetaKey']"}),
            'userCreateId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_CREATE_ID'", 'blank': 'True'}),
            'userModifyId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_MODIFY_ID'", 'blank': 'True'})
        },
        u'xpcore.workflowdata': {
            'Meta': {'unique_together': "(('userId', 'flow'),)", 'object_name': 'WorkflowData', 'db_table': "'CORE_WORKFLOW_DATA'"},
            'data': ('django.db.models.fields.TextField', [], {'default': "'eyJkYXRhIjoge30sICJ2aWV3TmFtZSI6ICIifQ==\\n'", 'db_column': "'DATA'"}),
            'dateCreate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'DATE_CREATE'", 'blank': 'True'}),
            'dateModify': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'DATE_MODIFY'", 'blank': 'True'}),
            'flow': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'flowData'", 'db_column': "'ID_FLOW'", 'to': u"orm['xpcore.Workflow']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'ID_CORE_WORKFLOW_DATA'"}),
            'isDeleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'IS_DELETED'"}),
            'userCreateId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_CREATE_ID'", 'blank': 'True'}),
            'userId': ('django.db.models.fields.CharField', [], {'max_length': '40', 'db_column': "'USER_ID'"}),
            'userModifyId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_MODIFY_ID'", 'blank': 'True'}),
            'view': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'viewFlowData'", 'db_column': "'ID_VIEW'", 'to': u"orm['xpcore.View']"})
        },
        u'xpcore.workflowmeta': {
            'Meta': {'object_name': 'WorkflowMeta', 'db_table': "'CORE_WORKFLOW_META'"},
            'dateCreate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'DATE_CREATE'", 'blank': 'True'}),
            'dateModify': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'DATE_MODIFY'", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'ID_CORE_VIEW_META'"}),
            'isDeleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'IS_DELETED'"}),
            'meta': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['xpcore.MetaKey']", 'db_column': "'ID_META'"}),
            'userCreateId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_CREATE_ID'", 'blank': 'True'}),
            'userModifyId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_MODIFY_ID'", 'blank': 'True'}),
            'value': ('django.db.models.fields.TextField', [], {'db_column': "'VALUE'"}),
            'workflow': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['xpcore.Workflow']", 'db_column': "'ID_WORKFLOW'"})
        },
        u'xpcore.workflowview': {
            'Meta': {'object_name': 'WorkflowView', 'db_table': "'CORE_WORKFLOW_VIEW'"},
            'action': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'wf_action'", 'null': 'True', 'db_column': "'ID_ACTION'", 'to': u"orm['xpcore.Action']"}),
            'dateCreate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'DATE_CREATE'", 'blank': 'True'}),
            'dateModify': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'DATE_MODIFY'", 'blank': 'True'}),
            'flow': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'flowView'", 'db_column': "'ID_FLOW'", 'to': u"orm['xpcore.Workflow']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'ID_CORE_WORKFLOW_VIEW'"}),
            'isDeleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'IS_DELETED'"}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '10', 'db_column': "'ORDER'"}),
            'params': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'flowView_params'", 'to': u"orm['xpcore.Param']", 'through': u"orm['xpcore.WFParamValue']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'userCreateId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_CREATE_ID'", 'blank': 'True'}),
            'userModifyId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_MODIFY_ID'", 'blank': 'True'}),
            'viewSource': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'flowViewSource'", 'null': 'True', 'db_column': "'ID_VIEW_SOURCE'", 'to': u"orm['xpcore.View']"}),
            'viewTarget': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'flowViewTarget'", 'db_column': "'ID_VIEW_TARGET'", 'to': u"orm['xpcore.View']"})
        },
        u'xpcore.xptemplate': {
            'Meta': {'unique_together': "(('application', 'name'),)", 'object_name': 'XpTemplate', 'db_table': "'CORE_TEMPLATE'"},
            'alias': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_column': "'ALIAS'"}),
            'application': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['xpcore.Application']", 'db_column': "'ID_APPLICATION'"}),
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
        u'xpsite.category': {
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
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'category_parent'", 'null': 'True', 'db_column': "'ID_PARENT'", 'to': u"orm['xpsite.Category']"}),
            'popularity': ('django.db.models.fields.IntegerField', [], {'default': '1', 'null': 'True', 'db_column': "'POPULARITY'", 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '200', 'db_column': "'SLUG'"}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['xpsite.Param']", 'db_column': "'ID_SITE_PARAMETER'"}),
            'userCreateId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_CREATE_ID'", 'blank': 'True'}),
            'userModifyId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_MODIFY_ID'", 'blank': 'True'})
        },
        u'xpsite.group': {
            'Meta': {'object_name': 'Group', 'db_table': "'SITE_GROUP'"},
            'accessGroups': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'group_access'", 'symmetrical': 'False', 'through': u"orm['xpsite.GroupAccess']", 'to': u"orm['xpsite.Group']"}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['xpsite.Category']", 'db_column': "'ID_CATEGORY'"}),
            'dateCreate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'DATE_CREATE'", 'blank': 'True'}),
            'dateModify': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'DATE_MODIFY'", 'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.Group']", 'unique': 'True', 'db_column': "'ID_GROUP_SYS'"}),
            'groupNameId': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'db_column': "'GROUP_NAME_ID'", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'ID_SITE_GROUP'"}),
            'isDeleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'IS_DELETED'"}),
            'isPublic': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_column': "'IS_PUBLIC'"}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'groupchannel_parent'", 'null': 'True', 'db_column': "'ID_PARENT'", 'to': u"orm['xpsite.Group']"}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'groupchannel_tags'", 'to': u"orm['xpsite.Tag']", 'through': u"orm['xpsite.GroupTag']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'userCreateId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_CREATE_ID'", 'blank': 'True'}),
            'userModifyId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_MODIFY_ID'", 'blank': 'True'})
        },
        u'xpsite.groupaccess': {
            'Meta': {'object_name': 'GroupAccess', 'db_table': "'SITE_GROUP_ACCESS'"},
            'dateCreate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'DATE_CREATE'", 'blank': 'True'}),
            'dateModify': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'DATE_MODIFY'", 'blank': 'True'}),
            'groupFrom': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'groupaccess_from'", 'db_column': "'ID_GROUP_FROM'", 'to': u"orm['xpsite.Group']"}),
            'groupTo': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'groupaccess_to'", 'db_column': "'ID_GROUP_TO'", 'to': u"orm['xpsite.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'ID_SITE_GROUP_ACCESS'"}),
            'isDeleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'IS_DELETED'"}),
            'userCreateId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_CREATE_ID'", 'blank': 'True'}),
            'userModifyId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_MODIFY_ID'", 'blank': 'True'})
        },
        u'xpsite.grouptag': {
            'Meta': {'object_name': 'GroupTag', 'db_table': "'SITE_GROUP_TAG'"},
            'dateCreate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'DATE_CREATE'", 'blank': 'True'}),
            'dateModify': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'DATE_MODIFY'", 'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['xpsite.Group']", 'db_column': "'ID_GROUP'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'ID_SITE_GROUP_TAG'"}),
            'isDeleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'IS_DELETED'"}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['xpsite.Tag']", 'db_column': "'ID_TAG'"}),
            'userCreateId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_CREATE_ID'", 'blank': 'True'}),
            'userModifyId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_MODIFY_ID'", 'blank': 'True'})
        },
        u'xpsite.param': {
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
        u'xpsite.tag': {
            'Meta': {'ordering': "['-popularity']", 'object_name': 'Tag', 'db_table': "'SITE_TAG'"},
            'dateCreate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'DATE_CREATE'", 'blank': 'True'}),
            'dateModify': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'DATE_MODIFY'", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'ID_SITE_TAG'"}),
            'isDeleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'IS_DELETED'"}),
            'isPublic': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_column': "'IS_PUBLIC'"}),
            'mode': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tag_mode'", 'db_column': "'ID_MODE'", 'to': u"orm['xpsite.TagMode']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'db_column': "'NAME'"}),
            'popularity': ('django.db.models.fields.IntegerField', [], {'default': '1', 'null': 'True', 'db_column': "'POPULARITY'", 'blank': 'True'}),
            'userCreateId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_CREATE_ID'", 'blank': 'True'}),
            'userModifyId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_MODIFY_ID'", 'blank': 'True'})
        },
        u'xpsite.tagmode': {
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

    complete_apps = ['xpcore']