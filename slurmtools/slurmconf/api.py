# Copyright 2023 Canonical Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Parse and render SLURM configuration data."""

__all__ = ["SlurmConf", "Node", "DownNode", "FrontendNode", "NodeSet", "Partition"]

import logging
import os
import pathlib
import re
import shlex
from dataclasses import make_dataclass
from itertools import chain
from typing import Dict, List, Optional, Union

from .token import (
    DownNodeConfOpts,
    FrontendNodeConfOpts,
    NodeConfOpts,
    NodeSetConfOpts,
    PartitionConfOpts,
    SlurmConfOpts,
)

SLURM_CONF_FILE = "/etc/slurm/slurm.conf"
_pre_prop_name = re.compile(r"(.)([A-Z][a-z]+)")
_prop_name = re.compile(r"([a-z0-9])([A-Z])")
_logger = logging.getLogger(__name__)


def _snakecase(opt):
    """Convert SLURM's loose PascalCase to snake_case.

    Args:
        opt: Configuration option in loose PascalCase to convert to snake_case.
    """
    pre_prop_name = _pre_prop_name.sub(r"\1_\2", opt)
    return _prop_name.sub(r"\1_\2", pre_prop_name).lower()


def _gen_descriptors(opt):
    """Generate descriptors for accessing SLURM configuration options.

    Args:
        opt: Option to generate descriptors for.
    """

    def new_getter(self):
        return self._data.get(opt, None)

    def new_setter(self, value: str):
        self._data[opt] = value

    def new_deleter(self):
        del self._data[opt]

    return new_getter, new_setter, new_deleter


# Methods to attach to SLURM data structs.
def _init(self, **kwargs):
    """__init__ method for SLURM data structs."""
    self._data = kwargs


def _repr(self):
    """__repr method for SLURM data structs."""
    return f"{self.__class__.__name__}({', '.join(f'{k}={v}' for k, v in self._data.items())})"


def _gen_from_line(conf_opts):
    """Generate from_line parser for SLURM data structs."""

    def from_line(cls, line: str):
        data = {}
        for token in shlex.split(line):  # Use shlex.split(...) to preserve quotation blocks.
            opt, value = token.split("=", 1)
            if hasattr(conf_opts, opt):
                if parse_callback := getattr(conf_opts, opt).parse:
                    value = parse_callback(value)
                data.update({opt: value})
            else:
                _logger.warning(f"Unrecognized configuration option: {token}")

        return cls(**data)

    return classmethod(from_line)


def _gen_to_line(conf_opts):
    """Generate to_line renderer for SLURM data structs."""

    def to_line(self):
        tokens = []
        for opt, value in self._data.items():
            if hasattr(conf_opts, opt):
                if render_callback := getattr(conf_opts, opt).render:
                    value = render_callback(value)
                tokens.append(f"{opt}={value}")
            else:
                _logger.warning(f"Unrecognized configuration option: {opt}")

        return " ".join(tokens)

    return to_line


# Generate descriptors for accessing SLURM configuration options
_node_desc = {_snakecase(f): property(*_gen_descriptors(f)) for f in NodeConfOpts._fields}
_dnode_desc = {_snakecase(f): property(*_gen_descriptors(f)) for f in DownNodeConfOpts._fields}
_fnode_desc = {_snakecase(f): property(*_gen_descriptors(f)) for f in FrontendNodeConfOpts._fields}
_nodeset_desc = {_snakecase(f): property(*_gen_descriptors(f)) for f in NodeSetConfOpts._fields}
_part_desc = {_snakecase(f): property(*_gen_descriptors(f)) for f in PartitionConfOpts._fields}

# Generate SLURM configuration data structs.
Comment = make_dataclass("Comment", ["content", "index", "inline"])
Node = type(
    "Node",
    (object,),
    {
        "__init__": _init,
        "__repr__": _repr,
        "from_line": _gen_from_line(NodeConfOpts),
        "to_line": _gen_to_line(NodeConfOpts),
        **_node_desc,
    },
)
DownNode = type(
    "DownNode",
    (object,),
    {
        "__init__": _init,
        "__repr__": _repr,
        "from_line": _gen_from_line(DownNodeConfOpts),
        "to_line": _gen_to_line(DownNodeConfOpts),
        **_dnode_desc,
    },
)
FrontendNode = type(
    "FrontendNode",
    (object,),
    {
        "__init__": _init,
        "__repr__": _repr,
        "from_line": _gen_from_line(FrontendNodeConfOpts),
        "to_line": _gen_to_line(FrontendNodeConfOpts),
        **_fnode_desc,
    },
)
NodeSet = type(
    "NodeSet",
    (object,),
    {
        "__init__": _init,
        "__repr__": _repr,
        "from_line": _gen_from_line(NodeSetConfOpts),
        "to_line": _gen_to_line(NodeSetConfOpts),
        **_nodeset_desc,
    },
)
Partition = type(
    "Partition",
    (object,),
    {
        "__init__": _init,
        "__repr__": _repr,
        "from_line": _gen_from_line(PartitionConfOpts),
        "to_line": _gen_to_line(PartitionConfOpts),
        **_part_desc,
    },
)


