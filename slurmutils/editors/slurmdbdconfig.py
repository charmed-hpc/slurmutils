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

"""Edit slurmdbd.conf files."""

__all__ = ["dump", "dumps", "load", "loads", "edit"]

import logging
import os
from contextlib import contextmanager
from pathlib import Path
from typing import Optional, Union

from ..models import SlurmdbdConfig
from .editor import dumper, loader, set_file_permissions

_logger = logging.getLogger("slurmutils")


@loader
def load(file: Union[str, os.PathLike]) -> SlurmdbdConfig:
    """Load `slurmdbd.conf` data model from slurmdbd.conf file."""
    return loads(Path(file).read_text())


def loads(content: str) -> SlurmdbdConfig:
    """Load `slurmdbd.conf` data model from string."""
    return SlurmdbdConfig.from_str(content)


@dumper
def dump(
    config: SlurmdbdConfig,
    file: Union[str, os.PathLike],
    mode: int = 0o644,
    user: Optional[Union[str, int]] = None,
    group: Optional[Union[str, int]] = None,
) -> None:
    """Dump `slurmdbd.conf` data model into slurmdbd.conf file."""
    Path(file).write_text(dumps(config))
    set_file_permissions(file, mode, user, group)


def dumps(config: SlurmdbdConfig) -> str:
    """Dump `slurmdbd.conf` data model into a string."""
    return str(config)


@contextmanager
def edit(
    file: Union[str, os.PathLike],
    mode: int = 0o644,
    user: Optional[Union[str, int]] = None,
    group: Optional[Union[str, int]] = None,
) -> SlurmdbdConfig:
    """Edit a slurmdbd.conf file.

    Args:
        file: slurmdbd.conf file to edit. An empty config will be created if it does not exist.
        mode: Access mode to apply to the slurmdbd.conf file. (Default: rw-r--r--)
        user: User to set as owner of the slurmdbd.conf file. (Default: $USER)
        group: Group to set as owner of the slurmdbd.conf file. (Default: None)
    """
    if not os.path.exists(file):
        _logger.warning("file %s not found. creating new empty slurmdbd.conf configuration", file)
        config = SlurmdbdConfig()
    else:
        config = load(file)

    yield config
    dump(config, file, mode, user, group)
