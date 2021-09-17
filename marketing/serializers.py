from django.db.models import fields
from rest_framework import serializers

from api.models import User


class GetPartnerDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "name", "second_name"]


class GetAllPartnerDataSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ["email", "name", "second_name", "phone_number"]
