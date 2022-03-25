from os import stat
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from datetime import datetime, timedelta
from django.utils import timezone
from api.models import User

from api.utils import get_user
from finance.models import UserFinance
from .models import Answers, Contest, Post
from .serializers import (
    ParticipateSerializer,
    CreateContestSerializer,
    VoteSerializer,
    CreatePostSerializer,
    AddQuestionSerializer,
)


class ParticipateAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ParticipateSerializer

    @swagger_auto_schema(tags=["Contest"])
    def post(self, request):
        user = get_user(request)
        serializer = self.serializer_class(data=request.data)
        contest = serializer.get.data("name")
        where_to_participate = Contest.objects.get(name=contest)
        balance = UserFinance.objects.get(user=user)
        if int(balance.balance) >= int(where_to_participate.price):
            new_balance = int(balance.balance) - int(where_to_participate.price)
            balance.balance = new_balance
            balance.save()
            where_to_participate.users.add(user)
            Response(
                {"Success": "Successfully participated"}, status=status.HTTP_200_OK
            )
        else:
            Response(
                {"Error": "You dont have enough money"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class CreateContestAPIView(generics.GenericAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = CreateContestSerializer

    @swagger_auto_schema(tags=["Contest"])
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        contest = Contest.objects.create()
        contest.name = serializer.data.get("name")
        contest.name = serializer.data.get("description")
        contest.name = serializer.data.get("price")
        contest.name = serializer.data.get("pic")
        days = serializer.data.get("time_to_expire")
        contest.expired_date = datetime.now() + timedelta(days=days)
        contest.save()
        return Response(
            {"Success": "Successfully created Contest"}, status=status.HTTP_201_CREATED
        )


class AddQuestionAPIView(generics.GenericAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = AddQuestionSerializer

    @swagger_auto_schema(tags=["Contest"])
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        answer = serializer.data.get("variation_of_answer")
        post = serializer.data.get("post")
        answer_to_add = Answers.objects.create()
        answer_to_add.variation_of_answer = answer
        what_post = Post.objects.get(question=post)
        what_post.answers.add(answer_to_add)
        return Response(
            {"Success": "Successfully added answer"}, status=status.HTTP_200_OK
        )


class ShowContestAPIView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(tags=["Contest"])
    def get(self, request, id):
        contest = Contest.objects.get(id=id)
        data = {"contest": []}
        data_first = {
            "id": contest.id,
            "name": contest.name,
            "description": contest.description,
            "price": contest.price,
            "published_date": contest.published_date,
            "expired": contest.expired_date,
        }
        data["contest"].append(data_first)
        return Response(data, status=status.HTTP_200_OK)


class ShowLastContestsAPIView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(tags=["Contest"])
    def get(self, request):
        contests = Contest.objects.filter().order_by("-published_date")
        data = {"contest": []}
        for contest in contests:
            members = contest.users.all().count()
            print(members)
            data_first = {
                "id": contest.id,
                "Name": contest.name,
                "Description": contest.description,
                "Price": contest.price,
                "pic": "avatar",
                "members": members,
                "date_of_creation": contest.published_date,
                "expired_date": contest.expired_date,
                "status": contest.status,
            }
            data["contest"].append(data_first)
        return Response(data, status=status.HTTP_200_OK)


class VoteAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = VoteSerializer

    @swagger_auto_schema(tags=["Votes"])
    def post(self, request):
        user = get_user(request)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        what_answer = serializer.data.get("vote_for")
        answer_for_post = Answers.objects.get(variation_of_answer=what_answer)
        answer = Post.objects.get(answer=answer_for_post)
        if user in answer.users:
            return Response(
                {"Error": "User voted alredy"}, status=status.HTTP_400_BAD_REQUEST
            )
        else:
            answer.users.add(user)
            Response({"Success": "Successfully voted"}, status=status.HTTP_200_OK)


class CreatePostAPIView(generics.GenericAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = CreatePostSerializer

    @swagger_auto_schema(tags=["Votes"])
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        question = serializer.data.get("question")
        days = serializer.data.get("days")
        post = Post.objects.create()
        post.question = question
        post.date_of_expired = datetime.now(timezone.utc) + timedelta(days=days)
        post.save()
        return Response(
            {"Success": "Successfully created post"}, status=status.HTTP_201_CREATED
        )


class ShowPostAPIView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(tags=["Votes"])
    def get(self, request):
        posts = Post.objects.filter().order_by("-date_of_creation")

        data = {"post": []}
        answers_finished = []
        for post in posts:
            answers = post.answers.all().prefetch_related("users")
            counter = 0
            all_answers = []
            counter_all = []
            for answer in answers:
                print(answer)
                print(answer.variation_of_answer)
                counters = answer.users.count()
                answer_single = {f"name": answer.variation_of_answer, "value": counters}
                counter += counters
                answers_finished.append(answer_single)
                var = answer.variation_of_answer
                all_answers.append(var)

            counters_count = {"all": counter}
            counter_all.append(counters_count)

            data_first = {
                "id": post.id,
                "question": post.question,
                "date_of_creation": post.date_of_creation,
                "date_of_expire": post.date_of_expired,
                "answers": answers_finished,
                "all_answers": all_answers,
                "all": counter_all,
            }
            data["post"].append(data_first)
        return Response(data, status=status.HTTP_200_OK)
