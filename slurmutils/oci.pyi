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

class OCIConfig(Model):
    container_path: str | None
    create_env_file: str | None
    debug_flags: list[str] | None
    disable_cleanup: bool | None
    disable_hooks: list[str] | None
    env_exclude: str | None
    mount_spool_dir: str | None
    run_time_env_exclude: str | None
    file_debug: str | None
    ignore_file_config_json: bool | None
    run_time_create: str | None
    run_time_delete: str | None
    run_time_kill: str | None
    run_time_query: str | None
    run_time_run: str | None
    run_time_start: str | None
    srun_path: str | None
    srun_args: list[str] | None
    std_io_debug: str | None
    syslog_debug: str | None
    @classproperty
    def __model_schema__(self) -> dict[str, Any]: ...  # noqa N804

class OCIConfigEditor(BaseEditor):
    @property
    def __model__(self) -> type[OCIConfig]: ...
    def dump(
        self,
        obj: OCIConfig,
        /,
        file: str | os.PathLike,
        *,
        mode: int = 0o644,
        user: str | int | None = None,
        group: str | int | None = None,
    ) -> None: ...
    def dumps(self, obj: OCIConfig, /) -> str: ...
    def load(self, file: str | os.PathLike, /) -> OCIConfig: ...
    def loads(self, s: str, /) -> OCIConfig: ...
    @contextmanager
    def edit(
        self,
        file: str | os.PathLike,
        *,
        mode: int = 0o644,
        user: int | str | None = None,
        group: int | str | None = None,
    ) -> Iterator[OCIConfig]: ...
