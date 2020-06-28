# from __future__ import print_function, unicode_literals
# Python2 files have to have this import

from global_logger import Log

log = Log.get_logger()
# this creates and/or reuses global logger, choosing its name dynamicaly

log = Log.get_logger(logs_dir='logs')
