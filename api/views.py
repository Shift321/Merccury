from django.core.files.base import ContentFile
from rest_framework import permissions
from admin.utils import is_blocked
from api.utils import get_user
import datetime
from rest_framework import status, generics, serializers
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import base64
from django.core.files.base import ContentFile
from messagesender.models import Dialog

from .models import BlackList, User
from .serializers import (
    LoginSerializer,
    LoginVerificationSerializer,
    LogoutSerializer,
    PutFromBlackListSerializer,
    ResetPasswordEmailRequestSerializer,
    SMSVerificationSerializer,
    RegistrationSerializer,
    ChangePasswordSerializer,
    EmailVerificationSerializer,
    SetNewPasswordSerializer,
    PasswordTokenCheckSerializer,
    AddMoreUserInfoSerializer,
    ChangeVerificationChoiceSerializer,
    PutOnBlackListSerializer,
    UploadAvatar,
)
from .utils import Util

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from django.utils.encoding import (
    smart_str,
    smart_bytes,
    DjangoUnicodeDecodeError,
)
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class RegistrationAPIView(generics.GenericAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(tags=["Auth"])
    def post(self, request, format=None):

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            partner = serializer.validated_data.get("id_of_invited")
            queryset = User.objects.filter(id=partner)
            if queryset.exists():
                serializer.save()
            else:
                return Response(
                    {"data error": "wrong id of partner partner doesn't exists"},
                    status=status.HTTP_404_NOT_FOUND,
                )
        else:
            return Response(
                {"serializer error": "serializer is not valid"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user_data = serializer.data
        token = serializer.data.get("token")
        user = User.objects.get(email=user_data["email"])
        phone_number = user.phone_number
        current_site = get_current_site(request).domain
        relative_link = reverse("email-verify")
        absurl = "http://" + current_site + relative_link + "?token=" + str(token)
        email_body = (
            "Hi " + user.username + " Use link below to verify you email \n" + absurl
        )
        data_for_email = {
            "email_body": email_body,
            "to_email": user.email,
            "email_subject": "Verify your email",
        }
        Util.send_email(data_for_email)
        code = Util.create_code(user, "SMS")
        Util.send_sms(code, phone_number)

        return Response(
            {
                "token": serializer.data.get("token", None),
            },
            status=status.HTTP_201_CREATED,
        )


class VerifySMSCode(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = SMSVerificationSerializer

    @swagger_auto_schema(tags=["Auth"])
    def get(self, request):
        serializer = self.serializer_class(data=request.data)
        user = get_user(request)
        if serializer.is_valid():
            code = serializer.data.get("code")
            if not user.is_verified_by_phone:
                if code == user.code_for_phone:
                    user.is_verified_by_phone = True
                    if user.is_verified_by_email == True:
                        user.date_of_activate = datetime.datetime.now()
                    return Response(
                        {"succeess": "Account verified successfully"},
                        status=status.HTTP_200_OK,
                    )
                else:
                    return Response(
                        {"Error": "wrong code"}, status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                return Response(
                    {"error": "user alredy verified by phone"},
                    status=status.HTTP_208_ALREADY_REPORTED,
                )
        else:
            return Response(
                {"Failed": "Cannot serialize data"}, status=status.HTTP_400_BAD_REQUEST
            )


class VerifyEmail(generics.GenericAPIView):
    serializer_class = EmailVerificationSerializer
    permission_classes = [AllowAny]
    token_param_config = openapi.Parameter(
        "token",
        in_=openapi.IN_QUERY,
        description="Description",
        type=openapi.TYPE_STRING,
    )

    @swagger_auto_schema(manual_parameters=[token_param_config], tags=["Auth"])
    def get(self, request):
        user = get_user(request)

        if not user.is_verified_by_email:
            user.is_verified_by_email = True
            if user.is_verified_by_phone_number == True:
                user.date_of_activate = datetime.datetime.now()
            user.save()
            return Response(
                {"email": "Successfully activated"}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"email": "Account alredy activated"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class LoginAPIView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    @swagger_auto_schema(tags=["Auth"])
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class RequestPasswordResetEmail(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = ResetPasswordEmailRequestSerializer

    @swagger_auto_schema(tags=["Reset password"])
    def post(self, request):
        email = request.data["email"]
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(request=request).domain
            relative_link = reverse(
                "password-reset-confirm", kwargs={"uidb64": uidb64, "token": token}
            )
            absurl = "http://" + current_site + relative_link
            email_body = "Hi " + " Use this link  to reset your password \n" + absurl
            data_for_email = {
                "email_body": email_body,
                "to_email": user.email,
                "email_subject": "Reset your password",
            }
            Util.send_email(data_for_email)
            return Response(
                {"success": "We have sent you a link to reset your password"},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"error": "the user with this email wasn't found"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class PasswordTokenCheckAPI(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = PasswordTokenCheckSerializer

    @swagger_auto_schema(tags=["Reset password"])
    def get(self, request, uidb64, token):
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response(
                    {"error": "Token is not valid,please request a new one"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            return Response(
                {
                    "success": True,
                    "message": "Credentinals Valid",
                    "uidb64": uidb64,
                    "token": token,
                },
                status=status.HTTP_200_OK,
            )
        except DjangoUnicodeDecodeError as identifier:
            return Response(
                {"error": "Token is not valid,please request a new one"},
                status=status.HTTP_401_UNAUTHORIZED,
            )


class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(tags=["Reset password"])
    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            {"success": True, "message": "Password reset success"},
            status=status.HTTP_200_OK,
        )


class LogoutAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LogoutSerializer

    @swagger_auto_schema(tags=["Auth"])
    def get(self, request):
        if not is_blocked(request):
            request.user.token.delete()

            return Response({"Logged out": "succeess"}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"Error": "your account blocked try to connect with admin"},
                status=status.HTTP_404_NOT_FOUND,
            )


class ChangePasswordAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def get_object(self):
        return self.request.user

    @swagger_auto_schema(tags=["Auth"])
    def put(self, request, *args, **kwargs):
        if not is_blocked(request):
            self.object = self.get_object()
            serializer = ChangePasswordSerializer(data=request.data)

            if serializer.is_valid():
                old_password = serializer.data.get("old_password")
                if not self.object.check_password(old_password):
                    return Response(
                        {"old password": "Wrong password"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                self.object.set_password(serializer.data.get("new_password"))
                self.object.save()
                return Response(
                    {"Success": "Successfully changed"}, status=status.HTTP_200_OK
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {"Error": "your account blocked try to connect with admin"},
                status=status.HTTP_404_NOT_FOUND,
            )


class AddMoreUserInfoAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddMoreUserInfoSerializer

    @swagger_auto_schema(tags=["Auth"])
    def post(self, request):
        if not is_blocked(request):
            user = get_user(request)
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                username = serializer.data.get("username")
                office = serializer.data.get("office")
                town = serializer.data.get("town")
                description = serializer.data.get("description")
                pasport_serial = serializer.data.get("pasport_serial")
                pasport_number = serializer.data.get("pasport_number")
                pasport_date_of_gave = serializer.data.get("pasport_date_of_gave")
                pasport_who_gave = serializer.data.get("pasport_who_gave")
                citizenship = serializer.data.get("citizenship")
                city_of_born = serializer.data.get("city_of_born")
                adress = serializer.data.get("adress")
                adress_of_living = serializer.data.get("adress_of_living")
                inn = serializer.data.get("inn")
                snils = serializer.data.get("snils")
                number_of_bank_cart = serializer.data.get("number_of_bank_cart")
                telegram = serializer.data.get("telegram")
                facebook = serializer.data.get("facebook")
                instagram = serializer.data.get("instagram")
                twitter = serializer.data.get("twitter")
                youtube = serializer.data.get("youtube")
                vk = serializer.data.get("vk")

                try:
                    user.username = username
                    user.office = office
                    user.town = town
                    user.description = description
                    user.pasport_serial = pasport_serial
                    user.pasport_number = pasport_number
                    user.pasport_date_of_gave = pasport_date_of_gave
                    user.pasport_who_gave = pasport_who_gave
                    user.citizenship = citizenship
                    user.city_of_born = city_of_born
                    user.adress = adress
                    user.adress_of_living = adress_of_living
                    user.inn = inn
                    user.snils = snils
                    user.number_of_bank_cart = number_of_bank_cart
                    user.telegram = telegram
                    user.facebook = facebook
                    user.instagram = instagram
                    user.twitter = twitter
                    user.youtube = youtube
                    user.vk = vk
                    user.save()
                    return Response(
                        {"success": "data added successfully"},
                        status=status.HTTP_200_OK,
                    )
                except:
                    return Response({"error": "Username alredy exists"})
            else:
                return Response(
                    {"error": "serializer error"}, status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {"Error": "your account blocked try to connect with admin"},
                status=status.HTTP_404_NOT_FOUND,
            )


class ChangeVerificationChoiceAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangeVerificationChoiceSerializer

    @swagger_auto_schema(tags=["Auth"])
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_user(request)
        choice = serializer.data.get("what_choice")
        user.verification_choice = choice
        user.save()
        return Response({"Success": "Changed"}, status=status.HTTP_200_OK)


class LoginVerificationChoiceAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LoginVerificationSerializer

    @swagger_auto_schema(tags=["Auth"])
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_user(request)
        sms_code = serializer.data.get("phone_code")
        email_code = serializer.data.get("email_code")
        if user.verification_choice == "absent":
            return Response({"Success": "Logined"}, status=status.HTTP_200_OK)
        if user.verification_choice == "SMS":
            if user.code_for_phone == sms_code:
                return Response({"Success": "Logined"}, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"Error": "Wrong code"}, status=status.HTTP_400_BAD_REQUEST
                )
        elif user.verification_choice == "email":
            if user.code_for_email == email_code:
                return Response({"Success": "Logined"}, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"Error": "Wrong code"}, status=status.HTTP_400_BAD_REQUEST
                )
        elif user.verification_choice == "SMS_email":
            if user.code_for_email == email_code and user.code_for_phone == sms_code:
                return Response({"Success": "Logined"}, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"Error": "Wrong code"}, status=status.HTTP_400_BAD_REQUEST
                )


class PutOnBlackListAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PutOnBlackListSerializer

    @swagger_auto_schema(tags=["Black list"])
    def post(self, request):
        user = get_user(request)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            list = BlackList.objects.get(user=user)
        except:
            list = BlackList.objects.create(user=user)
        id = serializer.data.get("id")
        who_to_block = User.objects.get(id=id)
        list.blocked_users.add(who_to_block)
        return Response(
            {"Success": "Successfuly added to block list"}, status=status.HTTP_200_OK
        )


class PutAwayFromBlackListAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=["Black list"])
    def post(self, request):
        user = get_user(request)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        list = BlackList.objects.get(user=user)
        id = serializer.data.get("id")
        who_to_block = User.objects.get(id=id)
        list.blocked_users.remove(who_to_block)
        return Response(
            {"Success": "Successfuly removed from block list"},
            status=status.HTTP_200_OK,
        )


class ShowMyDataAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=["User"])
    def get(self, request):
        user = get_user(request)
        dialogs = Dialog.objects.filter(users=user)
        counter = 0
        for dialog in dialogs:
            messages = dialog.messages.exclude(sender=user).all()
            for message in messages:
                if message.is_read == False:
                    counter += 1
        sponsor = User.objects.get(id=user.id_of_invited) 
        data = {
            "id": user.id,
            "Surename": user.second_name,
            "Name": user.name,
            "PhoneNumber": str(user.phone_number),
            "Username": user.username,
            "email": user.email,
            "verify_by_phone": user.is_verified_by_phone,
            "verify_by_email": user.is_verified_by_email,
            "unread_messages": counter,
            "viewers": "1",
            "avatar": str(user.avatar),
            "rank": "rank",
            "date_of_birth": user.date_of_birth,
            "country": user.citizenship,
            "city": user.city_of_born,
            "telegram": user.telegram,
            "vk": user.vk,
            "facebook": user.facebook,
            "instagram": user.instagram,
            "twitter": user.twitter,
            "youtube": user.youtube,
            "info_of_sponsor": {
                "id_of_sponsor": sponsor.id,
                "Name_of_sponsor": sponsor.name,
                "surename_of_sponsor": sponsor.second_name,
            },
        }

        return Response(data, status=status.HTTP_200_OK)


class ShowDataOfUserAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=["User"])
    def get(self, request, id):
        main_user = get_user(request)
        user = User.objects.get(id=id)
        is_user_me = False
        if main_user == user:
            is_user_me = True
        sponsor = User.objects.get(id=user.id_of_invited)
        data = {
            "id": user.id,
            "Surename": user.second_name,
            "Name": user.name,
            "PhoneNumber": str(user.phone_number),
            "Username": user.username,
            "email": user.email,
            "verify_by_phone": user.is_verified_by_phone,
            "verify_by_email": user.is_verified_by_email,
            "viewers": "1",
            "avatar": str(user.avatar),
            "date_of_birth": user.date_of_birth,
            "country": user.citizenship,
            "city": user.city_of_born,
            "telegram": user.telegram,
            "vk": user.vk,
            "facebook": user.facebook,
            "instagram": user.instagram,
            "twitter": user.twitter,
            "youtube": user.youtube,
            "info_of_sponsor": {
                "id_of_sponsor": sponsor.id,
                "Name_of_sponsor": sponsor.name,
                "surename_of_sponsor": sponsor.second_name,
            },
            "rank": "rank",
            "is_user_me": is_user_me,
        }

        return Response(data, status=status.HTTP_200_OK)


class IsVerify(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=["User"])
    def get(self, request):
        user = get_user(request)
        data = {"info": []}
        data_last = {
            "Phone": user.is_verified_by_phone,
            "Email": user.is_verified_by_email,
        }
        data["info"].append(data_last)
        return Response(data, status=status.HTTP_200_OK)


class UploadAvatar(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UploadAvatar

    @swagger_auto_schema(tags=["User"])
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_user(request)
        pic = serializer.data.get("avatar")
        format, imgstr = pic.split(";base64,")
        ext = format.split("/")[-1]
        avatar = ContentFile(base64.b64decode(imgstr), name="temp." + ext)
        user.avatar = avatar
        user.save()
        return Response({"Success": "Avatar uploaded"}, status=status.HTTP_200_OK)


class GenerateRefLink(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=["User"])
    def get(self, request):
        user = get_user(request)
        current_site = get_current_site(request).domain
        absurl = "http://" + current_site + f"/referal/{user.id}"
        return Response({"link": f"{absurl}"}, status=status.HTTP_200_OK)
