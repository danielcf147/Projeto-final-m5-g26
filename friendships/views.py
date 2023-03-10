from django.shortcuts import get_object_or_404
from .models import Friendship
from .serializers import FriendshipSerializer
from users.models import User
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    UpdateAPIView,
    RetrieveAPIView,
    DestroyAPIView,
)
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import Response, status
from rest_framework import serializers
from django.core.exceptions import PermissionDenied


class FriendshipView(
    CreateAPIView, ListAPIView, UpdateAPIView, RetrieveAPIView, DestroyAPIView
):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    queryset = Friendship.objects.all()
    serializer_class = FriendshipSerializer

    lookup_field = "pk"

    def get_queryset(self):
        user = self.kwargs["pk"]
        return Friendship.objects.filter(user=user) | Friendship.objects.filter(
            user_friendship=user
        )

    def perform_create(self, serializer):
        user_friendship = get_object_or_404(User, pk=self.kwargs.get("pk", None))

        if user_friendship == self.request.user:
            raise serializers.ValidationError(
                {"detail": "You cannot send a friend request to yourself"}
            )

        friendship_exists = Friendship.objects.filter(
            user=self.request.user, user_friendship=user_friendship, accepted=False
        ).exists()
        if friendship_exists:
            raise serializers.ValidationError(
                {"detail": "There is already a pending friend request between you"}
            )

        serializer.save(user_friendship=user_friendship, user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        friendship = get_object_or_404(Friendship, pk=self.kwargs.get("pk", None))
        user = request.user
        if friendship.user != user and friendship.user_friendship != user:
            raise PermissionDenied(
                {"detail": "You do not have permission to delete this friendship."}
            )
        friendship.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = get_object_or_404(Friendship, pk=self.kwargs.get("pk", None))

        if instance.user_friendship_id != request.user.id:
            raise PermissionDenied(
                {"detail": "You do not have permission to update this friendship."}
            )

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            instance._prefetched_objects_cache = {}

        instance.accepted = True
        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    lookup_url_kwarg = "pk"
