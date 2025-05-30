# Copyright 2025 Canonical Ltd.
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

import os
from collections.abc import Iterator
from contextlib import contextmanager
from typing import Any

from .core.base import Model, classproperty
from .core.editor import BaseEditor

class CGroupConfig(Model):
    cgroup_mountpoint: str | None
    cgroup_plugin: str | None
    systemd_timeout: int | None
    ignore_systemd: bool | None
    ignore_systemd_on_failure: bool
    enable_controllers: bool | None
    allowed_ram_space: float | None
    allowed_swap_space: float | None
    constrain_cores: bool | None
    constrain_devices: bool | None
    constrain_ram_space: bool | None
    constrain_swap_space: bool | None
    max_ram_percent: float | None
    max_swap_percent: float | None
    memory_swappiness: int | None
    min_ram_space: float | None
    signal_children_processes: bool | None
    @classproperty
    def __model_schema__(cls) -> dict[str, Any]: ...  # noqa N804

class CGroupConfigEditor(BaseEditor):
    @property
    def __model__(self) -> type[CGroupConfig]: ...
    def dump(
        self,
        obj: CGroupConfig,
        /,
        file: str | os.PathLike,
        *,
        mode: int = 0o644,
        user: str | int | None = None,
        group: str | int | None = None,
    ) -> None: ...
    def dumps(self, obj: CGroupConfig, /) -> str: ...
    def load(self, file: str | os.PathLike, /) -> CGroupConfig: ...
    def loads(self, s: str, /) -> CGroupConfig: ...
    @contextmanager
    def edit(
        self,
        file: str | os.PathLike,
        *,
        mode: int = 0o644,
        user: int | str | None = None,
        group: int | str | None = None,
    ) -> Iterator[CGroupConfig]: ...
