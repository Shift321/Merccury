from django.db import models
from django.db.models.deletion import CASCADE
from api.models import User


class Message(models.Model):
    sender = models.ForeignKey(
        User, on_delete=CASCADE, null=True, blank=True, related_name="Отправитель"
    )
    reciever = models.ForeignKey(
        User, on_delete=CASCADE, null=True, blank=True, related_name="Получатель"
    )
    msg_content = models.CharField(
        blank=True, null=True, max_length=255, verbose_name="Сообщение"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ("created_at",)


class Dialog(models.Model):
    messages = models.ManyToManyField("messagesender.Message", verbose_name="messages")
    users = models.ManyToManyField("api.User", verbose_name="users")
