from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from api.utils import Util, get_user
from .models import FAQ, Review

from feedback.serializers import (
    MakeFAQSerializer,
    SendFeedBackSerializer,
    MakeReviewSerializer,
)


class SendFeedBackAPIView(generics.GenericAPIView):
    serializer_class = SendFeedBackSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        name = serializer.data.get("name")
        email = serializer.data.get("email")
        phone_number = serializer.data.get("phone_number")
        subject = serializer.data.get("subject")
        message = serializer.data.get("message")
        data = {
            "email_subject": subject,
            "email_body": f"Номер телефона пользователя: {phone_number}\nИмя пользователя:{name}\nEmail ользователя:{email}\nСообщение:{message}",
            "to_email": "Komroden@gmail.com",
        }
        Util.send_email(data)
        return Response({"Success": "Succesfully sended"}, status=status.HTTP_200_OK)


class MakeReviewAPIView(generics.GenericAPIView):
    serializer_class = MakeReviewSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = get_user(request)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        text = serializer.data.get("text")
        review = Review.objects.create(user=user, text=text)
        review.save()
        return Response(
            {"Success": "Review created successfully"}, status=status.HTTP_200_OK
        )


class ShowReviewsAPIView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def get(self, request):
        reviews = Review.objects.filter()
        data = {"data": []}
        for review in reviews:
            last_data = {"user_info": "", "text": review.text}
            user_info = {
                "id": review.user.id,
                "username": review.user.username,
                "name": review.user.name,
                "surename": review.user.second_name,
            }
            last_data["user_info"].append(user_info)
            data["data"].append(last_data)
        return Response(data, status=status.HTTP_200_OK)


class ShowFAQAPIView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def get(self, request):
        faqs = FAQ.objects.filter()
        data = {"data": []}
        for faq in faqs:
            last_data = {"question": faq.question, "anwser": faq.anwser}
            data["data"].append(last_data)
        return Response(data, status=status.HTTP_200_OK)
