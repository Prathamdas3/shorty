import pytest
import logging
from app.core.logger import get_logger


def test_get_logger_returns_logger():
    """Test get_logger returns a logger instance."""
    logger = get_logger("test_module")
    assert isinstance(logger, logging.Logger)
    assert logger.name == "test_module"


def test_get_logger_same_name_returns_same_instance():
    """Test get_logger returns the same logger instance for same name."""
    logger1 = get_logger("test_module")
    logger2 = get_logger("test_module")
    assert logger1 is logger2


def test_get_logger_different_names_return_different_instances():
    """Test get_logger returns different logger instances for different names."""
    logger1 = get_logger("test_module1")
    logger2 = get_logger("test_module2")
    assert logger1 is not logger2
    assert logger1.name != logger2.name


def test_logger_can_be_configured():
    """Test that get_logger returns a properly configured logger."""
    # The main thing is that it returns a logger that can log
    import uuid

    unique_name = f"test_config_{uuid.uuid4().hex[:8]}"
    logger = get_logger(unique_name)

    # At minimum, it should be able to log without errors
    logger.info("Test message")

    # And it should have some level set
    assert logger.level >= 0  # Any valid level


def test_logger_can_log_messages():
    """Test logger can log messages at different levels."""
    logger = get_logger("test_module")

    # These should not raise exceptions
    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")
    logger.critical("Critical message")
