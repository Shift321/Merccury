from django.urls import path

from contest.views import (
    CreateContestAPIView,
    CreatePostAPIView,
    ParticipateAPIView,
    ShowContestAPIView,
    VoteAPIView,
    ShowLastContestsAPIView,
    ShowPostAPIView,
)


urlpatterns = [
    path("create-contest", CreateContestAPIView.as_view()),
    path("participate-in-contest", ParticipateAPIView.as_view()),
    path("vote", VoteAPIView.as_view()),
    path("create-post", CreatePostAPIView.as_view()),
    path("show-post", ShowPostAPIView.as_view()),
    path("show-contest/<int:id>/", ShowContestAPIView.as_view()),
    path("show-last-contests/", ShowLastContestsAPIView.as_view()),
]
