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

"""Model representing the `acct_gather.conf` configuration file."""

__all__ = ["AcctGatherConfig", "AcctGatherConfigEditor"]

from typing import Annotated, Any

from .core.base import Metadata, Model, classproperty
from .core.callback import CommaSepCallback, SemicolonDictCallback, StrBoolCallback
from .core.editor import BaseEditor
from .core.schema import ACCT_GATHER_CONFIG_MODEL_SCHEMA


class AcctGatherConfig(Model):
    """Model representing the `acct_gather.conf` configuration file."""

    energy_ipmi_frequency: int | None
    energy_ipmi_calc_adjustment: Annotated[bool | None, Metadata(callback=StrBoolCallback)]
    energy_ipmi_power_sensors: Annotated[
        dict[str, list[int]] | None,
        Metadata(callback=SemicolonDictCallback),
    ]
    energy_ipmi_username: str | None
    energy_ipmi_password: str | None
    energy_ipmi_frequency: int | None
    energy_ipmi_timeout: int | None
    profile_hdf5_dir: str | None
    profile_hdf5_default: Annotated[list[str] | None, Metadata(callback=CommaSepCallback)]
    profile_influxdb_database: str | None
    profile_influxdb_default: Annotated[list[str] | None, Metadata(callback=CommaSepCallback)]
    profile_influxdb_host: str | None
    profile_influxdb_pass: str | None
    profile_influxdb_rt_policy: str | None
    profile_influxdb_user: str | None
    profile_influxdb_timeout: int | None
    infiniband_ofed_port: int | None
    sysfs_interfaces: Annotated[list[str] | None, Metadata(callback=CommaSepCallback)]

    @classproperty
    def __model_schema__(cls) -> dict[str, Any]:  # noqa N805
        return ACCT_GATHER_CONFIG_MODEL_SCHEMA


class AcctGatherConfigEditor(BaseEditor):
    """Editor for the `acct_gather.conf` configuration file."""

    @property
    def __model__(self) -> type[Model]:  # noqa D105
        return AcctGatherConfig
