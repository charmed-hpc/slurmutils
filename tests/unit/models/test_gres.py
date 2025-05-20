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

"""Unit tests for models and editor of the `gres.conf` configuration file."""

from constants import EXAMPLE_GRES_CONFIG
from pyfakefs.fake_filesystem_unittest import TestCase

from slurmutils import Gres, GresConfig, ModelError, cgroupconfig, gresconfig

EXPECTED_GRES_DUMPS_OUTPUT = """
autodetect=nvml
name=gpu type=gp100 file=/dev/nvidia0 cores=0,1
name=gpu type=gp100 file=/dev/nvidia1 cores=0,1
name=gpu type=p6000 file=/dev/nvidia2 cores=2,3
name=gpu type=p6000 file=/dev/nvidia3 cores=2,3
name=gpu nodename=juju-abc654-1 type=tesla_t4 file=/dev/nvidia[0-1] count=8G
name=gpu nodename=juju-abc654-1 type=l40s file=/dev/nvidia[2-3] count=12G
name=mps count=200 file=/dev/nvidia0
name=mps count=200 file=/dev/nvidia1
name=mps count=100 file=/dev/nvidia2
name=mps count=100 file=/dev/nvidia3
name=bandwidth type=lustre count=4G flags=countonly
""".strip()


class TestGresConfig(TestCase):
    """Unit tests for models and the editor of the `gres.conf` configuration file."""

    def setUp(self) -> None:
        self.setUpPyfakefs()
        self.fs.create_file("/etc/slurm/gres.conf", contents=EXAMPLE_GRES_CONFIG)

    def test_loads(self) -> None:
        """Test `loads` method of `gres.conf` model editor."""
        config = gresconfig.loads(EXAMPLE_GRES_CONFIG)
        self.assertEqual(config.auto_detect, "nvml")
        self.assertDictEqual(
            config.gres.dict(),
            {
                "gpu": [
                    {"name": "gpu", "type": "gp100", "file": "/dev/nvidia0", "cores": [0, 1]},
                    {"name": "gpu", "type": "gp100", "file": "/dev/nvidia1", "cores": [0, 1]},
                    {"name": "gpu", "type": "p6000", "file": "/dev/nvidia2", "cores": [2, 3]},
                    {"name": "gpu", "type": "p6000", "file": "/dev/nvidia3", "cores": [2, 3]},
                    {
                        "name": "gpu",
                        "nodename": "juju-abc654-1",
                        "type": "tesla_t4",
                        "file": "/dev/nvidia[0-1]",
                        "count": "8G",
                    },
                    {
                        "name": "gpu",
                        "nodename": "juju-abc654-1",
                        "type": "l40s",
                        "file": "/dev/nvidia[2-3]",
                        "count": "12G",
                    },
                ],
                "mps": [
                    {"name": "mps", "count": 200, "file": "/dev/nvidia0"},
                    {"name": "mps", "count": 200, "file": "/dev/nvidia1"},
                    {"name": "mps", "count": 100, "file": "/dev/nvidia2"},
                    {"name": "mps", "count": 100, "file": "/dev/nvidia3"},
                ],
                "bandwidth": [
                    {"name": "bandwidth", "type": "lustre", "count": "4G", "flags": ["countonly"]}
                ],
            },
        )

    def test_dumps(self) -> None:
        """Test `dumps` method of the `gres.conf` model editor."""
        config = gresconfig.loads(EXAMPLE_GRES_CONFIG)
        # Check if output matches expected output.
        self.assertEqual(cgroupconfig.dumps(config), EXPECTED_GRES_DUMPS_OUTPUT)
        # New and old config should not be equal since editor strips all comments.
        self.assertNotEqual(cgroupconfig.dumps(config), EXAMPLE_GRES_CONFIG)

    def test_edit(self) -> None:
        """Test `edit` method of the `gres.conf` model editor."""
        with gresconfig.edit("/etc/slurm/gres.conf") as config:
            config.auto_detect = "rsmi"
            config.gres["gpu"].append(Gres(name="gpu", type="epyc", file="/dev/amd0"))

        config = gresconfig.load("/etc/slurm/gres.conf")
        self.assertEqual(config.auto_detect, "rsmi")
        self.assertDictEqual(
            config.gres["gpu"][-1].dict(), {"name": "gpu", "type": "epyc", "file": "/dev/amd0"}
        )

    def test_load_fail(self) -> None:
        """Test that bogus values are automatically caught when loading a new model."""
        # Catch if field is unexpected or in the incorrect syntax.
        with self.assertRaises(ModelError):
            GresConfig.from_str(
                """
                Accelerator=EXPENSIVE_GPU AutoDetect=False
                """
            )

        # Catch if field value is invalid when checking against the model schema.
        with self.assertRaises(ModelError):
            GresConfig.from_str(
                """
                autodetect=superpowerfulgpu
                name=gpu file=65
                """
            )

        with self.assertRaises(ModelError):
            Gres.from_str(
                """
                name=gpu type=gp100 file=/dev/nvidia0 flags=countonly,custom_gpu_env
                """
            )

    def test_edit_fail(self) -> None:
        """Test that bogus attributes are handled when editing a loaded model."""
        # Catch if user tries to edit a non-existent attribute.
        with self.assertRaises(AttributeError):
            config = gresconfig.loads(EXAMPLE_GRES_CONFIG)
            config.auto = "nvidia"

        # Catch if user tries to access a non-existent attribute.
        with self.assertRaises(AttributeError):
            config = gresconfig.loads(EXAMPLE_GRES_CONFIG)
            _ = config.auto
