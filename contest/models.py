from django.db import models
from django.db.models.fields import related

from api.models import User


class Contest(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    description = models.CharField(max_length=255, verbose_name="Описание")
    price = models.CharField(max_length=255, verbose_name="Стоимость на вход")
    pic = models.ImageField(upload_to="", verbose_name="Аватар")
    users = models.ManyToManyField(User, blank=True, related_name="Участники")
    expired_date = models.DateTimeField(verbose_name="Дата окончания конкурса")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Конкурсы"
        verbose_name_plural = "Конкурсы"
        ordering = ["-expired_date"]
