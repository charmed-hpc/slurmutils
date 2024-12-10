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

"""Data models for `gres.conf` configuration file."""

__all__ = ["GRESConfig", "GRESName", "GRESNode"]

import copy
from typing import Any

from .model import BaseModel, clean, marshall_content, parse_line
from .option import GRESConfigOptionSet, GRESNameOptionSet, GRESNodeOptionSet


class GRESName(BaseModel):
    """`gres.conf` name data model."""

    def __init__(self, *, Name, **kwargs) -> None:  # noqa N803
        super().__init__(GRESNameOptionSet, Name=Name, **kwargs)

    @classmethod
    def from_str(cls, content: str) -> "GRESName":
        """Construct `GRESName` data model from a gres.conf configuration line."""
        return cls(**parse_line(GRESNameOptionSet, content))

    def __str__(self) -> str:
        """Return `GRESName` data model as a gres.conf configuration line."""
        return " ".join(marshall_content(GRESNameOptionSet, self.data))

    @property
    def auto_detect(self) -> str | None:
        """Hardware detection mechanism to enable for automatic GRES configuration.

        Warnings:
            * Setting this option will override the configured global automatic
                hardware detection mechanism for this generic resource.
        """
        return self.data.get("AutoDetect", None)

    @auto_detect.setter
    def auto_detect(self, value: str) -> None:
        self.data["AutoDetect"] = value

    @auto_detect.deleter
    def auto_detect(self) -> None:
        try:
            del self.data["AutoDetect"]
        except KeyError:
            pass

    @property
    def count(self) -> str | None:
        """Number of resources of this name/type available on the node."""
        return self.data.get("Count", None)

    @count.setter
    def count(self, value: str) -> None:
        self.data["Count"] = value

    @count.deleter
    def count(self) -> None:
        try:
            del self.data["Count"]
        except KeyError:
            pass

    @property
    def cores(self) -> list[str] | None:
        """Core index numbers for the specific cores which can use this resource."""
        return self.data.get("Cores", None)

    @cores.setter
    def cores(self, value: list[str]) -> None:
        self.data["Cores"] = value

    @cores.deleter
    def cores(self) -> None:
        try:
            del self.data["Cores"]
        except KeyError:
            pass

    @property
    def file(self) -> str | None:
        """Fully qualified pathname of the device files associated with a resource."""
        return self.data.get("File", None)

    @file.setter
    def file(self, value: str) -> None:
        self.data["File"] = value

    @file.deleter
    def file(self) -> None:
        try:
            del self.data["File"]
        except KeyError:
            pass

    @property
    def flags(self) -> list[str] | None:
        """Flags to change the configured behavior of the generic resource."""
        return self.data.get("Flags", None)

    @flags.setter
    def flags(self, value: list[str]) -> None:
        self.data["Flags"] = value

    @flags.deleter
    def flags(self) -> None:
        try:
            del self.data["Flags"]
        except KeyError:
            pass

    @property
    def links(self) -> list[str] | None:
        """Numbers identifying the number of connections between this device and other devices."""
        return self.data.get("Links", None)

    @links.setter
    def links(self, value: list[str]) -> None:
        self.data["Links"] = value

    @links.deleter
    def links(self) -> None:
        try:
            del self.data["Links"]
        except KeyError:
            pass

    @property
    def multiple_files(self) -> str | None:
        """Fully qualified pathname of the device files associated with a resource.

        Warnings:
            * Uses `files` instead if not using GPUs with multi-instance functionality.
            * `files` and `multiple_files` cannot be used together.
        """
        return self.data.get("MultipleFiles", None)

    @multiple_files.setter
    def multiple_files(self, value: str) -> None:
        self.data["MultipleFiles"] = value

    @multiple_files.deleter
    def multiple_files(self) -> None:
        try:
            del self.data["MultipleFiles"]
        except KeyError:
            pass

    @property
    def name(self) -> str:
        """Name of generic resource."""
        return self.data.get("Name")

    @name.setter
    def name(self, value: str) -> None:
        self.data["Name"] = value

    @property
    def type(self) -> str | None:
        """Arbitrary string identifying the type of the generic resource."""
        return self.data.get("Type", None)

    @type.setter
    def type(self, value: str) -> None:
        self.data["Type"] = value

    @type.deleter
    def type(self) -> None:
        try:
            del self.data["Type"]
        except KeyError:
            pass


