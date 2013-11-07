from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import resolve, Resolver404, get_script_prefix
from tastypie import fields
from tastypie.resources import Resource, ModelResource
from tastypie.exceptions import ApiFieldError, NotFound
from website.library.tastypie_cache import ClientCachedResource

# If deserialize was passed request this could be moved to
# a custom deserializer class like it ought to be. If you don't want
# to use a separate branch you can use this mixin.


class MultipartResource(object):
    def deserialize(self, request, data, format=None):
        if not format:
            format = request.META.get('CONTENT_TYPE', 'application/json')
        if format == 'application/x-www-form-urlencoded':
            return request.POST
        if format.startswith('multipart'):
            data = request.POST.copy()
            data.update(request.FILES)
            return data
        return super(MultipartResource, self).deserialize(request, data,
                                                          format)


class GenericResource(ModelResource):

    def get_via_uri(self, uri, request=None):
        prefix = get_script_prefix()
        chomped_uri = uri

        if prefix and chomped_uri.startswith(prefix):
            chomped_uri = chomped_uri[len(prefix) - 1:]

        try:
            view, args, kwargs = resolve(chomped_uri)
        except Resolver404:
            raise NotFound("The URL provided '%s' was not a link to a valid "
                           "resource." % uri)

        # Hack to climb the closure chain to get back to the original resource
        # since tastypie doesn't have a great way of getting from a uri to
        # a resource.
        parent_resource = view.func_closure[
            0].cell_contents.func_closure[0].cell_contents
        return parent_resource.obj_get(
            **self.remove_api_resource_names(kwargs))


class DuJourModelResource(ClientCachedResource, MultipartResource,
                          ModelResource):
    """
    Subclass Tastypie ModelResource so that we can customize some
    methods that are applicable to our entire API library.
    """
    def determine_format(self, request):
        return "application/json"

    def get_via_uri(self, uri, request=None):
        prefix = get_script_prefix()
        chomped_uri = uri

        if prefix and chomped_uri.startswith(prefix):
            chomped_uri = chomped_uri[len(prefix) - 1:]

        try:
            view, args, kwargs = resolve(chomped_uri)
        except Resolver404:
            raise NotFound("The URL provided '%s' was not a link to a valid "
                           "resource." % uri)

        # Hack to climb the closure chain to get back to the original resource
        # since tastypie doesn't have a great way of getting from a uri to
        # a resource.
        parent_resource = view.func_closure[
            0].cell_contents.func_closure[0].cell_contents
        return parent_resource.obj_get(
            **self.remove_api_resource_names(kwargs))


class GenericForeignKeyField(fields.ToOneField):
    def __init__(self, to, attribute, **kwargs):
        if not isinstance(to, dict):
            raise ValueError('to field must be a dictionary in '
                             'GenericForeignKeyField')
        if len(to) <= 0:
            raise ValueError('to field must have some values')
        for k, v in to.iteritems():
            if not issubclass(k, models.Model) or not issubclass(v, Resource):
                raise ValueError('to field must map django models to tastypie '
                                 'resources')
        super(GenericForeignKeyField, self).__init__(to, attribute, **kwargs)

    def get_related_resource(self, related_instance):
        self._to_class = self.to[type(related_instance)]
        if self._to_class is None:
            raise TypeError('no resource for model %s' % type(
                related_instance))
        return super(GenericForeignKeyField, self).get_related_resource(
            related_instance)

    @property
    def to_class(self):
        if self._to_class:
            return self._to_class
        return GenericResource

    def resource_from_uri(self, fk_resource, uri,
                          request=None, related_obj=None, related_name=None):
        try:
            obj = fk_resource.get_via_uri(uri, request=request)
            fk_resource = self.get_related_resource(obj)
            return super(GenericForeignKeyField, self).resource_from_uri(
                fk_resource, uri, request, related_obj, related_name)
        except ObjectDoesNotExist:
            raise ApiFieldError("Could not find the provided object via "
                                "resource URI '%s'." % uri)

    def build_related_resource(self, *args, **kwargs):
        # Reset self._to_class so we're guaranteed to re-figure out
        # which class we want.
        self._to_class = None
        return super(GenericForeignKeyField, self).build_related_resource(
            *args, **kwargs)
