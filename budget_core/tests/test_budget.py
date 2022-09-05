import pytest
from rest_framework import status

from budget_core.models import BudgetItem


@pytest.mark.django_db
class TestBudget:

    ENDPOINT = '/budget/'
    BUDGET_ITEM_ENDPOINT = '/budget-item/'

    def test_list(self, api_client, user, budgets):
        client = api_client()
        client.force_authenticate(user=user)
        response = client.get(self.ENDPOINT)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) is 2

    def test_list_unauthorized_401(self, api_client, user, budgets):
        response = api_client().get(self.ENDPOINT)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_read_permissions(self, api_client, user2, budget_user1_only, budget_user1_shared_with_user2):
        url = f'{self.ENDPOINT}{budget_user1_only.id}/'
        url_shared_budget = f'{self.ENDPOINT}{budget_user1_shared_with_user2.id}/'
        client = api_client()
        client.force_authenticate(user=user2)

        response = client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

        response = client.get(url_shared_budget)
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.parametrize('user_fixture,status_code', [
        ('user', status.HTTP_204_NO_CONTENT),
        ('user2', status.HTTP_403_FORBIDDEN),
    ])
    def test_write_permissions(
            self, api_client, request, budget_user1_shared_with_user2, user_fixture,
            status_code
    ):
        url = f'{self.ENDPOINT}{budget_user1_shared_with_user2.id}/'
        user = request.getfixturevalue(user_fixture)

        client = api_client()
        client.force_authenticate(user=user)
        response = client.delete(url)
        assert response.status_code == status_code

    @pytest.mark.parametrize('item_type', [BudgetItem.EXPENSE, BudgetItem.INCOME])
    def test_budget_recalculate(
            self, api_client, budget_user1_only, user, budget_item_data, item_type
    ):
        initial_budget_total = budget_user1_only.total
        budget_url = f'{self.ENDPOINT}{budget_user1_only.id}/'
        client = api_client()
        client.force_authenticate(user=user)
        budget_item_data['item_type'] = item_type

        item_response = client.post(
            self.BUDGET_ITEM_ENDPOINT,
            data=budget_item_data,
            format='json'
        )
        budget_resp = client.get(budget_url)
        end_budget_total = budget_resp.data['total']

        assert item_response.status_code == status.HTTP_201_CREATED
        assert budget_resp.status_code == status.HTTP_200_OK
        if item_type == BudgetItem.EXPENSE:
            assert float(end_budget_total) == initial_budget_total - budget_item_data['amount']
        elif item_type == BudgetItem.INCOME:
            assert float(end_budget_total) == initial_budget_total + budget_item_data['amount']

    def test_create(self, api_client, user, category_name):
        some_random_name = 'Home budget'
        client = api_client()
        client.force_authenticate(user=user)
        response = client.post(
            self.ENDPOINT,
            data={"name": some_random_name, "total": 15190},
            format='json'
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['name'] == some_random_name
        # it should be 0 as total is read only field and should be calculated only on budget items change
        assert float(response.data['total']) == 0

    def test_filter_by_name(self, api_client, user, budget_user1_only):
        budget_name = budget_user1_only.name
        url = f'{self.ENDPOINT}?name={budget_name}'

        client = api_client()
        client.force_authenticate(user=user)
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1

