from django.urls import path, include

from messagesender.views import SendMessageAPIView, ShowMessageAPIView


urlpatterns = [
    path("send-message", SendMessageAPIView.as_view()),
    path("show-message", ShowMessageAPIView.as_view()),
]
