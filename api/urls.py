from api.serializers import IsVerified
from .views import (
    AddMoreUserInfoAPIView,
    GenerateRefLink,
    PasswordTokenCheckAPI,
    PutAwayFromBlackListAPIView,
    PutOnBlackListAPIView,
    RegistrationAPIView,
    LoginAPIView,
    LogoutAPIView,
    ChangePasswordAPIView,
    RequestPasswordResetEmail,
    SetNewPasswordAPIView,
    ShowDataOfUserAPIView,
    UploadAvatar,
    VerifyEmail,
    VerifySMSCode,
    IsVerify,
    ShowMyDataAPIView,
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
    path("isverify", IsVerify.as_view(), name="isverify"),
    path("add-more-info", AddMoreUserInfoAPIView.as_view(), name="get-partner-info"),
    path("block-user", PutOnBlackListAPIView.as_view(), name="get-partner-info"),
    path("show-my-data", ShowMyDataAPIView.as_view(), name="show-data-of-user"),
    path(
        "show-data-of-user/<int:id>",
        ShowDataOfUserAPIView.as_view(),
        name="show-data-of-user",
    ),
    path("upload-avatar", UploadAvatar.as_view(), name="upload-avatar"),
    path("generate-link", GenerateRefLink.as_view(), name="upload-avatar"),
    path(
        "unblock-user", PutAwayFromBlackListAPIView.as_view(), name="get-partner-info"
    ),
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
