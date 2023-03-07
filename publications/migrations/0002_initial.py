# Generated by Django 4.1.7 on 2023-03-07 13:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("publications", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="publication",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="publications",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="like",
            name="publication",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="likes_users",
                to="publications.publication",
            ),
        ),
        migrations.AddField(
            model_name="like",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="publication_likes_user",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="comment",
            name="publication",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="publications_comment_user",
                to="publications.publication",
            ),
        ),
        migrations.AddField(
            model_name="comment",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user_comments_publication",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
