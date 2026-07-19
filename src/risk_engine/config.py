"""Runtime configuration loading and validation."""

import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from risk_engine.exceptions import (
    ConfigurationFileError,
    ConfigurationSyntaxError,
    ConfigurationValidationError,
)

SUPPORTED_LOG_LEVELS = frozenset(
    {
        "DEBUG",
        "INFO",
        "WARNING",
        "ERROR",
        "CRITICAL",
    }
)


@dataclass(frozen=True, slots=True)
class ProjectConfig:
    """Identity settings for an analysis run."""

    name: str


@dataclass(frozen=True, slots=True)
class LoggingConfig:
    """Logging settings for an analysis run."""

    level: str = "INFO"


@dataclass(frozen=True, slots=True)
class OutputConfig:
    """Output settings for generated results."""

    directory: Path = Path("outputs")


@dataclass(frozen=True, slots=True)
class AppConfig:
    """Complete validated runtime configuration."""

    project: ProjectConfig
    logging: LoggingConfig
    output: OutputConfig


def _require_table(
    raw_config: dict[str, Any],
    table_name: str,
) -> dict[str, Any]:
    """Return a required TOML table or raise a validation error."""
    value = raw_config.get(table_name)

    if value is None:
        raise ConfigurationValidationError(f"missing required [{table_name}] table")

    if not isinstance(value, dict):
        raise ConfigurationValidationError(f"[{table_name}] must be a TOML table")

    return value


def _optional_table(
    raw_config: dict[str, Any],
    table_name: str,
) -> dict[str, Any]:
    """Return an optional TOML table, or an empty table when omitted."""
    value = raw_config.get(table_name)

    if value is None:
        return {}

    if not isinstance(value, dict):
        raise ConfigurationValidationError(f"[{table_name}] must be a TOML table")

    return value


def _require_non_empty_string(
    table: dict[str, Any],
    field_name: str,
    qualified_name: str,
) -> str:
    """Return a required non-empty string field."""
    value = table.get(field_name)

    if value is None:
        raise ConfigurationValidationError(f"missing required setting: {qualified_name}")

    if not isinstance(value, str):
        raise ConfigurationValidationError(f"{qualified_name} must be a string")

    normalized_value = value.strip()

    if not normalized_value:
        raise ConfigurationValidationError(f"{qualified_name} must not be empty")

    return normalized_value


def _optional_non_empty_string(
    table: dict[str, Any],
    field_name: str,
    qualified_name: str,
    default: str,
) -> str:
    """Return an optional non-empty string field."""
    value = table.get(field_name, default)

    if not isinstance(value, str):
        raise ConfigurationValidationError(f"{qualified_name} must be a string")

    normalized_value = value.strip()

    if not normalized_value:
        raise ConfigurationValidationError(f"{qualified_name} must not be empty")

    return normalized_value


def load_config(path: Path) -> AppConfig:
    """Load and validate runtime configuration from a TOML file.

    Args:
        path: Path to the runtime configuration file.

    Returns:
        A fully validated application configuration.

    Raises:
        ConfigurationFileError: If the file cannot be accessed.
        ConfigurationSyntaxError: If the file contains invalid TOML.
        ConfigurationValidationError: If required settings are invalid.
    """
    if not path.exists():
        raise ConfigurationFileError(f"configuration file not found: {path}")

    if not path.is_file():
        raise ConfigurationFileError(f"configuration path is not a file: {path}")

    try:
        with path.open("rb") as config_file:
            raw_config = tomllib.load(config_file)
    except PermissionError as error:
        raise ConfigurationFileError(f"configuration file cannot be read: {path}") from error
    except OSError as error:
        raise ConfigurationFileError(
            f"failed to read configuration file {path}: {error}"
        ) from error
    except tomllib.TOMLDecodeError as error:
        raise ConfigurationSyntaxError(f"invalid TOML in {path}: {error}") from error

    project_table = _require_table(raw_config, "project")
    logging_table = _optional_table(raw_config, "logging")
    output_table = _optional_table(raw_config, "output")

    project_name = _require_non_empty_string(
        project_table,
        "name",
        "project.name",
    )

    logging_level = _optional_non_empty_string(
        logging_table,
        "level",
        "logging.level",
        "INFO",
    ).upper()

    if logging_level not in SUPPORTED_LOG_LEVELS:
        supported_levels = ", ".join(sorted(SUPPORTED_LOG_LEVELS))
        raise ConfigurationValidationError(
            f"logging.level must be one of {supported_levels}; received {logging_level!r}"
        )

    output_directory = _optional_non_empty_string(
        output_table,
        "directory",
        "output.directory",
        "outputs",
    )

    return AppConfig(
        project=ProjectConfig(name=project_name),
        logging=LoggingConfig(level=logging_level),
        output=OutputConfig(directory=Path(output_directory)),
    )
