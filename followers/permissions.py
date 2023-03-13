from rest_framework import permissions
from rest_framework.views import View


class IsOnlyOtherUsers(permissions.BasePermission):
    def has_permission(self, request, view: View) -> bool:
        if request.method == "GET" and request.user.id == view.kwargs["user_follow_id"]:
            return True

        if request.method != "GET":
            return True
