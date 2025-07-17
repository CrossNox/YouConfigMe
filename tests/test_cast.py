"""Test cast functions"""

# pylint: disable=redefined-outer-name
# pylint: disable=missing-function-docstring
# pylint: disable=unused-variable

import pytest
from pytest.cast import to_bool
from youconfigme import Config


@pytest.fixture
def config_dict():
    return Config(
        from_items={
            "yes": {"k1": "yes", "k2": "true", "k4": "1", "k5": "True", "k6": True},
            "no": {
                "k1": "no",
                "k2": "false",
                "k3": "f",
                "k4": "0",
                "k5": "False",
                "k6": False,
            },
        }
    )


def test_to_bool(config_dict):
    """Test to_bool"""
    assert config_dict.yes.k1(cast=to_bool) is True
    assert config_dict.yes.k2(cast=to_bool) is True
    assert config_dict.yes.k3(cast=to_bool) is True
    assert config_dict.yes.k4(cast=to_bool) is True
    assert config_dict.yes.k5(cast=to_bool) is True
    assert config_dict.yes.k6(cast=to_bool) is True

    assert config_dict.no.k1(cast=to_bool) is False
    assert config_dict.no.k2(cast=to_bool) is False
    assert config_dict.no.k3(cast=to_bool) is False
    assert config_dict.no.k4(cast=to_bool) is False
    assert config_dict.no.k5(cast=to_bool) is False
    assert config_dict.no.k6(cast=to_bool) is False


@pytest.mark.mypy_testing
def test_to_bool_types(config_dict) -> None:
    """Test typing"""
    x: bool
    x = config_dict.yes.k1(cast=to_bool)
    x = config_dict.yes.k2(cast=to_bool)
    x = config_dict.yes.k3(cast=to_bool)
    x = config_dict.yes.k4(cast=to_bool)
    x = config_dict.yes.k5(cast=to_bool)
    x = config_dict.yes.k6(cast=to_bool)
