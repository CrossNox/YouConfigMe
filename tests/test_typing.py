"""Type checking tests for youconfigme using pytest-mypy-testing."""

# pylint: disable=redefined-outer-name
# pylint: disable=missing-function-docstring
# pylint: disable=unused-variable

from typing import Any, Dict, List

import pytest
from youconfigme import Config, ConfigSection

# fmt: off


@pytest.mark.mypy_testing
def test_correct_basic_usage() -> None:
    """Test correct basic usage - should produce no errors."""
    config = Config(from_items={"db": {"host": "localhost", "port": "5432"}})

    # These should all work without errors
    host: str = config.db.host()
    assert host == "localhost"
    port_str: str = config.db.port()
    assert port_str == "5432"
    port_int: int = config.db.port(cast=int)
    assert port_int == 5432

    # With defaults
    timeout: str = config.db.timeout(default="30")
    assert timeout == "30"
    timeout_int: int = config.db.timeout(default="30", cast=int)
    assert timeout_int == 5432
    timeout_int_2: int = config.db.timeout(default=30, cast=int)
    assert timeout_int_2 == 5432

    # Correct casting functions
    def to_int(value: str) -> int:
        return int(value)

    timeout_int_3: int = config.db.port(default="30", cast=to_int)
    assert timeout_int_3 == 5432
    timeout_int_4: int = config.db.port(default=30, cast=to_int)
    assert timeout_int_4 == 5432
    timeout_int_5: int = config.db.port(cast=to_int)
    assert timeout_int_5 == 5432


@pytest.mark.mypy_testing
def test_wrong_type_assignment_without_cast() -> None:
    """Test wrong type assignment without cast - should produce error."""
    config = Config(from_items={"test": {"value": "123"}})

    # This should produce a type error
    wrong: int = config.test.value()  # type: ignore  # E: Incompatible types in assignment (expression has type "str", variable has type "int")  [assignment]
    assert wrong == "123"  # type: ignore


@pytest.mark.mypy_testing
def test_invalid_cast_function_signature() -> None:
    """Test cast function with wrong input type - should produce error."""
    config = Config(from_items={"test": {"value": "123"}})

    # Cast function should take str, not int
    def bad_cast(value: int) -> str:
        return str(value)

    # This should produce error about incompatible argument type
    result = config.test.value(cast=bad_cast)  # type: ignore  # E: Argument "cast" to "__call__" of "ConfigAttribute" has incompatible type "Callable[[int], str]"; expected "Callable[[str], str]"  [arg-type]

    assert result == "123"


@pytest.mark.mypy_testing
def test_cast_return_type_mismatch() -> None:
    """Test mismatch between cast return type and variable type."""
    config = Config(from_items={"test": {"items": "a,b,c"}})

    def parse_to_list(value: str) -> List[str]:
        return value.split(",")

    # Expecting List[int] but cast returns List[str]
    numbers: List[int] = config.test.items(cast=parse_to_list)  # type: ignore  # E: Incompatible types in assignment (expression has type "List[str]", variable has type "List[int]")  [assignment]
    assert numbers == ["a", "b", "c"]  # type: ignore


@pytest.mark.mypy_testing
def test_bad_default_type_without_cast() -> None:
    """Test that default without cast doesn't convert types."""
    config = Config(from_items={})

    # Default is string "100", without cast it stays string
    port: int = config.server.port(default="100")  # type: ignore  # E: Incompatible types in assignment (expression has type "str", variable has type "int")  [assignment]
    assert port == "100"  # type: ignore

    # This works because we use cast
    port_ok: int = config.server.port(default="100", cast=int)
    assert port_ok == 100


@pytest.mark.mypy_testing
def test_correct_custom_cast_functions() -> None:
    """Test various custom cast functions work correctly."""
    config = Config(from_items={
        "app": {
            "debug": "true",
            "features": "auth,api,admin",
            "max_connections": "100"
        }
    })

    def str_to_bool(value: str) -> bool:
        return value.lower() in ("true", "1", "yes")

    def str_to_list(value: str) -> List[str]:
        return [item.strip() for item in value.split(",")]

    # These should all type check correctly
    debug: bool = config.app.debug(cast=str_to_bool)
    assert debug is True
    features: List[str] = config.app.features(cast=str_to_list)
    assert features == ["auth", "api", "admin"]
    connections: int = config.app.max_connections(cast=int)
    assert connections == 100


@pytest.mark.mypy_testing
def test_config_section_typing() -> None:
    """Test ConfigSection type and methods."""
    config = Config(from_items={"cache": {"ttl": "3600", "size": "1000"}})

    # ConfigSection access
    cache_section: ConfigSection = config.cache

    # to_dict returns Dict[str, str]
    cache_dict: Dict[str, str] = cache_section.to_dict()
    assert cache_dict == {"cache_ttl": "3600", "cache_size": "1000"}

    # Wrong type for to_dict
    wrong_dict: Dict[str, int] = cache_section.to_dict()  # type: ignore  # E: Incompatible types in assignment (expression has type "dict[str, str]", variable has type "dict[str, int]")  [assignment]
    assert wrong_dict == {"cache_ttl": "3600", "cache_size": "1000"}  # type: ignore


@pytest.mark.mypy_testing
def test_config_to_dict_return_type() -> None:
    """Test Config.to_dict() return type."""
    config = Config(from_items={
        "server": {"host": "0.0.0.0", "port": "8080"},
        "db": {"name": "mydb"}
    })

    # to_dict returns Dict[str, str]
    config_dict: Dict[str, str] = config.to_dict()
    assert config_dict == {"server_host": "0.0.0.0", "server_port": "8080", "db_name": "mydb"}

    # This is too wide
    wide_dict: Dict[str, Any] = config.to_dict()  # E: Incompatible types in assignment (expression has type "Dict[str, Any]", variable has type "Dict[str, str]")  [assignment]
    assert wide_dict == {"server_host": "0.0.0.0", "server_port": "8080", "db_name": "mydb"}
