"""Main module for youconfigme"""

import io
import logging
import os
from configparser import ConfigParser
from pathlib import Path


def config_logger(name):
    """Helper function that sets logging for stream and file

    Args:
        name (str): name for the logger

    Returns:
        logging.RootLogger: the configured logger
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    try:
        fh = logging.FileHandler(f'{name}.log')
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    except OSError:
        pass

    return logger


logger = config_logger(__name__)


DEFAULT_SECTION = 'settings'
INI_FILE = 'settings.ini'
# ENV_FILE = 'settings.env'


class ConfigItemNotFound(Exception):
    """The config item could not be found"""


class ConfigAttribute:
    """Handles an attribute in the following order:
    1) config value
    2) default value
    3) environment variable value
    """

    def __init__(self, name, value, section_name):
        """Creates a new attribute

        Args:
            name (str): name of the attribute
            value (object): stringify-able object to be used as value
            section_name (str): section where the value should be placed
        """
        self.name = name
        self.value = value
        self.section_name = section_name
        if self.section_name is not None:
            self.env_str = f"{section_name.upper()}_{name.upper()}"
        else:
            self.env_str = f"{name.upper()}"
        self.env = os.getenv(self.env_str)
        if self.value is not None:
            self.value = str(self.value)
        if self.env is not None:
            self.env = str(self.env)

    def __call__(self, default=None, cast=None):
        retval = None
        if self.value is not None:
            retval = self.value
        elif default is not None:
            retval = default
        elif self.env is not None:
            retval = self.env
        else:
            raise ConfigItemNotFound
        return (cast or str)(retval)

    def __getattr__(self, name):
        raise ConfigItemNotFound(f"section {name} not found")


class ConfigSection:
    """A section from a Config item"""

    def __init__(self, name, items):
        """Creates a new ConfigSection

        Args:
            name (str): name of the section
            items (mapping): mapping of attributes names to values
        """
        self.name = name
        self.items = items or {}

    def __getattr__(self, val):
        return ConfigAttribute(val, self.items.get(val), self.name)

    def __call__(self, default=None, cast=None):
        return ConfigAttribute(self.name, None, None)(default=default, cast=cast)


class Config:
    """Base Config item"""

    def __init__(self, from_items=INI_FILE, default_section=DEFAULT_SECTION):
        """Creates a new Config item

        Args:
            from_items (mapping or str or filename): where the config should be
                populated from:
                - filename: path for an `ini` file
                - mapping: mapping of sections -> mapping of name -> value
                - str: string representation of an `ini` file
            default_section (str): config items that need not be under a section
        """
        self.default_section = default_section

        if from_items is not None:
            try:
                self._init_from_mapping(from_items)
            except AttributeError:
                self._init_from_str(from_items)

    def _init_from_mapping(self, mapping):
        for section in mapping.keys():
            if section != self.default_section:
                setattr(self, section, ConfigSection(section, mapping[section]))
            else:
                for k, v in mapping[section].items():
                    setattr(self, k, ConfigAttribute(k, v, section))

    def _init_from_str(self, str_like):
        try:
            buf = io.StringIO(str_like)
            cp = ConfigParser()
            cp.read_file(buf)
            self._init_from_mapping(cp)
        except Exception:
            cwd_file = Path.cwd() / str_like
            if cwd_file.is_file():
                cp = ConfigParser()
                cp.read(cwd_file)
                self._init_from_mapping(cp)
            else:
                raise FileNotFoundError

    def __getattr__(self, name):
        return ConfigSection(name, None)


class AutoConfig(Config):
    """Safe Config item.


    It searches for an `ini` file upwards. If there's no `ini` file, it returns an
    empty Config file that can be used with defaults and/or env vars."""

    def __init__(self, max_up_levels=1):
        """Creates a new AutoConfig item

        Args:
            max_up_levels (int): how many parents should it traverse searching
                for an `ini` file
        """
        settings_file = Path.cwd() / INI_FILE
        for _ in range(max_up_levels + 1):
            try:
                logger.info(f"searching for config on {str(settings_file)}")
                super().__init__(from_items=str(settings_file))
                return
            except FileNotFoundError:
                settings_file = settings_file.parents[1] / INI_FILE
        logger.info("autoconfig - empty config")
        super().__init__(from_items=None)
