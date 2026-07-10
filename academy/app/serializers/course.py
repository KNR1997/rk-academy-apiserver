from academy.db.models import Course, CourseOffering
from .base import BaseSerializer
from .grade_level import GradeLevelListSerializer
from .subject import SubjectResponseSerializer
from .teacher import TeacherListSerializer


class CourseResponseSerializer(BaseSerializer):
    subject = SubjectResponseSerializer()

    class Meta:
        model = Course
        fields = (
            "id",
            "name",
            "code",
            "slug",
            "subject",
        )


class CourseLiteSerializer(BaseSerializer):
    class Meta:
        model = Course
        fields = (
            "id",
            "name",
            "code",
            "slug",
        )


class CourseSerializer(BaseSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class CourseCreateSerializer(BaseSerializer):
    class Meta:
        model = Course
        fields = ["name", "code", "slug", "subject"]


class CourseUpdateSerializer(BaseSerializer):
    class Meta:
        model = Course
        fields = ["name", "code", "slug", "subject"]


class CourseOfferingListSerializer(BaseSerializer):
    subject = SubjectResponseSerializer()
    teacher = TeacherListSerializer()
    grade_level = GradeLevelListSerializer()

    class Meta:
        model = CourseOffering
        fields = [
            'id',
            'subject',
            'teacher',
            'fee',
            'year',
            'batch',
            'grade_level'
        ]


class CourseOfferingResponseSerializer(BaseSerializer):
    class Meta:
        model = CourseOffering
        fields = [
            'id',
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
        instance.subject = validated_data.get('subject', instance.subject)
        instance.fee = validated_data.get('fee', instance.fee)
        instance.save(update_fields=['subject', 'fee'])
        return instance


class CourseOfferingCreateSerializer(BaseSerializer):
    class Meta:
        model = CourseOffering
        fields = [
            'subject', 
            'teacher', 
            'grade_level', 
            'fee', 
            'year', 
            'batch'
        ]


class CourseOfferingLiteSerializer(BaseSerializer):
    grade_level = GradeLevelListSerializer()
    course = CourseResponseSerializer()

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
