from logging import getLogger, DEBUG, StreamHandler, Formatter
from logging.config import dictConfig


log = getLogger(__name__)

default_format = "%(asctime)s %(name)-12s %(levelname)-8s %(message)s"
thread_format = "%(asctime)s %(threadName)-12s %(levelname)-8s %(message)s"
default_formatter = Formatter(default_format)


logging_config = dict(
    version=1,
    formatters={
        "f": {"format": default_format},
        "thread_formatter": {
            "format": thread_format,
        },
    },
    handlers={
        "h": {"class": "logging.StreamHandler", "formatter": "f"},
        "thread_handler": {
            "class": "logging.StreamHandler",
            "formatter": "thread_formatter",
        },
    },
    root={"handlers": ["h"], "level": DEBUG},
    loggers={
        "bat": {},
        "thread": {
            "handlers": ["thread_handler"],
            "level": DEBUG,
            "propagate": False,
        },
    },
)


base_config = dict(
    version=1,
    disable_existing_loggers=False,
    formatters={
        "f": {"format": default_format},
        "thread_formatter": {"format": thread_format},
    },
    root={"handlers": [], "level": DEBUG},
    loggers={
        "bat": {},
        "thread": {
            "handlers": [],
            "level": DEBUG,
            "propagate": False,
        },
    },
)


_module_logger = dict(
    version=1,
    loggers={"bat": {}},
)


def set_default_logging(log_level: str = "INFO"):
    set_module_logger(log_level=log_level)
    add_console_handler(log_level=log_level)
    log.info(f"set default logging level={log_level}")


def set_module_logger(
    log_level: str = "INFO",
    log_format: str = default_format,
    thread_handler_format: str = thread_format,
):
    config = log_conf_factory(
        log_level=log_level,
        log_format=log_format,
        thread_handler_format=thread_handler_format,
    )
    dictConfig(config)


def log_conf_factory(
    log_level: str = "INFO",
    log_format: str = default_format,
    thread_handler_format: str = thread_format,
):
    return dict(
        version=1,
        formatters={
            "f": {"format": log_format},
            "thread_formatter": {"format": thread_handler_format},
        },
        root={"handlers": [], "level": log_level},
        loggers={
            "bat": {},
            "thread": {
                "handlers": [],
                "level": log_level,
                "propagate": False,
            },
        },
    )


def add_console_handler(
    log_level: str = "INFO",
    log_format: str = default_format,
):
    root_logger = getLogger()
    # create a console handler
    console_handler = StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(Formatter(log_format))

    root_logger.addHandler(console_handler)
    log.info("added console logger")
