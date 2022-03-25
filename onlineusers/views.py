from api.models import User
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from drf_yasg.utils import swagger_auto_schema


class ShowOnlineUsersAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    @swagger_auto_schema(tags=["OnlineUsers"])
    def get(self, request):
        users = User.objects.filter()
        data = {"data": []}
        for user in users:
            serializer_data = self.serializer_class(user)
            if serializer_data.data["online"] == True:
                data["data"].append(serializer_data.data)

        return Response(data, status=status.HTTP_200_OK)
