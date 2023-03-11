from datetime import timezone
from rest_framework.views import APIView, status, Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from followers.models import Followers
from .models import Publication, Comment
from .serializers import PublicationSerializer, CommentSerializer
from .permissions import IsAccountOwner, isAuthenticated
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.views.generic import View
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from publications.models import Comment, Like
from friendships.models import Friendship
from users.models import User
<<<<<<< HEAD
import ipdb
from django.db.models.query import QuerySet
=======
from django.db.models.query import QuerySet
from rest_framework.exceptions import PermissionDenied
>>>>>>> 51b4cfd1e50d7184176b95471bf7110e51ac0f4a


class PublicationView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [isAuthenticated, IsAccountOwner]

    queryset = Publication.objects.all()
    serializer_class = PublicationSerializer

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)

    def get_queryset(self):
        if self.request.user.is_authenticated:
<<<<<<< HEAD

            user = self.request.user
            friendships = Friendship.objects.filter(user_id=user.id)
            friends = [friendship.user_friendship for friendship in friendships]
            publications = Publication.objects.filter(user__in=friends)
            publications_public = Publication.objects.filter(
                acess_permission=Publication.AcessChoices.DEFAULT
            )
            publications_list = list(publications) + list(publications_public)

            publications_queryset = QuerySet(model=Publication)
            publications_queryset._result_cache = publications_list

            return publications_queryset
=======
            return Publication.objects.all()
>>>>>>> 51b4cfd1e50d7184176b95471bf7110e51ac0f4a
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


class CommentDetailView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAccountOwner]
    serializer_class = CommentSerializer

    def get_queryset(self):
        user = self.request.user
        publication_owner = Publication.objects.filter(pk=self.kwargs["pk"]).values("user")
        followers = Followers.objects.filter(user_id=user.id, user_follow_id=publication_owner[0]["user"])

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

        queryset = queryset.union(private_pub_query, private_friends_pub_query).distinct()
        return queryset

    def perform_create(self, serializer):
        publication_id = self.request.data.get("publication_id")
        publication = Publication.objects.get(id=publication_id)

        if publication.user != self.request.user and not publication.user.user_friendship.filter(friend=self.request.user, is_following=True).exists():
            raise PermissionDenied("You are not allowed to comment on this publication")

        serializer.save(
            author=self.request.user,
            pub_date=timezone.now()
        )
        
class CommentLikeView(View):
    authentication_classes = [JWTAuthentication]

    def post(self, request, *args, **kwargs):
        comment_id = kwargs.get("pk")
        comment = get_object_or_404(Comment, pk=comment_id)
        user = request.user

        if Like.objects.filter(comment=comment, user=user).exists():
            return JsonResponse(
                {"success": False, "error": "You already liked this comment"}
            )

        Like.objects.create(comment=comment, user=user)
        return JsonResponse({"success": True})

