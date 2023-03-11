from django.db import models


class Friendship(models.Model):
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="friendship_user"
    )
    user_friendship = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="user_friendships"
    )
    accepted = models.BooleanField(default=False)
