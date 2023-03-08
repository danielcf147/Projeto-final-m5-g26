from rest_framework import permissions
from .models import Followers
from rest_framework.views import View
import ipdb


class IsOnlyOtherUsers(permissions.BasePermission):
    def has_permission(self, request, view: View) -> bool:
        if request.method == "GET" and request.user.id == view.kwargs["user_follow_id"]:
            return True

        if request.method != "GET":
            return True
