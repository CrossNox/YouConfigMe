"""Main module for youconfigme.

Basically a Config is made out of ConfigSections.
ConfigSections and Configs have ConfigAttributes.
"""

import io
import logging
import os
import sys
from configparser import ConfigParser
from pathlib import Path


def config_logger(name):
    """Set a new logger.

    Args:
        name (str): name for the logger

    Returns:
        logging.RootLogger: the configured logger
    """
    new_logger = logging.getLogger(name)
    new_logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    new_logger.addHandler(console_handler)

    return new_logger


logger = config_logger(__name__)


DEFAULT_SECTION = "settings"
INI_FILE = "settings.ini"
# ENV_FILE = 'settings.env'


class ConfigItemNotFound(Exception):
    """The config item could not be found."""


class ConfigAttribute:
    """Handles an attribute.

    The order to do so is:
    1) environment variable value
    2) config value
    3) default value
    """

    def __init__(self, name, value, section_name):
        """Create a new attribute.

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
        """Call the item.

        Follows the order of lookup.


        Args:
            default (str): default value if item not found
            cast (callable): how to cast the item

        Returns:
            Any: A str or casted item
        """
        retval = None
        if self.env is not None:
            retval = self.env
        elif self.value is not None:
            retval = self.value
        elif default is not None:
            retval = default
        else:
            raise ConfigItemNotFound
        return (cast or str)(retval)

    def __getattr__(self, name):
        """Get attr that does not exist."""
        raise ConfigItemNotFound(f"section {name} not found")


class ConfigSection:
    """A section from a Config item."""

    def __init__(self, name, items):
        """Create a new ConfigSection.

        Args:
            name (str): name of the section
            items (mapping): mapping of attributes names to values
        """
        self.name = name
        self.items = items or {}

    def __getattr__(self, val):
        """Get a new attribute."""
        return ConfigAttribute(val, self.items.get(val), self.name)

    def __call__(self, default=None, cast=None):
        """Get attribute called as section."""
        return ConfigAttribute(self.name, None, None)(default=default, cast=cast)

    def to_dict(self):
        """Return as dict.

        Args:
            None

        Returns:
            dict: all the key:value pairs from the initial mapping,
            neglecting environment variables not present there.
        """
        if self.items == {}:
            raise ConfigItemNotFound
        ret_dict = {k: self.__getattr__(k)() for k in self.items.keys()}
        return ret_dict


class Config:
    """Base Config item."""

    def __init__(self, from_items=INI_FILE, default_section=DEFAULT_SECTION):
        """Create a new Config item.

        Args:
            from_items (mapping or str or filename): where the config should be
                populated from:
                - filename: path for an `ini` file
                - mapping: mapping of sections -> mapping of name -> value
                - str: string representation of an `ini` file
            default_section (str): config items that need not be under a section
        """
        self.default_section = default_section
        self.fake_default_section = "None" if default_section != "None" else "enoN"
        self.config_sections = []
        self.config_attributes = []

        if from_items is not None:
            try:
                self._init_from_mapping(from_items)
            except AttributeError:
                self._init_from_str(from_items)

    def _init_from_mapping(self, mapping):
        for section in mapping.keys():
            if section == self.fake_default_section:
                continue
            if section != self.default_section:
                setattr(self, section, ConfigSection(section, mapping[section]))
                self.config_sections.append(section)
            else:
                for k, v in mapping[section].items():
                    setattr(self, k, ConfigAttribute(k, v, section))
                    self.config_attributes.append(k)

    def _init_from_str(self, str_like):
        try:
            buf = io.StringIO(str_like)
            config_parser = ConfigParser(default_section=self.fake_default_section)
            config_parser.read_file(buf)
            self._init_from_mapping(config_parser)
        except Exception as e:  # pylint: disable=broad-except
            cwd_file = Path.cwd() / str_like
            if cwd_file.is_file():
                config_parser = ConfigParser(default_section=self.fake_default_section)
                config_parser.read(cwd_file)
                self._init_from_mapping(config_parser)
            else:
                raise FileNotFoundError from e

    def __getattr__(self, name):
        """Get new section."""
        return ConfigSection(name, None)

    def to_dict(self):
        """Return as dict.

        Args:
            None

        Returns:
            dict: all the key:value pairs from the initial mapping,
            neglecting environment variables not present there.
        """
        ret_dict = {}
        for section in self.config_sections:
            ret_dict[section] = self.__getattribute__(section).to_dict()
        for attribute in self.config_attributes:
            ret_dict[attribute] = self.__getattribute__(attribute)()
        return ret_dict


class AutoConfig(Config):  # pylint: disable=too-few-public-methods
    """Safe Config item.

    Searches for an `ini` file upwards. If there's no `ini` file, it returns an
    empty Config file that can be used with defaults and/or env vars.
    """

    def __init__(self, max_up_levels=1):
        """Create a new AutoConfig item.

        Args:
            max_up_levels (int): how many parents should it traverse searching
                for an `ini` file
        """
        frame = sys._getframe()
        settings_file = Path(frame.f_back.f_code.co_filename).parent / INI_FILE
        for _ in range(max_up_levels + 1):
            try:
                logger.info("searching for config on %s", str(settings_file))
                super().__init__(from_items=str(settings_file))
                return
            except FileNotFoundError:
                try:
                    settings_file = settings_file.parents[1] / INI_FILE
                except IndexError:
                    break
        logger.info("autoconfig - empty config")
        super().__init__(from_items=None)
