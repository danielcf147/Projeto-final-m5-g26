from rest_framework import serializers
from .models import Followers
import ipdb


class FollowerSerializer(serializers.ModelSerializer):
    def create(self, validated_data: dict) -> Followers:
        return Followers.objects.create(**validated_data)

    class Meta:
        model = Followers
        fields = ["id", "user_id", "user_follow_id"]
        extra_kwargs = {
            "user_id": {"read_only": True},
            "user_follow_id": {"read_only": True},
        }
