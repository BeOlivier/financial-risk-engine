"""Tests for runtime configuration loading and validation."""

from pathlib import Path

import pytest

from risk_engine.config import load_config
from risk_engine.exceptions import (
    ConfigurationFileError,
    ConfigurationSyntaxError,
    ConfigurationValidationError,
)


def write_config(tmp_path: Path, content: str) -> Path:
    """Write and return a temporary TOML configuration file."""
    config_path = tmp_path / "config.toml"
    config_path.write_text(content, encoding="utf-8")
    return config_path


def test_load_valid_config(tmp_path: Path) -> None:
    config_path = write_config(
        tmp_path,
        """
[project]
name = "Test Portfolio"

[logging]
level = "DEBUG"

[output]
directory = "reports"
""".strip(),
    )

    config = load_config(config_path)

    assert config.project.name == "Test Portfolio"
    assert config.logging.level == "DEBUG"
    assert config.output.directory == Path("reports")


def test_load_config_uses_defaults(tmp_path: Path) -> None:
    config_path = write_config(
        tmp_path,
        """
[project]
name = "Default Test"
""".strip(),
    )

    config = load_config(config_path)

    assert config.logging.level == "INFO"
    assert config.output.directory == Path("outputs")


def test_logging_level_is_normalized(tmp_path: Path) -> None:
    config_path = write_config(
        tmp_path,
        """
[project]
name = "Normalization Test"

[logging]
level = "warning"
""".strip(),
    )

    config = load_config(config_path)

    assert config.logging.level == "WARNING"


def test_missing_config_file(tmp_path: Path) -> None:
    missing_path = tmp_path / "missing.toml"

    with pytest.raises(
        ConfigurationFileError,
        match="configuration file not found",
    ):
        load_config(missing_path)


def test_directory_is_rejected(tmp_path: Path) -> None:
    with pytest.raises(
        ConfigurationFileError,
        match="configuration path is not a file",
    ):
        load_config(tmp_path)


def test_malformed_toml(tmp_path: Path) -> None:
    config_path = write_config(
        tmp_path,
        '[project\nname = "Broken"',
    )

    with pytest.raises(
        ConfigurationSyntaxError,
        match="invalid TOML",
    ):
        load_config(config_path)


def test_missing_project_table(tmp_path: Path) -> None:
    config_path = write_config(
        tmp_path,
        """
[logging]
level = "INFO"
""".strip(),
    )

    with pytest.raises(
        ConfigurationValidationError,
        match=r"missing required \[project\] table",
    ):
        load_config(config_path)


def test_missing_project_name(tmp_path: Path) -> None:
    config_path = write_config(
        tmp_path,
        """
[project]
""".strip(),
    )

    with pytest.raises(
        ConfigurationValidationError,
        match="missing required setting: project.name",
    ):
        load_config(config_path)


def test_empty_project_name(tmp_path: Path) -> None:
    config_path = write_config(
        tmp_path,
        """
[project]
name = "   "
""".strip(),
    )

    with pytest.raises(
        ConfigurationValidationError,
        match="project.name must not be empty",
    ):
        load_config(config_path)


def test_non_string_project_name(tmp_path: Path) -> None:
    config_path = write_config(
        tmp_path,
        """
[project]
name = 123
""".strip(),
    )

    with pytest.raises(
        ConfigurationValidationError,
        match="project.name must be a string",
    ):
        load_config(config_path)


def test_invalid_logging_level(tmp_path: Path) -> None:
    config_path = write_config(
        tmp_path,
        """
[project]
name = "Invalid Level"

[logging]
level = "VERBOSE"
""".strip(),
    )

    with pytest.raises(
        ConfigurationValidationError,
        match="logging.level must be one of",
    ):
        load_config(config_path)


def test_non_string_output_directory(tmp_path: Path) -> None:
    config_path = write_config(
        tmp_path,
        """
[project]
name = "Invalid Output"

[output]
directory = 123
""".strip(),
    )

    with pytest.raises(
        ConfigurationValidationError,
        match="output.directory must be a string",
    ):
        load_config(config_path)
