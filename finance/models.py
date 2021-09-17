from datetime import date
from django.db import models
from django.db.models import fields
from django.db.models.deletion import CASCADE
from api.models import User


class Index(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE, verbose_name="Пользователь")
    purchase_date = models.DateField(
        auto_now_add=True, db_index=True, verbose_name="Дата покупки"
    )
    state = models.CharField(max_length=255, verbose_name="Статус")
    name = models.CharField(max_length=255, verbose_name="Название индекса")
    price = models.CharField(max_length=255, default=0, verbose_name="Цена")

    class Meta:
        def __str__(self):
            return self.name


class UserFinance(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE, verbose_name="Пользователь")
    balance = models.CharField(max_length=255, default=0, verbose_name="Баланс")
    price_of_all_indexes = models.CharField(
        max_length=255, default=0, verbose_name="Цена всех индексов"
    )

    class Meta:
        def __str__(self):
            return self.name


class HistoryOfTopUp(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE, verbose_name="Пользователь")
    summ = models.CharField(max_length=255, default=0, verbose_name="Сумма пополнения")
    time_of_payment = models.DateTimeField(
        auto_now_add=True, db_index=True, verbose_name="Время пополнения"
    )

    class Meta:
        def __str__(self):
            return self.name


class HistroyOfСonsumption(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE, verbose_name="Пользователь")
    summ = models.CharField(max_length=255, default=0, verbose_name="Сумма траты")
    time_of_spend = models.DateTimeField(
        auto_now_add=True, db_index=True, verbose_name="Время расхода"
    )

    class Meta:
        def __str__(self):
            return self.name
