# core/permissions/base.py
from enum import Enum
from functools import wraps

from rest_framework import status
from rest_framework.response import Response


class ROLE(Enum):
    ADMIN = 20
    TEACHER = 15
    COORDINATOR = 12
    STUDENT = 10
    GUEST = 5


ROLE_PERMISSIONS = {
    ROLE.ADMIN: ["super_admin"],
    ROLE.TEACHER: ["teacher"],
    ROLE.COORDINATOR: ["coordinator"],
    ROLE.STUDENT: ["student"],
    ROLE.GUEST: ["guest"],
}


def allow_permission(allowed_roles, creator=False, model=None):
    """
    Decorator for role and creator-based access control.
    - allowed_roles: list of ROLE enums or int values
    - creator: if True, allows the object's creator to modify it
    - model: required when creator=True
    """

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(instance, request, *args, **kwargs):
            user = request.user

            # Ensure user is authenticated
            if not user.is_authenticated:
                return Response(
                    {"detail": "Authentication required."},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            # Check if user has a role attribute (you’ll need to store this on your User model)
            user_role_value = getattr(user, "role", None)
            allowed_role_values = [
                role.value if isinstance(role, ROLE) else role for role in allowed_roles
            ]

            # Allow creator if applicable
            if creator and model and "pk" in kwargs:
                if model.objects.filter(id=kwargs["pk"], created_by=user).exists():
                    return view_func(instance, request, *args, **kwargs)

            # Allow if user role matches
            if user_role_value in allowed_role_values:
                return view_func(instance, request, *args, **kwargs)

            # Otherwise deny access
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )

        return _wrapped_view

    return decorator
