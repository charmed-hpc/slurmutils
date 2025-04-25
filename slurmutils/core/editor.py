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

"""Base classes and functions for composing Slurm configuration editors."""

import os
import shutil
from abc import ABC, abstractmethod
from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path

from .base import Model


def _set_file_permissions(
    file: str | os.PathLike,
    *,
    mode: int = 0o644,
    user: str | int | None = None,
    group: str | int | None = None,
) -> None:
    """Set permissions on a configuration file.

    Args:
        file: File to apply permission settings to.
        mode: Access mode to apply to file. (Default: rw-r--r--)
        user: User to set as owner of file. (Default: $USER)
        group: Group to set as owner of file. (Default: None)
    """
    Path(file).chmod(mode=mode)
    if user is None:
        user = os.getuid()

    shutil.chown(file, user, group)


class Editor(ABC):
    """Base class for defining Slurm configuration file editors."""

    def dump(
        self,
        obj: Model,
        /,
        file: str | os.PathLike,
        *,
        mode: int = 0o644,
        user: str | int | None = None,
        group: str | int | None = None,
    ) -> None:
        """Marshal a configuration model into a file."""
        Path(file).write_text(self.dumps(obj) + "\n")
        _set_file_permissions(file, mode=mode, user=user, group=group)

    def dumps(self, obj: Model, /) -> str:
        """Marshal a configuration model into a `str`."""
        return str(obj)

    def load(self, file: str | os.PathLike, /) -> Model:
        """Parse the contents of a file into a configuration model.

        Raises:
            FileNotFoundError: Raised if `file` does not exist.
        """
        return self.loads(Path(file).read_text())

    def loads(self, s: str, /) -> Model:
        """Parse a `str` into a configuration model."""
        return self.__model__.from_str(s)

    @contextmanager
    def edit(
        self,
        file: str | os.PathLike,
        *,
        mode: int = 0o644,
        user: int | str | None = None,
        group: int | str | None = None,
    ) -> Generator[Model, None, None]:
        """Edit a configuration file.

        Args:
            file:
                Configuration file to edit.
                An empty model will be created if the file does not exist.
            mode: Access mode to set on the configuration file. (Default: rw-r--r--)
            user: User to set as owner of the configuration file. (Default: $USER)
            group: Group to set as owner of the configuration file. (Default: None)
        """
        if not os.path.exists(file):
            model = self.__model__()
        else:
            model = self.load(file)

        yield model
        self.dump(model, file, mode=mode, user=user, group=group)

    @property
    @abstractmethod
    def __model__(self) -> type[Model]:
        """Model used by editor for interfacing with configuration files."""
