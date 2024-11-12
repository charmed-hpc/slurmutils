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

"""Unit tests for the slurm.conf editor."""


from constants import EXAMPLE_SLURM_CONFIG
from pyfakefs.fake_filesystem_unittest import TestCase

from slurmutils.editors import slurmconfig
from slurmutils.models import DownNodes, Node, Partition


class TestSlurmConfigEditor(TestCase):
    """Unit tests for slurm.conf file editor."""

    def setUp(self) -> None:
        self.setUpPyfakefs()
        self.fs.create_file("/etc/slurm/slurm.conf", contents=EXAMPLE_SLURM_CONFIG)

    def test_loads(self) -> None:
        """Test `loads` method of the slurmconfig module."""
        config = slurmconfig.loads(EXAMPLE_SLURM_CONFIG)
        self.assertListEqual(
            config.slurmctld_host, ["juju-c9fc6f-0(10.152.28.20)", "juju-c9fc6f-1(10.152.28.100)"]
        )
        self.assertEqual(config.slurmd_spool_dir, "/var/spool/slurmd.spool")
        self.assertEqual(config.scheduler_type, "sched/backfill")

        for name, params in config.nodes.items():
            self.assertIn(  # codespell:ignore
                name,
                {"juju-c9fc6f-2", "juju-c9fc6f-3", "juju-c9fc6f-4", "juju-c9fc6f-5"},
            )
            self.assertIn(  # codespell:ignore
                params["NodeAddr"],
                {"10.152.28.48", "10.152.28.49", "10.152.28.50", "10.152.28.51"},
            )
            self.assertEqual(params["CPUs"], "1")
            self.assertEqual(params["RealMemory"], "1000")
            self.assertEqual(params["TmpDisk"], "10000")

        for entry in config.down_nodes:
            self.assertEqual(entry["DownNodes"][0], "juju-c9fc6f-5")
            self.assertEqual(entry["State"], "DOWN")
            self.assertEqual(entry["Reason"], "Maintenance Mode")

        for partition in config.partitions:
            self.assertIn(partition, {"DEFAULT", "batch"})  # codespell:ignore

        batch = config.partitions["batch"]
        self.assertListEqual(
            batch["Nodes"], ["juju-c9fc6f-2", "juju-c9fc6f-3", "juju-c9fc6f-4", "juju-c9fc6f-5"]
        )

    def test_dumps(self) -> None:
        """Test `dumps` method of the slurmconfig module."""
        config = slurmconfig.loads(EXAMPLE_SLURM_CONFIG)
        # The new config and old config should not be equal since the
        # timestamps in the header will be different.
        self.assertNotEqual(slurmconfig.dumps(config), EXAMPLE_SLURM_CONFIG)

    def test_edit(self) -> None:
        """Test `edit` context manager from the slurmconfig module."""
        # Test descriptors for `slurm.conf` configuration options.
        with slurmconfig.edit("/etc/slurm/slurm.conf") as config:
            del config.inactive_limit
            config.max_job_count = 20000
            config.proctrack_type = "proctrack/linuxproc"
            config.plugin_dir.append("/snap/slurm/current/plugins")
            config.slurmctld_parameters = {"enable_configless": True}
            new_node = Node(NodeName="batch-0", **config.nodes["juju-c9fc6f-2"])
            del config.nodes["juju-c9fc6f-2"]
            config.nodes.update(new_node.dict())

        config = slurmconfig.load("/etc/slurm/slurm.conf")
        self.assertIsNone(config.inactive_limit)
        self.assertEqual(config.max_job_count, "20000")
        self.assertEqual(config.proctrack_type, "proctrack/linuxproc")
        self.assertListEqual(
            config.plugin_dir,
            ["/usr/local/lib", "/usr/local/slurm/lib", "/snap/slurm/current/plugins"],
        )
        self.assertDictEqual(config.slurmctld_parameters, {"enable_configless": True})
        self.assertEqual(config.nodes["batch-0"]["NodeAddr"], "10.152.28.48")

        with slurmconfig.edit("/etc/slurm/slurm.conf") as config:
            del config.nodes
            del config.frontend_nodes
            del config.down_nodes
            del config.node_sets
            del config.partitions

        config = slurmconfig.load("/etc/slurm/slurm.conf")
        self.assertDictEqual(config.nodes, {})
        self.assertDictEqual(config.frontend_nodes, {})
        self.assertListEqual(config.down_nodes, [])
        self.assertDictEqual(config.node_sets, {})
        self.assertDictEqual(config.partitions, {})

        new_nodes = [
            Node.from_dict(
                {
                    "juju-c9fc6f-2": {
                        "NodeAddr": "10.152.28.48",
                        "CPUs": "1",
                        "RealMemory": "1000",
                        "TmpDisk": "10000",
                    }
                }
            ),
            Node.from_dict(
                {
                    "juju-c9fc6f-3": {
                        "NodeAddr": "10.152.28.49",
                        "CPUs": "1",
                        "RealMemory": "1000",
                        "TmpDisk": "10000",
                    }
                }
            ),
            Node.from_dict(
                {
                    "juju-c9fc6f-4": {
                        "NodeAddr": "10.152.28.50",
                        "CPUs": "1",
                        "RealMemory": "1000",
                        "TmpDisk": "10000",
                    }
                }
            ),
            Node.from_dict(
                {
                    "juju-c9fc6f-5": {
                        "NodeAddr": "10.152.28.51",
                        "CPUs": "1",
                        "RealMemory": "1000",
                        "TmpDisk": "10000",
                    }
                }
            ),
        ]
        new_down_nodes = [
            DownNodes.from_dict(
                {
                    "DownNodes": ["juju-c9fc6f-5"],
                    "State": "DOWN",
                    "Reason": "Maintenance Mode",
                }
            )
        ]
        new_partitions = [
            Partition.from_dict({"DEFAULT": {"MaxTime": "30", "MaxNodes": "10", "State": "UP"}}),
            Partition.from_dict(
                {
                    "batch": {
                        "Nodes": [
                            "juju-c9fc6f-2",
                            "juju-c9fc6f-3",
                            "juju-c9fc6f-4",
                            "juju-c9fc6f-5",
                        ],
                        "MinNodes": "4",
                        "MaxTime": "120",
                        "AllowGroups": ["admin"],
                    }
                }
            ),
        ]

        with slurmconfig.edit("/etc/slurm/slurm.conf") as config:
            for node in new_nodes:
                config.nodes.update(node.dict())

            for down_node in new_down_nodes:
                config.down_nodes.append(down_node.dict())

            for partition in new_partitions:
                config.partitions.update(partition.dict())

    def test_update(self):
        """Test `update` method of the slurmconfig module."""
        config_updates = {
            "KillWait": 10,
            "PluginDir": "/var/snap/slurm/usr/local/lib:/var/snap/slurm/usr/local/slurm/lib",
            "ReturnToService": 0,
            "SchedulerType": "sched/builtin",
            "SwitchType": "switch/hpe_slingshot",
            "WaitTime": 30,
            "Nodes": {
                "juju-c9fc6f-2": {
                    "NodeAddr": "10.152.28.98",
                    "CPUs": "9",
                    "RealMemory": "9000",
                    "TmpDisk": "90000",
                },
                "juju-c9fc6f-6": {
                    "NodeAddr": "10.152.28.52",
                    "CPUs": "9",
                    "RealMemory": "1000",
                    "TmpDisk": "10000",
                },
                "juju-c9fc6f-7": {
                    "NodeAddr": "10.152.28.53",
                    "CPUs": "9",
                    "RealMemory": "1000",
                    "TmpDisk": "10000",
                },
            },
            "DownNodes": [
                {
                    "DownNodes": ["juju-c9fc6f-6", "juju-c9fc6f-7"],
                    "State": "DOWN",
                    "Reason": "New nodes",
                }
            ],
            "Partitions": {
                "DEFAULT": {
                    "MaxTime": "10",
                    "MaxNodes": "5",
                    "State": "UP",
                },
                "new_batch": {
                    "Nodes": ["juju-c9fc6f-6", "juju-c9fc6f-7"],
                    "MinNodes": "1",
                    "MaxTime": "120",
                    "AllowGroups": "admin",
                },
            },
        }

        config = slurmconfig.loads(EXAMPLE_SLURM_CONFIG)
        updates = slurmconfig.SlurmConfig.from_dict(config_updates)
        config.update(updates)

        self.assertEqual(config.kill_wait, 10)
        self.assertEqual(
            config.plugin_dir,
            "/var/snap/slurm/usr/local/lib:/var/snap/slurm/usr/local/slurm/lib",
        )
        self.assertEqual(config.scheduler_type, "sched/builtin")
        self.assertEqual(config.switch_type, "switch/hpe_slingshot")
        self.assertEqual(config.wait_time, 30)

        self.assertDictEqual(
            config.nodes,
            {
                "juju-c9fc6f-2": {
                    "NodeAddr": "10.152.28.98",
                    "CPUs": "9",
                    "RealMemory": "9000",
                    "TmpDisk": "90000",
                },
                "juju-c9fc6f-3": {
                    "NodeAddr": "10.152.28.49",
                    "CPUs": "1",
                    "RealMemory": "1000",
                    "TmpDisk": "10000",
                },
                "juju-c9fc6f-4": {
                    "NodeAddr": "10.152.28.50",
                    "CPUs": "1",
                    "RealMemory": "1000",
                    "TmpDisk": "10000",
                },
                "juju-c9fc6f-5": {
                    "NodeAddr": "10.152.28.51",
                    "CPUs": "1",
                    "RealMemory": "1000",
                    "TmpDisk": "10000",
                },
                "juju-c9fc6f-6": {
                    "NodeAddr": "10.152.28.52",
                    "CPUs": "9",
                    "RealMemory": "1000",
                    "TmpDisk": "10000",
                },
                "juju-c9fc6f-7": {
                    "NodeAddr": "10.152.28.53",
                    "CPUs": "9",
                    "RealMemory": "1000",
                    "TmpDisk": "10000",
                },
            },
        )
        self.assertListEqual(
            config.down_nodes,
            [
                {
                    "DownNodes": ["juju-c9fc6f-5"],
                    "State": "DOWN",
                    "Reason": "Maintenance Mode",
                },
                {
                    "DownNodes": ["juju-c9fc6f-6", "juju-c9fc6f-7"],
                    "State": "DOWN",
                    "Reason": "New nodes",
                },
            ],
        )
        self.assertDictEqual(
            config.partitions,
            {
                "DEFAULT": {
                    "MaxTime": "10",
                    "MaxNodes": "5",
                    "State": "UP",
                },
                "batch": {
                    "Nodes": ["juju-c9fc6f-2", "juju-c9fc6f-3", "juju-c9fc6f-4", "juju-c9fc6f-5"],
                    "MinNodes": "4",
                    "MaxTime": "120",
                    "AllowGroups": ["admin"],
                },
                "new_batch": {
                    "Nodes": ["juju-c9fc6f-6", "juju-c9fc6f-7"],
                    "MinNodes": "1",
                    "MaxTime": "120",
                    "AllowGroups": "admin",
                },
            },
        )
