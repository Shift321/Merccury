from rest_framework import serializers
from api.models import User


class BlockUserSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=255, min_length=1)

    class Meta:
        model = User
        fields = ["id"]
