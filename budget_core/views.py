from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from budget_core.models import Budget, BudgetItem, Category
from budget_core.permissions import IsBudgetOwnerOrReadOnly
from budget_core.serializers import (
    BudgetSerializer,
    BudgetItemSerializer,
    CategorySerializer,
)


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["name"]
    permission_classes = [IsAuthenticated]


class BudgetViewSet(viewsets.ModelViewSet):
    serializer_class = BudgetSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["name"]
    permission_classes = [IsBudgetOwnerOrReadOnly]

    def get_queryset(self):
        """
        This view should return a list of all the budget items
        for the currently authenticated user.
        """
        user = self.request.user
        return Budget.objects.filter(Q(owner=user) | Q(shared_with__id=user.id))

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class BudgetItemViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    serializer_class = BudgetItemSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ("budget", "category", "name")
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list of all the budget items
        for the currently authenticated user.
        """
        user = self.request.user
        return BudgetItem.objects.filter(
            Q(budget__owner=user) | Q(budget__shared_with__id=user.id)
        )

    def perform_destroy(self, instance):
        """
        Recalculate the budget accordingly based on the item to be removed.
        """
        budget = instance.budget
        amount = (
            -instance.amount
            if instance.item_type == BudgetItem.INCOME
            else instance.amount
        )
        budget.recalculate_total(amount)
        super().perform_destroy(instance)
