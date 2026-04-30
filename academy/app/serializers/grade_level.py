from rest_framework import serializers

from academy.db.models import GradeLevel


class GradeLevelListSerializer(serializers.ModelSerializer):
    class Meta:
        model = GradeLevel
        fields = '__all__'
