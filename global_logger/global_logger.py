# #!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

import inspect
import logging
import os
import platform
import re
import sys
import time
import traceback

import pendulum
from colorama import Fore
from colorama.ansi import AnsiFore
from colorlog import ColoredFormatter, default_log_colors
from pathlib import Path
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    pass

PYTHON2 = sys.version_info[0] < 3

if PYTHON2:
    pass
else:
    # noinspection PyShadowingBuiltins
    buffer = memoryview


class Struct(object):
    def __init__(self, **entries):
        self.__dict__.update(entries)


def get_prev_function_name():
    stack = inspect.stack()
    stack1 = stack[2]
    filepath = stack1[1]  # 'source\\toolset\\decorators.py'
    output = filepath.replace('/', '.').replace('\\', '.').replace('.py', '')
    module = stack1[3]  # 'measure' or '<module>'
    if module != '<module>':
        output = '%s.%s' % (output, module)
    return output


def clear_message(msg):
    return re.sub(r'\x1b(\[.*?[@-~]|\].*?(\x07|\x1b\\))', '', msg)


class InfoFilter(logging.Filter):
    def filter(self, rec):
        return rec.levelno <= logging.INFO


class Log(object):
    if PYTHON2:
        # noinspection PyProtectedMember
        LOGGER_LEVELS_DICT = {k: v for k, v in logging._levelNames.items() if not isinstance(k, int)}
    else:
        # noinspection PyProtectedMember
        LOGGER_LEVELS_DICT = logging._nameToLevel
    LOGGER_LEVELS = Struct(**LOGGER_LEVELS_DICT)
    GLOBAL_LOG_LEVEL = logging.INFO
    LOGGER_MESSAGE_FORMAT = '%(asctime)s.%(msecs)03d %(lineno)3s:%(name)-22s %(levelname)-6s %(message)s'
    LOGGER_DATE_FORMAT_FULL = '%Y-%m-%d %H:%M:%S'
    LOGGER_COLORED_MESSAGE_FORMAT = '%(log_color)s%(message)s'
    LOGGER_DATE_FORMAT = '%H:%M:%S'
    MAX_LOG_FILES = 50
    # DEFAULT_LOGS_DIR = Path(__file__).parent.parent.parent.resolve() / 'logs'
    DEFAULT_LOGS_DIR = 'logs'
    loggers = {}
    auto_added_handlers = []  # type: List[logging.Handler]
    log_session_filename = None
    logs_dir = DEFAULT_LOGS_DIR  # type: Path

    @staticmethod
    def set_global_log_level(level):
        print("Changing global logger level to %s" % level)
        Log.GLOBAL_LOG_LEVEL = level
        for logger in Log.loggers.values():
            logger.level = level
        for handler in Log.auto_added_handlers:
            handler.level = level

    def __init__(self, name, level=None, logs_dir=None, dump_initial_data=False, max_log_files=None,
                 message_format=None, date_format_full=None, date_format=None):
        level = level or Log.GLOBAL_LOG_LEVEL

        verbose = os.getenv('LOG_VERBOSE', False)
        if verbose:
            level = logging.DEBUG

        self.name = name
        Log.LOGGER_MESSAGE_FORMAT = message_format or Log.LOGGER_MESSAGE_FORMAT
        Log.LOGGER_DATE_FORMAT_FULL = date_format_full or Log.LOGGER_DATE_FORMAT_FULL
        Log.LOGGER_DATE_FORMAT = date_format or Log.LOGGER_DATE_FORMAT
        Log.MAX_LOG_FILES = max_log_files or Log.MAX_LOG_FILES
        Log.logs_dir = logs_dir or Log.logs_dir or Log.DEFAULT_LOGS_DIR

        self._dump_initial_data = dump_initial_data
        self.logger = logging.getLogger(self.name)
        self.logger.propagate = False  # this fixes a recursion if other modules also use logging

        self.debug = self.logger.debug
        self.info = self.logger.info
        self.warning = self.logger.warning
        self.error = self.logger.error
        self.critical = self.logger.critical
        self.exception = self.logger.exception

        new_log_file = False
        if Log.logs_dir:
            Log.logs_dir = Path(Log.logs_dir)
            if not (Log.logs_dir.exists() and Log.logs_dir.is_dir()):
                Log.logs_dir.mkdir()

            if Log.log_session_filename is None:
                from pendulum.tz.zoneinfo.exceptions import InvalidZoneinfoFile
                try:
                    now = pendulum.now()
                except InvalidZoneinfoFile:
                    now = pendulum.now(pendulum.UTC)  # travis-ci precaution
                Log.log_session_filename = "%s.log" % now.strftime('%Y-%m-%d_%H-%M-%S')
                self._clean_logs_folder()
                new_log_file = True

        formatter = logging.Formatter(Log.LOGGER_MESSAGE_FORMAT, datefmt=Log.LOGGER_DATE_FORMAT_FULL)
        # noinspection PyTypeChecker
        color_formatter = ColoredFormatter(fmt=Log.LOGGER_COLORED_MESSAGE_FORMAT, datefmt=Log.LOGGER_DATE_FORMAT,
                                           reset=True, log_colors=default_log_colors)

        self._stdout_handler = logging.StreamHandler(sys.stdout)
        self._stdout_handler.addFilter(InfoFilter())
        self.logger.addHandler(self._stdout_handler)
        self._stdout_handler.setFormatter(color_formatter)

        self._stderr_handler = logging.StreamHandler(sys.stderr)
        self.logger.addHandler(self._stderr_handler)
        self._stderr_handler.setFormatter(color_formatter)

        if Log.logs_dir:
            self.log_file_full_path = Log.logs_dir / Log.log_session_filename
            self._filehandler = logging.FileHandler(str(self.log_file_full_path), encoding='UTF-8')
            self._filehandler.setFormatter(formatter)
            self.logger.addHandler(self._filehandler)

        self.level = level
        Log.loggers[self.name] = self
        if Log.logs_dir and self._dump_initial_data and new_log_file:
            try:
                _env_dump_str = "Python {sysver} @ {platf}\n{user}@{comp} @ {winver}".format(
                    sysver=sys.version, platf=platform.architecture(), winver=sys.getwindowsversion(),
                    user=os.environ['USERNAME'], comp=os.environ['COMPUTERNAME'])
                self.debug(_env_dump_str)
            except:  # noqa
                pass

    def __str__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name

    @property
    def verbose(self):
        return self.level == logging.DEBUG

    @verbose.setter
    def verbose(self, value):
        if value is self.verbose:
            return

        if value is True:
            self.set_global_log_level(logging.DEBUG)
        else:
            self.set_global_log_level(logging.INFO)

    @classmethod
    def get_logger(cls, name=None, level=None, logs_dir=None, dump_initial_data=False, max_log_files=None,
                   message_format=None, date_format_full=None, date_format=None):
        """
        Main instantiating method for the class. Use it to instantiate global logger.

        :param name: a unique logger name that is re-/used if already exists, defaults to the function path.
        :type name: str
        :param level: Logging level for the current instance.
        :type level: int
        :param logs_dir: Path where the .log files would be created, if provided.
        :type logs_dir: Path or str
        :param dump_initial_data: Whether to fill the newly created .log file with initial user data.
        :type dump_initial_data: bool
        :param max_log_files: Maximum .log files to store.
        :type max_log_files: int
        :param message_format: Logging message format.
        :type message_format: str
        :param date_format_full: Logging full date format.
        :type date_format_full: str
        :param date_format: Logging on-screen date format.
        :type date_format: str
        :return: :class:`Log` instance to work with.
        :rtype: :class:`Log`
        """
        name = name or get_prev_function_name()
        output = Log.loggers.get(name) or cls(name, level=level, logs_dir=logs_dir, dump_initial_data=dump_initial_data,
                                              max_log_files=max_log_files, message_format=message_format,
                                              date_format_full=date_format_full, date_format=date_format)
        Log._add_autoadded_handlers()
        return output

    @staticmethod
    def _add_autoadded_handlers():
        for handler in Log.auto_added_handlers:
            for logger_name, logger in Log.loggers.items():
                if handler not in logger.logger.handlers:
                    logger.logger.addHandler(handler)

    @property
    def level(self):
        if hasattr(self, 'stdout_handler'):
            return self._stdout_handler.level

    @level.setter
    def level(self, value):
        Log.GLOBAL_LOG_LEVEL = value
        self.logger.setLevel(logging.DEBUG)
        if Log.logs_dir:
            self._filehandler.setLevel(logging.DEBUG)
        self._stdout_handler.setLevel(value)
        self._stderr_handler.setLevel(logging.WARNING)

    @property
    def _log_files(self):
        output = sorted(list(Log.logs_dir.glob('*.log')), key=lambda f: f.stat().st_ctime,
                        reverse=True)
        return output

    @staticmethod
    def _clean_logs_folder():
        log_files = sorted(list(Log.logs_dir.glob('*.log')), key=lambda f: f.stat().st_ctime,
                           reverse=True)
        if len(log_files) > Log.MAX_LOG_FILES:
            try:
                [_file.unlink() for _file in log_files[Log.MAX_LOG_FILES:]]
            except:  # noqa
                pass

    def green(self, *message, **kwargs):
        return self.printer(color='green', *message, **kwargs)

    def red(self, *message, **kwargs):
        return self.printer(color='red', *message, **kwargs)

    def yellow(self, *message, **kwargs):
        return self.printer(color='yellow', *message, **kwargs)

    def printer(self, *message, **kwargs):
        """

        :param message:
        :type message: str or list of str
        :param end:
        :type end: str
        :param color:
        :type color: AnsiFore
        :param clear:
        :type clear: bool
        """
        default_end = '\n'
        end = kwargs.get(str('end'), None)
        color = kwargs.get(str('color'))
        clear = kwargs.get(str('clear'), True)
        print_end = kwargs.get(str('end'), default_end)
        for msg in message:
            timestamp = '' if end == '' else '%s ' % time.strftime(str("%H:%M:%S"))

            if Log.logs_dir:
                _timestamped_message = '%s%s' % (timestamp, msg)
                _cleared_timestamped_message = clear_message(_timestamped_message)
                self._file_printer(_cleared_timestamped_message)

            # todo: emit to custom handlers
            for handler in Log.auto_added_handlers:
                handler.emit(msg)

            _cleared_message = msg
            if clear is True and isinstance(msg, (str, buffer)):
                _cleared_message = clear_message(msg)

            _colored_msg = _cleared_message
            if color:
                if not isinstance(color, AnsiFore):
                    color = getattr(Fore, color.upper(), Fore.GREEN)
                _colored_msg = '%s%s%s' % (color, _cleared_message, Fore.RESET)

            print(_colored_msg, end=print_end)

    def _file_printer(self, msg):
        if not Log.logs_dir:
            return

        if not msg.endswith('\n'):
            msg += '\n'

        # if not PYTHON2 and isinstance(msg, str):
        #     msg = msg.encode('UTF-8')
        self._filehandler.stream.write(msg)
        self._filehandler.flush()

    def trace(self):
        frame = inspect.currentframe().f_back
        file_path = Path(frame.f_globals['__file__'])
        file_name = file_path.stem
        file_dir = file_path.parent.stem
        func_name = traceback.extract_stack(None, 2)[0][2]
        args, _, _, values = inspect.getargvalues(frame)
        _params = [(i, values[i]) for i in args if 'self' not in i]
        self.debug("%s.%s.%s%s" % (file_dir, file_name, func_name, _params))

    # @staticmethod
    # def _string_magic(msg):
    #     # if not PYTHON2 and isinstance(msg, str):
    #     #     return msg.encode('UTF-8')
    #
    #     return msg
    #
    # def debug(self, msg, *args, **kwargs):
    #     msg = self._string_magic(msg)
    #     return self.logger.debug(msg, *args, **kwargs)
    #
    # def info(self, msg, *args, **kwargs):
    #     return self.logger.info(self._string_magic(msg), *args, **kwargs)
    #
    # def warning(self, msg, *args, **kwargs):
    #     return self.logger.warning(self._string_magic(msg), *args, **kwargs)
    #
    # def error(self, msg, *args, **kwargs):
    #     return self.logger.error(self._string_magic(msg), *args, **kwargs)
    #
    # def critical(self, msg, *args, **kwargs):
    #     return self.logger.critical(self._string_magic(msg), *args, **kwargs)
    #
    # def exception(self, msg, *args, exc_info=True, **kwargs):
    #     return self.logger.info(self._string_magic(msg), *args, exc_info=exc_info, **kwargs)


def __func():
    log.trace()
    log.debug('func called')


if __name__ == '__main__':
    log = Log.get_logger()
    log.debug('test debug абракадабра')
    log.info('test info абракадабра')
    log.error('test error абракадабра')
    log.printer('test filehandler message абракадабра')
    log.warning('test warning абракадабра')
    log.green('test green абракадабра')
    __func()
    print("")
