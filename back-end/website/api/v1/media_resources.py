import json
import StringIO

from boto.s3.connection import S3Connection
from operator import attrgetter
from itertools import chain
from django.conf.urls.defaults import url
from django.http import HttpResponseNotFound, HttpResponse
from django.core.exceptions import ObjectDoesNotExist, \
    MultipleObjectsReturned
from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.cache import SimpleCache
from tastypie.utils import now, trailing_slash
from tastypie.exceptions import ImmediateHttpResponse, BadRequest
from tastypie.constants import ALL
from tastypie import http
from tastypie.http import HttpGone, HttpForbidden, HttpCreated, \
    HttpMultipleChoices
from urllib import urlencode
from PIL import Image as PIL_Image
from PIL.ExifTags import TAGS
from website.library import pushwoosh
from website.library.tastypie_resources import DuJourModelResource
from website.library.tastypie_serializers import TzSerializer
from website.library.helper_functions import uuid_from_uri
from website.library.validators import uuid_re
from website.media.models import WordBox, Collection, Image, ImageVersion
from website.users.models import UserProfile, Community
from website.settings import S3_ACCESS_KEY_ID, S3_SECRET_ACCESS_KEY, S3_BUCKET


class ImageVersionResource(DuJourModelResource):
    class Meta:
        cache = SimpleCache()
        serializer = TzSerializer()
        include_resource_uri = False
        queryset = ImageVersion.objects.all()
        list_allowed_methods = []
        fields = ['width', 'height']
        detail_allowed_methods = ['get']

    def dehydrate(self, bundle):
        bundle.data['resource_uri'] = bundle.obj.get_uri()
        return bundle


