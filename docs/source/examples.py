#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Global Logger Examples """
from global_logger import Log

# create and/or reuse a global logger, choosing its name dynamicaly
# with screen-only output and the default logging level INFO
log = Log.get_logger()

# this forcec ALL loggers to lower their logging level to DEBUG
log.verbose = True

log.debug("debug text: level: %s" % log.Levels.DEBUG)
log.info("info text: level: %s" % log.Levels.INFO)
log.warning("warning text: level: %s" % log.Levels.WARNING)
log.error("error text: level: %s" % log.Levels.ERROR)
log.critical("critical text: level: %s" % log.Levels.CRITICAL)
# 2020-06-28 14:18:42.004  14:source.examples DEBUG  debug text: level: '10'
# 2020-06-28 14:18:42.004  15:source.examples INFO   info text: level: '20'
# 2020-06-28 14:18:42.004  16:source.examples WARNING warning text: level: '30'
# 2020-06-28 14:18:42.005  17:source.examples ERROR  error text: level: '40'
# 2020-06-28 14:18:42.005  18:source.examples CRITICAL critical text: level: '50'

# log text in purple color without a newline, clearing all the ANSI sylbols from the message
log.printer('always printed text....', color='blue', end='', clear=True)
# can also be simplified to:
log.green('green text', clear=False)
log.yellow('yellow text', end='\t\t\t\t')
log.red('red text')

# create and/or reuses a global logger, choosing its name dynamicaly
# with screen and .log files output at the relative folder 'logs' and the default logging level INFO
log = Log.get_logger(logs_dir='logs')

# force ALL loggers to lower their logging level to WARNING
# Note: file output will always remain on logging level DEBUG
log.level = log.Levels.WARNING


# log a function call including all the arguments
def func(number, other_number):
    log.trace()
    return number * other_number


func(1, 2)
# 2020-06-28 14:30:55.194 322:source.examples DEBUG  source.examples.func[('number', 1), ('other_number', 2)]
