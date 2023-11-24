import logging.config
import os

import structlog

DIR_PATH = "storage"
FILE_NAME = "log_file"

if not os.path.exists(DIR_PATH):
    try:
        os.makedirs(DIR_PATH)
    except OSError as e:
        print(f"Failed to create folder '{DIR_PATH}': {e}")

logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "structured",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": f"{DIR_PATH}/{FILE_NAME}.log",
            "maxBytes": 10485760,
            "backupCount": 5,
            "formatter": "structured",
        },
    },
    "loggers": {
        "": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False,
        },
    },
    "formatters": {
        "structured": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.dev.ConsoleRenderer(
                colors=True,
            ),
        },
    },
}

structlog.configure(
    processors=[
        structlog.stdlib.add_log_level_number,
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        structlog.processors.JSONRenderer(
            indent=2
        ),  # Improved JSON rendering with indentation
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

# Apply logging configuration
logging.config.dictConfig(logging_config)
logger = structlog.getLogger()
