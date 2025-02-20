import logging
import logging.config


def init_logging():
    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "json": {
                    "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
                    "format": "%(asctime)s %(levelname)s %(filename)s %(lineno)s %(message)s",
                }
            },
            "handlers": {
                "default": {
                    "level": "DEBUG",
                    "class": "logging.StreamHandler",
                    "formatter": "json",
                },
            },
            "loggers": {
                "__main__": {  # if you want to log from your script
                    "handlers": ["default"],
                    "level": "INFO",
                    "propagate": True,
                },
                "chat": {  # if you want to log from your script
                    "handlers": ["default"],
                    "level": "INFO",
                    "propagate": True,
                },
                "thoughts": {  # if you want to log from your script
                    "handlers": ["default"],
                    "level": "INFO",
                    "propagate": True,
                },
                "actions": {  # if you want to log from your script
                    "handlers": ["default"],
                    "level": "INFO",
                    "propagate": True,
                },
                "textworld": {  # if you want to log from your script
                    "handlers": ["default"],
                    "level": "INFO",
                    "propagate": True,
                },
                "relative_world_ollama": {  # if you want to log from your script
                    "handlers": ["default"],
                    "level": "DEBUG",
                    "propagate": True,
                },
                "relative_world": {  # if you want to log from your script
                    "handlers": ["default"],
                    "level": "DEBUG",
                    "propagate": True,
                },
            },
        }
    )
