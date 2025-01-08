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

"""Unit tests for the `utils` module."""

from unittest import TestCase

from slurmutils import calculate_rs


class TestUtils(TestCase):
    """Unit tests for the `utils` module ."""

    def test_calculate_rs(self) -> None:
        """Test the `calculate_rs` utility function."""
        node_range = [0, 1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 14, 15, 16, 18]
        r = calculate_rs(node_range)
        self.assertEqual(r, "[0-6,8-10,12,14-16,18]")
