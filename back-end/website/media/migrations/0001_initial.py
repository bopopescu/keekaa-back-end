# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Collection'
        db.create_table('media_collection', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uuid', self.gf('django.db.models.fields.CharField')(default='34beedaf-cb7a-58be-a76c-453cca2a3f98', unique=True, max_length=36)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(default='')),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('updated_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('created_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('IPaddress', self.gf('django.db.models.fields.GenericIPAddressField')(max_length=39)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_public', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('owner', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['users.UserProfile'], unique=True)),
        ))
        db.send_create_signal('media', ['Collection'])

        # Adding model 'Image'
        db.create_table('media_image', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uuid', self.gf('django.db.models.fields.CharField')(default='14500073-840f-5cb7-90a5-cd14fb3f2b65', unique=True, max_length=36)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('description', self.gf('django.db.models.fields.TextField')(default='')),
            ('created_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('updated_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('position', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('IPaddress', self.gf('django.db.models.fields.GenericIPAddressField')(max_length=39)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_public', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('has_owner', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('cameraMake', self.gf('django.db.models.fields.CharField')(max_length=52, null=True)),
            ('cameraModel', self.gf('django.db.models.fields.CharField')(max_length=52, null=True)),
            ('has_Geolocation', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('GPS_latitude', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('GPS_longitude', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('GPS_altitude', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.UserProfile'])),
        ))
        db.send_create_signal('media', ['Image'])

        # Adding M2M table for field collection_set on 'Image'
        db.create_table('media_image_collection_set', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('image', models.ForeignKey(orm['media.image'], null=False)),
            ('collection', models.ForeignKey(orm['media.collection'], null=False))
        ))
        db.create_unique('media_image_collection_set', ['image_id', 'collection_id'])

        # Adding M2M table for field community_set on 'Image'
        db.create_table('media_image_community_set', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('image', models.ForeignKey(orm['media.image'], null=False)),
            ('community', models.ForeignKey(orm['users.community'], null=False))
        ))
        db.create_unique('media_image_community_set', ['image_id', 'community_id'])

        # Adding model 'ImageVersion'
        db.create_table('media_imageversion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('height', self.gf('django.db.models.fields.IntegerField')()),
            ('width', self.gf('django.db.models.fields.IntegerField')()),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('filesize', self.gf('django.db.models.fields.BigIntegerField')()),
            ('image', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['media.Image'])),
        ))
        db.send_create_signal('media', ['ImageVersion'])

        # Adding model 'WordBox'
        db.create_table('media_wordbox', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uuid', self.gf('django.db.models.fields.CharField')(default='3b3c8de3-d6eb-5ab3-be74-16eec4730d8e', unique=True, max_length=36)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('message', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('created_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('updated_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('IPaddress', self.gf('django.db.models.fields.GenericIPAddressField')(max_length=39)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_public', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.UserProfile'])),
        ))
        db.send_create_signal('media', ['WordBox'])

        # Adding M2M table for field community_set on 'WordBox'
        db.create_table('media_wordbox_community_set', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('wordbox', models.ForeignKey(orm['media.wordbox'], null=False)),
            ('community', models.ForeignKey(orm['users.community'], null=False))
        ))
        db.create_unique('media_wordbox_community_set', ['wordbox_id', 'community_id'])

        # Adding M2M table for field collection_set on 'WordBox'
        db.create_table('media_wordbox_collection_set', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('wordbox', models.ForeignKey(orm['media.wordbox'], null=False)),
            ('collection', models.ForeignKey(orm['media.collection'], null=False))
        ))
        db.create_unique('media_wordbox_collection_set', ['wordbox_id', 'collection_id'])


    def backwards(self, orm):
        # Deleting model 'Collection'
        db.delete_table('media_collection')

        # Deleting model 'Image'
        db.delete_table('media_image')

        # Removing M2M table for field collection_set on 'Image'
        db.delete_table('media_image_collection_set')

        # Removing M2M table for field community_set on 'Image'
        db.delete_table('media_image_community_set')

        # Deleting model 'ImageVersion'
        db.delete_table('media_imageversion')

        # Deleting model 'WordBox'
        db.delete_table('media_wordbox')

        # Removing M2M table for field community_set on 'WordBox'
        db.delete_table('media_wordbox_community_set')

        # Removing M2M table for field collection_set on 'WordBox'
        db.delete_table('media_wordbox_collection_set')


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
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'b0a2c114-82e3-5445-8438-4b9e0d0d0a67'", 'unique': 'True', 'max_length': '36'})
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
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'34a80377-f5fa-50c3-b2c4-5e3cba8cd275'", 'unique': 'True', 'max_length': '36'}),
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
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'94fe9c0e-4d14-541a-be75-f0ea6e785f8f'", 'unique': 'True', 'max_length': '36'}),
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
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'38fe6298-cb9c-5b97-9cb2-b0310f71562c'", 'unique': 'True', 'max_length': '36'})
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
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'1aa2c7ce-afba-5587-9457-1fc432f7be09'", 'unique': 'True', 'max_length': '36'})
        },
        'media.imageversion': {
            'Meta': {'object_name': 'ImageVersion'},
            'filesize': ('django.db.models.fields.BigIntegerField', [], {}),
            'height': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['media.Image']"}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'width': ('django.db.models.fields.IntegerField', [], {})
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
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'3fee950f-2659-5536-85a8-99cce7f3dc64'", 'unique': 'True', 'max_length': '36'})
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
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'0723eb06-fa26-5b1b-8053-dda17262cca7'", 'unique': 'True', 'max_length': '36'})
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
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'3eb568cf-2841-56eb-8b72-89d9533b3870'", 'unique': 'True', 'max_length': '36'})
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
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'63f32f20-0c58-5100-96e6-ba146fc65492'", 'unique': 'True', 'max_length': '36'}),
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
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'599a0c5f-4b8d-5998-ab8b-be1308519b80'", 'unique': 'True', 'max_length': '36'}),
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
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'58b1b0a1-bd7f-524d-a6cf-e053656b6115'", 'unique': 'True', 'max_length': '36'}),
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
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'8b4aee27-ba8f-507f-ab41-f5b1d78a4c1d'", 'unique': 'True', 'max_length': '36'})
        }
    }

    complete_apps = ['media']