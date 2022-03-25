from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAdminUser
from datetime import datetime, timedelta
from rest_framework.response import Response

from .models import News
from .serializers import CreateNewsSerializer


class CreateNewsAPIView(generics.GenericAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = CreateNewsSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        text = serializer.data.get("text")
        name = serializer.data.get("name")
        days = serializer.data.get("days")
        news = News.objects.create()
        news.name = name
        news.text = text
        news.expired = datetime.now + timedelta(days=days)
        news.save()
        return Response(
            {"Success": "News created succesfuly"}, status=status.HTTP_201_CREATED
        )


class ShowNewsAPIView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def get(self, request):
        news = News.objects.filter().order_by("-created_at")
        data = {"news": []}
        for i in range(news.count()):
            data_first = {
                "id": news[i].id,
                "name": news[i].name,
                "text": news[i].text,
                "created_at": news[i].created_at,
                "expired": news[i].expired,
                "avatar": "avatar",
            }
            data["news"].append(data_first)
        return Response(data, status=status.HTTP_200_OK)
