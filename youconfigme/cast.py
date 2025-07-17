"""Common casts"""

import builtins
from typing import Optional, Union


def ellipsis_none(config_value: Union[str, "builtins.ellipsis"]) -> Optional[str]:
    """Return None for ellipsis defaults."""
    if config_value is ...:
        return None
    if config_value == "":
        return None
    return config_value


def to_bool(config_value: Union[str, bool]) -> bool:
    """Cast a configuration option into boolean."""
    if isinstance(config_value, bool):
        return config_value

    if config_value.lower() in ("yes", "true", "t", "1", "True"):
        return True

    if config_value.lower() in ("no", "false", "f", "0", "False"):
        return False

    raise ValueError(f"Invalid value for bool: {config_value}")
