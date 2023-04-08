from django.urls import path, include

urlpatterns = [
    path('user/', include('User.urls')),
    path('expense-record/', include('ExpenseRecord.urls')),
]
