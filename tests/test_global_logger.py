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
    log.debug('test debug абракадабра')
    log.info('test info абракадабра')
    log.error('test error абракадабра')
    log.printer('test filehandler message абракадабра')
    log.warning('test warning абракадабра')
    log.green('test green абракадабра')
