from datetime import datetime
from django.db.models import Sum
from django.http import JsonResponse
from django.utils.timezone import make_aware
from rest_framework.views import APIView
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
        serializer.save(user=self.request.user)


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
    
    permission_classes = [IsAuthenticated]

    def get_total_expenses(self, start_date, end_date):
        total_expenses = Expense.objects.filter(
            user=self.request.user,
            date__range=(start_date, end_date)
        ).aggregate(total=Sum('amount'))['total'] or 0
        return total_expenses

    def get_category_expenses(self, start_date, end_date):
        category_expenses = Expense.objects.filter(
            user=self.request.user,
            date__range=(start_date, end_date)
        ).values('category').annotate(total=Sum('amount'))
        return category_expenses

    def get_remaining_budgets(self):
        remaining_budgets = Budget.objects.filter(user=self.request.user).values('category', 'amount')
        return remaining_budgets

    def get(self, request):
        start_date_str = request.GET.get('start_date')
        end_date_str = request.GET.get('end_date')

        # Convert date strings to datetime objects
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

        # Make datetime objects aware
        start_date = make_aware(start_date)
        end_date = make_aware(end_date)

        total_expenses = self.get_total_expenses(start_date, end_date)
        category_expenses = self.get_category_expenses(start_date, end_date)
        remaining_budgets = self.get_remaining_budgets()


        data = {
            'total_expenses': total_expenses,
            'category_expenses': list(category_expenses),
            'remaining_budgets': list(remaining_budgets)
        }
        return JsonResponse(data)


