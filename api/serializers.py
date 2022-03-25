from api.utils import Util
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers, status
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
import base64


from .models import User


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=6,
        write_only=True,
    )
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "name",
            "second_name",
            "id_of_invited",
            "patronymic",
            "password",
            "phone_number",
            "token",
        ]

    def get_base64_image(self, obj):
        f = open(obj.image_file.path, "rb")

    def create(self, validate_data):
        return User.objects.create_user(**validate_data)


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=128, write_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=128, read_only=True)

    class Meta:
        model = User
        fields = ["username", "password", "token"]

    def send_email_with_code(user):
        code = Util.create_code(user, "email")
        data_for_email = {
            "email_body": f"yout verification code : {code}",
            "to_email": user.email,
            "email_subject": "Verify your email",
        }
        Util.send_email(data_for_email)

    def send_sms_with_code(user):
        code = Util.create_code(user, "SMS")
        Util.send_sms(code, user.phone_number)

    def validate(self, data):
        username = data.get("username", None)
        password = data.get("password", None)

        if username is None:
            raise serializers.ValidationError("An email adress is required to log in")
        if password is None:
            raise serializers.ValidationError("Password is required to log ing")

        user = authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError("A user with this login was not found")

        if not user.is_active:
            raise serializers.ValidationError("this user has beed deactivated")

        if user.verification_choice == "absent":
            return {"token": user.token}
        if user.verification_choice == "SMS":
            self.send_sms_with_code(user)
            return {"token": user.token}
        if user.verification_choice == "email":
            self.send_email_with_code(user)
            return {"token": user.token}
        if user.verification_choice == "SMS_email":
            self.send_sms_with_code(user)
            self.send_email_with_code(user)
            return {"token": user.token}
        else:
            return {"token": user.token}


class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ["old_password", "new_password"]

    def validate_new_password(self, value):
        validate_password(value)
        return value


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=255)

    class Meta:
        model = User
        fields = ["token"]


class SMSVerificationSerializer(serializers.ModelSerializer):
    code = serializers.CharField(max_length=6)

    class Meta:
        model = User
        fields = ["code"]


class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    class Meta:
        fields = ["email"]


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=6, max_length=255, write_only=True)
    token = serializers.CharField(min_length=1, write_only=True)
    uidb64 = serializers.CharField(min_length=1, write_only=True)

    class Meta:
        fields = ["password", "token", "uidb64"]

    def validate(self, attrs):
        try:
            password = attrs.get("password")
            token = attrs.get("token")
            uidb64 = attrs.get("uidb64")

            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed("The reset link is invalid", 401)
            user.set_password(password)
            user.save()
            return user
        except Exception as e:
            raise AuthenticationFailed("the reset link is invalid", 401)


class PasswordTokenCheckSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=255)

    class Meta:
        model = User
        fields = ["token"]


class LogoutSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=255)

    class Meta:
        model = User
        fields = ["token"]


class AddMoreUserInfoSerializer(serializers.Serializer):
    username = serializers.CharField(required=False)
    office = serializers.CharField(required=False)
    town = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    pasport_serial = serializers.CharField(required=False)
    pasport_number = serializers.CharField(required=False)
    pasport_date_of_gave = serializers.CharField(required=False)
    pasport_who_gave = serializers.CharField(required=False)
    citizenship = serializers.CharField(required=False)
    city_of_born = serializers.CharField(required=False)
    adress = serializers.CharField(required=False)
    adress_of_living = serializers.CharField(required=False)
    inn = serializers.CharField(required=False)
    snils = serializers.CharField(required=False)
    number_of_bank_cart = serializers.CharField(required=False)
    telegram = serializers.CharField(required=False)
    facebook = serializers.CharField(required=False)
    instagram = serializers.CharField(required=False)
    twitter = serializers.CharField(required=False)
    youtube = serializers.CharField(required=False)
    vk = serializers.CharField(required=False)

    class Meta:
        model = User


class ChangeVerificationChoiceSerializer(serializers.Serializer):
    what_choice = serializers.CharField(max_length=1, min_length=1)

    class Meta:
        model = User


class LoginVerificationSerializer(serializers.Serializer):
    email_code = serializers.CharField(max_length=6, min_length=6, required=False)
    sms_code = serializers.CharField(max_length=6, min_length=6, required=False)

    class Meta:
        model = User


class PutOnBlackListSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=255, min_length=1)

    class Meta:
        model = User


class PutFromBlackListSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=255, min_length=1)

    class Meta:
        model = User


class IsVerified(serializers.Serializer):
    id = serializers.CharField(max_length=255, min_length=1)


class UploadAvatar(serializers.Serializer):
    avatar = serializers.CharField(max_length=90000000, min_length=1)
