"""Test cast functions"""

# pylint: disable=redefined-outer-name
# pylint: disable=missing-function-docstring
# pylint: disable=unused-variable

import pytest
from youconfigme import Config
from youconfigme.cast import to_bool

# fmt: off


@pytest.fixture
def config_dict() -> Config:
    return Config(
        from_items={
            "yes": {
                "k1": "yes",
                "k2": "true",
                "k3": "t",
                "k4": "1",
                "k5": "True",
                "k6": True,
            },
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


def test_to_bool(config_dict: Config) -> None:
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
def test_to_bool_types(config_dict: Config) -> None:
    """Test typing"""
    x: bool = config_dict.yes.k1(cast=to_bool)


@pytest.mark.mypy_testing
def test_to_bool_bad_types(config_dict: Config) -> None:
    """Test typing"""
    x: str = config_dict.yes.k1(cast=to_bool)  # E: Incompatible types in assignment (expression has type "bool", variable has type "str")  [assignment]
