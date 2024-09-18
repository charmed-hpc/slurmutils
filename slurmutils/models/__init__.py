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

"""Data models for common Slurm objects."""

from .cgroup import CgroupConfig as CgroupConfig
from .slurm import DownNodes as DownNodes
from .slurm import FrontendNode as FrontendNode
from .slurm import Node as Node
from .slurm import NodeSet as NodeSet
from .slurm import Partition as Partition
from .slurm import SlurmConfig as SlurmConfig
from .slurmdbd import SlurmdbdConfig as SlurmdbdConfig
