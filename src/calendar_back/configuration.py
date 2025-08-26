"""
Handles application configuration, including environment variable parsing,
settings management, and shared constants.

This module centralizes configuration logic to provide consistent and reusable
settings across the backend.
"""

import configparser
import os
from datetime import date

from .utils.logger_api import LoggerApi

__version__ = "0.1.6"

LOGGER = LoggerApi("calendar_back")

conf_file = os.getenv('CONF_FILE', './conf/config.cfg')

config = configparser.ConfigParser()
config.read(conf_file)

API_IP = config.get('conf', "api_ip", fallback='0.0.0.0')
API_PORT = int(config.get('conf', "api_port", fallback='8000'))

cors_ = config.get('conf', "cors_origins", fallback='*').split(',')
CORS_ORIGINS = [c_ for c_ in cors_ if c_ != '']

current_year = date.today().year

HOLIDAYS = [
    {"date": f"{current_year}-01-01", "description": "Año Nuevo"},
    {"date": f"{current_year}-01-06", "description": "Epifanía del Señor"},
    {"date": f"{current_year}-04-17", "description": "Jueves Santo"},
    {"date": f"{current_year}-04-18", "description": "Viernes Santo"},
    {"date": f"{current_year}-05-01", "description": "Día del Trabajo"},
    {"date": f"{current_year}-05-02", "description": "Fiesta de la Comunidad de Madrid"},
    {"date": f"{current_year}-05-15", "description": "San Isidro"},
    {"date": f"{current_year}-08-15", "description": "Asunción de la Virgen"},
    {"date": f"{current_year}-11-01", "description": "Todos los Santos"},
    {"date": f"{current_year}-11-10", "description": "Todos los Santos"},
    {"date": f"{current_year}-12-06", "description": "Día de la Constitución Española"},
    {"date": f"{current_year}-12-08", "description": "Inmaculada Concepción"},
    {"date": f"{current_year}-12-25", "description": "Navidad"}
]


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
