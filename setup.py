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

"""setup.py for slurmutils package."""

from os.path import exists

from setuptools import setup

setup(
    name="slurmutils",
    version="0.1.0",
    author="Jason C. Nucciarone",
    author_email="jason.nucciarone@canonical.com",
    license="LGPL-3.0",
    url="https://github.com/canonical/slurmutils",
    description="Utilities and APIs for interacting with the SLURM workload manager",
    long_description=open("README.md").read() if exists("README.md") else "",
    long_description_content_type="text/markdown",
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    packages=[
        "slurmutils",
        "slurmutils.editors"
    ]
)
