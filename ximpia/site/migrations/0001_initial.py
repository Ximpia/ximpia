# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Param'
        db.create_table('SITE_PARAMETER', (
            ('dateCreate', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_column='DATE_CREATE', blank=True)),
            ('dateModify', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, db_column='DATE_MODIFY', blank=True)),
            ('userCreateId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_CREATE_ID', blank=True)),
            ('userModifyId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_MODIFY_ID', blank=True)),
            ('isDeleted', self.gf('django.db.models.fields.BooleanField')(default=False, db_column='IS_DELETED')),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column='ID_SITE_PARAMETER')),
            ('mode', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, db_column='MODE', blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20, db_column='NAME')),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, db_column='VALUE', blank=True)),
            ('paramType', self.gf('django.db.models.fields.CharField')(default='string', max_length=10, db_column='PARAM_TYPE')),
        ))
        db.send_create_signal(u'site', ['Param'])

        # Adding model 'MetaKey'
        db.create_table('SITE_META_KEY', (
            ('dateCreate', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_column='DATE_CREATE', blank=True)),
            ('dateModify', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, db_column='DATE_MODIFY', blank=True)),
            ('userCreateId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_CREATE_ID', blank=True)),
            ('userModifyId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_MODIFY_ID', blank=True)),
            ('isDeleted', self.gf('django.db.models.fields.BooleanField')(default=False, db_column='IS_DELETED')),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column='ID_SITE_META_KEY')),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, db_column='NAME')),
            ('keyType', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['site.Param'], db_column='ID_SITE_PARAMETER')),
        ))
        db.send_create_signal(u'site', ['MetaKey'])

        # Adding model 'TagMode'
        db.create_table('SITE_TAG_MODE', (
            ('dateCreate', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_column='DATE_CREATE', blank=True)),
            ('dateModify', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, db_column='DATE_MODIFY', blank=True)),
            ('userCreateId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_CREATE_ID', blank=True)),
            ('userModifyId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_MODIFY_ID', blank=True)),
            ('isDeleted', self.gf('django.db.models.fields.BooleanField')(default=False, db_column='IS_DELETED')),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column='ID_SITE_TAG_MODE')),
            ('mode', self.gf('django.db.models.fields.CharField')(max_length=30, db_column='MODE')),
            ('isPublic', self.gf('django.db.models.fields.BooleanField')(default=True, db_column='IS_PUBLIC')),
        ))
        db.send_create_signal(u'site', ['TagMode'])

        # Adding model 'Tag'
        db.create_table('SITE_TAG', (
            ('dateCreate', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_column='DATE_CREATE', blank=True)),
            ('dateModify', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, db_column='DATE_MODIFY', blank=True)),
            ('userCreateId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_CREATE_ID', blank=True)),
            ('userModifyId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_MODIFY_ID', blank=True)),
            ('isDeleted', self.gf('django.db.models.fields.BooleanField')(default=False, db_column='IS_DELETED')),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column='ID_SITE_TAG')),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30, db_column='NAME')),
            ('mode', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tag_mode', db_column='ID_MODE', to=orm['site.TagMode'])),
            ('popularity', self.gf('django.db.models.fields.IntegerField')(default=1, null=True, db_column='POPULARITY', blank=True)),
            ('isPublic', self.gf('django.db.models.fields.BooleanField')(default=True, db_column='IS_PUBLIC')),
        ))
        db.send_create_signal(u'site', ['Tag'])

        # Adding model 'Address'
        db.create_table('SITE_ADDRESS', (
            ('dateCreate', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_column='DATE_CREATE', blank=True)),
            ('dateModify', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, db_column='DATE_MODIFY', blank=True)),
            ('userCreateId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_CREATE_ID', blank=True)),
            ('userModifyId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_MODIFY_ID', blank=True)),
            ('isDeleted', self.gf('django.db.models.fields.BooleanField')(default=False, db_column='IS_DELETED')),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column='ID_SITE_ADDRESS')),
            ('street', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, db_column='STREET', blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=20, db_column='CITY')),
            ('region', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, db_column='REGION', blank=True)),
            ('zipCode', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, db_column='ZIP_CODE', blank=True)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=2, db_column='COUNTRY')),
            ('long', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=18, decimal_places=12, blank=True)),
            ('lat', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=18, decimal_places=12, blank=True)),
        ))
        db.send_create_signal(u'site', ['Address'])

        # Adding model 'UserChannel'
        db.create_table('SITE_USER', (
            ('dateCreate', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_column='DATE_CREATE', blank=True)),
            ('dateModify', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, db_column='DATE_MODIFY', blank=True)),
            ('userCreateId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_CREATE_ID', blank=True)),
            ('userModifyId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_MODIFY_ID', blank=True)),
            ('isDeleted', self.gf('django.db.models.fields.BooleanField')(default=False, db_column='IS_DELETED')),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column='ID_SITE_USER')),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], db_column='ID_USER')),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=20, db_column='TITLE')),
            ('name', self.gf('django.db.models.fields.CharField')(default='user', max_length=20, db_column='NAME')),
            ('tag', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['site.Tag'], null=True, db_column='ID_TAG', blank=True)),
        ))
        db.send_create_signal(u'site', ['UserChannel'])

        # Adding unique constraint on 'UserChannel', fields ['user', 'name']
        db.create_unique('SITE_USER', ['ID_USER', 'NAME'])

        # Adding model 'Category'
        db.create_table('SITE_CATEGORY', (
            ('dateCreate', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_column='DATE_CREATE', blank=True)),
            ('dateModify', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, db_column='DATE_MODIFY', blank=True)),
            ('userCreateId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_CREATE_ID', blank=True)),
            ('userModifyId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_MODIFY_ID', blank=True)),
            ('isDeleted', self.gf('django.db.models.fields.BooleanField')(default=False, db_column='IS_DELETED')),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column='ID_SITE_CATEGORY')),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=55, db_column='NAME')),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=200, db_column='SLUG')),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='DESCRIPTION', blank=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='category_parent', null=True, db_column='ID_PARENT', to=orm['site.Category'])),
            ('image', self.gf('filebrowser.fields.FileBrowseField')(max_length=200, null=True, db_column='IMAGE', blank=True)),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['site.Param'], db_column='ID_SITE_PARAMETER')),
            ('isPublished', self.gf('django.db.models.fields.BooleanField')(default=False, db_column='IS_PUBLISHED')),
            ('isPublic', self.gf('django.db.models.fields.BooleanField')(default=True, db_column='IS_PUBLIC')),
            ('popularity', self.gf('django.db.models.fields.IntegerField')(default=1, null=True, db_column='POPULARITY', blank=True)),
            ('menuOrder', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1, db_column='MENU_ORDER')),
        ))
        db.send_create_signal(u'site', ['Category'])

        # Adding model 'SocialNetworkUser'
        db.create_table('SITE_SOCIAL_NETWORK_USER', (
            ('dateCreate', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_column='DATE_CREATE', blank=True)),
            ('dateModify', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, db_column='DATE_MODIFY', blank=True)),
            ('userCreateId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_CREATE_ID', blank=True)),
            ('userModifyId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_MODIFY_ID', blank=True)),
            ('isDeleted', self.gf('django.db.models.fields.BooleanField')(default=False, db_column='IS_DELETED')),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column='ID_SITE_SOCIAL_NETWORK_USER')),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], db_column='ID_USER')),
            ('socialNetwork', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.CoreParam'], db_column='ID_CORE_PARAMETER')),
            ('socialId', self.gf('django.db.models.fields.BigIntegerField')(db_column='SOCIAL_ID')),
            ('token', self.gf('django.db.models.fields.CharField')(max_length=255, db_column='TOKEN')),
            ('tokenSecret', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='TOKEN_SECRET', blank=True)),
        ))
        db.send_create_signal(u'site', ['SocialNetworkUser'])

        # Adding unique constraint on 'SocialNetworkUser', fields ['user', 'socialNetwork']
        db.create_unique('SITE_SOCIAL_NETWORK_USER', ['ID_USER', 'ID_CORE_PARAMETER'])

        # Adding model 'Setting'
        db.create_table('SITE_SETTING', (
            ('dateCreate', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_column='DATE_CREATE', blank=True)),
            ('dateModify', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, db_column='DATE_MODIFY', blank=True)),
            ('userCreateId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_CREATE_ID', blank=True)),
            ('userModifyId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_MODIFY_ID', blank=True)),
            ('isDeleted', self.gf('django.db.models.fields.BooleanField')(default=False, db_column='IS_DELETED')),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column='ID_SITE_SETTING')),
            ('application', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='site_setting_app', null=True, db_column='ID_CORE_APPLICATION', to=orm['core.Application'])),
            ('name', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['site.MetaKey'], db_column='ID_META')),
            ('value', self.gf('django.db.models.fields.TextField')(db_column='VALUE')),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255, db_column='DESCRIPTION')),
            ('mustAutoload', self.gf('django.db.models.fields.BooleanField')(default=False, db_column='MUST_AUTOLOAD')),
        ))
        db.send_create_signal(u'site', ['Setting'])

        # Adding model 'UserMeta'
        db.create_table('SITE_USER_META', (
            ('dateCreate', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_column='DATE_CREATE', blank=True)),
            ('dateModify', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, db_column='DATE_MODIFY', blank=True)),
            ('userCreateId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_CREATE_ID', blank=True)),
            ('userModifyId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_MODIFY_ID', blank=True)),
            ('isDeleted', self.gf('django.db.models.fields.BooleanField')(default=False, db_column='IS_DELETED')),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column='ID_SITE_USER_PROFILE')),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], db_column='ID_USER')),
            ('meta', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['site.MetaKey'], db_column='ID_META')),
            ('value', self.gf('django.db.models.fields.TextField')(db_column='VALUE')),
        ))
        db.send_create_signal(u'site', ['UserMeta'])

        # Adding model 'UserProfile'
        db.create_table('SITE_USER_PROFILE', (
            ('dateCreate', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_column='DATE_CREATE', blank=True)),
            ('dateModify', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, db_column='DATE_MODIFY', blank=True)),
            ('userCreateId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_CREATE_ID', blank=True)),
            ('userModifyId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_MODIFY_ID', blank=True)),
            ('isDeleted', self.gf('django.db.models.fields.BooleanField')(default=False, db_column='IS_DELETED')),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column='ID_SITE_USER_PROFILE')),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], db_column='ID_USER')),
            ('image', self.gf('filebrowser.fields.FileBrowseField')(max_length=200, null=True, db_column='IMAGE', blank=True)),
            ('status', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['site.Param'], db_column='ID_SITE_PARAMETER')),
        ))
        db.send_create_signal(u'site', ['UserProfile'])

        # Adding model 'UserAddress'
        db.create_table('SITE_USER_ADDRESS', (
            ('dateCreate', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_column='DATE_CREATE', blank=True)),
            ('dateModify', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, db_column='DATE_MODIFY', blank=True)),
            ('userCreateId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_CREATE_ID', blank=True)),
            ('userModifyId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_MODIFY_ID', blank=True)),
            ('isDeleted', self.gf('django.db.models.fields.BooleanField')(default=False, db_column='IS_DELETED')),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column='ID_SITE_USER_ADDRESS')),
            ('userProfile', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['site.UserProfile'], db_column='ID_SITE_USER_PROFILE')),
            ('address', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['site.Address'], db_column='ID_ADDRESS')),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['site.Param'], db_column='ID_SITE_PARAMETER')),
        ))
        db.send_create_signal(u'site', ['UserAddress'])

        # Adding model 'Group'
        db.create_table('SITE_GROUP', (
            ('dateCreate', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_column='DATE_CREATE', blank=True)),
            ('dateModify', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, db_column='DATE_MODIFY', blank=True)),
            ('userCreateId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_CREATE_ID', blank=True)),
            ('userModifyId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_MODIFY_ID', blank=True)),
            ('isDeleted', self.gf('django.db.models.fields.BooleanField')(default=False, db_column='IS_DELETED')),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column='ID_SITE_GROUP')),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.Group'], unique=True, db_column='ID_GROUP_SYS')),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='groupchannel_parent', null=True, db_column='ID_PARENT', to=orm['site.Group'])),
            ('groupNameId', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, db_column='GROUP_NAME_ID', blank=True)),
            ('isPublic', self.gf('django.db.models.fields.BooleanField')(default=True, db_column='IS_PUBLIC')),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['site.Category'], db_column='ID_CATEGORY')),
        ))
        db.send_create_signal(u'site', ['Group'])

        # Adding model 'GroupAccess'
        db.create_table('SITE_GROUP_ACCESS', (
            ('dateCreate', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_column='DATE_CREATE', blank=True)),
            ('dateModify', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, db_column='DATE_MODIFY', blank=True)),
            ('userCreateId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_CREATE_ID', blank=True)),
            ('userModifyId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_MODIFY_ID', blank=True)),
            ('isDeleted', self.gf('django.db.models.fields.BooleanField')(default=False, db_column='IS_DELETED')),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column='ID_SITE_GROUP_ACCESS')),
            ('groupFrom', self.gf('django.db.models.fields.related.ForeignKey')(related_name='groupaccess_from', db_column='ID_GROUP_FROM', to=orm['site.Group'])),
            ('groupTo', self.gf('django.db.models.fields.related.ForeignKey')(related_name='groupaccess_to', db_column='ID_GROUP_TO', to=orm['site.Group'])),
        ))
        db.send_create_signal(u'site', ['GroupAccess'])

        # Adding model 'UserChannelGroup'
        db.create_table('SITE_USER_GROUP', (
            ('dateCreate', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_column='DATE_CREATE', blank=True)),
            ('dateModify', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, db_column='DATE_MODIFY', blank=True)),
            ('userCreateId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_CREATE_ID', blank=True)),
            ('userModifyId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_MODIFY_ID', blank=True)),
            ('isDeleted', self.gf('django.db.models.fields.BooleanField')(default=False, db_column='IS_DELETED')),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column='ID_SITE_USER_GROUP')),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['site.Group'], db_column='ID_GROUP')),
            ('userChannel', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['site.UserChannel'], db_column='ID_USER_CHANNEL')),
        ))
        db.send_create_signal(u'site', ['UserChannelGroup'])

        # Adding model 'GroupTag'
        db.create_table('SITE_GROUP_TAG', (
            ('dateCreate', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_column='DATE_CREATE', blank=True)),
            ('dateModify', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, db_column='DATE_MODIFY', blank=True)),
            ('userCreateId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_CREATE_ID', blank=True)),
            ('userModifyId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_MODIFY_ID', blank=True)),
            ('isDeleted', self.gf('django.db.models.fields.BooleanField')(default=False, db_column='IS_DELETED')),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column='ID_SITE_GROUP_TAG')),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['site.Group'], db_column='ID_GROUP')),
            ('tag', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['site.Tag'], db_column='ID_TAG')),
        ))
        db.send_create_signal(u'site', ['GroupTag'])

        # Adding model 'SignupData'
        db.create_table('SITE_SIGNUP_DATA', (
            ('dateCreate', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_column='DATE_CREATE', blank=True)),
            ('dateModify', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, db_column='DATE_MODIFY', blank=True)),
            ('userCreateId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_CREATE_ID', blank=True)),
            ('userModifyId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_MODIFY_ID', blank=True)),
            ('isDeleted', self.gf('django.db.models.fields.BooleanField')(default=False, db_column='IS_DELETED')),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column='ID_SITE_SIGNUP_DATA')),
            ('user', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30, db_column='USER')),
            ('activationCode', self.gf('django.db.models.fields.PositiveSmallIntegerField')(db_column='ACTIVATION_CODE')),
            ('data', self.gf('django.db.models.fields.TextField')(db_column='DATA')),
        ))
        db.send_create_signal(u'site', ['SignupData'])

        # Adding model 'Invitation'
        db.create_table('SITE_INVITATION', (
            ('dateCreate', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_column='DATE_CREATE', blank=True)),
            ('dateModify', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, db_column='DATE_MODIFY', blank=True)),
            ('userCreateId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_CREATE_ID', blank=True)),
            ('userModifyId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_MODIFY_ID', blank=True)),
            ('isDeleted', self.gf('django.db.models.fields.BooleanField')(default=False, db_column='IS_DELETED')),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column='ID_SITE_INVITATION')),
            ('fromUser', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], db_column='ID_USER')),
            ('invitationCode', self.gf('django.db.models.fields.CharField')(unique=True, max_length=10, db_column='INVITATION_CODE')),
            ('email', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=75, db_column='EMAIL')),
            ('status', self.gf('django.db.models.fields.CharField')(default='pending', max_length=10, db_column='STATUS')),
            ('number', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1, db_column='NUMBER')),
            ('message', self.gf('django.db.models.fields.TextField')(null=True, db_column='MESSAGE', blank=True)),
        ))
        db.send_create_signal(u'site', ['Invitation'])

        # Adding model 'InvitationMeta'
        db.create_table('SITE_INVITATION_META', (
            ('dateCreate', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_column='DATE_CREATE', blank=True)),
            ('dateModify', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, db_column='DATE_MODIFY', blank=True)),
            ('userCreateId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_CREATE_ID', blank=True)),
            ('userModifyId', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='USER_MODIFY_ID', blank=True)),
            ('isDeleted', self.gf('django.db.models.fields.BooleanField')(default=False, db_column='IS_DELETED')),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column='ID_SITE_USER_PROFILE')),
            ('invitation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['site.Invitation'], db_column='ID_INVITATION')),
            ('meta', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['site.MetaKey'], db_column='ID_META')),
            ('value', self.gf('django.db.models.fields.TextField')(db_column='VALUE')),
        ))
        db.send_create_signal(u'site', ['InvitationMeta'])


    def backwards(self, orm):
        # Removing unique constraint on 'SocialNetworkUser', fields ['user', 'socialNetwork']
        db.delete_unique('SITE_SOCIAL_NETWORK_USER', ['ID_USER', 'ID_CORE_PARAMETER'])

        # Removing unique constraint on 'UserChannel', fields ['user', 'name']
        db.delete_unique('SITE_USER', ['ID_USER', 'NAME'])

        # Deleting model 'Param'
        db.delete_table('SITE_PARAMETER')

        # Deleting model 'MetaKey'
        db.delete_table('SITE_META_KEY')

        # Deleting model 'TagMode'
        db.delete_table('SITE_TAG_MODE')

        # Deleting model 'Tag'
        db.delete_table('SITE_TAG')

        # Deleting model 'Address'
        db.delete_table('SITE_ADDRESS')

        # Deleting model 'UserChannel'
        db.delete_table('SITE_USER')

        # Deleting model 'Category'
        db.delete_table('SITE_CATEGORY')

        # Deleting model 'SocialNetworkUser'
        db.delete_table('SITE_SOCIAL_NETWORK_USER')

        # Deleting model 'Setting'
        db.delete_table('SITE_SETTING')

        # Deleting model 'UserMeta'
        db.delete_table('SITE_USER_META')

        # Deleting model 'UserProfile'
        db.delete_table('SITE_USER_PROFILE')

        # Deleting model 'UserAddress'
        db.delete_table('SITE_USER_ADDRESS')

        # Deleting model 'Group'
        db.delete_table('SITE_GROUP')

        # Deleting model 'GroupAccess'
        db.delete_table('SITE_GROUP_ACCESS')

        # Deleting model 'UserChannelGroup'
        db.delete_table('SITE_USER_GROUP')

        # Deleting model 'GroupTag'
        db.delete_table('SITE_GROUP_TAG')

        # Deleting model 'SignupData'
        db.delete_table('SITE_SIGNUP_DATA')

        # Deleting model 'Invitation'
        db.delete_table('SITE_INVITATION')

        # Deleting model 'InvitationMeta'
        db.delete_table('SITE_INVITATION_META')


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
        u'site.address': {
            'Meta': {'object_name': 'Address', 'db_table': "'SITE_ADDRESS'"},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '20', 'db_column': "'CITY'"}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '2', 'db_column': "'COUNTRY'"}),
            'dateCreate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'DATE_CREATE'", 'blank': 'True'}),
            'dateModify': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'DATE_MODIFY'", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'ID_SITE_ADDRESS'"}),
            'isDeleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'IS_DELETED'"}),
            'lat': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '18', 'decimal_places': '12', 'blank': 'True'}),
            'long': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '18', 'decimal_places': '12', 'blank': 'True'}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'db_column': "'REGION'", 'blank': 'True'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'db_column': "'STREET'", 'blank': 'True'}),
            'userCreateId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_CREATE_ID'", 'blank': 'True'}),
            'userModifyId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_MODIFY_ID'", 'blank': 'True'}),
            'zipCode': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'db_column': "'ZIP_CODE'", 'blank': 'True'})
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
        u'site.invitation': {
            'Meta': {'object_name': 'Invitation', 'db_table': "'SITE_INVITATION'"},
            'dateCreate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'DATE_CREATE'", 'blank': 'True'}),
            'dateModify': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'DATE_MODIFY'", 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75', 'db_column': "'EMAIL'"}),
            'fromUser': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'db_column': "'ID_USER'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'ID_SITE_INVITATION'"}),
            'invitationCode': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10', 'db_column': "'INVITATION_CODE'"}),
            'isDeleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'IS_DELETED'"}),
            'message': ('django.db.models.fields.TextField', [], {'null': 'True', 'db_column': "'MESSAGE'", 'blank': 'True'}),
            'meta': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'invitation_meta'", 'symmetrical': 'False', 'through': u"orm['site.InvitationMeta']", 'to': u"orm['site.MetaKey']"}),
            'number': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1', 'db_column': "'NUMBER'"}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'pending'", 'max_length': '10', 'db_column': "'STATUS'"}),
            'userCreateId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_CREATE_ID'", 'blank': 'True'}),
            'userModifyId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_MODIFY_ID'", 'blank': 'True'})
        },
        u'site.invitationmeta': {
            'Meta': {'object_name': 'InvitationMeta', 'db_table': "'SITE_INVITATION_META'"},
            'dateCreate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'DATE_CREATE'", 'blank': 'True'}),
            'dateModify': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'DATE_MODIFY'", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'ID_SITE_USER_PROFILE'"}),
            'invitation': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['site.Invitation']", 'db_column': "'ID_INVITATION'"}),
            'isDeleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'IS_DELETED'"}),
            'meta': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['site.MetaKey']", 'db_column': "'ID_META'"}),
            'userCreateId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_CREATE_ID'", 'blank': 'True'}),
            'userModifyId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_MODIFY_ID'", 'blank': 'True'}),
            'value': ('django.db.models.fields.TextField', [], {'db_column': "'VALUE'"})
        },
        u'site.metakey': {
            'Meta': {'ordering': "['name']", 'object_name': 'MetaKey', 'db_table': "'SITE_META_KEY'"},
            'dateCreate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'DATE_CREATE'", 'blank': 'True'}),
            'dateModify': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'DATE_MODIFY'", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'ID_SITE_META_KEY'"}),
            'isDeleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'IS_DELETED'"}),
            'keyType': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['site.Param']", 'db_column': "'ID_SITE_PARAMETER'"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'NAME'"}),
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
        u'site.setting': {
            'Meta': {'object_name': 'Setting', 'db_table': "'SITE_SETTING'"},
            'application': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'site_setting_app'", 'null': 'True', 'db_column': "'ID_CORE_APPLICATION'", 'to': u"orm['core.Application']"}),
            'dateCreate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'DATE_CREATE'", 'blank': 'True'}),
            'dateModify': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'DATE_MODIFY'", 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_column': "'DESCRIPTION'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'ID_SITE_SETTING'"}),
            'isDeleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'IS_DELETED'"}),
            'mustAutoload': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'MUST_AUTOLOAD'"}),
            'name': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['site.MetaKey']", 'db_column': "'ID_META'"}),
            'userCreateId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_CREATE_ID'", 'blank': 'True'}),
            'userModifyId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_MODIFY_ID'", 'blank': 'True'}),
            'value': ('django.db.models.fields.TextField', [], {'db_column': "'VALUE'"})
        },
        u'site.signupdata': {
            'Meta': {'object_name': 'SignupData', 'db_table': "'SITE_SIGNUP_DATA'"},
            'activationCode': ('django.db.models.fields.PositiveSmallIntegerField', [], {'db_column': "'ACTIVATION_CODE'"}),
            'data': ('django.db.models.fields.TextField', [], {'db_column': "'DATA'"}),
            'dateCreate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'DATE_CREATE'", 'blank': 'True'}),
            'dateModify': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'DATE_MODIFY'", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'ID_SITE_SIGNUP_DATA'"}),
            'isDeleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'IS_DELETED'"}),
            'user': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30', 'db_column': "'USER'"}),
            'userCreateId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_CREATE_ID'", 'blank': 'True'}),
            'userModifyId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_MODIFY_ID'", 'blank': 'True'})
        },
        u'site.socialnetworkuser': {
            'Meta': {'unique_together': "(('user', 'socialNetwork'),)", 'object_name': 'SocialNetworkUser', 'db_table': "'SITE_SOCIAL_NETWORK_USER'"},
            'dateCreate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'DATE_CREATE'", 'blank': 'True'}),
            'dateModify': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'DATE_MODIFY'", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'ID_SITE_SOCIAL_NETWORK_USER'"}),
            'isDeleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'IS_DELETED'"}),
            'socialId': ('django.db.models.fields.BigIntegerField', [], {'db_column': "'SOCIAL_ID'"}),
            'socialNetwork': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.CoreParam']", 'db_column': "'ID_CORE_PARAMETER'"}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_column': "'TOKEN'"}),
            'tokenSecret': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'TOKEN_SECRET'", 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'db_column': "'ID_USER'"}),
            'userCreateId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_CREATE_ID'", 'blank': 'True'}),
            'userModifyId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_MODIFY_ID'", 'blank': 'True'})
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
        },
        u'site.useraddress': {
            'Meta': {'object_name': 'UserAddress', 'db_table': "'SITE_USER_ADDRESS'"},
            'address': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['site.Address']", 'db_column': "'ID_ADDRESS'"}),
            'dateCreate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'DATE_CREATE'", 'blank': 'True'}),
            'dateModify': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'DATE_MODIFY'", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'ID_SITE_USER_ADDRESS'"}),
            'isDeleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'IS_DELETED'"}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['site.Param']", 'db_column': "'ID_SITE_PARAMETER'"}),
            'userCreateId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_CREATE_ID'", 'blank': 'True'}),
            'userModifyId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_MODIFY_ID'", 'blank': 'True'}),
            'userProfile': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['site.UserProfile']", 'db_column': "'ID_SITE_USER_PROFILE'"})
        },
        u'site.userchannel': {
            'Meta': {'unique_together': "(('user', 'name'),)", 'object_name': 'UserChannel', 'db_table': "'SITE_USER'"},
            'dateCreate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'DATE_CREATE'", 'blank': 'True'}),
            'dateModify': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'DATE_MODIFY'", 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_groups'", 'symmetrical': 'False', 'through': u"orm['site.UserChannelGroup']", 'to': u"orm['site.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'ID_SITE_USER'"}),
            'isDeleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'IS_DELETED'"}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'user'", 'max_length': '20', 'db_column': "'NAME'"}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['site.Tag']", 'null': 'True', 'db_column': "'ID_TAG'", 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '20', 'db_column': "'TITLE'"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'db_column': "'ID_USER'"}),
            'userCreateId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_CREATE_ID'", 'blank': 'True'}),
            'userModifyId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_MODIFY_ID'", 'blank': 'True'})
        },
        u'site.userchannelgroup': {
            'Meta': {'object_name': 'UserChannelGroup', 'db_table': "'SITE_USER_GROUP'"},
            'dateCreate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'DATE_CREATE'", 'blank': 'True'}),
            'dateModify': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'DATE_MODIFY'", 'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['site.Group']", 'db_column': "'ID_GROUP'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'ID_SITE_USER_GROUP'"}),
            'isDeleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'IS_DELETED'"}),
            'userChannel': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['site.UserChannel']", 'db_column': "'ID_USER_CHANNEL'"}),
            'userCreateId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_CREATE_ID'", 'blank': 'True'}),
            'userModifyId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_MODIFY_ID'", 'blank': 'True'})
        },
        u'site.usermeta': {
            'Meta': {'object_name': 'UserMeta', 'db_table': "'SITE_USER_META'"},
            'dateCreate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'DATE_CREATE'", 'blank': 'True'}),
            'dateModify': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'DATE_MODIFY'", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'ID_SITE_USER_PROFILE'"}),
            'isDeleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'IS_DELETED'"}),
            'meta': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['site.MetaKey']", 'db_column': "'ID_META'"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'db_column': "'ID_USER'"}),
            'userCreateId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_CREATE_ID'", 'blank': 'True'}),
            'userModifyId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_MODIFY_ID'", 'blank': 'True'}),
            'value': ('django.db.models.fields.TextField', [], {'db_column': "'VALUE'"})
        },
        u'site.userprofile': {
            'Meta': {'object_name': 'UserProfile', 'db_table': "'SITE_USER_PROFILE'"},
            'addresses': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'userprofile_addresses'", 'symmetrical': 'False', 'through': u"orm['site.UserAddress']", 'to': u"orm['site.Address']"}),
            'dateCreate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'DATE_CREATE'", 'blank': 'True'}),
            'dateModify': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'DATE_MODIFY'", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'ID_SITE_USER_PROFILE'"}),
            'image': ('filebrowser.fields.FileBrowseField', [], {'max_length': '200', 'null': 'True', 'db_column': "'IMAGE'", 'blank': 'True'}),
            'isDeleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'IS_DELETED'"}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['site.Param']", 'db_column': "'ID_SITE_PARAMETER'"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'db_column': "'ID_USER'"}),
            'userCreateId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_CREATE_ID'", 'blank': 'True'}),
            'userModifyId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'USER_MODIFY_ID'", 'blank': 'True'})
        }
    }

    complete_apps = ['site']