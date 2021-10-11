from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema

from api.utils import get_user
from api.models import User
from .models import Message
from .serializer import SendMessageSerializer, ShowMessageSerializer


class SendMessageAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SendMessageSerializer

    @swagger_auto_schema(tags=["Messages"])
    def post(self, request):
        sender = get_user(request)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.data.get("username")
        message_text = serializer.data.get("message")
        reciever = User.objects.get(username=username)
        message = Message.objects.create()
        message.sender = sender
        message.reciever = reciever
        message.msg_content = message_text
        message.save()
        return Response(
            {"Success": "Message send successfully"}, status=status.HTTP_200_OK
        )


class ShowMessageAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ShowMessageSerializer

    @swagger_auto_schema(tags=["Messages"])
    def get(self, request):
        user = get_user(request)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        dialog_user = serializer.data.get("username")
        username_dialog_user = User.objects.get(username=dialog_user)
        dialog = Message.objects.filter(
            Q(sender=user, reciever=username_dialog_user)
            | Q(sender=username_dialog_user, reciever=user),
        )
        data = {}
        for i in range(dialog.count()):
            data[str(dialog[i].created_at)] = {
                "Sender": dialog[i].sender.username,
                "Reciever": dialog[i].reciever.username,
                "message": dialog[i].msg_content,
            }
        return Response(data, status=status.HTTP_200_OK)
