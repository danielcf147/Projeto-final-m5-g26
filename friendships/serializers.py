from rest_framework import serializers
from .models import Friendship


class FriendshipSerializer(serializers.ModelSerializer):
    def create(self, validated_data: dict) -> Friendship:
        return Friendship.objects.create(**validated_data)

    class Meta:
        model = Friendship
        fields = ["id", "user_id", "user_friendship_id", "accepted"]
        extra_kwargs = {
            "user_id": {"read_only": True},
            "user_friendship_id": {"read_only": True},
            "accepted": {"read_only": True},
        }
