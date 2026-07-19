"""Tests for application logging configuration."""

import logging
from collections.abc import Iterator

import pytest
from _pytest.capture import CaptureFixture

from risk_engine.logging_config import configure_logging


@pytest.fixture(autouse=True)
def restore_root_logger() -> Iterator[None]:
    """Restore root logger state after each logging test."""
    root_logger = logging.getLogger()
    original_handlers = list(root_logger.handlers)
    original_level = root_logger.level

    yield

    for handler in root_logger.handlers:
        if handler not in original_handlers:
            handler.close()

    root_logger.handlers[:] = original_handlers
    root_logger.setLevel(original_level)


def test_info_logging_is_emitted(
    capsys: CaptureFixture[str],
) -> None:
    configure_logging("INFO")

    logger = logging.getLogger("risk_engine.test")
    logger.info("configuration loaded")

    captured = capsys.readouterr()

    assert logging.getLogger().level == logging.INFO
    assert "INFO" in captured.err
    assert "risk_engine.test" in captured.err
    assert "configuration loaded" in captured.err


def test_warning_suppresses_info(
    capsys: CaptureFixture[str],
) -> None:
    configure_logging("WARNING")

    logger = logging.getLogger("risk_engine.test")
    logger.info("hidden message")

    captured = capsys.readouterr()

    assert logging.getLogger().level == logging.WARNING
    assert "hidden message" not in captured.err


def test_invalid_logging_level() -> None:
    with pytest.raises(
        ValueError,
        match="unsupported logging level: VERBOSE",
    ):
        configure_logging("VERBOSE")
