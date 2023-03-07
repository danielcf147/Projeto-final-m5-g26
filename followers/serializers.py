from rest_framework import serializers
from .models import Followers


class FollowersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Followers
        fields = ["id", "user_id", "user_follow_id"]
        extra_kwargs = {
            "user_id": {"read_only": True},
            "user_follow_id": {"read_only": True},
        }
