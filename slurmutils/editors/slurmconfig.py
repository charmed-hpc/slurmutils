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

"""Edit slurm.conf files."""

__all__ = ["dump", "dumps", "load", "loads", "edit"]

import logging
import os
from contextlib import contextmanager
from pathlib import Path
from typing import Union

from ..models import SlurmConfig
from .editor import dumper, loader

_logger = logging.getLogger("slurmutils")


@loader
def load(file: Union[str, os.PathLike]) -> SlurmConfig:
    """Load `slurm.conf` data model from slurm.conf file."""
    return loads(Path(file).read_text())


def loads(content: str) -> SlurmConfig:
    """Load `slurm.conf` data model from string."""
    return SlurmConfig.from_str(content)


@dumper
def dump(config: SlurmConfig, file: Union[str, os.PathLike]) -> None:
    """Dump `slurm.conf` data model into slurm.conf file."""
    Path(file).write_text(dumps(config))


def dumps(config: SlurmConfig) -> str:
    """Dump `slurm.conf` data model into a string."""
    return str(config)


@contextmanager
def edit(file: Union[str, os.PathLike]) -> SlurmConfig:
    """Edit a slurm.conf file.

    Args:
        file: Path to slurm.conf file to edit. If slurm.conf does
            not exist at the specified file path, it will be created.
    """
    if not os.path.exists(file):
        _logger.warning("file %s not found. creating new empty slurm.conf configuration", file)
        config = SlurmConfig()
    else:
        config = load(file)

    yield config
    dump(config, file)
