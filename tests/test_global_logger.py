#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
    # noinspection PyProtectedMember
    output._clean()
    [f.unlink() for f in tmpdir.glob('*.log')]


def test_basic(logger_file):
    """Basic Test.
    :type logger_file: Log
    """

    def __func(arg, *args, **kwargs):
        logger_file.trace()
        logger_file.debug('func called')

    logger_file.debug("debug text абракадабра ™: level: '%s'" % logger_file.LOGGER_LEVELS.DEBUG)
    logger_file.info("info text абракадабра ™: level: '%s'" % logger_file.LOGGER_LEVELS.INFO)
    logger_file.warning("warning text абракадабра ™: level: '%s'" % logger_file.LOGGER_LEVELS.WARNING)
    logger_file.error("error text абракадабра ™: level: '%s'" % logger_file.LOGGER_LEVELS.ERROR)
    logger_file.critical("critical text абракадабра ™: level: '%s'" % logger_file.LOGGER_LEVELS.CRITICAL)
    logger_file.printer('test filehandler message абракадабра ™', color='blue', end='', clear=True)
    logger_file.green('test green абракадабра ™', end='\t\t\t\t')
    logger_file.yellow('test yellow абракадабра ™')
    logger_file.red('red text')
    __func('argument', 'arg', 'arg1', named_arg='test')


def test_instance_exception():
    with pytest.raises(ValueError):
        Log('something')
