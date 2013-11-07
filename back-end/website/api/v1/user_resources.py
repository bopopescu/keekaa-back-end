import simplejson
import json

from django.contrib.auth import login as auth_login, \
    logout as auth_logout, authenticate as auth_authenticate
from django.contrib.auth.models import User as DjangoUser
from django.core.exceptions import ObjectDoesNotExist, \
    MultipleObjectsReturned
from django.db import models
from django.db.models import Count
from django.http import HttpResponse, HttpResponseNotFound
from itertools import chain
from operator import attrgetter
from registration.backends import get_backend
from tastypie import fields
from tastypie import http
from tastypie.http import HttpGone, HttpMultipleChoices
from tastypie.authorization import Authorization
from tastypie.constants import ALL
from tastypie.cache import SimpleCache
from tastypie.exceptions import ImmediateHttpResponse, BadRequest
from tastypie.http import HttpForbidden, HttpCreated
from tastypie.utils import trailing_slash
from tastypie.fields import ListField
from tastypie.utils import now
from tastypie.models import create_api_key
from urllib import urlencode
from website.library.helper_functions import uuid_from_uri
from website.library.validators import get_match_name, uuid_re, email_re, \
    username_re
from django.conf.urls.defaults import url
from website.library import accounts as account_library
from website.library.tastypie_resources import DuJourModelResource
from website.library.tastypie_serializers import TzSerializer
from website.media.models import Image, WordBox
from website.users.models import UserProfile, Friendship, Community, \
    CommunityCategory, CommunityMembership, UserSubscription
from website.actions.models import Vote, Comment

# A signal function you can use to auto-create Tastypie api key
models.signals.post_save.connect(create_api_key, sender=DjangoUser)


class UserResource(DuJourModelResource):
    profile_image_thumbnail = fields.OneToOneField(
        'website.api.v1.media_resources.ImageResource',
        'profile_image_thumbnail', full=True, null=True)
    profile_image_standard = fields.OneToOneField(
        'website.api.v1.media_resources.ImageResource',
        'profile_image_standard', full=True, null=True)
    created_time = fields.DateTimeField(
        attribute='created_time', readonly=True, default=now)
    updated_time = fields.DateTimeField(
        attribute='updated_time', readonly=True, default=now)
    age = fields.IntegerField(attribute='age')

    class Meta:
        always_return_data = True
        authorization = Authorization()
        cache = SimpleCache()
        #cache_control = [public,{ "max_age": 60*10}]
        detail_allowed_methods = ['get', 'post', 'patch']
        detail_uri_name = 'uuid'
        fields = ['username', 'about_me', 'fashion_statement', 'gender',
                  'first_name', 'last_name', 'middle_name', 'email', 'website',
                  'location']
        filtering = {"community": ALL}
        include_resource_uri = True
        list_allowed_methods = ['get', 'post']
        queryset = UserProfile.objects.filter(is_active=True).distinct()
        resource_name = 'user'
        serializer = TzSerializer()

    def dehydrate(self, bundle):
        bundle.data['total_subscribers'] = bundle.obj.total_subscribers()
        bundle.data['total_images'] = bundle.obj.total_images()
        bundle.data['name'] = bundle.obj.full_name()
        bundle.data['total_wordboxes'] = bundle.obj.total_wordboxes()
        bundle.data['community'] = '/v1/community/?' + urlencode({
            'member': bundle.data['resource_uri']})
        return bundle

        # Sign Up
    def obj_create(self, bundle, request=None, **kwargs):
        if not (u'username' in bundle.data and u'first_name' in bundle.data
                and u'last_name' in bundle.data and u'email' in bundle.data
                and u'password' in bundle.data):
            raise ImmediateHttpResponse(response=HttpResponse(status=400))

        backend = get_backend('registration.backends.default.DefaultBackend')
        if not backend.registration_allowed(request):
            raise ImmediateHttpResponse(response=HttpResponse(status=410))

        form_class = backend.get_form_class(request)
        username = bundle.data[u'username']
        email = bundle.data[u'email']
        first_name = bundle.data[u'first_name']
        last_name = bundle.data[u'last_name']
        password = bundle.data[u'password']

        # The username doesn't match r'@([A-Za-z0-9_]+)'
        if not username_re.search(username):
            raise ImmediateHttpResponse(response=HttpResponse(status=461))
        # The username already exists
        if not account_library.check_name_available(username):
            raise ImmediateHttpResponse(response=HttpResponse(status=462))
        if not email_re.search(email):  # This email is not valid
            raise ImmediateHttpResponse(response=HttpResponse(status=463))
        # The email already exists
        if not account_library.check_email_available(email):
            raise ImmediateHttpResponse(response=HttpResponse(status=464))
        data = {'username': username, 'email': email, 'first_name': first_name,
                'last_name': last_name, 'password1': password,
                'password2': password}
        form = form_class(data)
        if form.is_valid():
            new_user = backend.register(request, first_name,
                                        last_name, **form.cleaned_data)
            new_user.username = account_library.get_matched_name(username)
            new_user.first_name = first_name
            new_user.last_name = last_name
            new_user.is_active = False
            new_user.save()
            bundle = super(UserResource, self).obj_create(
                bundle, request=None, **kwargs)
            bundle.obj.user = new_user
            bundle.obj.save()
        else:
            raise ImmediateHttpResponse("Unknown Error",
                                        response=HttpResponse(status=400))
        return bundle

    def build_filters(self, filters=None):
        if filters is None:
            filters = {}
        orm_filters = super(UserResource, self).build_filters(
            filters)  # modify super(*,self)
        if filters:  # check if dictionary is empty or not
            try:
                if "community" in filters:
                    obj = Community.objects.get(uuid=uuid_re.search(
                        filters['community']).group())
                    if 'community_set__exact' in orm_filters:
                        # delete this field since this is a GFK
                        del orm_filters['community_set__exact']
                    if not obj.is_active:
                        return orm_filters
                    sqs = obj.member_set.filter(is_active=True)
                elif "subscriber" in filters:
                    obj = UserProfile.objects.get(uuid=uuid_re.search(
                        filters['subscriber']).group())
                    if not obj.is_active:
                        return orm_filters
                    sqs = obj.to_subscribers.filter(is_active=True)
                else:
                    return orm_filters
                orm_filters["pk__in"] = [i.pk for i in sqs]
            except UserProfile.DoesNotExist:
                    orm_filters["pk__in"] = []  # return HttpGone()
        return orm_filters

    def prepend_urls(self):
        return [
            url(str(r"^(?P<resource_name>%s)/(?P<uuid>" + uuid_re.pattern +
                    ")/add_to_collection%s$") %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('add_children'), name="api_get_children"),
            url(str(r"^(?P<resource_name>%s)/(?P<uuid>" + uuid_re.pattern +
                    ")/remove_from_collection%s$") %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('remove_children'), name="api_get_children"),
        ]

    def add_children(self, request, **kwargs):
        try:
            obj = self.cached_obj_get(request=request,
                                      **self.remove_api_resource_names(kwargs))
        except ObjectDoesNotExist:
            return HttpGone()
        except MultipleObjectsReturned:
            return HttpMultipleChoices(
                "More than one resource is found at this URI.")
        if request.method == 'POST':
            data = json.loads(request.POST.items()[0][0])
            if 'image' in data:
                if isinstance(data['image'], list):
                    for URI in data['image']:
                        try:
                            im = Image.objects.get(uuid=uuid_re.search(
                                URI).group())
                            obj.image_collection_set.add(im)
                        except ObjectDoesNotExist:
                            return HttpResponseNotFound(
                                'At least one of the image URI\'s cannot be \
                                found'
                            )
                else:
                    raise ImmediateHttpResponse(response=HttpForbidden(
                        'Image URI\'s must be in an array'))
            if 'wordbox' in data:
                if isinstance(data['wordbox'], list):
                    for URI in data['wordbox']:
                        try:
                            wb = WordBox.objects.get(uuid=uuid_re.search(
                                URI).group())
                            obj.wordbox_collection_set.add(wb)
                        except ObjectDoesNotExist:
                            return HttpResponseNotFound(
                                'At least one of the wordbox URI\'s cannot be \
                                found')
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
            return HttpMultipleChoices("More than one resource is found at \
                                       this URI.")
        if request.method == 'POST':
            data = json.loads(request.POST.items()[0][0])
            if 'image' in data:
                if isinstance(data['image'], list):
                    for URI in data['image']:
                        try:
                            im = Image.objects.get(uuid=uuid_re.search(
                                URI).group())
                            obj.image_collection_set.remove(im)
                        except ObjectDoesNotExist:
                            return HttpResponseNotFound(
                                'At least one of the image URI\'s cannot be \
                                found')
                else:
                    raise ImmediateHttpResponse(response=HttpForbidden(
                        'Image URI\'s must be in an array'))
            if 'wordbox' in data:
                if isinstance(data['wordbox'], list):
                    for URI in data['wordbox']:
                        try:
                            wb = WordBox.objects.get(uuid=uuid_re.search(
                                URI).group())
                            obj.wordbox_collection_set.remove(wb)
                        except ObjectDoesNotExist:
                            return HttpResponseNotFound(
                                'At least one of the wordbox URI\'s cannot be \
                                found')
                else:
                    raise ImmediateHttpResponse(response=HttpForbidden(
                        'Wordbox URI\'s must be in an array'))
        else:
            raise ImmediateHttpResponse(response=HttpResponse(status=405))
        return HttpCreated()


