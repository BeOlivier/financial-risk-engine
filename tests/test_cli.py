"""Tests for the command-line interface."""

from pathlib import Path

from _pytest.capture import CaptureFixture

from risk_engine import __version__
from risk_engine.cli import build_parser, main


def write_config(tmp_path: Path, content: str) -> Path:
    """Write and return a temporary CLI configuration file."""
    config_path = tmp_path / "config.toml"
    config_path.write_text(content, encoding="utf-8")
    return config_path


def test_version_returns_success(
    capsys: CaptureFixture[str],
) -> None:
    exit_code = main(["version"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert captured.out == f"risk-engine {__version__}\n"
    assert captured.err == ""


def test_help_can_be_generated() -> None:
    help_text = build_parser().format_help()

    assert "Portfolio analytics" in help_text
    assert "version" in help_text
    assert "config-check" in help_text


def test_config_check_valid_config(
    tmp_path: Path,
    capsys: CaptureFixture[str],
) -> None:
    config_path = write_config(
        tmp_path,
        """
[project]
name = "CLI Test"

[logging]
level = "WARNING"

[output]
directory = "reports"
""".strip(),
    )

    exit_code = main(
        [
            "config-check",
            "--config",
            str(config_path),
        ]
    )
    captured = capsys.readouterr()

    assert exit_code == 0
    assert f"Configuration is valid: {config_path}" in captured.out
    assert "Project: CLI Test" in captured.out
    assert "Logging level: WARNING" in captured.out
    assert "Output directory: reports" in captured.out
    assert captured.err == ""


def test_config_check_missing_file(
    tmp_path: Path,
    capsys: CaptureFixture[str],
) -> None:
    missing_path = tmp_path / "missing.toml"

    exit_code = main(
        [
            "config-check",
            "--config",
            str(missing_path),
        ]
    )
    captured = capsys.readouterr()

    assert exit_code == 1
    assert captured.out == ""
    assert "configuration file not found" in captured.err
    assert str(missing_path) in captured.err
