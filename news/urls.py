from django.urls import path

from news.views import CreateNewsAPIView, ShowNewsAPIView


urlpatterns = [
    path("create-news", CreateNewsAPIView.as_view()),
    path("show-news", ShowNewsAPIView.as_view()),
]
