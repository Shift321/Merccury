from onlineusers.models import OnlineUserActivity
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import ShowOnlineUsersSerializer
from drf_yasg.utils import swagger_auto_schema


class ShowOnlineUsersAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ShowOnlineUsersSerializer

    @swagger_auto_schema(tags=["OnlineUsers"])
    def get(self, request):
        user_activity_objects = OnlineUserActivity.get_user_activities()
        online_users = {}
        for i in range(user_activity_objects.count()):
            online_users[i] = {"username": user_activity_objects[i].user.username}

        number_of_actrive_users = user_activity_objects.count()
        online_users.update({"number_of_online_users": number_of_actrive_users})
        return Response(
            online_users,
            status=status.HTTP_200_OK,
        )
