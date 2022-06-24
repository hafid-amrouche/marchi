from django.urls import path
from . import views

urlpatterns=[
  path("", views.accounts, name="accounts"),
  path("register/", views.register, name="register"),
  path("log-in/", views.log_in, name="log-in"),
  path("log-out/", views.log_out, name="log-out"),
  path("dashboard/", views.dashboard, name="dashboard"),
  path("forgot-password/", views.forgot_password, name="forgot_password"),
  path("activate/<uidb64>/<token>/", views.activate, name='activate'),
  path("reset-password", views.reset_password, name='reset_password'),
  path("reset-password-validation/<uidb64>/<token>/", views.reset_password_validation, name='reset_password_validation'),
]