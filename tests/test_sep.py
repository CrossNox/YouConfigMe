"""Test sep arg."""

# pylint: disable=redefined-outer-name
# pylint: disable=missing-function-docstring

import os

import pytest
from youconfigme import Config


@pytest.fixture
def config_underscore():
    os.environ["A_K1"] = "7"
    os.environ["K4"] = "11"
    yield Config(
        from_items={"a": {"k1": 1, "k2": 2}, "b": {"k3": 3, "k4": 4}},
        default_section="b",
    )
    del os.environ["A_K1"]
    del os.environ["K4"]


@pytest.fixture
def config_dunderscore():
    os.environ["A_K1"] = "7"
    os.environ["A__K1"] = "77"
    os.environ["K4"] = "11"
    yield Config(
        from_items={"a": {"k1": 1, "k2": 2}, "b": {"k3": 3, "k4": 4}},
        default_section="b",
        sep="__",
    )
    del os.environ["A__K1"]
    del os.environ["K4"]


def test_to_dict1(config_underscore):
    assert config_underscore.to_dict() == {
        "k4": "11",
        "k3": "3",
        "a": {"k1": "7", "k2": "2"},
    }


def test_to_dict2(config_dunderscore):
    assert config_dunderscore.to_dict() == {
        "k4": "11",
        "k3": "3",
        "a": {"k1": "77", "k2": "2"},
    }


def test_defsep1(config_underscore):
    assert config_underscore.k4() == "11"


def test_defsep2(config_underscore):
    assert config_underscore.a.k1() == "7"


def test_sep1(config_dunderscore):
    assert config_dunderscore.a.k1() == "77"


def test_sep2(config_dunderscore):
    assert config_dunderscore.k4() == "11"
