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
from typing import (Any, Callable, Dict, List, Mapping, Optional, TypeVar,
                    Union, overload)

import toml as libtoml

from youconfigme.getpass import get_pass


def config_logger(name: str) -> logging.Logger:
    """Set a new logger.

    Args:
        name (str): name for the logger

    Returns:
        logging.Logger: the configured logger
    """
    loglevel = (
        os.environ.get("YOUCONFIGME_LOGLEVEL", os.environ.get("YCM_LOGLEVEL", "error"))
    ).lower()

    if loglevel not in ("info", "error", "debug"):
        raise ValueError(f"YouConfigMe - log level {loglevel} is not valid")

    logging_level = {
        "info": logging.INFO,
        "error": logging.ERROR,
        "debug": logging.DEBUG,
    }[loglevel]

    new_logger = logging.getLogger(name)
    new_logger.setLevel(logging_level)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging_level)
    console_handler.setFormatter(formatter)
    new_logger.addHandler(console_handler)

    return new_logger


logger = config_logger(__name__)


DEFAULT_SECTION = "settings"
INI_FILE = "settings.ini"
DEFAULT_SEP = "_"
# ENV_FILE = 'settings.env'

T = TypeVar("T")


class ConfigItemNotFound(Exception):
    """The config item could not be found."""


class ConfigAttribute:
    """Handles an attribute.

    The order to do so is:
    1) environment variable value
    2) config value
    3) default value
    """

    def __init__(
        self,
        name: str,
        value: Optional[Any],
        section_name: Optional[str],
        sep: str = DEFAULT_SEP,
    ) -> None:
        """Create a new attribute.

        Args:
            name (str): name of the attribute
            value (object): stringify-able object to be used as value
            section_name (str): section where the value should be placed
            sep (str): string to separate sections from items in env vars.
        """
        self.__name = name
        self.__value = value
        self.__section_name = section_name
        if self.__section_name is not None:
            self.__env_str = f"{self.__section_name.upper()}{sep}{name.upper()}"
        else:
            self.__env_str = f"{name.upper()}"
        logger.debug("Try to get env_str: %s", self.__env_str)
        self.__env = os.getenv(self.__env_str)
        if self.__value is not None:
            self.__value = str(self.__value)
        if self.__env is not None:
            self.__env = str(self.__env)

    @overload
    def __call__(
        self, default: None = None, cast: None = None, from_pass: bool = False
    ) -> str: ...

    @overload
    def __call__(
        self, default: T, cast: None = None, from_pass: bool = False
    ) -> Union[T, str]: ...

    @overload
    def __call__(
        self,
        default: None = None,
        cast: Callable[[str], T] = ...,
        from_pass: bool = False,
    ) -> T: ...

    @overload
    def __call__(
        self, default: Any, cast: Callable[[str], T] = ..., from_pass: bool = False
    ) -> T: ...

    def __call__(
        self,
        default: Optional[Any] = None,
        cast: Optional[Callable[[str], Any]] = None,
        from_pass: bool = False,
    ) -> Any:
        """Call the item.

        Follows the order of lookup.

        Args:
            default (str): default value if item not found
            cast (callable): how to cast the item
            from_pass (bool): whether to retrieve value from pass

        Returns:
            Any: A str or casted item
        """
        retval: Any
        if self.__env is not None:
            retval = self.__env
        elif self.__value is not None:
            retval = self.__value
        elif default is not None:
            retval = str(default)
        else:
            err_str = f"Configuration item {self.__name}"
            if self.__section_name is not None:
                err_str = f"{err_str} on section {self.__section_name}"
            err_str = f"{err_str} was not found"
            raise ConfigItemNotFound(err_str)

        if from_pass:
            retval = get_pass(retval)

        return (cast or str)(retval)

    def __getattr__(self, name: str) -> None:
        """Get attr that does not exist."""
        raise ConfigItemNotFound(f"section {name} not found")


class ConfigSection:
    """A section from a Config item."""

    def __init__(
        self, name: str, items: Optional[Mapping[str, Any]], sep: str = DEFAULT_SEP
    ) -> None:
        """Create a new ConfigSection.

        Args:
            name (str): name of the section
            items (mapping): mapping of attributes names to values
            sep (str): string to separate sections from items in env vars.
        """
        self.__name = name
        self.__items = items or {}
        self.__sep = sep
        self.__prefix = f"{self.__name}{self.__sep}".upper()

    def __getattr__(self, val: str) -> ConfigAttribute:
        """Get a new attribute."""
        return ConfigAttribute(val, self.__items.get(val), self.__name, sep=self.__sep)

    def __call__(
        self, default: Optional[Any] = None, cast: Optional[Callable[[str], Any]] = None
    ) -> Any:
        """Get attribute called as section."""
        return ConfigAttribute(self.__name, None, None, sep=self.__sep)(
            default=default, cast=cast
        )

    def to_dict(self) -> Dict[str, str]:
        """Return as dict.

        Args:
            None

        Returns:
            dict: all the key:value pairs from the initial mapping,
            neglecting environment variables not present there.
        """
        items = dict(self.__items)
        env_items = {
            envvar[len(self.__prefix) :].lower(): envval  # noqa: E203
            for envvar, envval in os.environ.items()
            if envvar.startswith(self.__prefix)
        }
        items.update(env_items)
        if items == {}:
            raise ConfigItemNotFound(f"Section {self.__name} is empty")
        ret_dict = {k: self.__getattr__(k)() for k in items.keys()}
        return ret_dict


