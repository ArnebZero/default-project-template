import logging
import sys


class CustomFormatter(logging.Formatter):
    """
    Custom logging formatter that shows the first letter of the log level,
    followed by a timestamp, the logger name, and the log message.

    Format: [<first_letter_of_level> <date time>] (<logger_name>) <message>
    Example: [I 01.01.1999 18:00] (MyApp) This is a log message.
    """

    def format(self, record: logging.LogRecord) -> str:
        # Add a new attribute to the record with just the first letter of the levelname
        record.shortlevel = record.levelname[0]
        return super().format(record)


def setup_logging(log_level: int = logging.INFO) -> None:
    """
    Set up logging configuration with both console and file handlers using a custom formatter.

    The logs will be formatted in a more readable style:
        [<first_letter_of_level> <date time>] (<logger_name>) <message>
    The date format is: '%d.%m.%Y %H:%M'

    Args:
        log_level (int): The logging level threshold (default is logging.INFO).
    """
    # Get the root logger and set its level.
    logger = logging.getLogger()
    logger.setLevel(log_level)

    # Clear existing handlers to avoid duplication.
    if logger.hasHandlers():
        logger.handlers.clear()

    # Define the custom formatter.
    formatter = CustomFormatter(
        fmt="[%(shortlevel)s %(asctime)s] (%(name)s) %(message)s", datefmt="%d.%m.%Y %H:%M"
    )

    # Create a stream handler for console output.
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
