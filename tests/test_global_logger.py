#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for `global_logger` package."""
import pytest

from global_logger import Log


@pytest.fixture
def log():
    return Log.get_logger()


def test_basic(log):
    """Basic Test.
    :type log: Log
    """
    log.debug('test debug абракадабра')
    log.info('test info абракадабра')
    log.error('test error абракадабра')
    log.printer('test filehandler message абракадабра')
    log.warning('test warning абракадабра')
    log.green('test green абракадабра')
