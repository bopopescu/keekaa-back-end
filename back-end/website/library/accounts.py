from django.contrib.auth.models import User


def get_matched_name(name):
    return name.lower().replace('.', '').replace('-', '').replace('_', '')


def check_email_available(email):
    try:
        User.objects.get(email=email)
    except User.DoesNotExist:
        return True
    except User.MultipleObjectsReturned:
        return False
    return False


def check_name_available(name):
    name = get_matched_name(name)
    try:
        User.objects.get(username=name)
        return False
    except User.DoesNotExist:
        pass
    except User.MultipleObjectsReturned:
        return False
    return True
