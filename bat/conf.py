from typing import Optional

from dataclasses import dataclass
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from textwrap import dedent
from logging import getLogger
from pathlib import Path

from batconf.manager import Configuration, ConfigProtocol
from batconf.source import SourceList
from batconf.sources.args import CliArgsConfig, Namespace
from batconf.sources.env import EnvConfig
from batconf.sources.ini import IniConfig
from batconf.sources.dataclass import DataclassConfig

CONFIG_FILE_NAME = str(Path.cwd() / "config.ini")

@dataclass
class ConfigSchema:
    token: str

def get_config(
    config_class: ConfigProtocol = ConfigSchema,
    cfg_path: str = 'batcanvas',
    cli_args: Namespace = None,
    config_file: IniConfig = None,
    config_file_name: str = CONFIG_FILE_NAME,
    config_env: str = None,
) -> Configuration:
    # Build a prioritized config source list
    config_sources = [
        CliArgsConfig(cli_args) if cli_args else None,
        EnvConfig(),
        (
            config_file
            if config_file
            else IniConfig(config_file_name, config_env=config_env)
        ),
        DataclassConfig(config_class),
    ]

    source_list = SourceList(config_sources)

    return Configuration(source_list, config_class, path=cfg_path)


log = getLogger(__name__)


def conf_cli() -> ArgumentParser:
    conf = ArgumentParser(
        prog="conf",
        formatter_class=RawDescriptionHelpFormatter,
        description=dedent(
            """\
                tools for working with batconf configuration manager
            """
        ),
    )
    # Default behavior if no sub-command is given
    # example.set_defaults(func=get_help(example))
    conf.set_defaults(func=_Commands.print_config)

    return conf


class _Commands:
    @staticmethod
    def print_config(args: Namespace):
        print(
            global_config(
                cli_args=args,
                config_file_name=args.config_file,
                config_env=args.config_env,
            )
        )


def global_config(
    cli_args: Optional[Namespace],
    config_file_name: Optional[str],
    config_env: Optional[str],
) -> str:
    """Return a string representing the current configuration"""
    cfg = get_config(
        cli_args=cli_args,
        config_file_name=config_file_name,
        config_env=config_env,
    )
    return str(cfg)
