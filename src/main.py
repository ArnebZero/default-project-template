import argparse
from typing import List, Type

from .commands._base import BaseCommand
from .utils.imports import import_module
from .utils.logging_utils import setup_logging


def main():
    parser = argparse.ArgumentParser(description="CLI for the project commands.")
    subparsers = parser.add_subparsers(dest="command", required=True, help="Sub-command to run")

    modules: List[Type[BaseCommand]] = import_module(
        base=".commands",
        cls_name="Command",
        attribute_name="command_name",
        file_path=__file__,
        package=__package__,
        base_cls=BaseCommand,
    )
    if not modules:
        parser.error("No command modules found.")

    commands = {}
    for command_cls in modules:
        cmd_name = getattr(command_cls, "command_name", None)
        if not cmd_name:
            parser.error(
                f"The Command class in '{command_cls.__module__}' must define a "
                "non-empty 'command_name' attribute"
            )
        if cmd_name in commands:
            parser.error(f"Duplicate command name found: {cmd_name}")
        commands[cmd_name] = command_cls
        command_parser = subparsers.add_parser(cmd_name, help=command_cls.help())
        command_cls.setup_parser(command_parser)

    args = parser.parse_args()
    setup_logging()

    command_cls = commands.get(args.command)
    command_instance: BaseCommand = command_cls()
    command_instance.run(args)


if __name__ == "__main__":
    main()
