from django.contrib.auth import views as authViews
from django.urls import path

from . import views as user_views

urlpatterns = [
    path('logout/', authViews.LogoutView.as_view(), name='logout'),

    path('password-change/', authViews.PasswordChangeView.as_view(), name='password_change'),
    path('password-change/done/', authViews.PasswordChangeDoneView.as_view(), name='password_change_done'),

    path('password-reset/', authViews.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', authViews.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', authViews.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('password-reset/complete/', authViews.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # url from the User module
    path('sign-in/', user_views.SignInView.as_view(), name='signIn'),
    path('login/', user_views.LoginView.as_view(), name='login'),
]
