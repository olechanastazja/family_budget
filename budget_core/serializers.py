from rest_framework import serializers

from budget_core.models import Budget, BudgetItem, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class BudgetItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BudgetItem
        fields = '__all__'

    def create(self, validated_data):
        print('validate_data', validated_data)
        budget = validated_data['budget']
        amount = -validated_data['amount'] if validated_data['item_type'] == BudgetItem.EXPANSE else validated_data['amount']
        budget.recalculate_total(amount)
        return super().create(validated_data)


class BudgetSerializer(serializers.ModelSerializer):
    budget_items = BudgetItemSerializer(many=True, required=False)

    class Meta:
        model = Budget
        fields = '__all__'
        read_only_fields = ('id', 'date_created', 'owner', 'total', 'budget_items')
