#!/usr/bin/env python3
# Copyright 2025 Canonical Ltd.
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

"""Unit tests for the model and editor of the `oci.conf` configuration file."""

from constants import EXAMPLE_OCI_CONFIG
from pyfakefs.fake_filesystem_unittest import TestCase

from slurmutils import ModelError, OCIConfig, ociconfig

EXPECTED_OCI_DUMPS_OUTPUT = """
ignorefileconfigjson=true
envexclude="^(SLURM_CONF|SLURM_CONF_SERVER)="
runtimeenvexclude="^(SLURM_CONF|SLURM_CONF_SERVER)="
runtimerun="singularity exec --userns %r %@"
runtimekill="kill -s SIGTERM %p"
runtimedelete="kill -s SIGKILL %p"
""".strip()


class TestOCIConfig(TestCase):
    """Unit tests for the model and editor of the `oci.conf` configuration file."""

    def setUp(self) -> None:
        self.setUpPyfakefs()
        self.fs.create_file("/etc/slurm/oci.conf", contents=EXAMPLE_OCI_CONFIG)

    def test_loads(self) -> None:
        """Test `loads` method of the `oci.conf` model editor."""
        config = ociconfig.loads(EXAMPLE_OCI_CONFIG)
        self.assertTrue(config.ignore_file_config_json)
        self.assertEqual(config.env_exclude, "^(SLURM_CONF|SLURM_CONF_SERVER)=")
        self.assertEqual(config.run_time_env_exclude, "^(SLURM_CONF|SLURM_CONF_SERVER)=")
        self.assertEqual(config.run_time_run, "singularity exec --userns %r %@")
        self.assertEqual(config.run_time_kill, "kill -s SIGTERM %p")
        self.assertEqual(config.run_time_delete, "kill -s SIGKILL %p")

    def test_dumps(self) -> None:
        """Test `dumps` method of the `oci.conf` model editor."""
        config = ociconfig.loads(EXAMPLE_OCI_CONFIG)
        # Check if output matches expected output.
        self.assertEqual(ociconfig.dumps(config), EXPECTED_OCI_DUMPS_OUTPUT)
        # New config and old config should not be equal since the editor strips all comments.
        self.assertNotEqual(ociconfig.dumps(config), EXAMPLE_OCI_CONFIG)

    def test_edit(self) -> None:
        """Test `edit` context manager of the `oci.conf` model editor."""
        with ociconfig.edit("/etc/slurm/oci.conf") as config:
            config.ignore_file_config_json = False
            config.env_exclude = "^(SLURM_CONF)="
            config.run_time_run = "sudo " + config.run_time_run
            config.run_time_kill = "sudo " + config.run_time_kill
            config.run_time_delete = "sudo " + config.run_time_delete

        config = ociconfig.load("/etc/slurm/oci.conf")
        self.assertFalse(config.ignore_file_config_json)
        self.assertEqual(config.env_exclude, "^(SLURM_CONF)=")
        self.assertEqual(config.run_time_run, "sudo singularity exec --userns %r %@")
        self.assertEqual(config.run_time_kill, "sudo kill -s SIGTERM %p")
        self.assertEqual(config.run_time_delete, "sudo kill -s SIGKILL %p")

    def test_load_fail(self) -> None:
        """Test that bogus values are automatically caught when loading a new model."""
        # Catch if field value is unexpected. e.g. not a boolean value.
        with self.assertRaises(ValueError):
            OCIConfig.from_str(
                """
                ignorefileconfigjson=totallybro
                """
            )

        # Catch if field is unexpected or in the incorrect syntax.
        with self.assertRaises(ModelError):
            OCIConfig.from_str(
                """
                run_time_kill="kill -9 %p"
                """
            )

        # Catch if field value is invalid when checking against the model schema.
        with self.assertRaises(ModelError):
            OCIConfig.from_str(
                """
                createenvfile=nodontdothat
                """
            )

    def test_edit_fail(self) -> None:
        """Test that bogus attributes are handled when editing a loaded model."""
        # Catch if user tries to edit a non-existent attribute.
        with self.assertRaises(AttributeError):
            config = ociconfig.loads(EXAMPLE_OCI_CONFIG)
            config.env_include = "^(SLURM_JWT)="

        # Catch if user tries to access a non-existent attribute.
        with self.assertRaises(AttributeError):
            config = ociconfig.loads(EXAMPLE_OCI_CONFIG)
            _ = config.env_include
