#!/usr/bin/env python3
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

"""Unit tests for base editor functions."""

import os
import stat
from pathlib import Path

from constants import EXAMPLE_SLURM_CONFIG
from pyfakefs.fake_filesystem_unittest import TestCase

from slurmutils import slurmconfig
from slurmutils.core.editor import _set_file_permissions  # noqa


class TestBaseEditor(TestCase):
    """Unit tests for base editor functions."""

    def setUp(self) -> None:
        self.setUpPyfakefs()
        self.fs.create_file("/etc/slurm/slurm.conf", contents=EXAMPLE_SLURM_CONFIG)

    def test_set_file_permissions(self) -> None:
        """Test the `set_file_permissions` function."""
        target = Path("/etc/slurm/slurm.conf")
        _set_file_permissions(target, mode=0o600, user=os.getuid(), group=os.getgid())
        f_info = target.stat()
        self.assertEqual("-rw-------", stat.filemode(f_info.st_mode))
        self.assertEqual(os.getuid(), f_info.st_uid)
        self.assertEqual(os.getgid(), f_info.st_gid)

    def test_loader_fail(self) -> None:
        """Test that `FileNotFoundError` is raised when attempting to load non-existent file."""
        self.fs.remove("/etc/slurm/slurm.conf")
        with self.assertRaises(FileNotFoundError):
            slurmconfig.load("/etc/slurm/slurm.conf")

    def test_dumper_first_write(self) -> None:
        """Test that `dumper` succeeds when there is no pre-existing config file."""
        self.fs.remove("/etc/slurm/slurm.conf")
        slurmconfig.dump(slurmconfig.loads(EXAMPLE_SLURM_CONFIG), "/etc/slurm/slurm.conf")
