from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.models import User
from account.models import Profile
# # Register your models here.

admin.site.register(Profile)

admin.site.register(User, UserAdmin)

