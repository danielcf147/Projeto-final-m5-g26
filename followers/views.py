from django.shortcuts import get_object_or_404
from .models import Followers
from users.models import User
from .serializers import FollowerSerializer
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView, Request, Response, status
import ipdb


class FollowerView(ListAPIView, CreateAPIView, DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    queryset = Followers.objects.all()
    serializer_class = FollowerSerializer

    def get_queryset(self):
        user = get_object_or_404(User, pk=self.kwargs.get("user_follow_id", None))
        return Followers.objects.filter(user_id=user)

    def perform_create(self, serializer):
        user_follow = get_object_or_404(
            User, pk=self.kwargs.get("user_follow_id", None)
        )
        print(user_follow)

        serializer.save(user_follow=user_follow, user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        user_follow = get_object_or_404(
            User, pk=self.kwargs.get("user_follow_id", None)
        )
        instance = get_object_or_404(
            Followers, user_follow=user_follow, user=request.user
        )
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    lookup_url_kwarg = "user_follow_id"
