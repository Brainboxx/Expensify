from django.contrib import admin
from .models import Expense, Budget


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('category', 'amount',)


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount',)

