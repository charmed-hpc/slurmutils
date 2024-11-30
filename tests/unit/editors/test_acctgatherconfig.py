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

"""Unit tests for the acct_gather.conf editor."""


from constants import EXAMPLE_ACCT_GATHER_CONFIG
from pyfakefs.fake_filesystem_unittest import TestCase

from slurmutils.editors import acctgatherconfig


class TestAcctGatherConfigEditor(TestCase):
    """Unit tests for acct_gather.conf file editor."""

    def setUp(self) -> None:
        self.setUpPyfakefs()
        self.fs.create_file("/etc/slurm/acct_gather.conf", contents=EXAMPLE_ACCT_GATHER_CONFIG)

    def test_loads(self) -> None:
        """Test `loads` method of the acct_gatherconfig module."""
        config = acctgatherconfig.loads(EXAMPLE_ACCT_GATHER_CONFIG)
        self.assertEqual(config.energy_ipmi_frequency, "1")
        self.assertEqual(config.energy_ipmi_calc_adjustment, "yes")
        self.assertEqual(
            config.energy_ipmi_power_sensors,
            {"Node": ["16", "19"], "Socket1": ["19", "26"], "KNC": ["16", "19"]},
        )
        self.assertEqual(config.energy_ipmi_username, "testipmiusername")
        self.assertEqual(config.energy_ipmi_password, "testipmipassword")
        self.assertEqual(config.energy_ipmi_timeout, "10")
        self.assertEqual(config.profile_hdf5_dir, "/mydir")
        self.assertEqual(config.profile_hdf5_default, ["ALL"])
        self.assertEqual(config.profile_influx_db_database, "acct_gather_db")
        self.assertEqual(config.profile_influx_db_default, ["ALL"])
        self.assertEqual(config.profile_influx_db_host, "testhostname")
        self.assertEqual(config.profile_influx_db_pass, "testpassword")
        self.assertEqual(config.profile_influx_dbrt_policy, "testpolicy")
        self.assertEqual(config.profile_influx_db_user, "testuser")
        self.assertEqual(config.profile_influx_db_timeout, "10")
        self.assertEqual(config.infiniband_ofed_port, "0")
        self.assertEqual(config.sysfs_interfaces, ["enp0s1"])

        config = acctgatherconfig.loads(EXAMPLE_ACCT_GATHER_CONFIG)
        # The new config and old config should not be equal since the
        # timestamps in the header will be different.
        self.assertNotEqual(acctgatherconfig.dumps(config), EXAMPLE_ACCT_GATHER_CONFIG)

    def test_edit(self) -> None:
        """Test `edit` context manager from the acctgatherconfig module."""
        with acctgatherconfig.edit("/etc/slurm/acct_gather.conf") as config:
            config.energy_ipmi_frequency = "2"
            config.energy_ipmi_calc_adjustment = "no"
            config.energy_ipmi_power_sensors = {
                "Node": ["20", "21"],
                "Socket1": ["10", "26"],
                "KNC": ["16", "19"],
            }
            config.energy_ipmi_username = "testipmiusername1"
            config.energy_ipmi_password = "testipmipassword1"
            config.energy_ipmi_timeout = "20"
            config.profile_hdf5_dir = "/mydir1234"
            config.profile_hdf5_default = ["NONE"]
            config.profile_influx_db_database = "test_acct_gather_db"
            config.profile_influx_db_default = ["NONE"]
            config.profile_influx_db_host = "testhostname1"
            config.profile_influx_db_pass = "testpassword1"
            config.profile_influx_dbrt_policy = "testpolicy1"
            config.profile_influx_db_user = "testuser1"
            config.profile_influx_db_timeout = "20"
            config.infiniband_ofed_port = "1"
            config.sysfs_interfaces = ["enp0s2"]

        config = acctgatherconfig.load("/etc/slurm/acct_gather.conf")
        self.assertEqual(config.energy_ipmi_frequency, "2")
        self.assertEqual(config.energy_ipmi_calc_adjustment, "no")
        self.assertEqual(
            config.energy_ipmi_power_sensors,
            {"Node": ["20", "21"], "Socket1": ["10", "26"], "KNC": ["16", "19"]},
        ),
        self.assertEqual(config.energy_ipmi_username, "testipmiusername1")
        self.assertEqual(config.energy_ipmi_password, "testipmipassword1")
        self.assertEqual(config.energy_ipmi_timeout, "20")
        self.assertEqual(config.profile_hdf5_dir, "/mydir1234")
        self.assertEqual(config.profile_hdf5_default, ["NONE"])
        self.assertEqual(config.profile_influx_db_database, "test_acct_gather_db")
        self.assertEqual(config.profile_influx_db_default, ["NONE"])
        self.assertEqual(config.profile_influx_db_host, "testhostname1")
        self.assertEqual(config.profile_influx_db_pass, "testpassword1")
        self.assertEqual(config.profile_influx_dbrt_policy, "testpolicy1")
        self.assertEqual(config.profile_influx_db_user, "testuser1")
        self.assertEqual(config.profile_influx_db_timeout, "20")
        self.assertEqual(config.infiniband_ofed_port, "1")
        self.assertEqual(config.sysfs_interfaces, ["enp0s2"])
