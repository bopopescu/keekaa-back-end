from tastypie.authentication import Authentication
from tastypie.exceptions import ImmediateHttpResponse
from tastypie import http

#from tastypie.authorization import DjangoAuthorization


class DujourAuthentication(Authentication):
    def is_authenticated(self, request, **kwargs):
        if request.user.is_authenticated():
            return True
        else:
            raise ImmediateHttpResponse(response=http.HttpForbidden())
            return False
#return super(DujourAuthentication, self).is_authenticated(request, **kwargs)

    def get_identifier(self, request):
        if request.user.is_authenticated():
            return request.user.username
        else:
            return super(DujourAuthentication, self).get_identifier(request)
