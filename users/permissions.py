from rest_framework import permissions
from .models import User
from rest_framework.views import View
import ipdb


class IsAccountOwnerOrSuperUser(permissions.BasePermission):
    def has_object_permission(self, request, view: View, obj: User) -> bool:
        return request.user.is_authenticated and (
            obj == request.user or request.user.is_superuser
        )


class IsSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_superuser
