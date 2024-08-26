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

"""Data models for `slurm.conf` configuration file."""

__all__ = [
    "Node",
    "DownNodes",
    "FrontendNode",
    "NodeSet",
    "Partition",
    "SlurmConfig",
]

import copy
from typing import Any, Dict, List, Optional

from ..editors.editor import marshall_content, parse_line
from .model import BaseModel, LineInterface, format_key, generate_descriptors
from .option import (
    DownNodeOptionSet,
    FrontendNodeOptionSet,
    NodeOptionSet,
    NodeSetOptionSet,
    PartitionOptionSet,
    SlurmConfigOptionSet,
)


class Node(BaseModel, LineInterface):
    """`Node` data model."""

    def __init__(self, *, NodeName: str, **kwargs) -> None:  # noqa N803
        self.__node_name = NodeName
        super().__init__(NodeOptionSet, **kwargs)

    @property
    def node_name(self) -> str:
        """Get node name."""
        return self.__node_name

    @node_name.setter
    def node_name(self, name: str) -> None:
        """Set new node name."""
        self.__node_name = name

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Node":
        """Construct model from dictionary."""
        name = list(data.keys())[0]
        return cls(NodeName=name, **data[name])

    @classmethod
    def from_str(cls, line: str) -> "Node":
        """Construct model from configuration line."""
        data = parse_line(NodeOptionSet, line)
        return cls(**data)

    def dict(self) -> Dict[str, Any]:
        """Return model as dictionary."""
        return copy.deepcopy({self.__node_name: self.data})

    def __str__(self) -> str:
        """Return model as configuration line."""
        line = [f"NodeName={self.__node_name}"]
        line.extend(marshall_content(NodeOptionSet, self.data))
        return " ".join(line)


class DownNodes(BaseModel, LineInterface):
    """`DownNodes` data model."""

    def __init__(self, **kwargs):
        super().__init__(DownNodeOptionSet, **kwargs)

    @classmethod
    def from_str(cls, line: str) -> "DownNodes":
        """Construct model from configuration line."""
        data = parse_line(DownNodeOptionSet, line)
        return cls(**data)

    def __str__(self) -> str:
        """Return model as configuration line."""
        return " ".join(marshall_content(DownNodeOptionSet, self.data))


class FrontendNode(BaseModel, LineInterface):
    """`FrontendNode` data model."""

    def __init__(self, *, FrontendName: str, **kwargs) -> None:  # noqa N803
        self.__frontend_name = FrontendName
        super().__init__(FrontendNodeOptionSet, **kwargs)

    @property
    def frontend_name(self) -> str:
        """Get frontend node name."""
        return self.__frontend_name

    @frontend_name.setter
    def frontend_name(self, name: str) -> None:
        """Set new frontend node name."""
        self.__frontend_name = name

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "FrontendNode":
        """Construct model from dictionary."""
        name = list(data.keys())[0]
        return cls(FrontendName=name, **data[name])

    @classmethod
    def from_str(cls, line: str) -> "FrontendNode":
        """Construct model from configuration line."""
        data = parse_line(FrontendNodeOptionSet, line)
        return cls(**data)

    def dict(self) -> Dict[str, Any]:
        """Return model as dictionary."""
        return copy.deepcopy({self.__frontend_name: self.data})

    def __str__(self) -> str:
        """Return model as configuration line."""
        line = [f"FrontendName={self.__frontend_name}"]
        line.extend(marshall_content(FrontendNodeOptionSet, self.data))
        return " ".join(line)


class NodeSet(BaseModel, LineInterface):
    """`NodeSet` data model."""

    def __init__(self, *, NodeSet: str, **kwargs) -> None:  # noqa N803
        self.__node_set = NodeSet
        super().__init__(NodeSetOptionSet, **kwargs)

    @property
    def node_set(self) -> str:
        """Get node set name."""
        return self.__node_set

    @node_set.setter
    def node_set(self, name: str) -> None:
        """Set new node set name."""
        self.__node_set = name

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "NodeSet":
        """Construct model from dictionary."""
        name = list(data.keys())[0]
        return cls(NodeSet=name, **data[name])

    @classmethod
    def from_str(cls, line: str) -> "NodeSet":
        """Construct model from configuration line."""
        data = parse_line(NodeSetOptionSet, line)
        return cls(**data)

    def dict(self) -> Dict[str, Any]:
        """Return model as dictionary."""
        return copy.deepcopy({self.__node_set: self.data})

    def __str__(self) -> str:
        """Return model as configuration line."""
        line = [f"NodeSet={self.__node_set}"]
        line.extend(marshall_content(NodeSetOptionSet, self.data))
        return " ".join(line)


