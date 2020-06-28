#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
import pytest


@pytest.fixture
def log():
    from global_logger import Log
    return Log.get_logger()


def test_basic(log):
    """Basic Test.
    :type log: Log
    """
    log.debug("debug text абракадабра ™: level: '%s'" % log.LOGGER_LEVELS.DEBUG)
    log.info("info text абракадабра ™: level: '%s'" % log.LOGGER_LEVELS.INFO)
    log.warning("warning text абракадабра ™: level: '%s'" % log.LOGGER_LEVELS.WARNING)
    log.error("error text абракадабра ™: level: '%s'" % log.LOGGER_LEVELS.ERROR)
    log.critical("critical text абракадабра ™: level: '%s'" % log.LOGGER_LEVELS.CRITICAL)
    log.printer('test filehandler message абракадабра ™', color='blue', end='', clear=True)
    log.green('test green абракадабра ™', end='\t\t\t\t')
    log.yellow('test yellow абракадабра ™')
    log.red('red text')
