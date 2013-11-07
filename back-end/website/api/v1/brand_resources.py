#from django.db.models import Count
from tastypie.constants import ALL
#from django.conf.urls.defaults import *
from django.contrib.auth.models import User
from tastypie import http
from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.cache import SimpleCache
from tastypie.utils import now
from tastypie.exceptions import ImmediateHttpResponse
from urllib import urlencode
from website.library.validators import uuid_re
#from website.actions.models import *
from website.brands.models import Item, ItemTag, Brand
from website.users.models import UserProfile
from website.media.models import Image
#from website.api.v1.action_resources import *
from website.api.v1.media_resources import ImageResource
#from website.api.v1.user_resources import *
from website.library.tastypie_resources import DuJourModelResource
#    GenericForeignKeyField
from website.library.tastypie_serializers import TzSerializer


class BrandResource(DuJourModelResource):
    user = fields.ToOneField(
        'website.api.v1.user_resources.UserResource', 'owner')
    item = fields.ToManyField(
        'website.api.v1.brand_resources.ItemResource', 'item_set')
    created_time = fields.DateTimeField(
        attribute='created_time', readonly=True, default=now)
    updated_time = fields.DateTimeField(
        attribute='updated_time', readonly=True, default=now)

    class Meta:
        cache = SimpleCache()
        serializer = TzSerializer()
        detail_uri_name = 'uuid'
        always_return_data = True
        queryset = Brand.objects.filter(is_active=True)
        resource_name = 'brand'
        fields = ['name', 'url_name', 'description', 'address']
        detail_allowed_methods = ['get', 'put', 'delete']
        list_allowed_methods = ['get', 'post']
        ordering = ['created_time']
        filtering = {
            "owner": ALL,
            "total_votes": ALL,
        }
        max_limit = 20
        authorization = Authorization()
        include_resource_uri = True

    def dehydrate(self, bundle):
        bundle.data['total_items'] = bundle.obj.item_set.all().count()
        bundle.data['total_votes'] = bundle.obj.total_votes()
        bundle.data['total_comments'] = bundle.obj.total_comments()
        bundle.data['total_favorites'] = bundle.obj.total_favorites()
        bundle.data['comment'] = '/v1/comment/?' + \
            urlencode({'parent': bundle.data['resource_uri']})
        bundle.data['vote'] = '/v1/vote/?' + \
            urlencode({'parent': bundle.data['resource_uri']})
        if self.get_resource_uri(bundle) != bundle.request.path:
            bundle.data['item'] = '/v1/item/?' + \
                urlencode({'brand': bundle.data['resource_uri']})
        return bundle

    def apply_sorting(self, objects, options=None):
        options = {"order_by": "-created_time"}
        return super(BrandResource, self).apply_sorting(objects, options)

    # set value of field that is not visible
    def hydrate(self, bundle):
        if hasattr(bundle.obj, 'IPaddress'):
            bundle.obj.IPaddress = bundle.request.META['REMOTE_ADDR']
        return bundle

    # set custom value of field that is visible
    def hydrate_owner(self, bundle):
        # WARNING (DB) - makes sure user is authorized first for
        # this may cause problems
        bundle.obj.owner = User.objects.get(
            pk=bundle.request.user.id).get_profile()
        bundle.data['owner'] = None
        return bundle

    def build_filters(self, filters=None):
        if filters is None:
            filters = {}
        orm_filters = super(BrandResource, self).build_filters(
            filters)  # modify super(*,self)
        if filters:  # check if dictionary is empty or not
            try:
                if "owner" in filters:
                    obj = UserProfile.objects.get(uuid=uuid_re.search(
                        filters['owner']).group())
                    if 'owner__exact' in orm_filters:
                        # delete this field since this is a GFK
                        del orm_filters['owner__exact']
                    else:
                        raise ImmediateHttpResponse(response=http.HttpNotFound(
                        ))
                else:
                    return orm_filters
                if not obj.is_active:
                    return orm_filters
                sqs = obj.brand_set.filter(is_active=True)
                orm_filters["pk__in"] = [i.pk for i in sqs]
            except Brand.DoesNotExist:
                orm_filters["pk__in"] = []
                # return HttpGone()
            except Brand.MultipleObjectsReturned:
                # return HttpMultipleChoices("More than one resource is found "
                #                            "at this URI.")
                orm_filters["pk__in"] = []
                raise ImmediateHttpResponse(response=http.HttpNotFound())
        return orm_filters


class ItemResource(DuJourModelResource):
    owner = fields.ToOneField('website.api.v1.user_resources.UserResource',
                              'owner')
