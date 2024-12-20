# Copyright 2024 Canonical Ltd.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License version 3 as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Base classes and methods for composing Slurm data models."""

__all__ = [
    "BaseMapping",
    "BaseModel",
    "clean",
    "format_key",
    "generate_descriptors",
    "marshall_content",
    "parse_line",
]

import copy
import json
import re
import shlex
from abc import ABC, abstractmethod
from collections.abc import Callable, Iterable, MutableMapping
from typing import Any

from jsonschema import ValidationError, validate
from typing_extensions import Self

from ..exceptions import ModelError

_acronym = re.compile(r"(?<=[A-Z])(?=[A-Z][a-z])")
_camelize = re.compile(r"(?<=[a-z0-9])(?=[A-Z])")


def format_key(key: str) -> str:
    """Format Slurm configuration keys from SlurmCASe to camelCase.

    Args:
        key: Configuration key to format into camel case.

    Notes:
       Slurm configuration syntax does not follow proper PascalCasing
       format, so we cannot put keys directly through a kebab case converter
       to get the desired format. Some additional processing is needed for
       certain keys before the key can properly camelized.

       For example, without additional preprocessing, the key `CPUs` will
       become `cp-us` if put through a caramelize with being preformatted to `Cpus`.
    """
    if "CPUs" in key:
        key = key.replace("CPUs", "Cpus")
    key = _acronym.sub(r"_", key)
    return _camelize.sub(r"_", key).lower()


def _expand_iter(i: Iterable[Any]) -> list[Any]:
    """Recursively expand a complex iterable with nested Slurm data models.

    Args:
        i: Iterable to expand.
    """
    out = []
    for v in i:
        if issubclass(type(v), BaseModel):
            out.append(_expand_dict(v.dict()))
        elif issubclass(type(v), MutableMapping):
            out.append(_expand_dict(v))
        elif isinstance(v, list | tuple):
            out.append(_expand_iter(v))
        else:
            out.append(v)

    return out


def _expand_dict(d: MutableMapping[str, Any]) -> dict[str, Any]:
    """Recursively expand a complex dictionary with nested Slurm data models.

    Args:
        d: Dictionary to expand.
    """
    out = {}
    for k, v in d.items():
        if issubclass(type(v), BaseModel):
            out.update({k: _expand_dict(v.dict())})
        elif issubclass(type(v), MutableMapping):
            out.update({k: _expand_dict(v)})
        elif isinstance(v, list | tuple):
            out.update({k: _expand_iter(v)})
        else:
            out[k] = v

    return out


def expand(d: MutableMapping[str, Any]) -> dict[str, Any]:
    """Expand a complex dictionary with nested Slurm data models."""
    return _expand_dict(d)


def generate_descriptors(opt: str) -> tuple[Callable, Callable, Callable]:
    """Generate descriptors for retrieving and mutating configuration options.

    Args:
        opt: Configuration option to generate descriptors for.
    """

    def getter(self):
        return self.data.get(opt, None)

    def setter(self, value):
        self.data[opt] = value

    def deleter(self):
        del self.data[opt]

    return getter, setter, deleter


def clean(line: str) -> str | None:
    """Clean line before further processing.

    Returns:
        Line with inline comments removed. `None` if line is a comment.
    """
    return cleaned if (cleaned := line.split("#", maxsplit=1)[0]) != "" else None


def parse_line(options, line: str) -> dict[str, Any]:
    """Parse configuration line.

    Args:
        options: Available options for line.
        line: Configuration line to parse.
    """
    data = {}
    opts = shlex.split(line)  # Use `shlex.split(...)` to preserve quotation strings.
    for opt in opts:
        k, v = opt.split("=", maxsplit=1)
        if not hasattr(options, k):
            raise ModelError(
                (
                    f"unable to parse configuration option {k}. "
                    + f"valid configuration options are {list(options.keys())}"
                )
            )

        parse = getattr(options, k).parser
        data[k] = parse(v) if parse else v

    return data


def marshall_content(options, line: MutableMapping[str, Any]) -> list[str]:
    """Marshall data model content back into configuration line.

    Args:
        options: Available options for line.
        line: Data model to marshall into line.
    """
    result = []
    for k, v in line.items():
        if not hasattr(options, k):
            raise ModelError(
                (
                    f"unable to marshall configuration option {k}. "
                    + f"valid configuration options are {[option.name for option in options]}"
                )
            )

        marshall = getattr(options, k).marshaller
        result.append(f"{k}={marshall(v) if marshall else v}")

    return result


class BaseModel(ABC):
    """Base model for Slurm data models."""

    def __init__(self, validator=None, /, **kwargs) -> None:
        for k, v in kwargs.items():
            if not hasattr(validator, k):
                raise ModelError(
                    (
                        f"unrecognized argument {k}. "
                        + f"valid arguments are {list(validator.keys())}"
                    )
                )

        self.data = kwargs

    def _slice(self, exclude: Iterable[str]) -> dict[str, Any]:
        """Slice the internal data store by excluding specific keys.

        Args:
            exclude: List of keys to exclude from slice.
        """
        return {k: v for k, v in self.data.items() if k not in exclude}

    @classmethod
    def from_dict(cls, data: MutableMapping[str, Any]):
        """Construct new model from dictionary."""
        return cls(**data)

    @classmethod
    def from_json(cls, obj: str):
        """Construct new model from JSON object."""
        data = json.loads(obj)
        return cls.from_dict(data)

    @classmethod
    @abstractmethod
    def from_str(cls, content: str):
        """Construct data model from configuration string."""

    @abstractmethod
    def __str__(self) -> str:
        """Return model as configuration string."""

    def dict(self) -> dict[str, Any]:
        """Return model as dictionary."""
        return copy.deepcopy(self.data)

    def json(self) -> str:
        """Return model as json object."""
        return json.dumps(self.dict())

    def update(self, other) -> None:
        """Update current data model content with content of other data model."""
        self.data.update(other.data)


class BaseMapping(MutableMapping[str, Any], ABC):
    """Base map for Slurm data model mappings."""

    def __init__(self, d: MutableMapping[str, Any] | None = None) -> None:
        if not d:
            self._data = {}
            return

        try:
            d = expand(d)
            validate(d, schema=self._schema)
            self._data = json.loads(json.dumps(d), object_hook=self._decoder)
        except ValidationError as e:
            raise ModelError(e.message)

    @property
    @abstractmethod
    def _schema(self) -> dict[str, Any]:
        """Get data model JSON schema."""

    @property
    @abstractmethod
    def _decoder(self) -> Any:
        """Get data model decoder."""

    @classmethod
    def from_dict(cls, d: MutableMapping[str, Any]) -> Self:
        """Create model from dictionary."""
        return cls(d)

    @classmethod
    def from_json(cls, s: str | bytes | bytearray) -> Self:
        """Create model from JSON object."""
        return cls(json.loads(s))

    def dict(self) -> dict[str, Any]:
        """Return data model mapping as an expanded dictionary object."""
        return expand(self._data)

    def json(self) -> str:
        """Return model mapping as a JSON object."""
        return json.dumps(expand(self._data))

    @abstractmethod
    def __str__(self) -> str:  # noqa D105
        pass

    def __getitem__(self, key: str, /) -> Any:  # noqa D105
        return self._data[key]

    def __setitem__(self, key: str, value: Any, /) -> None:  # noqa D105
        self._data[key] = value

    def __delitem__(self, key: str, /) -> None:  # noqa D105
        del self._data[key]

    def __len__(self) -> int:  # noqa D105
        return len(self._data)

    def __iter__(self) -> Iterable[str]:  # noqa D105
        return iter(self._data)
