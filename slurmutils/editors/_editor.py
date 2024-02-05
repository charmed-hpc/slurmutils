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

"""Base methods for Slurm workload manager configuration file editors."""

import logging
import re
import shlex
from collections import deque
from os import PathLike
from pathlib import Path
from typing import Deque, Dict, List, Optional, Set, Union

from slurmutils.exceptions import EditorError

_logger = logging.getLogger(__name__)


def dump_base(content, file: Union[str, PathLike], marshaller):
    """Dump configuration into file using provided marshalling function.

    Do not use this function directly.
    """
    if (loc := Path(file)).exists():
        _logger.warning("Overwriting contents of %s file located at %s.", loc.name, loc)

    _logger.debug("Marshalling configuration into %s file located at %s.", loc.name, loc)
    return loc.write_text(marshaller(content), encoding="ascii")


def dumps_base(content, marshaller) -> str:
    """Dump configuration into Python string using provided marshalling function.

    Do not use this function directly.
    """
    return marshaller(content)


def load_base(file: Union[str, PathLike], parser):
    """Load configuration from file using provided parsing function.

    Do not use this function directly.
    """
    if (file := Path(file)).exists():
        _logger.debug("Parsing contents of %s located at %s.", file.name, file)
        config = file.read_text(encoding="ascii")
        return parser(config)
    else:
        msg = "Unable to locate file"
        _logger.error(msg + " %s.", file)
        raise FileNotFoundError(msg + f" {file}")


def loads_base(content: str, parser):
    """Load configuration from Python String using provided parsing function.

    Do not use this function directly.
    """
    return parser(content)


# Helper functions for parsing and marshalling Slurm configuration data.

_loose_pascal_filter = re.compile(r"(.)([A-Z][a-z]+)")
_snakecase_convert = re.compile(r"([a-z0-9])([A-Z])")


def _pascal2snake(v: str) -> str:
    """Convert string in loose PascalCase to snakecase.

    This private method takes in Slurm configuration knob keys and converts
    them to snakecase. The returned snakecase representation is used to
    dynamically access Slurm data model attributes and retrieve callbacks.
    """
    # The precompiled regex filters do a good job of converting Slurm's
    # loose PascalCase to snakecase, however, there are still some tokens
    # that slip through such as `CPUs`. This filter identifies those problematic
    # tokens and converts them into tokens that can be easily processed by the
    # compiled regex expressions.
    if "CPUs" in v:
        v = v.replace("CPUs", "Cpus")
    holder = _loose_pascal_filter.sub(r"\1_\2", v)
    return _snakecase_convert.sub(r"\1_\2", holder).lower()


def clean(config: Deque[str]) -> Deque[str]:
    """Clean loaded configuration file before parsing.

    Cleaning tasks include:
      1. Stripping away comments (#) in configuration. Slurm does not
         support octothorpes in strings; only for inline and standalone
         comments. **Do not use** octothorpes in Slurm configuration knob
         values as Slurm will treat anything proceeding an octothorpe as a comment.
      2. Strip away any extra whitespace at the end of each line.

    Args:
        config: Loaded configuration file. Split by newlines.
    """
    processed = deque()
    while config:
        line = config.popleft()
        if line.startswith("#"):
            # Skip comment lines as they're not necessary for configuration.
            continue
        elif "#" in line:
            # Slice off inline comment and strip away extra whitespace.
            processed.append(line[: line.index("#")].strip())
        else:
            processed.append(line.strip())

    return processed


def header(msg: str) -> str:
    """Generate header for marshalled configuration file.

    Args:
        msg: Message to put into header.
    """
    return "#\n" + "".join(f"# {line}\n" for line in msg.splitlines()) + "#\n"


def parse_repeating_config(__key, __value, pocket: Dict) -> None:
    """Parse `slurm.conf` configuration knobs with keys that can repeat.

    Args:
        __key: Configuration knob key that can repeat.
        __value: Value of the current configuration knob.
        pocket: Dictionary to add parsed configuration knob to.
    """
    if __key not in pocket:
        pocket[__key] = [__value]
    else:
        pocket[__key].append(__value)


def parse_model(line: str, pocket: Union[Dict, List], model) -> None:
    """Parse configuration knobs based on Slurm models.

    Model callbacks will be used for invoking special
    parsing if required for the configuration value in line.

    Args:
         line: Configuration line to parse.
         pocket: Dictionary to add parsed configuration knob to.
         model: Slurm data model to use for invoking callbacks and validating knob keys.
    """
    holder = {}
    for token in shlex.split(line):  # Use `shlex.split(...)` to preserve quotation blocks.
        # Word in front of the first `=` denotes the parent configuration knob key.
        option, value = token.split("=", maxsplit=1)
        if hasattr(model, attr := _pascal2snake(option)):
            if attr in model.callbacks and (callback := model.callbacks[attr].parse) is not None:
                holder.update({option: callback(value)})
            else:
                holder.update({option: value})
        else:
            raise EditorError(
                f"{option} is not a valid configuration option for {model.__name__}."
            )

    # Use temporary model object to update pocket with a Python dictionary
    # in the format that we want the dictionary to be.
    if isinstance(pocket, list):
        pocket.append(model(**holder).dict())
    else:
        pocket.update(model(**holder).dict())


def marshal_model(
    model, ignore: Optional[Set] = None, inline: bool = False
) -> Union[List[str], str]:
    """Marshal a Slurm model back into its Slurm configuration syntax.

    Args:
        model: Slurm model object to marshal into Slurm configuration syntax.
        ignore: Set of keys to ignore on model object when marshalling. Useful for models that
            have child models under certain keys that are directly handled. Default is None.
        inline: If True, marshal object into single line rather than multiline. Default is False.
    """
    marshalled = []
    if ignore is None:
        # Create an empty set if not ignores are specified. Prevents us from needing to
        # rely on a mutable default in the function signature.
        ignore = set()

    if primary_key := model.primary_key:
        attr = _pascal2snake(primary_key)
        primary_value = getattr(model, attr)
        data = {primary_key: primary_value, **model.dict()[primary_value]}
    else:
        data = model.dict()

    for option, value in data.items():
        if option not in ignore:
            if hasattr(model, attr := _pascal2snake(option)):
                if (
                    attr in model.callbacks
                    and (callback := model.callbacks[attr].marshal) is not None
                ):
                    value = callback(value)

                marshalled.append(f"{option}={value}")
            else:
                raise EditorError(
                    f"{option} is not a valid configuration option for {model.__class__.__name__}."
                )
        else:
            _logger.debug("Ignoring option %s. Option is present in ignore set %s", option, ignore)

    if inline:
        # Whitespace is the separator in Slurm configuration syntax.
        marshalled = " ".join(marshalled) + "\n"
    else:
        # Append newline character so that each configuration is on its own line.
        marshalled = [line + "\n" for line in marshalled]

    return marshalled
