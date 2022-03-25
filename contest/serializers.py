from rest_framework import serializers
from django.core.files import File
import base64


from .models import Contest


class ParticipateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)

    class Meta:
        model = Contest


class CreateContestSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=255)
    base64_image = serializers.SerializerMethodField()
    price = serializers.CharField(max_length=255)
    time_to_expire = serializers.CharField(max_length=255)

    def get_base64_image(self, obj):
        f = open(obj.pic.path, "rb")
        image = File(f)
        data = base64.b64encode(image.read())
        return data


class VoteSerializer(serializers.Serializer):
    vote_for = serializers.CharField(max_length=255)
    post = serializers.CharField(max_length=255)


class CreatePostSerializer(serializers.Serializer):
    question = serializers.CharField(max_length=255)
    days = serializers.CharField(max_length=2)


class AddQuestionSerializer(serializers.Serializer):
    variation_of_anwser = serializers.CharField(max_length=255)
    post = serializers.CharField(max_length=255)
