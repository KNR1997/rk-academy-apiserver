# Python imports
import traceback

# Django imports
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import IntegrityError
from django_filters.rest_framework import DjangoFilterBackend

# Third part imports
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

# Module imports
from academy.utils.exception_logger import log_exception


class BaseViewSet(ModelViewSet):
    model = None

    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)

    authentication_classes = [JWTAuthentication]

    filterset_fields = []

    search_fields = []

    def get_queryset(self):
        try:
            return self.model.objects.all()
        except Exception as e:
            log_exception(e)
            raise APIException("Please check the view")

    def handle_exception(self, exc):
        """
        Handle any exception that occurs, by returning an appropriate response,
        or re-raising the error.
        """
        try:
            response = super().handle_exception(exc)
            return response
        except Exception as e:
            # (print(e, traceback.format_exc()) if settings.DEBUG else print("Server Error"))
            if isinstance(e, IntegrityError):
                return Response(
                    {"error": "The payload is not valid"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if isinstance(e, ValidationError):
                return Response(
                    {"error": "Please provide valid detail"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if isinstance(e, ObjectDoesNotExist):
                return Response(
                    {"error": "The required object does not exist."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            if isinstance(e, KeyError):
                log_exception(e)
                return Response(
                    {"error": "The required key does not exist."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            log_exception(e)
            return Response(
                {"error": "Something went wrong please try again later"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class BaseAPIView(APIView):
    permission_classes = []

    filter_backends = (DjangoFilterBackend, SearchFilter)

    authentication_classes = [JWTAuthentication]

    filterset_fields = []

    search_fields = []

    def filter_queryset(self, queryset):
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset

    def handle_exception(self, exc):

        # Log all unexpected exceptions
        if not isinstance(exc, APIException):
            log_exception(exc)

        if isinstance(exc, IntegrityError):
            return Response(
                {"error": "The payload is not valid"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if isinstance(exc, ValidationError):
            return Response(
                {"error": "Please provide valid detail"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if isinstance(exc, ObjectDoesNotExist):
            return Response(
                {"error": "The required object does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )

        return super().handle_exception(exc)
