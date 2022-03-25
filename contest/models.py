from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.expressions import Case
from django.db.models.fields import related

from api.models import User

STATUS_CHOICES = (
    ("active", "Активен"),
    ("end", "Закончился"),
)


class Contest(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    description = models.CharField(max_length=255, verbose_name="Описание")
    price = models.CharField(max_length=255, verbose_name="Стоимость на вход")
    pic = models.ImageField(upload_to="", verbose_name="Аватар")
    users = models.ManyToManyField(User, blank=True, related_name="Участники")
    expired_date = models.DateTimeField(verbose_name="Дата окончания конкурса")
    published_date = models.DateTimeField(auto_now_add=True)
    winner = models.ManyToManyField(User, blank=True, verbose_name="Победитель")
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default="active")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Конкурс"
        verbose_name_plural = "Конкурсы"
        ordering = ["-expired_date"]


class Answers(models.Model):
    variation_of_answer = models.CharField(max_length=255)
    users = models.ManyToManyField(
        User, blank=True, verbose_name="Пользователи", related_name="Answers"
    )

    def __str__(self):
        return self.variation_of_answer

    class Meta:
        verbose_name = "Вариант ответа"


class Post(models.Model):
    question = models.CharField(max_length=255, verbose_name="Вопрос")
    date_of_creation = models.DateTimeField(auto_now_add=True)
    date_of_expired = models.DateTimeField()
    users = models.ManyToManyField(User, blank=True, verbose_name="Проголосовавшие")
    answers = models.ManyToManyField(Answers, blank=True, verbose_name="Ответы")

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = "Опрос"
        verbose_name_plural = "Опросы"
