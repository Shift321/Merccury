from admin.views import BlockUserAPIView
from django.urls import path

urlpatterns = [
    path("block-user", BlockUserAPIView.as_view()),
]
