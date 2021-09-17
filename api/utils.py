from django.core.mail import EmailMessage, message
from rest_framework import response
import random
from mercury.settings import ACCOUNT_KEY, ACCOUNT_SECRET
import vonage

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

    def create_code(user):
        code = ""
        for i in range(6):
            number = random.randint(0, 9)
            code = code + str(number)
        user.code_for_phone = code
        user.save()
        return code

    def send_sms(user_code, phone_number):
        print(phone_number)
        print(user_code)
        responseData = sms.send_message(
            {
                "from": "Vonage APIs",
                "to": f"{phone_number}",
                "text": f"Your code is {user_code}",
            }
        )
        print(responseData["messages"])
        if responseData["messages"][0]["status"] == "0":
            print("Message sent successfully.")
        else:
            print(
                f"Message failed with error: {responseData['messages'][0]['error-text']}"
            )
