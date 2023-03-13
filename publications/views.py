from datetime import timezone
from rest_framework.views import APIView, status, Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from followers.models import Followers
from .models import Publication, Comment
from .serializers import LikeSerializer, PublicationSerializer, CommentSerializer
from .permissions import IsAccountOwner, isAuthenticated
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    CreateAPIView,
    UpdateAPIView,
    DestroyAPIView,
)
from rest_framework.mixins import CreateModelMixin
from django.views.generic import View
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from publications.models import Comment, Like, Publication
from friendships.models import Friendship
from users.models import User
import ipdb
from django.db.models.query import QuerySet
from rest_framework.exceptions import PermissionDenied
from django.db.models import Q
from django.http import Http404
from django.core.exceptions import PermissionDenied
from rest_framework.exceptions import ValidationError

# import followers.models from Followers


class PublicationView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [isAuthenticated]

    queryset = Publication.objects.all()
    serializer_class = PublicationSerializer

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)

    def get_queryset(self):
        if self.request.user.is_authenticated:
            user = self.request.user
            friendships = Friendship.objects.filter(
                user_id=user.id,
                accepted=True,
            )
            friends = []
            for friendship in friendships:
                if friendship.user_friendship == user:
                    friends.append(friendship.user)
                else:
                    friends.append(friendship.user_friendship)
            publications = Publication.objects.filter(
                user__in=friends,
                acess_permission=Publication.AcessChoices.PRIVATE,
            )
            publications_public = Publication.objects.filter(
                acess_permission=Publication.AcessChoices.DEFAULT
            )
            publications_list = list(publications) + list(publications_public)

            publications_queryset = QuerySet(model=Publication)
            publications_queryset._result_cache = publications_list

            return publications_queryset
        else:
            return Publication.objects.filter(
                acess_permission=Publication.AcessChoices.DEFAULT
            )


class TimeLinePublicationView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAccountOwner]

    queryset = Publication.objects.all()
    serializer_class = PublicationSerializer

    def get_queryset(self):
        user = self.request.user
        friendships = Friendship.objects.filter(
            Q(user_id=user) | Q(user_friendship_id=user),
            accepted=True,
        )
        followerships = Followers.objects.filter(user_id=user)
        friends = []
        for friendship in friendships:
            if friendship.user_friendship == user:
                friends.append(friendship.user)
            else:
                friends.append(friendship.user_friendship)
        followers = [followership.user_follow for followership in followerships]
        publications = Publication.objects.filter(user__in=friends)
        publications_public = Publication.objects.filter(
            user__in=followers,
            acess_permission=Publication.AcessChoices.DEFAULT,
        )
        publications_list = list(publications) + list(publications_public)

        publications_queryset = QuerySet(model=Publication)
        publications_queryset._result_cache = publications_list

        return publications_queryset


class PublicationDetailView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAccountOwner]

    queryset = Publication.objects.all()
    serializer_class = PublicationSerializer


class CommentView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAccountOwner]

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id, publication_id=self.kwargs["pk"])


class CommentDetailView(CreateAPIView, DestroyAPIView, UpdateAPIView, ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAccountOwner]
    serializer_class = CommentSerializer

    def get_queryset(self):
        publication_id = self.kwargs.get("pk")
        publication = get_object_or_404(Publication, id=publication_id)
        user = self.request.user
        owner = publication.user

        if user == owner:
            queryset = Comment.objects.filter(publication_id=publication_id)
            return queryset

        if publication.acess_permission == Publication.AcessChoices.PRIVATE:
            if (
                Friendship.objects.filter(
                    user=user, user_friendship_id=owner, accepted=True
                )
                or Friendship.objects.filter(
                    user=owner, user_friendship_id=user, accepted=True
                )
                or Followers.objects.filter(user=user, user_follow_id=owner)
            ):
                queryset = Comment.objects.filter(publication_id=publication_id)
                return queryset
            else:
                raise PermissionDenied(
                    "This publication is private and you are not allowed to view it."
                )
        else:
            queryset = Comment.objects.filter(publication_id=publication_id)
            return queryset

    def perform_create(self, serializer):
        publication_id = self.kwargs.get("pk")
        publication = Publication.objects.get(id=publication_id)

        if publication.acess_permission == Publication.AcessChoices.PRIVATE:
            user = self.request.user
            publication_owner = publication.user
            is_friend = Friendship.objects.filter(
                user=user, user_friendship=publication_owner, accepted=True
            ).exists()
            is_follower = Followers.objects.filter(
                user_follow=publication_owner, user=user
            ).exists()

            if not is_friend and not is_follower:
                raise PermissionDenied(
                    "You are not allowed to comment on this publication"
                )

        serializer.save(user=self.request.user, publication=publication)


