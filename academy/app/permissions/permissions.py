# core/permissions/permissions.py
from rest_framework import permissions
from rest_framework.permissions import BasePermission

from academy.app.permissions.base import ROLE


class IsAdminOrReadOnly(BasePermission):
    """
    Allow read-only access to everyone, but restrict create/update/delete to ADMIN users.
    """

    def has_permission(self, request, view):
        # SAFE_METHODS = GET, HEAD, OPTIONS
        if request.method in permissions.SAFE_METHODS:
            return True

        # Require authentication
        if not request.user or not request.user.is_authenticated:
            return False

        # Check role
        user_role = getattr(request.user, "role", None)
        return user_role == ROLE.ADMIN.value


class IsAdminOrCreator(BasePermission):
    """
    Admins can do anything, creators can update/delete their own objects.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        user = request.user
        if not user.is_authenticated:
            return False

        user_role = getattr(user, "role", None)
        return user_role == ROLE.ADMIN.value or getattr(obj, "created_by", None) == user
