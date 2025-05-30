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

"""Model representing the `cgroup.conf` configuration file."""

__all__ = ["CGroupConfig", "CGroupConfigEditor"]

from typing import Annotated, Any

from .core.base import Metadata, Model, classproperty
from .core.callback import StrBoolCallback
from .core.editor import BaseEditor
from .core.schema import CGROUP_CONFIG_MODEL_SCHEMA


class CGroupConfig(Model):
    """Model representing the `cgroup.conf` configuration file.."""

    cgroup_mountpoint: str | None
    cgroup_plugin: str | None
    systemd_timeout: int | None
    ignore_systemd: Annotated[bool | None, Metadata(callback=StrBoolCallback)]
    ignore_systemd_on_failure: Annotated[bool, Metadata(callback=StrBoolCallback)]
    enable_controllers: Annotated[bool | None, Metadata(callback=StrBoolCallback)]
    allowed_ram_space: float | None
    allowed_swap_space: float | None
    constrain_cores: Annotated[bool | None, Metadata(callback=StrBoolCallback)]
    constrain_devices: Annotated[bool | None, Metadata(callback=StrBoolCallback)]
    constrain_ram_space: Annotated[bool | None, Metadata(callback=StrBoolCallback)]
    constrain_swap_space: Annotated[bool | None, Metadata(callback=StrBoolCallback)]
    max_ram_percent: float | None
    max_swap_percent: float | None
    memory_swappiness: int | None
    min_ram_space: float | None
    signal_children_processes: Annotated[bool | None, Metadata(callback=StrBoolCallback)]

    @classproperty
    def __model_schema__(cls) -> dict[str, Any]:  # noqa N805
        return CGROUP_CONFIG_MODEL_SCHEMA


class CGroupConfigEditor(BaseEditor):
    """Editor for the `cgroup.conf` configuration file."""

    @property
    def __model__(self) -> type[Model]:  # noqa D105
        return CGroupConfig
