from academy.db.models import Subject
from .base import BaseSerializer


class SubjectSerializer(BaseSerializer):
    class Meta:
        model = Subject
        fields = '__all__'


class SubjectListSerializer(BaseSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name', 'slug', 'code']
