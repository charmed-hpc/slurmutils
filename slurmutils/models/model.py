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
from typing import Any, Callable, Dict, List, Optional, Tuple

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


def generate_descriptors(opt: str) -> Tuple[Callable, Callable, Callable]:
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


def clean(line: str) -> Optional[str]:
    """Clean line before further processing.

    Returns:
        Line with inline comments removed. `None` if line is a comment.
    """
    return cleaned if (cleaned := line.split("#", maxsplit=1)[0]) != "" else None


def parse_line(options, line: str) -> Dict[str, Any]:
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


def marshall_content(options, line: Dict[str, Any]) -> List[str]:
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

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
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

    def dict(self) -> Dict[str, Any]:
        """Return model as dictionary."""
        return copy.deepcopy(self.data)

    def json(self) -> str:
        """Return model as json object."""
        return json.dumps(self.dict())

    def update(self, other) -> None:
        """Update current data model content with content of other data model."""
        self.data.update(other.data)
