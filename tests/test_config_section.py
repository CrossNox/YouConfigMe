"""ConfigSection tests"""
# pylint: disable=redefined-outer-name
# pylint: disable=missing-function-docstring

import os

import pytest

from youconfigme import ConfigItemNotFound, ConfigSection


@pytest.fixture
def config_section():
    os.environ["CONFIG_SECTION_DEBUSSY"] = "1"
    os.environ['config_section_z'] = '10'
    yield ConfigSection('config_section', {'z': 0})
    del os.environ["CONFIG_SECTION_DEBUSSY"]
    del os.environ['config_section_z']


def test_to_dict(config_section):
    assert config_section.to_dict() == {'z': '0', 'DEBUSSY': '1'}


def test_val_ex(config_section):
    assert config_section.z() == '0'


def test_val_ex_cast(config_section):
    assert config_section.z(cast=int) == 0


def test_val_ex_def(config_section):
    assert config_section.z(1) == '0'


def test_val_ex_def_cast(config_section):
    assert config_section.z(1, cast=int) == 0


def test_val_nex(config_section):
    with pytest.raises(ConfigItemNotFound):
        config_section.w()


def test_val_nex_def(config_section):
    assert config_section.w(7) == '7'


def test_val_nex_def_cast(config_section):
    assert config_section.w(7, cast=int) == 7


def test_val_nex_ev_ex(config_section):
    assert config_section.DEBUSSY() == '1'


def test_val_nex_ev_ex_cast(config_section):
    assert config_section.DEBUSSY(cast=int) == 1


def test_val_nex_ev_ex_def(config_section):
    assert config_section.DEBUSSY(17) == '17'


def test_val_nex_ev_ex_def_cast(config_section):
    assert config_section.DEBUSSY(17, cast=int) == 17


def test_val_nex_ev_nex(config_section):
    with pytest.raises(ConfigItemNotFound):
        config_section.GAUDI()
