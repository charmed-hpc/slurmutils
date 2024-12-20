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

from unittest import TestCase

from slurmutils.models import GRESConfig, GRESName, GRESNode
from slurmutils.models.gres import GRESNameMapping, GRESNodeMapping


class TestGRESConfig(TestCase):
    """Unit tests for `gres.conf` data model."""

    def setUp(self) -> None:
        self.config = GRESConfig()
        self.names = GRESName.from_dict(
            {"Name": "gpu", "Type": "gp100", "File": "/dev/nvidia0", "Cores": ["0", "1"]}
        )
        self.nodes = GRESNode.from_dict(
            {
                "NodeName": "juju-c9c6f-[1-10]",
                "Name": "gpu",
                "Type": "rtx",
                "File": "/dev/nvidia[0-3]",
                "Count": "8G",
            }
        )

    def test_auto_detect(self) -> None:
        """Test global `AutoDetect` descriptor."""
        del self.config.auto_detect
        self.config.auto_detect = "rsmi"
        self.assertEqual(self.config.auto_detect, "rsmi")
        del self.config.auto_detect
        self.assertIsNone(self.config.auto_detect)

    def test_names(self) -> None:
        """Test `Names` descriptor."""
        new = GRESNameMapping({self.names.name: [self.names]})
        self.config.names = new
        self.assertEqual(self.config.names, new)
        del self.config.names
        self.assertEqual(self.config.names, GRESNameMapping())

    def test_nodes(self) -> None:
        """Test `Nodes` descriptor."""
        new = GRESNodeMapping({self.nodes.node_name: [self.nodes]})
        self.config.nodes = new
        self.assertEqual(self.config.nodes, new)
        del self.config.nodes
        self.assertEqual(self.config.nodes, GRESNodeMapping())


class TestGRESName(TestCase):
    """Unit tests for `GRESName` data model."""

    def setUp(self) -> None:
        self.config = GRESName(Name="gpu")

    def test_auto_detect(self) -> None:
        """Test in-line `AutoDetect` descriptor."""
        del self.config.auto_detect
        self.config.auto_detect = "rsmi"
        self.assertEqual(self.config.auto_detect, "rsmi")
        del self.config.auto_detect
        self.assertIsNone(self.config.auto_detect)

    def test_count(self) -> None:
        """Test `Count` descriptor."""
        del self.config.count
        self.config.count = "10G"
        self.assertEqual(self.config.count, "10G")
        del self.config.count
        self.assertIsNone(self.config.count)

    def test_cores(self) -> None:
        """Test `Cores` descriptor."""
        del self.config.cores
        self.config.cores = ["0", "1"]
        self.assertListEqual(self.config.cores, ["0", "1"])
        del self.config.cores
        self.assertIsNone(self.config.cores)

    def test_file(self) -> None:
        """Test `File` descriptor."""
        del self.config.file
        self.config.file = "/dev/amd[0-4]"
        self.assertEqual(self.config.file, "/dev/amd[0-4]")
        del self.config.file
        self.assertIsNone(self.config.file)

    def test_flags(self) -> None:
        """Test `Flags` descriptor."""
        del self.config.flags
        self.config.flags = ["CountOnly", "amd_gpu_env"]
        self.assertListEqual(self.config.flags, ["CountOnly", "amd_gpu_env"])
        del self.config.flags
        self.assertIsNone(self.config.flags)

    def test_links(self) -> None:
        """Test `Links` descriptor."""
        del self.config.links
        self.config.links = ["-1", "16", "16", "16"]
        self.assertListEqual(self.config.links, ["-1", "16", "16", "16"])
        del self.config.links
        self.assertIsNone(self.config.links)

    def test_multiple_files(self) -> None:
        """Test `MultipleFiles` descriptor."""
        del self.config.multiple_files
        self.config.multiple_files = "/dev/amd[0-4]"
        self.assertEqual(self.config.multiple_files, "/dev/amd[0-4]")
        del self.config.multiple_files
        self.assertIsNone(self.config.multiple_files)

    def test_name(self) -> None:
        """Test `Name` descriptor."""
        self.assertEqual(self.config.name, "gpu")
        self.config.name = "shard"
        self.assertEqual(self.config.name, "shard")
        # Ensure that `Name` cannot be deleted.
        with self.assertRaises(AttributeError):
            del self.config.name  # noqa

    def test_type(self) -> None:
        """Test `Type` descriptor."""
        del self.config.type
        self.config.type = "epyc"
        self.assertEqual(self.config.type, "epyc")
        del self.config.type
        self.assertIsNone(self.config.type)


class TestGRESNode(TestCase):
    """Unit tests for `GRESNode` data model."""

    def setUp(self) -> None:
        self.config = GRESNode(NodeName="juju-c9c6f-[1-10]")

    def test_node_name(self) -> None:
        """Test `NodeName` descriptor."""
        self.assertEqual(self.config.node_name, "juju-c9c6f-[1-10]")
        self.config.node_name = "juju-c9c6f-[1-5]"
        self.assertEqual(self.config.node_name, "juju-c9c6f-[1-5]")
        # Ensure that `NodeName` cannot be deleted.
        with self.assertRaises(AttributeError):
            del self.config.node_name  # noqa
