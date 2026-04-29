# Third party imports
import structlog
from rest_framework import status, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

# Django imports
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password

# Module imports
from academy.app.permissions.base import ROLE
from academy.app.permissions.permissions import IsAdminOrReadOnly
from academy.app.serializers.authentication import SignupSerializer, SigninSerializer, ChangePasswordSerializer, \
    ChangeEmailSerializer
from academy.app.serializers.user import UserLiteSerializer
from academy.app.views.base import BaseAPIView
from academy.db.models import User

logger = structlog.getLogger(__name__)


# Create your views here.
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class SignupView(APIView):
    def post(self, request):
        logger.info("signup_started", requested_by=request.user.id)

        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            tokens = get_tokens_for_user(user)
            return Response(
                {'user': serializer.data, 'tokens': tokens},
                status=status.HTTP_201_CREATED
            )

        logger.info("signup_completed", requested_by=request.user.id)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SigninView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        logger.info("signin_started")

        serializer = SigninSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            request,
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password']
        )

        if not user:
            return Response(
                {'detail': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        output = {
            'tokens': get_tokens_for_user(user),
            'permissions': user.permissions,
            'role': user.role_name,
        }

        logger.info("signin_completed", requested_by=user.id)
        return Response(output, status=status.HTTP_200_OK)


class CreateAdminView(APIView):
    permission_classes = []

    def post(self, request):
        logger.info("create_admin_started", requested_by=request.user.id)

        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.role = ROLE.ADMIN.value
        user.is_staff = True
        user.is_superuser = True
        user.save()

        logger.info("create_admin_completed", requested_by=request.user.id)
        return Response(
            {"detail": "Admin user created successfully"},
            status=status.HTTP_201_CREATED
        )


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # logger.info("me_data_requested", requested_by=request.user.id)

        serializer = UserLiteSerializer(request.user)
        return Response(serializer.data)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logger.info("user_logout", requested_by=request.user.id)
        return Response(status=HTTP_200_OK)


class ChangePasswordEndpoint(BaseAPIView):
    def post(self, request):
        logger.info("change_password_started", requested_by=request.user.id)

        serializer = ChangePasswordSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)

        user = request.user
        new_password = serializer.validated_data['new_password']

        user.set_password(new_password)
        user.save()

        logger.info("change_password_completed", requested_by=request.user.id)
        return Response(status=status.HTTP_200_OK)


class ChangeEmailEndpoint(BaseAPIView):
    def post(self, request):
        logger.info("change_email_started", requested_by=request.user.id)

        serializer = ChangeEmailSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)

        user = request.user
        new_email = serializer.validated_data['email']

        if user.email != new_email:
            if User.objects.filter(email=new_email).exists():
                raise serializers.ValidationError({
                    "email": "A user with this email already exists."
                })

        user.email = new_email
        user.save()

        logger.info("change_email_started", requested_by=request.user.id)
        return Response(status=status.HTTP_200_OK)


class InitializeAdminView(APIView):
    permission_classes = []

    def post(self, request):
        logger.info("initialize_admin_started", requested_by=request.user.id)

        User.objects.create(
            username='John_Doe',
            email='admin@demo.com',
            role=ROLE.ADMIN.value,
            mobile_number='0113123888',
            password=make_password('demodemo')
        )

        logger.info("initialize_admin_completed", requested_by=request.user.id)
        return Response(
            {"detail": "Admin initialized successfully"},
            status=status.HTTP_201_CREATED
        )
