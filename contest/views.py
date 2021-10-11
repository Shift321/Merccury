from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from datetime import datetime, timedelta

from api.utils import get_user
from .models import Contest
from .serializers import ParticipateSerializer, CreateContestSerializer


class ParticipateAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ParticipateSerializer

    @swagger_auto_schema(tags=["Contest"])
    def post(self, request):
        user = get_user(request)
        serializer = self.serializer_class(data=request.data)
        contest = serializer.get.data("name")
        where_to_participate = Contest.objects.get(name=contest)
        where_to_participate.users.add(user)
        Response({"Success": "Successfully participated"}, status=status.HTTP_200_OK)


class CreateContestAPIView(generics.GenericAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = CreateContestSerializer

    @swagger_auto_schema(tags=["Contest"])
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid()
        contest = Contest.objects.create()
        contest.name = serializer.data.get("name")
        contest.name = serializer.data.get("description")
        contest.name = serializer.data.get("price")
        contest.name = serializer.data.get("pic")
        days = serializer.data.get("time_to_expire")
        contest.expired_date = datetime.now() + timedelta(days=days)
        contest.save()
        return Response(
            {"Success": "Successfully created Contest"}, status=status.HTTP_200_OK
        )
