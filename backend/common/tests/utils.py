import os
from abc import ABC
from http import HTTPMethod
from importlib import import_module
from typing import Type, List

import pytest
from django.conf import settings
from django.db.models import Model
from requests import Response
from rest_framework.test import APIClient

from draw.models import User
from draw.tests.mock.models.user import models as users


class Loader:

    @staticmethod
    def load_mock_data() -> None:
        """Discovers any mock data defined under /tests/mock/models and loads them into the test database.
        Handles dependencies between models by loading related models first.

        :return: None
        """
        imported_models = []
        # Everything depends on users so we'll first load those
        Loader.load_users()
        imported_models.append(User)

        def sort_order(item):
            order = ['user']
            if item in order:
                return order.index(item)
            return len(order) + 1

        for app in sorted(settings.INSTALLED_APPS, key=sort_order):
            dir_name = os.path.join(settings.BASE_DIR, app, 'tests/mock/models/')

            if not os.path.isdir(dir_name):
                continue

            # Ignore files starting with an underscore
            for filename in [f for f in os.listdir(dir_name) if not f.startswith('_')]:
                items = import_module(f'{app}.tests.mock.models.{filename[:-3]}').models
                model = items[0].__class__
                # Skip if we've already loaded this model
                if model in imported_models:
                    continue
                # Load related models first
                for field in model._meta.get_fields(include_parents=False, include_hidden=False):
                    related_model = field.related_model
                    # The related model might be itself, for instance Comment has a ForeignKey to itself;
                    # Also only import concrete fields, not reverse relations, which would cause a loop;
                    if related_model and related_model != model and related_model not in imported_models and field.concrete:
                        try:
                            related_model.objects.bulk_create(Loader.import_items(related_model))
                            imported_models.append(related_model)
                        except ModuleNotFoundError:
                            # We don't have mock data for this field/model so we'll just ignore it
                            pass
                model.objects.bulk_create(items)
                imported_models.append(model)
        print(f'Loaded mock data for {", ".join([model.__name__ for model in imported_models])}')

    @staticmethod
    def load_users():
        User.objects.bulk_create(users)

    @staticmethod
    def import_items(model: Type[Model]) -> List[Model]:
        """Import the items for the given model.
        @param model: the model to import items for
        @return: the items to load
        """
        if related_class := model._meta.auto_created:
            # If we're loading a through model, load the base model beforehand
            Loader.load(related_class)
        app_name = model.__module__.split('.')[0]
        if app_name == 'allauth':  # Special case for allauth
            app_name = 'authentication'
        module_name = f'{app_name}.tests.mock.models.{model.__name__.lower()}'
        items = import_module(module_name).models
        return items


@pytest.mark.django_db()
class ViewTestBase(ABC):
    """Base class for all view test classes."""

    required_mocks: List[Type[Model]] = []
    client: APIClient = None
    unauth_client: APIClient = None
    tested_endpoints: dict = {}  # This property will be shared across all instances of ViewTestBase

    def _stash_endpoint(self, url: str, method: HTTPMethod) -> None:
        """Stash the given endpoint for testing."""
        trimmed_url = url.split('?')[0]  # Remove query params
        if trimmed_url not in self.tested_endpoints:
            self.tested_endpoints[trimmed_url] = {method.value}
        else:
            self.tested_endpoints[trimmed_url].add(method.value)

    @pytest.fixture(autouse=True)
    def setup(self, client, unauthed_client):
        self.client = client
        self.unauth_client = unauthed_client

    def run(self, url: str, method: HTTPMethod, data=None, data_format='json', authed: bool = True,
            validate_requires_auth: bool = True) -> Response:
        """Run the given method and check that it requires authentication.
        @param url: the url to hit
        @param method: the method to use (get, post, patch, etc.)
        @param data: the data to send
        @param data_format: the format to use (json, etc.)
        @param authed: whether the request should be made as an authenticated user (userA)
        @param validate_requires_auth: if authed is True, validate that the endpoint requires authentication
        @return: the response
        """
        if authed:
            if validate_requires_auth:
                self._validate_endpoint_requires_auth(url, method, data)
            response = getattr(self.client, method.lower())(url, data, format=data_format)
        else:
            response = getattr(self.unauth_client, method.lower())(url, data, format=data_format)
        self._stash_endpoint(url, method)
        return response

    def _validate_endpoint_requires_auth(self, url, method: HTTPMethod, data=None, data_format='json') -> None:
        """Make sure the given endpoint requires authentication."""
        response = getattr(self.unauth_client, method.lower())(url, data, format=data_format)
        expected = 401
        assert expected == response.status_code, f'Expected status code {expected} for {method} on {url} but got {response.status_code}'

    def test_only_tested_methods_allowed(self):
        """Make sure only tested methods are allowed. This test should be the last one run in the class and thus
        the tests should be sorted accordingly. This is done in conftest.py"""
        all_methods = {'GET', 'POST', 'PATCH', 'DELETE', 'PUT'}
        tested_endpoints = self.tested_endpoints.copy()
        self.tested_endpoints.clear()
        for url, methods in tested_endpoints.items():
            forbidden_methods = all_methods - methods
            for method in forbidden_methods:
                response = getattr(self.client, method.lower())(url)
                expected = 405
                assert expected == response.status_code, f'Method {method} should not be allowed on {url} (got {response.status_code})'
