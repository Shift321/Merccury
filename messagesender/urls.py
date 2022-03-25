from django.urls import path, include

from messagesender.views import (
    DeleteDialogAPIView,
    SendMessageAPIView,
    ShowDialogAPIView,
    ShowAllDialogsAPIView,
)


urlpatterns = [
    path("send-message/<int:id>", SendMessageAPIView.as_view()),
    path("show-dialog/<int:id>", ShowDialogAPIView.as_view()),
    path("show-all-dialogs", ShowAllDialogsAPIView.as_view()),
    path("delete-dialog/<int:id>", DeleteDialogAPIView.as_view()),
]
