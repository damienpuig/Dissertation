import pytest
import redis
from mongoengine import *


def _get_client(cls, request=None, **kwargs):
    params = {'host': 'localhost', 'port': 6379}
    params.update(kwargs)
    client = cls(**params)
    client.flushdb()
    if request:
        request.addfinalizer(client.flushdb)
    return client

@pytest.fixture()
def r(request, **kwargs):
    return _get_client(redis.Redis, request, **kwargs)