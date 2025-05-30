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

class AcctGatherConfig(Model):
    energy_ipmi_frequency: int | None
    energy_ipmi_calc_adjustment: bool | None
    energy_ipmi_power_sensors: dict[str, list[int]] | None
    energy_ipmi_username: str | None
    energy_ipmi_password: str | None
    energy_ipmi_frequency: int | None
    energy_ipmi_timeout: int | None
    profile_hdf5_dir: str | None
    profile_hdf5_default: list[str] | None
    profile_influxdb_database: str | None
    profile_influxdb_default: list[str] | None
    profile_influxdb_host: str | None
    profile_influxdb_pass: str | None
    profile_influxdb_rt_policy: str | None
    profile_influxdb_user: str | None
    profile_influxdb_timeout: int | None
    infiniband_ofed_port: int | None
    sysfs_interfaces: list[str] | None
    @classproperty
    def __model_schema__(cls) -> dict[str, Any]: ...  # noqa N804

class AcctGatherConfigEditor(BaseEditor):
    @property
    def __model__(self) -> type[AcctGatherConfig]: ...
    def dump(
        self,
        obj: AcctGatherConfig,
        /,
        file: str | os.PathLike,
        *,
        mode: int = 0o644,
        user: str | int | None = None,
        group: str | int | None = None,
    ) -> None: ...
    def dumps(self, obj: AcctGatherConfig, /) -> str: ...
    def load(self, file: str | os.PathLike, /) -> AcctGatherConfig: ...
    def loads(self, s: str, /) -> AcctGatherConfig: ...
    @contextmanager
    def edit(
        self,
        file: str | os.PathLike,
        *,
        mode: int = 0o644,
        user: int | str | None = None,
        group: int | str | None = None,
    ) -> Iterator[AcctGatherConfig]: ...