class ImageResource(DuJourModelResource):
    owner = fields.ToOneField(
        'website.api.v1.user_resources.UserResource', 'owner')
    versions = fields.ToManyField(
        ImageVersionResource,
        attribute=lambda bundle:
        bundle.obj.imageversion_set.all(),
        full=True, readonly=True, null=True
    )
    top_comments = fields.ToManyField(
        'website.api.v1.action_resources.CommentResource',
        attribute=lambda bundle:
        bundle.obj.comment_set.filter(is_active=True).order_by('created_time')
        [0:2], full=True, readonly=True, null=True
    )
    created_time = fields.DateTimeField(
        attribute='created_time', readonly=True, default=now
    )
    updated_time = fields.DateTimeField(
        attribute='updated_time', readonly=True, default=now
    )

    class Meta(object):
        always_return_data = True
        authorization = Authorization()
        serializer = TzSerializer()
        cache = SimpleCache()
        #cache_control = {"max_age": 60*5}
        detail_allowed_methods = ['get', 'post', 'delete', 'patch']
        detail_uri_name = 'uuid'
        fields = ['title', 'description', 'has_owner']
        filtering = {
            "owner": ALL,
            "collection": ALL,
            "total_votes": ALL,
        }
        list_allowed_methods = ['get', 'post', 'delete']
        max_limit = 20
        ordering = ['created_time']
        queryset = Image.objects.filter(is_active=True).select_related(
            'user').prefetch_related('imageversion_set')
        resource_name = 'image'

    def dehydrate(self, bundle):
        try:
            bundle.data['username'] = bundle.obj.owner.username
            bundle.data['name'] = bundle.obj.owner.full_name(
            )  # owner's full name
        except:
            pass

        bundle.data['total_votes'] = bundle.obj.total_votes()
        bundle.data['total_comments'] = bundle.obj.total_comments()
        bundle.data['total_collected'] = bundle.obj.userprofile_set.count()
        bundle.data['total_items'] = bundle.obj.item_set.count()
        # fields for list end-points
        bundle.data['comment'] = '/v1/comment/?' + urlencode({
            'parent': bundle.data['resource_uri']})
        bundle.data['vote'] = '/v1/vote/?' + \
            urlencode({'parent': bundle.data['resource_uri']})
        return bundle

    def apply_sorting(self, objects, options=None):
        options = {"order_by": "-created_time"}
        return super(ImageResource, self).apply_sorting(objects, options)

    def build_filters(self, filters=None):
        if filters is None:
            filters = {}
        orm_filters = super(ImageResource, self).build_filters(
            filters)  # modify super(*,self)
        orm_filters = {}
        if filters:  # check if dictionary is empty or not
            try:
                if "collection" in filters:
                    obj = Collection.objects.get(uuid=uuid_re.search(
                        filters['collection']).group())
                elif "owner" in filters:
                    obj = UserProfile.objects.get(uuid=uuid_re.search(
                        filters['owner']).group())
                elif "community" in filters:
                    obj = Community.objects.get(uuid=uuid_re.search(
                        filters['community']).group())
                else:
                    return orm_filters
                if not obj.is_active:
                    return orm_filters
                sqs = obj.image_set.filter(is_active=True)
                orm_filters["pk__in"] = [i.pk for i in sqs]
            except Image.DoesNotExist:
                orm_filters["pk__in"] = []
                # return HttpGone()
            except Image.MultipleObjectsReturned:
                orm_filters["pk__in"] = []
                # return HttpMultipleChoices("More than one resource is found "
                #                            "at this URI.")
                raise ImmediateHttpResponse(response=http.HttpNotFound())
        return orm_filters

    def hydrate(self, bundle):
        if hasattr(bundle.obj, 'IPaddress'):
            bundle.obj.IPaddress = bundle.request.META['REMOTE_ADDR']
        return bundle

    #def hydrate_owner(self, bundle):
        ## WARNING - makes sure user is authorized first
        ## for this may cause problems
        #bundle.obj.owner = User.objects.get(
            #pk=bundle.request.user.id).get_profile()
        #bundle.data['owner'] = None
        #return bundle

    def obj_create(self, bundle, request=None, **kwargs):
        key_len = len(request.FILES)
        # If there is no image, simply return 415 (Unsupported Media Type)
        if key_len < 1:
            raise ImmediateHttpResponse(response=HttpResponse(status=415))
        key = list(request.FILES.viewkeys())[0]
        raw_file = request.FILES[key]
        try:
            image = PIL_Image.open(raw_file)
        except IOError:
        # If the image type is not supported,
        # return 415 (Unsupported Media Type)
            raise ImmediateHttpResponse(response=HttpResponse(status=415))
        RawImageWidth, RawImageHeight = image.size
        # JPEG rotation!
        if hasattr(image, "_getexif"):
            exif_info = image._getexif()
            ret = {}
            if exif_info is not None:
                for tag, value in exif_info.items():
                    decoded = TAGS.get(tag, tag)
                    ret[decoded] = value
                if 'Orientation' in ret:
                    orientation = int(ret['Orientation'])
                    if orientation == 3:
                        image = image.rotate(180)
                    if orientation == 6:
                        image = image.rotate(270)
                    if orientation == 8:
                        image = image.rotate(90)

        imageWidth, imageHeight = image.size

        ratio = float(imageWidth) / float(imageHeight)
        if imageWidth > 1920 or imageHeight > 1080:
        # If the image is too large, simply resize it.
            if ratio > 16.0 / 9.0:
                imageWidth = 1920
                imageHeight = int(imageWidth / ratio)
            else:
                imageHeight = 1080
                imageWidth = int(imageHeight * ratio)
        resizedVersions = [[imageWidth, imageHeight]]
        potentialVersions = [[int(800 * ratio), 800], [int(400 * ratio), 400],
                            [200, int(200 / ratio)], [100, int(100 / ratio)],
                            [50, int(50 / ratio)]]
        for i in potentialVersions:
            if i[0] * i[1] < imageHeight * imageWidth:
                resizedVersions.append(i)
        imageVersionList = []
        add_nulls = lambda number, zero_count: "{0:0{1}d}".format(
            number, zero_count)

        try:
            s3_conn = S3Connection(S3_ACCESS_KEY_ID,
                                   S3_SECRET_ACCESS_KEY, is_secure=False)
            s3_bucket = s3_conn.create_bucket(S3_BUCKET)
        except Exception:
            raise ImmediateHttpResponse(response=HttpResponse(status=415))
        for size in resizedVersions:
            v = ImageVersion()
            v.width = size[0]
            v.height = size[1]
            image.thumbnail(size, PIL_Image.ANTIALIAS)
            filename = (str(bundle.obj.uuid) + "_" + str(add_nulls(v.width, 5))
                        + "x" + str(add_nulls(v.height, 5)) + '.jpg')

            try:
                fp = StringIO.StringIO()
                image.save(fp, format="JPEG", quality=95)
                size = fp.len
                key = s3_bucket.new_key('images/' + filename)
                key.set_metadata('Content-Type', 'image/jpeg')
                key.set_metadata('Cache-Control', 'public,max-age=5184000')
                key.set_contents_from_string(fp.getvalue())
                key.set_acl('public-read')
            except Exception:
                raise ImmediateHttpResponse(response=HttpResponse(status=415))
            v.url = "/images/" + filename
            v.filesize = size
            imageVersionList.append(v)
        bundle = super(ImageResource, self).obj_create(bundle,
                                                       request=None, **kwargs)
        for imageVersionObj in imageVersionList:
            imageVersionObj.image = bundle.obj
            imageVersionObj.save()

        try:
            filename = (str(bundle.obj.uuid) + "_" +
                        str(add_nulls(RawImageWidth, 5)) +
                        "x" + str(add_nulls(RawImageHeight, 5)) + '.raw')
            key = s3_bucket.new_key('images/' + filename)
            key.set_contents_from_string(raw_file.read())
        except Exception:
            raise ImmediateHttpResponse(response=HttpResponse(status=415))

        push = pushwoosh.Pushwoosh(
            'dbtsai',
            'bbf8bd651409019ba808f26ab2c3ce43',
            '953DE-72507'
        )
        data={'resource_uri': '/v1/image/%s/' % bundle.obj.uuid}
        notification = push.Notification(
            u"%s wants your opinion!" % request.user.first_name,
            devices=None, data=data
        )
        try:
            push.push(notification)
        except Exception:
            pass

        return bundle


