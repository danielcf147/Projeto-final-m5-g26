from django.db import models


class Comment(models.Model):
    comment = models.TextField()
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="user_comments_publication"
    )
    publication = models.ForeignKey(
        "publications.Publication",
        on_delete=models.CASCADE,
        related_name="publications_comment_user",
    )


class Publication(models.Model):
    class AcessChoices(models.TextChoices):
        DEFAULT = "public"
        PRIVATE = "private"

    post_photo = models.CharField(null=True, max_length=500)
    text = models.TextField()
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="publications"
    )
    comments = models.ManyToManyField(
        "users.User", through="publications.Comment", related_name="comment"
    )
    likes = models.ManyToManyField(
        "users.User", through="publications.Like", related_name="like"
    )
    acess_permission = models.CharField(
        max_length=7,
        choices=AcessChoices.choices,
        default=AcessChoices.DEFAULT,
    )


class Like(models.Model):
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="publication_likes_user"
    )
    publication = models.ForeignKey(
        "publications.Publication", on_delete=models.CASCADE, related_name="likes_users"
    )
