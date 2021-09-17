from django.utils.deprecation import MiddlewareMixin

from .models import OnlineUserActivity


class OnlineNowMiddleware(MiddlewareMixin):
    @staticmethod
    def process_request(request):
        user = request.user
        if not user.is_authenticated:
            return

        OnlineUserActivity.update_user_activity(user)
