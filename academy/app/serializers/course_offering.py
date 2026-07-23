from academy.db.models import CourseOffering
from academy.app.serializers.base import BaseSerializer
from academy.app.serializers.teacher import TeacherLiteSerializer
from academy.app.serializers.grade_level import GradeLevelPageDataSerializer
from academy.app.serializers.subject import SubjectListSerializer


class CourseOfferingPageDataSerializer(BaseSerializer):
    teacher = TeacherLiteSerializer()
    grade_level = GradeLevelPageDataSerializer()
    subject = SubjectListSerializer()

    class Meta:
        model = CourseOffering
        fields = [
            'id',
            'fee',
            'year',
            'batch',

            'teacher',
            'grade_level',
            'subject',
        ]
