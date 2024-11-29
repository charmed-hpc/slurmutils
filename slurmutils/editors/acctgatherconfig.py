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

"""Edit acct_gather.conf file."""

__all__ = ["dump", "dumps", "load", "loads", "edit"]

import logging
import os
from contextlib import contextmanager
from pathlib import Path
from typing import Optional, Union

from ..models import AcctGatherConfig
from .editor import dumper, loader, set_file_permissions

_logger = logging.getLogger("slurmutils")


@loader
def load(file: Union[str, os.PathLike]) -> AcctGatherConfig:
    """Load `acct_gather.conf` data model from acct_gather.conf file."""
    return loads(Path(file).read_text())


def loads(content: str) -> AcctGatherConfig:
    """Load `acct_gather.conf` data model from string."""
    return AcctGatherConfig.from_str(content)


@dumper
def dump(
    config: AcctGatherConfig,
    file: Union[str, os.PathLike],
    mode: int = 0o644,
    user: Optional[Union[str, int]] = None,
    group: Optional[Union[str, int]] = None,
) -> None:
    """Dump `acct_gather.conf` data model into acct_gather.conf file."""
    Path(file).write_text(dumps(config))
    set_file_permissions(file, mode, user, group)


def dumps(config: AcctGatherConfig) -> str:
    """Dump `acct_gather.conf` data model into a string."""
    return str(config)


@contextmanager
def edit(
    file: Union[str, os.PathLike],
    mode: int = 0o644,
    user: Optional[Union[str, int]] = None,
    group: Optional[Union[str, int]] = None,
) -> AcctGatherConfig:
    """Edit a acct_gather.conf file.

    Args:
        file: acct_gather.conf file to edit. An empty config will be created if it does not exist.
        mode: Access mode to apply to the acct_gather.conf file. (Default: rw-r--r--)
        user: User to set as owner of the acct_gather.conf file. (Default: $USER)
        group: Group to set as owner of the acct_gather.conf file. (Default: None)
    """
    if not os.path.exists(file):
        _logger.warning(
            "file %s not found. creating new empty acct_gather.conf configuration", file
        )
        config = AcctGatherConfig()
    else:
        config = load(file)

    yield config
    dump(config, file, mode, user, group)