# Be carefull to modify this resouce,
# since it can directly access to Django User object
# which contains the hashed password!!!
class UsernameResource(DuJourModelResource):
    user_profile = fields.ToManyField(
        UserResource, attribute=lambda bundle: UserProfile.objects.filter(
            user=bundle.obj, is_active=True), full=False)

    class Meta:
        cache = SimpleCache()
        serializer = TzSerializer()
        queryset = DjangoUser.objects.filter(is_active=True)
        resource_name = 'username'
        list_allowed_methods = []
        detail_allowed_methods = ['get']
       # cache_control = {"public": True,"max_age": 1}
        include_resource_uri = False

    def dehydrate(self, bundle):
        if len(bundle.data['user_profile']) > 0:
            bundle.data = {'user': bundle.data['user_profile'][0]}
        else:
            raise ImmediateHttpResponse(response=http.HttpNotFound())
        return bundle

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<username>.+)/$" %
                self._meta.resource_name, self.wrap_view('dispatch_detail'),
                name="api_dispatch_detail"),
        ]

    def dispatch(self, request_type, request, **kwargs):
        if 'username' in kwargs:
            if(username_re.search(kwargs['username'])):
                kwargs['username'] = get_match_name(kwargs['username'])
            else:
                raise ImmediateHttpResponse(response=http.HttpNotFound())
        return super(UsernameResource, self).dispatch(request_type, request,
                                                      **kwargs)


class EmailResource(DuJourModelResource):
    user_profile = fields.ToManyField(
        UserResource, attribute=lambda bundle: UserProfile.objects.filter(
            user=bundle.obj, is_active=True), full=False)

    class Meta:
        cache = SimpleCache()
        serializer = TzSerializer()
        queryset = DjangoUser.objects.filter(is_active=True)
        resource_name = 'email'
        list_allowed_methods = []
        detail_allowed_methods = ['get']
        #cache_control = {"max_age": 60*48}
        include_resource_uri = False

    def dehydrate(self, bundle):
        if len(bundle.data['user_profile']) > 0:
            bundle.data = {'user': bundle.data['user_profile'][0]}
        else:
            raise ImmediateHttpResponse(response=http.HttpNotFound())
        return bundle

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<email>.+)/$" %
                self._meta.resource_name, self.wrap_view('dispatch_detail'),
                name="api_dispatch_detail"),
        ]

    def dispatch(self, request_type, request, **kwargs):
        if 'email' in kwargs:
            if not email_re.search(kwargs['email']):
                raise ImmediateHttpResponse(response=http.HttpNotFound())
        return super(EmailResource, self).dispatch(request_type, request,
                                                   **kwargs)


