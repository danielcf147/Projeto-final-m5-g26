from datetime import timezone
from rest_framework.views import APIView, status, Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from followers.models import Followers
from .models import Publication, Comment
from .serializers import PublicationSerializer, CommentSerializer
from .permissions import IsAccountOwner, isAuthenticated
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView,CreateAPIView
from django.views.generic import View
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from publications.models import Comment, Like
from friendships.models import Friendship
from users.models import User
from django.db.models.query import QuerySet
from rest_framework.exceptions import PermissionDenied


class PublicationView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [isAuthenticated, IsAccountOwner]

    queryset = Publication.objects.all()
    serializer_class = PublicationSerializer

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Publication.objects.all()
        else:
            return Publication.objects.filter(
                acess_permission=Publication.AcessChoices.DEFAULT
            )


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


class CommentDetailView(CreateAPIView, RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAccountOwner]
    serializer_class = CommentSerializer

    def get_queryset(self):
        user = self.request.user
        publication_owner = Publication.objects.filter(pk=self.kwargs["pk"]).values(
            "user"
        )
        followers = Followers.objects.filter(
            user_id=user.id, user_follow_id=publication_owner[0]["user"]
        )

        queryset = Comment.objects.none()

        private_pub_query = Comment.objects.filter(
            publicationacess_permission=Publication.AcessChoices.PRIVATE,
            publicationuser=user,
            publicationacess_permissionin=[Publication.AcessChoices.PRIVATE],
        ).distinct()

        private_friends_pub_query = Comment.objects.filter(
            publicationacess_permission=Publication.AcessChoices.PRIVATE,
            publicationuserin=followers,
            publicationuserfriendship__is_following=True,
            publicationacess_permissionin=[Publication.AcessChoices.PRIVATE],
        ).distinct()

        queryset = queryset.union(
            private_pub_query, private_friends_pub_query
        ).distinct()
        return queryset

    def perform_create(self, serializer):
        publication_id = self.kwargs.get("pk")
        publication = Publication.objects.get(id=publication_id)

        if publication.user != self.request.user:
            raise PermissionDenied("You are not allowed to comment on this publication")

        serializer.save(
            author=self.request.user, publication=publication, pub_date=timezone.now()
        )


        
class CommentLikeView(View):
    authentication_classes = [JWTAuthentication]

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


