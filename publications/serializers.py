from rest_framework import serializers
from .models import Publication, Comment, Like


class PublicationSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Publication
        fields = ["id", "post_photo", "text", "user_id", "comments"]
        extra_kwargs = {
            "id": {"read_only": True},
            "comments": {"read_only": True},
        }

    def create(self, validated_data: dict) -> Publication:
        return Publication.objects.create(**validated_data)

    def get_comments(self, obj):
        comments = obj.publications_comment_user.all()
        return [
            {"id": comment.id, "user_id": comment.user_id, "comment": comment.comment}
            for comment in comments
        ]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "comment", "user_id", "publication_id"]
        extra_kwargs = {
            "id": {"read_only": True},
            "publication_id": {"read_only": True},
        }

    def create(self, validated_data: dict) -> Comment:
        return Comment.objects.create(**validated_data)
