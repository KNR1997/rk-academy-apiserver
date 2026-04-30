from rest_framework import serializers

from academy.db.models import CourseContent, Video
from .base import BaseSerializer
from .course import CourseOfferingLiteSerializer


class VideoCreateSerializer(BaseSerializer):
    """
    Serializer for creating video with course content validation and date checking.
    """

    month = serializers.IntegerField()
    year = serializers.IntegerField()
    course_offering_id = serializers.UUIDField()

    class Meta:
        model = Video
        fields = [
            'title',
            'video_url',
            'month',
            'year',
            'course_offering_id',
        ]

    def create(self, validated_data):
        month = validated_data.pop('month')
        year = validated_data.pop('year')
        course_offering_id = validated_data.pop('course_offering_id')

        course_content, created = CourseContent.objects.get_or_create(
            month=month,
            year=year,
            course_offering_id=course_offering_id,
        )

        video = Video.objects.create(
            **validated_data,
            course_content=course_content
        )

        return video


class CourseContentCreateSerializer(BaseSerializer):
    video = VideoCreateSerializer()

    class Meta:
        model = CourseContent
        fields = '__all__'

    def create(self, validated_data):
        month = validated_data.get('month')
        year = validated_data.get('year')
        course_offering = validated_data.get('course_offering')

        course_content, created = CourseContent.objects.get_or_create(
            course_offering=course_offering,
            month=month,
            year=year,
        )

        # save video serializer data
        video_data = validated_data.pop('video')
        Video.objects.create(
            course_content=course_content,
            **video_data,
        )

        return course_content


class CourseContentUpdateSerializer(CourseContentCreateSerializer):
    """
    Serializer for updating course content with enhanced state and estimation management.

    Extends project creation with update-specific validations including default state
    assignment, estimation configuration, and project setting modifications.
    """

    class Meta:
        model = CourseContent
        fields = '__all__'


class CourseContentListSerializer(BaseSerializer):
    class Meta:
        model = CourseContent
        fields = [
            'id',
            'month',
            'year',

            'videos'
        ]


class CourseContentLiteSerializer(BaseSerializer):
    course_offering = CourseOfferingLiteSerializer()

    class Meta:
        model = CourseContent
        fields = [
            'id',
            'month',
            'year',

            'course_offering',
        ]


class VideoUpdateSerializer(BaseSerializer):
    """
    Serializer for updating video.
    """

    month = serializers.IntegerField()
    year = serializers.IntegerField()
    course_offering_id = serializers.UUIDField()

    class Meta:
        model = Video
        fields = [
            'title',
            'video_url',
            'month',
            'year',
            'course_offering_id',
        ]

    def update(self, instance, validated_data):
        month = validated_data.pop('month')
        year = validated_data.pop('year')
        course_offering_id = validated_data.pop('course_offering_id')

        course_content, created = CourseContent.objects.get_or_create(
            month=month,
            year=year,
            course_offering_id=course_offering_id,
        )

        validated_data['course_content_id'] = course_content.id

        return super().update(instance, validated_data)


class VideoListSerializer(BaseSerializer):
    course_content = CourseContentLiteSerializer()

    class Meta:
        model = Video
        fields = [
            'id',
            'title',
            'video_url',

            'course_content'
        ]


class VideoLiteSerializer(BaseSerializer):
    class Meta:
        model = Video
        fields = [
            'id',
            'title',
            'video_url',
        ]
