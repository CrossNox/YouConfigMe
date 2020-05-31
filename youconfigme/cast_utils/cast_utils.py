"""Utils that can be used for casting."""

from functools import partial
from pathlib import Path


def ensure_path(path):
    """Create a path if it does not exist."""
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def as_prefix(prefix):
    """Make the option into a prefix."""
    full_opt = "{prefix}{}"
    return partial(full_opt.format, prefix=prefix)
