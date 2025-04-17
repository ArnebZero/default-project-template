# Project Template

# CLI Tool for Project Commands

A command-line interface (CLI) tool for running various project commands.

## Overview

This CLI tool provides a simple and consistent way to execute different commands related to the project. It is built with a modular architecture that allows easy addition of new commands.

## Installation

This project requires Python 3.10 or higher. To install the project, clone the repository and install the required dependencies.

```bash
# Clone the repository
git clone <repository_url>
# rename project folder
mv <repository_name> <your_project_name>
cd <your_project_name>

# Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
python -m src.main <command> [options]
```

### Available Commands

- `example`: An example command demonstrating the command structure. You can run this command to see how the CLI works.

### Example Command

The example command demonstrates how to create and execute commands with the CLI.

```bash
# Run the example command without flags
python -m src.main example

# Run the example command with the example flag
python -m src.main example --example
```

## Adding New Commands

To add a new command:

1. Create a new Python file in the `src/commands` directory
2. Define a command class that inherits from `BaseCommand`
3. Implement the required methods: `setup_parser`, `run`, and `help` (optional)
4. Define a unique `command_name` class attribute

Example command structure:

```python
from argparse import ArgumentParser, Namespace
from ._base import BaseCommand, BaseArgs

class Args(BaseArgs):
    # Define your command-specific arguments here
    example: bool = False

class Command(BaseCommand):
    command_name = "your_command_name"

    @staticmethod
    def setup_parser(parser: ArgumentParser) -> None:
        # Add command-specific arguments
        parser.add_argument(
            "--example",
            action="store_true",
            help="Your argument description"
        )

    def run(self, args: Namespace) -> None:
        # Implement the command's functionality
        parsed_args = Args(**vars(args))
        # Your command logic here

    @classmethod
    def help(cls):
        return "Description of what your command does"
```

To run the new command, use the following command:

```bash
python -m src.main your_command_name
```

## Logging

Now we use global logging configuration. You can change this behavior by modifying the `src/utils/logging_utils.py` file.

## Useful functions

### File Utilities

The project includes file utility functions to simplify file operations:

#### Remove Files or Folders

```python
# you can also use relative imports
from src.utils.file_utils import remove_file_or_folder

# Remove a file
remove_file_or_folder("path/to/file.txt")

# Remove a directory and all its contents
remove_file_or_folder("path/to/directory")
```

This function handles both files and directories, automatically using the appropriate removal method based on the path type.

### Import Utilities

The project includes a utility `import_module` (`src/utils/imports.py`) for dynamically importing classes from modules:

#### Basic Import
```python
# Import all classes named 'Command' from modules in 'src.commands' 
commands = import_module(
    base="src.commands",  # Base package path as dot-separated string
    cls_name="Command"    # Name of the class to import
)
```

#### Attribute Filtering
```python
# Filter classes by attribute existence
commands = import_module(
    base="src.commands",
    cls_name="Command",
    attribute_name="command_name"  # Only import classes with this attribute
)

# Filter classes by attribute value
commands = import_module(
    base="src.commands",
    cls_name="Command",
    attribute_name="command_type",
    attribute_value="processing",
    check_attribute_value=True  # Verify attribute has specific value
)
```

#### Relative Imports
```python
# Using relative imports (requires file_path)
commands = import_module(
    base=".commands",     # Relative import path (starts with dot)
    cls_name="Command",
    file_path=__file__,   # Current file path for resolving relative imports
    package=__package__   # Current package name
)
```

#### Type Validation
```python
# Ensure imported classes inherit from a specific base class
from src.commands._base import BaseCommand
validated_commands = import_module(
    base="src.commands",
    cls_name="Command",
    base_cls=BaseCommand  # Classes must inherit from this base class
)
```

#### Custom Name Filtering
```python
# Define custom module name filtering
def custom_filter(name: str) -> bool:
    return not name.startswith("_") and not name.endswith("_test")

commands = import_module(
    base="src.commands",
    cls_name="Command",
    name_filter=custom_filter  # Custom function to filter module names
)
```

#### Safe Mode
```python
# Control safety checks
commands = import_module(
    base="src.commands",
    cls_name="Command",
    safe=True  # Uses AST to verify class/attribute exists before importing
)
```

This utility automatically discovers and imports classes from modules, making it easy to extend functionality without modifying core code.

## Development

The project follows a modular architecture:

- `src/main.py`: Entry point for the CLI
- `src/commands/`: Directory containing all available commands
- `src/commands/_base.py`: Base classes for commands
- `src/utils/`: Utility functions including logging setup

## License

MIT License