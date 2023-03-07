from django.db import models

# Create your models here.

class Followers(models.Model):
    user= models.ForeignKey("users.User", on_delete =models.CASCADE , related_name = "user")
    user_follow= models.ForeignKey("users.User", on_delete =models.CASCADE , related_name = "user_follows")
