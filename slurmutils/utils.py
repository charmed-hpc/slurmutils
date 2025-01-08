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

"""Utilities for streamlining common Slurm-related operations."""

__all__ = ["calculate_rs"]

from collections.abc import Iterable
from itertools import groupby


def calculate_rs(elements: Iterable[int]) -> str:
    """Calculate ranges and strides in an iterable.

    Args:
        elements: Iterable to calculate ranges and strides in.
            The iterable's elements must be unique and sortable in ascending order.

    Returns:
        A square-bracketed string with comma-separated ranges of consecutive values.
        example_input  = [0,1,2,3,4,5,6,8,9,10,12,14,15,16,18]
        example_output = '[0-6,8-10,12,14-16,18]'

    Notes:
        This function can be used to assist with converting arrays of resource names
        such as device files and node names into the Slurm hostname specification.
    """
    elements = sorted(elements)

    # The input is enumerate()-ed to produce a list of tuples of the elements and their indices.
    # groupby() uses the lambda key function to group these tuples by the difference between the
    # element and index. Consecutive values have equal difference between element and index,
    # so are grouped together. Hence, the elements of the first and last members of each
    # group give the range of consecutive values. If the group has only a single member, there are
    # no consecutive values either side of it (a "stride").
    out = "["
    for _, group in groupby(enumerate(elements), lambda elem: elem[1] - elem[0]):
        group = list(group)

        if len(group) == 1:
            # Single member, this is a stride.
            out += f"{group[0][1]},"
        else:
            # Range of consecutive values is first-last in group.
            out += f"{group[0][1]}-{group[-1][1]},"

    out = out.rstrip(",") + "]"
    return out
