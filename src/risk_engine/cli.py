"""Command-line interface for the financial risk engine."""

import argparse
import json
import logging
import sys
from collections.abc import Callable, Sequence
from pathlib import Path

from risk_engine import __version__
from risk_engine.config import load_config
from risk_engine.exceptions import ConfigurationError
from risk_engine.logging_config import configure_logging

logger = logging.getLogger(__name__)
CommandHandler = Callable[[argparse.Namespace], int]


def handle_version(_: argparse.Namespace) -> int:
    """Print the installed application version."""
    print(f"risk-engine {__version__}")
    return 0


def handle_config_check(args: argparse.Namespace) -> int:
    """Load, validate, and summarize a runtime configuration file."""
    config_path: Path = args.config

    try:
        config = load_config(config_path)
    except ConfigurationError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1

    configure_logging(config.logging.level)

    logger.info("Loaded runtime configuration from %s", config_path)
    logger.info("Selected project: %s", config.project.name)

    print(f"Configuration is valid: {config_path}")
    print(f"Project: {config.project.name}")
    print(f"Logging level: {config.logging.level}")
    print(f"Output directory: {config.output.directory}")
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
        help="Validate and summarize a runtime configuration file.",
        description=(
            "Load a TOML configuration file, validate its supported settings, "
            "and display a concise summary."
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
