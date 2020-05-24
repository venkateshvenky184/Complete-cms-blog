from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.conf import settings
User = settings.AUTH_USER_MODEL
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User,on_delete= models.CASCADE)
    bio = models.CharField(max_length=500,blank = True)
    image = models.ImageField(upload_to="profile/",blank = True)

    def __str__(self):
        return self.user.username


class User(AbstractUser):
    email = models.EmailField(unique=True)
    bio = models.TextField(max_length=500, blank=True)
    image = models.ImageField(upload_to='profile/', blank=True)
    is_author = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['email']