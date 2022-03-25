from django.db import reset_queries
from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status

from api.utils import get_user
from viewers.models import Viewer
from drf_yasg.utils import swagger_auto_schema


class ShowViewers(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(tags=["Viewers"])
    def get(self, request):
        user = get_user(request)
        viewers = Viewer.objects.select_related("viewer").filter(user=user)
        data = {}
        for i in range(viewers.count()):
            data[i] = {
                "viewer username": viewers.viewer.username,
                "time of view": viewers.view_at,
                "name": "",
                "avata": "",
                "online": "",
                "age": "",
                "id": "",
            }
        return Response(data, status=status.HTTP_200_OK)
