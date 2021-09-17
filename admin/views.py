from django_rest.permissions import IsAdminUser
from rest_framework import generics, status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from .serializer import BlockUserSerializer
from api.models import User


class BlockUserAPIView(generics.GenericAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = BlockUserSerializer

    @swagger_auto_schema(tags=["Admin"])
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            id = serializer.data.get("id")
            user = User.objects.get(id=id)
            user.is_blocked = True
            user.save()
            return Response(
                {"Success": f"User {user.username} has been blocked"},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"Error": "Serializer error"}, status=status.HTTP_400_BAD_REQUEST
            )
