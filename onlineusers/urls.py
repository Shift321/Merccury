from onlineusers.views import ShowOnlineUsersAPIView
from django.urls import path

urlpatterns = [
    path("show-online-users", ShowOnlineUsersAPIView.as_view()),
]
