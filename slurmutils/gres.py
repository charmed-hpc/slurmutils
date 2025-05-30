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

"""Models representing the `gres.conf` configuration file."""

__all__ = ["Gres", "GresList", "GresMapping", "GresConfig", "GresConfigEditor"]

from typing import Annotated, Any, Callable

from .core.base import (
    Metadata,
    Mode,
    Model,
    ModelList,
    ModelMapping,
    classproperty,
    make_model_builder,
)
from .core.callback import CommaSepCallback
from .core.editor import BaseEditor
from .core.schema import (
    GRES_CONFIG_MODEL_SCHEMA,
    GRES_LIST_MODEL_SCHEMA,
    GRES_MAPPING_MODEL_SCHEMA,
    GRES_MODEL_SCHEMA,
)


class Gres(Model):
    """Model representing a generic resource declaration in the `gres.conf` configuration file."""

    name: Annotated[str | None, Metadata(primary=True)]
    autodetect: str | None
    count: int | str | None
    cores: Annotated[list[int | str] | None, Metadata(callback=CommaSepCallback)]
    file: str | None
    flags: Annotated[list[str] | None, Metadata(callback=CommaSepCallback)]
    links: Annotated[list[int] | None, Metadata(callback=CommaSepCallback)]
    multiplefiles: Annotated[list[str] | None, Metadata(callback=CommaSepCallback)]
    nodename: str | None
    type: str | None

    @classproperty
    def __model_schema__(cls) -> dict[str, Any]:  # noqa N804
        return GRES_MODEL_SCHEMA

    @classproperty
    def __model_mode__(cls) -> Mode:  # noqa N804
        return Mode.ONELINE


class GresList(ModelList[Gres]):
    """List of generic resource declarations that share the same name."""

    @classproperty
    def __model_schema__(cls) -> dict[str, Any]:  # noqa N804
        return GRES_LIST_MODEL_SCHEMA

    @classproperty
    def __model_builder__(cls) -> Callable[[Any], Any] | None:  # noqa N804
        return _gres_list_model_builder


class GresMapping(ModelMapping[str, GresList]):
    """Mapping of generic resource names to generic resource declarations."""

    @classproperty
    def __model_schema__(cls) -> dict[str, Any]:  # noqa N804
        return GRES_MAPPING_MODEL_SCHEMA

    @classproperty
    def __model_builder__(cls) -> Callable[[Any], Any] | None:  # noqa N804
        return _gres_mapping_model_builder


class GresConfig(Model):
    """Model representing the `gres.conf` configuration file."""

    auto_detect: str | None
    gres: Annotated[
        GresMapping,
        Metadata(origin="gres", alias="name", unique=False, default_factory=lambda: GresMapping()),
    ]

    @classproperty
    def __model_schema__(cls) -> dict[str, Any]:  # noqa N804
        return GRES_CONFIG_MODEL_SCHEMA

    @classproperty
    def __model_builder__(cls) -> Callable[[Any], Any] | None:  # noqa N804
        return _gres_config_model_builder


class GresConfigEditor(BaseEditor):
    """Editor for the `gres.conf` configuration file."""

    @property
    def __model__(self) -> type[Model]:  # noqa D105
        return GresConfig


_gres_list_model_builder = make_model_builder(Gres)
_gres_mapping_model_builder = make_model_builder(GresList)
_gres_config_model_builder = make_model_builder(GresMapping)
