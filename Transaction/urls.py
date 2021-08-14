from django.urls import path

from Transaction.views import TransactionAddView

urlpatterns = [
    path('add/', TransactionAddView.as_view(), name='transaction-add')
]
