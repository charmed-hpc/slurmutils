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

import unittest
from pathlib import Path

from slurmutils.editors import slurmdbdconfig

example_slurmdbd_conf = """#
# `slurmdbd.conf` file generated at 2024-01-30 17:18:36.171652 by slurmutils.
#
ArchiveEvents=yes
ArchiveJobs=yes
ArchiveResvs=yes
ArchiveSteps=no
ArchiveTXN=no
ArchiveUsage=no
ArchiveScript=/usr/sbin/slurm.dbd.archive
AuthInfo=/var/run/munge/munge.socket.2
AuthType=auth/munge
AuthAltTypes=auth/jwt
AuthAltParameters=jwt_key=16549684561684@
DbdHost=slurmdbd-0
DbdBackupHost=slurmdbd-1
DebugLevel=info
PluginDir=/all/these/cool/plugins
PurgeEventAfter=1month
PurgeJobAfter=12month
PurgeResvAfter=1month
PurgeStepAfter=1month
PurgeSuspendAfter=1month
PurgeTXNAfter=12month
PurgeUsageAfter=24month
LogFile=/var/log/slurmdbd.log
PidFile=/var/run/slurmdbd.pid
SlurmUser=slurm
StoragePass=supersecretpasswd
StorageType=accounting_storage/mysql
StorageUser=slurm
StorageHost=127.0.0.1
StoragePort=3306
StorageLoc=slurm_acct_db
"""


class TestSlurmdbdConfigEditor(unittest.TestCase):
    """Unit tests for the slurmdbd.conf file editor."""

    def setUp(self) -> None:
        Path("slurmdbd.conf").write_text(example_slurmdbd_conf)

    def test_loads(self) -> None:
        """Test `loads` method of the slurmdbdconfig module."""
        config = slurmdbdconfig.loads(example_slurmdbd_conf)
        self.assertListEqual(config.plugin_dir, ["/all/these/cool/plugins"])
        self.assertDictEqual(config.auth_alt_parameters, {"jwt_key": "16549684561684@"})
        self.assertEqual(config.slurm_user, "slurm")
        self.assertEqual(config.log_file, "/var/log/slurmdbd.log")

    def test_dumps(self) -> None:
        """Test `dumps` method of the slurmdbdconfig module."""
        config = slurmdbdconfig.loads(example_slurmdbd_conf)
        # The new config and old config should not be equal since the
        # timestamps in the header will be different.
        self.assertNotEqual(slurmdbdconfig.dumps(config), example_slurmdbd_conf)

    def test_edit(self) -> None:
        """Test `edit` context manager from the slurmdbdconfig module."""
        with slurmdbdconfig.edit("slurmdbd.conf") as config:
            config.archive_usage = "yes"
            config.log_file = "/var/spool/slurmdbd.log"
            config.debug_flags = ["DB_EVENT", "DB_JOB", "DB_USAGE"]
            del config.auth_alt_types
            del config.auth_alt_parameters

        config = slurmdbdconfig.load("slurmdbd.conf")
        self.assertEqual(config.archive_usage, "yes")
        self.assertEqual(config.log_file, "/var/spool/slurmdbd.log")
        self.assertListEqual(config.debug_flags, ["DB_EVENT", "DB_JOB", "DB_USAGE"])
        self.assertIsNone(config.auth_alt_types)
        self.assertIsNone(config.auth_alt_parameters)

    def tearDown(self) -> None:
        Path("slurmdbd.conf").unlink()
