from rest_framework.views import APIView, Request, Response, status
from .models import User
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import UserSerializer
from django.shortcuts import get_object_or_404
from .permissions import IsAccountOwnerOrSuperUser, IsSuperUser
from rest_framework.generics import (
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
    ListAPIView,
)
from rest_framework.exceptions import PermissionDenied


class UserView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAccountOwnerOrSuperUser]

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_destroy(self, instance):
        setattr(instance, "is_superuser", False)
        instance.save()


class ListUserView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsSuperUser]

    queryset = User.objects.all()
    serializer_class = UserSerializer
