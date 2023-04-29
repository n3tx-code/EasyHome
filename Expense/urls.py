from django.urls import path

from Expense.views import ExpenseCreationView, ExpenseDetailView

urlpatterns = [
    path('new', ExpenseCreationView.as_view(), name='expense_creation'),
    path('<int:pk>', ExpenseDetailView.as_view(), name='expense_detail'),
]
