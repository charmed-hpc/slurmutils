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

"""Model representing the `slurmdbd.conf` configuration file."""

__all__ = ["SlurmdbdConfig", "SlurmdbdConfigEditor"]

from typing import Annotated, Any

from .core.base import Metadata, Model, classproperty
from .core.callback import (
    ColonSepCallback,
    CommaDictCallback,
    CommaSepCallback,
    StrBoolCallback,
)
from .core.editor import BaseEditor
from .core.schema import SLURMDBD_CONFIG_MODEL_SCHEMA


class SlurmdbdConfig(Model):
    """Model representing the `slurmdbd.conf` configuration file."""

    allow_no_def_acct: Annotated[bool | None, Metadata(callback=StrBoolCallback)]
    all_resources_absolute: Annotated[bool | None, Metadata(callback=StrBoolCallback)]
    archive_dir: str | None
    archive_events: Annotated[bool | None, Metadata(callback=StrBoolCallback)]
    archive_jobs: Annotated[bool | None, Metadata(callback=StrBoolCallback)]
    archive_resvs: Annotated[bool | None, Metadata(callback=StrBoolCallback)]
    archive_script: str | None
    archive_steps: Annotated[str | None, Metadata(callback=StrBoolCallback)]
    archive_suspend: Annotated[str | None, Metadata(callback=StrBoolCallback)]
    archive_txn: Annotated[str | None, Metadata(callback=StrBoolCallback)]
    archive_usage: Annotated[str | None, Metadata(callback=StrBoolCallback)]
    auth_alt_types: Annotated[list[str] | None, Metadata(callback=CommaSepCallback)]
    auth_alt_parameters: Annotated[dict[str, str] | None, Metadata(callback=CommaDictCallback)]
    auth_info: Annotated[dict[str, str | bool] | None, Metadata(callback=CommaDictCallback)]
    auth_type: str | None
    commit_delay: int | None
    communication_parameters: Annotated[
        dict[str, int | bool] | None,
        Metadata(callback=CommaDictCallback),
    ]
    dbd_addr: str | None
    dbd_backup_host: str | None
    dbd_host: str | None
    dbd_port: int | None
    debug_flags: Annotated[list[str] | None, Metadata(callback=CommaSepCallback)]
    debug_level: str | None
    debug_level_syslog: str | None
    default_qos: str | None
    disable_coord_dbd: Annotated[bool | None, Metadata(callback=StrBoolCallback)]
    hash_plugin: str | None
    log_file: str | None
    log_time_format: str | None
    max_query_time_range: str | int | None
    message_timeout: str | None
    parameters: Annotated[dict[str, bool] | None, Metadata(callback=CommaDictCallback)]
    pid_file: str | None
    plugin_dir: Annotated[list[str] | None, Metadata(callback=ColonSepCallback)]
    private_data: Annotated[list[str] | None, Metadata(callback=CommaSepCallback)]
    purge_event_after: str | None
    purge_job_after: str | None
    purge_resv_after: str | None
    purge_step_after: str | None
    purge_suspend_after: str | None
    purge_txn_after: str | None
    purge_usage_after: str | None
    slurm_user: str | None
    storage_backup_host: str | None
    storage_host: str | None
    storage_loc: str | None
    storage_parameters: Annotated[
        dict[str, str | list[str]] | None,
        Metadata(callback=CommaDictCallback),
    ]
    storage_pass: str | None
    storage_port: int | None
    storage_type: str | None
    storage_user: str | None
    tcp_timeout: int | None
    track_slurmctld_down: Annotated[bool | None, Metadata(callback=StrBoolCallback)]
    track_wc_key: Annotated[bool | None, Metadata(callback=StrBoolCallback)]

    @classproperty
    def __model_schema__(cls) -> dict[str, Any]:  # noqa N805
        return SLURMDBD_CONFIG_MODEL_SCHEMA


class SlurmdbdConfigEditor(BaseEditor):
    """Editor for the `slurmdbd.conf` configuration file."""

    @property
    def __model__(self) -> type[Model]:  # noqa D105
        return SlurmdbdConfig