class MeResource(DuJourModelResource):
    user_profile = fields.ToManyField(
        UserResource, attribute=lambda bundle: UserProfile.objects.filter(
            user=bundle.obj, is_active=True), full=False)

    class Meta:
       # cache = SimpleCache()
        serializer = TzSerializer()
        queryset = DjangoUser.objects.filter(is_active=True)
        resource_name = 'me'
        list_allowed_methods = []
        fields = []
        detail_allowed_methods = ['get', 'delete']
        authorization = Authorization()
        include_resource_uri = True

    def dehydrate(self, bundle):
        if len(bundle.data['user_profile']) > 0:
            bundle.data = {'user': bundle.data['user_profile'][0]}
        else:
            raise ImmediateHttpResponse(response=http.HttpNotFound())
        return bundle

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/$" %
                self._meta.resource_name, self.wrap_view('dispatch_detail'),
                name="api_dispatch_detail"),
        ]

    def obj_get(self, request=None, **kwargs):
        # The following is the code for sign in.
        if (u'user' in request.GET and u'password' in request.GET):
            auth_logout(request)
            username = request.GET['user']
            password = request.GET['password']
            # If username is an email address, then try to pull it up first
            if email_re.search(username):
                try:
                    user = DjangoUser.objects.get(email=username)
                except:
                    raise ImmediateHttpResponse(response=http.HttpNotFound())
            # This is a real username, so try username instead
            elif username_re.search(username):
                username = account_library.get_matched_name(username)
                try:
                    user = DjangoUser.objects.get(username=username)
                except:
                    raise ImmediateHttpResponse(response=http.HttpNotFound())
            else:
                raise ImmediateHttpResponse(response=http.HttpNotFound())

            # Return 404 if we can not identify the user.
            if user is None:
                raise ImmediateHttpResponse(response=http.HttpNotFound())

            ## Hgj9Ek and hGJ9ek can be both valid password
            for i in [1, 2]:
                if i is 2:
                    password = password.swapcase()
                auth_login_user = auth_authenticate(
                    username=user.username, password=password)
                if auth_login_user is not None:
                    if user.is_active:
                        auth_login(request, auth_login_user)
                        #check_user_profile_exist
                        #_and_create_one_if_not_exist(user)
                        if request.session.test_cookie_worked():
                            request.session.delete_test_cookie()
                        if u'stay_signed_in' in request.GET:
                            if cmp(request.GET['stay_signed_in'], u'True'):
                                request.session.set_expiry(0)
                        break
                    else:  # Disabled account (403 error)
                        raise ImmediateHttpResponse(
                            response=http.HttpForbidden())

            if request.user.is_authenticated():
                kwargs['pk'] = request.user.pk
            else:  # Can not get session, password is wrong.(401 Unauthorized)
                raise ImmediateHttpResponse(response=http.HttpUnauthorized())
        else:
            # Get user's uri when we access this api without any parameter.
            if request.user.is_authenticated():
                kwargs['pk'] = request.user.pk
            else:  # If not signed in, return (401 Unauthorized) error
                raise ImmediateHttpResponse(response=http.HttpUnauthorized())

        return super(MeResource, self).obj_get(request=None, **kwargs)

    def obj_delete(self, request=None, **kwargs):
        #import pdb; pdb.set_trace()
        if request.user.is_authenticated():
            auth_logout(request)
            raise ImmediateHttpResponse(response=http.HttpNoContent())
        else:
            auth_logout(request)
            raise ImmediateHttpResponse(response=http.HttpUnauthorized())


class FriendshipResource(DuJourModelResource):
    # only parent & message can be modified
    user1 = fields.ToOneField(UserResource, 'from_user')
    user2 = fields.ToOneField(UserResource, 'to_user')

    class Meta:
        cache = SimpleCache()
        serializer = TzSerializer()
        detail_uri_name = 'uuid'
        queryset = Friendship.objects.filter(is_active=True)
        resource_name = 'friend'
        ordering = []
        fields = ['user']
        list_allowed_methods = ['get', 'post', 'delete']
        detail_allowed_methods = ['get', 'delete']
        max_limit = 20
        filtering = {
            "user": ALL,
        }
        authorization = Authorization()
#        validation = FormValidation(form_class=CommentForm)
        include_resource_uri = True

    def dehydrate(self, bundle):
        obj = self.fields['user1'].build_related_resource(
            bundle.request.GET['user']).obj
        if bundle.obj.from_user == obj:
            bundle.data['friend'] = self.fields[
                'user2'].hydrate(bundle).data['resource_uri']
        else:
            bundle.data['friend'] = self.fields[
                'user1'].hydrate(bundle).data['resource_uri']
        if 'user2' in bundle.data:
            del bundle.data['user2']
        if 'user1' in bundle.data:
            del bundle.data['user1']
        return bundle

