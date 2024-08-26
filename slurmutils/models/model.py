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

__all__ = ["BaseModel", "LineInterface", "format_key", "generate_descriptors"]

import copy
import json
import re
from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, Tuple

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


class LineInterface:
    """Interface for data models that can be constructed from a configuration line."""

    @classmethod
    @abstractmethod
    def from_str(cls, line: str):
        """Construct data model from configuration line."""

    @abstractmethod
    def __str__(self) -> str:
        """Return model as configuration line."""


class BaseModel(ABC):
    """Base model for Slurm data models."""

    def __init__(self, validator=None, /, **kwargs) -> None:
        for k, v in kwargs.items():
            if not hasattr(validator, k):
                raise ModelError(
                    (
                        f"unrecognized argument {k}. "
                        + f"valid arguments are {[opt.name for opt in validator]}"
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

    def dict(self) -> Dict[str, Any]:
        """Return model as dictionary."""
        return copy.deepcopy(self.data)

    def json(self) -> str:
        """Return model as json object."""
        return json.dumps(self.dict())
