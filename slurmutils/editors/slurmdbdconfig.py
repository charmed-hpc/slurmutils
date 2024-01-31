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

import functools
import os
from collections import deque
from contextlib import contextmanager
from datetime import datetime
from typing import Union

from slurmutils.models import SlurmdbdConfig

from ._editor import (
    clean,
    dump_base,
    dumps_base,
    header,
    load_base,
    loads_base,
    marshal_model,
    parse_model,
)


def _marshaller(config: SlurmdbdConfig) -> str:
    """Marshal Python object into slurmdbd.conf configuration file.

    Args:
        config: `SlurmdbdConfig` object to convert to slurmdbd.conf configuration file.
    """
    marshalled = [header(f"`slurmdbd.conf` file generated at {datetime.now()} by slurmutils.")]
    marshalled.extend(marshal_model(config))

    return "".join(marshalled)


def _parser(config: str) -> SlurmdbdConfig:
    """Parse slurmdbd.conf configuration file into Python object.

    Args:
        config: Content of slurmdbd.conf configuration file.
    """
    slurmdbd_conf = {}

    config = clean(deque(config.splitlines()))
    while config:
        line = config.popleft()
        parse_model(line, pocket=slurmdbd_conf, model=SlurmdbdConfig)

    return SlurmdbdConfig(**slurmdbd_conf)


dump = functools.partial(dump_base, marshaller=_marshaller)
dumps = functools.partial(dumps_base, marshaller=_marshaller)
load = functools.partial(load_base, parser=_parser)
loads = functools.partial(loads_base, parser=_parser)


@contextmanager
def edit(file: Union[str, os.PathLike]) -> SlurmdbdConfig:
    """Edit a slurmdbd.conf file.

    Args:
        file: Path to slurmdbd.conf file to edit. If slurmdbd.conf does
            not exist at the specified file path, it will be created.
    """
    if not os.path.exists(file):
        # Create an empty SlurmConfig that can be populated.
        config = SlurmdbdConfig()
    else:
        config = load(file=file)

    yield config
    dump(content=config, file=file)
