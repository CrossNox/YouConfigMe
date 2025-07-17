"""Common casts"""

from typing import Union


def to_bool(config_value: Union[str, bool]) -> bool:
    """Cast a configuration option into boolean."""
    if isinstance(config_value, bool):
        return config_value

    if config_value.lower() in ("yes", "true", "t", "1", "True"):
        return True

    if config_value.lower() in ("no", "false", "f", "0", "False"):
        return False

    raise ValueError(f"Invalid value for to_bool: {config_value}")
