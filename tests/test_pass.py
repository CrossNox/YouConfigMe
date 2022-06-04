"""Test getting from pass."""
# pylint: disable=redefined-outer-name
# pylint: disable=missing-function-docstring

import os
import subprocess

import pytest
from youconfigme import Config


@pytest.fixture
def config_underscore():
    subprocess.run(["pass", "generate", "--force", "ycm_test"], check=True)
    pwd = (
        subprocess.run(["pass", "ycm_test"], capture_output=True, check=True)
        .stdout.decode()
        .strip()
    )
    os.environ["A_K1"] = "ycm_test"
    os.environ["K4"] = "ycm_test"
    yield pwd, Config(
        from_items={"a": {"k1": 1, "k2": "ycm_test"}, "b": {"k3": "ycm_test", "k4": 4}},
        default_section="b",
    )
    del os.environ["A_K1"]
    del os.environ["K4"]
    subprocess.run(["pass", "rm", "--force", "ycm_test"], check=True)


def test_k1(config_underscore):
    pwd, cfg = config_underscore
    assert cfg.a.k1(from_pass=True) == pwd


def test_k2(config_underscore):
    pwd, cfg = config_underscore
    assert cfg.a.k2(from_pass=True) == pwd


def test_k3(config_underscore):
    pwd, cfg = config_underscore
    assert cfg.k3(from_pass=True) == pwd


def test_k4(config_underscore):
    pwd, cfg = config_underscore
    assert cfg.k4(from_pass=True) == pwd
