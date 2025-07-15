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
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from typing import Any

from .core.base import Mode, Model, ModelList, ModelMapping, classproperty
from .core.editor import BaseEditor

class Gres(Model):
    name: str | None
    autodetect: str | None
    count: int | str | None
    cores: list[int | str] | None
    file: str | None
    flags: list[str] | None
    links: list[int] | None
    multiplefiles: list[str] | None
    nodename: str | None
    type: str | None
    @classproperty
    def __model_schema__(cls) -> dict[str, Any]: ...  # noqa N804
    @classproperty
    def __model_mode__(cls) -> Mode: ...  # noqa N804

class GresList(ModelList[Gres]):
    @classproperty
    def __model_schema__(cls) -> dict[str, Any]: ...  # noqa N804
    @classproperty
    def __model_builder__(cls) -> Callable[[Any], Any] | None: ...  # noqa N804

class GresMapping(ModelMapping[str, GresList]):
    @classproperty
    def __model_schema__(cls) -> dict[str, Any]: ...  # noqa N804
    @classproperty
    def __model_builder__(cls) -> Callable[[Any], Any] | None: ...  # noqa N804

class GresConfig(Model):
    auto_detect: str | None
    gres: GresMapping
    @classproperty
    def __model_schema__(cls) -> dict[str, Any]: ...  # noqa N804
    @classproperty
    def __model_builder__(cls) -> Callable[[Any], Any] | None: ...  # noqa N804

class GresConfigEditor(BaseEditor):
    @property
    def __model__(self) -> type[GresConfig]: ...
    def dump(
        self,
        obj: GresConfig,
        /,
        file: str | os.PathLike,
        *,
        mode: int = 0o644,
        user: str | int | None = None,
        group: str | int | None = None,
    ) -> None: ...
    def dumps(self, obj: GresConfig, /) -> str: ...
    def load(self, file: str | os.PathLike, /) -> GresConfig: ...
    def loads(self, s: str, /) -> GresConfig: ...
    @contextmanager
    def edit(
        self,
        file: str | os.PathLike,
        *,
        mode: int = 0o644,
        user: int | str | None = None,
        group: int | str | None = None,
    ) -> Iterator[GresConfig]: ...

_gres_list_model_builder: Callable[[Any], Any] = ...
_gres_mapping_model_builder: Callable[[Any], Any] = ...
_gres_config_model_builder: Callable[[Any], Any] = ...
