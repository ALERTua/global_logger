#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=redefined-outer-name
"""Global Logger Tests"""

from __future__ import print_function, unicode_literals
import logging
import random
import string
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

from global_logger import Log

if TYPE_CHECKING:
    from _pytest.tmpdir import TempdirFactory  # noqa


@pytest.fixture
def _logger():
    def __logger(*args, **kwargs):
        ___logger = Log.get_logger(*args, **kwargs)
        return ___logger

    yield __logger


@pytest.fixture
def logger(_logger):
    yield _logger()


@pytest.fixture(scope="function")
def _logger_file(_logger, tmpdir_factory):
    created_loggers = []
    created_tmpdirs = []

    def __logger_file(*args, **kwargs):
        tempdir = Path(str(tmpdir_factory.mktemp("tests_logs")))  # type: Path
        created_tmpdirs.append(tempdir)
        output = _logger(*args, logs_dir=tempdir, **kwargs)
        created_loggers.append(output)
        return output

    yield __logger_file

    for created_logger in created_loggers:
        for created_logger_logger in created_logger.loggers.values():
            # noinspection PyProtectedMember
            # pylint: disable=protected-access
            created_logger_logger._clean()

    for tmpdir in created_tmpdirs:
        # pylint: disable=expression-not-assigned
        [f.unlink() for f in tmpdir.glob("*.log")]


@pytest.fixture
def logger_file(_logger_file):
    yield _logger_file()


@pytest.fixture
def logger_screen(_logger):
    yield _logger(logs_dir=None)


def test_basic(logger_file):
    """

    :type logger_file: Log
    """

    # pylint: disable=unused-argument
    def __func(arg, *args, **kwargs):
        logger_file.trace()
        logger_file.debug("func called")

    logger_file.debug("debug text абракадабра ™: level: '%s'" % logger_file.Levels.DEBUG)
    logger_file.info("info text абракадабра ™: level: '%s'" % logger_file.Levels.INFO)
    logger_file.warning("warning text абракадабра ™: level: '%s'" % logger_file.Levels.WARNING)
    logger_file.error("error text абракадабра ™: level: '%s'" % logger_file.Levels.ERROR)
    logger_file.critical("critical text абракадабра ™: level: '%s'" % logger_file.Levels.CRITICAL)
    logger_file.printer("test filehandler message абракадабра ™", color="blue", end="", clear=True)
    logger_file.green("test green абракадабра ™", end="\t\t\t\t")
    logger_file.yellow("test yellow абракадабра ™")
    logger_file.red("red text")
    __func("argument", "arg", "arg1", named_arg="test")


def test_instance_exception():
    with pytest.raises(ValueError):
        Log("something")


def test_levels(logger, logger_screen):
    log = logger_screen
    assert log.level == log.Levels.INFO, "default logging level should be %s, but not %s" % (log.Levels.INFO, log.level)

    log.level = log.Levels.WARNING
    assert log.level == log.Levels.WARNING, "failed changing logging level to %s: it is %s instead" % (
        log.Levels.WARNING,
        log.level,
    )

    assert log.verbose is not True, "logging should not be verbose, but %s" % log.Levels.WARNING

    log.verbose = True
    assert log.verbose is True, "logging should be verbose after turninig it on, but not %s" % log.level
    assert log.level == log.Levels.DEBUG, "logging should be %s after turning verbose on, but not %s" % (
        log.Levels.DEBUG,
        log.level,
    )

    log.set_global_log_level(log.Levels.DEBUG)
    assert log.level == log.Levels.DEBUG, (
        "logging should not change from %s to %s after switching to the same level" % (log.Levels.DEBUG, log.level)
    )

    log.set_global_log_level(log.Levels.INFO)
    assert log.level == log.Levels.INFO, "logging should change to %s" % log.Levels.INFO


# noinspection PyUnusedLocal
def test_handlers_quantity(_logger, logger_file):
    logger1 = _logger(name="logger1")  # noqa: F841
    logger2 = _logger(name="logger2")  # noqa: F841
    logger3 = logger_file  # noqa: F841
    for logger in Log.loggers.values():
        filehandlers = [handler for handler in logger.logger.handlers if isinstance(handler, logging.FileHandler)]
        assert len(filehandlers) == 1


