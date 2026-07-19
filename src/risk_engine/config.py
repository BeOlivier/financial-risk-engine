"""Runtime configuration loading and basic validation."""

import tomllib
from pathlib import Path


def validate_toml_file(path: Path) -> None:
    """Validate that a path refers to a readable, syntactically valid TOML file.

    Args:
        path: Path to the TOML configuration file.

    Raises:
        FileNotFoundError: If the path does not exist.
        IsADirectoryError: If the path does not refer to a regular file.
        tomllib.TOMLDecodeError: If the file contains invalid TOML.
    """
    if not path.exists():
        raise FileNotFoundError(path)

    if not path.is_file():
        raise IsADirectoryError(path)

    with path.open("rb") as config_file:
        tomllib.load(config_file)
