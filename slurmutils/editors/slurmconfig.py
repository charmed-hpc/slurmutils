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
from datetime import datetime
from typing import Union

from slurmutils.models import DownNodes, FrontendNode, Node, NodeSet, Partition, SlurmConfig

from ._editor import (
    clean,
    dump_base,
    dumps_base,
    header,
    load_base,
    loads_base,
    marshal_model,
    parse_model,
    parse_repeating_config,
)


def _marshaller(config: SlurmConfig) -> str:
    """Marshal Python object into slurm.conf configuration file.

    Args:
        config: `SlurmConfig` object to convert to slurm.conf configuration file.
    """
    marshalled = [header(f"`slurm.conf` file generated at {datetime.now()} by slurmutils.")]

    if config.include:
        marshalled.append(header("Included configuration files"))
        marshalled.extend([f"Include {i}\n" for i in config.include] + ["\n"])
    if config.slurmctld_host:
        marshalled.extend([f"SlurmctldHost={host}\n" for host in config.slurmctld_host] + ["\n"])

    # Marshal the SlurmConfig object into Slurm configuration format.
    # Ignore pockets containing child models as they will be marshalled inline.
    marshalled.extend(
        marshal_model(
            config,
            ignore={
                "Includes",
                "SlurmctldHost",
                "nodes",
                "frontend_nodes",
                "down_nodes",
                "node_sets",
                "partitions",
            },
        )
        + ["\n"]
    )

    if len(config.nodes) != 0:
        marshalled.extend(
            [header("Node configurations")]
            + [marshal_model(node, inline=True) for node in config.nodes]
            + ["\n"]
        )

    if len(config.frontend_nodes) != 0:
        marshalled.extend(
            [header("Frontend node configurations")]
            + [marshal_model(frontend, inline=True) for frontend in config.frontend_nodes]
            + ["\n"]
        )

    if len(config.down_nodes) != 0:
        marshalled.extend(
            [header("Down node configurations")]
            + [marshal_model(down_node, inline=True) for down_node in config.down_nodes]
            + ["\n"]
        )

    if len(config.node_sets) != 0:
        marshalled.extend(
            [header("Node set configurations")]
            + [marshal_model(node_set, inline=True) for node_set in config.node_sets]
            + ["\n"]
        )

    if len(config.partitions) != 0:
        marshalled.extend(
            [header("Partition configurations")]
            + [marshal_model(part, inline=True) for part in config.partitions]
        )

    return "".join(marshalled)


def _parser(config: str) -> SlurmConfig:
    """Parse slurm.conf configuration file into Python object.

    Args:
        config: Content of slurm.conf configuration file.
    """
    slurm_conf = {}
    nodes = {}
    frontend_nodes = {}
    down_nodes = []
    node_sets = {}
    partitions = {}

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
            parse_model(line, pocket=nodes, model=Node)
        elif line.startswith("FrontendNode"):
            parse_model(line, pocket=frontend_nodes, model=FrontendNode)
        elif line.startswith("DownNodes"):
            parse_model(line, pocket=down_nodes, model=DownNodes)
        elif line.startswith("NodeSet"):
            parse_model(line, pocket=node_sets, model=NodeSet)
        elif line.startswith("PartitionName"):
            parse_model(line, pocket=partitions, model=Partition)
        else:
            parse_model(line, pocket=slurm_conf, model=SlurmConfig)

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
    if not os.path.exists(file):
        # Create an empty SlurmConfig that can be populated.
        config = SlurmConfig()
    else:
        config = load(file=file)

    yield config
    dump(content=config, file=file)
