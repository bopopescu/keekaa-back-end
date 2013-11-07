import re
import uuid

from time import time
from website.library.validators import VERSION_REGEX, RESOURCE_REGEX, \
    uuid_re, UUID_REGEX


def parse_uri(uri):
    """
    return 'version', 'resource', and 'uuid' of the uri
    """
    return re.match(r"/(?P<version>{version})/(?P<resource>{resource})/"
                    "(?P<uuid>{uuid})/".format(
                    version=VERSION_REGEX, resource=RESOURCE_REGEX,
                    uuid=UUID_REGEX), uri).groupdict()


def construct_detail_uri(version='v1', resource='default',
                         uuid='12345678-1234-1234-1234-123456789012'):
    """
    return uri given 'version', 'resource', and 'uuid'
    """
    return '/{version}/{resource}/{uuid}/'.format(
        version=version, resource=resource, uuid=uuid)


def construct_filter_uri(version='v1', resource='default', parameter='parent',
                         filter_uri=
                         '/v1/parent/12345678-1234-1234-1234-123456789012'):
    """
    return filter uri given 'version', 'resource', and 'uri of filter object'
    """
    return '/{version}/{resource}/?{parameter}={filter_uri}'.format(
        version=version, resource=resource, parameter=parameter,
        filter_uri=filter_uri.replace('/', '%2F'))


def construct_list_uri(version='v1', resource='default'):
    """
        return uri given 'version', 'resource', and 'uuid'
    """
    return '/{version}/{resource}/'.format(version=version, resource=resource)


def uuid_from_uri(uri):
    return uuid_re.search(uri).group()


def create_uuid():
    return str(uuid.uuid5(uuid.NAMESPACE_URL, str(time()) + str(uuid.uuid4())))
