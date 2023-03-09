from rest_framework.views import APIView, Request, Response, status
from .models import User
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import UserSerializer
from django.shortcuts import get_object_or_404
from .permissions import IsAccountOwnerOrSuperUser
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView


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
