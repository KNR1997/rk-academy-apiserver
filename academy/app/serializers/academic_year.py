from rest_framework import serializers

from academy.db.models import AcademicYear


class AcademicYearListSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicYear
        fields = '__all__'
