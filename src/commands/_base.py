from abc import ABC, abstractmethod
from argparse import ArgumentParser, Namespace

from pydantic import BaseModel


class BaseArgs(BaseModel):
    """
    Base class for command-line argument parsing.
    This class can be extended to define specific arguments for each command.
    """

    command: str


class BaseCommand(ABC):
    command_name: str | None = None

    @staticmethod
    @abstractmethod
    def setup_parser(parser: ArgumentParser) -> None:
        """
        Configure the command-specific arguments on the provided parser.
        """

    @abstractmethod
    def run(self, args: Namespace) -> None:
        """
        Execute the command using the parsed arguments.
        """

    @classmethod
    def help(cls) -> str:
        """
        Return help information for this command.
        By default, returns '<command_name> command'.
        """
        return f"{cls.command_name} command"
