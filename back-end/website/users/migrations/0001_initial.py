# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UserProfile'
        db.create_table('users_userprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uuid', self.gf('django.db.models.fields.CharField')(default='5dc1f732-d659-5304-8898-193f6638de34', unique=True, max_length=36)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('middle_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('updated_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('created_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('last_login_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('about_me', self.gf('django.db.models.fields.CharField')(default='', max_length=1024)),
            ('location', self.gf('django.db.models.fields.CharField')(default='', max_length=2048)),
            ('fashion_statement', self.gf('django.db.models.fields.CharField')(default='', max_length=2048)),
            ('website', self.gf('django.db.models.fields.URLField')(default='', max_length=200)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=1, null=True)),
            ('birthday', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('height', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('weight', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=32, null=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('notification_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('statement', self.gf('django.db.models.fields.TextField')(default='')),
            ('last_notification', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(1970, 1, 1, 0, 0))),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, null=True)),
            ('total_collections', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('total_groups', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('total_friends', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('total_notifications', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('profile_image_thumbnail', self.gf('django.db.models.fields.related.OneToOneField')(related_name='profile_of_thumbnail', unique=True, null=True, to=orm['media.Image'])),
            ('profile_image_standard', self.gf('django.db.models.fields.related.OneToOneField')(related_name='profile_of_standard', unique=True, null=True, to=orm['media.Image'])),
        ))
        db.send_create_signal('users', ['UserProfile'])

        # Adding M2M table for field image_collection_set on 'UserProfile'
        db.create_table('users_userprofile_image_collection_set', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('userprofile', models.ForeignKey(orm['users.userprofile'], null=False)),
            ('image', models.ForeignKey(orm['media.image'], null=False))
        ))
        db.create_unique('users_userprofile_image_collection_set', ['userprofile_id', 'image_id'])

        # Adding M2M table for field wordbox_collection_set on 'UserProfile'
        db.create_table('users_userprofile_wordbox_collection_set', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('userprofile', models.ForeignKey(orm['users.userprofile'], null=False)),
            ('wordbox', models.ForeignKey(orm['media.wordbox'], null=False))
        ))
        db.create_unique('users_userprofile_wordbox_collection_set', ['userprofile_id', 'wordbox_id'])

        # Adding model 'Notification'
        db.create_table('users_notification', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uuid', self.gf('django.db.models.fields.CharField')(default='ee4669e8-7e04-5256-96a5-fb86f8768f76', unique=True, max_length=36)),
            ('from_user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='to_notifications', to=orm['users.UserProfile'])),
            ('to_user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='from_notifications', to=orm['users.UserProfile'])),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('was_read', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('IPaddress', self.gf('django.db.models.fields.GenericIPAddressField')(max_length=39)),
            ('created_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('updated_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('users', ['Notification'])

        # Adding model 'UserSubscription'
        db.create_table('users_usersubscription', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uuid', self.gf('django.db.models.fields.CharField')(default='977a3199-2cc1-558a-9916-4279cd9c9441', unique=True, max_length=36)),
            ('from_user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='to_usersubscriptions', to=orm['users.UserProfile'])),
            ('to_user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='from_usersubscriptions', to=orm['users.UserProfile'])),
            ('created_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('updated_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('IPaddress', self.gf('django.db.models.fields.GenericIPAddressField')(max_length=39)),
            ('status', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('users', ['UserSubscription'])

        # Adding model 'Friendship'
        db.create_table('users_friendship', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uuid', self.gf('django.db.models.fields.CharField')(default='b2b68643-92ca-5b07-a5dc-778ea918f46f', unique=True, max_length=36)),
            ('from_user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='to_friendships', to=orm['users.UserProfile'])),
            ('to_user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='from_friendships', to=orm['users.UserProfile'])),
            ('updated_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('created_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('IPaddress', self.gf('django.db.models.fields.GenericIPAddressField')(max_length=39)),
            ('status', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('was_accepted', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('users', ['Friendship'])

        # Adding model 'Community'
        db.create_table('users_community', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uuid', self.gf('django.db.models.fields.CharField')(default='8a9157b2-71d1-56f4-acef-0480d393ae70', unique=True, max_length=36)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('description', self.gf('django.db.models.fields.TextField')(default='')),
            ('updated_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('created_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('IPaddress', self.gf('django.db.models.fields.GenericIPAddressField')(max_length=39)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_public', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(related_name='created_community_set', to=orm['users.UserProfile'])),
            ('total_subscribers', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('total_admins', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('total_collections', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('profile_image_thumbnail', self.gf('django.db.models.fields.related.OneToOneField')(related_name='community_of_thumbnail', unique=True, null=True, to=orm['media.Image'])),
            ('profile_image_standard', self.gf('django.db.models.fields.related.OneToOneField')(related_name='community_of_standard', unique=True, null=True, to=orm['media.Image'])),
        ))
        db.send_create_signal('users', ['Community'])

        # Adding model 'CommunityCategory'
        db.create_table('users_communitycategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uuid', self.gf('django.db.models.fields.CharField')(default='29ed8d9b-2c8b-52ba-88cf-14ca40cf441c', unique=True, max_length=36)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('description', self.gf('django.db.models.fields.TextField')(default='')),
            ('updated_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('created_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('IPaddress', self.gf('django.db.models.fields.GenericIPAddressField')(max_length=39)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_public', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('users', ['CommunityCategory'])

        # Adding M2M table for field community_set on 'CommunityCategory'
        db.create_table('users_communitycategory_community_set', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('communitycategory', models.ForeignKey(orm['users.communitycategory'], null=False)),
            ('community', models.ForeignKey(orm['users.community'], null=False))
        ))
        db.create_unique('users_communitycategory_community_set', ['communitycategory_id', 'community_id'])

        # Adding model 'CommunityMembership'
        db.create_table('users_communitymembership', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uuid', self.gf('django.db.models.fields.CharField')(default='62c062bf-5471-5132-94e1-c47f9c0ba733', unique=True, max_length=36)),
            ('kind', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('updated_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('created_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('last_visited', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('community', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.Community'])),
            ('member', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.UserProfile'])),
        ))
        db.send_create_signal('users', ['CommunityMembership'])


    def backwards(self, orm):
        # Deleting model 'UserProfile'
        db.delete_table('users_userprofile')

        # Removing M2M table for field image_collection_set on 'UserProfile'
        db.delete_table('users_userprofile_image_collection_set')

        # Removing M2M table for field wordbox_collection_set on 'UserProfile'
        db.delete_table('users_userprofile_wordbox_collection_set')

        # Deleting model 'Notification'
        db.delete_table('users_notification')

        # Deleting model 'UserSubscription'
        db.delete_table('users_usersubscription')

        # Deleting model 'Friendship'
        db.delete_table('users_friendship')

        # Deleting model 'Community'
        db.delete_table('users_community')

        # Deleting model 'CommunityCategory'
        db.delete_table('users_communitycategory')

        # Removing M2M table for field community_set on 'CommunityCategory'
        db.delete_table('users_communitycategory_community_set')

        # Deleting model 'CommunityMembership'
        db.delete_table('users_communitymembership')


    models = {
        'actions.comment': {
            'IPaddress': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39'}),
            'Meta': {'object_name': 'Comment'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True', 'blank': 'True'}),
            'created_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'owner_comment_set'", 'to': "orm['users.UserProfile']"}),
            'parent_comment': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['actions.Comment']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'total_votes': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'17652e0e-b7c7-559c-8ac7-5f57e2e883fc'", 'unique': 'True', 'max_length': '36'})
        },
        'actions.favorite': {
            'IPaddress': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39'}),
            'Meta': {'object_name': 'Favorite'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'created_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['users.UserProfile']"}),
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'74779476-022e-5454-aae3-d570ed1bf373'", 'unique': 'True', 'max_length': '36'}),
            'value': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'actions.vote': {
            'IPaddress': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39'}),
            'Meta': {'object_name': 'Vote'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'created_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['users.UserProfile']"}),
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'3c76a9d9-2f38-5073-a25f-a45b6a95ed52'", 'unique': 'True', 'max_length': '36'}),
            'value': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'media.collection': {
            'IPaddress': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39'}),
            'Meta': {'object_name': 'Collection'},
            'created_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'owner': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['users.UserProfile']", 'unique': 'True'}),
            'updated_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'643c30ae-773d-5489-ac85-9050df101c09'", 'unique': 'True', 'max_length': '36'})
        },
        'media.image': {
            'GPS_altitude': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'GPS_latitude': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'GPS_longitude': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'IPaddress': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39'}),
            'Meta': {'ordering': "['id']", 'object_name': 'Image'},
            'cameraMake': ('django.db.models.fields.CharField', [], {'max_length': '52', 'null': 'True'}),
            'cameraModel': ('django.db.models.fields.CharField', [], {'max_length': '52', 'null': 'True'}),
            'collection_set': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'image_set'", 'symmetrical': 'False', 'to': "orm['media.Collection']"}),
            'community_set': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'image_set'", 'symmetrical': 'False', 'to': "orm['users.Community']"}),
            'created_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'has_Geolocation': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_owner': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['users.UserProfile']"}),
            'position': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'updated_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'d582dc07-48e6-5cc2-88b6-ccc014ad61c1'", 'unique': 'True', 'max_length': '36'})
        },
        'media.wordbox': {
            'IPaddress': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39'}),
            'Meta': {'ordering': "['id']", 'object_name': 'WordBox'},
            'collection_set': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'wordbox_set'", 'symmetrical': 'False', 'to': "orm['media.Collection']"}),
            'community_set': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'wordbox_set'", 'symmetrical': 'False', 'to': "orm['users.Community']"}),
            'created_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['users.UserProfile']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'updated_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'2ae443b0-5169-5b06-b2e9-399fb3f77775'", 'unique': 'True', 'max_length': '36'})
        },
        'taggit.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
        },
        'taggit.taggeditem': {
            'Meta': {'object_name': 'TaggedItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'taggit_taggeditem_tagged_items'", 'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'taggit_taggeditem_items'", 'to': "orm['taggit.Tag']"})
        },
        'users.community': {
            'IPaddress': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39'}),
            'Meta': {'object_name': 'Community'},
            'created_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'created_community_set'", 'to': "orm['users.UserProfile']"}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'member_set': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'community_set'", 'symmetrical': 'False', 'through': "orm['users.CommunityMembership']", 'to': "orm['users.UserProfile']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'profile_image_standard': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'community_of_standard'", 'unique': 'True', 'null': 'True', 'to': "orm['media.Image']"}),
            'profile_image_thumbnail': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'community_of_thumbnail'", 'unique': 'True', 'null': 'True', 'to': "orm['media.Image']"}),
            'total_admins': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'total_collections': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'total_subscribers': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'updated_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'0b1806e2-2e53-56f7-ab25-f10b63318782'", 'unique': 'True', 'max_length': '36'})
        },
        'users.communitycategory': {
            'IPaddress': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39'}),
            'Meta': {'object_name': 'CommunityCategory'},
            'community_set': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'communitycategory_set'", 'symmetrical': 'False', 'to': "orm['users.Community']"}),
            'created_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'updated_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'9d975268-fbfa-5efe-aa0e-2d440c66a2e9'", 'unique': 'True', 'max_length': '36'})
        },
        'users.communitymembership': {
            'Meta': {'object_name': 'CommunityMembership'},
            'community': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['users.Community']"}),
            'created_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'kind': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'last_visited': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['users.UserProfile']"}),
            'updated_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'be78fd4c-8311-592c-92be-6a40146517c1'", 'unique': 'True', 'max_length': '36'})
        },
        'users.friendship': {
            'IPaddress': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39'}),
            'Meta': {'object_name': 'Friendship'},
            'created_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'from_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'to_friendships'", 'to': "orm['users.UserProfile']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'to_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'from_friendships'", 'to': "orm['users.UserProfile']"}),
            'updated_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'b274db9d-f1e6-5771-ac42-c6a0164f105c'", 'unique': 'True', 'max_length': '36'}),
            'was_accepted': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'users.notification': {
            'IPaddress': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39'}),
            'Meta': {'object_name': 'Notification'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'created_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'from_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'to_notifications'", 'to': "orm['users.UserProfile']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'to_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'from_notifications'", 'to': "orm['users.UserProfile']"}),
            'updated_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'502cdd65-317e-5409-9908-dcdb5d272dee'", 'unique': 'True', 'max_length': '36'}),
            'was_read': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'users.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'about_me': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1024'}),
            'birthday': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'created_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'fashion_statement': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '2048'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'height': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_collection_set': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'userprofile_set'", 'symmetrical': 'False', 'to': "orm['media.Image']"}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'last_login_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'last_notification': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(1970, 1, 1, 0, 0)'}),
            'location': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '2048'}),
            'middle_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'notification_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True'}),
            'profile_image_standard': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'profile_of_standard'", 'unique': 'True', 'null': 'True', 'to': "orm['media.Image']"}),
            'profile_image_thumbnail': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'profile_of_thumbnail'", 'unique': 'True', 'null': 'True', 'to': "orm['media.Image']"}),
            'statement': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'to_friends': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'from_friends'", 'symmetrical': 'False', 'through': "orm['users.Friendship']", 'to': "orm['users.UserProfile']"}),
            'to_notifiers': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'from_notifiers'", 'symmetrical': 'False', 'through': "orm['users.Notification']", 'to': "orm['users.UserProfile']"}),
            'to_subscribers': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'from_subscribers'", 'symmetrical': 'False', 'through': "orm['users.UserSubscription']", 'to': "orm['users.UserProfile']"}),
            'total_collections': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'total_friends': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'total_groups': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'total_notifications': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'updated_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'null': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'31324b7c-b9c4-5556-93b8-96759af5ffac'", 'unique': 'True', 'max_length': '36'}),
            'website': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '200'}),
            'weight': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'wordbox_collection_set': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'userprofile_set'", 'symmetrical': 'False', 'to': "orm['media.WordBox']"})
        },
        'users.usersubscription': {
            'IPaddress': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39'}),
            'Meta': {'object_name': 'UserSubscription'},
            'created_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'from_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'to_usersubscriptions'", 'to': "orm['users.UserProfile']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'to_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'from_usersubscriptions'", 'to': "orm['users.UserProfile']"}),
            'updated_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'729fbe27-4ccd-506d-af5b-508dc831ed17'", 'unique': 'True', 'max_length': '36'})
        }
    }

    complete_apps = ['users']