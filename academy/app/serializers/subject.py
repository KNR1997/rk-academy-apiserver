from academy.db.models import Subject
from .base import BaseSerializer


class SubjectResponseSerializer(BaseSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name', 'slug', 'code']


class SubjectCreateSerializer(BaseSerializer):
    class Meta:
        model = Subject
        fields = ['name', 'slug', 'code']


class SubjectUpdateSerializer(BaseSerializer):
    class Meta:
        model = Subject
        fields = ['name', 'slug', 'code']


class SubjectListSerializer(BaseSerializer):
    class Meta:
        model = Subject
        fields = '__all__'
