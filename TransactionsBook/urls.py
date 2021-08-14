from django.urls import path

from .views import TransactionBookView, TransactionBookCreateView

urlpatterns = [
    path('', TransactionBookView.as_view(), name='transactions-book'),
    path('create/', TransactionBookCreateView.as_view(), name='transactions-book-create')
]
