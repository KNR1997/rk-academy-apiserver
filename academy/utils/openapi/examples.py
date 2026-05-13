"""
Common OpenAPI examples for drf-spectacular.

This module provides reusable example data for API responses and requests
to make the generated documentation more helpful and realistic.
"""

SAMPLE_GENERIC = {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "Sample Item",
    "created_at": "2024-01-15T12:00:00Z",
}

SAMPLE_SUBJECT = {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "Science",
    "slug": "science",
    "created_at": "2024-01-15T12:00:00Z",
}

# Mapping of schema types to sample data
SCHEMA_EXAMPLES = {
    "Subject": SAMPLE_SUBJECT,
}

def get_sample_for_schema(schema_name):
    """
    Get appropriate sample data for a schema type.

    Args:
        schema_name (str): Name of the schema (e.g., "PaginatedIssueResponse")

    Returns:
        dict: Sample data for the schema type
    """
    # Extract base schema name from paginated responses
    if schema_name.startswith("Paginated"):
        base_name = schema_name.replace("Paginated", "").replace("Response", "")
        return SCHEMA_EXAMPLES.get(base_name, SAMPLE_GENERIC)

    return SCHEMA_EXAMPLES.get(schema_name, SAMPLE_GENERIC)
