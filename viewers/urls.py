from django.urls import path

from .views import ShowViewers


urlpatterns = [
    path("show-views", ShowViewers.as_view()),
]
