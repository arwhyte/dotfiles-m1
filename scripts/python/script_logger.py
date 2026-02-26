#!/usr/bin/env python3
"""
Script logging helper. Wraps `logging.Logger` with a simple interface to create loggers that
log to console and/or file, with consistent formatting and no duplicate handlers.:

Features:
1. Configures console-only or console+file logging
2. Avoids duplicate handlers
3. Exposes logging methods directly (info, debug, etc.)
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import Optional


class ScriptLogger:
    msg_format = "%(asctime)s [%(levelname)s] %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    def __init__(
        self,
        name: str,
        *,
        level: int = logging.INFO,
        log_to_console: bool = True,
        log_to_file: Optional[Path | str] = None,
        propagate: bool = False,
        formatter: Optional[logging.Formatter] = None,
    ) -> None:

        """
        Create (or retrieve) a logger by name and configure it once.

        Parameters:
            name (str): Logger name (module name, script name, etc.).
            level (int): Logging level (default: INFO).
            log_to_console (bool): Whether to log to stdout.
            log_to_file (Path | str): Optional file path to also log to.
            propagate (bool): Whether to propagate to ancestor loggers.
            formatter (logging.Formatter): Optional custom formatter; if omitted, uses defaults.

        Returns:
            None
        """

        self._logger = logging.getLogger(name)
        self._level = level
        self._propagate = propagate
        self._formatter = formatter or logging.Formatter(
            self.msg_format,
            self.date_format,
        )
        self._configure(log_to_console=log_to_console, log_to_file=log_to_file)

    def _configure(
        self,
        *,
        log_to_console: bool,
        log_to_file: Optional[Path | str],
    ) -> None:

        if self._logger.handlers:
            return  # Avoid adding duplicate handlers on multiple instantiations.

        self._logger.setLevel(self._level)
        self._logger.propagate = self._propagate

        if log_to_console:
            stream_handler = logging.StreamHandler(sys.stdout)
            stream_handler.setFormatter(self._formatter)
            self._logger.addHandler(stream_handler)

        if log_to_file is not None:
            log_path = Path(log_to_file)
            file_handler = logging.FileHandler(log_path, encoding="utf-8")
            file_handler.setFormatter(self._formatter)
            self._logger.addHandler(file_handler)

    @classmethod
    def log_to_console(
        cls,
        name: str,
        *,
        level: int = logging.INFO,
        propagate: bool = False,
    ) -> "ScriptLogger":
        """Create a console-only logger.

        Parameters:
            name (str): Logger name.
            level (int): Logging level (default: INFO).
            propagate (bool): Whether to propagate to ancestor loggers.

        Returns:
            ScriptLogger: Configured logger instance.
        """
        return cls(
            name,
            level=level,
            log_to_console=True,
            log_to_file=None,
            propagate=propagate,
        )

    @classmethod
    def log_to_console_and_file(
        cls,
        name: str,
        log_file: Path | str,
        *,
        level: int = logging.INFO,
        propagate: bool = False,
    ) -> "ScriptLogger":
        """Create a logger that logs to both console and a file.

        Parameters:
            name (str): Logger name.
            log_file (Path | str): File path to log to.
            level (int): Logging level (default: INFO).
            propagate (bool): Whether to propagate to ancestor loggers.

        Returns:
            ScriptLogger: Configured logger instance.
        """
        return cls(
            name,
            level=level,
            log_to_console=True,
            log_to_file=log_file,
            propagate=propagate,
        )

    @property
    def logger(self) -> logging.Logger:
        """Access the underlying `logging.Logger`.

        Parameters:
            None

        Returns:
            logging.Logger: The configured logger instance.
        """

        return self._logger

    # delegate common logging methods
    def debug(self, msg: str, *args, **kwargs) -> None:
        """Log a debug message.

        Parameters:
            msg (str): The message format string.
            *args: Arguments for the message format string.
            **kwargs: Additional keyword arguments for the logger.

        Returns:
            None
        """

        self._logger.debug(msg, *args, **kwargs)

    def info(self, msg: str, *args, **kwargs) -> None:
        """Log an info message.

        Parameters:
            msg (str): The message format string.
            *args: Arguments for the message format string.
            **kwargs: Additional keyword arguments for the logger.

        Returns:
            None
        """

        self._logger.info(msg, *args, **kwargs)

    def warning(self, msg: str, *args, **kwargs) -> None:
        """Log a warning message.

        Parameters:
            msg (str): The message format string.
            *args: Arguments for the message format string.
            **kwargs: Additional keyword arguments for the logger.

        Returns:
            None
        """

        self._logger.warning(msg, *args, **kwargs)

    def critical(self, msg: str, *args, **kwargs) -> None:
        """Log a critical message.

        Parameters:
            msg (str): The message format string.
            *args: Arguments for the message format string.
            **kwargs: Additional keyword arguments for the logger.

        Returns:
            None
        """

        self._logger.critical(msg, *args, **kwargs)

    def error(self, msg: str, *args, **kwargs) -> None:
        """Log an error message.

        Parameters:
            msg (str): The message format string.
            *args: Arguments for the message format string.
            **kwargs: Additional keyword arguments for the logger.

        Returns:
            None
        """

        self._logger.error(msg, *args, **kwargs)

    def exception(self, msg: str, *args, **kwargs) -> None:
        """Shortcut for logging an exception with stack trace.

        Parameters:
            msg (str): The message format string.
            *args: Arguments for the message format string.
            **kwargs: Additional keyword arguments for the logger.

        Returns:
            None
        """
        self._logger.exception(msg, *args, **kwargs)
