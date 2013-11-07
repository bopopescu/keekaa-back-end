from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q  # Count
from django.core.mail import send_mail
from itertools import chain
from operator import attrgetter
from tastypie.authorization import Authorization
from tastypie.validation import FormValidation
from tastypie import fields
from tastypie.cache import SimpleCache
from tastypie.constants import ALL
from tastypie import http
from tastypie.utils import now
from tastypie.exceptions import NotFound, BadRequest, ImmediateHttpResponse
from website.api.v1.brand_resources import BrandResource, ItemResource, \
    ItemTagResource
from website.api.v1.user_resources import UserResource
from website.api.v1.media_resources import ImageResource, \
    CollectionResource, WordBoxResource, Collection
from website.actions.models import Vote, Comment, CommentForm, Action
from website.brands.models import ItemTag, Brand, Item
from website.media.models import Image, WordBox
from website.users.models import UserProfile
from website.settings import PAGE_BASE_URL, BASE_URL
from website.library.helper_functions import uuid_from_uri
from website.library.validators import uuid_re
from website.library.tastypie_resources import DuJourModelResource,\
    GenericForeignKeyField
from website.library.tastypie_serializers import TzSerializer


GFK_DICT_comment = {Image: ImageResource,
                    Collection: CollectionResource,
                    Brand: BrandResource,
                    Item: ItemResource,
                    ItemTag: ItemTagResource,
                    WordBox: WordBoxResource,
                    UserProfile: UserResource}


class CommentResource(DuJourModelResource):
    # only parent & message can be modified
    parent = GenericForeignKeyField(GFK_DICT_comment, 'parent')
    owner = fields.ToOneField(
        'website.api.v1.user_resources.UserResource', 'owner')
    created_time = fields.DateTimeField(
        attribute='created_time', readonly=True)

    class Meta:
        cache = SimpleCache()
        serializer = TzSerializer()
        include_resource_uri = True
        always_return_data = True
        detail_uri_name = 'uuid'
        queryset = Comment.objects.filter(is_active=True)
        resource_name = 'comment'
        ordering = ['created_time']
        fields = ['message']
        detail_allowed_methods = ['get', 'delete', 'patch']
        list_allowed_methods = ['get', 'post']
        max_limit = 20
        filtering = {
            "parent": ALL,
            "total_votes": ALL,
        }
        authorization = Authorization()
        validation = FormValidation(form_class=CommentForm)

    def dehydrate(self, bundle):
        bundle.data['username'] = bundle.obj.owner.username
        bundle.data['name'] = bundle.obj.owner.full_name()
        bundle.data['total_votes'] = bundle.obj.total_votes
#        bundle.data['total_favorites'] = bundle.obj.total_favorites()

        return bundle

    def apply_sorting(self, objects, options=None):
        options = {"order_by": "-created_time"}
        return super(CommentResource, self).apply_sorting(objects, options)

    def build_filters(self, filters=None):
        if filters is None:
            filters = {}
        orm_filters = super(CommentResource, self).build_filters(
            filters)  # modify super(*,self)
        if 'parent__exact' in orm_filters:
            del orm_filters['parent__exact']
                # delete this field since this is a GFK
