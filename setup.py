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

"""setup.py for slurmutils package."""

from os.path import exists

from setuptools import setup

setup(
    name="slurmutils",
    version="0.1.0",
    author="Jason C. Nucciarone",
    author_email="jason.nucciarone@canonical.com",
    license="Apache-2.0",
    url="https://github.com/canonical/slurmutils",
    description="Utilities and APIs for interacting with the SLURM workload manager",
    long_description=open("README.md").read() if exists("README.md") else "",
    long_description_content_type="text/markdown",
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    packages=[
        "slurmutils",
        "slurmutils.slurmconf"
    ]
)
