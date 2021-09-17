from .views import (
    AddMoreUserInfoAPIView,
    PasswordTokenCheckAPI,
    RegistrationAPIView,
    LoginAPIView,
    LogoutAPIView,
    ChangePasswordAPIView,
    RequestPasswordResetEmail,
    SetNewPasswordAPIView,
    VerifyEmail,
    VerifySMSCode,
)
from django.urls import path


from rest_framework import permissions


urlpatterns = [
    path("register", RegistrationAPIView.as_view(), name="Register"),
    path("login", LoginAPIView.as_view(), name="Login"),
    path("logout", LogoutAPIView.as_view(), name="Logout"),
    path("change-password", ChangePasswordAPIView.as_view(), name="Change-password"),
    path("email-verify", VerifyEmail.as_view(), name="email-verify"),
    path("sms-verify", VerifySMSCode.as_view(), name="SMS-verify"),
    path("add-more-info", AddMoreUserInfoAPIView.as_view(), name="get-partner-info"),
    path(
        "password-reset-complete",
        SetNewPasswordAPIView.as_view(),
        name="password-reset-compete",
    ),
    path(
        "request-reset-email",
        RequestPasswordResetEmail.as_view(),
        name="request-reset-email",
    ),
    path(
        "password-reset/<uidb64>/<token>/",
        PasswordTokenCheckAPI.as_view(),
        name="password-reset-confirm",
    ),
]
