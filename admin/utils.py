from api.utils import get_user


def is_blocked(request):
    user = get_user(request)
    return user.is_blocked
