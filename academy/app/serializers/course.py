from academy.db.models import Course, CourseOffering
from .base import BaseSerializer
from .grade_level import GradeLevelListSerializer
from .subject import SubjectListSerializer
from .teacher import TeacherListSerializer


class CourseListSerializer(BaseSerializer):
    subject = SubjectListSerializer()

    class Meta:
        model = Course
        fields = (
            "id",
            "name",
            "code",
            "slug",
            "subject",
        )


class CourseSerializer(BaseSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class CourseOfferingListSerializer(BaseSerializer):
    course = CourseListSerializer()
    teacher = TeacherListSerializer()
    grade_level = GradeLevelListSerializer()

    class Meta:
        model = CourseOffering
        fields = [
            'id',
            'course',
            'teacher',
            'fee',
            'year',
            'batch',
            'grade_level'
        ]


class CourseOfferingSerializer(BaseSerializer):
    class Meta:
        model = CourseOffering
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.fee = validated_data.get('fee', instance.fee)
        instance.save(update_fields=['fee'])
        return instance


class CourseOfferingLiteSerializer(BaseSerializer):
    grade_level = GradeLevelListSerializer()
    course = CourseListSerializer()

    class Meta:
        model = CourseOffering
        fields = [
            'id',
            'fee',
            'year',
            'batch',

            'grade_level',
            'course',
        ]