class GRESNode(GRESName):
    """`gres.conf` node data model."""

    def __init__(self, *, NodeName: str, **kwargs):  # noqa N803
        self.__node_name = NodeName
        # Want to share `GRESName` descriptors, but not constructor.
        BaseModel.__init__(self, GRESNodeOptionSet, **kwargs)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "GRESNode":
        """Construct `GRESNode` data model from dictionary object."""
        node_name = list(data.keys())[0]
        return cls(NodeName=node_name, **data[node_name])

    @classmethod
    def from_str(cls, content: str) -> "GRESNode":
        """Construct `GRESNode` data model from a gres.conf configuration line."""
        return cls(**parse_line(GRESNodeOptionSet, content))

    def dict(self) -> dict[str, Any]:
        """Return `GRESNode` data model as a dictionary object."""
        return copy.deepcopy({self.__node_name: self.data})

    def __str__(self) -> str:
        """Return `GRESNode` data model as a gres.conf configuration line."""
        line = [f"NodeName={self.__node_name}"]
        line.extend(marshall_content(GRESNodeOptionSet, self.data))
        return " ".join(line)

    @property
    def node_name(self) -> str:
        """Node(s) the generic resource configuration will be applied to.

        Value `NodeName` specification can use a Slurm hostlist specification.
        """
        return self.__node_name

    @node_name.setter
    def node_name(self, value: str) -> None:
        self.__node_name = value


class GRESConfig(BaseModel):
    """`gres.conf` data model."""

    def __init__(
        self,
        *,
        Names: list[str] | None = None,  # noqa N803
        Nodes: dict[str, Any] | None = None,  # noqa N803
        **kwargs,
    ) -> None:
        super().__init__(GRESConfigOptionSet, **kwargs)
        self.data["Names"] = Names or []
        self.data["Nodes"] = Nodes or {}

    @classmethod
    def from_str(cls, content: str) -> "GRESConfig":
        """Construct `gres.conf` data model from a gres.conf configuration file."""
        data = {}
        lines = content.splitlines()
        for line in lines:
            config = clean(line)
            if config is None:
                continue

            if config.startswith("Name"):
                data["Names"] = data.get("Names", []) + [GRESName.from_str(config).dict()]
            elif config.startswith("NodeName"):
                nodes = data.get("Nodes", {})
                nodes.update(GRESNode.from_str(config).dict())
                data["Nodes"] = nodes
            else:
                data.update(parse_line(GRESConfigOptionSet, config))

        return GRESConfig.from_dict(data)

    def __str__(self) -> str:
        """Return `gres.conf` data model in gres.conf format."""
        data = self.dict()
        global_auto_detect = data.pop("AutoDetect", None)
        names = data.pop("Names", [])
        nodes = data.pop("Nodes", {})

        content = []
        if global_auto_detect:
            content.append(f"AutoDetect={global_auto_detect}")
        if names:
            content.extend([str(GRESName(**name)) for name in names])
        if nodes:
            content.extend([str(GRESNode(NodeName=k, **v)) for k, v in nodes.items()])

        return "\n".join(content) + "\n"

    @property
    def auto_detect(self) -> str | None:
        """Get global `AutoDetect` configuration in `gres.conf`.

        Warnings:
            * Setting this option will configure the automatic hardware detection mechanism
                globally within `gres.conf`. Inline `AutoDetect` can be set used on
                `GRESNode` and`GRESName` to override the global automatic hardware
                detection mechanism for specific nodes or resource names.
        """
        return self.data.get("AutoDetect", None)

    @auto_detect.setter
    def auto_detect(self, value: str) -> None:
        self.data["AutoDetect"] = value

    @auto_detect.deleter
    def auto_detect(self) -> None:
        try:
            del self.data["AutoDetect"]
        except KeyError:
            pass

    @property
    def names(self) -> list[dict[str, Any]] | None:
        """List of configured generic resources."""
        return self.data.get("Names", None)

    @names.setter
    def names(self, value: list[dict[str, Any]]) -> None:
        self.data["Names"] = value

    @names.deleter
    def names(self) -> None:
        self.data["Names"] = []

    @property
    def nodes(self) -> dict[str, dict[str, Any]]:
        """Map of nodes with configured generic resources."""
        return self.data["Nodes"]

    @nodes.setter
    def nodes(self, value: dict[str, GRESNode]) -> None:
        self.data["Nodes"] = value

    @nodes.deleter
    def nodes(self) -> None:
        self.data["Nodes"] = {}
