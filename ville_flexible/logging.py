import logging

import uvicorn


def configure_logging(log_level: str):
    log_level = getattr(logging, log_level, logging.INFO)

    log_config = {
        "version": 1,
        "disable_existing_loggers": True,
        "formatters": {
            "standard": {
                "()": uvicorn.logging.DefaultFormatter,
                "format": "{levelprefix} {asctime} - {name} - {message}",
                "style": "{",
                "use_colors": True,
            },
        },
        "handlers": {
            "default": {
                "level": log_level,
                "formatter": "standard",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",  # Default is stderr
            },
        },
        "loggers": {
            "ville_flexible": {
                "level": log_level,
                "handlers": ["default"],
                "propagate": False,
            },
            "": {  # root logger
                "level": log_level,
                "handlers": ["default"],
                "propagate": False,
            },
            "uvicorn.error": {
                "level": "DEBUG",
                "handlers": ["default"],
                "propagate": False,
            },
            "uvicorn.access": {
                "level": "DEBUG",
                "handlers": ["default"],
                "propagate": False,
            },
        },
    }
    logging.config.dictConfig(log_config)
