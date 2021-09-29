from django.db.models import fields
from finance.models import HistoryOfTopUp, Index, SharingMoney, UserFinance
from rest_framework import serializers


class GetFinanceInfoSerializer(serializers.Serializer):
    balance = serializers.CharField(max_length=255)
    price_of_all_indexes = serializers.CharField(max_length=255)

    class Meta:
        model = UserFinance
        fields = ["balance", "price_of_all_indexes"]


class CreateIndexSerializer(serializers.Serializer):
    state = serializers.CharField(max_length=255)
    name = serializers.CharField(max_length=255)
    price = serializers.CharField(max_length=255)

    class Meta:
        model = Index
        fields = ["state", "name", "price"]


class TopUpSerializer(serializers.Serializer):
    summ_of_top_up = serializers.CharField(max_length=255)

    class Meta:
        model = UserFinance
        fields = ["summ_of_top_up"]


class CreateSharingMoneySerializer(serializers.Serializer):
    summ = serializers.CharField(max_length=255)
    way_to_pay = serializers.CharField(max_length=255)

    class Meta:
        model = SharingMoney
        fields = ["summ", "way_to_pay"]


class ShowSharingMoneyApplicationSerializer(serializers.Serializer):
    class Meta:
        model = SharingMoney


class ShowHistoryOfTopUpSerializer(serializers.Serializer):
    class Meta:
        model = HistoryOfTopUp


class ShowHistoryOfConSerializer(serializers.Serializer):
    class Meta:
        model = HistoryOfTopUp
