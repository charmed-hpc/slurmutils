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
from functools import wraps
from os import path

_logger = logging.getLogger("slurmutils")


def loader(func):
    """Wrap function that loads configuration data from file."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        fin = args[0]
        if not path.exists(fin):
            raise FileNotFoundError(f"could not locate {fin}")

        _logger.debug("reading contents of %s", fin)
        return func(*args, **kwargs)

    return wrapper


def dumper(func):
    """Wrap function that dumps configuration data to file."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        fout = args[1]
        if path.exists(fout):
            _logger.debug("overwriting current contents of %s", fout)

        _logger.debug("updating contents of %s", fout)
        return func(*args, **kwargs)

    return wrapper
