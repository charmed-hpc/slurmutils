#!/usr/bin/env python3
# Copyright 2023 Canonical Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Test SLURM configuration API."""

import unittest
from pathlib import Path

from slurmconf import SlurmConf

example_conf = """
#
# /etc/slurm/slurm.conf for juju-c9fc6f-[0-5].canonical.com
# Author: Jason C. Nucciarone
# Date: 17/07/2023
#
SlurmctldHost=juju-c9fc6f-0(10.152.28.20)  # Primary server
SlurmctldHost=juju-c9fc6f-1(10.152.28.100)  # Backup server
#
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
# Node Configurations
#
NodeName=juju-c9fc6f-2 NodeAddr=10.152.28.48 CPUs=1 RealMemory=1000 TmpDisk=10000
NodeName=juju-c9fc6f-3 NodeAddr=10.152.28.49 CPUs=1 RealMemory=1000 TmpDisk=10000
NodeName=juju-c9fc6f-4 NodeAddr=10.152.28.50 CPUs=1 RealMemory=1000 TmpDisk=10000
NodeName=juju-c9fc6f-5 NodeAddr=10.152.28.51 CPUs=1 RealMemory=1000 TmpDisk=10000
DownNodes=juju-c9fc6f-5 State=DOWN Reason="Maintenance Mode"
#
# Partition Configurations
#
PartitionName=DEFAULT MaxTime=30 MaxNodes=10 State=UP
PartitionName=batch Nodes=juju-c9fc6f-2,juju-c9fc6f-3,juju-c9fc6f-4,juju-c9fc6f-5 MinNodes=4 MaxTime=120 AllowGroups=admin
"""


class TestSlurmConf(unittest.TestCase):
    """Unit tests for slurm.conf file editor."""

    def setUp(self) -> None:
        Path("slurm.conf").write_text(example_conf.strip())

    def test_load(self) -> None:
        """Test that SlurmConf can successfully load/parse example configuration file."""
        with SlurmConf("slurm.conf") as conf:
            self.assertNotEqual(conf.comments, [])
            self.assertNotEqual(conf.nodes, {})
            self.assertNotEqual(conf.down_nodes, [])
            self.assertEqual(conf.frontend_nodes, {})
            self.assertEqual(conf.nodesets, {})
            self.assertNotEqual(conf.partitions, {})

    def test_edit(self) -> None:
        """Test if SlurmConf can successfully edit the example configuration file."""
        with SlurmConf("slurm.conf") as conf:
            del conf.inactive_limit
            conf.max_job_count = 20000
            conf.proctrack_type = "proctrack/linuxproc"

        conf = SlurmConf("slurm.conf")
        conf.load()
        self.assertIsNone(conf.inactive_limit)
        self.assertEqual(conf.max_job_count, "20000")
        self.assertEqual(conf.proctrack_type, "proctrack/linuxproc")
        self.assertListEqual(conf.plugin_dir, ["/usr/local/lib", "/usr/local/slurm/lib"])

    def tearDown(self) -> None:
        Path("slurm.conf").unlink()
