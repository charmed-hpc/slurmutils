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

"""Macros for Slurm workload manager data models."""

import copy
import functools
import inspect
import json
from abc import ABC, abstractmethod
from types import MappingProxyType
from typing import Any, Callable, Dict, NamedTuple, Optional


# Simple type checking decorator; used to verify input into Slurm data models
# without needing every method to contain an `if isinstance(...)` block.
def assert_type(*typed_args, **typed_kwargs):
    """Check the type of args and kwargs passed to a function/method."""

    def decorator(func: Callable):
        sig = inspect.signature(func)
        bound_types = sig.bind_partial(*typed_args, **typed_kwargs).arguments

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            bound_values = sig.bind(*args, **kwargs).arguments
            for name in bound_types.keys() & bound_values.keys():
                if not isinstance(bound_values[name], bound_types[name]):
                    raise TypeError(f"{bound_values[name]} is not {bound_types[name]}.")

            return func(*args, **kwargs)

        return wrapper

    return decorator


# Generate descriptors for Slurm configuration knobs.
# These descriptors are used for retrieving configuration values but
# also preserve the integrity of Slurm's loose pascal casing.
# The descriptors will use an internal _register dictionary to
# manage the parsed configuration knobs.
def base_descriptors(knob: str):
    """Generate descriptors for accessing configuration knob values.

    Args:
        knob: Configuration knob to generate descriptors for.
    """

    def getter(self):
        return self._register.get(knob, None)

    def setter(self, value):
        self._register[knob] = value

    def deleter(self):
        try:
            del self._register[knob]
        except KeyError:
            pass

    return getter, setter, deleter


# Nodes, FrontendNodes, DownNodes, NodeSets, and Partitions are represented
# as a Python dictionary with a primary key and nested dictionary when
# parsed in from the slurm.conf configuration file:
#
# {"node_1": {"NodeHostname": ..., "NodeAddr": ..., "CPUs", ...}}
#
# Since these models are parsed in this way, they need special descriptors
# for accessing the primary key (e.g. the NodeName), and sub values in the
# nested dictionary.
def primary_key_descriptors():
    """Generate descriptors for accessing a configuration knob key."""

    def getter(self):
        # There will only be a single key in _register,
        # so it's okay to return the first index. If the
        # primary key doesn't exist, return None.
        try:
            return list(self._register.keys())[0]
        except IndexError:
            return None

    def setter(self, value):
        old_primary = list(self._register.keys())[0]
        if old_primary:
            self._register[value] = self._register.pop(old_primary, {})
        else:
            self._register[value] = {}

    def deleter(self):
        try:
            primary_key = list(self._register.keys())[0]
            del self._register[primary_key]
        except IndexError:
            pass

    return getter, setter, deleter


def nested_descriptors(knob: str, knob_key_alias: str):
    """Generate descriptors for accessing a nested configuration knob.

    Args:
        knob: Nested configuration knob to generate descriptors for.
        knob_key_alias: Alias of knob key that needs to pbe defined in
            register before accessing nested configuration knobs.
    """

    def getter(self):
        try:
            primary_key = list(self._register.keys())[0]
            return self._register[primary_key].get(knob, None)
        except IndexError:
            raise KeyError(f"{knob_key_alias} must be defined before {knob} can be accessed.")

    def setter(self, value):
        try:
            primary_key = list(self._register.keys())[0]
            self._register[primary_key][knob] = value
        except IndexError:
            raise KeyError(f"{knob_key_alias} must be defined before {knob} can be accessed.")

    def deleter(self):
        try:
            primary_key = list(self._register.keys())[0]
            del self._register[primary_key][knob]
        except IndexError:
            raise KeyError(f"{knob_key_alias} must be defined before {knob} can be accessed.")
        except KeyError:
            pass

    return getter, setter, deleter


