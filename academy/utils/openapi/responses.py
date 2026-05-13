"""
Common OpenAPI responses for drf-spectacular.

This module provides reusable response definitions for common HTTP status codes
and scenarios that occur across multiple API endpoints.
"""

from drf_spectacular.utils import OpenApiResponse, OpenApiExample, inline_serializer
from rest_framework import serializers
from .examples import get_sample_for_schema

# Authentication & Authorization Responses
UNAUTHORIZED_RESPONSE = OpenApiResponse(
    description="Authentication credentials were not provided or are invalid.",
    examples=[
        OpenApiExample(
            name="Unauthorized",
            value={
                "error": "Authentication credentials were not provided",
                "error_code": "AUTHENTICATION_REQUIRED",
            },
        )
    ],
)

FORBIDDEN_RESPONSE = OpenApiResponse(
    description="Permission denied. User lacks required permissions.",
    examples=[
        OpenApiExample(
            name="Forbidden",
            value={
                "error": "You do not have permission to perform this action",
                "error_code": "PERMISSION_DENIED",
            },
        )
    ],
)

# Resource Responses
NOT_FOUND_RESPONSE = OpenApiResponse(
    description="The requested resource was not found.",
    examples=[
        OpenApiExample(
            name="Not Found",
            value={"error": "Not found", "error_code": "RESOURCE_NOT_FOUND"},
        )
    ],
)

VALIDATION_ERROR_RESPONSE = OpenApiResponse(
    description="Validation error occurred with the provided data.",
    examples=[
        OpenApiExample(
            name="Validation Error",
            value={
                "error": "Validation failed",
                "details": {"field_name": ["This field is required."]},
            },
        )
    ],
)

# Generic Success Responses
DELETED_RESPONSE = OpenApiResponse(
    description="Resource deleted successfully",
    examples=[
        OpenApiExample(
            name="Deleted Successfully",
            value={"message": "Resource deleted successfully"},
        )
    ],
)

# Subject-specific Responses
SUBJECT_NOT_FOUND_RESPONSE = OpenApiResponse(
    description="Subject not found",
    examples=[
        OpenApiExample(
            name="Subject Not Found",
            value={"error": "Subject not found"},
        )
    ],
)


# Pagination Response Templates
def create_paginated_response(
    item_schema,
    schema_name,
    description="Paginated results",
    example_name="Paginated Response",
):
    """Create a paginated response with the specified item schema"""

    return OpenApiResponse(
        description=description,
        response=inline_serializer(
            name=schema_name,
            fields={
                # "grouped_by": serializers.CharField(allow_null=True),
                # "sub_grouped_by": serializers.CharField(allow_null=True),
                # "next_cursor": serializers.CharField(),
                # "prev_cursor": serializers.CharField(),
                # "next_page_results": serializers.BooleanField(),
                # "prev_page_results": serializers.BooleanField(),
                # "count": serializers.IntegerField(),
                # "total_pages": serializers.IntegerField(),
                # "total_results": serializers.IntegerField(),
                # "extra_stats": serializers.CharField(allow_null=True),
                "current_page": serializers.IntegerField(),
                "first_page_url": serializers.CharField(),
                "from": serializers.IntegerField(),
                "last_page": serializers.IntegerField(),
                "last_page_url": serializers.CharField(),
                "links": serializers.IntegerField(),
                "next_page_url": serializers.CharField(),
                "path": serializers.CharField(),
                "per_page": serializers.IntegerField(),
                "prev_page_url": serializers.CharField(),
                "to": serializers.IntegerField(),
                "total": serializers.IntegerField(),
                "data": serializers.ListField(child=item_schema()),
            },
        ),
        examples=[
            OpenApiExample(
                name=example_name,
                value={
                    # "grouped_by": "state",
                    # "sub_grouped_by": "priority",
                    # "total_count": 150,
                    # "next_cursor": "20:1:0",
                    # "prev_cursor": "20:0:0",
                    # "next_page_results": True,
                    # "prev_page_results": False,
                    # "count": 20,
                    # "total_pages": 8,
                    # "total_results": 150,
                    # "extra_stats": None,
                    "current_page": 1,
                    "first_page_url": None,
                    "from": 1,
                    "last_page": 1,
                    "last_page_url": None,
                    "links": None,
                    "next_page_url": None,
                    "path": None,
                    "per_page": 1,
                    "prev_page_url": None,
                    "to": 1,
                    "total": 10,
                    "data": [get_sample_for_schema(schema_name)],
                },
                summary=example_name,
            )
        ],
    )
