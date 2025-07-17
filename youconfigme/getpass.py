"""Get values from GNU pass."""

import subprocess
from typing import Optional


def get_pass(key: str, section: Optional[str] = None) -> str:
    """Get password from GNU pass.

    Args:
        key: The key to retrieve
        section: Optional section prefix

    Returns:
        The password value as a string
    """
    if section is not None:
        key = f"{section}/{key}"
    res = subprocess.run(["pass", key], capture_output=True, check=True)
    return res.stdout.decode().strip()
