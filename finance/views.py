from re import T
from django.db.models import query
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from mercury.settings import SECRET_KEY
from .models import Index, UserFinance, HistoryOfTopUp, HistroyOfСonsumption
from .serializers import (
    GetFinanceInfoSerializer,
    CreateIndexSerializer,
    TopUpSerializer,
)
from .utils import get_user

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

        if serializer.is_valid(raise_exception=True):
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
        else:
            return Response(
                {"error": "Serrializer is not valid"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class TopUpBalanceAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TopUpSerializer

    @swagger_auto_schema(tags=["Finance"])
    def post(self, request):
        user = get_user(request)
        serilizer = self.serializer_class(data=request.data)
        if serilizer.is_valid(raise_exception=True):
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
        else:
            return Response({"Error": "Serializer error"})


class ShowHistroyOfTopUpAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=["Finance"])
    def get(self, request):
        user = get_user(request)
        history = HistoryOfTopUp.objects.filter(user=user)
        summ_of_all_top_up = 0
        data = {}
        for i in range(history.count()):
            data[i] = {
                "summ_of_top_up": history[i].summ,
                "date_of_top_up": history[i].time_of_payment,
            }
            summ_of_all_top_up += int(history[i].summ)
        data.update({"summ_of_all_top_up": summ_of_all_top_up})
        return Response(data, status=status.HTTP_200_OK)


class ShowHistroyOfСonsumptionAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=["Finance"])
    def get(self, request):
        user = get_user(request)
        history = HistroyOfСonsumption.objects.filter(user=user)
        summ_of_all_consumption = 0
        data = {}
        for i in range(history.count()):
            data[i] = {
                "summ_of_spend": history[i].summ,
                "date_of_spend": history[i].time_of_spend,
            }
            summ_of_all_consumption += int(history[i].summ)
        data.update({"summ_of_all_consumption": summ_of_all_consumption})
        return Response(data, status=status.HTTP_200_OK)
