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

"""Model representing the `oci.conf` configuration file."""

__all__ = ["OCIConfig", "OCIConfigEditor"]

from typing import Annotated, Any

from .core.base import Metadata, Model, classproperty
from .core.callback import (
    BoolCallback,
    CommaSepCallback,
    MultilineCallback,
    QuoteCallback,
)
from .core.editor import BaseEditor
from .core.schema import OCI_CONFIG_MODEL_SCHEMA


class OCIConfig(Model):
    """Model representing the `oci.conf` configuration file."""

    container_path: str | None
    create_env_file: str | None
    debug_flags: Annotated[list[str] | None, Metadata(callback=CommaSepCallback)]
    disable_cleanup: Annotated[bool | None, Metadata(callback=BoolCallback)]
    disable_hooks: Annotated[list[str] | None, Metadata(callback=CommaSepCallback)]
    env_exclude: Annotated[str | None, Metadata(callback=QuoteCallback)]
    mount_spool_dir: str | None
    run_time_env_exclude: Annotated[str | None, Metadata(callback=QuoteCallback)]
    file_debug: str | None
    ignore_file_config_json: Annotated[bool | None, Metadata(callback=BoolCallback)]
    run_time_create: Annotated[str | None, Metadata(callback=QuoteCallback)]
    run_time_delete: Annotated[str | None, Metadata(callback=QuoteCallback)]
    run_time_kill: Annotated[str | None, Metadata(callback=QuoteCallback)]
    run_time_query: Annotated[str | None, Metadata(callback=QuoteCallback)]
    run_time_run: Annotated[str | None, Metadata(callback=QuoteCallback)]
    run_time_start: Annotated[str | None, Metadata(callback=QuoteCallback)]
    srun_path: str | None
    srun_args: Annotated[list[str] | None, Metadata(unique=False, callback=MultilineCallback)]
    std_io_debug: str | None
    syslog_debug: str | None

    @classproperty
    def __model_schema__(self) -> dict[str, Any]:  # noqa N805
        return OCI_CONFIG_MODEL_SCHEMA


class OCIConfigEditor(BaseEditor):
    """Editor for the `oci.conf` configuration file."""

    @property
    def __model__(self) -> type[Model]:  # noqa D105
        return OCIConfig
