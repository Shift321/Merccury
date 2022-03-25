import datetime
from django.core.cache import cache
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
import datetime
from api.utils import get_user


class OnlineNowMiddleware(MiddlewareMixin):
    def process_request(self, request):
        current_user = get_user(request)
        if current_user.is_authenticated:
            now = datetime.datetime.now()
            cache.set(
                "seen_%s" % (current_user.username), now, settings.USER_LASTSEEN_TIMEOUT
            )