# this one has to be before test_file_writing
def test_individual_logger(_logger, logger_file):
    individual_logger = _logger("test_individual_logger_individual", global_level=False, level=Log.Levels.CRITICAL)
    individual_logger._filehandler.level = constant_level = 98
    Log.set_global_log_level(Log.Levels.WARNING)
    assert logger_file.level == Log.Levels.WARNING, (
        "log level should be %s after set_global_log_level" % Log.Levels.WARNING
    )
    assert individual_logger.level == Log.Levels.CRITICAL, (
        "individual logger should ignore set_global_log_level and remain %s" % Log.Levels.CRITICAL
    )
    assert individual_logger._filehandler.level == constant_level, (
        "individual logger filehandler should ignore set_global_log_level and remain %s" % constant_level
    )


# test_individual_logger has to be before this one
def test_file_writing(logger_file):
    def get_random_string(length):
        letters = string.ascii_lowercase
        result_str = "".join(random.choice(letters) for i in range(length))
        return result_str

    def check_logger_file_contents(logger, text):
        fle = logger.logs_dir / logger.log_session_filename
        with fle.open("r") as f:
            contents = f.read()
            output = text in contents
            if not output:
                print("text: %s" % text)
                print("contents: %s" % contents)
            return output

    unique_string = get_random_string(24)

    unique_string += "1"
    logger_file.debug(
        "debug text абракадабра ™: level: '%s' unique_string: '%s'" % (logger_file.Levels.DEBUG, unique_string)
    )
    assert check_logger_file_contents(logger_file, unique_string)

    unique_string += "1"
    logger_file.info(
        "info text абракадабра ™: level: '%s' unique_string: '%s'" % (logger_file.Levels.INFO, unique_string)
    )
    assert check_logger_file_contents(logger_file, unique_string)

    unique_string += "1"
    logger_file.warning(
        "warning text абракадабра ™: level: '%s' unique_string: '%s'" % (logger_file.Levels.WARNING, unique_string)
    )
    assert check_logger_file_contents(logger_file, unique_string)

    unique_string += "1"
    logger_file.error(
        "error text абракадабра ™: level: '%s' unique_string: '%s'" % (logger_file.Levels.ERROR, unique_string)
    )
    assert check_logger_file_contents(logger_file, unique_string)

    unique_string += "1"
    logger_file.critical(
        "critical text абракадабра ™: level: '%s' unique_string: '%s'" % (logger_file.Levels.CRITICAL, unique_string)
    )
    assert check_logger_file_contents(logger_file, unique_string)

    unique_string += "1"
    logger_file.printer(
        "test filehandler message абракадабра ™ unique_string: '%s'" % unique_string, color="blue", end="", clear=True
    )
    assert check_logger_file_contents(logger_file, unique_string)

    unique_string += "1"
    logger_file.green("test green абракадабра ™ unique_string: '%s'" % unique_string, end="\t\t\t\t")
    assert check_logger_file_contents(logger_file, unique_string)

    unique_string += "1"
    logger_file.yellow("test yellow абракадабра ™ unique_string: '%s'" % unique_string)
    assert check_logger_file_contents(logger_file, unique_string)

    unique_string += "1"
    logger_file.red("red text unique_string: '%s'" % unique_string)
    assert check_logger_file_contents(logger_file, unique_string)


# noinspection PyUnusedLocal
def test_add_handler(_logger, logger_file):
    class CustomHandler(logging.Handler):
        pass

    logger1 = _logger(name="logger1")  # noqa: F841
    logger2 = logger_file  # noqa: F841
    logger3 = _logger(name="logger3")  # noqa: F841
    handler = CustomHandler()
    logger1.logger.addHandler(handler)
    assert handler not in logger2.logger.handlers, "Handler shouldn't be in a logger where it wasn't added"

    Log.add_handler_to_all_loggers(handler)
    for logger in Log.loggers.values():
        if logger in logger.individual_loggers.values():
            continue

        assert handler in logger.logger.handlers, "%s must be in %s %s" % (handler, logger, logger.logger.handlers)


if __name__ == "__main__":
    __logger_file = logger("logger", logs_dir=Path(__file__).parent.parent / "Logs")
    test_basic(__logger_file)
    test_instance_exception()
    test_levels()
    test_file_writing(__logger_file)
    print("")
