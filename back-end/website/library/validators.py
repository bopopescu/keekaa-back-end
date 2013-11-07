import re
from django.core.validators import email_re as django_email_re

email_re = django_email_re
username_re = re.compile(r'^[a-zA-Z0-9\.\-_]{5,30}$')
UUID_REGEX = r'[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}'
uuid_re = re.compile(UUID_REGEX)
VERSION_REGEX = r'v[0-9]+'
version_re = re.compile(VERSION_REGEX)
RESOURCE_REGEX = r'[a-z]{2,}'
resource_re = re.compile(RESOURCE_REGEX)
URI_REGEX = r'/{version}/{resource}/{uuid}/'.format(
    version=VERSION_REGEX, resource=RESOURCE_REGEX, uuid=UUID_REGEX)
uri_re = re.compile(URI_REGEX)


def is_valid_uri(uri):
    return uri_re.search(uri) is not None


def check_if_valid_display_name(name):
    if username_re.match(name) is None:
        return False
    else:
        if len(name) <= 30:
            return True
        else:
            return False


def get_match_name(name):
    if check_if_valid_display_name(name):
        return name.lower().replace('.', '').replace('-', '').replace('_', '')
    else:
        return ''
