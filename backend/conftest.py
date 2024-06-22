import pytest
from rest_framework.test import APIClient

from common.tests.utils import Loader
from draw.tests.mock.models.token import token_userA


@pytest.fixture(scope='session')
def client() -> APIClient:
    """A DRF test client with a token authenticating as userA."""
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token_userA.key}')
    return client


@pytest.fixture(scope='function')
def unauthed_client() -> APIClient:
    """A DRF test client with no authentication"""
    return APIClient()


def pytest_collection_modifyitems(items):
    """Modifies test items in place to ensure test modules run in a given order.
    ViewTestBase.test_only_tested_methods_allowed must be the last test run in each test module."""

    def sort_order(item):
        # Ensure that ViewTestBase.test_only_tested_methods_allowed is the last test run in each test module
        if item.cls:
            return item.cls.__name__, 1 if item.name == 'test_only_tested_methods_allowed' else 0
        return item.name, 0

    items.sort(key=sort_order)


@pytest.fixture(scope='session', autouse=True)
def load_mock_data(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        Loader.load_mock_data()
