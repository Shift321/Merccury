from admin.utils import is_blocked
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from api.models import User

from .serializers import GetPartnerDataSerializer, GetAllPartnerDataSerializer
from finance.utils import get_user

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class GetAllPartnersDataAPIView(generics.GenericAPIView):
    serializer_class = GetAllPartnerDataSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=["Marketing"])
    def get(self, request):
        if not is_blocked(request):
            user = get_user(request)
            queryset = User.objects.filter(id_of_invited=user.id)
            if queryset.exists():
                data = {}
                for i in range(queryset.count()):
                    data[i] = {
                        "name": f"{queryset[i].name}",
                        "surename": f"{queryset[i].second_name}",
                        "phone_number": f"{queryset[i].phone_number}",
                        "email": f"{queryset[i].email}",
                    }
                print(data)
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"Error": "you dont have partners"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                {"Error": "your account blocked try to connect with admin"},
                status=status.HTTP_404_NOT_FOUND,
            )


class GetPartnerData(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GetPartnerDataSerializer

    @swagger_auto_schema(tags=["Marketing"])
    def get(self, request):
        if not is_blocked:

            user = get_user(request)
            partner = User.objects.filter(id=user.id_of_invited)
            if partner.exists():
                data = GetPartnerDataSerializer(partner[0]).data
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response({"error", "partner doesnot exists"})
        else:
            return Response(
                {"Error": "your account blocked try to connect with admin"},
                status=status.HTTP_404_NOT_FOUND,
            )
