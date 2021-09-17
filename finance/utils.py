from api.models import User
from rest_framework import exceptions
from mercury.settings import SECRET_KEY
import jwt


def get_user(request):
    token = request.headers["Authorization"].split()
    try:
        payload = jwt.decode(token[1], SECRET_KEY, algorithms=["HS256"])
    except:
        msg = "Invalid authenticated. Could not decode token."
        raise exceptions.AuthenticationFailed(msg)
    user = User.objects.get(id=payload["id"])
    return user
