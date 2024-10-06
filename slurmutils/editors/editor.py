# Copyright 2024 Canonical Ltd.
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

"""Base methods for Slurm workload manager configuration file editors."""

import logging
import os
import shutil
from functools import wraps
from pathlib import Path
from typing import Optional, Union

_logger = logging.getLogger("slurmutils")


def set_file_permissions(
    file: Union[str, os.PathLike],
    mode: int = 0o644,
    user: Optional[Union[str, int]] = None,
    group: Optional[Union[str, int]] = None,
) -> None:
    """Set file permissions to configuration file.

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


def loader(func):
    """Wrap function that loads configuration data from file."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        fin = args[0]
        if not os.path.exists(fin):
            raise FileNotFoundError(f"could not locate {fin}")

        _logger.debug("reading contents of %s", fin)
        return func(*args, **kwargs)

    return wrapper


def dumper(func):
    """Wrap function that dumps configuration data to file."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        fout = args[1]
        if os.path.exists(fout):
            _logger.debug("overwriting current contents of %s", fout)

        _logger.debug("updating contents of %s", fout)
        return func(*args, **kwargs)

    return wrapper