class Partition(BaseModel, LineInterface):
    """`Partition` data model."""

    def __init__(self, *, PartitionName: str, **kwargs):  # noqa N803
        self.__partition_name = PartitionName
        super().__init__(PartitionOptionSet, **kwargs)

    @property
    def partition_name(self) -> str:
        """Get partition name."""
        return self.__partition_name

    @partition_name.setter
    def partition_name(self, name: str) -> None:
        """Set new partition name."""
        self.__partition_name = name

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Partition":
        """Construct model from dictionary."""
        name = list(data.keys())[0]
        return cls(PartitionName=name, **data[name])

    @classmethod
    def from_str(cls, line: str) -> "Partition":
        """Construct model from configuration line."""
        data = parse_line(PartitionOptionSet, line)
        return cls(**data)

    def dict(self) -> Dict[str, Any]:
        """Return model as dictionary."""
        return copy.deepcopy({self.__partition_name: self.data})

    def __str__(self) -> str:
        """Return model as configuration line."""
        line = [f"PartitionName={self.__partition_name}"]
        line.extend(marshall_content(PartitionOptionSet, self.data))
        return " ".join(line)


class SlurmConfig(BaseModel):
    """`slurm.conf` data model."""

    def __init__(
        self,
        *,
        Nodes: Optional[Dict[str, Any]] = None,  # noqa N803
        DownNodes: Optional[List[Dict[str, Any]]] = None,  # noqa N803
        FrontendNodes: Optional[Dict[str, Any]] = None,  # noqa N803
        NodeSets: Optional[Dict[str, Any]] = None,  # noqa N803
        Partitions: Optional[Dict[str, Any]] = None,  # noqa N803
        **kwargs,
    ) -> None:
        super().__init__(SlurmConfigOptionSet, **kwargs)
        self.data["Nodes"] = Nodes or {}
        self.data["DownNodes"] = DownNodes or []
        self.data["FrontendNodes"] = FrontendNodes or {}
        self.data["NodeSets"] = NodeSets or {}
        self.data["Partitions"] = Partitions or {}

    @property
    def nodes(self):
        """Get map of all nodes in the Slurm configuration."""
        return self.data["Nodes"]

    @nodes.setter
    def nodes(self, value):
        """Set new node mapping for the Slurm configuration."""
        self.data["Nodes"] = value

    @nodes.deleter
    def nodes(self):
        """Delete entire node mapping in the Slurm configuration."""
        self.data["Nodes"] = {}

    @property
    def down_nodes(self):
        """Get list of all down nodes in the Slurm configuration."""
        return self.data["DownNodes"]

    @down_nodes.setter
    def down_nodes(self, value):
        """Set new down node list for the Slurm configuration."""
        self.data["DownNodes"] = value

    @down_nodes.deleter
    def down_nodes(self):
        """Delete entire down node list in the Slurm configuration."""
        self.data["DownNodes"] = []

    @property
    def frontend_nodes(self):
        """Get map of all frontend nodes in the Slurm configuration."""
        return self.data["FrontendNodes"]

    @frontend_nodes.setter
    def frontend_nodes(self, value):
        """Set new frontend node mapping for the Slurm configuration."""
        self.data["FrontendNodes"] = value

    @frontend_nodes.deleter
    def frontend_nodes(self):
        """Delete entire frontend node mapping in the Slurm configuration."""
        self.data["FrontendNodes"] = {}

    @property
    def node_sets(self):
        """Get map of all node sets in the Slurm configuration."""
        return self.data["NodeSets"]

    @node_sets.setter
    def node_sets(self, value):
        """Set new node set mapping for the Slurm configuration."""
        self.data["NodeSets"] = value

    @node_sets.deleter
    def node_sets(self):
        """Delete entire node set mapping in the Slurm configuration."""
        self.data["NodeSets"] = {}

    @property
    def partitions(self):
        """Get map of all partitions in the Slurm configuration."""
        return self.data["Partitions"]

    @partitions.setter
    def partitions(self, value):
        """Set partition mapping for the Slurm configuration."""
        self.data["Partitions"] = value

    @partitions.deleter
    def partitions(self):
        """Delete entire partition mapping in the Slurm configuration."""
        self.data["Partitions"] = {}


for opt in NodeOptionSet.keys():
    setattr(Node, format_key(opt), property(*generate_descriptors(opt)))
for opt in DownNodeOptionSet.keys():
    setattr(DownNodes, format_key(opt), property(*generate_descriptors(opt)))
for opt in FrontendNodeOptionSet.keys():
    setattr(FrontendNode, format_key(opt), property(*generate_descriptors(opt)))
for opt in NodeSetOptionSet.keys():
    setattr(NodeSet, format_key(opt), property(*generate_descriptors(opt)))
for opt in PartitionOptionSet.keys():
    setattr(Partition, format_key(opt), property(*generate_descriptors(opt)))
for opt in SlurmConfigOptionSet.keys():
    setattr(SlurmConfig, format_key(opt), property(*generate_descriptors(opt)))