class CommentLikeView(View):
    authentication_classes = [JWTAuthentication]
    serializer_class = LikeSerializer

    def post(self, request, *args, **kwargs):
        comment_id = kwargs.get("pk")
        comment = get_object_or_404(Comment, pk=comment_id)
        user = request.user

        like_queryset = Like.objects.filter(comment=comment, user=user)
        if like_queryset.exists():
            like_queryset.delete()
            return JsonResponse({"success": True})
        else:
            Like.objects.create(comment=comment, user=user)
            return JsonResponse({"success": True})


class PublicationLikeView(ListAPIView, CreateAPIView, DestroyAPIView, View):
    authentication_classes = [JWTAuthentication]
    permission_classes = [isAuthenticated]
    serializer_class = LikeSerializer

    def perform_create(self, serializer):
        publication_id = self.kwargs.get("pk")
        user = self.request.user
        publication = get_object_or_404(Publication, id=publication_id)
        owner = publication.user
        if user == owner:
            return serializer.save(user=user, publication=publication)

        if publication.acess_permission == Publication.AcessChoices.DEFAULT:
            if Like.objects.filter(user=user, publication=publication).exists():
                raise ValidationError(
                    {"detail": "You have already liked this publication."}
                )
            else:
                return serializer.save(user=user, publication=publication)
        else:
            if (
                Friendship.objects.filter(
                    user=user, user_friendship_id=owner, accepted=True
                )
                or Friendship.objects.filter(
                    user=owner, user_friendship_id=user, accepted=True
                )
                or Followers.objects.filter(user=user, user_follow_id=owner)
            ):
                if Like.objects.filter(user=user, publication=publication).exists():
                    raise ValidationError(
                        {"detail": "You have already liked this publication."}
                    )
                else:
                    return serializer.save(user=user, publication=publication)

            else:
                raise PermissionDenied(
                    "This publication is private and you are not allowed to view it."
                )

    def destroy(self, request, *args, **kwargs):
        like_id = kwargs.get("pk")
        like = get_object_or_404(Like, id=like_id)
        if like.user != request.user:
            raise PermissionDenied("You do not have permission to perform this action.")

        like.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_queryset(self):
        publication_id = self.kwargs.get("pk")
        publication = get_object_or_404(Publication, id=publication_id)
        user = self.request.user
        owner = publication.user

        if user == owner:
            queryset = Like.objects.filter(publication_id=publication_id)
            return queryset

        if publication.acess_permission == Publication.AcessChoices.PRIVATE:
            if (
                Friendship.objects.filter(
                    user=user, user_friendship_id=owner, accepted=True
                )
                or Friendship.objects.filter(
                    user=owner, user_friendship_id=user, accepted=True
                )
                or Followers.objects.filter(user=user, user_follow_id=owner)
            ):
                queryset = Like.objects.filter(publication_id=publication_id)
                return queryset
            else:
                raise PermissionDenied(
                    "This publication is private and you are not allowed to view it."
                )
        else:
            queryset = Like.objects.filter(publication_id=publication_id)
            return queryset
