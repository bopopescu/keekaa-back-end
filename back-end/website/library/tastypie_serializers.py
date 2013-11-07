"""
Rewrite the default behavior of Serializer of tastypie
"""

import datetime
from django.conf import settings
from tastypie.utils import format_datetime, make_naive
from dateutil.tz import gettz
from tastypie.serializers import Serializer


class TzSerializer(Serializer):
    """
    A subclass of the built-in Serializer that adds timezone offsets to
    outputted times, making them ISO-8601 compliant.

    Based on the patch in this pull request:
    https://github.com/toastdriven/django-tastypie/pull/445
    """

    def __init__(self, formats=None, content_types=None,
                 datetime_formatting=None):
        super(TzSerializer, self).\
            __init__(formats, content_types, datetime_formatting)
        timezone_str = getattr(settings, 'TIME_ZONE', None)
        if timezone_str:
            self.tzinfo = gettz(timezone_str)

    def format_datetime(self, data):
        """
        A hook to control how datetimes are formatted.

        Can be overridden at the ``Serializer`` level (``datetime_formatting``)
        or globally (via ``settings.TASTYPIE_DATETIME_FORMATTING``).

        Default is ``iso-8601``, which looks like "2010-12-16T03:02:14+00:00".
        """
        data = make_naive(data)
        if self.datetime_formatting == 'rfc-2822':
            return format_datetime(data)

        if self.tzinfo:
            data = datetime.datetime(data.year, data.month, data.day,
                                     data.hour, data.minute, data.second,
                                     data.microsecond, self.tzinfo)

        return data.isoformat()
