"""
Common OpenAPI parameters for drf-spectacular.

This module provides reusable parameter definitions that can be shared
across multiple API endpoints to ensure consistency.
"""

from drf_spectacular.utils import OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes

# Path Parameters
SUBJECT_SLUG_PARAMETER = OpenApiParameter(
    name="slug",
    description="Subject slug",
    required=True,
    type=OpenApiTypes.STR,
    location=OpenApiParameter.PATH,
    examples=[
        OpenApiExample(
            name="Example subject",
            value="science",
            description="A typical subject slug",
        )
    ],
)

COURSE_SLUG_PARAMETER = OpenApiParameter(
    name="slug",
    description="Course slug",
    required=True,
    type=OpenApiTypes.STR,
    location=OpenApiParameter.PATH,
    examples=[
        OpenApiExample(
            name="Example course",
            value="ict-2026",
            description="A typical course slug",
        )
    ],
)

ID_PARAMETER = OpenApiParameter(
    name="id",
    description="Model id",
    required=True,
    type=OpenApiTypes.STR,
    location=OpenApiParameter.PATH,
    examples=[
        OpenApiExample(
            name="Example model id",
            value="43535353434",
            description="A typical model id",
        )
    ],
)