#        else:
#            raise ImmediateHttpResponse(response=http.HttpNotFound())

        if "parent" in filters:
            try:
                obj = self.fields['parent'].build_related_resource(
                    filters['parent']).obj
                if not obj.is_active:
                    raise NotFound("Parent object does not exist")
                sqs = obj.comment_set.filter(is_active=True)
                orm_filters["pk__in"] = [i.pk for i in sqs]
            except Comment.DoesNotExist:
                orm_filters["pk__in"] = []
                # return HttpGone()
            except Comment.MultipleObjectsReturned:
                orm_filters["pk__in"] = []
                # return HttpMultipleChoices("More than one resource is found "
                #                            "at this URI.")
                raise ImmediateHttpResponse(response=http.HttpNotFound())
        return orm_filters

    # set value of field that is not visible
    # remove fields that should cannot be changed
    def hydrate(self, bundle):
        if hasattr(bundle.obj, 'IPaddress'):
            bundle.obj.IPaddress = bundle.request.META['REMOTE_ADDR']
        return bundle

    def obj_create(self, bundle, request=None, **kwargs):
        bundle = super(CommentResource, self).obj_create(bundle,
                                                         request=request,
                                                         **kwargs)
        # email owner whos photo was commented on
        if bundle.obj.parent.obj_type() == 'image':
            parent_owner = bundle.obj.parent.owner
            comment_owner = bundle.obj.owner
            if parent_owner != comment_owner:
                media_url = u'{page_base_url}image/{uuid}'.format(
                    page_base_url=PAGE_BASE_URL,
                    uuid=bundle.obj.parent.uuid)
                comment_owner_url = u'{base_url}{comment_owner}'.format(
                    base_url=BASE_URL,
                    comment_owner=comment_owner.username)
                # send email to the owner of the image
                send_mail(u'Dujour: New comment on your photo!',
                          u'Hi {parent_owner}!\n\n'.format(
                              parent_owner=parent_owner.first_name) +
                          u'{comment_owner} commented on your photo at '
                          u'{media_url}.\n\n'.format(
                              comment_owner=comment_owner.first_name,
                              media_url=media_url) +
                          u'\t \"{comment}\"\n\n'.format(
                              comment=bundle.obj.message) +
                          u'Take a look at {comment_owner}\'s profile here:'
                          u'{comment_owner_url}\n\n'.format(
                              comment_owner=comment_owner.first_name,
                              comment_owner_url=comment_owner_url) +
                          u'- Dujour Team',
                          u'noreply@dujour.im',
                          [str(parent_owner.email)],
                          fail_silently=False)
        # email user whose wall was commented on
        elif bundle.obj.parent.obj_type() == 'userprofile':
            user = bundle.obj.parent
            comment_owner = bundle.obj.owner
            if user != comment_owner:
                wall_url = u'{base_url}{user}'.format(
                    base_url=BASE_URL, user=user.username)
                comment_owner_url = u'{base_url}{comment_owner}'.format(
                    base_url=BASE_URL,
                    comment_owner=comment_owner.username)
                # send email to the owner of the image
                send_mail(u'Dujour: New comment on your wall!',
                          u'Hi {user}!\n\n'.format(user=user.first_name) +
                          u'{comment_owner} commented on your wall at'
                          u'{wall_url}.\n\n'.format(
                              comment_owner=comment_owner.first_name,
                              wall_url=wall_url) +
                          u'\t \"{comment}\"\n\n'.format(
                              comment=bundle.obj.message) +
                          u'Take a look at {comment_owner}\'s profile here:'
                          u'{comment_owner_url}\n\n'.format(
                              comment_owner=comment_owner.first_name,
                              comment_owner_url=comment_owner_url) +
                          u'- Dujour Team',
                          u'noreply@dujour.im',
                          [str(user.email)],
                          fail_silently=False)
        return bundle

    def hydrate_owner(self, bundle):
        # WARNING - makes sure user is authorized
        # first for this may cause problems
        bundle.obj.owner = User.objects.get(
            pk=bundle.request.user.id).get_profile()
        bundle.data['owner'] = None
        return bundle


# add CommentResource to GFK dictionary for VoteResource
GFK_DICT_vote = {Image: ImageResource,
                 Collection: CollectionResource,
                 Brand: BrandResource,
                 Item: ItemResource,
                 ItemTag: ItemTagResource,
                 WordBox: WordBoxResource,
                 Comment: CommentResource}


