# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022-2024)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Logging module."""

from __future__ import annotations

import logging
import sys
import os
import json
from typing import Final
import logging
from logging.config import dictConfig
from logging.handlers import TimedRotatingFileHandler
import string

DEFAULT_LOG_MESSAGE: Final = "%(asctime)s %(levelname) -7s " "%(name)s: %(message)s"

# Loggers for each name are saved here.
_loggers: dict[str, logging.Logger] = {}

# The global log level is set here across all names.
_global_log_level = logging.INFO

class CustomFormatter(logging.Formatter):

    grey = "\x1b[38;20m"
    green = "\x1b[32;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = string.Template("%(asctime)s | %(name)s | $color%(levelname)s\x1b[0m | %(filename)s:%(lineno)d | %(message)s ")

    FORMATS = {
        logging.DEBUG: format.substitute({"color":grey}),
        logging.INFO: format.substitute({"color":green}),
        logging.WARNING: format.substitute({"color":yellow}),
        logging.ERROR:format.substitute({"color":red}),
        logging.CRITICAL: format.substitute({"color":bold_red})
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)
    

def set_log_level(level: str | int) -> None:
    """Set log level."""
    logger = get_logger(__name__)

    if isinstance(level, str):
        level = level.upper()
    if level == "CRITICAL" or level == logging.CRITICAL:
        log_level = logging.CRITICAL
    elif level == "ERROR" or level == logging.ERROR:
        log_level = logging.ERROR
    elif level == "WARNING" or level == logging.WARNING:
        log_level = logging.WARNING
    elif level == "INFO" or level == logging.INFO:
        log_level = logging.INFO
    elif level == "DEBUG" or level == logging.DEBUG:
        log_level = logging.DEBUG
    else:
        msg = 'undefined log level "%s"' % level
        logger.critical(msg)
        sys.exit(1)

    for log in _loggers.values():
        log.setLevel(log_level)

    global _global_log_level
    _global_log_level = log_level


def setup_formatter(logger: logging.Logger) -> None:
    """Set up the console formatter for a given logger."""
    # Deregister any previous console loggers.
    if hasattr(logger, "streamlit_console_handler"):
        logger.removeHandler(logger.streamlit_console_handler)

    logger.streamlit_console_handler = logging.StreamHandler()  # type: ignore[attr-defined]

    logger.streamlit_console_handler.setFormatter(CustomFormatter())  # type: ignore[attr-defined]

    # Register the new console logger.
    logger.addHandler(logger.streamlit_console_handler)  # type: ignore[attr-defined]


def update_formatter() -> None:
    for log in _loggers.values():
        setup_formatter(log)


def init_tornado_logs() -> None:
    """Set Tornado log levels.

    This function does not import any Tornado code, so it's safe to call even
    when Server is not running.
    """
    # http://www.tornadoweb.org/en/stable/log.html
    for log in ("access", "application", "general"):
        # get_logger will set the log level for the logger with the given name.
        get_logger(f"tornado.{log}")


def get_logger(name: str, log_to_file:bool=False) -> logging.Logger:
    """Return a logger.

    Parameters
    ----------
    name : str
        The name of the logger to use. You should just pass in __name__.

    Returns
    -------
    Logger

    """
    if name in _loggers.keys():
        return _loggers[name]

    if name == "root":
        logger = logging.getLogger("streamlit")
    else:
        logger = logging.getLogger(name)

    logger.setLevel(_global_log_level)
    logger.propagate = False
    setup_formatter(logger)
    
    _loggers[name] = logger

    if log_to_file:
        trace_handler, error_handler = _get_file_handers(dirname=os.getenv('STREAMLIT_LOG_PATH', 'Log'))
        logger.addHandler(trace_handler)
        logger.addHandler(error_handler)
    return logger


def _get_file_handers(dirname:os.PathLike='Log'):
    if not os.path.isdir(dirname):
        os.makedirs(dirname)

    formatter = logging.Formatter("%(asctime)s | %(name)s | %(levelname)s | %(filename)s:%(lineno)d | %(message)s ")

    # Create file handler for trace.log
    file_handler = TimedRotatingFileHandler(f'{dirname}/trace.log', when='midnight', interval=1, backupCount=30, encoding='utf8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Create file handler for error.log
    file_error_handler = TimedRotatingFileHandler(f'{dirname}/error.log', when='midnight', interval=1, backupCount=30, encoding='utf8')
    file_error_handler.setLevel(logging.ERROR)
    file_error_handler.setFormatter(formatter)

    return file_handler, file_error_handler
