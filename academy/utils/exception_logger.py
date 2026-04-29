# Python imports
import traceback

# Third part imports
import structlog
# Django imports
from django.conf import settings


def log_exception(e):
    # Log the error
    logger = structlog.getLogger("academy.exception")
    logger.exception(
        "Unhandled exception",
        exception=str(e),
        error_type=type(e).__name__,
    )

    if settings.DEBUG:
        # Print the traceback if in debug mode
        print(traceback.format_exc())

    return
