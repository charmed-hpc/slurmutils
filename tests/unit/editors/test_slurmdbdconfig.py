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

"""Unit tests for the slurmdbd.conf editor."""


from constants import EXAMPLE_SLURMDBD_CONFIG
from pyfakefs.fake_filesystem_unittest import TestCase

from slurmutils.editors import slurmdbdconfig


class TestSlurmdbdConfigEditor(TestCase):
    """Unit tests for the slurmdbd.conf file editor."""

    def setUp(self) -> None:
        self.setUpPyfakefs()
        self.fs.create_file("/etc/slurm/slurmdbd.conf", contents=EXAMPLE_SLURMDBD_CONFIG)

    def test_loads(self) -> None:
        """Test `loads` method of the slurmdbdconfig module."""
        config = slurmdbdconfig.loads(EXAMPLE_SLURMDBD_CONFIG)
        self.assertListEqual(config.plugin_dir, ["/all/these/cool/plugins"])
        self.assertDictEqual(config.auth_alt_parameters, {"jwt_key": "16549684561684@"})
        self.assertEqual(config.slurm_user, "slurm")
        self.assertEqual(config.log_file, "/var/log/slurmdbd.log")

    def test_dumps(self) -> None:
        """Test `dumps` method of the slurmdbdconfig module."""
        config = slurmdbdconfig.loads(EXAMPLE_SLURMDBD_CONFIG)
        # The new config and old config should not be equal since the
        # timestamps in the header will be different.
        self.assertNotEqual(slurmdbdconfig.dumps(config), EXAMPLE_SLURMDBD_CONFIG)

    def test_edit(self) -> None:
        """Test `edit` context manager from the slurmdbdconfig module."""
        with slurmdbdconfig.edit("/etc/slurm/slurmdbd.conf") as config:
            config.archive_usage = "yes"
            config.log_file = "/var/spool/slurmdbd.log"
            config.debug_flags = ["DB_EVENT", "DB_JOB", "DB_USAGE"]
            del config.auth_alt_types
            del config.auth_alt_parameters

        config = slurmdbdconfig.load("/etc/slurm/slurmdbd.conf")
        self.assertEqual(config.archive_usage, "yes")
        self.assertEqual(config.log_file, "/var/spool/slurmdbd.log")
        self.assertListEqual(config.debug_flags, ["DB_EVENT", "DB_JOB", "DB_USAGE"])
        self.assertIsNone(config.auth_alt_types)
        self.assertIsNone(config.auth_alt_parameters)
