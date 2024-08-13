from unittest import TestCase
from unittest.mock import patch, Mock

from ..logconf import (
    set_default_logging,
    default_format,
    thread_format,
    set_module_logger,
    log_conf_factory,
    add_console_handler,
)


SRC = "bat.logconf"


class LogConfTests(TestCase):
    log: Mock
    getLogger: Mock
    Formatter: Mock

    def setUp(t):
        patches = [
            "log",
            "getLogger",
            "Formatter",
        ]
        for target in patches:
            patcher = patch(f"{SRC}.{target}", autospec=True)
            setattr(t, target, patcher.start())
            t.addCleanup(patcher.stop)

        t.default_log_level = "INFO"
        t.log_level = "DEBUG"
        t.default_file_name = "log/bat.log"
        t.file_name = "/tmp/log/bat.log"
        t.default_log_format = default_format
        t.log_format = "CUSTOM: %(message)s"
        t.default_thread_handler_format = thread_format
        t.thread_handler_format = "CUSTOM THREAD: %(message)s"

        t.default_conf_dict = dict(
            version=1,
            formatters={
                "f": {"format": t.default_log_format},
                "thread_formatter": {
                    "format": t.default_thread_handler_format,
                },
            },
            root={"handlers": [], "level": t.default_log_level},
            loggers={
                "bat": {},
                "thread": {
                    "handlers": [],
                    "level": t.default_log_level,
                    "propagate": False,
                },
            },
        )

    @patch(f"{SRC}.add_console_handler")
    @patch(f"{SRC}.set_module_logger")
    def test_set_default_logging(
        t,
        set_module_logger: Mock,
        add_console_handler: Mock,
    ):
        set_default_logging(log_level=t.log_level)

        set_module_logger.assert_called_with(log_level=t.log_level)
        add_console_handler.assert_called_with(log_level=t.log_level)
        t.log.info.assert_called_with(
            f"set default logging level={t.log_level}"
        )

    @patch(f"{SRC}.add_console_handler")
    @patch(f"{SRC}.set_module_logger")
    def test_set_default_logging_defaults(
        t,
        set_module_logger: Mock,
        add_console_handler: Mock,
    ):
        set_default_logging()

        set_module_logger.assert_called_with(log_level="INFO")
        add_console_handler.assert_called_with(log_level=t.default_log_level)
        t.log.info.assert_called_with(
            f"set default logging level={t.default_log_level}"
        )

    @patch(f"{SRC}.dictConfig")
    @patch(f"{SRC}.log_conf_factory")
    def test_set_module_logger_defaults(
        t,
        log_conf_factory: Mock,
        dictConfig: Mock,
    ):
        set_module_logger()

        log_conf_factory.assert_called_with(
            log_level=t.default_log_level,
            log_format=t.default_log_format,
            thread_handler_format=t.default_thread_handler_format,
        )
        dictConfig.assert_called_with(log_conf_factory.return_value)

    @patch(f"{SRC}.dictConfig")
    @patch(f"{SRC}.log_conf_factory")
    def test_set_module_logger(
        t,
        log_conf_factory: Mock,
        dictConfig: Mock,
    ):
        set_module_logger(
            log_level=t.log_level,
            log_format=t.log_format,
            thread_handler_format=t.thread_handler_format,
        )

        log_conf_factory.assert_called_with(
            log_level=t.log_level,
            log_format=t.log_format,
            thread_handler_format=t.thread_handler_format,
        )
        dictConfig.assert_called_with(log_conf_factory.return_value)

    def test_log_conf_factory_defaults(t):
        ret = log_conf_factory()
        t.assertEqual(ret, t.default_conf_dict)

    def test_log_conf_factory(t):
        ret = log_conf_factory(
            log_level=t.log_level,
            log_format=t.log_format,
            thread_handler_format=t.thread_handler_format,
        )
        t.assertDictEqual(
            ret,
            dict(
                version=1,
                formatters={
                    "f": {"format": t.log_format},
                    "thread_formatter": {
                        "format": t.thread_handler_format,
                    },
                },
                root={"handlers": [], "level": t.log_level},
                loggers={
                    "bat": {},
                    "thread": {
                        "handlers": [],
                        "level": t.log_level,
                        "propagate": False,
                    },
                },
            ),
        )

    @patch(f"{SRC}.StreamHandler")
    def test_add_console_handler_defaults(t, StreamHandler: Mock):
        add_console_handler()

        t.getLogger.assert_called_with()
        sh = StreamHandler.return_value
        sh.setLevel.assert_called_with(t.default_log_level)
        sh.setFormatter.assert_called_with(t.Formatter.return_value)
        t.Formatter.assert_called_with(t.default_log_format)

        root = t.getLogger.return_value
        root.addHandler.assert_called_with(sh)
        t.log.info.assert_called_with("added console logger")

    @patch(f"{SRC}.StreamHandler")
    def test_add_console_handler(t, StreamHandler: Mock):
        add_console_handler(
            log_level=t.log_level,
            log_format=t.log_format,
        )

        t.getLogger.assert_called_with()
        sh = StreamHandler.return_value
        sh.setLevel.assert_called_with(t.log_level)
        sh.setFormatter.assert_called_with(t.Formatter.return_value)
        t.Formatter.assert_called_with(t.log_format)

        root = t.getLogger.return_value
        root.addHandler.assert_called_with(sh)
        t.log.info.assert_called_with("added console logger")
