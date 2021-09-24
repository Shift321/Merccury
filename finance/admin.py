from django.contrib.auth.models import User
from api.admin import UserAdmin
from django.contrib import admin
from django.db import models
from .models import (
    HistoryOfTopUp,
    Index,
    SharingMoney,
    UserFinance,
    HistroyOfСonsumption,
)


class HistoryAdmin(UserAdmin):
    list_filter = UserAdmin.list_filter + ("user",)

    def summ(self, obj):
        return obj.summ

    def date_of_operation(self, obj):
        return obj.date_of_operation

    def username(self, obj):
        return obj.user.username

    username.short_description = "Логин"
    list_display = ["username", "summ", "date_of_operation"]


class IndexAdmin(UserAdmin):
    list_filter = UserAdmin.list_filter + (
        "user",
        "name",
    )

    def username(self, obj):
        return obj.user.username

    username.short_description = "Логин"

    def price(self, obj):
        return obj.price

    def state(self, obj):
        return obj.state

    def purchase_date(self, obj):
        return obj.purchase_date

    def name(self, obj):
        return obj.name

    list_display = ["username", "price", "state", "name", "purchase_date"]


class FinanceAdmin(UserAdmin):
    list_filter = UserAdmin.list_filter + ("user",)

    def username(self, obj):
        return obj.user.username

    username.short_description = "Логин"

    def balance(self, obj):
        return obj.balance

    def price_of_all(self, obj):
        return obj.price_of_all_indexes

    list_display = ["username", "balance", "price_of_all"]


class SharingMoneyAdmin(UserAdmin):
    list_filter = UserAdmin.list_filter + (
        "user",
        "status",
        "way_to_pay",
    )

    def username(self, obj):
        return obj.user.username

    def summ(self, obj):
        return obj.summ

    def way_to_pay(self, obj):
        return obj.way_to_pay

    def status(self, obj):
        return obj.status

    def date(self, obj):
        return obj.date_of_operation

    list_display = ["username", "summ", "way_to_pay", "status", "date"]


admin.site.register(UserFinance, FinanceAdmin)
admin.site.register(HistoryOfTopUp, HistoryAdmin)
admin.site.register(HistroyOfСonsumption, HistoryAdmin)
admin.site.register(Index, IndexAdmin)
admin.site.register(SharingMoney, SharingMoneyAdmin)
