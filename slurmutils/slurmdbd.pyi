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

class SlurmdbdConfig(Model):
    allow_no_def_acct: bool | None
    all_resources_absolute: bool | None
    archive_dir: str | None
    archive_events: bool | None
    archive_jobs: bool | None
    archive_resvs: bool | None
    archive_script: str | None
    archive_steps: str | None
    archive_suspend: str | None
    archive_txn: str | None
    archive_usage: str | None
    auth_alt_types: list[str] | None
    auth_alt_parameters: dict[str, str] | None
    auth_info: dict[str, str | bool] | None
    auth_type: str | None
    commit_delay: int | None
    communication_parameters: dict[str, int | bool] | None
    dbd_addr: str | None
    dbd_backup_host: str | None
    dbd_host: str | None
    dbd_port: int | None
    debug_flags: list[str] | None
    debug_level: str | None
    debug_level_syslog: str | None
    default_qos: str | None
    disable_coord_dbd: bool | None
    hash_plugin: str | None
    log_file: str | None
    log_time_format: str | None
    max_query_time_range: str | int | None
    message_timeout: str | None
    parameters: dict[str, bool] | None
    pid_file: str | None
    plugin_dir: list[str] | None
    private_data: list[str] | None
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
    storage_parameters: dict[str, str | list[str]] | None
    storage_pass: str | None
    storage_port: int | None
    storage_type: str | None
    storage_user: str | None
    tcp_timeout: int | None
    track_slurmctld_down: bool | None
    track_wc_key: bool | None
    @classproperty
    def __model_schema__(cls) -> dict[str, Any]: ...  # noqa N804

class SlurmdbdConfigEditor(BaseEditor):
    @property
    def __model__(self) -> type[SlurmdbdConfig]: ...
    def dump(
        self,
        obj: SlurmdbdConfig,
        /,
        file: str | os.PathLike,
        *,
        mode: int = 0o644,
        user: str | int | None = None,
        group: str | int | None = None,
    ) -> None: ...
    def dumps(self, obj: SlurmdbdConfig, /) -> str: ...
    def load(self, file: str | os.PathLike, /) -> SlurmdbdConfig: ...
    def loads(self, s: str, /) -> SlurmdbdConfig: ...
    @contextmanager
    def edit(
        self,
        file: str | os.PathLike,
        *,
        mode: int = 0o644,
        user: int | str | None = None,
        group: int | str | None = None,
    ) -> Iterator[SlurmdbdConfig]: ...
