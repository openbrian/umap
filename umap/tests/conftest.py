import shutil
import tempfile

import pytest
from django.core.cache import cache
from django.core.signing import get_cookie_signer

from .base import (
    DataLayerFactory,
    MapFactory,
    UserFactory,
    TileLayerFactory,
    LicenceFactory,
)

TMP_ROOT = tempfile.mkdtemp()


def pytest_configure(config):
    from django.conf import settings

    settings.MEDIA_ROOT = TMP_ROOT


def pytest_unconfigure(config):
    shutil.rmtree(TMP_ROOT, ignore_errors=True)


def pytest_runtest_teardown():
    cache.clear()


@pytest.fixture
def user():
    return UserFactory(password="123123")


@pytest.fixture
def user2():
    return UserFactory(username="Averell", password="456456")


@pytest.fixture
def licence():
    return LicenceFactory()


@pytest.fixture
def map(licence, tilelayer):
    user = UserFactory(username="Gabriel", password="123123")
    return MapFactory(owner=user, licence=licence)


@pytest.fixture
def anonymap(map):
    map.owner = None
    map.save()
    return map


@pytest.fixture
def cookieclient(client, map):
    key, value = map.signed_cookie_elements
    client.cookies[key] = get_cookie_signer(salt=key).sign(value)
    return client


@pytest.fixture
def allow_anonymous(settings):
    settings.UMAP_ALLOW_ANONYMOUS = True


@pytest.fixture
def datalayer(map):
    return DataLayerFactory(map=map, name="Default Datalayer")


@pytest.fixture
def tilelayer():
    return TileLayerFactory()
