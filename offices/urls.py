from django.urls import path

from .views import ShowOfficeAdress


urlpatterns = [
    path("show-office-adress", ShowOfficeAdress.as_view()),
]
