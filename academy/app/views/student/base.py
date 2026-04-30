# Third party imports
import structlog
from rest_framework import status
from rest_framework.response import Response

# Module imports
from academy.app.permissions.base import allow_permission, ROLE
from academy.app.serializers.course import CourseOfferingListSerializer
from academy.app.serializers.enrollment import EnrollmentListSerializer
from academy.app.serializers.student import StudentListSerializer, StudentCreateSerializer, StudentUpdateSerializer
from academy.app.views.base import BaseViewSet, BaseAPIView
from academy.db.models import Student, Enrollment, CourseOffering

logger = structlog.getLogger(__name__)


class StudentViewSet(BaseViewSet):
    model = Student
    serializer_class = StudentListSerializer

    search_fields = ['user__email', 'user__first_name', 'user__last_name']
    ordering_fields = ['user__first_name', 'created_at']

    def get_queryset(self):
        queryset = (
            self.filter_queryset(
                super().get_queryset().select_related(
                    'user',
                    'current_grade',
                    'current_academic_year'
                )
            )
        )
        logger.info("student_queryset_loaded", user_id=self.request.user.id, role=self.request.user.role)
        return queryset

    @allow_permission([ROLE.ADMIN, ROLE.COORDINATOR])
    def list(self, request, *args, **kwargs):
        logger.info("student_list_requested", requested_by=request.user.id, role=request.user.role)
        return super().list(request, *args, **kwargs)

    @allow_permission([ROLE.ADMIN, ROLE.COORDINATOR])
    def create(self, request, *args, **kwargs):
        logger.info("student_create_started", requested_by=request.user.id)

        serializer = StudentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        student = serializer.save()

        logger.info("student_created", student_id=student.id, student_number=student.student_number,
                    created_by=request.user.id)
        return Response(StudentListSerializer(student).data, status=status.HTTP_201_CREATED)

    @allow_permission([ROLE.ADMIN, ROLE.COORDINATOR])
    def update(self, request, *args, **kwargs):
        logger.info("student_update_started", requested_by=request.user.id)

        student = Student.objects.get(pk=kwargs["pk"])
        serializer = StudentUpdateSerializer(
            student,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        student = serializer.save()

        logger.info("student_updated", student_id=student.id, student_number=student.student_number,
                    created_by=request.user.id)

        output = StudentListSerializer(student, context={"request": request}).data
        return Response(output, status=status.HTTP_200_OK)

    @allow_permission([ROLE.ADMIN, ROLE.COORDINATOR])
    def destroy(self, request, *args, **kwargs):
        logger.info("student_delete_requested", requested_by=request.user.id)

        super().destroy(request, *args, **kwargs)

        logger.info("student_deleted", requested_by=request.user.id)
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class StudentEnrolledCoursesEndpoint(BaseAPIView):
    @allow_permission([ROLE.ADMIN])
    def get(self, request, pk):
        logger.info("student_enrolled_courses_requested", student_id=pk, requested_by=request.user.id)

        student = Student.objects.get(pk=pk)

        # Get all course_offerings the student is enrolled in
        course_offerings = CourseOffering.objects.filter(enrollments__student=student)

        logger.info("student_enrolled_courses_loaded", student_id=pk, total_courses=course_offerings.count())

        output = CourseOfferingListSerializer(course_offerings, many=True).data
        return Response(output, status=status.HTTP_200_OK)


class StudentMeEnrollmentsEndpoint(BaseAPIView):
    @allow_permission([ROLE.ADMIN])
    def get(self, request):
        logger.info("student_me_enrollments_requested", user_id=request.user.id)

        student = Student.objects.get(user=request.user)

        # Get all courses the student is enrolled in
        enrollments = Enrollment.objects.filter(student=student)

        logger.info("student_me_enrollments_loaded", student_id=student.id, total=enrollments.count())

        output = EnrollmentListSerializer(enrollments, many=True).data
        return Response(output, status=status.HTTP_200_OK)


class StudentEnrollmentsEndpoint(BaseAPIView):
    @allow_permission([ROLE.ADMIN])
    def get(self, request, pk):
        logger.info("student_enrollments_requested", student_id=pk, requested_by=request.user.id)

        enrollments = Enrollment.objects.filter(student_id=pk)

        logger.info("student_enrollments_loaded", student_id=pk, total=enrollments.count())

        output = EnrollmentListSerializer(enrollments, many=True).data
        return Response(output, status=status.HTTP_200_OK)
