from urllib.parse import quote

import pytest
from rest_framework import status

from budget_core.models import Category


@pytest.mark.django_db
class TestCategory:

    ENDPOINT = '/category/'

    def test_list(self, api_client, user, categories):
        client = api_client()
        client.force_authenticate(user=user)
        response = client.get(self.ENDPOINT)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) is 4

    def test_list_unauthorized_401(self, api_client, user, categories):
        response = api_client().get(self.ENDPOINT)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create(self, api_client, user, category_name):
        client = api_client()
        client.force_authenticate(user=user)
        response = client.post(
            self.ENDPOINT,
            data={"name": category_name},
            format='json'
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['name'] == category_name

    def test_retrieve(self, api_client, user, categories, category_name):
        category = categories[0]
        url = f'{self.ENDPOINT}{category.id}/'

        client = api_client()
        client.force_authenticate(user=user)
        response = client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'].startswith(category_name)

    def test_delete(self, api_client, user, categories, category_name):
        category = categories[0]
        url = f'{self.ENDPOINT}{category.id}/'

        client = api_client()
        client.force_authenticate(user=user)
        response = client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Category.objects.count() is len(categories) - 1

    def test_filter_by_name(self, api_client, user, categories):
        category = categories[0]
        category_name = quote(category.name)
        url = f'{self.ENDPOINT}?name={category_name}'

        client = api_client()
        client.force_authenticate(user=user)
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
