from typing import Optional, Sequence

import logging
from argparse import ArgumentParser, Namespace
from sys import exit

from .logconf import set_default_logging

from .lib import hello_world, check_assignment
from .conf import conf_cli, get_config, CONFIG_FILE_NAME


log = logging.getLogger("root")


def BATCLI(ARGS: Optional[Sequence[str]] = None):
    p = argparser()
    # Execute
    # get only the first command in args
    args: Namespace = p.parse_args(ARGS)
    Commands.setup_logging(args)
    log.debug(f"BATCLI: {args=}")
    try:
        log.debug(f"BATCLI: exec {args.func=}")
        args.func(args)
    except Exception as err:
        log.exception(err)
        p.print_help()
        exit(1)
    exit(0)


def argparser() -> ArgumentParser:
    p = ArgumentParser(
        description="Utility for executing various bat tasks",
        usage="bat [<args>] <command>",
    )
    p.set_defaults(func=get_help(p))

    p.add_argument(
        "-v",
        "--verbose",
        help="enable INFO output",
        action="store_const",
        dest="loglevel",
        const=logging.INFO,
    )
    p.add_argument(
        "--debug",
        help="enable DEBUG output",
        action="store_const",
        dest="loglevel",
        const=logging.DEBUG,
    )
    p.add_argument(
        "-c",
        "--conf",
        "--config_file",
        dest="config_file",
        default=CONFIG_FILE_NAME,
        help="specify a config file to get environment details from."
        f" default is {CONFIG_FILE_NAME}",
    )
    p.add_argument(
        "-e",
        "--env",
        "--config_environment",
        dest="config_env",
        default=None,
        help="specify the remote environment to use from the config file",
    )

    # Add a subparser to handle sub-commands
    commands = p.add_subparsers(
        dest="command",
        title="commands",
        description="for additonal details on each command use: "
        '"bat {command name} --help"',
    )
    # hello args
    hello = commands.add_parser(
        "hello",
        description="execute command hello",
        help="for details use hello --help",
    )
    hello.set_defaults(func=Commands.hello)

    # Add a subparser from a module
    commands.add_parser(
        "conf",
        help="configuration management cli",
        add_help=False,
        parents=[conf_cli()],
    )

    # add command
    check_assignment = commands.add_parser(
        "check_assignment",
        description="executes command check_assignment",
        help="for details use check_assignment --help",
    )
    check_assignment.set_defaults(func=Commands.check_assignment)
    check_assignment.add_argument(
        "-t",
        "--token",
        dest="token",
        help="api auth bearer token",
    )
    check_assignment.add_argument(
        "-c",
        "--courseid",
        dest="courseid",
        help="canvas course id",
    )
    check_assignment.add_argument(
        "-a",
        "--assignmentid",
        dest="assignmentid",
        help="canvas assignment id",
    )

    return p


def get_help(parser):
    def help(_: Namespace):
        parser.print_help()

    return help


class Commands:

    @staticmethod
    def hello(_: Namespace):
        print(hello_world())

    @staticmethod
    def setup_logging(args: Namespace):
        if args.loglevel:
            set_default_logging(log_level=args.loglevel)
        else:
            set_default_logging(log_level="ERROR")

    @staticmethod
    def raise_exception(_: Namespace):
        raise RuntimeError("boom!")

    @staticmethod
    def check_assignment(args: Namespace):
        cfg = get_config(cli_args=args, config_file_name=args.config_file, config_env=args.config_env)
        ret = check_assignment(token=cfg.token, courseid=cfg.courseid, assignmentid=cfg.assignmentid)
        print(ret)