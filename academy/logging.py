import os
from pathlib import Path

import structlog
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
os.makedirs(BASE_DIR / "logs", exist_ok=True)

load_dotenv()

DEBUG = os.getenv("DEBUG", "True") == "True"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json_formatter": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.processors.JSONRenderer(),
        },
        "plain_console": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.dev.ConsoleRenderer(),
        },
        "key_value": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.processors.KeyValueRenderer(key_order=['timestamp', 'level', 'event', 'logger']),
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "plain_console",
        },
        "json_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "logs/json.log",
            "maxBytes": 5 * 1024 * 1024,
            "backupCount": 5,
            "formatter": "json_formatter",
        },
        "flat_line_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "logs/flat_line.log",
            "maxBytes": 5 * 1024 * 1024,
            "backupCount": 5,
            "formatter": "key_value",
        },
        "error_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "logs/errors.log",
            "maxBytes": 5 * 1024 * 1024,
            "backupCount": 5,
            "formatter": "key_value",
        },
    },
    "loggers": {

        # Root logger
        "": {
            "handlers": ["console"] if DEBUG else ["json_file", "flat_line_file"],
            "level": "INFO",
        },

        # Django logs
        "django_structlog": {
            "handlers": ["console"] if DEBUG else ["json_file", "flat_line_file"],
            "level": "INFO",
        },

        # Your app
        "academy.app": {
            "handlers": ["console", "json_file", "flat_line_file"] if DEBUG else ["json_file", "flat_line_file"],
            "level": "INFO",
            "propagate": False,
        },

        "academy.authentication": {
            "handlers": ["console", "json_file", "flat_line_file"] if DEBUG else ["json_file", "flat_line_file"],
            "level": "INFO",
            "propagate": False,
        },

        "academy.exception": {
            "handlers": ["console", "error_file"] if DEBUG else ["error_file"],
            "level": "WARNING",
            "propagate": False,
        },

        # Make sure to replace the following logger's name for yours
        # "django_structlog_demo_project": {
        #     "handlers": ["console"],
        #     "level": "INFO",
        # },
    },
}

# LOGGING = {
#     "version": 1,
#     "disable_existing_loggers": False,
#
#     "formatters": {
#         "verbose": {
#             "format": "{levelname} {asctime} {name} {module} {message}",
#             "style": "{",
#         },
#         "simple": {
#             "format": "{levelname} {name} {message}",
#             "style": "{",
#         },
#     },
#
#     "handlers": {
#         "console": {
#             "class": "logging.StreamHandler",
#             "formatter": "simple",
#         },
#
#         "django_file": {
#             "class": "logging.FileHandler",
#             "filename": os.path.join(BASE_DIR, "logs/django.log"),
#             "formatter": "verbose",
#             "level": "INFO",
#         },
#
#         "app_file": {
#             "class": "logging.FileHandler",
#             "filename": os.path.join(BASE_DIR, "logs/app.log"),
#             "formatter": "verbose",
#             "level": "DEBUG",
#         },
#
#         "error_file": {
#             "class": "logging.FileHandler",
#             "filename": os.path.join(BASE_DIR, "logs/errors.log"),
#             "formatter": "verbose",
#             "level": "ERROR",
#         },
#     },
#
#     "loggers": {
#
#         # Root logger (fallback)
#         "": {
#             "handlers": ["console"],
#             "level": "INFO",
#         },
#
#         # Django internal logs
#         "django": {
#             "handlers": ["console", "django_file"],
#             "level": "INFO",
#             "propagate": False,
#         },
#
#         # Your application logs
#         # "academy.app": {
#         #     "handlers": ["console", "app_file", "error_file"],
#         #     "level": "WARNING",
#         #     "propagate": False,
#         # },
#
#         # "academy.authentication": {
#         #     "handlers": ["console", "app_file", "error_file"],
#         #     "level": "WARNING",
#         #     "propagate": False,
#         # },
#
#         "academy.exception": {
#             "handlers": ["console", "error_file"],
#             "level": "WARNING",
#             "propagate": False,
#         },
#     },
# }