#    def apply_sorting(self, objects, options=None):
#        options = {"order_by":"-created_time"}
#        return super(FriendshipResource, self).apply_sorting(objects, options)

    def build_filters(self, filters=None):
        if filters is None:
            filters = {}
        orm_filters = super(FriendshipResource, self).build_filters(
            filters)  # modify super(*,self)
        if 'user1__exact' in orm_filters:
            del orm_filters['user1__exact']
                # delete this field since this is a GFK
        else:
            raise ImmediateHttpResponse(response=http.HttpNotFound())
        if "user" in filters:
            try:
                obj = self.fields['user2'].build_related_resource(
                    filters['user']).obj
                if not obj.is_active:
                    return orm_filters
                sqs = obj.to_friendships.filter(
                    was_accepted=True,
                    to_user__is_active=True) | obj.from_friendships.filter(
                        was_accepted=True, from_user__is_active=True)
                orm_filters["pk__in"] = [i.pk for i in sqs]
            except Friendship.DoesNotExist:
                orm_filters["pk__in"] = []  # return HttpGone()
            except Friendship.MultipleObjectsReturned:
                # return HttpMultipleChoices("More than one resource is
                #                             found at this URI.")
                orm_filters["pk__in"] = []
                raise ImmediateHttpResponse(response=http.HttpNotFound())
        return orm_filters

    # set value of field that is not visible
    def hydrate(self, bundle):
        if hasattr(bundle.obj, 'IPaddress'):
            bundle.obj.IPaddress = bundle.request.META['REMOTE_ADDR']
        return bundle

    def obj_create(self, bundle, request=None, **kwargs):
        # check if this friendship already exists not or if it's active
        user1 = self.fields['user1'].hydrate(bundle).obj
        user2 = self.fields['user2'].hydrate(bundle).obj
        try:
            f = user1.to_friendships.get(was_accepted=True, to_user=user2)
        except:
            try:
                f = user1.from_friendships.get(
                    was_accepted=True, from_user=user2)
            except:
                return super(FriendshipResource, self).obj_create(
                    bundle, request=None, **kwargs)
        if f.is_active:
            raise BadRequest('This friendship already exists!')
        else:
            f.is_active = True
            f.save()
            return bundle
#        friends = self.fields['to_user'].hydrate(bundle).obj.friends()
#        user.from_friendships.filter(is_active=True, was_accepted=True)
#        if user in friends:
#            raise BadRequest('This friendship already exists!')
#        else:
#            return super(FriendshipResource, self).obj_create(
#               bundle, request=None, **kwargs)


class CommunityResource(DuJourModelResource):
    tag = ListField(readonly=True)
    creator = fields.ToOneField(UserResource, 'creator')
    profile_image_thumbnail = fields.OneToOneField(
        'website.api.v1.media_resources.ImageResource',
        'profile_image_thumbnail', full=True, null=True)
    profile_image_standard = fields.OneToOneField(
        'website.api.v1.media_resources.ImageResource',
        'profile_image_standard', full=True, null=True)
#    member = fields.ToManyField(UserResource, 'member_set', readonly=True)
    created_time = fields.DateTimeField(
        attribute='created_time', readonly=True, default=now)
    updated_time = fields.DateTimeField(
        attribute='updated_time', readonly=True, default=now)