#    brand = fields.ToOneField(BrandResource, 'brand')
    created_time = fields.DateTimeField(
        attribute='created_time', readonly=True, default=now)
    updated_time = fields.DateTimeField(
        attribute='updated_time', readonly=True, default=now)

    class Meta:
        cache = SimpleCache()
        serializer = TzSerializer()
        detail_uri_name = 'uuid'
        always_return_data = True
        queryset = Item.objects.filter(is_active=True)
        ordering = ['created_time']
        resource_name = 'item'
        fields = ['name', 'description', 'size', 'price', 'color',
                  'url', 'brand_name']
        detail_allowed_methods = ['get', 'delete', 'patch']
        list_allowed_methods = ['get', 'post']
        filtering = {
            "owner": ALL,
            "brand": ALL,
            "total_votes": ALL,
        }
        max_limit = 20
        authorization = Authorization()
        include_resource_uri = True

    def dehydrate(self, bundle):
        bundle.data['total_votes'] = bundle.obj.total_votes()
        bundle.data['total_comments'] = bundle.obj.total_comments()
        bundle.data['comment'] = '/v1/comment/?' + \
            urlencode({'parent': bundle.data['resource_uri']})
        bundle.data['vote'] = '/v1/vote/?' + \
            urlencode({'parent': bundle.data['resource_uri']})
        return bundle

    def apply_sorting(self, objects, options=None):
        options = {"order_by": "-created_time"}
        return super(ItemResource, self).apply_sorting(objects, options)

    # set value of field that is not visible
    def hydrate(self, bundle):
        if hasattr(bundle.obj, 'IPaddress'):
            bundle.obj.IPaddress = bundle.request.META['REMOTE_ADDR']
        return bundle

    # set custom value of field that is visible
    def hydrate_owner(self, bundle):
        # WARNING (DB) - makes sure user is authorized first
        # for this may cause problems
        bundle.obj.owner = User.objects.get(
            pk=bundle.request.user.id).get_profile()
#        bundle.data['owner'] = None
        return bundle

    def build_filters(self, filters=None):
        if filters is None:
            filters = {}
        orm_filters = super(ItemResource, self).build_filters(
            filters)  # modify super(*,self)
        if filters:  # check if dictionary is empty or not
            try:
                if "owner" in filters:
                    obj = UserProfile.objects.get(uuid=uuid_re.search(
                        filters['owner']).group())
                    if 'owner__exact' in orm_filters:
                        # delete this field since this is a GFK
                        del orm_filters['owner__exact']
                if "brand" in filters:
                    obj = Brand.objects.get(uuid=uuid_re.search(
                        filters['brand']).group())
                    if 'brand__exact' in orm_filters:
                        # delete this field since this is a GFK
                        del orm_filters['brand__exact']
                else:
                    return orm_filters
                if not obj.is_active:
                    return orm_filters
                sqs = obj.item_set.filter(is_active=True)
                orm_filters["pk__in"] = [i.pk for i in sqs]
            except Item.DoesNotExist:
                orm_filters["pk__in"] = []
                # return HttpGone()
            except Item.MultipleObjectsReturned:
                # return HttpMultipleChoices("More than one resource is found "
                #                            "at this URI.")
                orm_filters["pk__in"] = []
                raise ImmediateHttpResponse(response=http.HttpNotFound())
        return orm_filters


class ItemTagResource(DuJourModelResource):
    owner = fields.ToOneField(
        'website.api.v1.user_resources.UserResource', 'owner', readonly=False)
    item = fields.ToOneField(ItemResource, 'item')
    image = fields.ToOneField(ImageResource, 'image')
    created_time = fields.DateTimeField(
        attribute='created_time', readonly=True, default=now)
    updated_time = fields.DateTimeField(
        attribute='updated_time', readonly=True, default=now)

    class Meta:
        cache = SimpleCache()
        serializer = TzSerializer()
        detail_uri_name = 'uuid'
        always_return_data = True
        queryset = ItemTag.objects.filter(is_active=True)
        resource_name = 'itemtag'
        ordering = ['created_time']
        fields = ['num', 'x', 'y']
        detail_allowed_methods = ['get', 'delete', 'patch']
        list_allowed_methods = ['get', 'post']
        filtering = {
            "image": ALL,
            "total_votes": ALL,
        }
        max_limit = 20
        authorization = Authorization()
        include_resource_uri = True

    def apply_sorting(self, objects, options=None):
        options = {"order_by": "-created_time"}
        return super(ItemTagResource, self).apply_sorting(objects, options)

    # set value of field that is not visible
    def hydrate(self, bundle):
        if hasattr(bundle.obj, 'IPaddress'):
            bundle.obj.IPaddress = bundle.request.META['REMOTE_ADDR']
        return bundle

    # set custom value of field that is visible
    def hydrate_owner(self, bundle):
        ## WARNING (DB) - makes sure user is authorized first or this
        # may cause problems
        bundle.obj.owner = User.objects.get(
            pk=bundle.request.user.id).get_profile()
        bundle.data['owner'] = None
        return bundle

    def build_filters(self, filters=None):
        if filters is None:
            filters = {}
        orm_filters = super(ItemTagResource, self).build_filters(
            filters)  # modify super(*,self)
        if filters:  # check if dictionary is empty or not
            try:
                if "image" in filters:
                    obj = Image.objects.get(uuid=uuid_re.search(
                        filters['image']).group())
                    if 'image__exact' in orm_filters:
                        # delete this field since this is a GFK
                        del orm_filters['image__exact']
                else:
                    return orm_filters
                if not obj.is_active:
                    return orm_filters
                sqs = obj.itemtag_set.filter(is_active=True)
                orm_filters["pk__in"] = [i.pk for i in sqs]
            except ItemTag.DoesNotExist:
                orm_filters["pk__in"] = []
                # return HttpGone()
            except ItemTag.MultipleObjectsReturned:
                # return HttpMultipleChoices("More than one resource is found "
                #                            "at this URI.")
                orm_filters["pk__in"] = []
                raise ImmediateHttpResponse(response=http.HttpNotFound())
        return orm_filters
