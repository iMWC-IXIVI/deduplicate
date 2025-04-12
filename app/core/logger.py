import logging
import sys
import os

from datetime import date
from core import settings


class LoggingService:
    """
    Класс логирование сервиса\n
    LoggingService:\n
    __attributes:
        __console_logger - Логгер для вывода сообщений в консоль\n
        __file_logger - Логгер для вывода сообщений в файл (Файл с именем дня + .log)\n
    __methods:
        __console_handler (static) - Настройка хэндлера для логгера в консоль\n
        __file_handler (static) - Настрйока хэндлера для логгера в файл\n
        __settings_console_logger - Базовые настройки логгера в консоль\n
        __settings_file_logger - Базовые настрйоки логгера в файл\n
    methods:
        debug_message - Вывод сообщений уровня debug (В консоль)\n
        info_message - Вывод сообщений уровня info (В консоль)\n
        warning_message - Вывод сообщений уровня warning (В консоль)\n
        error_message - Вывод сообщений уровня error (В файл и консоль)\n
    """
    def __init__(self):
        self.__console_logger = logging.getLogger('console_logger')
        self.__file_logger = logging.getLogger('file_logger')

        self.__setting_console_logger()
        self.__setting_file_logger()

        self.__console_logger.addHandler(self.__console_handler())
        self.__file_logger.addHandler(self.__file_handler())

    @staticmethod
    def __console_handler():
        fmt = logging.Formatter('[CONSOLE - %(filename)s] %(asctime)s | %(levelname)s | %(message)s', '%H:%M:%S')

        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(fmt=fmt)

        return handler

    @staticmethod
    def __file_handler():
        fmt = logging.Formatter('[FILE - %(filename)s] %(asctime)s | %(levelname)s | %(message)s', '%H:%M:%S')

        handler = logging.FileHandler(os.path.join(settings.BASE_DIR, 'loggers', f'{date.today()}.log'))
        handler.setLevel(logging.ERROR)
        handler.setFormatter(fmt=fmt)

        return handler

    def __setting_console_logger(self):
        self.__console_logger.setLevel(logging.DEBUG)
        self.__console_logger.propagate = False

    def __setting_file_logger(self):
        self.__file_logger.setLevel(logging.ERROR)
        self.__file_logger.propagate = False

    def debug_message(self, message):
        self.__console_logger.debug(msg=message)

    def info_message(self, message):
        self.__console_logger.info(msg=message)

    def warning_message(self, message):
        self.__console_logger.warning(msg=message)

    def error_message(self, message):
        self.__console_logger.error(msg=message)
        self.__file_logger.error(msg=message)


log = LoggingService()
