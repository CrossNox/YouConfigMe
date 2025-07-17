"""Entrypoint to make relevant classes available at the top level."""

from typing import TYPE_CHECKING

from .youconfigme import AutoConfig, Config, ConfigItemNotFound, ConfigSection

if TYPE_CHECKING:
    # Re-export for type checkers
    from .youconfigme import AutoConfig as AutoConfig
    from .youconfigme import Config as Config
    from .youconfigme import ConfigItemNotFound as ConfigItemNotFound
    from .youconfigme import ConfigSection as ConfigSection

__version__ = "1.0.0"
__all__ = ["AutoConfig", "Config", "ConfigItemNotFound", "ConfigSection"]
