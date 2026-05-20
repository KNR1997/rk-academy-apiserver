"""
OpenAPI utilities for drf-spectacular integration.

This module provides reusable components for API documentation:
- Authentication extensions
- Common parameters and responses
- Helper decorators
- Schema preprocessing hooks
- Examples
"""

# Parameters
from .parameters import (
    ID_PARAMETER,
    SUBJECT_SLUG_PARAMETER,
    COURSE_SLUG_PARAMETER,
)

# Responses
from .responses import (
    UNAUTHORIZED_RESPONSE,
    FORBIDDEN_RESPONSE,
    SUBJECT_NOT_FOUND_RESPONSE,
    NOT_FOUND_RESPONSE,
    TEACHER_NOT_FOUND_RESPONSE,
    create_paginated_response,
)

__all__ = [
    # Parameters
    "ID_PARAMETER",
    "SUBJECT_SLUG_PARAMETER",
    "COURSE_SLUG_PARAMETER",
    # Responses
    "UNAUTHORIZED_RESPONSE",
    "FORBIDDEN_RESPONSE",
    "SUBJECT_NOT_FOUND_RESPONSE",
    "TEACHER_NOT_FOUND_RESPONSE",
    "NOT_FOUND_RESPONSE",
    "create_paginated_response",
]
