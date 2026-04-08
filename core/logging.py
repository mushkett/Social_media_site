"""
Structlog configuration for the Social Media application.

Provides JSON-formatted structured logging for production environments.
"""

from __future__ import annotations

import sys

import structlog


def configure_structlog(debug: bool = False) -> None:
    """
    Configure structlog with appropriate processors for the environment.

    Args:
        debug: If True, use console-friendly output. If False, use JSON.
    """
    # Shared processors for both dev and prod
    shared_processors: list = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt='iso'),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.UnicodeDecoder(),
    ]

    if debug:
        # Development: colorful console output
        processors = shared_processors + [structlog.dev.ConsoleRenderer(colors=True)]
    else:
        # Production: JSON output for log aggregation
        processors = shared_processors + [structlog.processors.format_exc_info, structlog.processors.JSONRenderer()]

    structlog.configure(
        processors=processors,
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )


def get_logging_config(debug: bool = False) -> dict:
    """
    Get Django LOGGING configuration with structlog integration.

    Args:
        debug: If True, log to console with colors. If False, JSON output.

    Returns:
        Dictionary suitable for Django's LOGGING setting.
    """
    return {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'json': {
                '()': structlog.stdlib.ProcessorFormatter,
                'processor': structlog.processors.JSONRenderer(),
                'foreign_pre_chain': [
                    structlog.contextvars.merge_contextvars,
                    structlog.stdlib.add_log_level,
                    structlog.stdlib.add_logger_name,
                    structlog.processors.TimeStamper(fmt='iso'),
                ],
            },
            'console': {
                '()': structlog.stdlib.ProcessorFormatter,
                'processor': structlog.dev.ConsoleRenderer(colors=True),
                'foreign_pre_chain': [
                    structlog.contextvars.merge_contextvars,
                    structlog.stdlib.add_log_level,
                    structlog.stdlib.add_logger_name,
                    structlog.processors.TimeStamper(fmt='iso'),
                ],
            },
        },
        'handlers': {
            'console': {
                'level': 'DEBUG' if debug else 'INFO',
                'class': 'logging.StreamHandler',
                'formatter': 'console' if debug else 'json',
                'stream': sys.stdout,
            },
        },
        'root': {
            'handlers': ['console'],
            'level': 'DEBUG' if debug else 'INFO',
        },
        'loggers': {
            'django': {
                'handlers': ['console'],
                'level': 'INFO',
                'propagate': False,
            },
            'django.request': {
                'handlers': ['console'],
                'level': 'WARNING',
                'propagate': False,
            },
            'django.db.backends': {
                'handlers': ['console'],
                'level': 'WARNING',
                'propagate': False,
            },
            # Application loggers
            'accounts': {
                'handlers': ['console'],
                'level': 'DEBUG' if debug else 'INFO',
                'propagate': False,
            },
            'groups': {
                'handlers': ['console'],
                'level': 'DEBUG' if debug else 'INFO',
                'propagate': False,
            },
            'posts': {
                'handlers': ['console'],
                'level': 'DEBUG' if debug else 'INFO',
                'propagate': False,
            },
        },
    }
