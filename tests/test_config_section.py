"""ConfigSection tests"""

# pylint: disable=redefined-outer-name
# pylint: disable=missing-function-docstring

import os

import pytest
from youconfigme import ConfigItemNotFound, ConfigSection


@pytest.fixture
def config_section():
    """Test env var preceding config file.

    Default section (config_section):
        z = 10 (env var)
            z = 0 (config file)
                z = _ (default)
        debussy = 1 (env var)
            debussy = not present, skipped (config file)
                debussy = _ (default)
    """
    os.environ["CONFIG_SECTION_DEBUSSY"] = "1"
    os.environ["CONFIG_SECTION_Z"] = "10"
    yield ConfigSection("config_section", {"z": 0})
    del os.environ["CONFIG_SECTION_DEBUSSY"]
    del os.environ["CONFIG_SECTION_Z"]


def test_to_dict(config_section):
    """Env var before config file."""
    assert config_section.to_dict() == {"z": "10", "debussy": "1"}


def test_val_ex(config_section):
    assert config_section.z() == "10"


def test_val_ex_cast(config_section):
    assert config_section.z(cast=int) == 10


def test_val_ex_def(config_section):
    assert config_section.z(1) == "10"


def test_val_ex_def_cast(config_section):
    assert config_section.z(1, cast=int) == 10


def test_val_nex(config_section):
    with pytest.raises(ConfigItemNotFound):
        config_section.w()


def test_val_nex_def(config_section):
    assert config_section.w(7) == "7"


def test_val_nex_def_cast(config_section):
    assert config_section.w(7, cast=int) == 7


def test_val_nex_ev_ex(config_section):
    assert config_section.DEBUSSY() == "1"


def test_val_nex_ev_ex_cast(config_section):
    assert config_section.DEBUSSY(cast=int) == 1


def test_val_nex_ev_ex_def(config_section):
    assert config_section.DEBUSSY(17) == "1"


def test_val_nex_ev_ex_def_cast(config_section):
    assert config_section.DEBUSSY(17, cast=int) == 1


def test_val_nex_ev_nex(config_section):
    with pytest.raises(ConfigItemNotFound):
        config_section.GAUDI()
