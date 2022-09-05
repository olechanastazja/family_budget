import pytest
from rest_framework import status

from budget_core.models import BudgetItem


@pytest.mark.django_db
class TestBudgetItem:

    ENDPOINT = "/budget-item/"

    def test_list(self, api_client, user, budget_items):
        client = api_client()
        client.force_authenticate(user=user)
        response = client.get(self.ENDPOINT)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) is 2

    def test_list_unauthorized_401(self, api_client, user, budgets):
        response = api_client().get(self.ENDPOINT)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.parametrize(
        "user_fixture,status_code",
        [
            ("user", status.HTTP_200_OK),
            ("user2", status.HTTP_404_NOT_FOUND),
        ],
    )
    def test_read_permissions(
        self, api_client, request, user2, budget_income, user_fixture, status_code
    ):
        url = f"{self.ENDPOINT}{budget_income.id}/"
        user = request.getfixturevalue(user_fixture)

        client = api_client()
        client.force_authenticate(user=user)
        response = client.get(url)
        assert response.status_code == status_code

    @pytest.mark.parametrize(
        "user_fixture,status_code",
        [
            ("user", status.HTTP_204_NO_CONTENT),
            ("user2", status.HTTP_404_NOT_FOUND),
        ],
    )
    def test_write_permissions(
        self, api_client, request, budget_expense, user_fixture, status_code
    ):
        url = f"{self.ENDPOINT}{budget_expense.id}/"
        user = request.getfixturevalue(user_fixture)

        client = api_client()
        client.force_authenticate(user=user)
        response = client.delete(url)
        assert response.status_code == status_code

    def test_create(self, api_client, user, budget_item_data):
        client = api_client()
        client.force_authenticate(user=user)
        budget_item_data["item_type"] = BudgetItem.INCOME
        response = client.post(self.ENDPOINT, data=budget_item_data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["name"] == budget_item_data["name"]

    def test_filter_by_budget_and_category(
        self, api_client, user, budget_expense, budget_user1_only, categories
    ):
        url = (
            f"{self.ENDPOINT}?budget={budget_user1_only.id}&category={categories[0].id}"
        )
        client = api_client()
        client.force_authenticate(user=user)
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1
