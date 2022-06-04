"""Get values from GNU pass."""

import subprocess


def get_pass(key, section=None):
    if section is not None:
        key = f"{section}/{key}"
    res = subprocess.run(["pass", key], capture_output=True, check=True)
    return res.stdout.decode().strip()
