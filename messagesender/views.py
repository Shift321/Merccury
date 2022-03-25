from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from api.utils import get_user
from api.models import User
from .models import Dialog, Message
from .serializer import (
    SendMessageSerializer,
)
from onlineusers.serializers import UserSerializer


class SendMessageAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SendMessageSerializer

    @swagger_auto_schema(tags=["Messages"])
    def post(self, request, id):
        sender = get_user(request)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        message_text = serializer.data.get("message")
        reciever = User.objects.get(id=id)
        dialog = Dialog.objects.filter(users__in=[sender, reciever]).first()
        if not dialog:
            dialog = Dialog.objects.create()
            dialog.users.add(sender, reciever)
        message = Message.objects.create(
            sender=sender, reciever=reciever, msg_content=message_text
        )
        dialog.messages.add(message)
        return Response(
            {"Success": "Message send successfully"}, status=status.HTTP_200_OK
        )


class ShowDialogAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_online = UserSerializer

    @swagger_auto_schema(tags=["Messages"])
    def get(self, request, id):

        user = get_user(request)
        id_of_dialog = id
        dialog = Dialog.objects.filter(id=id_of_dialog)
        if dialog.exists():
            dialog = dialog[0]
            reciever = dialog.users.exclude(id=user.id).first()
            serializer_data = self.serializer_online(reciever)
            status_of_user = serializer_data.data["online"]
            last_seen = serializer_data.data["last_seen"]
            if not reciever:
                print("no users")
                reciever = user
            messages = dialog.messages.all()
            for message in messages:
                message.is_read = True
                message.save()
            data = {
                "messages": [],
                "info_of_reciver": {
                    "id": reciever.id,
                    "username": reciever.username,
                    "date_of_birth": reciever.date_of_birth,
                    "avatar": "avatar",
                    "status": status_of_user,
                    "last_seen": last_seen,
                },
            }
            for message in dialog.messages.all():
                data_of_messages = {
                    "id": message.id,
                    "text": message.msg_content,
                    "time_send": message.created_at,
                    "is_read": message.is_read,
                    "sender_id": message.sender.id,
                }
                data["messages"].append(data_of_messages)
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"Error": "Dialog doesn't exists"}, status=status.HTTP_404_NOT_FOUND
            )


class ShowAllDialogsAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=["Messages"])
    def get(self, request):
        user = get_user(request)
        dialogs = Dialog.objects.filter(users=user)
        data = {"item": []}
        for dialog in dialogs:
            reciever = dialog.users.exclude(id=user.id).first()
            last_message = dialog.messages.last()
            data_of_chat = {
                "id": dialog.id,
                "userID": user.id,
                "recieverID": reciever.id,
                "recieverName": reciever.username,
                "date_of_last_message": last_message.created_at,
                "text_of_last_message": last_message.msg_content,
            }
            data["item"].append(data_of_chat)
        return Response(data, status=status.HTTP_200_OK)


class CountUnreadMessages(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=["Messages"])
    def get(self, request):
        user = get_user(request)
        dialogs = Dialog.objects.filter(users=user)
        messages = dialogs.messages.exclude(sender=user).all()
        counter = 0
        for message in messages:
            if message.is_read == False:
                counter += 1
        return Response({"missed messages": f"{counter}"}, status=status.HTTP_200_OK)


class DeleteDialogAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=["Messages"])
    def delete(self, request, id):
        dialog = Dialog.objects.get(id=id)
        dialog.delete()
        return Response(
            {"Success": "Dialog successfully deleted"}, status=status.HTTP_200_OK
        )
