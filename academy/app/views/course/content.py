# Third party imports
from django.db import IntegrityError
from rest_framework import status
from rest_framework.response import Response

# Module imports
from academy.app.permissions.base import allow_permission, ROLE
from academy.app.serializers.course_content import CourseContentListSerializer, CourseContentCreateSerializer, \
    CourseContentUpdateSerializer
from academy.app.views.base import BaseViewSet, BaseAPIView
from academy.db.models import CourseContent


# Create your views here.
class CourseContentListCreateAPIEndpoint(BaseViewSet):
    """CourseContent List and Create Endpoint"""

    model = CourseContent
    serializer_class = CourseContentListSerializer

    search_fields = []
    filterset_fields = []

    def get_queryset(self):
        return (
            self.filter_queryset(super().get_queryset().prefetch_related('videos'))
        )

    @allow_permission([ROLE.ADMIN])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @allow_permission([ROLE.ADMIN])
    def create(self, request, *args, **kwargs):
        serializer = CourseContentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        course_content = serializer.save()

        output = self.serializer_class(course_content, context={"request": request}).data
        return Response(output, status=status.HTTP_201_CREATED)


class CourseContentDetailAPIEndpoint(BaseAPIView):
    """CourseContent Endpoints to update, retrieve and delete endpoint"""

    model = CourseContent
    serializer_class = CourseContentListSerializer

    search_fields = []
    filterset_fields = []

    def get_queryset(self):
        return (
            CourseContent.objects.filter(id=self.kwargs['pk'])
            .distinct()
        )

    @allow_permission([ROLE.ADMIN])
    def get(self, request, *args, pk):
        """Retrieve course content

        Retrieve details of a specific project.
        """
        course_content = self.get_queryset().get(pk=pk)
        serializer = CourseContentListSerializer(course_content)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @allow_permission([ROLE.ADMIN])
    def patch(self, request, pk):
        """Update course content

        Partially update an existing course content's properties like name, description, or settings.
        Tracks changes in model activity logs for audit purposes.
        """
        try:
            course_content = CourseContent.objects.get(pk=pk)

            serializer = CourseContentUpdateSerializer(
                course_content,
                data={**request.data},
                partial=True,
            )

            if serializer.is_valid():
                serializer.save()

                course_content = self.get_queryset().filter(pk=serializer.instance.id).first()

                serializer = CourseContentListSerializer(course_content)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
            if "already exists" in str(e):
                return Response(
                    {"name": "The project name is already taken"},
                    status=status.HTTP_409_CONFLICT,
                )
