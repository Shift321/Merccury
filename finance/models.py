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

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Индексы"
        verbose_name = "Индекс"


class UserFinance(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE, verbose_name="Пользователь")
    balance = models.CharField(max_length=255, default=0, verbose_name="Баланс")
    price_of_all_indexes = models.CharField(
        max_length=255, default=0, verbose_name="Цена всех индексов"
    )

    class Meta:
        verbose_name_plural = "Финансовая информация пользователей"
        verbose_name = "Финансовая информация пользователей"

    def __str__(self):
        return self.name


class HistoryOfTopUp(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE, verbose_name="Пользователь")
    summ = models.CharField(max_length=255, default=0, verbose_name="Сумма пополнения")
    time_of_payment = models.DateTimeField(
        auto_now_add=True, db_index=True, verbose_name="Время пополнения"
    )

    class Meta:
        verbose_name_plural = "История пополнения пользователей"
        verbose_name = "История пополнения пользователя"

    def __str__(self):
        return "Сумма пополнения: " + self.summ


class HistroyOfСonsumption(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE, verbose_name="Пользователь")
    summ = models.CharField(max_length=255, default=0, verbose_name="Сумма траты")
    time_of_spend = models.DateTimeField(
        auto_now_add=True, db_index=True, verbose_name="Время расхода"
    )

    class Meta:
        verbose_name_plural = "История расхода пользователей"
        verbose_name = "История расхода пользователя"

    def __str__(self):
        return "Сумма трат: " + self.summ
