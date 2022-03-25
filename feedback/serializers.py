from rest_framework import serializers


class SendFeedBackSerializer(serializers.Serializer):
    name = serializers.CharField()
    email = serializers.CharField()
    phone_number = serializers.CharField()
    subject = serializers.CharField()
    message = serializers.CharField()


class MakeReviewSerializer(serializers.Serializer):
    text = serializers.CharField()


class MakeFAQSerializer(serializers.Serializer):
    text = serializers.CharField()
    user = serializers.CharField()
