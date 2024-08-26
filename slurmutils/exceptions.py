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

"""Exceptions raised by Slurm utilities in this package."""


class BaseError(Exception):
    """Base exception for errors in `slurmutils` module."""

    @property
    def message(self) -> str:
        """Return message passed as argument to exception."""
        return self.args[0]


class EditorError(BaseError):
    """Raise when a Slurm configuration editor encounters an error."""


class ModelError(BaseError):
    """Raise when a Slurm configuration model encounters an error."""
