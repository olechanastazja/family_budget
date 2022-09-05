import random
from datetime import date, time
import uuid

from django.contrib.auth.models import User
import pytest
from rest_framework.test import APIClient

from budget_core.models import Budget, BudgetItem, Category


@pytest.fixture
def api_client():
    return APIClient


@pytest.fixture
def user():
    return User.objects.create(username="test_user", email="email@gmail.com")


@pytest.fixture
def user2():
    return User.objects.create(username="test_user2", email="email2@gmail.com")


@pytest.fixture()
def users(user, user2):
    return [user, user2]


# ------------------ Budget ------------------ #


@pytest.fixture
def budget_factory():
    # Closure
    def create_budget(name, owner, shared_with):
        budget = Budget.objects.create(name=name, owner=owner, total=666)
        budget.shared_with.set(shared_with)
        return budget

    return create_budget


@pytest.fixture
def budget_user1_only(budget_factory, user, user2):
    return budget_factory("User1 budget", owner=user, shared_with=[])


@pytest.fixture
def budget_user1_shared_with_user2(budget_factory, user, user2):
    return budget_factory(
        "User1 budget shared with User2", owner=user, shared_with=[user2]
    )


@pytest.fixture
def budgets(budget_user1_only, budget_user1_shared_with_user2):
    return [budget_user1_only, budget_user1_shared_with_user2]


# ------------------ Category ------------------ #


@pytest.fixture()
def category_name():
    return "category"


@pytest.fixture()
def categories(category_name):
    return [
        Category.objects.create(name=f"{category_name} {uuid.uuid4()}")
        for _ in range(4)
    ]


# ------------------ BudgetItem ------------------ #


@pytest.fixture
def budget_item_data(budget_user1_only, categories):
    return {
        "name": f"{uuid.uuid4()}",
        "budget": budget_user1_only.id,
        "category": categories[0].id,
        "amount": 66.6,
    }


@pytest.fixture
def budget_expense(budget_item_data, categories, budget_user1_only):
    budget_item_data["budget"] = budget_user1_only
    budget_item_data["category"] = categories[0]
    budget_item_data["item_type"] = BudgetItem.EXPENSE
    return BudgetItem.objects.create(**budget_item_data)


@pytest.fixture
def budget_income(budget_item_data, categories, budget_user1_only):
    budget_item_data["budget"] = budget_user1_only
    budget_item_data["category"] = categories[1]
    budget_item_data["item_type"] = BudgetItem.INCOME
    return BudgetItem.objects.create(**budget_item_data)


@pytest.fixture
def budget_items(budget_expense, budget_income):
    return [budget_expense, budget_income]
