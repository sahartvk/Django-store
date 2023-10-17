from django.urls import path
from . import views

urlpatterns = [
    path('register', views.RegisterView.as_view(), name='register_page'),
    path('activate-account/<email_active_code>', views.ActivateView.as_view(), name='activate_account'),
    path('login', views.LoginView.as_view(), name='login_page'),
    path('logout', views.LogoutView.as_view(), name='logout_page'),
    path('forget-password', views.ForgotPasswordFormView.as_view(), name='forget_password_page'),
    path('reset-password/<email_active_code>', views.ResetPasswordView.as_view(), name='reset_password_page'),
]
