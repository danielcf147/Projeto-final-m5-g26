from rest_framework import serializers
from .models import Publication, Comment, Like


class PublicationSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Publication
        fields = ["id", "post_photo", "text", "user_id", "comments", "acess_permission"]
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
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    class Meta:
        model = Comment
        fields = ["id", "comment", "user_id", "publication_id", "created_at"]
        extra_kwargs = {
            "id": {"read_only": True},
            "publication_id": {"read_only": True},
        }

    def create(self, validated_data: dict) -> Comment:
        return Comment.objects.create(**validated_data)
