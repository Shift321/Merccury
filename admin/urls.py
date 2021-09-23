from admin.views import BlockUserAPIView, UnBlockUserAPIView
from django.urls import path

urlpatterns = [
    path("block-user", BlockUserAPIView.as_view()),
    path("unblock-user", UnBlockUserAPIView.as_view()),
]
