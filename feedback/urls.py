from django.urls import path
from .views import (
    MakeReviewAPIView,
    SendFeedBackAPIView,
    ShowFAQAPIView,
    ShowReviewsAPIView,
)

urlpatterns = [
    path("send-feedback", SendFeedBackAPIView.as_view(), name="SendFeedback"),
    path("make-review", MakeReviewAPIView.as_view(), name="MakeReview"),
    path("show-reviews", ShowReviewsAPIView.as_view(), name="ShowReview"),
    path("show-faqs", ShowFAQAPIView.as_view(), name="ShowReview"),
]
