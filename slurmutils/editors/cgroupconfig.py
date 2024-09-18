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

"""Edit cgroup.conf files."""

__all__ = ["dump", "dumps", "load", "loads", "edit"]

import logging
import os
from contextlib import contextmanager
from pathlib import Path
from typing import Union

from ..models import  CgroupConfig
from ..models.option import CgroupConfigOptionSet
from .editor import (
    clean,
    dumper,
    loader,
    marshall_content,
    parse_line,
)

_logger = logging.getLogger("slurmutils")


@loader
def load(file: Union[str, os.PathLike]) -> CgroupConfig:
    """Load `cgroup.conf` data model from cgroup.conf file."""
    return loads(Path(file).read_text())


def loads(content: str) -> CgroupConfig:
    """Load `cgroup.conf` data model from string."""
    return _parse(content)


@dumper
def dump(config: CgroupConfig, file: Union[str, os.PathLike]) -> None:
    """Dump `cgroup.conf` data model into cgroup.conf file."""
    Path(file).write_text(dumps(config))


def dumps(config: CgroupConfig) -> str:
    """Dump `cgroup.conf` data model into a string."""
    return _marshall(config)


@contextmanager
def edit(file: Union[str, os.PathLike]) -> CgroupConfig:
    """Edit a cgroup.conf file.

    Args:
        file: Path to cgroup.conf file to edit. If cgroup.conf does
            not exist at the specified file path, it will be created.
    """
    if not os.path.exists(file):
        _logger.warning("file %s not found. creating new empty cgroup.conf configuration", file)
        config = CgroupConfig()
    else:
        config = load(file)

    yield config
    dump(config, file)


def _parse(content: str) -> CgroupConfig:
    """Parse contents of `cgroup.conf`.

    Args:
        content: Contents of `cgroup.conf`.
    """
    data = {}
    lines = content.splitlines()
    for index, line in enumerate(lines):
        config = clean(line)
        if config is None:
            _logger.debug("ignoring line %s at index %s in cgroup.conf", line, index)
            continue

        data.update(parse_line(CgroupConfigOptionSet, config))

    return CgroupConfig.from_dict(data)


def _marshall(config: CgroupConfig) -> str:
    """Marshall `cgroup.conf` data model back into cgroup.conf format.

    Args:
        config: `cgroup.conf` data model to marshall.
    """
    result = []
    result.extend(marshall_content(CgroupConfigOptionSet, config.dict()))
    return "\n".join(result)
