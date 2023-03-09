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

class PublicationView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [isAuthenticated, IsAccountOwner]

    queryset = Publication.objects.all()
    serializer_class = PublicationSerializer

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)


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
        # ipdb.set_trace()
        serializer.save(user_id=self.request.user.id, publication_id=self.kwargs["pk"])


class CommentDetailView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAccountOwner]

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class CommentLikeView(View):
    authentication_classes = [JWTAuthentication]

    def post(self, request, *args, **kwargs):
        comment_id = kwargs.get("pk")
        comment = get_object_or_404(Comment, pk=comment_id)
        user = request.user

        if Like.objects.filter(comment=comment, user=user).exists():
            return JsonResponse({"success": False, "error": "You already liked this comment"})

        Like.objects.create(comment=comment, user=user)
        return JsonResponse({"success": True})