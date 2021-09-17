from django.contrib import admin
from .models import HistoryOfTopUp, UserFinance, HistroyOfСonsumption

admin.site.register(UserFinance)
admin.site.register(HistoryOfTopUp)
admin.site.register(HistroyOfСonsumption)
