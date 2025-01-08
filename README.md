# slurmutils

![PyPI - Version](https://img.shields.io/pypi/v/slurmutils)
![PyPI - Downloads](https://img.shields.io/pypi/dm/slurmutils)
![GitHub License](https://img.shields.io/github/license/charmed-hpc/slurmutils)
[![Matrix](https://img.shields.io/matrix/ubuntu-hpc%3Amatrix.org?logo=matrix&label=ubuntu-hpc)](https://matrix.to/#/#hpc:ubuntu.com)

Utilities and APIs for interfacing with the Slurm workload manager.

slurmutils is a collection of various utilities that make it easier 
for you and your friends to interface with the Slurm workload manager, especially if you 
are orchestrating deployments of new and current Slurm clusters. Gone are the days of
seething over incomplete Jinja2 templates. Current utilities shipped in the 
slurmutils package include:

#### `from slurmutils import ...`

* `calculate_rs`: A function for calculating the ranges and strides of an iterable with
  unique elements. This function can be used to help convert arrays of node hostnames,
  device file ids, etc into a Slurm hostname specification.

#### `from slurmutils.editors import ...`

* `acctgatherconfig`: An editor for _acct_gather.conf_ configuration files.
* `cgroupconfig`: An editor for _cgroup.conf_ configuration files.
* `gresconfig`: An editor for _gres.conf_ configuration files.
* `slurmconfig`: An editor for _slurm.conf_ configuration files.
* `slurmdbdconfig`: An editor for _slurmdbd.conf_ configuration files.

For more information on how to use or contribute to slurmutils, 
check out the [Getting Started](#-getting-started) and [Development](#-development) 
sections below 👇

## ✨ Getting Started

### Installation

#### Option 1: Install from PyPI

```shell
$ python3 -m pip install slurmutils
```

#### Option 2: Install from source

We use the [Poetry](https://python-poetry.org) packaging and dependency manager to
manage this project. It must be installed on your system if installing slurmutils
from source.

```shell
$ git clone https://github.com/canonical/slurmutils.git
$ cd slurmutils
$ poetry install
```

### Usage

#### `slurmutils`

The top-level provides access to some utilities that streamline common Slurm-related
operations such as calculating the ranges and strides for a Slurm hostname specification.
Here's some example operations you can perform with these utilities:

##### `calculate_rs`

###### Calculate a range and/or stride from a list of node hostnames

```python3
from os.path import commonprefix

from slurmutils import calculate_rs

nodes = ["juju-abc654-1", "juju-abc654-2", "juju-abc654-4"]
prefix = commonprefix(nodes)
nums = [int(n.partition(prefix)[2]) for n in nodes]
slurm_host_spec = prefix + calculate_rs(nums)  # "juju-abc654-[1-2,4]"
```

###### Calculate a device file range for Nvidia GPUs

```python3
from pathlib import Path

from slurmutils import calculate_rs

device_files = [file for file in Path("/dev").iterdir() if "nvidia" in file.name]
prefix = "/dev/nvidia"
nums = [int(n.partition(prefix)[2]) for n in device_files]
file_spec = prefix + calculate_rs(nums)  # "/dev/nvidia[0-4]"
```

#### `slurmutils.editors`

This module provides an API for editing files, and creating new files if they do not
exist. Here's some operations you can perform on files using the editors in this module:

##### `acctgatherconfig`

###### Edit a pre-existing _acct_gather.conf_ configuration file

```python
from slurmutils.editors import acctgatherconfig

with acctgatherconfig.edit("/etc/slurm/acct_gather.conf") as config:
    config.profile_influx_db_database = "test_acct_gather_db"
    config.profile_influx_db_default = ["NONE"]
    config.profile_influx_db_host = "testhostname1"
    config.profile_influx_db_pass = "testpassword1"
    config.profile_influx_dbrt_policy = "testpolicy1"
    config.profile_influx_db_user = "testuser1"
    config.profile_influx_db_timeout = "20"
```

##### `cgroupconfig`

###### Edit a pre-existing _cgroup.conf_ configuration file

```python
from slurmutils.editors import cgroupconfig

with cgroupconfig.edit("/etc/slurm/cgroup.conf") as config:
    config.constrain_cores = "yes"
    config.constrain_devices = "yes"
    config.constrain_ram_space = "yes"
    config.constrain_swap_space = "yes"
```

##### `gresconfig`

###### Edit a pre-existing _gres.conf_ configuration file

```python
from slurmutils.editors import gresconfig
from slurmutils.models import GRESName, GRESNode

with gresconfig.edit("/etc/slurm/gres.conf") as config:
    new_gres = GRESName(
            Name="gpu",
            Type="epyc",
            File="/dev/amd4",
            Cores=["0", "1"],
        )
    new_node = GRESNode(
        NodeName="juju-abc654-[1-20]",
        Name="gpu",
        Type="epyc",
        File="/dev/amd[0-3]",
        Count="12G",
    )
    config.auto_detect = "rsmi"
    config.names[new_gres.name] = [new_gres]
    config.nodes[new_node.node_name] = [new_node]
```

##### `slurmconfig`

###### Edit a pre-existing _slurm.conf_ configuration file

```python
from slurmutils.editors import slurmconfig

# Open, edit, and save the slurm.conf file located at _/etc/slurm/slurm.conf_.
with slurmconfig.edit("/etc/slurm/slurm.conf") as config:
    del config.inactive_limit
    config.max_job_count = 20000
    config.proctrack_type = "proctrack/linuxproc"
```

###### Add a new node to the _slurm.conf_ file

```python
from slurmutils.editors import slurmconfig
from slurmutils.models import Node

with slurmconfig.edit("/etc/slurm/slurm.conf") as config:
    node = Node(
        NodeName="batch-[0-25]", 
        NodeAddr="12.34.56.78", 
        CPUs=1, 
        RealMemory=1000, 
        TmpDisk=10000,
    )
    config.nodes.update(node.dict())
```

##### `slurmdbdconfig`

###### Edit a pre-existing _slurmdbd.conf_ configuration file

```python
from slurmutils.editors import slurmdbdconfig

with slurmdbdconfig.edit("/etc/slurm/slurmdbd.conf") as config:
    config.archive_usage = "yes"
    config.log_file = "/var/spool/slurmdbd.log"
    config.debug_flags = ["DB_EVENT", "DB_JOB", "DB_USAGE"]
    del config.auth_alt_types
    del config.auth_alt_parameters
```

## 🤔 What's next?

If you want to learn more about all the things you can do with slurmutils, 
here are some further resources for you to explore:

* [Open an issue](https://github.com/charmed-hpc/slurmutils/issues/new?title=ISSUE+TITLE&body=*Please+describe+your+issue*)
* [Ask a question on Github](https://github.com/orgs/charmed-hpc/discussions/categories/q-a)

## 🛠️ Development

This project uses [tox](https://tox.wiki) as its command runner, which provides 
some useful commands that will help you while hacking on slurmutils:

```shell
tox run -e fmt   # Apply formatting standards to code.
tox run -e lint  # Check code against coding style standards.
tox run -e unit  # Run unit tests.
```

If you're interested in contributing your work to slurmutils, 
take a look at our [contributing guidelines](./CONTRIBUTING.md) for further details.

## 🤝 Project and community

slurmutils is a project of the [Ubuntu High-Performance Computing community](https://ubuntu.com/community/governance/teams/hpc).
Interested in contributing bug fixes, new editors, documentation, or feedback? Want to join the Ubuntu HPC community? You’ve come to the right place 🤩

Here’s some links to help you get started with joining the community:

* [Ubuntu Code of Conduct](https://ubuntu.com/community/ethos/code-of-conduct)
* [Contributing guidelines](./CONTRIBUTING.md)
* [Join the conversation on Matrix](https://matrix.to/#/#hpc:ubuntu.com)
* [Get the latest news on Discourse](https://discourse.ubuntu.com/c/hpc/151)
* [Ask and answer questions on GitHub](https://github.com/orgs/charmed-hpc/discussions/categories/q-a)

## 📋 License

slurmutils is free software, distributed under the GNU Lesser General Public License, v3.0.
See the [LGPL-3.0 LICENSE](./LICENSE) file for further details.
