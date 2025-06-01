"""Config tests from an ini file defining a default section"""

# pylint: disable=redefined-outer-name
# pylint: disable=missing-function-docstring

import os

import pytest
from youconfigme import Config, ConfigSection


@pytest.fixture
def config_dict_defs_osenv():
    os.environ["SEC_A_I1"] = "1"
    os.environ["SEC_A_I2"] = "2"
    yield Config(
        from_items={},
    )
    del os.environ["SEC_A_I1"]
    del os.environ["SEC_A_I2"]


def test_to_dict(config_dict_defs_osenv):
    assert isinstance(config_dict_defs_osenv.sec_a, ConfigSection)
    assert config_dict_defs_osenv.sec_a.to_dict() == {"i1": "1", "i2": "2"}
