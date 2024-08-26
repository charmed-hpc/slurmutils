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
import shlex
from functools import wraps
from os import path
from typing import Any, Dict, List, Tuple

from ..exceptions import EditorError

_logger = logging.getLogger("slurmutils")


def _is_comment(line: str) -> bool:
    """Check if line is a comment."""
    return line.startswith("#")


def _contains_comment(line: str) -> bool:
    """Check if line contains an inline comment."""
    return "#" in line


def _slice_comment(line: str) -> str:
    """Slice inline comment off of line."""
    return line.split("#", maxsplit=1)[0]


def clean(line: str) -> Tuple[str, bool]:
    """Clean line before further processing.

    Returns:
        Returns the cleaned line and False if it should be ignored.
        If True, then the processors should ignore the line.
    """
    if _is_comment(line):
        return "", True

    return (_slice_comment(line) if _contains_comment(line) else line).strip(), False


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
            raise EditorError(
                (
                    f"unable to parse configuration option {k}. "
                    + f"valid configuration options are {[option.name for option in options]}"
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
            raise EditorError(
                (
                    f"unable to marshall configuration option {k}. "
                    + f"valid configuration options are {[option.name for option in options]}"
                )
            )

        marshall = getattr(options, k).marshaller
        result.append(f"{k}={marshall(v) if marshall else v}")

    return result


def loader(func):
    """Wrap function that loads configuration data from file."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        fin = args[0]
        if not path.exists(fin):
            raise FileNotFoundError("could not locate %s", fin)

        _logger.debug("reading contents of %s", fin)
        return func(*args, **kwargs)

    return wrapper


def dumper(func):
    """Wrap function that dumps configuration data to file."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        fout = args[1]
        if path.exists(fout):
            _logger.debug("overwriting current contents of %s", fout)

        _logger.debug("updating contents of %s", fout)
        return func(*args, **kwargs)

    return wrapper
