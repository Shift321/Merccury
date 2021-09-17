from onlineusers.models import OnlineUserActivity
from rest_framework import serializers


class ShowOnlineUsersSerializer(serializers.Serializer):
    class Meta:
        model = OnlineUserActivity
        fields = ["users"]
