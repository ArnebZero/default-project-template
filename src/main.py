import argparse
import importlib
from pathlib import Path

from .commands._base import BaseCommand
from .utils.logging_utils import setup_logging

def main():
    parser = argparse.ArgumentParser(description="CLI for the project commands.")
    subparsers = parser.add_subparsers(dest="command", required=True, help="Sub-command to run")

    commands = {}

    commands_path = Path(__file__).parent / "commands"

    for file in commands_path.glob("*.py"):
        if file.name.startswith("_"):
            continue

        try:
            module = importlib.import_module(f".commands.{file.stem}", __package__)
        except ImportError as err:
            parser.error(f"Failed to import command module '{file.stem}': {err}")

        command_cls: BaseCommand | None = getattr(module, "Command", None)
        if command_cls is None:
            parser.error(f"Module '{file.stem}' does not define a 'Command' class")
        if not issubclass(command_cls, BaseCommand):
            parser.error(f"The Command class in '{file.stem}' must inherit from BaseCommand")

        cmd_name = getattr(command_cls, "command_name", None)
        if not cmd_name:
            parser.error(
                f"The Command class in '{file.stem}' must define a "
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