def _parse(conf):
    """Parse SLURM configuration data.

    Args:
        conf: SLURM configuration data in SLURM format.
    """
    conf_opts = {
        "nodes": {},
        "down_nodes": [],
        "frontend_nodes": {},
        "nodesets": {},
        "partitions": {},
        "comments": [],
    }

    for index, line in enumerate(conf.splitlines()):
        if "#" in line:
            if line.startswith("#"):
                conf_opts["comments"].append(Comment(line, index, inline=False))
                continue
            else:
                pos = line.index("#")
                conf_opts["comments"].append(Comment(line[pos:], index, inline=True))
                line = line[:pos].strip()

        opt, value = line.split("=", 1)
        if opt == "NodeName":
            node = Node.from_line(line)
            conf_opts["nodes"][node.node_name] = node
        elif opt == "DownNodes":
            conf_opts["down_nodes"].append(DownNode.from_line(line))
        elif opt == "FrontendName":
            frontend = FrontendNode.from_line(line)
            conf_opts["frontend_nodes"][frontend.frontend_name] = frontend
        elif opt == "NodeSet":
            nodeset = NodeSet.from_line(line)
            conf_opts["nodesets"][nodeset.nodeset] = nodeset
        elif opt == "PartitionName":
            partition = Partition.from_line(line)
            conf_opts["partitions"][partition.partition_name] = partition
        elif opt == "SlurmctldHost":
            if "SlurmctldHost" not in conf_opts.keys():
                conf_opts["SlurmctldHost"] = [value]
            else:
                conf_opts["SlurmctldHost"].append(value)
        elif hasattr(SlurmConfOpts, opt):
            if parse_callback := getattr(SlurmConfOpts, opt).parse:
                value = parse_callback(value)
            conf_opts.update({opt: value})
        else:
            _logger.warning(f"Unable to parse line: {line}. Invalid configuration")

    return conf_opts


def _render(conf):
    """Render SLURM configuration data into SLURM format.

    Args:
        conf: SLURM configuration data in parsed format.
    """
    conf_render = []
    nodes = conf.pop("nodes")
    down_nodes = conf.pop("down_nodes")
    frontend_nodes = conf.pop("frontend_nodes")
    nodesets = conf.pop("nodesets")
    partitions = conf.pop("partitions")
    comments = conf.pop("comments")

    for opt, value in conf.items():
        if opt == "SlurmctldHost":
            conf_render.extend([f"SlurmctldHost={host}" for host in value])
        elif hasattr(SlurmConfOpts, opt):
            if render_callback := getattr(SlurmConfOpts, opt).render:
                value = render_callback(value)
            conf_render.append(f"{opt}={value}")
        else:
            _logger.warning(f"Unrecognized configuration option: {opt}")

    for struct in chain(
        nodes.values(), down_nodes, frontend_nodes.values(), nodesets.values(), partitions.values()
    ):
        conf_render.append(struct.to_line())

    for comment in comments:
        if comment.inline:
            conf_render[comment.index] = conf_render[comment.index] + f"  {comment.content}"
        else:
            conf_render.insert(comment.index, comment.content)

    return "\n".join(conf_render) + "\n"


class SlurmConf:
    """API interface to the slurm.conf file."""

    def __init__(self, conf_file: Union[str, os.PathLike] = SLURM_CONF_FILE) -> None:
        self._data = {}
        self._conf_file = conf_file

    def __enter__(self) -> "SlurmConf":
        """Load metadata file when entering context."""
        self.load()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Render and dump metadata file and configuration file when leaving context."""
        self.dump()

    @property
    def comments(self) -> Optional[List[Comment]]:
        """Get comments in SLURM configuration file."""
        return self._data.get("comments")

    @property
    def nodes(self) -> Optional[Dict[str, Node]]:
        """Get nodes in SLURM configuration file."""
        return self._data.get("nodes")

    @property
    def down_nodes(self) -> Optional[List[DownNode]]:
        """Get down nodes in SLURM configuration file."""
        return self._data.get("down_nodes")

    @property
    def frontend_nodes(self) -> Optional[Dict[str, FrontendNode]]:
        """Get frontend nodes in SLURM configuration file."""
        return self._data.get("frontend_nodes")

    @property
    def nodesets(self) -> Optional[Dict[str, NodeSet]]:
        """Get nodesets in SLURM configuration file."""
        return self._data.get("nodesets")

    @property
    def partitions(self) -> Optional[Dict[str, Partition]]:
        """Get partitions in SLURM configuration file."""
        return self._data.get("partitions")

    def load(self) -> None:
        """Load slurm.conf configuration file.

        Notes:
            This method will create a blank configuration if the slurm.conf
            configuration file passed during initialisation does not exist.
        """
        if (conf := pathlib.Path(self._conf_file)).exists():
            self._data = _parse(conf.read_text(encoding="ascii"))
        else:
            _logger.debug(f"{self._conf_file} not found. Creating blank configuration")

    def dump(self, conf_file: Optional[Union[str, os.PathLike]] = None) -> None:
        """Render and dump slurm.conf configuration file.

        Args:
            conf_file: Location to dump SLURM configuration information.

        Notes:
            This method will overwrite any existing slurm.conf file if a
            pre-existing file located in the same location as `conf_file`.
        """
        conf_file = conf_file if conf_file else self._conf_file
        if (conf := pathlib.Path(conf_file)).exists():
            _logger.debug(f"Overwriting pre-existing {conf_file}")

        conf.write_text(_render(self._data.copy()), encoding="ascii")


# Generate SLURM configuration API.
for field in SlurmConfOpts._fields:
    # Attach descriptors for modifying configuration values.
    setattr(SlurmConf, _snakecase(field), property(*_gen_descriptors(field)))
