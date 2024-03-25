from datetime import datetime
from django.db.models import Sum
from django.http import JsonResponse
from django.utils.timezone import make_aware
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Expense, Budget
from .permissions import IsOwnerOrReadOnly
from .serializers import ExpenseSerializer, BudgetSerializer
from drf_spectacular.utils import extend_schema


class ExpenseListCreateView(ListCreateAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly,)

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        user = self.request.user
        budget_id = self.request.data.get('category')
        try:
            budget = Budget.objects.get(user=user, id=budget_id)
            amount = serializer.validated_data.get('amount')
            if budget.amount >= amount:
                budget.amount_spent += amount
                budget.current_balance = budget.amount - budget.amount_spent
                budget.save()
                serializer.save(user=user)
            else:
                return Response({"detail": "Expense amount exceeds budget amount."}, status=status.HTTP_400_BAD_REQUEST)
        except Budget.DoesNotExist:
            return Response({"detail": "Budget does not exist"}, status=status.HTTP_400_BAD_REQUEST)    

class ExpenseDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly,)
    lookup_field = 'id'

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)



class BudgetListCreateView(ListCreateAPIView):
    serializer_class = BudgetSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly,)

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BudgetDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = BudgetSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly,)
    lookup_field = 'id'

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)


class AnalyticsView(APIView):
    permission_classes = (IsAuthenticated,)

    def get_expense_statistics(self, user):
        total_expenses = Expense.objects.filter(user=user).aggregate(total=Sum('amount'))['total'] or 0
        return total_expenses

    def get_budget_statistics(self, user):
        total_budgets = Budget.objects.filter(user=user).count()
        total_spent = Budget.objects.filter(user=user).aggregate(total=Sum('amount_spent'))['total'] or 0
        total_balance = Budget.objects.filter(user=user).aggregate(total=Sum('current_balance'))['total'] or 0
        return total_budgets, total_spent, total_balance

    def get(self, request):
        user = request.user
        expense_stats = self.get_expense_statistics(user)
        budget_stats = self.get_budget_statistics(user)
        data = {
            'expense_statistics': {
                'total_expenses': expense_stats,
            },
            'budget_statistics': {
                'total_budgets': budget_stats[0],
                'total_spent': budget_stats[1],
                'total_balance': budget_stats[2],
            }
        }
        return Response(data)