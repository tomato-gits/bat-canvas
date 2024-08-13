from unittest import TestCase
from unittest.mock import patch, Mock

from ..cli import (
    argparser,
    BATCLI,
    Namespace,
    Commands,
    logging,
    argparser,
)

from logging import getLogger

log = getLogger(__name__)


SRC = "bat.cli"


class ArgparserTests(TestCase):
    def test_argparser(t):
        argparser()


class BATCLITests(TestCase):
    exit: callable

    def setUp(t):
        patches = [
            "exit",
        ]
        for target in patches:
            patcher = patch(f"{SRC}.{target}", autospec=True)
            setattr(t, target, patcher.start())
            t.addCleanup(patcher.stop)

    def validate_commands(t, commands):
        for cmd in commands:
            with t.subTest(cmd):
                func = "_".join(cmd.split())
                with patch(f"{SRC}.Commands.{func}", autospec=True) as m_cmd:
                    m_cmd.__name__ = func
                    ARGS = cmd.split()
                    BATCLI(ARGS)
                    args = argparser().parse_args(ARGS)
                    m_cmd.assert_called_with(args)
                    t.exit.assert_called_with(0)

    @patch(f"{SRC}.Commands.setup_logging", autospec=True)
    def test_setup_logging(t, setup_logging: Mock):
        ARGS = [
            "--debug",
            "hello",
        ]
        parsed_args = argparser().parse_args(ARGS)

        with patch(f"{SRC}.argparser", autospec=True) as parser:
            parser.return_value.parse_args.return_value = parsed_args
            BATCLI(ARGS)

        setup_logging.assert_called_with(parsed_args)
        t.exit.assert_called_with(0)

    @patch(f"{SRC}.log", autospec=True)
    @patch(f"{SRC}.argparser", wraps=argparser)
    def test_command_error(t, argparser: Mock, mlog: Mock):
        """prints the error message, and help if a command throws an error"""
        ARGS = ["hello"]
        exc = RuntimeError("test error")

        def bomb(_: Namespace):
            print("set up the bomb")
            raise exc

        parser = argparser()
        args = parser.parse_args(ARGS)
        args.func = bomb
        parser.parse_args = Mock(parser.parse_args)
        parser.parse_args.return_value = args
        parser.print_help = Mock(parser.print_help)
        argparser.return_value = parser

        BATCLI(ARGS)

        parser.print_help.assert_called_with()
        mlog.exception.assert_called_with(exc)

    def test_commands(t):
        commands = [
            "hello",
        ]

        t.validate_commands(commands)


class NestedNameSpaceTests(TestCase):

    def test_nesting(t):
        nns = NestedNameSpace()
        setattr(nns, "top", "level")
        setattr(nns, "bat.baz", "baz")
        setattr(nns, "bat.sub.var", "sub_var")

        t.assertEqual(nns.top, "level")
        t.assertEqual(nns.bat.baz, "baz")
        t.assertEqual(nns.bat.sub.var, "sub_var")


class CommandsTests(TestCase):

    @patch(f"{SRC}.set_default_logging", autospec=True)
    def test_setup_logging(t, set_default_logging: Mock):
        with t.subTest("default to ERROR"):
            args = Namespace(loglevel=logging.INFO)
            Commands.setup_logging(args)
            set_default_logging.assert_called_with(logging.INFO)

        with t.subTest("set given value"):
            args = Namespace(loglevel=logging.INFO)
            Commands.setup_logging(args)
            set_default_logging.assert_called_with(logging.INFO)
