#!/usr/bin/env python3
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

"""Unit tests for the cgroup.conf editor."""

import unittest
from pathlib import Path

from slurmutils.editors import cgroupconfig


EXAMPLE_CGROUP_CONF = """#
# `cgroup.conf` file generated at 2024-09-18 15:10:44.652017 by slurmutils.
#
ConstrainCores=yes
ConstrainDevices=yes
ConstrainRAMSpace=yes
ConstrainSwapSpace=yes
"""


class TestCgroupConfigEditor(unittest.TestCase):
    """Unit tests for cgroup.conf file editor."""

    def setUp(self) -> None:
        Path("cgroup.conf").write_text(EXAMPLE_CGROUP_CONF)

    def test_loads(self) -> None:
        """Test `loads` method of the cgroupconfig module."""
        config = cgroupconfig.loads(EXAMPLE_CGROUP_CONF)
        self.assertEqual(config.constrain_cores, "yes")
        self.assertEqual(config.constrain_devices, "yes")
        self.assertEqual(config.constrain_ram_space, "yes")
        self.assertEqual(config.constrain_swap_space, "yes")

    def test_dumps(self) -> None:
        """Test `dumps` method of the cgroupconfig module."""
        config = cgroupconfig.loads(EXAMPLE_CGROUP_CONF)
        # The new config and old config should not be equal since the
        # timestamps in the header will be different.
        self.assertNotEqual(cgroupconfig.dumps(config), EXAMPLE_CGROUP_CONF)

    def test_edit(self) -> None:
        """Test `edit` context manager from the cgroupconfig module."""
        with cgroupconfig.edit("cgroup.conf") as config:
            config.constrain_cores = "no"
            config.constrain_devices = "no"
            config.constrain_ram_space = "no"
            config.constrain_swap_space = "no"

        config = cgroupconfig.load("cgroup.conf")
        self.assertEqual(config.constrain_cores, "no")
        self.assertEqual(config.constrain_devices, "no")
        self.assertEqual(config.constrain_ram_space, "no")
        self.assertEqual(config.constrain_swap_space, "no")

    def tearDown(self) -> None:
        Path("cgroup.conf").unlink()
