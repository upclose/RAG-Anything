"""
Logging configuration for RAG-Anything

Provides centralized logging setup with environment variable support
"""

import logging
import sys
from typing import Optional
from lightrag.utils import get_env_value


def setup_logger(
    name: str = "raganything",
    level: Optional[str] = None,
    format_string: Optional[str] = None,
) -> logging.Logger:
    """
    Setup and configure logger for RAG-Anything.
    
    Args:
        name: Logger name
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format_string: Custom format string for log messages
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Get log level from environment if not provided
    if level is None:
        level = get_env_value("RAGANYTHING_LOG_LEVEL", "INFO", str)
    
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    
    # Avoid adding multiple handlers
    if logger.handlers:
        return logger
    
    # Default format
    if format_string is None:
        format_string = get_env_value(
            "RAGANYTHING_LOG_FORMAT",
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            str
        )
    
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logger.level)
    
    formatter = logging.Formatter(format_string)
    handler.setFormatter(formatter)
    
    logger.addHandler(handler)
    
    return logger


def get_logger(name: str = "raganything") -> logging.Logger:
    """
    Get or create a logger instance.
    
    Args:
        name: Logger name
        
    Returns:
        Logger instance
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        return setup_logger(name)
    return logger


# Default logger instance
default_logger = get_logger()
