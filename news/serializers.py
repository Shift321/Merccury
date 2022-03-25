from rest_framework import serializers


class CreateNewsSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    text = serializers.CharField(max_length=255)
    image = serializers.ImageField()
    days = serializers.CharField(max_length=255)
