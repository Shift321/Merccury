from django.db import models
from django.db.models.deletion import CASCADE


class Viewer(models.Model):
    user = models.ForeignKey(
        "api.User",
        on_delete=CASCADE,
        related_name="Viewers",
        verbose_name="Пользователь",
    )
    viewer = models.ForeignKey(
        "api.User", on_delete=CASCADE, related_name="viewer", verbose_name="Смотрящий"
    )
    view_at = models.DateTimeField(auto_now_add=True)
