from django.urls import path
from .views import ExpenseCreateView, ExpenseListView, ExpenseAnalyticsView

urlpatterns = [
    path('expenses/', ExpenseListView.as_view(), name='list_expenses'),
    path('expenses/create/', ExpenseCreateView.as_view(), name='create_expense'),
    path('expenses/analytics/', ExpenseAnalyticsView.as_view(), name='expense_analytics'),
]

