<h1 align="center">
  slurmutils
</h1>

<p align="center">
  Utilities and APIs for interacting with the SLURM workload manager.
</p>

## Features

* `slurmconf`: An API for performing CRUD operations on the SLURM configuration file _slurm.conf_

## Installation

#### Option 1: PyPI

```shell
$ python3 -m pip install slurmutils
```

#### Option 2: Install from source

```shell
$ git clone https://github.com/canonical/slurmutils.git
$ cd slurmutils
$ python3 -m pip install .
```

## Usage

#### `slurmconf`

This module provides an API for performing CRUD operations on the SLURM configuration file _slurm.conf_.
With this module, you can:

##### Edit a pre-existing configuration

```python
from slurmutils.slurmconf import SlurmConf

with SlurmConf("/etc/slurm/slurm.conf") as conf:
    del conf.inactive_limit
    conf.max_job_count = 20000
    conf.proctrack_type = "proctrack/linuxproc"
```

##### Add new nodes

```python3
from slurmutils.slurmconf import Node, SlurmConf

with SlurmConf("/etc/slurm/slurm.conf") as conf:
    node_name = "test-node"
    node_conf = {
        "NodeName": node_name,
        "NodeAddr": "12.34.56.78",
        "CPUs": 1, 
        "RealMemory": 1000, 
        "TmpDisk": 10000,
    }
    conf.nodes.update({node_name: Node(**node_conf)})
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

The `slurmutils` package is free software, distributed under the Apache Software License, version 2.0.
See the [LICENSE](./LICENSE) file for more information.