class VoteResource(DuJourModelResource):
    created_time = fields.DateTimeField(
        attribute='created_time', readonly=True)
    parent = GenericForeignKeyField(GFK_DICT_vote, 'parent')
    owner = fields.ToOneField('website.api.v1.user_resources.UserResource',
                              'owner', readonly=True)

    class Meta:
        always_return_data = True
        authorization = Authorization()
        cache = SimpleCache()
        #cache_control = {"max_age": 60*1}
        detail_allowed_methods = ['get', 'delete']
        detail_uri_name = 'uuid'
        fields = ['created_time']
        filtering = {
            "parent": ALL,
            "owner": ALL,
            "total_votes": ALL,
        }
        include_resource_uri = True
        list_allowed_methods = ['get', 'post']
        max_limit = 20
        ordering = ['created_time']
        queryset = Vote.objects.all()  # filter(is_active=True)
        resource_name = 'vote'
        serializer = TzSerializer()

    def dehydrate(self, bundle):
        bundle.data['username'] = bundle.obj.owner.username
        bundle.data['name'] = bundle.obj.owner.full_name()
        return bundle

    def apply_sorting(self, objects, options=None):
        options = {"order_by": "-created_time"}
        return super(VoteResource, self).apply_sorting(objects, options)

    def build_filters(self, filters=None):
        if filters is None:
            filters = {}
        orm_filters = super(VoteResource, self).build_filters(
            filters)  # modify super(*,self)
        if 'parent__exact' in orm_filters:
            del orm_filters['parent__exact']
                # delete this field since this is a GFK
        if 'owner__exact' in orm_filters:
            del orm_filters['owner__exact']
                # delete this field since this is a GFK
        if "parent" in filters and "owner" in filters:
            try:
                parent_type = filters['parent'].split(';')[0].split('/')[2]
                parent_uuid_list = uuid_re.findall(filters['parent'])
                parent_model = ContentType.objects.get(
                    model=parent_type).model_class()
                parent = parent_model.objects.filter(
                    is_active=True, uuid__in=parent_uuid_list)
                user = UserProfile.objects.get(uuid=uuid_re.search(
                    filters['owner']).group())
                if not user.is_active:
                    return orm_filters
                Qparent = Q(content_type__model=parent_type,
                            object_id__in=[p.pk for p in parent])
                sqs = user.vote_set.filter(Q(is_active=True), Qparent)
                orm_filters["pk__in"] = [i.pk for i in sqs]
            except Vote.DoesNotExist:
                orm_filters["pk__in"] = []  # return HttpGone()
            except Vote.MultipleObjectsReturned:
                orm_filters["pk__in"] = []
                raise ImmediateHttpResponse(response=http.HttpNotFound())
        elif "parent" in filters:
