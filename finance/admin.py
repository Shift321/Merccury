from django.contrib.auth.models import User
from api.admin import UserAdmin
from django.contrib import admin
from django.db import models
from .models import HistoryOfTopUp, Index, UserFinance, HistroyOfСonsumption


class HistoryAdmin(UserAdmin):
    list_filter = UserAdmin.list_filter + ("user",)


admin.site.register(UserFinance)
admin.site.register(HistoryOfTopUp, HistoryAdmin)
admin.site.register(HistroyOfСonsumption, HistoryAdmin)
admin.site.register(Index)
