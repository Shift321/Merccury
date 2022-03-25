import json
from os import stat
from re import T
import re
from django.db.models import query
from rest_framework import generics
from rest_framework import permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
import requests
from mercury.settings import SECRET_KEY
from .models import (
    Index,
    SharingMoney,
    UserFinance,
    HistoryOfTopUp,
    HistroyOfСonsumption,
)
from .serializers import (
    GetFinanceInfoSerializer,
    CreateIndexSerializer,
    ShowHistoryOfConSerializer,
    ShowHistoryOfTopUpSerializer,
    TopUpSerializer,
    CreateSharingMoneySerializer,
    ShowSharingMoneyApplicationSerializer,
)
from api.utils import get_user

from drf_yasg.utils import swagger_auto_schema


class GetFinanceInfoAPIView(generics.GenericAPIView):
    permission_class = [IsAuthenticated]
    serializer_class = GetFinanceInfoSerializer

    @swagger_auto_schema(tags=["Finance"])
    def get(self, request):
        user = get_user(request)
        price_of_all_indexes = 0
        finance = UserFinance.objects.get(user=user)
        price_of_index = Index.objects.filter(user=user)
        for i in range(price_of_index.count()):
            price_of_all_indexes += int(price_of_index[i].price)
        data = {
            "Balance": finance.balance,
            "Price of all indexes": price_of_all_indexes,
        }
        return Response(data, status=status.HTTP_200_OK)


class CreateIndexAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateIndexSerializer

    @swagger_auto_schema(tags=["Finance"])
    def post(self, request):
        user = get_user(request)
        serializer = self.serializer_class(data=request.data)
        finance = UserFinance.objects.get(user=user)

        serializer.is_valid(raise_exception=True)
        state = serializer.data.get("state")
        name = serializer.data.get("name")
        price = serializer.data.get("price")
        if int(finance.balance) >= int(price):
            index = Index.objects.create(user=user)
            index.state = state
            index.name = name
            index.price = price
            new_balance = int(finance.balance) - int(price)
            finance.balance = new_balance
            new_summ = int(finance.price_of_all_indexes) + int(price)
            finance.price_of_all_indexes = new_summ
            histroy = HistroyOfСonsumption.objects.create(user=user)
            histroy.summ = price
            histroy.save()
            finance.save()
            index.save()
        else:
            return Response(
                {"error": "Not enough money on balance"},
                status=status.HTTP_406_NOT_ACCEPTABLE,
            )
        return Response(
            {"Success": "Successfully added index"}, status=status.HTTP_201_CREATED
        )


class TopUpBalanceAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TopUpSerializer

    @swagger_auto_schema(tags=["Finance"])
    def post(self, request):
        user = get_user(request)
        serilizer = self.serializer_class(data=request.data)
        serilizer.is_valid(raise_exception=True)
        summ_of_top_up = serilizer.data.get("summ_of_top_up")
        queryset = UserFinance.objects.filter(user=user)
        if queryset.exists():
            balance = queryset[0]
        else:
            balance = UserFinance.objects.create(user=user)
        new_balance = int(balance.balance) + int(summ_of_top_up)
        balance.balance = new_balance
        balance.save()
        history = HistoryOfTopUp.objects.create(user=user)
        history.summ = summ_of_top_up
        history.save()
        return Response(
            {"Success": "Balance top up successfull"}, status=status.HTTP_200_OK
        )


class ShowHistroyOfTopUpAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ShowHistoryOfTopUpSerializer

    @swagger_auto_schema(tags=["Finance"])
    def get(self, request):
        user = get_user(request)
        history = HistoryOfTopUp.objects.filter(user=user)
        if history.exists():
            summ_of_all_top_up = 0
            data = {"histroy": []}
            for i in range(history.count()):
                data_end = {
                    "summ_of_top_up": history[i].summ,
                    "date_of_top_up": history[i].time_of_payment,
                }
                summ_of_all_top_up += int(history[i].summ)
                data["histroy"].append(data_end)
            data.update({"summ_of_all_top_up": summ_of_all_top_up})
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({"Error": "No history"}, status=status.HTTP_204_NO_CONTENT)


class ShowHistroyOfСonsumptionAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ShowHistoryOfConSerializer

    @swagger_auto_schema(tags=["Finance"])
    def get(self, request):
        user = get_user(request)
        history = HistroyOfСonsumption.objects.filter(user=user)
        if history.exists():
            summ_of_all_consumption = 0
            data = {"history": []}
            for i in range(history.count()):
                data_end = {
                    "summ_of_spend": history[i].summ,
                    "date_of_spend": history[i].time_of_spend,
                }
                summ_of_all_consumption += int(history[i].summ)
                data["history"].append(data_end)
            data.update({"summ_of_all_consumption": summ_of_all_consumption})
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({"Error": "No histroy"}, status=status.HTTP_404_NOT_FOUND)


class CreateSharingMoneyAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateSharingMoneySerializer

    @swagger_auto_schema(tags=["Finance"])
    def post(self, request):
        serilazer = self.serializer_class(data=request.data)
        serilazer.is_valid(raise_exception=True)
        user = get_user(request)
        application = SharingMoney.objects.create()
        application.user = user
        application.summ = serilazer.data.get("summ")
        application.way_to_pay = serilazer.data.get("way_to_pay")
        application.save()
        return Response(
            {"success": "Your application created successfully"},
            status=status.HTTP_200_OK,
        )


class ShowSharingMoneyApplicationAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ShowSharingMoneyApplicationSerializer

    @swagger_auto_schema(tags=["Finance"])
    def get(self, request):
        user = get_user(request)
        aplications = SharingMoney.objects.filter(user=user)
        data = {"info": []}
        for aplication in aplications:
            data_last = {
                "date_of_operation": aplication.date_of_operation,
                "status": aplication.status,
                "summ": aplication.summ,
                "way_to_pay": aplication.way_to_pay,
            }
            data["info"].append(data_last)
        return Response(data, status=status.HTTP_200_OK)


class ShowPriceOfCryptoAPIView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def get(self, request):
        prices = {"prices": []}
        url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?symbol=btc,eth,bnb,usdt,sol,ada,xrp,usdt,bnb,usdc,ltc&convert=USD"
        headers = {
            "Accepts": "application/json",
            "X-CMC_PRO_API_KEY": "7f386aef-d035-4300-866f-8563fc5e03c7",
        }
        r = requests.get(url, headers=headers)
        text = json.loads(r.text)
        currency = ["BTC", "ETH", "SOL", "ADA", "XRP", "USDT", "BNB", "USDC", "LTC"]
        data = {"data": []}
        for i in currency:
            id = text["data"][f"{i}"]["id"]
            market_cap = text["data"][f"{i}"]["quote"]["USD"]["market_cap"]
            price = text["data"][f"{i}"]["quote"]["USD"]["price"]
            data_of_current_currency = {
                "name": text["data"][f"{i}"]["name"],
                "symbol": text["data"][f"{i}"]["symbol"],
                "Rank": text["data"][f"{i}"]["cmc_rank"],
                "PriceUSD": price,
                "volume24hUSD": text["data"][f"{i}"]["quote"]["USD"]["volume_24h"],
                "marketCapUSD": market_cap,
                "percentChange24h": text["data"][f"{i}"]["quote"]["USD"][
                    "percent_change_24h"
                ],
                "Supl": float(market_cap) / float(price),
                "icon": f"https://s2.coinmarketcap.com/static/img/coins/64x64/{id}.png",
            }
            data["data"].append(data_of_current_currency)
        return Response(data, status=status.HTTP_200_OK)
