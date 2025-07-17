"""Get values from GNU pass."""

import re
import subprocess
from typing import Optional


def get_pass(key: str, section: Optional[str] = None) -> str:
    """Get password from GNU pass.

    Args:
        key: The key to retrieve (letters, numbers, -, _, /)
        section: Optional section prefix - (letters, numbers, -, _)

    Returns:
        The password value as a string

    Raises:
        ValueError: If key or section contains invalid characters
        subprocess.SubprocessError: If pass command fails
        subprocess.TimeoutExpired: If pass command times out
    """
    # Validate key to prevent command injection
    if not _is_valid_pass_key(key):
        raise ValueError(
            f"Invalid key format: {key}. Only alphanumeric characters, -, _, and / are allowed."
        )

    if section is not None:
        if not _is_valid_pass_key(
            section.replace("/", "")
        ):  # Allow slashes in section for nested paths
            raise ValueError(
                f"Invalid section format: {section}. Only alphanumeric characters, -, and _ are allowed."
            )
        key = f"{section}/{key}"

    try:
        res = subprocess.run(
            ["pass", "show", key],
            capture_output=True,
            check=True,
            timeout=10,  # Add timeout to prevent hanging
            text=True,  # Handle text encoding properly
        )
        return res.stdout.strip()
    except subprocess.TimeoutExpired as e:
        raise subprocess.TimeoutExpired(
            f"pass command timed out for key: {key}", 10
        ) from e
    except subprocess.CalledProcessError as e:
        raise subprocess.SubprocessError(
            f"pass command failed for key: {key}. Error: {e.stderr}"
        ) from e


def _is_valid_pass_key(key: str) -> bool:
    """Validate that a pass key contains only safe characters.

    Args:
        key: The key to validate

    Returns:
        True if key is safe, False otherwise
    """
    if not key:
        return False
    # Allow alphanumeric, hyphens, underscores, and forward slashes
    return re.match(r"^[a-zA-Z0-9/_-]+$", key) is not None