class CollectionResource(DuJourModelResource):
    user = fields.ToOneField(
        'website.api.v1.user_resources.UserResource', 'owner')
#    image = fields.ToManyField(ImageResource, 'image_set')
    created_time = fields.DateTimeField(
        attribute='created_time', readonly=True, default=now)
    updated_time = fields.DateTimeField(
        attribute='updated_time', readonly=True, default=now)

    class Meta:
        cache = SimpleCache()
        serializer = TzSerializer()
        detail_uri_name = 'uuid'
        always_return_data = True
        queryset = Collection.objects.filter(is_active=True)
        ordering = ['created_time']
        resource_name = 'collection'
        fields = ['name', 'description']
        detail_allowed_methods = ['get', 'put', 'delete']
        list_allowed_methods = ['get', 'post']
        filtering = {
            "owner": ALL,
        }
        max_limit = 20
        authorization = Authorization()
        include_resource_uri = True

    def dehydrate(self, bundle):
        bundle.data['total_images'] = bundle.obj.total_images()
        bundle.data['total_wordboxes'] = bundle.obj.total_wordboxes()
        bundle.data['image'] = '/v1/image/?' + \
            urlencode({'collection': bundle.data['resource_uri']})
        bundle.data['wordbox'] = '/v1/wordbox/?' + \
            urlencode({'collection': bundle.data['resource_uri']})
        bundle.data['comment'] = '/v1/comment/?' + \
            urlencode({'parent': bundle.data['resource_uri']})
        bundle.data['vote'] = '/v1/vote/?' + \
            urlencode({'parent': bundle.data['resource_uri']})
        return bundle

    def prepend_urls(self):
        return [
            url(str(r"^(?P<resource_name>%s)/(?P<uuid>" + uuid_re.pattern +
                ")/add%s$") % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('add_children'), name="api_get_children"),
            url(str(r"^(?P<resource_name>%s)/(?P<uuid>" + uuid_re.pattern +
                ")/remove%s$") % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('remove_children'), name="api_get_children"),
        ]

    def add_children(self, request, **kwargs):
        try:
            obj = self.cached_obj_get(request=request,
                                      **self.remove_api_resource_names(kwargs))
        except ObjectDoesNotExist:
            return HttpGone()
        except MultipleObjectsReturned:
            return HttpMultipleChoices("More than one resource "
                                       "is found at this URI.")
        if request.method == 'POST':
            data = json.loads(request.POST.items()[0][0])
            if 'image' in data:
                if isinstance(data['image'], list):
                    for URI in data['image']:
                        try:
                            im = Image.objects.get(uuid=uuid_re.search(
                                URI).group())
                            obj.image_set.add(im)
                        except ObjectDoesNotExist:
                            return HttpResponseNotFound(
                                'At least one of the image '
                                'URI\'s cannot be found')
                else:
                    raise ImmediateHttpResponse(response=HttpForbidden(
                        'Image URI\'s must be in an array'))
            if 'wordbox' in data:
                if isinstance(data['wordbox'], list):
                    for URI in data['wordbox']:
                        try:
                            wb = WordBox.objects.get(uuid=uuid_re.search(
                                URI).group())
                            obj.wordbox_set.add(wb)
                        except ObjectDoesNotExist:
                            return HttpResponseNotFound(
                                'At least one of the wordbox '
                                'URI\'s cannot be found')
                else:
                    raise ImmediateHttpResponse(response=HttpForbidden(
                        'Wordbox URI\'s must be in an array'))
        else:
            raise ImmediateHttpResponse(response=HttpResponse(status=405))
        return HttpCreated()

    def remove_children(self, request, **kwargs):
        try:
            obj = self.cached_obj_get(request=request,
                                      **self.remove_api_resource_names(kwargs))
        except ObjectDoesNotExist:
            return HttpGone()
        except MultipleObjectsReturned:
            return HttpMultipleChoices("More than one resource "
                                       "is found at this URI.")
        if request.method == 'POST':
            data = json.loads(request.POST.items()[0][0])
            if 'image' in data:
                if isinstance(data['image'], list):
                    for URI in data['image']:
                        try:
                            im = Image.objects.get(
                                uuid=uuid_re.search(URI).group()
                            )
                            obj.image_set.remove(im)
                        except ObjectDoesNotExist:
                            return HttpResponseNotFound(
                                'At least one of the image '
                                'URI\'s cannot be found')
                else:
                    raise ImmediateHttpResponse(response=HttpForbidden(
                        'Image URI\'s must be in an array'))
            if 'wordbox' in data:
                if isinstance(data['wordbox'], list):
                    for URI in data['wordbox']:
                        try:
                            wb = WordBox.objects.get(uuid=uuid_re.search(
                                URI).group())
                            obj.wordbox_set.remove(wb)
                        except ObjectDoesNotExist:
                            return HttpResponseNotFound(
                                'At least one of the wordbox '
                                'URI\'s cannot be found')
                else:
                    raise ImmediateHttpResponse(response=HttpForbidden(
                        'Wordbox URI\'s must be in an array'))
        else:
            raise ImmediateHttpResponse(response=HttpResponse(status=405))
        return HttpCreated()

    def apply_sorting(self, objects, options=None):
        options = {"order_by": "-created_time"}
        return super(CollectionResource, self).apply_sorting(objects, options)

    # set value of field that is not visible
    def hydrate(self, bundle):
        if hasattr(bundle.obj, 'IPaddress'):
            bundle.obj.IPaddress = bundle.request.META['REMOTE_ADDR']
        return bundle

    def build_filters(self, filters=None):
        if filters is None:
            filters = {}
        orm_filters = super(CollectionResource,
                            self).build_filters(filters)
                            # modify super(*,self)
        if filters:  # check if dictionary is empty or not
            try:
                if "owner" in filters:
                    obj = UserProfile.objects.get(uuid=uuid_re.search(
                        filters['owner']).group())
                    if 'owner__exact' in orm_filters:
                        # delete this field since this is a GFK
                        del orm_filters['owner__exact']
                else:
                    return orm_filters
                if not obj.is_active:
                    return orm_filters
                sqs = obj.collection_set.filter(is_active=True)
                orm_filters["pk__in"] = [i.pk for i in sqs]
            except Collection.DoesNotExist:
                orm_filters["pk__in"] = []
                # return HttpGone()
            except Collection.MultipleObjectsReturned:
                orm_filters["pk__in"] = []
                # return HttpMultipleChoices("More than one resource is found "
                #                            "at this URI.")
                raise ImmediateHttpResponse(response=http.HttpNotFound())
        return orm_filters


