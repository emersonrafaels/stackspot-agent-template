from pathlib import Path
from loguru import logger
import sys


def setup_logger():
    """
    Configure Loguru logger with custom settings.

    Features:
    - Log rotation (daily)
    - Log retention (30 days)
    - Separate log levels in different files
    - Console output with colors
    - Structured format with timestamp
    """
    # Create logs directory if it doesn't exist
    log_path = Path(__file__).parent / "logs"
    log_path.mkdir(exist_ok=True)

    # Remove default logger
    logger.remove()

    # Add console logger with colors
    logger.add(
        sys.stdout,
        colorize=True,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>",
        level="INFO",
    )

    # Add file logger for all levels (DEBUG and above)
    logger.add(
        log_path / "debug_{time:YYYY-MM-DD}.log",
        rotation="00:00",  # Create new file at midnight
        retention="30 days",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}",
        level="DEBUG",
        encoding="utf-8",
    )

    # Add file logger for errors only
    logger.add(
        log_path / "error_{time:YYYY-MM-DD}.log",
        rotation="00:00",
        retention="30 days",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}",
        level="ERROR",
        encoding="utf-8",
        backtrace=True,  # Include traceback for errors
        diagnose=True,  # Include variables in traceback
    )

    return logger


# Initialize logger
logger = setup_logger()
