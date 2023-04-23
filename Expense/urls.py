from django.urls import path

from Expense.views import ExpenseCreationView

urlpatterns = [
    path('new', ExpenseCreationView.as_view(), name='expense_creation'),
]
