# Copyright 2024-2025 Canonical Ltd.
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

"""Utilities and APIs for interfacing with the Slurm workload manager."""

__all__ = [
    # From `acctgather.py`
    "AcctGatherConfig",
    "AcctGatherConfigEditor",
    # From `cgroup.py`
    "CGroupConfig",
    "CGroupConfigEditor",
    # From `core/*.py`
    "Model",
    "ModelList",
    "ModelMapping",
    "BaseEditor",
    "Callback",
    # From `exceptions.py`
    "ModelError",
    # From `gres.py`
    "Gres",
    "GresConfig",
    "GresConfigEditor",
    "GresList",
    "GresMapping",
    # From `oci.py`
    "OCIConfig",
    "OCIConfigEditor",
    # From `slurm.py`
    "DownNodes",
    "DownNodesList",
    "FrontendNode",
    "FrontendNodeMapping",
    "Node",
    "NodeMapping",
    "NodeSet",
    "NodeSetMapping",
    "Partition",
    "PartitionMapping",
    "SlurmConfig",
    "SlurmConfigEditor",
    # From `slurmdbd.py`
    "SlurmdbdConfig",
    "SlurmdbdConfigEditor",
    # From `utils.py`
    "calculate_rs",
    # Local
    "acctgatherconfig",
    "cgroupconfig",
    "gresconfig",
    "slurmconfig",
    "slurmdbdconfig",
]


from .acctgather import AcctGatherConfig, AcctGatherConfigEditor
from .cgroup import CGroupConfig, CGroupConfigEditor
from .core.base import Model, ModelList, ModelMapping
from .core.callback import Callback
from .core.editor import BaseEditor
from .exceptions import ModelError
from .gres import Gres, GresConfig, GresConfigEditor, GresList, GresMapping
from .oci import OCIConfig, OCIConfigEditor
from .slurm import (
    DownNodes,
    DownNodesList,
    FrontendNode,
    FrontendNodeMapping,
    Node,
    NodeMapping,
    NodeSet,
    NodeSetMapping,
    Partition,
    PartitionMapping,
    SlurmConfig,
    SlurmConfigEditor,
)
from .slurmdbd import SlurmdbdConfig, SlurmdbdConfigEditor
from .utils import calculate_rs

acctgatherconfig = AcctGatherConfigEditor()
cgroupconfig = CGroupConfigEditor()
gresconfig = GresConfigEditor()
ociconfig = OCIConfigEditor()
slurmconfig = SlurmConfigEditor()
slurmdbdconfig = SlurmdbdConfigEditor()
