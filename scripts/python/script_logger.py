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


class _LevelColorFormatter(logging.Formatter):
    """Formatter that adds ANSI color codes to the level name only.

    Attributes:
        color_map (dict[int, str]): Mapping of log levels to ANSI color codes.
        reset_code (str): ANSI code to reset color after the level name.
    """

    def __init__(
        self,
        fmt: str,
        datefmt: str,
        *,
        color_map: dict[int, str],
        reset_code: str = "\033[0m",
    ) -> None:

        super().__init__(fmt, datefmt)
        self._color_map = color_map
        self._reset_code = reset_code

    def format(self, record: logging.LogRecord) -> str:
        """Override to inject color codes into the level name.

        Parameters:
            record (logging.LogRecord): The log record to format.
        Returns:
            str: The formatted log message with color codes applied to the level name.
        """

        original_levelname = record.levelname
        color = self._color_map.get(record.levelno)

        if color:
            record.levelname = f"{color}{original_levelname}{self._reset_code}"

        try:
            return super().format(record)
        finally:
            record.levelname = original_levelname


class ScriptLogger:
    """Helper class to create and manage loggers for scripts with consistent formatting.

    Attributes:
        msg_format (str): Log message format string.
        date_format (str): Log date format string.
        level_colors (dict[int, str]): Mapping of log levels to ANSI color codes for console output.
        reset_code (str): ANSI code to reset color after the level name.
    """

    msg_format = "%(asctime)s [%(levelname)s] %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"
    level_colors: dict[int, str] = {
        logging.DEBUG: "\033[36m",  # cyan
        logging.INFO: "\033[32m",  # green
        logging.WARNING: "\033[33m",  # yellow
        logging.ERROR: "\033[31m",  # red
        logging.CRITICAL: "\033[35m",  # magenta
    }
    reset_code = "\033[0m"

    def __init__(
        self,
        name: str,
        *,
        level: int = logging.INFO,
        log_to_console: bool = True,
        log_to_file: Optional[Path | str] = None,
        propagate: bool = False,
        formatter: Optional[logging.Formatter] = None,
        colorize: bool = False,
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
            colorize (bool): If True, colorizes the log level in console output.

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
        self._colorize = colorize
        self._configure(log_to_console=log_to_console, log_to_file=log_to_file)

    def _configure(
        self,
        *,
        log_to_console: bool,
        log_to_file: Optional[Path | str],
    ) -> None:
        """Configure the logger with console and/or file handlers.

        Parameters:
            log_to_console (bool): Whether to add a console handler.
            log_to_file (Path | str | None): Optional file path to add a file handler.

        Returns:
            None
        """

        if self._logger.handlers:
            return  # Avoid adding duplicate handlers on multiple instantiations.

        self._logger.setLevel(self._level)
        self._logger.propagate = self._propagate

        if log_to_console:
            if self._colorize:
                console_formatter = _LevelColorFormatter(
                    self.msg_format,
                    self.date_format,
                    color_map=self.level_colors,
                    reset_code=self.reset_code,
                )
            else:
                console_formatter = self._formatter

            stream_handler = logging.StreamHandler(sys.stdout)
            stream_handler.setFormatter(console_formatter)
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
        colorize: bool = False,
    ) -> "ScriptLogger":
        """Create a console-only logger.

        Parameters:
            name (str): Logger name.
            level (int): Logging level (default: INFO).
            propagate (bool): Whether to propagate to ancestor loggers.
            colorize (bool): If True, colorizes the log level in console output.

        Returns:
            ScriptLogger: Configured logger instance.
        """

        return cls(
            name,
            level=level,
            log_to_console=True,
            log_to_file=None,
            propagate=propagate,
            colorize=colorize,
        )

    @classmethod
    def log_to_console_and_file(
        cls,
        name: str,
        log_file: Path | str,
        *,
        level: int = logging.INFO,
        propagate: bool = False,
        colorize: bool = False,
    ) -> "ScriptLogger":
        """Create a logger that logs to both console and a file.

        Parameters:
            name (str): Logger name.
            log_file (Path | str): File path to log to.
            level (int): Logging level (default: INFO).
            propagate (bool): Whether to propagate to ancestor loggers.
            colorize (bool): If True, colorizes the log level in console output.

        Returns:
            ScriptLogger: Configured logger instance.
        """

        return cls(
            name,
            level=level,
            log_to_console=True,
            log_to_file=log_file,
            propagate=propagate,
            colorize=colorize,
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
