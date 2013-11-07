# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Brand'
        db.create_table('brands_brand', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uuid', self.gf('django.db.models.fields.CharField')(default='35d145a0-3469-560f-aa5a-a1516e348cdc', unique=True, max_length=36)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('url_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('address', self.gf('django.db.models.fields.TextField')(default='')),
            ('description', self.gf('django.db.models.fields.TextField')(default='')),
            ('updated_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('created_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('IPaddress', self.gf('django.db.models.fields.GenericIPAddressField')(max_length=39)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.UserProfile'])),
        ))
        db.send_create_signal('brands', ['Brand'])

        # Adding model 'Item'
        db.create_table('brands_item', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uuid', self.gf('django.db.models.fields.CharField')(default='e98b1f97-6f12-57c3-9945-5a42582408a5', unique=True, max_length=36)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('size', self.gf('django.db.models.fields.CharField')(default='', max_length=3)),
            ('price', self.gf('django.db.models.fields.DecimalField')(default=0.0, max_digits=9, decimal_places=2)),
            ('color', self.gf('django.db.models.fields.CharField')(default='', max_length=32)),
            ('description', self.gf('django.db.models.fields.TextField')(default='')),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('brand_name', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
            ('updated_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('created_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('IPaddress', self.gf('django.db.models.fields.GenericIPAddressField')(max_length=39)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('brand', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['brands.Brand'], null=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['users.UserProfile'])),
        ))
        db.send_create_signal('brands', ['Item'])

        # Adding model 'ItemTag'
        db.create_table('brands_itemtag', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uuid', self.gf('django.db.models.fields.CharField')(default='97c87897-718b-5df0-b6d6-d233263eb34f', unique=True, max_length=36)),
            ('x', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('y', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('num', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('updated_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('created_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('IPaddress', self.gf('django.db.models.fields.GenericIPAddressField')(max_length=39)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.UserProfile'])),
            ('image', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['media.Image'])),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['brands.Item'])),
        ))
        db.send_create_signal('brands', ['ItemTag'])


    def backwards(self, orm):
        # Deleting model 'Brand'
        db.delete_table('brands_brand')

        # Deleting model 'Item'
        db.delete_table('brands_item')

        # Deleting model 'ItemTag'
        db.delete_table('brands_itemtag')


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
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'f9083b4e-f17c-54dc-8417-b96b25815cd2'", 'unique': 'True', 'max_length': '36'})
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
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'54b1f067-b972-50da-ac56-19bf70f8144f'", 'unique': 'True', 'max_length': '36'}),
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
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'aa6295aa-4c6e-5c94-b5a3-c14bff4eb298'", 'unique': 'True', 'max_length': '36'}),
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
        'brands.brand': {
            'IPaddress': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39'}),
            'Meta': {'object_name': 'Brand'},
            'address': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'created_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['users.UserProfile']"}),
            'updated_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'url_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'d417a32a-be3f-55a7-9bf8-2b0f75cee965'", 'unique': 'True', 'max_length': '36'})
        },
        'brands.item': {
            'IPaddress': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39'}),
            'Meta': {'object_name': 'Item'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['brands.Brand']", 'null': 'True'}),
            'brand_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'color': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '32'}),
            'created_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_set': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['media.Image']", 'through': "orm['brands.ItemTag']", 'symmetrical': 'False'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'to': "orm['users.UserProfile']"}),
            'price': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '9', 'decimal_places': '2'}),
            'size': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '3'}),
            'updated_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'bb1c33ce-d3d1-59a1-bdac-0d906560b87f'", 'unique': 'True', 'max_length': '36'})
        },
        'brands.itemtag': {
            'IPaddress': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39'}),
            'Meta': {'object_name': 'ItemTag'},
            'created_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['media.Image']"}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['brands.Item']"}),
            'num': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['users.UserProfile']"}),
            'updated_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'bfdfef4e-e8eb-54d6-944e-486ec29b0593'", 'unique': 'True', 'max_length': '36'}),
            'x': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'y': ('django.db.models.fields.FloatField', [], {'default': '0'})
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
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'7d0218e3-dd6e-5548-b645-e021578c1e12'", 'unique': 'True', 'max_length': '36'})
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
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'f665f636-d57c-5c62-a071-0b377aafd6c0'", 'unique': 'True', 'max_length': '36'})
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
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'26f5114a-09fe-56ba-bee8-c6edeeb30436'", 'unique': 'True', 'max_length': '36'})
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
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'da7ba5ec-3f34-5e63-802d-c85694a70f44'", 'unique': 'True', 'max_length': '36'})
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
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'bd9555c5-4d24-5912-98ba-f2a6a6abd233'", 'unique': 'True', 'max_length': '36'})
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
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'dc5961d3-2abd-5976-b691-ed6e98bd0a66'", 'unique': 'True', 'max_length': '36'}),
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
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'7e13d1c8-2b95-539c-a4d0-d4a677cdb5cb'", 'unique': 'True', 'max_length': '36'}),
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
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'a8ea2be3-3cbc-5a85-b440-26fbfc6c3eb6'", 'unique': 'True', 'max_length': '36'}),
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
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'7a2c2ba8-7cce-5fe2-850d-77c066d11224'", 'unique': 'True', 'max_length': '36'})
        }
    }

    complete_apps = ['brands']