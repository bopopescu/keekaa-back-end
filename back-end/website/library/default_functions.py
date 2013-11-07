import uuid
from time import time


def create_uuid():
    return str(uuid.uuid5(uuid.NAMESPACE_URL, str(time()) + str(uuid.uuid4())))