#    total_posts = fields.IntegerField(attribute='total_posts', readonly=True)
#    image = fields.ToManyField(ImageResource, 'image_set', readonly=True)
#    wordbox = fields.ToManyField(WordBoxResource,'wordbox_set',readonly=True)

    class Meta:
        cache = SimpleCache()
        serializer = TzSerializer()
        detail_uri_name = 'uuid'
        always_return_data = True
        # annotate -> so we can order by total_images
        queryset = Community.objects.filter(is_active=True).annotate(
            total_p=Count('image_set')).order_by('-total_p')
        resource_name = 'community'
        fields = ['name', 'description', 'total_posts']
        detail_allowed_methods = ['get', 'delete', 'patch']
        list_allowed_methods = ['get', 'post']
        max_limit = 20
        ordering = ['created_time']
        authorization = Authorization()
        include_resource_uri = True

    def dehydrate(self, bundle):
        bundle.data['total_images'] = bundle.obj.total_images()
        bundle.data['total_wordboxes'] = bundle.obj.total_wordboxes()
        bundle.data['total_members'] = bundle.obj.total_members()
        bundle.data['total_communitycategories'] = \
            bundle.obj.communitycategory_set.count()
        bundle.data['image'] = '/v1/image/?' + urlencode({
            'community': bundle.data['resource_uri']})
        bundle.data['wordbox'] = '/v1/wordbox/?' + urlencode({
            'community': bundle.data['resource_uri']})
        bundle.data['comment'] = '/v1/comment/?' + urlencode({
            'parent': bundle.data['resource_uri']})
        bundle.data['vote'] = '/v1/vote/?' + \
            urlencode({'parent': bundle.data['resource_uri']})
        bundle.data['member'] = '/v1/user/?' + urlencode({
            'community': bundle.data['resource_uri']})
        bundle.data['communitycategory'] = '/v1/communitycategory/?' + \
            urlencode({'community': bundle.data['resource_uri']})
        return bundle

    def dehydrate_tag(self, bundle):
        return map(str, bundle.obj.tags.all())

    def prepend_urls(self):
        return [
            # add images/wordboxes
            url(str(r"^(?P<resource_name>%s)/(?P<uuid>" + uuid_re.pattern +
                    ")/add%s$") % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('add_children'), name="api_get_children"),
            # remove images/wordboxes
            url(str(r"^(?P<resource_name>%s)/(?P<uuid>" + uuid_re.pattern +
                    ")/remove%s$") %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('remove_children'), name="api_get_children"),
            # add tags
            url(str(r"^(?P<resource_name>%s)/(?P<uuid>" + uuid_re.pattern +
                    ")/add_tag%s$") %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('add_tag'), name="api_get_children"),
            # remove tags
            url(str(r"^(?P<resource_name>%s)/(?P<uuid>" + uuid_re.pattern +
                    ")/remove_tag%s$") %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('remove_tag'), name="api_get_children"),
            # set tags
            url(str(r"^(?P<resource_name>%s)/(?P<uuid>" + uuid_re.pattern +
                    ")/set_tag%s$") %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('set_tag'), name="api_get_children"),
        ]

    def set_tag(self, request, **kwargs):
        try:
            obj = self.cached_obj_get(request=request,
                                      **self.remove_api_resource_names(kwargs))
        except ObjectDoesNotExist:
            return HttpGone()
        except MultipleObjectsReturned:
            return HttpMultipleChoices("More than one resource is found at \
                                       this URI.")
        if request.method == 'POST':
            data = json.loads(request.POST.items()[0][0])
            if 'tag' in data:
                if isinstance(data['tag'], list):
                    obj.tags.clear()
                    for tag in data['tag']:
                        obj.tags.add(tag)
                else:
                    raise ImmediateHttpResponse(response=HttpForbidden(
                        'Tag must be an array of tag strings'))
        else:
            raise ImmediateHttpResponse(response=HttpResponse(status=405))
        return HttpCreated()

    def add_tag(self, request, **kwargs):
        try:
            obj = self.cached_obj_get(request=request,
                                      **self.remove_api_resource_names(kwargs))
        except ObjectDoesNotExist:
            return HttpGone()
        except MultipleObjectsReturned:
            return HttpMultipleChoices("More than one resource is found at \
                                       this URI.")
        if request.method == 'POST':
            data = json.loads(request.POST.items()[0][0])
            if 'tag' in data:
                if isinstance(data['tag'], list):
                    for tag in data['tag']:
                        obj.tags.add(tag)
                else:
                    raise ImmediateHttpResponse(response=HttpForbidden(
                        'Tag must be an array of tag strings'))
        else:
            raise ImmediateHttpResponse(response=HttpResponse(status=405))
        return HttpCreated()

    def remove_tag(self, request, **kwargs):
        try:
            obj = self.cached_obj_get(request=request,
                                      **self.remove_api_resource_names(kwargs))
        except ObjectDoesNotExist:
            return HttpGone()
        except MultipleObjectsReturned:
            return HttpMultipleChoices("More than one resource is found at \
                                       this URI.")
        if request.method == 'POST':
            data = json.loads(request.POST.items()[0][0])
            if 'tag' in data:
                if isinstance(data['tag'], list):
                    for tag in data['tag']:
                        obj.tags.remove(tag)
                else:
                    raise ImmediateHttpResponse(response=HttpForbidden(
                        'Tag must be an array of tag strings'))
        else:
            raise ImmediateHttpResponse(response=HttpResponse(status=405))
        return HttpCreated()

    def add_children(self, request, **kwargs):
        try:
            obj = self.cached_obj_get(request=request,
                                      **self.remove_api_resource_names(kwargs))
        except ObjectDoesNotExist:
            return HttpGone()
        except MultipleObjectsReturned:
            return HttpMultipleChoices("More than one resource is found at \
                                       this URI.")
        if request.method == 'POST':
            data = json.loads(request.POST.items()[0][0])
            if 'image' in data:
                if isinstance(data['image'], list):
                    for URI in data['image']:
                        im = Image.objects.get(uuid=uuid_re.search(
                            URI).group())
                        obj.image_set.add(im)
                else:
                    raise ImmediateHttpResponse(response=HttpForbidden(
                        'Image URI\'s must be in an array'))
            if 'wordbox' in data:
                if isinstance(data['wordbox'], list):
                    for URI in data['wordbox']:
                        wb = WordBox.objects.get(uuid=uuid_re.search(
                            URI).group())
                        obj.wordbox_set.add(wb)
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
            return HttpMultipleChoices("More than one resource is found at \
                                       this URI.")
        if request.method == 'POST':
            data = json.loads(request.POST.items()[0][0])
            if 'image' in data:
                if isinstance(data['image'], list):
                    for URI in data['image']:
                        im = Image.objects.get(uuid=uuid_re.search(
                            URI).group())
                        obj.image_set.remove(im)
                else:
                    raise ImmediateHttpResponse(response=HttpForbidden(
                        'Image URI\'s must be in an array'))
            if 'wordbox' in data:
                if isinstance(data['wordbox'], list):
                    for URI in data['wordbox']:
                        wb = WordBox.objects.get(uuid=uuid_re.search(
                            URI).group())
                        obj.wordbox_set.remove(wb)
                else:
                    raise ImmediateHttpResponse(response=HttpForbidden(
                        'Wordbox URI\'s must be in an array'))
        else:
            raise ImmediateHttpResponse(response=HttpResponse(status=405))
        return HttpCreated()

#    def apply_sorting(self, objects, options=None):
#        if not options.has_key('order_by'):
#            options = {"order_by":"-created_time"}
#        return super(CommunityResource, self).apply_sorting(objects, options)

    def build_filters(self, filters=None):
        if filters is None:
            filters = {}
        orm_filters = super(CommunityResource, self).build_filters(
            filters)  # modify super(*,self)
        if filters:  # check if dictionary is empty or not
            try:
                if 'tag' in filters:
                    orm_filters['tags__name__in'] = filters['tag'].split(',')
                    return orm_filters
                elif "user" in filters:
                    obj = UserProfile.objects.get(uuid=uuid_re.search(
                        filters['user']).group())
                    if not obj.is_active:
                        return orm_filters
                    # make sure communities that the user is actively a part of
                    # is retrieved
                    memberships = obj.communitymembership_set.filter(
                        is_active=True)
                    sqs = obj.community_set.filter(
                        is_active=True, communitymembership__in=memberships)
                    orm_filters["pk__in"] = [i.pk for i in sqs]
                    return orm_filters
                elif "communitycategory" in filters:
                    obj = CommunityCategory.objects.get(uuid=uuid_re.search(
                        filters['communitycategory']).group())
                else:
                    return orm_filters
                if not obj.is_active:
                    return orm_filters
                sqs = obj.community_set.filter(is_active=True)
                orm_filters["pk__in"] = [i.pk for i in sqs]
            except Community.DoesNotExist:
                orm_filters["pk__in"] = []  # return HttpGone()
            except Community.MultipleObjectsReturned:
                # return HttpMultipleChoices("More than one resource is found
                #                             at this URI.")
                orm_filters["pk__in"] = []
                raise ImmediateHttpResponse(response=http.HttpNotFound())
        return orm_filters

    # set value of field that is not visible
    def hydrate(self, bundle):
        if hasattr(bundle.obj, 'IPaddress'):
            bundle.obj.IPaddress = bundle.request.META['REMOTE_ADDR']
        return bundle


