from rest_framework import permissions
from .models import User
from rest_framework.views import View
import ipdb


class IsAccountOwner(permissions.BasePermission):
    def has_object_permission(self, request, view: View, obj: User) -> bool:
        ipdb.set_trace()
        return request.user.is_authenticated and obj == request.user
