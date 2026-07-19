"""Command-line interface for the financial risk engine."""

import argparse
import sys
import tomllib
from collections.abc import Callable, Sequence
from pathlib import Path

from risk_engine import __version__
from risk_engine.config import validate_toml_file

CommandHandler = Callable[[argparse.Namespace], int]


def handle_version(_: argparse.Namespace) -> int:
    """Print the installed application version."""
    print(f"risk-engine {__version__}")
    return 0


def handle_config_check(args: argparse.Namespace) -> int:
    """Validate that a configuration file is readable TOML."""
    config_path: Path = args.config

    try:
        validate_toml_file(config_path)
    except FileNotFoundError:
        print(
            f"error: configuration file not found: {config_path}",
            file=sys.stderr,
        )
        return 1
    except IsADirectoryError:
        print(
            f"error: configuration path is not a file: {config_path}",
            file=sys.stderr,
        )
        return 1
    except PermissionError:
        print(
            f"error: configuration file cannot be read: {config_path}",
            file=sys.stderr,
        )
        return 1
    except tomllib.TOMLDecodeError as error:
        print(
            f"error: invalid TOML in {config_path}: {error}",
            file=sys.stderr,
        )
        return 1

    print(f"Configuration is valid TOML: {config_path}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    """Build and return the command-line argument parser."""
    parser = argparse.ArgumentParser(
        prog="risk-engine",
        description=("Portfolio analytics, simulation, and financial risk modelling."),
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
        metavar="COMMAND",
    )

    version_parser = subparsers.add_parser(
        "version",
        help="Display the installed application version.",
        description="Display the installed application version.",
    )
    version_parser.set_defaults(handler=handle_version)

    config_parser = subparsers.add_parser(
        "config-check",
        help="Check whether a configuration file contains valid TOML.",
        description=(
            "Verify that a configuration path exists, is readable, "
            "and contains syntactically valid TOML."
        ),
    )
    config_parser.add_argument(
        "-c",
        "--config",
        required=True,
        type=Path,
        metavar="PATH",
        help="Path to the TOML configuration file.",
    )
    config_parser.set_defaults(handler=handle_config_check)

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the command-line interface and return its exit status."""
    parser = build_parser()
    args = parser.parse_args(argv)

    handler: CommandHandler = args.handler
    return handler(args)