class CommunityCategoryResource(DuJourModelResource):
    created_time = fields.DateTimeField(
        attribute='created_time', readonly=True, default=now)
    updated_time = fields.DateTimeField(
        attribute='updated_time', readonly=True, default=now)

    class Meta:
        cache = SimpleCache()
        serializer = TzSerializer()
        detail_uri_name = 'uuid'
        always_return_data = True
        queryset = CommunityCategory.objects.filter(is_active=True).distinct()
        resource_name = 'communitycategory'
        fields = ['name', 'description']
        detail_allowed_methods = ['get']
        list_allowed_methods = ['get', 'post']
        max_limit = 20
        ordering = ['created_time']
        authorization = Authorization()
        include_resource_uri = True

    def dehydrate(self, bundle):
        bundle.data['total_communities'] = bundle.obj.community_set.count()
        bundle.data['community'] = '/v1/community/?' + urlencode(
            {'communitycategory': bundle.data['resource_uri']})
        return bundle

    def prepend_urls(self):
        return [
            # add images/wordboxes
            url(str(r"^(?P<resource_name>%s)/(?P<uuid>" + uuid_re.pattern +
                    ")/add_community%s$") %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('add_community'), name="api_get_children"),
            # remove images/wordboxes
            url(str(r"^(?P<resource_name>%s)/(?P<uuid>" + uuid_re.pattern +
                    ")/remove_community%s$") %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('remove_community'), name="api_get_children"),
        ]

    def add_community(self, request, **kwargs):
        try:
            obj = self.cached_obj_get(request=request,
                                      **self.remove_api_resource_names(kwargs))
        except ObjectDoesNotExist:
            return HttpGone()
        except MultipleObjectsReturned:
            return HttpMultipleChoices("More than one resource is found at \
                                       this URI.")
        if request.method == 'POST':
            data = json.loads(request.POST.items()[0][0])
            if 'community' in data:
                if isinstance(data['community'], list):
                    for URI in data['community']:
                        com = Community.objects.get(uuid=uuid_re.search(
                            URI).group())
                        obj.community_set.add(com)
                else:
                    raise ImmediateHttpResponse(response=HttpForbidden(
                        'Community URI\'s must be in an array'))
        else:
            raise ImmediateHttpResponse(response=HttpResponse(status=405))
        return HttpCreated()

    def remove_community(self, request, **kwargs):
        try:
            obj = self.cached_obj_get(request=request,
                                      **self.remove_api_resource_names(kwargs))
        except ObjectDoesNotExist:
            return HttpGone()
        except MultipleObjectsReturned:
            return HttpMultipleChoices("More than one resource is found at \
                                       this URI.")
        if request.method == 'POST':
            data = json.loads(request.POST.items()[0][0])
            if 'community' in data:
                if isinstance(data['community'], list):
                    for URI in data['community']:
                        com = Community.objects.get(uuid=uuid_re.search(
                            URI).group())
                        obj.community_set.remove(com)
                else:
                    raise ImmediateHttpResponse(response=HttpForbidden(
                        'Community URI\'s must be in an array'))
        else:
            raise ImmediateHttpResponse(response=HttpResponse(status=405))
        return HttpCreated()

    def build_filters(self, filters=None):
        if filters is None:
            filters = {}
        # modify super(*,self)
        orm_filters = super(CommunityCategoryResource,
                            self).build_filters(filters)
        if filters:  # check if dictionary is empty or not
            try:
                if "community" in filters:
                    obj = Community.objects.get(uuid=uuid_re.search(
                        filters['community']).group())
                else:
                    return orm_filters
                if not obj.is_active:
                    return orm_filters
                sqs = obj.communitycategory_set.filter(is_active=True)
                orm_filters["pk__in"] = [i.pk for i in sqs]
            except CommunityCategory.DoesNotExist:
                orm_filters["pk__in"] = []  # return HttpGone()
            except CommunityCategory.MultipleObjectsReturned:
                # return HttpMultipleChoices("More than one resource is found
                #                             at this URI.")
                orm_filters["pk__in"] = []
                raise ImmediateHttpResponse(response=http.HttpNotFound())
        return orm_filters

    # set value of field that is not visible
    def hydrate(self, bundle):
        if hasattr(bundle.obj, 'IPaddress'):
            bundle.obj.IPaddress = bundle.request.META['REMOTE_ADDR']
        return bundle


class CommunityMembershipResource(DuJourModelResource):
    community = fields.ToOneField(CommunityResource, 'community')
    member = fields.ToOneField(UserResource, 'member')
    created_time = fields.DateTimeField(
        attribute='created_time', readonly=True, default=now)
    updated_time = fields.DateTimeField(
        attribute='updated_time', readonly=True, default=now)

    class Meta:
        cache = SimpleCache()
        serializer = TzSerializer()
        detail_uri_name = 'uuid'
        queryset = CommunityMembership.objects.filter(is_active=True)
        resource_name = 'communitymembership'
        fields = ['last_visited']
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'delete']
        filtering = {
            "member": ALL,
            "community": ALL,
        }
        ordering = ['created_time']
