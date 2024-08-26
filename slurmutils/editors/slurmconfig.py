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

from ..models import DownNodes, FrontendNode, Node, NodeSet, Partition, SlurmConfig
from ..models.option import SlurmConfigOptionSet
from .editor import (
    clean,
    dumper,
    loader,
    marshall_content,
    parse_line,
)

_logger = logging.getLogger("slurmutils")


@loader
def load(file: Union[str, os.PathLike]) -> SlurmConfig:
    """Load `slurm.conf` data model from slurm.conf file."""
    return loads(Path(file).read_text())


def loads(content: str) -> SlurmConfig:
    """Load `slurm.conf` data model from string."""
    return _parse(content)


@dumper
def dump(config: SlurmConfig, file: Union[str, os.PathLike]) -> None:
    """Dump `slurm.conf` data model into slurm.conf file."""
    Path(file).write_text(dumps(config))


def dumps(config: SlurmConfig) -> str:
    """Dump `slurm.conf` data model into a string."""
    return _marshall(config)


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


def _parse(content: str) -> SlurmConfig:
    """Parse contents of `slurm.conf`.

    Args:
        content: Contents of `slurm.conf`.
    """
    data = {}
    lines = content.splitlines()
    for index, line in enumerate(lines):
        config = clean(line)
        if config is None:
            _logger.debug("ignoring line %s at index %s in slurm.conf", line, index)
            continue

        if config.startswith("Include"):
            _, v = config.split(maxsplit=1)
            data["Include"] = data.get("Include", []) + [v]
        elif config.startswith("SlurmctldHost"):
            _, v = config.split("=", maxsplit=1)
            data["SlurmctldHost"] = data.get("SlurmctldHost", []) + [v]
        elif config.startswith("NodeName"):
            nodes = data.get("Nodes", {})
            nodes.update(Node.from_str(config).dict())
            data["Nodes"] = nodes
        elif config.startswith("DownNodes"):
            data["DownNodes"] = data.get("DownNodes", []) + [DownNodes.from_str(config).dict()]
        elif config.startswith("FrontendNode"):
            frontend_nodes = data.get("FrontendNodes", {})
            frontend_nodes.update(FrontendNode.from_str(config).dict())
            data["FrontendNodes"] = frontend_nodes
        elif config.startswith("NodeSet"):
            node_sets = data.get("NodeSets", {})
            node_sets.update(NodeSet.from_str(config).dict())
            data["NodeSets"] = node_sets
        elif config.startswith("PartitionName"):
            partitions = data.get("Partitions", {})
            partitions.update(Partition.from_str(config).dict())
            data["Partitions"] = partitions
        else:
            data.update(parse_line(SlurmConfigOptionSet, config))

    return SlurmConfig.from_dict(data)


def _marshall(config: SlurmConfig) -> str:
    """Marshall `slurm.conf` data model back into slurm.conf format.

    Args:
        config: `slurm.conf` data model to marshall.
    """
    result = []
    data = config.dict()
    include = data.pop("Include", None)
    slurmctld_host = data.pop("SlurmctldHost", None)
    nodes = data.pop("Nodes", {})
    down_nodes = data.pop("DownNodes", [])
    frontend_nodes = data.pop("FrontendNodes", {})
    node_sets = data.pop("NodeSets", {})
    partitions = data.pop("Partitions", {})

    if include:
        result.extend([f"Include {i}" for i in include])

    if slurmctld_host:
        result.extend([f"SlurmctldHost={host}" for host in slurmctld_host])

    result.extend(marshall_content(SlurmConfigOptionSet, data))

    if nodes:
        for k, v in nodes.items():
            result.append(str(Node(NodeName=k, **v)))

    if down_nodes:
        for entry in down_nodes:
            result.append(str(DownNodes(**entry)))

    if frontend_nodes:
        for k, v in frontend_nodes.items():
            result.append(str(FrontendNode(FrontendName=k, **v)))

    if node_sets:
        for k, v in node_sets.items():
            result.append(str(NodeSet(NodeSet=k, **v)))

    if partitions:
        for k, v in partitions.items():
            result.append(str(Partition(PartitionName=k, **v)))

    return "\n".join(result)
