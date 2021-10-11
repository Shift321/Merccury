from django.urls import path

from contest.views import CreateContestAPIView, ParticipateAPIView


urlpatterns = [
    path("create-contest", CreateContestAPIView.as_view()),
    path("participate-in-contest", ParticipateAPIView.as_view()),
]