#        cache = SimpleCache()
        authorization = Authorization()
        include_resource_uri = True

    def dehydrate(self, bundle):
        bundle.data['new_posts'] = bundle.obj.community.image_set.filter(
            is_active=True, created_time__gt=bundle.obj.last_visited).count()
        return bundle

    def build_filters(self, filters=None):
        if filters is None:
            filters = {}
        # modify super(*,self)
        orm_filters = super(CommunityMembershipResource,
                            self).build_filters(filters)
        # dual filter, supports multiple parents
        if "community" in filters and "member" in filters:
            if 'community__exact' in orm_filters:
                del orm_filters['community__exact']
                    # delete this field since this is a GFK
            if 'member__exact' in orm_filters:
                del orm_filters['member__exact']
                    # delete this field since this is a GFK
            try:
                community_uuid_list = uuid_re.findall(filters['community'])
                member = UserProfile.objects.get(uuid=uuid_re.search(
                    filters['member']).group())
                if not member.is_active:
                    return orm_filters
                sqs = CommunityMembership.objects.filter(
                    is_active=True, member=member,
                    community__uuid__in=community_uuid_list)
                orm_filters["pk__in"] = [i.pk for i in sqs]
            except CommunityMembership.DoesNotExist:
                orm_filters["pk__in"] = []  # return HttpGone()
            except CommunityMembership.MultipleObjectsReturned:
                # return HttpMultipleChoices("More than one resource is found
                #                             at this URI.")
                orm_filters["pk__in"] = []
                raise ImmediateHttpResponse(response=http.HttpNotFound())
        else:
            try:
                if "member" in filters:
                    obj = UserProfile.objects.get(uuid=uuid_re.search(
                        filters['member']).group())
                    if 'member__exact' in orm_filters:
                        # delete this field since this is a GFK
                        del orm_filters['member__exact']
                elif "community" in filters:
                    obj = Community.objects.get(uuid=uuid_re.search(
                        filters['community']).group())
                    if 'community__exact' in orm_filters:
                        # delete this field since this is a GFK
                        del orm_filters['community__exact']
                else:
                    return orm_filters
                if not obj.is_active:
                    return orm_filters
                sqs = obj.communitymembership_set.filter(is_active=True)
                orm_filters["pk__in"] = [i.pk for i in sqs]
            except CommunityMembership.DoesNotExist:
                orm_filters["pk__in"] = []  # return HttpGone()
            except CommunityMembership.MultipleObjectsReturned:
                # return HttpMultipleChoices("More than one resource is
                #                             found at this URI.")
                orm_filters["pk__in"] = []
                raise ImmediateHttpResponse(response=http.HttpNotFound())
        return orm_filters

    def obj_create(self, bundle, request=None, **kwargs):
        # check if this friendship already exists not or if it's active
        community = self.fields['community'].hydrate(bundle).obj
        member = self.fields['member'].hydrate(bundle).obj
        try:
            membership = CommunityMembership.objects.get(
                community=community, member=member)
        except:
            return super(CommunityMembershipResource,
                         self).obj_create(bundle, request=None, **kwargs)
        else:
            if membership.is_active:
                raise BadRequest('This friendship already exists!')
            else:
                membership.is_active = True
                membership.save()
                return bundle

    def prepend_urls(self):
        return [
            url(str(r"^(?P<resource_name>%s)/(?P<uuid>" + uuid_re.pattern +
                    ")/visited%s$") %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('visited'), name="api_count")
        ]

    def visited(self, request, **kwargs):
        if request.method == 'GET':
            self.obj_get(request=request, **self.remove_api_resource_names(
                kwargs)).reset_last_visited_date()
            data = {}
            return HttpResponse(simplejson.dumps(data),
                                mimetype='application/javascript')
        else:
            raise ImmediateHttpResponse(response=HttpResponse(status=405))

    def apply_sorting(self, objects, options=None):
        options = {"order_by": "-created_time"}
        return super(CommunityMembershipResource,
                     self).apply_sorting(objects, options)


class UserSubscriptionResource(DuJourModelResource):
    from_user = fields.ToOneField(UserResource, 'from_user')
    to_user = fields.ToOneField(UserResource, 'to_user')

    class Meta:
        cache = SimpleCache()
        serializer = TzSerializer()
        always_return_data = True
        detail_uri_name = 'uuid'
        queryset = UserSubscription.objects.filter(is_active=True)
        resource_name = 'usersubscription'
        ordering = []
        fields = ['status']
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'put', 'delete']
        max_limit = 20
        filtering = {
            "user": ALL,
        }
        authorization = Authorization()
#        validation = FormValidation(form_class=CommentForm)
        include_resource_uri = True

    def dehydrate(self, bundle):
#        if self.get_resource_uri(bundle) != bundle.request.path:
#            bundle.data['member'] = '/v1/user/?community=' +
#               self.get_resource_uri(bundle)
#        bundle.data['user_voted'] = bundle.obj.user_voted(USER_PK)
#        bundle.data['user'] = bundle.data['user2']
        del bundle.data['status']
#        del bundle.data['user1']
#        del bundle.data['user2']
        return bundle

    def build_filters(self, filters=None):
        if filters is None:
            filters = {}
        # modify super(*,self)
        orm_filters = super(UserSubscriptionResource,
                            self).build_filters(filters)
        if filters:  # check if dictionary is empty or not
            try:
                if "user" in filters:
                    obj = UserProfile.objects.get(uuid=uuid_re.search(
                        filters['user']).group())
                    if 'user__exact' in orm_filters:
                        # delete this field since this is a GFK
                        del orm_filters['user__exact']
                else:
                    return orm_filters
                if not obj.is_active:
                    return orm_filters
                sqs = obj.to_usersubscriptions.filter(is_active=True)
                orm_filters["pk__in"] = [i.pk for i in sqs]
            except UserSubscription.DoesNotExist:
                orm_filters["pk__in"] = []  # return HttpGone()
            except UserSubscription.MultipleObjectsReturned:
                # return HttpMultipleChoices("More than one resource is found
                #                             at this URI.")
                orm_filters["pk__in"] = []
                raise ImmediateHttpResponse(response=http.HttpNotFound())
        return orm_filters

    # set value of field that is not visible
    def hydrate(self, bundle):
        if hasattr(bundle.obj, 'IPaddress'):
            bundle.obj.IPaddress = bundle.request.META['REMOTE_ADDR']
        return bundle

    def obj_create(self, bundle, request=None, **kwargs):
        to_user = UserProfile.objects.get(
            uuid=uuid_re.search(bundle.data['to_user']).group())
        from_user = UserProfile.objects.get(
            uuid=uuid_re.search(bundle.data['from_user']).group())
        if UserSubscription.objects.filter(
                is_active=True, to_user=to_user, from_user=from_user).exists():
            raise ImmediateHttpResponse(
                HttpForbidden("This subscription already exists"))
        else:
            return super(UserSubscriptionResource,
                         self).obj_create(bundle, request=None, **kwargs)


