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

"""Unit tests for the model and editor of the `slurmdbd.conf` configuration file."""

from constants import EXAMPLE_SLURMDBD_CONFIG
from pyfakefs.fake_filesystem_unittest import TestCase

from slurmutils import ModelError, SlurmdbdConfig, slurmdbdconfig

EXPECTED_SLURMDBD_DUMPS_OUTPUT = """
archiveevents=yes
archivejobs=yes
archiveresvs=yes
archivesteps=no
archivetxn=no
archiveusage=no
archivescript=/usr/sbin/slurm.dbd.archive
authinfo=socket=/var/run/munge/munge.socket.2
authtype=auth/munge
authalttypes=auth/jwt
authaltparameters=jwt_key=16549684561684@
dbdhost=slurmdbd-0
dbdbackuphost=slurmdbd-1
debuglevel=info
plugindir=/all/these/cool/plugins
purgeeventafter=1month
purgejobafter=12month
purgeresvafter=1month
purgestepafter=1month
purgesuspendafter=1month
purgetxnafter=12month
purgeusageafter=24month
logfile=/var/log/slurmdbd.log
pidfile=/var/run/slurmdbd.pid
slurmuser=slurm
storagepass=supersecretpasswd
storagetype=accounting_storage/mysql
storageuser=slurm
storagehost=127.0.0.1
storageport=3306
storageloc=slurm_acct_db
""".strip()


class TestSlurmdbdConfigEditor(TestCase):
    """Unit tests for the model and editor of the `slurmdbd.conf` configuration file."""

    def setUp(self) -> None:
        self.setUpPyfakefs()
        self.fs.create_file("/etc/slurm/slurmdbd.conf", contents=EXAMPLE_SLURMDBD_CONFIG)

    def test_loads(self) -> None:
        """Test `loads` method of the `slurmdbd.conf` model editor."""
        config = slurmdbdconfig.loads(EXAMPLE_SLURMDBD_CONFIG)
        self.assertListEqual(config.plugin_dir, ["/all/these/cool/plugins"])
        self.assertDictEqual(config.auth_alt_parameters, {"jwt_key": "16549684561684@"})
        self.assertEqual(config.slurm_user, "slurm")
        self.assertEqual(config.log_file, "/var/log/slurmdbd.log")

    def test_dumps(self) -> None:
        """Test `dumps` method of the `slurmdbd.conf` model editor."""
        config = slurmdbdconfig.loads(EXAMPLE_SLURMDBD_CONFIG)
        # Check if output matches expected output.
        self.assertEqual(slurmdbdconfig.dumps(config), EXPECTED_SLURMDBD_DUMPS_OUTPUT)
        # New config and old config should not be equal since the editor strips all comments.
        self.assertNotEqual(slurmdbdconfig.dumps(config), EXAMPLE_SLURMDBD_CONFIG)

    def test_edit(self) -> None:
        """Test `edit` context manager of the `slurmdbd.conf` model editor."""
        with slurmdbdconfig.edit("/etc/slurm/slurmdbd.conf") as config:
            config.archive_usage = True
            config.log_file = "/var/spool/slurmdbd.log"
            config.debug_flags = ["db_event", "db_job", "db_usage"]
            del config.auth_alt_types
            del config.auth_alt_parameters

        config = slurmdbdconfig.load("/etc/slurm/slurmdbd.conf")
        self.assertTrue(config.archive_usage)
        self.assertEqual(config.log_file, "/var/spool/slurmdbd.log")
        self.assertListEqual(config.debug_flags, ["db_event", "db_job", "db_usage"])
        self.assertIsNone(config.auth_alt_types)
        self.assertIsNone(config.auth_alt_parameters)

    def test_load_fail(self) -> None:
        """Test that bogus values are automatically caught when loading a new model."""
        # Catch if field value is unexpected. e.g. not a boolean value.
        with self.assertRaises(ValueError):
            SlurmdbdConfig.from_str(
                """
                archivesteps=totally
                """
            )

        # Catch if field is unexpected or in the incorrect syntax.
        with self.assertRaises(ModelError):
            SlurmdbdConfig.from_str(
                """
                archive_steps=yes
                """
            )

        # Catch if field value is invalid when checking against the model schema.
        with self.assertRaises(ModelError):
            SlurmdbdConfig.from_str(
                """
                LogFile=67
                """
            )

    def test_edit_fail(self) -> None:
        """Test that bogus attributes are handled when editing a loaded model."""
        # Catch if user tries to edit a non-existent attribute.
        with self.assertRaises(AttributeError):
            config = slurmdbdconfig.loads(EXAMPLE_SLURMDBD_CONFIG)
            config.archive = True

        # Catch if user tries to access a non-existent attribute.
        with self.assertRaises(AttributeError):
            config = slurmdbdconfig.loads(EXAMPLE_SLURMDBD_CONFIG)
            _ = config.archive
