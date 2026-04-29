# Django imports
from multiprocessing.context import AuthenticationError

from django.core.validators import validate_email
from django.views import View
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from academy.app.views.base import BaseAPIView
from academy.authentication.provider.credentials.email import EmailProvider
from academy.db.models import User


class SignInAuthEndpoint(BaseAPIView):
    def post(self, request):
        email = request.data.get("email", False)
        password = request.data.get("password", False)

        ## Raise exception if any of the above are missing
        if not email or not password:
            raise ValidationError(
                detail="Require email, password for sign-in"
            )

        # Validate email
        email = email.strip().lower()
        try:
            validate_email(email)
        except ValidationError:
            raise ValidationError(
                detail="Invalid email"
            )

        existing_user = User.objects.filter(email=email).first()

        if not existing_user:
            raise ValidationError(
                detail="Invalid credentials"
            )

        try:
            provider = EmailProvider(
                request=request,
                key=email,
                code=password,
                is_signup=False,
                callback=None,
            )
            provider.authenticate()
            token = provider.get_user_token(existing_user)

            return Response(
                {
                    'token': token
                },
                status=status.HTTP_200_OK
            )
        except AuthenticationError:
            raise ValidationError(
                detail="Invalid credentials"
            )


class SignUpAuthEndpoint(View):
    def post(self, request):
        email = request.POST.get("email", False)
        password = request.POST.get("password", False)
        ## Raise exception if any of the above are missing
        if not email or not password:
            ...
        # Validate the email
        email = email.strip().lower()
        try:
            validate_email(email)
        except ValidationError:
            ...

        # Existing user
        existing_user = User.objects.filter(email=email).first()

        if existing_user:
            ...

        try:
            provider = EmailProvider(
                request=request,
                key=email,
                code=password,
                is_signup=True,
                callback=None,
            )
            user, token = provider.authenticate()
        except AuthenticationError:
            ...
