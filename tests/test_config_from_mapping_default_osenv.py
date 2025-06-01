"""Config tests from an ini file defining a default section"""

# pylint: disable=redefined-outer-name
# pylint: disable=missing-function-docstring

import os

import pytest
from youconfigme import Config, ConfigItemNotFound


@pytest.fixture
def config_dict_defs_osenv():
    os.environ["A_K7"] = "7"
    os.environ["K7"] = "11"
    yield Config(
        from_items={"a": {"k1": 1, "k2": 2}, "b": {"k3": 3, "k4": 4}},
        default_section="b",
    )
    del os.environ["A_K7"]
    del os.environ["K7"]


def test_config_from_mapping_env_defs_sa_to_dict(config_dict_defs_osenv):
    assert config_dict_defs_osenv.a.to_dict() == {"k1": "1", "k2": "2", "k7": "7"}


def test_config_from_mapping_env_defs_sb_to_dict(config_dict_defs_osenv):
    with pytest.raises(ConfigItemNotFound):
        config_dict_defs_osenv.b.to_dict()


def test_config_from_mapping_env_defs_to_dict(config_dict_defs_osenv):
    assert config_dict_defs_osenv.to_dict() == {
        "a": {"k1": "1", "k2": "2", "k7": "7"},
        "k3": "3",
        "k4": "4",
    }


def test_config_from_mapping_env_defs_sa_k1(config_dict_defs_osenv):
    assert config_dict_defs_osenv.a.k1() == "1"
    assert config_dict_defs_osenv.a.k1(cast=int) == 1
    assert config_dict_defs_osenv.a.k1(default="z") == "1"
    assert config_dict_defs_osenv.a.k1(default="z", cast=int) == 1


def test_config_from_mapping_env_defs_sa_k2(config_dict_defs_osenv):
    assert config_dict_defs_osenv.a.k2() == "2"
    assert config_dict_defs_osenv.a.k2(cast=int) == 2
    assert config_dict_defs_osenv.a.k2(default="z") == "2"
    assert config_dict_defs_osenv.a.k2(default="z", cast=int) == 2


def test_config_from_mapping_env_defs_sa_k7(config_dict_defs_osenv):
    assert config_dict_defs_osenv.a.k7(default="777") == "7"
    assert config_dict_defs_osenv.a.k7(default="777", cast=int) == 7
    assert config_dict_defs_osenv.a.k7() == "7"
    assert config_dict_defs_osenv.a.k7(cast=int) == 7


def test_config_from_mapping_env_defs_sb(config_dict_defs_osenv):
    with pytest.raises(ConfigItemNotFound):
        config_dict_defs_osenv.b.a()


def test_config_from_mapping_env_defs_defset_k3(config_dict_defs_osenv):
    assert config_dict_defs_osenv.k3() == "3"
    assert config_dict_defs_osenv.k3(cast=int) == 3
    assert config_dict_defs_osenv.k3(default="z") == "3"
    assert config_dict_defs_osenv.k3(default="z", cast=int) == 3


def test_config_from_mapping_env_defs_defset_k4(config_dict_defs_osenv):
    assert config_dict_defs_osenv.k4() == "4"
    assert config_dict_defs_osenv.k4(cast=int) == 4
    assert config_dict_defs_osenv.k4(default="z") == "4"
    assert config_dict_defs_osenv.k4(default="z", cast=int) == 4


def test_config_from_mapping_env_defs_defset_k7(config_dict_defs_osenv):
    assert config_dict_defs_osenv.k7(default="7") == "11"
    assert config_dict_defs_osenv.k7(default="7", cast=int) == 11
    assert config_dict_defs_osenv.k7(cast=int) == 11
    assert config_dict_defs_osenv.k7() == "11"
