from django.urls import path
from .views import GetAllPartnersDataAPIView, GetPartnerData

urlpatterns = [
    path("get-all-partners-info", GetAllPartnersDataAPIView.as_view()),
    path("get-partner-info", GetPartnerData.as_view(), name="get-partner-info"),
]
