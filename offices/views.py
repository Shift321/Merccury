from rest_framework import generics, status
from rest_framework import permissions
from rest_framework.permissions import AllowAny, IsAdminUser
from datetime import datetime, timedelta
from rest_framework.response import Response

from offices.models import Office


class ShowOfficeAdress(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def get(self, request):
        offices = Office.objects.filter()
        data = {"offices": []}
        for office in offices:
            info_of_office = {
                "id": office.id,
                "country": office.country,
                "city": office.city,
                "address": office.adress,
                "phone_number": office.phone_number,
                "email": office.email,
                "latitude": office.latitude,
                "longitude":office.longitude,

            }
            data["offices"].append(info_of_office)
        return Response(data, status=status.HTTP_200_OK)
