# Django imports
from multiprocessing.context import AuthenticationError

from django.core.validators import validate_email
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from academy.app.views.base import BaseAPIView
from academy.authentication.provider.credentials.username import UsernameProvider
from academy.db.models import User


class UsernameInitiateEndpoint(BaseAPIView):
    def post(self, request):
        username = request.data.get("username", False)
        password = request.data.get("password", False)

        ## Raise exception if any of the above are missing
        if not username or not password:
            raise ValidationError(
                detail="Require username, password for sign-in"
            )


        existing_user = User.objects.filter(username=username).first()

        if not existing_user:
            raise ValidationError(
                detail="Invalid credentials"
            )

        try:
            provider = UsernameProvider(
                request=request,
                key=username,
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
            ...
