""" URLconf

The root URL dispatcher.

"""

from django.conf.urls import patterns, url, include

urlpatterns = patterns('website.views',
                       url(r'', include('website.api.v1.urls')),
                       )

#    url(r'^accounts/', include('website.accounts.urls')),
