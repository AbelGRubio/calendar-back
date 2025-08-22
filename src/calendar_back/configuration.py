"""
Handles application configuration, including environment variable parsing,
settings management, and shared constants.

This module centralizes configuration logic to provide consistent and reusable
settings across the backend.
"""

import configparser
import os

from .utils.logger_api import LoggerApi

__version__ = "0.0.3"

LOGGER = LoggerApi("calendar_back")

conf_file = os.getenv('CONF_FILE', './conf/config.cfg')

config = configparser.ConfigParser()
config.read(conf_file)

API_IP = config.get('conf', "api_ip", fallback='0.0.0.0')
API_PORT = int(config.get('conf', "api_port", fallback='8000'))

cors_ = config.get('conf', "cors_origins", fallback='*').split(',')
CORS_ORIGINS = [c_ for c_ in cors_ if c_ != '']

LOG_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "calendar_back.utils.logger_api.ColoredFormatter",
            "format": LOGGER.msg_format,
            "datefmt": LOGGER.datetime_format,
        },
        "filefrmt": {
            "format": LOGGER.msg_format,
            "datefmt": LOGGER.datetime_format,
        },

    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "level": "DEBUG",
        },
        "file": {
            "()": "logging.handlers.TimedRotatingFileHandler",
            "formatter": "filefrmt",
            "level": "DEBUG",
            "filename": LOGGER.file_name,
            "when": "midnight",
            "interval": 1,
            "backupCount": 4,
        },
    },
    "loggers": {
        "": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
        },
        "uvicorn.error": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": False,
        },
        "uvicorn.access": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}
