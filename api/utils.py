from django.core.mail import EmailMessage, message
from rest_framework import response
import random
from mercury.settings import ACCOUNT_KEY, ACCOUNT_SECRET
import vonage
from api.models import User
from rest_framework import exceptions
from mercury.settings import SECRET_KEY
import jwt


client = vonage.Client(key="26e4494f", secret=f"gd25YsMVBwimNR2J")
sms = vonage.Sms(client)


class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data["email_subject"],
            body=data["email_body"],
            to=[data["to_email"]],
        )
        email.send()

    def create_code(user, what_for):
        code = ""
        for i in range(6):
            number = random.randint(0, 9)
            code = code + str(number)
        if what_for == "SMS":
            user.code_for_phone = code
            user.save()
            return code
        elif what_for == "email":
            user.code_for_email = code
            user.save()
            return code

    def send_sms(user_code, phone_number):
        responseData = sms.send_message(
            {
                "from": "Vonage APIs",
                "to": f"{phone_number}",
                "text": f"Your code is {user_code}",
            }
        )
        if responseData["messages"][0]["status"] == "0":
            print("Message sent successfully.")
        else:
            print(
                f"Message failed with error: {responseData['messages'][0]['error-text']}"
            )


def get_user(request):
    token = request.headers["Authorization"].split()
    try:
        payload = jwt.decode(token[1], SECRET_KEY, algorithms=["HS256"])
    except:
        msg = "Invalid authenticated. Could not decode token."
        raise exceptions.AuthenticationFailed(msg)
    user = User.objects.get(id=payload["id"])
    return user
