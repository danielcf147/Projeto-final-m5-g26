# Generated by Django 4.1.7 on 2023-03-09 15:59

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("publications", "0005_publication_comments"),
    ]

    operations = [
        migrations.AddField(
            model_name="publication",
            name="acess_permission",
            field=models.CharField(
                choices=[("public", "Default"), ("private", "Private")],
                default="public",
                max_length=7,
            ),
        ),
    ]