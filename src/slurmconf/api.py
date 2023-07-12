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

__all__ = ["SlurmConf"]

import logging
import os
import pathlib
import re
from dataclasses import make_dataclass
from itertools import chain
from typing import List, Union

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
        for token in line.split():
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
        "nodes": [],
        "down_nodes": [],
        "frontend_nodes": [],
        "nodesets": [],
        "partitions": [],
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
            conf_opts["nodes"].append(Node.from_line(line))
        elif opt == "DownNodes":
            conf_opts["down_nodes"].append(DownNode.from_line(line))
        elif opt == "FrontendName":
            conf_opts["frontend_nodes"].append(FrontendNode.from_line(line))
        elif opt == "NodeSet":
            conf_opts["nodesets"].append(NodeSet.from_line(line))
        elif opt == "PartitionName":
            conf_opts["partitions"].append(Partition.from_line(line))
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
        if hasattr(SlurmConfOpts, opt):
            if render_callback := getattr(SlurmConfOpts, opt).render:
                value = render_callback(value)
            conf_render.append(f"{opt}={value}")
        else:
            _logger.warning(f"Unrecognized configuration option: {opt}")

    for struct in chain(nodes, down_nodes, frontend_nodes, nodesets, partitions):
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
        self.load(self._conf_file)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Render and dump metadata file and configuration file when leaving context."""
        self.dump(self._conf_file)

    @property
    def comments(self) -> List[Comment]:
        """Get comments in SLURM configuration file."""
        return self._data["comments"]

    @property
    def nodes(self) -> List[Node]:
        """Get nodes in SLURM configuration file."""
        return self._data["nodes"]

    @property
    def down_nodes(self) -> List[DownNode]:
        """Get down nodes in SLURM configuration file."""
        return self._data["down_nodes"]

    @property
    def frontend_nodes(self) -> List[FrontendNode]:
        """Get frontend nodes in SLURM configuration file."""
        return self._data["frontend_nodes"]

    @property
    def nodesets(self) -> List[NodeSet]:
        """Get nodesets in SLURM configuration file."""
        return self._data["nodesets"]

    @property
    def partitions(self) -> List[Partition]:
        """Get partitions in SLURM configuration file."""
        return self._data["partitions"]

    def load(self, conf_file: Union[str, os.PathLike] = SLURM_CONF_FILE) -> None:
        """Load metadata file.

        Args:
            conf_file: Path of metadata file to load.
        """
        if (conf := pathlib.Path(conf_file)).exists():
            self._data = _parse(conf.read_text(encoding="ascii"))
        else:
            _logger.warning(f"{conf_file} not found")

    def dump(self, conf_file: Union[str, os.PathLike] = SLURM_CONF_FILE) -> None:
        """Render and dump metadata file and slurm configuration file.

        Args:
            conf_file: Filesystem location to dump SLURM configuration file.
        """
        if (conf := pathlib.Path(conf_file)).exists():
            _logger.debug(f"Overwriting pre-existing {conf_file}")

        conf.write_text(_render(self._data), encoding="ascii")


# Generate SLURM configuration API.
for field in SlurmConfOpts._fields:
    # Attach descriptors for modifying configuration values.
    setattr(SlurmConf, _snakecase(field), property(*_gen_descriptors(field)))