# Callbacks are used during parsing and marshalling for performing
# extra processing on specific configuration knob values. They contain callables
# that accept a single argument. Makes it easy to convert Python objects to Slurm
# configuration values and vice versa.
class Callback(NamedTuple):
    """Object for invoking callables on Slurm configuration knobs during parsing/marshalling.

    Possible callables:
        parse: Invoked when value is being parsed in from configuration file.
        marshal: Invoked when value is being marshalled into configuration file.
    """

    parse: Optional[Callable[[Any], Any]] = None
    marshal: Optional[Callable[[Any], Any]] = None


# Common parsing/marshalling callbacks for Slurm configuration values.
# Arrays are denoted using comma/colon separators. Maps are denoted as
# key1=value,key2=value,bool. Booleans are mapped by the inclusion of
# the keyword in maps. So key1=value,key2 would equate to:
#
# {
#   "key1": "value",
#   "key2": True,
# }
@functools.singledispatch
def _slurm_dict(v):
    raise TypeError(f"Expected str or dict, not {type(v)}")


@_slurm_dict.register
def _(v: str):
    """Convert Slurm dictionary to Python dictionary."""
    result = {}
    for val in v.split(","):
        if "=" in val:
            sub_opt, sub_val = val.split("=", 1)
            result.update({sub_opt: sub_val})
        else:
            result.update({val: True})

    return result


@_slurm_dict.register
def _(v: dict):
    """Convert Python dictionary to Slurm dictionary."""
    result = []
    for sub_opt, sub_val in v.items():
        if not isinstance(sub_val, bool):
            result.append(f"{sub_opt}={sub_val}")
        elif sub_val:
            result.append(sub_opt)

    return ",".join(result)


CommaSeparatorCallback = Callback(lambda v: v.split(","), lambda v: ",".join(v))
ColonSeparatorCallback = Callback(lambda v: v.split(":"), lambda v: ":".join(v))
SlurmDictCallback = Callback(_slurm_dict, _slurm_dict)
ReasonCallback = Callback(None, lambda v: f'"{v}"')


# All Slurm data models should inherit from this abstract parent class.
# The class provides method definitions for common operations and
# requires models to specify callbacks so that models can be treated
# generically when parsing and marshalling rather than having an infinite if-else tree.
class BaseModel(ABC):
    """Abstract base class for Slurm-related data models."""

    def __init__(self, **kwargs):
        self._register = kwargs

    def __repr__(self):
        return (
            f"{self.__class__.__name__}"
            f"({', '.join(f'{k}={v}' for k, v in self._register.items())})"
        )

    @property
    @abstractmethod
    def primary_key(self) -> Optional[str]:
        """Primary key for data model.

        A primary key is required for data models that have a unique identifier
        to preserve the integrity of the Slurm configuration syntax. For example,
        for compute nodes, the primary key would be the node name `NodeName`. Node
        name can be used nicely for identifying nodes in maps, but it is difficult to
        carry along the NodeName key inside the internal register of the class.

        _primary_key is used to track what the Slurm configuration key should be for
        unique identifiers. Without this "protected" attribute, we would likely need
        to write a custom parser for each data model. The generic model marshaller can
        detect this attribute and marshal the model accordingly.
        """
        pass

    @property
    @abstractmethod
    def callbacks(self) -> MappingProxyType:
        """Store callbacks.

        This map will be queried during parsing and marshalling to determine if
        a configuration value needs any further processing. Each model class will
        need to define the callbacks specific to its configuration knobs. Every model
        class should declare whether it has callbacks or not.

        Callbacks should be MappingProxyType (read-only dict) to prevent any accidental
        mutation of callbacks used during parsing and marshalling.
        """
        pass

    def dict(self) -> Dict:
        """Get model in dictionary form.

        Returns a deep copy of model's internal register. The deep copy is needed
        because assigned variables all point to the same dictionary in memory. Without the
        deep copy, operations performed on the returned dictionary could cause unintended
        mutations in the internal register.
        """
        return copy.deepcopy(self._register)

    def json(self) -> str:
        """Get model as JSON object."""
        return json.dumps(self._register)
