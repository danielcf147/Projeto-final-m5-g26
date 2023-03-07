from rest_framework import serializers
from .models import Publication, Comment, Like


class Publication(serializers.Serializer):
    def create(self, validated_data: dict) -> Publication:
        return Publication.objects.create(**validated_data)

    class Meta:
        model = Publication
        fields = ["id", "post_photo", "text", "user_id", "comments_id"]
        extra_kwargs = {
            "id": {"read_only": True},
        }