class WordBoxResource(DuJourModelResource):
    owner = fields.ToOneField(
        'website.api.v1.user_resources.UserResource', 'owner')
    top_comments = fields.ToManyField(
        'website.api.v1.action_resources.CommentResource',
        attribute=lambda bundle:
        bundle.obj.comment_set.filter(is_active=True).order_by('created_time')
        [0:2], full=True, readonly=True, null=True)
    created_time = fields.DateTimeField(attribute='created_time',
                                        readonly=True)
    updated_time = fields.DateTimeField(attribute='updated_time',
                                        readonly=True)

    def dehydrate(self, bundle):
        bundle.data['username'] = bundle.obj.owner.username
        bundle.data['name'] = bundle.obj.owner.full_name()
        bundle.data['total_votes'] = bundle.obj.total_votes()
        bundle.data['total_comments'] = bundle.obj.total_comments()
        bundle.data['total_collected'] = bundle.obj.userprofile_set.count()
        bundle.data['comment'] = '/v1/comment/?' + \
            urlencode({'parent': bundle.data['resource_uri']})
        bundle.data['vote'] = '/v1/vote/?' + \
            urlencode({'parent': bundle.data['resource_uri']})
        return bundle

    class Meta:
        cache = SimpleCache()
        serializer = TzSerializer()
        detail_uri_name = 'uuid'
        always_return_data = True
        queryset = WordBox.objects.filter(is_active=True)
        ordering = ['created_time']
        resource_name = 'wordbox'
        fields = ['title', 'message']
        detail_allowed_methods = ['get', 'delete', 'patch']
        list_allowed_methods = ['get', 'post']
        filtering = {
            "owner": ALL,
            "total_votes": ALL,
        }
        max_limit = 20
        authorization = Authorization()
        include_resource_uri = True

    def apply_sorting(self, objects, options=None):
        options = {"order_by": "-created_time"}
        return super(WordBoxResource, self).apply_sorting(objects, options)

    # set value of field that is not visible
    def hydrate(self, bundle):
        if hasattr(bundle.obj, 'IPaddress'):
            bundle.obj.IPaddress = bundle.request.META['REMOTE_ADDR']
        return bundle

    def build_filters(self, filters=None):
        if filters is None:
            filters = {}
        orm_filters = super(WordBoxResource, self).build_filters(
            filters)  # modify super(*,self)
        if filters:  # check if dictionary is empty or not
            try:
                if "owner" in filters:
                    obj = UserProfile.objects.get(uuid=uuid_re.search(
                        filters['owner']).group())
                    if 'owner__exact' in orm_filters:
                        # delete this field since this is a GFK
                        del orm_filters['owner__exact']
                elif "community" in filters:
                    obj = Community.objects.get(uuid=uuid_re.search(
                        filters['community']).group())
                elif "collection" in filters:
                    obj = Collection.objects.get(uuid=uuid_re.search(
                        filters['collection']).group())
                else:
                    return orm_filters
                sqs = obj.wordbox_set.filter(is_active=True)
                orm_filters["pk__in"] = [i.pk for i in sqs]
            except WordBox.DoesNotExist:
                orm_filters["pk__in"] = []
                # return HttpGone()
            except WordBox.MultipleObjectsReturned:
                orm_filters["pk__in"] = []
                # return HttpMultipleChoices("More than one resource is found "
                #                            "at this URI.")
                raise ImmediateHttpResponse(response=http.HttpNotFound())
        return orm_filters