class SubscriberResource(DuJourModelResource):
    from_user = fields.ToOneField(UserResource, 'from_user')
    to_user = fields.ToOneField(UserResource, 'to_user')

    class Meta:
        cache = SimpleCache()
        serializer = TzSerializer()
        detail_uri_name = 'uuid'
        queryset = UserSubscription.objects.filter(is_active=True)
        resource_name = 'usersubscriber'
        ordering = []
        fields = ['status']
        list_allowed_methods = ['get']
        detail_allowed_methods = []
        max_limit = 20
        filtering = {
            "user": ALL,
        }
        authorization = Authorization()
#        validation = FormValidation(form_class=CommentForm)
        include_resource_uri = True

    def dehydrate(self, bundle):
        del bundle.data['status']
        return bundle

    def build_filters(self, filters=None):
        if filters is None:
            filters = {}
        # modify super(*,self)
        orm_filters = super(SubscriberResource,
                            self).build_filters(filters)
        if filters:  # check if dictionary is empty or not
            try:
                if "user" in filters:
                    obj = UserProfile.objects.get(uuid=uuid_re.search(
                        filters['user']).group())
                    if 'user__exact' in orm_filters:
                        # delete this field since this is a GFK
                        del orm_filters['user__exact']
                else:
                    return orm_filters
                if not obj.is_active:
                    return orm_filters
                sqs = obj.from_usersubscriptions.filter(is_active=True)
                orm_filters["pk__in"] = [i.pk for i in sqs]
            except UserProfile.DoesNotExist:
                orm_filters["pk__in"] = []  # return HttpGone()
            except UserProfile.MultipleObjectsReturned:
                # return HttpMultipleChoices("More than one resource is found
                #                             at this URI.")
                orm_filters["pk__in"] = []
                raise ImmediateHttpResponse(response=http.HttpNotFound())
        return orm_filters


class NotificationResource(DuJourModelResource):

    class Meta:
        cache = SimpleCache()
        serializer = TzSerializer()
        include_resource_uri = False
        detail_uri_name = 'uuid'
        queryset = UserProfile.objects.filter(is_active=True)
        resource_name = 'notification'
        ordering = ['created_time']
        fields = ['message']
        detail_allowed_methods = []
        list_allowed_methods = ['get']
        max_limit = 20
        filtering = {
            "user": ALL,
        }
        authorization = Authorization()
#        validation = FormValidation()

    def prepend_urls(self):
        return [
            url(str(r"^(?P<resource_name>%s)/count%s$") %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('count'), name="api_count"),
            url(str(r"^(?P<resource_name>%s)/reset_count%s$") %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('reset_count'), name="api_count"),
        ]

    def count(self, request, **kwargs):
        if request.method == 'GET':
            owner = UserProfile.objects.get(
                uuid=uuid_from_uri(request.GET['user']))
            image_pk = [im.pk for im in owner.image_set.all()]
            v = Vote.objects.filter(
                is_active=True, content_type__model='image',
                object_id__in=image_pk,
                created_time__gt=owner.last_notification).exclude(owner=owner)
            c = Comment.objects.filter(
                is_active=True, content_type__model='image',
                object_id__in=image_pk,
                created_time__gt=owner.last_notification).exclude(owner=owner)
            # sort reverse chronologically
            base_object_list = sorted(chain(v, c),
                                      key=attrgetter('created_time'))[::-1]
            data = {}
            data['count'] = len(base_object_list)
            return HttpResponse(simplejson.dumps(data),
                                mimetype='application/javascript')
        else:
            raise ImmediateHttpResponse(response=HttpResponse(status=405))

    def reset_count(self, request, **kwargs):
        if request.method == 'GET':
            owner = UserProfile.objects.get(
                uuid=uuid_from_uri(request.GET['user']))
            owner.reset_notification_date()
            data = {}
            data['count'] = 0
            return HttpResponse(simplejson.dumps(data),
                                mimetype='application/javascript')
        else:
            raise ImmediateHttpResponse(response=HttpResponse(status=405))

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
            owner = UserProfile.objects.get(
                uuid=uuid_from_uri(filters['user']))
            image_pk = [im.pk for im in owner.image_set.all()]
            v = Vote.objects.filter(
                is_active=True, content_type__model='image',
                object_id__in=image_pk).exclude(owner=owner)
            c = Comment.objects.filter(
                is_active=True, content_type__model='image',
                object_id__in=image_pk).exclude(owner=owner)
            # sort reverse chronologically
            base_object_list = sorted(
                chain(v, c), key=attrgetter('created_time'))[::-1]
            return self.apply_authorization_limits(request, base_object_list)
        except ValueError:
            raise BadRequest("Invalid resource lookup data provided \
                             (mismatched type).")

    def full_dehydrate(self, bundle):
        """
        Given a bundle with an object instance, extract the information from it
        to populate the resource.
        """
        from website.api.v1.action_resources import CommentResource, \
            VoteResource
        # Dehydrate each field.
        if bundle.obj.obj_type() == 'comment':
            obj = CommentResource()
        elif bundle.obj.obj_type() == 'vote':
            obj = VoteResource()
        else:
            return bundle
        for field_name, field_object in obj.fields.items():
            # A touch leaky but it makes URI resolution work.
            if getattr(field_object, 'dehydrated_type', None) == 'related':
                field_object.api_name = self._meta.api_name
                field_object.resource_name = obj._meta.resource_name

            bundle.data[field_name] = field_object.dehydrate(bundle)

            # Check for an optional method to do further dehydration.
            method = getattr(obj, "dehydrate_%s" % field_name, None)

            if method:
                bundle.data[field_name] = method(bundle)

        bundle = obj.dehydrate(bundle)
        return bundle
