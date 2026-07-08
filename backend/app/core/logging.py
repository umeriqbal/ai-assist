import logging
import sys

import structlog

from app.core.config import settings


def configure_logging() -> None:
    """
    Configure application logging.
    """

    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper()),
        format="%(message)s",
        stream=sys.stdout,
    )

    structlog.configure(
        wrapper_class=structlog.make_filtering_bound_logger(
            getattr(logging, settings.log_level.upper())
        ),
        logger_factory=structlog.PrintLoggerFactory(),
    )


logger = structlog.get_logger()