class MediaResource(DuJourModelResource):
    class Meta:
        cache = SimpleCache()
        serializer = TzSerializer()
        include_resource_uri = False
        detail_uri_namesss = 'uuid'
        queryset = UserProfile.objects.filter(is_active=True)
        resource_name = 'media'
        ordering = ['created_time']
        fields = ['']
        detail_allowed_methods = []
        list_allowed_methods = ['get']
        max_limit = 20
        filtering = {
            "user": ALL,
        }
        authorization = Authorization()
#        validation = FormValidation()

    def obj_get_list(self, request=None, **kwargs):
        """
        A ORM-specific implementation of ``obj_get_list``.

        Takes an optional ``request`` object, whose ``GET`` dictionary can be
        used to narrow the query.
        """
        filters = {}
        if hasattr(request, 'GET'):
            # Grab a mutable copy.
            filters = request.GET.copy()

        # Update with the provided kwargs.
        filters.update(kwargs)
        if "community" in filters:
            try:
                community = Community.objects.get(
                    uuid=uuid_from_uri(filters['community']))
                im = community.image_set.filter(is_active=True)
                wb = community.wordbox_set.filter(is_active=True)
                base_object_list = sorted(chain(im, wb),
                                          key=attrgetter('created_time'))[::-1]
                return self.apply_authorization_limits(request,
                                                       base_object_list)
            except ValueError:
                raise BadRequest("Invalid resource lookup data provided "
                                 "(mismatched type).")
        else:
            raise BadRequest("Invalid filtering parameter")

    def full_dehydrate(self, bundle):
        """
        Given a bundle with an object instance, extract the information from it
        to populate the resource.
        """
        # Dehydrate each field.
        if bundle.obj.obj_type() == 'image':
            obj = ImageResource()
        elif bundle.obj.obj_type() == 'wordbox':
            obj = WordBoxResource()
        else:
            return bundle
        for field_name, field_object in obj.fields.items():
            try:
                # A touch leaky but it makes URI resolution work.
                if getattr(field_object, 'dehydrated_type', None) == 'related':
                    field_object.api_name = self._meta.api_name
                    field_object.resource_name = obj._meta.resource_name

                bundle.data[field_name] = field_object.dehydrate(bundle)

                # Check for an optional method to do further dehydration.
                method = getattr(obj, "dehydrate_%s" % field_name, None)
            except:
                raise BadRequest("Internal error, possible problem with "
                                 "top_commnets for images")

            if method:
                bundle.data[field_name] = method(bundle)

        bundle = obj.dehydrate(bundle)
        return bundle


