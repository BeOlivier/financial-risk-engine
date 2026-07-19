"""Application logging configuration."""

import logging

LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def configure_logging(level: str) -> None:
    """Configure console logging for the command-line application.

    Args:
        level: Standard Python logging level name.

    Raises:
        ValueError: If the logging level is unsupported.
    """
    normalized_level = level.upper()
    numeric_level = getattr(logging, normalized_level, None)

    if not isinstance(numeric_level, int):
        raise ValueError(f"unsupported logging level: {level}")

    logging.basicConfig(
        level=numeric_level,
        format=LOG_FORMAT,
        datefmt=DATE_FORMAT,
        force=True,
    )
