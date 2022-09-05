from django.conf import settings
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Budget(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    name = models.CharField(max_length=50, blank=False)
    total = models.DecimalField(
        max_digits=6, decimal_places=2, blank=True, default=0.0
    )
    shared_with = models.ManyToManyField(
        to=settings.AUTH_USER_MODEL, related_name="budgets", blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def recalculate_total(self, amount):
        self.total += amount
        self.save()  # maybe use update fields here, make sure if needed


class BudgetItem(models.Model):
    EXPANSE = 'EXPANSE'
    INCOME = 'INCOME'
    ITEM_TYPE = [
        (EXPANSE, 'EXPANSE'),
        (INCOME, 'INCOME'),
    ]
    name = models.CharField(max_length=50, blank=False)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE
    )
    amount = models.DecimalField(
        max_digits=6, decimal_places=2, blank=True, null=True
    )
    item_type = models.CharField(
        max_length=32,
        choices=ITEM_TYPE,
        default=INCOME
    )
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, related_name='budget_items')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
