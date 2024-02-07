from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from users.views import UserRegistrationView, LogoutView
from expenses.views import (ExpenseListCreateView, 
                            ExpenseDetailView, 
                            BudgetListCreateView, 
                            BudgetDetailView)
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from expenses.views import AnalyticsView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('expenses/', ExpenseListCreateView.as_view(), name='expense-list-create'),
    path('expenses/<int:id>', ExpenseDetailView.as_view(), name='expense-detail'),
    path('budgets/', BudgetListCreateView.as_view(), name='budget-list-create'),
    path('budgets/<int:id>', BudgetDetailView.as_view(), name='budget-detail'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/docs/', SpectacularSwaggerView.as_view(url_name="schema")),
    path('analytics/', AnalyticsView.as_view(), name='analytics'),
]
