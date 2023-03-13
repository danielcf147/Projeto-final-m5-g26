from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    birthdate = models.DateField(null=True)
    profile_picture = models.CharField(null=True, max_length=500)