FromItemsType = Union[str, Path, Mapping[str, Any], None]


class Config:
    """Base Config item."""

    def __init__(
        self,
        from_items: FromItemsType = INI_FILE,
        default_section: str = DEFAULT_SECTION,
        sep: str = DEFAULT_SEP,
    ) -> None:
        """Create a new Config item.

        Args:
            from_items (mapping or str or filename): where the config should be
                populated from:
                - filename: path for an `ini` file
                - mapping: mapping of sections -> mapping of name -> value
                - str: string representation of an `ini` file
            default_section (str): config items that need not be under a section
            sep (str): string to separate sections from items in env vars.
        """
        self.__sep: str = sep
        self.__default_section: str = default_section
        self.__fake_default_section: str = (
            "None" if default_section != "None" else "enoN"
        )
        self.__config_sections: List[str] = []
        self.__config_attributes: List[str] = []

        if from_items is not None:
            try:
                self._init_from_mapping(from_items)  # type: ignore
            except AttributeError:
                self._init_from_str(from_items)  # type: ignore

    def _init_from_mapping(self, mapping: Mapping[str, Any]) -> None:
        for section in mapping.keys():
            if section == self.__fake_default_section:
                continue
            if section != self.__default_section:
                setattr(
                    self, section, ConfigSection(section, mapping[section], self.__sep)
                )
                self.__config_sections.append(section)
            else:
                for k, v in mapping[section].items():
                    setattr(self, k, ConfigAttribute(k, v, None, sep=self.__sep))
                    self.__config_attributes.append(k)

    def _init_from_str(self, str_like: Union[str, Path]) -> None:
        try:
            buf = io.StringIO(str(str_like))
            config_parser = ConfigParser(default_section=self.__fake_default_section)
            config_parser.read_file(buf)
            self._init_from_mapping(config_parser)
        except Exception as e:  # pylint: disable=broad-except
            cwd_file = Path.cwd() / str(str_like)
            if cwd_file.is_file() and cwd_file.suffix == ".ini":
                config_parser = ConfigParser(
                    default_section=self.__fake_default_section
                )
                config_parser.read(cwd_file)
                self._init_from_mapping(config_parser)
            elif cwd_file.is_file() and cwd_file.suffix == ".toml":
                config = libtoml.load(cwd_file)
                self._init_from_mapping(config)
            else:
                raise FileNotFoundError from e

    def __getattr__(self, name: str) -> ConfigSection:
        """Get new section."""
        return ConfigSection(name, None, self.__sep)

    def to_dict(self) -> Dict[str, Dict[str, str]]:
        """Return as dict.

        Args:
            None

        Returns:
            dict: all the key:value pairs from the initial mapping,
            neglecting environment variables not present there.
        """
        ret_dict: Dict[str, Any] = {}
        for section in self.__config_sections:
            ret_dict[section] = self.__getattribute__(section).to_dict()
        for attribute in self.__config_attributes:
            ret_dict[attribute] = self.__getattribute__(attribute)()
        return ret_dict

    def to_dotenv(self) -> str:
        """Return as .env file"""
        lines: List[str] = []
        for k, v in self.to_dict().items():
            try:
                for k1, v1 in v.items():
                    lines.append(f"{k}{self.__sep}{k1}={v1}".upper())
            except AttributeError:
                lines.append(f"{k}={v}".upper())
        return "\n".join(sorted(lines))


class AutoConfig(Config):  # pylint: disable=too-few-public-methods
    """Safe Config item.

    Searches for an `ini` file upwards. If there's no `ini` file, it returns an
    empty Config file that can be used with defaults and/or env vars.
    """

    def __init__(
        self, max_up_levels: int = 1, filename: str = INI_FILE, sep: str = DEFAULT_SEP
    ) -> None:
        """Create a new AutoConfig item.

        Args:
            max_up_levels (int): how many parents should it traverse searching
                for an `ini` file
            filename (str): filename to search for
            sep (str): string to separate sections from items in env vars.
        """
        frame = sys._getframe()
        if frame.f_back is None:
            raise ValueError("No caller frame")
        settings_file = Path(frame.f_back.f_code.co_filename).parent / filename
        for _ in range(max_up_levels + 1):
            try:
                logger.info("searching for config on %s", str(settings_file))
                super().__init__(from_items=str(settings_file), sep=sep)
                return
            except FileNotFoundError:
                try:
                    settings_file = settings_file.parents[1] / filename
                except IndexError:
                    break
        logger.info("autoconfig - empty config")
        super().__init__(from_items=None, sep=sep)
