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

import unittest
from pathlib import Path

from slurmutils.editors import slurmconfig
from slurmutils.models import DownNodes, Node, Partition

example_slurm_conf = """#
# `slurm.conf` file generated at 2024-01-30 17:18:36.171652 by slurmutils.
#
SlurmctldHost=juju-c9fc6f-0(10.152.28.20)
SlurmctldHost=juju-c9fc6f-1(10.152.28.100)

ClusterName=charmed-hpc
AuthType=auth/munge
Epilog=/usr/local/slurm/epilog
Prolog=/usr/local/slurm/prolog
FirstJobId=65536
InactiveLimit=120
JobCompType=jobcomp/filetxt
JobCompLoc=/var/log/slurm/jobcomp
KillWait=30
MaxJobCount=10000
MinJobAge=3600
PluginDir=/usr/local/lib:/usr/local/slurm/lib
ReturnToService=0
SchedulerType=sched/backfill
SlurmctldLogFile=/var/log/slurm/slurmctld.log
SlurmdLogFile=/var/log/slurm/slurmd.log
SlurmctldPort=7002
SlurmdPort=7003
SlurmdSpoolDir=/var/spool/slurmd.spool
StateSaveLocation=/var/spool/slurm.state
SwitchType=switch/none
TmpFS=/tmp
WaitTime=30

#
# Node configurations
#
NodeName=juju-c9fc6f-2 NodeAddr=10.152.28.48 CPUs=1 RealMemory=1000 TmpDisk=10000
NodeName=juju-c9fc6f-3 NodeAddr=10.152.28.49 CPUs=1 RealMemory=1000 TmpDisk=10000
NodeName=juju-c9fc6f-4 NodeAddr=10.152.28.50 CPUs=1 RealMemory=1000 TmpDisk=10000
NodeName=juju-c9fc6f-5 NodeAddr=10.152.28.51 CPUs=1 RealMemory=1000 TmpDisk=10000

#
# Down node configurations
#
DownNodes=juju-c9fc6f-5 State=DOWN Reason="Maintenance Mode"

#
# Partition configurations
#
PartitionName=DEFAULT MaxTime=30 MaxNodes=10 State=UP
PartitionName=batch Nodes=juju-c9fc6f-2,juju-c9fc6f-3,juju-c9fc6f-4,juju-c9fc6f-5 MinNodes=4 MaxTime=120 AllowGroups=admin
"""


class TestSlurmConfigEditor(unittest.TestCase):
    """Unit tests for slurm.conf file editor."""

    def setUp(self) -> None:
        Path("slurm.conf").write_text(example_slurm_conf)

    def test_loads(self) -> None:
        """Test `loads` method of the slurmconfig module."""
        config = slurmconfig.loads(example_slurm_conf)
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
        config = slurmconfig.loads(example_slurm_conf)
        # The new config and old config should not be equal since the
        # timestamps in the header will be different.
        self.assertNotEqual(slurmconfig.dumps(config), example_slurm_conf)

    def test_edit(self) -> None:
        """Test `edit` context manager from the slurmconfig module."""
        # Test descriptors for `slurm.conf` configuration options.
        with slurmconfig.edit("slurm.conf") as config:
            del config.inactive_limit
            config.max_job_count = 20000
            config.proctrack_type = "proctrack/linuxproc"
            config.plugin_dir.append("/snap/slurm/current/plugins")
            new_node = Node(NodeName="batch-0", **config.nodes["juju-c9fc6f-2"])
            del config.nodes["juju-c9fc6f-2"]
            config.nodes.update(new_node.dict())

        config = slurmconfig.load("slurm.conf")
        self.assertIsNone(config.inactive_limit)
        self.assertEqual(config.max_job_count, "20000")
        self.assertEqual(config.proctrack_type, "proctrack/linuxproc")
        self.assertListEqual(
            config.plugin_dir,
            ["/usr/local/lib", "/usr/local/slurm/lib", "/snap/slurm/current/plugins"],
        )
        self.assertEqual(config.nodes["batch-0"]["NodeAddr"], "10.152.28.48")

        with slurmconfig.edit("slurm.conf") as config:
            del config.nodes
            del config.frontend_nodes
            del config.down_nodes
            del config.node_sets
            del config.partitions

        config = slurmconfig.load("slurm.conf")
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

        with slurmconfig.edit("slurm.conf") as config:
            for node in new_nodes:
                config.nodes.update(node.dict())

            for down_node in new_down_nodes:
                config.down_nodes.append(down_node.dict())

            for partition in new_partitions:
                config.partitions.update(partition.dict())

    def tearDown(self):
        Path("slurm.conf").unlink()
