from rest_framework import serializers
from .models import Expense, Budget


class ExpenseSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    budget_amount = serializers.ReadOnlyField(source='category.amount')
    budget_balance = serializers.ReadOnlyField(source='category.current_balance')
    budget_spent = serializers.ReadOnlyField(source='category.amount_spent')

    class Meta:
        model = Expense
        fields = ['id', 'amount', 'category', 'category_name', 'budget_amount', 'budget_balance',
                  'budget_spent', 'description', 'date']       


class BudgetSerializer(serializers.ModelSerializer):
    amount_spent = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    current_balance = serializers.SerializerMethodField()

    class Meta:
        model = Budget
        fields = ['id', 'name', 'amount', 'amount_spent', 'current_balance']

    def get_current_balance(self, obj):
        return obj.amount - obj.amount_spent
