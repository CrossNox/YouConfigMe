"""Type stubs for youconfigme"""

import logging
from pathlib import Path
from typing import (Any, Callable, Dict, List, Mapping, Optional, TypeVar,
                    Union, overload)

T = TypeVar("T")

DEFAULT_SECTION: str
INI_FILE: str
DEFAULT_SEP: str

def config_logger(name: str) -> logging.Logger: ...

class ConfigItemNotFound(Exception): ...

class ConfigAttribute:
    name: str
    value: Optional[str]
    section_name: Optional[str]
    env_str: str
    __env: Optional[str]

    def __init__(
        self,
        name: str,
        value: Optional[Any],
        section_name: Optional[str],
        sep: str = ...,
    ) -> None: ...
    @overload
    def __call__(
        self, default: None = ..., cast: None = ..., from_pass: bool = ...
    ) -> str: ...
    @overload
    def __call__(self, default: T, cast: None = ..., from_pass: bool = ...) -> str: ...
    @overload
    def __call__(
        self, default: None = ..., cast: Callable[[str], T] = ..., from_pass: bool = ...
    ) -> T: ...
    @overload
    def __call__(
        self, default: Any, cast: Callable[[str], T] = ..., from_pass: bool = ...
    ) -> T: ...

class ConfigSection:
    name: str
    items: Dict[str, Any]
    sep: str
    prefix: str

    def __init__(
        self, name: str, items: Optional[Mapping[str, Any]], sep: str = ...
    ) -> None: ...
    def __getattr__(self, val: str) -> ConfigAttribute: ...
    def __call__(
        self, default: Optional[Any] = ..., cast: Optional[Callable[[str], Any]] = ...
    ) -> Any: ...
    def to_dict(self) -> Dict[str, str]: ...

FromItemsType = Union[str, Path, Mapping[str, Any], None]

class Config:
    sep: str
    default_section: str
    fake_default_section: str
    config_sections: List[str]
    config_attributes: List[str]

    def __init__(
        self,
        from_items: FromItemsType = ...,
        default_section: str = ...,
        sep: str = ...,
    ) -> None: ...
    def __getattr__(self, name: str) -> ConfigSection: ...
    def to_dict(self) -> Dict[str, Any]: ...
    def to_dotenv(self) -> str: ...

class AutoConfig(Config):
    def __init__(
        self, max_up_levels: int = ..., filename: str = ..., sep: str = ...
    ) -> None: ...