#        elifs: # dual filter, supports multiple parents
            try:
                obj = self.fields['parent'].build_related_resource(
                    filters['parent']).obj
                if not obj.is_active:
                    return orm_filters
                sqs = obj.vote_set.filter(is_active=True)
                orm_filters["pk__in"] = [i.pk for i in sqs]
            except Vote.DoesNotExist:
                orm_filters["pk__in"] = []  # return HttpGone()
            except Vote.MultipleObjectsReturned:
                orm_filters["pk__in"] = []
                raise ImmediateHttpResponse(response=http.HttpNotFound())
        return orm_filters

    # set custom value of field that is visible
    def hydrate_owner(self, bundle):
        ## WARNING (DB) -
        # makes sure user is authorized first for this may cause problems
        bundle.obj.owner = User.objects.get(
            pk=bundle.request.user.id).get_profile()
        bundle.data['owner'] = None
        return bundle

    def hydrate(self, bundle):
        if hasattr(bundle.obj, 'IPaddress'):
            bundle.obj.IPaddress = bundle.request.META['REMOTE_ADDR']
        return bundle

    def obj_create(self, bundle, request=None, **kwargs):
        try:
            userProfile = User.objects.get(
                pk=bundle.request.user.id).get_profile()
        except:
            raise ImmediateHttpResponse(response=http.HttpNotFound())
        try:
            obj = self.fields['parent'].build_related_resource(
                bundle.data['parent']).obj
        except:
            raise ImmediateHttpResponse(response=http.HttpNotFound())
        if obj.vote_set.filter(owner_id=userProfile.pk).exists():
            bundle.obj = obj.vote_set.get(owner_id=userProfile.pk)
            if bundle.obj.is_active is not True:
                bundle.obj.IPaddress = bundle.request.META['REMOTE_ADDR']
                bundle.obj.is_active = True
                bundle.obj.created_time = now()
        else:
            bundle.obj.parent = obj
            bundle.obj.IPaddress = bundle.request.META['REMOTE_ADDR']
            bundle.obj.owner = userProfile
        if hasattr(bundle.obj, 'total_votes'):
            bundle.obj.total_votes = bundle.obj.total_votes()
        bundle.obj.save()
        # email owner of the image that this vote modifies
        if bundle.obj.parent.obj_type() == 'image':
            parent_owner = bundle.obj.parent.owner
            vote_owner = bundle.obj.owner
            if parent_owner != vote_owner:
                media_url = u'{page_base_url}image/{uuid}'.format(
                    page_base_url=PAGE_BASE_URL,
                    uuid=bundle.obj.parent.uuid)
                vote_owner_url = u'{base_url}{vote_owner}'.format(
                    base_url=BASE_URL,
                    vote_owner=vote_owner.username)
                # send email to the owner of the image
                send_mail(u'Dujour: New vote on your photo!',
                          u'Hi {parent_owner}!\n\n'.format(
                              parent_owner=parent_owner.first_name) +
                          u'{vote_owner} voted on your photo at'
                          u'{media_url}.\n\n'.format(
                              vote_owner=vote_owner.first_name,
                              media_url=media_url) +
                          u'Take a look at {vote_owner}\'s profile here:'
                          u'{vote_owner_url}\n\n'.format(
                              vote_owner=vote_owner.first_name,
                              vote_owner_url=vote_owner_url) +
                          u'- Dujour Team',
                          u'noreply@dujour.im',
                          [str(parent_owner.email)],
                          fail_silently=False)
        return bundle

    def obj_delete(self, request=None, **kwargs):
        obj = kwargs.pop('_obj', None)
        if not hasattr(obj, 'delete'):
            try:
                obj = self.obj_get(request, **kwargs)
            except ObjectDoesNotExist:
                raise NotFound('A model instance matching the provided'
                               'arguments could not be found.')
        obj.is_active = False
        if hasattr(obj, 'total_votes'):
            obj.total_votes = obj.total_votes()
        obj.save()


class NewsfeedResource(DuJourModelResource):
    # only parent & message can be modified
    user = fields.ToOneField(
        'website.api.v1.user_resources.UserResource', 'user')

    class Meta:
        cache = SimpleCache()
        serializer = TzSerializer()
        #cache_control = {"max_age": 60*1}
        include_resource_uri = False
        detail_uri_name = 'uuid'
        queryset = Action.objects.filter(is_active=True)
        resource_name = 'newsfeed'
        ordering = ['created_time']
        fields = ['message']
        detail_allowed_methods = []
        list_allowed_methods = ['get']
        max_limit = 20
        filtering = {
            "owner": ALL,
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
        try:
            user = UserProfile.objects.filter(
                uuid=uuid_from_uri(filters['user']))
            sub_pk = sorted(chain(user[0].subscriptions(), user))
            im = Image.objects.filter(is_active=True, owner__in=sub_pk)
            wb = WordBox.objects.filter(is_active=True, owner__in=sub_pk)
            # sort reverse chronologically
            base_object_list = sorted(chain(im, wb),
                                      key=attrgetter('created_time'))[::-1]
            return self.apply_authorization_limits(request, base_object_list)
        except ValueError:
            raise BadRequest('Invalid resource lookup data provided'
                             '(mismatched type).')

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

                if method:
                    bundle.data[field_name] = method(bundle)
            except:
                if field_name == 'versions':
                    raise NotFound('imageversion not found'
                                   'for this image (pk=%s' +
                                   str(bundle.obj.pk) + " uuid=%s" +
                                   str(bundle.obj.uuid) + ")")
                else:
                    raise NotFound('Error with field \"%s\"'
                                   'in resource \"%s\"' %
                                   (field_name, bundle.obj.obj_type()))

        bundle = obj.dehydrate(bundle)
        return bundle
