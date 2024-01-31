<div align="center">

# slurmutils

Utilities and APIs for interfacing with the Slurm workload manager.

[![Matrix](https://img.shields.io/matrix/ubuntu-hpc%3Amatrix.org?logo=matrix&label=ubuntu-hpc)](https://matrix.to/#/#ubuntu-hpc:matrix.org)

</div>

## Features

`slurmutils` is a collection of various utilities and APIs to make it easier 
for you and your friends to interface with the Slurm workload manager, especially if you 
are orchestrating deployments of new and current Slurm clusters. Gone are the days of
seething over incomplete Jinja2 templates. Current utilities and APIs shipped in the 
`slurmutils` package include:

#### `from slurmutils.editors import ...`

* `slurmconfig`:  An editor _slurm.conf_ and _Include_ files.
* `slurmdbdconfig`: An editor for _slurmdbd.conf_ files.

## Installation

#### Option 1: Install from PyPI

```shell
$ python3 -m pip install slurmutils
```

#### Option 2: Install from source

We use the [Poetry](https://python-poetry.org) packaging and dependency manager to
manage this project. It must be installed on your system if installing `slurmutils`
from source.

```shell
$ git clone https://github.com/canonical/slurmutils.git
$ cd slurmutils
$ poetry install
```

## Usage

### Editors

#### `slurmconfig`

This module provides an API for editing both _slurm.conf_ and _Include_ files,
and can create new configuration files if they do not exist. Here's some common Slurm
lifecycle management operators you can perform using this editor:

##### Edit a pre-existing _slurm.conf_ configuration file

```python
from slurmutils.editors import slurmconfig

# Open, edit, and save the slurm.conf file located at _/etc/slurm/slurm.conf_.
with slurmconfig.edit("/etc/slurm/slurm.conf") as config:
    del config.inactive_limit
    config.max_job_count = 20000
    config.proctrack_type = "proctrack/linuxproc"
```

##### Add a new node to the _slurm.conf_ file

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
    config.nodes[node.node_name] = node
```

#### `slurmdbdconfig`

This module provides and API for editing _slurmdbd.conf_ files, and can create new
_slurmdbd.conf_ files if they do not exist. Here's some operations you can perform
on the _slurmdbd.conf_ file using this editor:

##### Edit a pre-existing _slurmdbd.conf_ configuration file

```python
from slurmutils.editors import slurmdbdconfig

with slurmdbdconfig.edit("/etc/slurm/slurmdbd.conf") as config:
    config.archive_usage = "yes"
    config.log_file = "/var/spool/slurmdbd.log"
    config.debug_flags = ["DB_EVENT", "DB_JOB", "DB_USAGE"]
    del config.auth_alt_types
    del config.auth_alt_parameters
```

## Project & Community

The `slurmutils` package is a project of the 
[Ubuntu HPC](https://discourse.ubuntu.com/t/high-performance-computing-team/35988) community. 
It is an open-source project that is welcome to community involvement, contributions, suggestions, fixes, 
and constructive feedback. Interested in being involved with the development of `slurmutils`? 
Check out these links below:

* [Join our online chat](https://matrix.to/#/#ubuntu-hpc:matrix.org)
* [Code of Conduct](https://ubuntu.com/community/code-of-conduct)
* [Contributing guidelines](./CONTRIBUTING.md)

## License

The `slurmutils` package is free software, distributed under the GNU Lesser General Public License, v3.0.
See the [LICENSE](./LICENSE) file for more information.
