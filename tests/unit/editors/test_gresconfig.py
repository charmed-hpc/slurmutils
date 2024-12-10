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

from constants import EXAMPLE_GRES_CONFIG
from pyfakefs.fake_filesystem_unittest import TestCase

from slurmutils.editors import gresconfig
from slurmutils.models import GRESName, GRESNode


class TestGRESConfigEditor(TestCase):
    """Unit tests for gres.conf configuration file editor."""

    def setUp(self) -> None:
        self.setUpPyfakefs()
        self.fs.create_file("/etc/slurm/gres.conf", contents=EXAMPLE_GRES_CONFIG)

    def test_loads(self) -> None:
        """Test `loads` function from the `gresconfig` editor module."""
        config = gresconfig.loads(EXAMPLE_GRES_CONFIG)
        self.assertEqual(config.auto_detect, "nvml")
        self.assertListEqual(
            config.names,
            [
                {"Name": "gpu", "Type": "gp100", "File": "/dev/nvidia0", "Cores": ["0", "1"]},
                {"Name": "gpu", "Type": "gp100", "File": "/dev/nvidia1", "Cores": ["0", "1"]},
                {"Name": "gpu", "Type": "p6000", "File": "/dev/nvidia2", "Cores": ["2", "3"]},
                {"Name": "gpu", "Type": "p6000", "File": "/dev/nvidia3", "Cores": ["2", "3"]},
                {"Name": "mps", "Count": "200", "File": "/dev/nvidia0"},
                {"Name": "mps", "Count": "200", "File": "/dev/nvidia1"},
                {"Name": "mps", "Count": "100", "File": "/dev/nvidia2"},
                {"Name": "mps", "Count": "100", "File": "/dev/nvidia3"},
                {"Name": "bandwidth", "Type": "lustre", "Count": "4G", "Flags": ["CountOnly"]},
            ],
        )
        self.assertDictEqual(
            config.nodes,
            {
                "juju-c9c6f-[1-10]": {
                    "Name": "gpu",
                    "Type": "rtx",
                    "File": "/dev/nvidia[0-3]",
                    "Count": "8G",
                }
            },
        )

    def test_dumps(self) -> None:
        """Test `dumps` function from the `gresconfig` editor module."""
        config = gresconfig.loads(EXAMPLE_GRES_CONFIG)
        # New `gres.conf` will be different since the comments have been
        # stripped out by the editor.
        self.assertNotEqual(gresconfig.dumps(config), EXAMPLE_GRES_CONFIG)

    def test_edit(self) -> None:
        """Test `edit` context manager from the `gresconfig` editor module."""
        name = GRESName(
            Name="gpu",
            Type="epyc",
            File="/dev/amd4",
            Cores=["0", "1"],
        )
        node = GRESNode(
            NodeName="juju-abc654-[1-20]",
            Name="gpu",
            Type="epyc",
            File="/dev/amd[0-3]",
            Count="12G",
        )

        # Set new values with each accessor.
        with gresconfig.edit("/etc/slurm/gres.conf") as config:
            config.auto_detect = "rsmi"
            config.names = [name.dict()]
            config.nodes = node.dict()

        config = gresconfig.load("/etc/slurm/gres.conf")
        self.assertEqual(config.auto_detect, "rsmi")
        self.assertListEqual(config.names, [name.dict()])
        self.assertDictEqual(config.nodes, node.dict())

        # Delete all configured values from GRES configuration.
        with gresconfig.edit("/etc/slurm/gres.conf") as config:
            del config.auto_detect
            del config.names
            del config.nodes

        config = gresconfig.load("/etc/slurm/gres.conf")
        self.assertIsNone(config.auto_detect)
        self.assertListEqual(config.names, [])
        self.assertDictEqual(config.nodes, {})
