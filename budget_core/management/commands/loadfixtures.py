import json
import os
import random
import uuid

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from budget_core.models import Budget, BudgetItem, Category

PATH = os.path.join(os.path.dirname(__file__), "..", "..", "..", "fixtures")


def load_users():
    with open(os.path.join(PATH, "users.json")) as f:
        data = json.load(f)
        if User.objects.filter(username=data[0]["username"]).exists():
            return list(User.objects.all()), "Users already exist in the database"
        users = []
        for user_data in data:
            user = User.objects.create(**user_data)
            user.set_password(user_data["password"])
            user.save()
            users.append(user)
        return users, "Users successfully loaded"


def load_categories():
    with open(os.path.join(PATH, "categories.json")) as f:
        data = json.load(f)
        return [Category.objects.create(**category) for category in data]


def load_budgets(users):
    budgets = []
    with open(os.path.join(PATH, "budgets.json")) as f:
        data = json.load(f)
        for budget_data in data:
            owner, shared_with = random.sample(users, 2)
            budget = Budget.objects.create(**budget_data, owner=owner)
            budget.shared_with.add(shared_with)
            budgets.append(budget)
        return budgets


def create_budget_items(budget, categories):
    return [
        BudgetItem.objects.create(
            name=f"{uuid.uuid4()}",
            category=random.choice(categories),
            budget=budget,
            item_type=random.choice([BudgetItem.EXPENSE, BudgetItem.INCOME]),
            amount=round(random.random(), 2),
        )
        for _ in range(4)
    ]


class Command(BaseCommand):
    help = "Loads fixtures (users, budgets, categories) into the database"

    @transaction.atomic
    def handle(self, *args, **options):
        try:
            users, message = load_users()
            self.stdout.write(self.style.NOTICE(message))
            categories = load_categories()
            budgets = load_budgets(users)
            [create_budget_items(budget, categories) for budget in budgets]
            self.stdout.write(self.style.SUCCESS("Successfully loaded all fixtures!!!"))
        except Exception as e:
            raise CommandError(f"{e} :(")
