# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Action'
        db.create_table('actions_action', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uuid', self.gf('django.db.models.fields.CharField')(default='8fbc393c-f6b8-5978-a0b7-4c9ca719339a', unique=True, max_length=36)),
            ('request_method', self.gf('django.db.models.fields.IntegerField')()),
            ('created_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, db_index=True)),
            ('parent_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='parent_action_set', to=orm['contenttypes.ContentType'])),
            ('parent_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('child_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='child_action_set', null=True, to=orm['contenttypes.ContentType'])),
            ('child_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True)),
            ('has_error', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('IPaddress', self.gf('django.db.models.fields.GenericIPAddressField')(max_length=39)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_public', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.UserProfile'])),
        ))
        db.send_create_signal('actions', ['Action'])

        # Adding model 'Vote'
        db.create_table('actions_vote', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uuid', self.gf('django.db.models.fields.CharField')(default='938f5b01-9063-51a1-847e-14ddc05863c5', unique=True, max_length=36)),
            ('value', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('created_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('IPaddress', self.gf('django.db.models.fields.GenericIPAddressField')(max_length=39)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_public', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.UserProfile'])),
        ))
        db.send_create_signal('actions', ['Vote'])

        # Adding model 'Favorite'
        db.create_table('actions_favorite', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uuid', self.gf('django.db.models.fields.CharField')(default='b6a29cef-ef36-5ad2-8520-2f340c0bd468', unique=True, max_length=36)),
            ('value', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('created_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('IPaddress', self.gf('django.db.models.fields.GenericIPAddressField')(max_length=39)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_public', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.UserProfile'])),
        ))
        db.send_create_signal('actions', ['Favorite'])

        # Adding model 'Comment'
        db.create_table('actions_comment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('uuid', self.gf('django.db.models.fields.CharField')(default='33cbc4ca-e159-5f87-a1eb-8553661410af', unique=True, max_length=36)),
            ('message', self.gf('django.db.models.fields.TextField')()),
            ('created_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('IPaddress', self.gf('django.db.models.fields.GenericIPAddressField')(max_length=39)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_public', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'], null=True, blank=True)),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('parent_comment', self.gf('mptt.fields.TreeForeignKey')(blank=True, related_name='children', null=True, to=orm['actions.Comment'])),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='owner_comment_set', to=orm['users.UserProfile'])),
            ('total_votes', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal('actions', ['Comment'])


    def backwards(self, orm):
        # Deleting model 'Action'
        db.delete_table('actions_action')

        # Deleting model 'Vote'
        db.delete_table('actions_vote')

        # Deleting model 'Favorite'
        db.delete_table('actions_favorite')

        # Deleting model 'Comment'
        db.delete_table('actions_comment')


    models = {
        'actions.action': {
            'IPaddress': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39'}),
            'Meta': {'object_name': 'Action'},
            'child_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'child_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'child_action_set'", 'null': 'True', 'to': "orm['contenttypes.ContentType']"}),
            'created_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'db_index': 'True'}),
            'has_error': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['users.UserProfile']"}),
            'parent_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'parent_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'parent_action_set'", 'to': "orm['contenttypes.ContentType']"}),
            'request_method': ('django.db.models.fields.IntegerField', [], {}),
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'78b69025-cbb7-5768-bd1d-704adb09a999'", 'unique': 'True', 'max_length': '36'})
        },
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
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'97159d35-2878-52a4-b718-afe045367d85'", 'unique': 'True', 'max_length': '36'})
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
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'5805f78c-6f21-5556-bc19-56e8afdb94ea'", 'unique': 'True', 'max_length': '36'}),
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
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'6165f9fe-6070-526d-9f4a-fcb58fbb9964'", 'unique': 'True', 'max_length': '36'}),
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
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'249f3313-1614-5471-b773-0136bad3546c'", 'unique': 'True', 'max_length': '36'})
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
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'7733e5eb-2185-52a9-96b6-518c5739c51f'", 'unique': 'True', 'max_length': '36'})
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
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'d00ce084-aafc-5558-99c3-5a7ca14e52cf'", 'unique': 'True', 'max_length': '36'})
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
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'7db17528-6e31-5559-b757-b75bcd2d4add'", 'unique': 'True', 'max_length': '36'})
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
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'ac2df894-c94d-5804-a0cf-e42b0e81d376'", 'unique': 'True', 'max_length': '36'})
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
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'c6e3336c-b780-5418-bf12-ae277bc3ccfa'", 'unique': 'True', 'max_length': '36'}),
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
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'372e529a-d476-5b66-b26f-27573a7b6e4e'", 'unique': 'True', 'max_length': '36'}),
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
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'a5709497-fb7b-5c5a-8dd2-c358773c0028'", 'unique': 'True', 'max_length': '36'}),
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
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'63ae6f60-176c-58c2-b925-78ae0625358a'", 'unique': 'True', 'max_length': '36'})
        }
    }

    complete_apps = ['actions']