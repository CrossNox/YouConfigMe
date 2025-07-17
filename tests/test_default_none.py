"""Test cast functions"""

# pylint: disable=redefined-outer-name
# pylint: disable=missing-function-docstring
# pylint: disable=unused-variable

import pytest
from youconfigme import Config, ConfigItemNotFound


def test_default_none() -> None:
    config = Config(from_items={"a": {"b": 1}})
    with pytest.raises(ConfigItemNotFound):
        config.a.c()

    assert config.a.c(default=None) is None
