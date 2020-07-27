#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=redefined-outer-name
""" Global Logger Tests """
from __future__ import print_function, unicode_literals

from pathlib import Path
from typing import TYPE_CHECKING

import pytest

from global_logger import Log

if TYPE_CHECKING:
    from _pytest.tmpdir import TempdirFactory  # noqa


@pytest.fixture
def logger_screen():
    return Log.get_logger(logs_dir=None)


@pytest.fixture(scope='session')
def logger_file(tmpdir_factory):
    """

    :type tmpdir_factory: TempdirFactory
    """
    tmpdir = Path(str(tmpdir_factory.mktemp('tests_logs')))  # type: Path
    output = Log.get_logger(logs_dir=tmpdir)
    yield output
    for logger in output.loggers.values():
        # noinspection PyProtectedMember
        # pylint: disable=protected-access
        logger._clean()
    # pylint: disable=expression-not-assigned
    [f.unlink() for f in tmpdir.glob('*.log')]


def test_basic(logger_file):
    """

    :type logger_file: Log
    """

    # pylint: disable=unused-argument
    def __func(arg, *args, **kwargs):
        logger_file.trace()
        logger_file.debug('func called')

    logger_file.debug("debug text абракадабра ™: level: '%s'" % logger_file.Levels.DEBUG)
    logger_file.info("info text абракадабра ™: level: '%s'" % logger_file.Levels.INFO)
    logger_file.warning("warning text абракадабра ™: level: '%s'" % logger_file.Levels.WARNING)
    logger_file.error("error text абракадабра ™: level: '%s'" % logger_file.Levels.ERROR)
    logger_file.critical("critical text абракадабра ™: level: '%s'" % logger_file.Levels.CRITICAL)
    logger_file.printer('test filehandler message абракадабра ™', color='blue', end='', clear=True)
    logger_file.green('test green абракадабра ™', end='\t\t\t\t')
    logger_file.yellow('test yellow абракадабра ™')
    logger_file.red('red text')
    __func('argument', 'arg', 'arg1', named_arg='test')


def test_instance_exception():
    with pytest.raises(ValueError):
        Log('something')


def test_levels():
    log = Log.get_logger(logs_dir=None)
    assert log.level == log.Levels.INFO, "default logging level should be %s, but not %s" % (
        log.Levels.INFO, log.level)

    log.level = log.Levels.WARNING
    assert log.level == log.Levels.WARNING, "failed changing logging level to %s: it is %s instead" % (
        log.Levels.WARNING, log.level)

    assert log.verbose is not True, "logging should not be verbose, but %s" % log.Levels.WARNING

    log.verbose = True
    assert log.verbose is True, "logging should be verbose after turninig it on, but not %s" % log.level
    assert log.level == log.Levels.DEBUG, "logging should be %s after turning verbose on, but not %s" % (
        log.Levels.DEBUG, log.level)

    log.set_global_log_level(log.Levels.DEBUG)
    assert log.level == log.Levels.DEBUG, "logging should not change from %s to %s after switching to the same level" \
                                          % (log.Levels.DEBUG, log.level)

    log.set_global_log_level(log.Levels.INFO)
    assert log.level == log.Levels.INFO, "logging should change to %s" % log.Levels.INFO


def test_individual_logger():
    log = Log.get_logger('test_individual_logger_global', logs_dir=None, level=Log.Levels.DEBUG)
    individual_logger = Log.get_logger('test_individual_logger_individual', logs_dir=None, global_level=False,
                                       level=Log.Levels.CRITICAL)
    Log.set_global_log_level(Log.Levels.WARNING)
    assert log.level == Log.Levels.WARNING, "log level should be %s after set_global_log_level" % Log.Levels.WARNING
    assert individual_logger.level == Log.Levels.CRITICAL, \
        "individual logger should ignore set_global_log_level and remain %s" % Log.Levels.CRITICAL
