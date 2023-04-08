from django.urls import path

from ExpenseRecord.views import ExpenseRecordCreationView, ExpenseRecordDetailView, ExpenseRecordCheckCodeView

urlpatterns = [
    path('new', ExpenseRecordCreationView.as_view(), name='expense_record_creation'),
    path('', ExpenseRecordDetailView.as_view(), name='expense_record_detail'),
    path('code', ExpenseRecordCheckCodeView.as_view(), name='expense_record_check_code'),
]
