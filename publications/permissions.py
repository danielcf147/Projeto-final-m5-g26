from rest_framework import permissions
from .models import Publication
from rest_framework.views import View


class isAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated


class IsAccountOwner(permissions.BasePermission):
    def has_object_permission(self, request, view: View, obj: Publication) -> bool:

        return request.user.is_authenticated and obj.user == request.user
