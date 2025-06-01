"""Test getting from pass."""

# pylint: disable=redefined-outer-name
# pylint: disable=missing-function-docstring

import os
from unittest.mock import patch

import pytest
from youconfigme import Config

PASS = "oijfoijsdfjoifoij"


@pytest.fixture
def config_underscore():
    os.environ["A_K1"] = "ycm_test"
    os.environ["K4"] = "ycm_test"
    yield Config(
        from_items={"a": {"k1": 1, "k2": "ycm_test"}, "b": {"k3": "ycm_test", "k4": 4}},
        default_section="b",
    )
    del os.environ["A_K1"]
    del os.environ["K4"]


@patch("youconfigme.getpass.subprocess.run")
def test_k1(mock_run, config_underscore):
    mock_run.return_value.stdout.decode.return_value.strip.return_value = PASS
    cfg = config_underscore
    assert cfg.a.k1(from_pass=True) == PASS


@patch("youconfigme.getpass.subprocess.run")
def test_k2(mock_run, config_underscore):
    mock_run.return_value.stdout.decode.return_value.strip.return_value = PASS
    cfg = config_underscore
    assert cfg.a.k2(from_pass=True) == PASS


@patch("youconfigme.getpass.subprocess.run")
def test_k3(mock_run, config_underscore):
    mock_run.return_value.stdout.decode.return_value.strip.return_value = PASS
    cfg = config_underscore
    assert cfg.k3(from_pass=True) == PASS


@patch("youconfigme.getpass.subprocess.run")
def test_k4(mock_run, config_underscore):
    mock_run.return_value.stdout.decode.return_value.strip.return_value = PASS
    cfg = config_underscore
    assert cfg.k4(from_pass=True) == PASS