class UserCollectionResource(DuJourModelResource):
    class Meta:
        cache = SimpleCache()
        serializer = TzSerializer()
        include_resource_uri = False
        detail_uri_namesss = 'uuid'
        queryset = UserProfile.objects.filter(is_active=True)
        resource_name = 'usercollection'
        ordering = ['created_time']
        fields = ['']
        detail_allowed_methods = []
        list_allowed_methods = ['get']
        max_limit = 20
        filtering = {
            "user": ALL,
        }
        authorization = Authorization()
#        validation = FormValidation()

    def obj_get_list(self, request=None, **kwargs):
        """
        A ORM-specific implementation of ``obj_get_list``.

        Takes an optional ``request`` object, whose ``GET`` dictionary can be
        used to narrow the query.
        """
        filters = {}
        if hasattr(request, 'GET'):
            # Grab a mutable copy.
            filters = request.GET.copy()

        # Update with the provided kwargs.
        filters.update(kwargs)
        if "user" in filters and "media" in filters:
            try:
                image_uuid_list = []
                wordbox_uuid_list = []
                for item in filters['media'].split(','):
                    # use kwarg "resource" field to be more general rather
                    # than take the 2 element
                    try:
                        if item.split('/')[2] == 'image':
                            image_uuid_list.append(uuid_re.findall(item)[0])
                        elif item.split('/')[2] == 'wordbox':
                            wordbox_uuid_list.append(uuid_re.findall(item)[0])
                    except IndexError:
                        raise BadRequest("Invalid uuid or resource URI.")
                userprofile = UserProfile.objects.get(
                    uuid=uuid_from_uri(filters['user']))
                im = userprofile.image_collection_set.filter(
                    is_active=True, uuid__in=image_uuid_list)
                wb = userprofile.wordbox_collection_set.\
                    filter(is_active=True, uuid__in=wordbox_uuid_list)
                base_object_list = sorted(chain(im, wb),
                                          key=attrgetter('created_time'))[::-1]
                return self.apply_authorization_limits(request,
                                                       base_object_list)
            except ValueError:
                raise BadRequest("Invalid resource lookup data provided "
                                 "(mismatched type).")
        elif "user" in filters and len(filters) == 1:
            try:
                userprofile = UserProfile.objects.get(
                    uuid=uuid_from_uri(filters['user']))
                im = userprofile.image_collection_set.filter(is_active=True)
                wb = userprofile.wordbox_collection_set.filter(is_active=True)
                base_object_list = sorted(chain(im, wb),
                                          key=attrgetter('created_time'))[::-1]
                return self.apply_authorization_limits(request,
                                                       base_object_list)
            except ValueError:
                raise BadRequest("Invalid resource lookup data provided "
                                 "(mismatched type).")
        else:
            raise BadRequest("Invalid filtering parameter(s)")

    def full_dehydrate(self, bundle):
        """
        Given a bundle with an object instance, extract the information from it
        to populate the resource.
        """
        # Dehydrate each field.
        if bundle.obj.obj_type() == 'image':
            obj = ImageResource()
        elif bundle.obj.obj_type() == 'wordbox':
            obj = WordBoxResource()
        else:
            return bundle
        for field_name, field_object in obj.fields.items():
            try:
                # A touch leaky but it makes URI resolution work.
                if(getattr(field_object, 'dehydrated_type', None)
                   == 'related'):
                    field_object.api_name = self._meta.api_name
                    field_object.resource_name = obj._meta.resource_name

                bundle.data[field_name] = field_object.dehydrate(bundle)

                # Check for an optional method to do further dehydration.
                method = getattr(obj, "dehydrate_%s" % field_name, None)
            except:
                raise BadRequest("Internal error, possible problem with"
                                 " top_commnets for images")

            if method:
                bundle.data[field_name] = method(bundle)

        bundle = obj.dehydrate(bundle)
        return bundle
