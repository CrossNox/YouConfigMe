"""Config tests from an ini file defining a default section"""
# pylint: disable=redefined-outer-name
# pylint: disable=missing-function-docstring

import tempfile

import pytest

from youconfigme import Config, ConfigItemNotFound


@pytest.fixture
def config_from_tempfile_defs():
    config_string = """[a]
k1=1
k2=2

[b]
k3=3
k4=4
"""
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    with open(temp_file.name, 'w') as f:
        f.write(config_string)

    return Config(from_items=temp_file.name, default_section='b')


def test_config_from_tempfile_defs_sa_to_dict(config_from_tempfile_defs):
    assert config_from_tempfile_defs.a.to_dict() == {'k1': '1', 'k2': '2'}


def test_config_from_tempfile_defs_sb_to_dict(config_from_tempfile_defs):
    with pytest.raises(ConfigItemNotFound):
        config_from_tempfile_defs.b.to_dict()


def test_config_from_tempfile_defs_to_dict(config_from_tempfile_defs):
    assert config_from_tempfile_defs.to_dict() == {
        'a': {'k1': '1', 'k2': '2'},
        'k3': '3',
        'k4': '4',
    }


def test_config_from_tempfile_defs_sa_k1(config_from_tempfile_defs):
    assert config_from_tempfile_defs.a.k1() == '1'
    assert config_from_tempfile_defs.a.k1(cast=int) == 1
    assert config_from_tempfile_defs.a.k1(default='z') == '1'
    assert config_from_tempfile_defs.a.k1(default='z', cast=int) == 1


def test_config_from_tempfile_defs_sa_k2(config_from_tempfile_defs):
    assert config_from_tempfile_defs.a.k2() == '2'
    assert config_from_tempfile_defs.a.k2(cast=int) == 2
    assert config_from_tempfile_defs.a.k2(default='z') == '2'
    assert config_from_tempfile_defs.a.k2(default='z', cast=int) == 2


def test_config_from_tempfile_defs_sa_k7(config_from_tempfile_defs):
    assert config_from_tempfile_defs.a.k7(default='7') == '7'
    assert config_from_tempfile_defs.a.k7(default='7', cast=int) == 7


def test_config_from_tempfile_defs_sa_k7_raise(config_from_tempfile_defs):
    with pytest.raises(ConfigItemNotFound):
        config_from_tempfile_defs.a.k7()


def test_config_from_tempfile_defs_sb(config_from_tempfile_defs):
    with pytest.raises(ConfigItemNotFound):
        config_from_tempfile_defs.b.a()


def test_config_from_tempfile_defs_defset_k3(config_from_tempfile_defs):
    assert config_from_tempfile_defs.k3() == '3'
    assert config_from_tempfile_defs.k3(cast=int) == 3
    assert config_from_tempfile_defs.k3(default='z') == '3'
    assert config_from_tempfile_defs.k3(default='z', cast=int) == 3


def test_config_from_tempfile_defs_defset_k4(config_from_tempfile_defs):
    assert config_from_tempfile_defs.k4() == '4'
    assert config_from_tempfile_defs.k4(cast=int) == 4
    assert config_from_tempfile_defs.k4(default='z') == '4'
    assert config_from_tempfile_defs.k4(default='z', cast=int) == 4


def test_config_from_tempfile_defs_defset_k7(config_from_tempfile_defs):
    assert config_from_tempfile_defs.k7(default='7') == '7'
    assert config_from_tempfile_defs.k7(default='7', cast=int) == 7


def test_config_from_tempfile_defs_defset_k7_raise(config_from_tempfile_defs):
    with pytest.raises(ConfigItemNotFound):
        config_from_tempfile_defs.k7()
