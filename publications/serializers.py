from rest_framework import serializers
from .models import Publication, Comment, Like


class PublicationSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()

    class Meta:
        model = Publication
        fields = [
            "id",
            "post_photo",
            "text",
            "user_id",
            "comments",
            "likes",
            "acess_permission",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "comments": {"read_only": True},
            "likes": {"read_only": True},
        }

    def create(self, validated_data: dict) -> Publication:
        return Publication.objects.create(**validated_data)

    def get_comments(self, obj):
        comments = obj.publications_comment_user.all()
        return [
            {"id": comment.id, "user_id": comment.user_id, "comment": comment.comment}
            for comment in comments
        ]

    def get_likes(self, obj):
        likes = obj.likes_users.all()
        return [{"id": like.id, "user_id": like.user_id} for like in likes]


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


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ["id", "user", "publication"]
        extra_kwargs = {
            "id": {"read_only": True},
        }

    def create(self, validated_data: dict) -> Like:
        return Like.objects.create(**validated_data)
