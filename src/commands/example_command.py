import logging
from argparse import ArgumentParser, Namespace

from ._base import BaseCommand, BaseArgs

logger = logging.getLogger(__name__)


class Args(BaseArgs):
    example: bool = False


class Command(BaseCommand):
    command_name = "example"

    @staticmethod
    def setup_parser(parser: ArgumentParser) -> None:
        parser.add_argument(
            "--example",
            action="store_true",
            help="An example argument for the example command.",
        )

    def run(self, args: Namespace) -> None:
        parsed_args = Args(**vars(args))
        if parsed_args.example:
            logger.info("Example command executed with the --example flag.")
        else:
            logger.info("Example command executed without the --example flag.")

    @classmethod
    def help(cls):
        return (
            "This is an example command. "
            "It demonstrates how to create a command with arguments. "
            "Use --example to see the example argument in action."
        )
