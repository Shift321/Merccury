from django.contrib import admin
from django.contrib.auth.models import UserManager

from .models import User

admin.site.register(User)
