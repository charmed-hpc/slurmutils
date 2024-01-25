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

import functools
import os
from collections import deque
from contextlib import contextmanager
from typing import Union

from slurmutils.models import DownNodes, FrontendNode, Node, NodeSet, Partition, SlurmConfig

from ._editor import (
    clean,
    dump_base,
    dumps_base,
    load_base,
    loads_base,
    parse_model,
    parse_repeating_config,
)


def _marshaller(config: SlurmConfig) -> str:
    """Marshall Python object into slurm.conf configuration file.

    Args:
        config: Python object to convert to slurm.conf configuration file.
    """
    ...


_parse_slurm = functools.partial(parse_model, model=SlurmConfig)
_parse_node = functools.partial(parse_model, model=Node)
_parse_frontend = functools.partial(parse_model, model=FrontendNode)
_parse_down_node = functools.partial(parse_model, model=DownNodes)
_parse_node_set = functools.partial(parse_model, model=NodeSet)
_parse_partition = functools.partial(parse_model, model=Partition)


def _parser(config: str) -> SlurmConfig:
    """Parse slurm.conf configuration file into Python object.

    Args:
        config: Content of slurm.conf configuration file.
    """
    slurm_conf = {}
    nodes = {}
    down_nodes = []
    frontend_nodes = {}
    node_sets = {}
    partitions = {}

    # import pdb
    # pdb.set_trace()
    config = clean(deque(config.splitlines()))
    while config:
        line = config.popleft()
        # slurm.conf `Include` is the only configuration knob whose
        # separator is whitespace rather than `=`.
        if line.startswith("Include"):
            option, value = line.split(maxsplit=1)
            parse_repeating_config(option, value, pocket=slurm_conf)

        # `SlurmctldHost` is the same as `Include` where it can
        # be specified on multiple lines.
        elif line.startswith("SlurmctldHost"):
            option, value = line.split("=", 1)
            parse_repeating_config(option, value, pocket=slurm_conf)

        # Check if option maps to slurm.conf data model. If so, invoke parsing
        # rules for that specific data model and enter its parsed information
        # into the appropriate pocket.
        elif line.startswith("NodeName"):
            _parse_node(line, pocket=nodes)
        elif line.startswith("DownNodes"):
            _parse_down_node(line, pocket=down_nodes)
        elif line.startswith("FrontendNode"):
            _parse_frontend(line, pocket=frontend_nodes)
        elif line.startswith("NodeSet"):
            _parse_node_set(line, pocket=node_sets)
        elif line.startswith("PartitionName"):
            _parse_partition(line, pocket=partitions)
        else:
            _parse_slurm(line, pocket=slurm_conf)

    return SlurmConfig(
        **slurm_conf,
        nodes=nodes,
        frontend_nodes=frontend_nodes,
        down_nodes=down_nodes,
        node_sets=node_sets,
        partitions=partitions,
    )


dump = functools.partial(dump_base, marshaller=_marshaller)
dumps = functools.partial(dumps_base, marshaller=_marshaller)
load = functools.partial(load_base, parser=_parser)
loads = functools.partial(loads_base, parser=_parser)


@contextmanager
def edit(file: Union[str, os.PathLike]) -> SlurmConfig:
    """Edit a slurm.conf file.

    Args:
        file: Path to slurm.conf file to edit. If slurm.conf does
            not exist at the specified file path, it will be created.
    """
    if os.path.exists(file):
        # Create an empty SlurmConfig that can be populated.
        config = SlurmConfig()
    else:
        config = load(file=file)

    yield config
    dump(content=config, file=file)
