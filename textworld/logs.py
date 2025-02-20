import logging
import logging.config


def init_logging():
    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "standard": {
                    "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
                },
            },
            "handlers": {
                "default": {
                    "level": "DEBUG",
                    "formatter": "standard",
                    "class": "logging.StreamHandler",
                    "stream": "ext://sys.stdout",  # Default is stderr
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
                    "level": "WARN",
                    "propagate": True,
                },
                "relative_world": {  # if you want to log from your script
                    "handlers": ["default"],
                    "level": "WARN",
                    "propagate": True,
                },
            },
        }
    )
