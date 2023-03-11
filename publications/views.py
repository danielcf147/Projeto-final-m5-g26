from datetime import timezone
from rest_framework.views import APIView, status, Response
from rest_framework_simplejwt.authentication import JWTAuthentication
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
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        user = self.request.user
        friends = user.user_friendship.filter(is_following=True)

        queryset = Comment.objects.none()

        private_pub_query = Comment.objects.filter(
            publication__acess_permission=Publication.AcessChoices.PRIVATE,
            publication__user=user,
        ).filter(
            publication__acess_permission__in=[Publication.AcessChoices.FRIENDS, Publication.AcessChoices.PRIVATE],
        ) | Comment.objects.filter(
            publication__acess_permission=Publication.AcessChoices.PRIVATE,
            publication__user__follower=user,
        ).filter(
            publication__acess_permission__in=[Publication.AcessChoices.FOLLOWERS, Publication.AcessChoices.PRIVATE],
        ).distinct()

        private_friends_pub_query = Comment.objects.filter(
            publication__acess_permission=Publication.AcessChoices.PRIVATE,
            publication__user__in=friends,
            publication__user__friendship__is_following=True,
        ).distinct()

        queryset = queryset.union(private_pub_query, private_friends_pub_query).distinct()
        return queryset

    def perform_create(self, serializer):
        publication_id = self.request.data.get("publication_id")
        publication = Publication.objects.get(id=publication_id)

        if publication.user != self.request.user:
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

