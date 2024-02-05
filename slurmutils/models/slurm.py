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

"""Generic data models for the Slurm workload manager."""

import functools
from collections import UserList
from collections.abc import MutableMapping
from types import MappingProxyType
from typing import Any, Dict

from ._model import (
    BaseModel,
    ColonSeparatorCallback,
    CommaSeparatorCallback,
    ReasonCallback,
    SlurmDictCallback,
    assert_type,
    base_descriptors,
    nested_descriptors,
    primary_key_descriptors,
)

_node_descriptors = functools.partial(nested_descriptors, knob_key_alias="NodeName")
_frontend_descriptors = functools.partial(nested_descriptors, knob_key_alias="FrontendName")
_nodeset_descriptors = functools.partial(nested_descriptors, knob_key_alias="NodeSet")
_partition_descriptors = functools.partial(nested_descriptors, knob_key_alias="PartitionName")


class Node(BaseModel):
    """Object representing Node(s) definition in slurm.conf.

    Node definition and data validators sourced from
    the slurm.conf manpage. `man slurm.conf.5`
    """

    def __init__(self, **kwargs):
        super().__init__()
        self._register.update({kwargs.pop("NodeName"): {**kwargs}})

    primary_key = "NodeName"
    callbacks = MappingProxyType(
        {
            "cpu_spec_list": CommaSeparatorCallback,
            "features": CommaSeparatorCallback,
            "gres": CommaSeparatorCallback,
            "reason": ReasonCallback,
        }
    )

    node_name = property(*primary_key_descriptors())
    node_hostname = property(*_node_descriptors("NodeHostname"))
    node_addr = property(*_node_descriptors("NodeAddr"))
    bcast_addr = property(*_node_descriptors("BcastAddr"))
    boards = property(*_node_descriptors("Boards"))
    core_spec_count = property(*_node_descriptors("CoreSpecCount"))
    cores_per_socket = property(*_node_descriptors("CoresPerSocket"))
    cpu_bind = property(*_node_descriptors("CpuBind"))
    cpus = property(*_node_descriptors("CPUs"))
    cpu_spec_list = property(*_node_descriptors("CpuSpecList"))
    features = property(*_node_descriptors("Features"))
    gres = property(*_node_descriptors("Gres"))
    mem_spec_limit = property(*_node_descriptors("MemSpecLimit"))
    port = property(*_node_descriptors("Port"))
    procs = property(*_node_descriptors("Procs"))
    real_memory = property(*_node_descriptors("RealMemory"))
    reason = property(*_node_descriptors("Reason"))
    sockets = property(*_node_descriptors("Sockets"))
    sockets_per_board = property(*_node_descriptors("SocketsPerBoard"))
    state = property(*_node_descriptors("State"))
    threads_per_core = property(*_node_descriptors("ThreadsPerCore"))
    tmp_disk = property(*_node_descriptors("TmpDisk"))
    weight = property(*_node_descriptors("Weight"))


class DownNodes(BaseModel):
    """Object representing DownNodes definition in slurm.conf.

    DownNodes definition and data validators sourced from
    the slurm.conf manpage. `man slurm.conf.5`
    """

    primary_key = None
    callbacks = MappingProxyType(
        {
            "down_nodes": CommaSeparatorCallback,
            "reason": ReasonCallback,
        }
    )

    down_nodes = property(*base_descriptors("DownNodes"))
    reason = property(*base_descriptors("Reason"))
    state = property(*base_descriptors("State"))


class FrontendNode(BaseModel):
    """FrontendNode data model.

    FrontendNode definition and data validators sourced from
    the slurm.conf manpage. `man slurm.conf.5`
    """

    def __init__(self, **kwargs):
        super().__init__()
        self._register.update({kwargs.pop("FrontendName"): {**kwargs}})

    primary_key = "FrontendName"
    callbacks = MappingProxyType(
        {
            "allow_groups": CommaSeparatorCallback,
            "allow_users": CommaSeparatorCallback,
            "deny_groups": CommaSeparatorCallback,
            "deny_users": CommaSeparatorCallback,
            "reason": ReasonCallback,
        }
    )

    frontend_name = property(*primary_key_descriptors())
    frontend_addr = property(*_frontend_descriptors("FrontendAddr"))
    allow_groups = property(*_frontend_descriptors("AllowGroups"))
    allow_users = property(*_frontend_descriptors("AllowUsers"))
    deny_groups = property(*_frontend_descriptors("DenyGroups"))
    deny_users = property(*_frontend_descriptors("DenyUsers"))
    port = property(*_frontend_descriptors("Port"))
    reason = property(*_frontend_descriptors("Reason"))
    state = property(*_frontend_descriptors("State"))


class NodeSet(BaseModel):
    """Object representing NodeSet definition in slurm.conf.

    NodeSet definition and data validators sourced from
    the slurm.conf manpage. `man slurm.conf.5`
    """

    def __init__(self, **kwargs):
        super().__init__()
        self._register.update({kwargs.pop("NodeSet"): {**kwargs}})

    primary_key = "NodeSet"
    callbacks = MappingProxyType({"nodes": CommaSeparatorCallback})

    node_set = property(*primary_key_descriptors())
    feature = property(*_nodeset_descriptors("Feature"))
    nodes = property(*_nodeset_descriptors("Nodes"))


class Partition(BaseModel):
    """Object representing Partition definition in slurm.conf.

    Partition definition and data validators sourced from
    the slurm.conf manpage. `man slurm.conf.5`
    """

    def __init__(self, **kwargs):
        super().__init__()
        self._register.update({kwargs.pop("PartitionName"): {**kwargs}})

    primary_key = "PartitionName"
    callbacks = MappingProxyType(
        {
            "alloc_nodes": CommaSeparatorCallback,
            "allow_accounts": CommaSeparatorCallback,
            "allow_groups": CommaSeparatorCallback,
            "allow_qos": CommaSeparatorCallback,
            "deny_accounts": CommaSeparatorCallback,
            "deny_qos": CommaSeparatorCallback,
            "nodes": CommaSeparatorCallback,
            "tres_billing_weights": SlurmDictCallback,
        }
    )

    partition_name = property(*primary_key_descriptors())
    alloc_nodes = property(*_partition_descriptors("AllocNodes"))
    allow_accounts = property(*_partition_descriptors("AllowAccounts"))
    allow_groups = property(*_partition_descriptors("AllowGroups"))
    allow_qos = property(*_partition_descriptors("AllowQos"))
    alternate = property(*_partition_descriptors("Alternate"))
    cpu_bind = property(*_partition_descriptors("CpuBind"))
    default = property(*_partition_descriptors("Default"))
    default_time = property(*_partition_descriptors("DefaultTime"))
    def_cpu_per_gpu = property(*_partition_descriptors("DefCpuPerGPU"))
    def_mem_per_cpu = property(*_partition_descriptors("DefMemPerCPU"))
    def_mem_per_gpu = property(*_partition_descriptors("DefMemPerGPU"))
    def_mem_per_node = property(*_partition_descriptors("DefMemPerNode"))
    deny_accounts = property(*_partition_descriptors("DenyAccounts"))
    deny_qos = property(*_partition_descriptors("DenyQos"))
    disable_root_jobs = property(*_partition_descriptors("DisableRootJobs"))
    exclusive_user = property(*_partition_descriptors("ExclusiveUser"))
    grace_time = property(*_partition_descriptors("GraceTime"))
    hidden = property(*_partition_descriptors("Hidden"))
    lln = property(*_partition_descriptors("LLN"))
    max_cpus_per_node = property(*_partition_descriptors("MaxCPUsPerNode"))
    max_cpus_per_socket = property(*_partition_descriptors("MaxCPUsPerSocket"))
    max_mem_per_cpu = property(*_partition_descriptors("MaxMemPerCPU"))
    max_mem_per_node = property(*_partition_descriptors("MaxMemPerNode"))
    max_nodes = property(*_partition_descriptors("MaxNodes"))
    max_time = property(*_partition_descriptors("MaxTime"))
    min_nodes = property(*_partition_descriptors("MinNodes"))
    nodes = property(*_partition_descriptors("Nodes"))
    over_subscribe = property(*_partition_descriptors("OverSubscribe"))
    over_time_limit = property(*_partition_descriptors("OverTimeLimit"))
    power_down_on_idle = property(*_partition_descriptors("PowerDownOnIdle"))
    preempt_mode = property(*_partition_descriptors("PreemptMode"))
    priority_job_factor = property(*_partition_descriptors("PriorityJobFactor"))
    priority_tier = property(*_partition_descriptors("PriorityTier"))
    qos = property(*_partition_descriptors("QOS"))
    req_resv = property(*_partition_descriptors("ReqResv"))
    resume_timeout = property(*_partition_descriptors("ResumeTimeout"))
    root_only = property(*_partition_descriptors("RootOnly"))
    select_type_parameters = property(*_partition_descriptors("SelectTypeParameters"))
    state = property(*_partition_descriptors("State"))
    suspend_time = property(*_partition_descriptors("SuspendTime"))
    suspend_timeout = property(*_partition_descriptors("SuspendTimeout"))
    tres_billing_weights = property(*_partition_descriptors("TRESBillingWeights"))


class NodeMap(MutableMapping):
    """Map of Node names to dictionaries for composing `Node` objects."""

    def __init__(self, data: Dict[str, Dict[str, Any]]):
        self._register = data

    @assert_type(value=Node)
    def __setitem__(self, key: str, value: Node) -> None:
        if key != value.node_name:
            raise ValueError(f"{key} and {value.node_name} are not equal.")
        else:
            self._register.update(value.dict())

    def __delitem__(self, key: str) -> None:
        del self._register[key]

    def __getitem__(self, key: str) -> Node:
        try:
            node = self._register.get(key)
            return Node(NodeName=key, **node)
        except KeyError:
            raise KeyError(f"Node {key} is not defined.")

    def __len__(self):
        return len(self._register)

    def __iter__(self):
        return iter([Node(NodeName=k, **self._register[k]) for k in self._register.keys()])


class FrontendNodeMap(MutableMapping):
    """Map of FrontendNode names to dictionaries for composing `FrontendNode` objects."""

    def __init__(self, data: Dict[str, Dict[str, Any]]):
        self._register = data

    @assert_type(value=FrontendNode)
    def __setitem__(self, key: str, value: FrontendNode) -> None:
        if key != value.frontend_name:
            raise ValueError(f"{key} and {value.frontend_name} are not equal.")
        else:
            self._register.update(value.dict())

    def __delitem__(self, key: str) -> None:
        del self._register[key]

    def __getitem__(self, key: str) -> FrontendNode:
        try:
            frontend_node = self._register.get(key)
            return FrontendNode(FrontendName=key, **frontend_node)
        except KeyError:
            raise KeyError(f"FrontendNode {key} is not defined.")

    def __len__(self):
        return len(self._register)

    def __iter__(self):
        return iter(
            [FrontendNode(FrontendName=k, **self._register[k]) for k in self._register.keys()]
        )


class DownNodesList(UserList):
    """List of dictionaries for composing `DownNodes` objects."""

    def __getitem__(self, i):
        if isinstance(i, slice):
            return self.__class__(self.data[i])
        else:
            return DownNodes(**self.data[i])

    @assert_type(value=DownNodes)
    def __setitem__(self, i: int, value: DownNodes):
        super().__setitem__(i, value.dict())

    @assert_type(value=DownNodes)
    def __contains__(self, value):
        return value.dict() in self.data

    def __iter__(self):
        return iter([DownNodes(**data) for data in self.data])

    def __add__(self, other):
        if isinstance(other, DownNodesList):
            return self.__class__(self.data + other.data)
        elif isinstance(other, type(self.data)):
            # Cannot use `assert_type` here because isinstance does
            # not support using subscripted generics for runtime validation.
            for down_node in other:
                if not isinstance(down_node, DownNodes):
                    raise TypeError(f"{down_node} is not {type(DownNodes)}.")

            return self.__class__(self.data + other)

        return self.__class__(self.data + list(other))

    def __radd__(self, other):
        if isinstance(other, DownNodesList):
            return self.__class__(other.data + self.data)
        elif isinstance(other, type(self.data)):
            for down_node in other:
                if not isinstance(down_node, DownNodes):
                    raise TypeError(f"{down_node} is not {type(DownNodes)}.")

            return self.__class__(other + self.data)

        return self.__class__(list(other) + self.data)

    def __iadd__(self, other):
        if isinstance(other, DownNodesList):
            self.data += other.data
        elif isinstance(other, type(self.data)):
            for down_node in other:
                if not isinstance(down_node, DownNodes):
                    raise TypeError(f"{down_node} is not {type(DownNodes)}.")

            self.data += other
        else:
            if not isinstance(other, DownNodes):
                raise TypeError(f"{other} is not {type(DownNodes)}.")

            self.data += other
        return self

    @assert_type(value=DownNodes)
    def append(self, value: DownNodes):
        """Add DownNodes object to list of DownNodes."""
        super().append(value.dict())

    @assert_type(value=DownNodes)
    def insert(self, i, value):
        """Insert DownNodes object into list of DownNodes at the given index."""
        super().insert(i, value.dict())

    @assert_type(value=DownNodes)
    def remove(self, value):
        """Remove DownNodes object from list of DownNodes."""
        self.data.remove(value.dict())

    @assert_type(value=DownNodes)
    def count(self, value):
        """Count the numbers of occurrences for the given DownNodes object.

        Warnings:
            Each DownNodes object should only occur once (1). If the object
            occurs more than once, this can create BIG problems when trying to
            restart the Slurm daemons.
        """
        return self.data.count(value.dict())

    @assert_type(value=DownNodes)
    def index(self, value, *args):
        """Get the index of the give DownNodes object."""
        return self.data.index(value.dict(), *args)

    def extend(self, other):
        """Extend DownNodes list by appending DownNodes objects from the iterable."""
        if isinstance(other, DownNodesList):
            self.data.extend(other.data)
        else:
            for down_node in other:
                if not isinstance(down_node, DownNodes):
                    raise TypeError(f"{down_node} is not {type(DownNodes)}.")

            self.data.extend(other)


class NodeSetMap(MutableMapping):
    """Map of NodeSet names to dictionaries for composing `NodeSet` objects."""

    def __init__(self, data: Dict[str, Dict[str, Any]]):
        self._register = data

    @assert_type(value=NodeSet)
    def __setitem__(self, key: str, value: NodeSet) -> None:
        if key != value.node_set:
            raise ValueError(f"{key} and {value.node_set} are not equal.")
        else:
            self._register.update(value.dict())

    def __delitem__(self, key: str) -> None:
        del self._register[key]

    def __getitem__(self, key: str) -> NodeSet:
        try:
            node_set = self._register.get(key)
            return NodeSet(NodeSet=key, **node_set)
        except KeyError:
            raise KeyError(f"NodeSet {key} is not defined.")

    def __len__(self):
        return len(self._register)

    def __iter__(self):
        return iter([NodeSet(NodeSet=k, **self._register[k]) for k in self._register.keys()])


class PartitionMap(MutableMapping):
    """Map of Partition names to dictionaries for composing `Partition` objects."""

    def __init__(self, data: Dict[str, Dict[str, Any]]):
        self._register = data

    def __contains__(self, key: str):
        return key in self._register

    def __len__(self):
        return len(self._register)

    def __iter__(self):
        return iter(
            [Partition(PartitionName=k, **self._register[k]) for k in self._register.keys()]
        )

    def __getitem__(self, key: str) -> Partition:
        try:
            partition = self._register.get(key)
            return Partition(PartitionName=key, **partition)
        except KeyError:
            raise KeyError(f"Partition {key} is not defined.")

    @assert_type(value=Partition)
    def __setitem__(self, key: str, value: Partition) -> None:
        if key != value.partition_name:
            raise ValueError(f"{key} and {value.partition_name} are not equal.")
        else:
            self._register.update(value.dict())

    def __delitem__(self, key: str) -> None:
        del self._register[key]


class SlurmConfig(BaseModel):
    """Object representing the slurm.conf configuration file.

    Top-level configuration definition and data validators sourced from
    the slurm.conf manpage. `man slurm.conf.5`
    """

    primary_key = None
    callbacks = MappingProxyType(
        {
            "acct_storage_external_host": CommaSeparatorCallback,
            "acct_storage_param": SlurmDictCallback,
            "acct_storage_tres": CommaSeparatorCallback,
            "acct_store_flags": CommaSeparatorCallback,
            "auth_alt_types": CommaSeparatorCallback,
            "auth_alt_param": SlurmDictCallback,
            "auth_info": SlurmDictCallback,
            "bcast_exclude": CommaSeparatorCallback,
            "bcast_param": SlurmDictCallback,
            "cli_filter_plugins": CommaSeparatorCallback,
            "communication_params": SlurmDictCallback,
            "cpu_freq_def": CommaSeparatorCallback,
            "cpu_freq_governors": CommaSeparatorCallback,
            "debug_flags": CommaSeparatorCallback,
            "dependency_param": SlurmDictCallback,
            "federation_param": CommaSeparatorCallback,
            "health_check_node_state": CommaSeparatorCallback,
            "job_acct_gather_frequency": SlurmDictCallback,
            "job_comp_params": SlurmDictCallback,
            "job_submit_plugins": CommaSeparatorCallback,
            "launch_parameters": SlurmDictCallback,
            "licenses": CommaSeparatorCallback,
            "plugin_dir": ColonSeparatorCallback,
            "power_parameters": SlurmDictCallback,
            "preempt_mode": CommaSeparatorCallback,
            "preempt_param": SlurmDictCallback,
            "prep_plugins": CommaSeparatorCallback,
            "priority_weight_tres": SlurmDictCallback,
            "private_data": CommaSeparatorCallback,
            "prolog_flags": CommaSeparatorCallback,
            "propagate_resource_limits": CommaSeparatorCallback,
            "propagate_resource_limits_except": CommaSeparatorCallback,
            "scheduler_param": SlurmDictCallback,
            "scron_param": CommaSeparatorCallback,
            "slurmctld_param": SlurmDictCallback,
            "slurmd_param": CommaSeparatorCallback,
            "switch_param": SlurmDictCallback,
            "task_plugin": CommaSeparatorCallback,
            "task_plugin_param": SlurmDictCallback,
            "topology_param": CommaSeparatorCallback,
        }
    )

    include = property(*base_descriptors("Include"))
    accounting_storage_backup_host = property(*base_descriptors("AccountingStorageBackupHost"))
    accounting_storage_enforce = property(*base_descriptors("AccountingStorageEnforce"))
    account_storage_external_host = property(*base_descriptors("AccountStorageExternalHost"))
    accounting_storage_host = property(*base_descriptors("AccountingStorageHost"))
    accounting_storage_parameters = property(*base_descriptors("AccountingStorageParameters"))
    accounting_storage_pass = property(*base_descriptors("AccountingStoragePass"))
    accounting_storage_port = property(*base_descriptors("AccountingStoragePort"))
    accounting_storage_tres = property(*base_descriptors("AccountingStorageTRES"))
    accounting_storage_type = property(*base_descriptors("AccountingStorageType"))
    accounting_storage_user = property(*base_descriptors("AccountingStorageUser"))
    accounting_store_flags = property(*base_descriptors("AccountingStoreFlags"))
    acct_gather_node_freq = property(*base_descriptors("AcctGatherNodeFreq"))
    acct_gather_energy_type = property(*base_descriptors("AcctGatherEnergyType"))
    acct_gather_interconnect_type = property(*base_descriptors("AcctGatherInterconnectType"))
    acct_gather_filesystem_type = property(*base_descriptors("AcctGatherFilesystemType"))
    acct_gather_profile_type = property(*base_descriptors("AcctGatherProfileType"))
    allow_spec_resources_usage = property(*base_descriptors("AllowSpecResourcesUsage"))
    auth_alt_types = property(*base_descriptors("AuthAltTypes"))
    auth_alt_parameters = property(*base_descriptors("AuthAltParameters"))
    auth_info = property(*base_descriptors("AuthInfo"))
    auth_type = property(*base_descriptors("AuthType"))
    batch_start_timeout = property(*base_descriptors("BatchStartTimeout"))
    bcast_exclude = property(*base_descriptors("BcastExclude"))
    bcast_parameters = property(*base_descriptors("BcastParameters"))
    burst_buffer_type = property(*base_descriptors("BurstBufferType"))
    cli_filter_plugins = property(*base_descriptors("CliFilterPlugins"))
    cluster_name = property(*base_descriptors("ClusterName"))
    communication_parameters = property(*base_descriptors("CommunicationParameters"))
    complete_wait = property(*base_descriptors("CompleteWait"))
    core_spec_plugin = property(*base_descriptors("CoreSpecPlugin"))
    cpu_freq_def = property(*base_descriptors("CpuFreqDef"))
    cpu_freq_governors = property(*base_descriptors("CpuFreqGovernors"))
    cred_type = property(*base_descriptors("CredType"))
    debug_flags = property(*base_descriptors("DebugFlags"))
    def_cpu_per_gpu = property(*base_descriptors("DefCpuPerGPU"))
    def_mem_per_cpu = property(*base_descriptors("DefMemPerCPU"))
    def_mem_per_gpu = property(*base_descriptors("DefMemPerGPU"))
    def_mem_per_node = property(*base_descriptors("DefMemPerNode"))
    dependency_parameters = property(*base_descriptors("DependencyParameters"))
    disable_root_jobs = property(*base_descriptors("DisableRootJobs"))
    eio_timeout = property(*base_descriptors("EioTimeout"))
    enforce_part_limits = property(*base_descriptors("EnforcePartLimits"))
    epilog = property(*base_descriptors("Epilog"))
    epilog_msg_time = property(*base_descriptors("EpilogMsgTime"))
    epilog_slurmctld = property(*base_descriptors("EpilogSlurmctld"))
    ext_sensors_freq = property(*base_descriptors("ExtSensorsFreq"))
    ext_sensors_type = property(*base_descriptors("ExtSensorsType"))
    fair_share_dampening_factor = property(*base_descriptors("FairShareDampeningFactor"))
    federation_parameters = property(*base_descriptors("FederationParameters"))
    first_job_id = property(*base_descriptors("FirstJobId"))
    get_env_timeout = property(*base_descriptors("GetEnvTimeout"))
    gres_types = property(*base_descriptors("GresTypes"))
    group_update_force = property(*base_descriptors("GroupUpdateForce"))
    group_update_time = property(*base_descriptors("GroupUpdateTime"))
    gpu_freq_def = property(*base_descriptors("GpuFreqDef"))
    health_check_interval = property(*base_descriptors("HealthCheckInterval"))
    health_check_node_state = property(*base_descriptors("HealthCheckNodeState"))
    health_check_program = property(*base_descriptors("HealthCheckProgram"))
    inactive_limit = property(*base_descriptors("InactiveLimit"))
    interactive_step_options = property(*base_descriptors("InteractiveStepOptions"))
    job_acct_gather_type = property(*base_descriptors("JobAcctGatherType"))
    job_acct_gather_frequency = property(*base_descriptors("JobAcctGatherFrequency"))
    job_acct_gather_params = property(*base_descriptors("JobAcctGatherParams"))
    job_comp_host = property(*base_descriptors("JobCompHost"))
    job_comp_loc = property(*base_descriptors("JobCompLoc"))
    job_comp_params = property(*base_descriptors("JobCompParams"))
    job_comp_pass = property(*base_descriptors("JobCompPass"))
    job_comp_port = property(*base_descriptors("JobCompPort"))
    job_comp_type = property(*base_descriptors("JobCompType"))
    job_comp_user = property(*base_descriptors("JobCompUser"))
    job_container_type = property(*base_descriptors("JobContainerType"))
    job_file_append = property(*base_descriptors("JobFileAppend"))
    job_requeue = property(*base_descriptors("JobRequeue"))
    job_submit_plugins = property(*base_descriptors("JobSubmitPlugins"))
    kill_on_bad_exit = property(*base_descriptors("KillOnBadExit"))
    kill_wait = property(*base_descriptors("KillWait"))
    max_batch_requeue = property(*base_descriptors("MaxBatchRequeue"))
    node_features_plugins = property(*base_descriptors("NodeFeaturesPlugins"))
    launch_parameters = property(*base_descriptors("LaunchParameters"))
    licenses = property(*base_descriptors("Licenses"))
    log_time_format = property(*base_descriptors("LogTimeFormat"))
    mail_domain = property(*base_descriptors("MailDomain"))
    mail_prog = property(*base_descriptors("MailProg"))
    max_array_size = property(*base_descriptors("MaxArraySize"))
    max_job_count = property(*base_descriptors("MaxJobCount"))
    max_job_id = property(*base_descriptors("MaxJobId"))
    max_mem_per_cpu = property(*base_descriptors("MaxMemPerCPU"))
    max_mem_per_node = property(*base_descriptors("MaxMemPerNode"))
    max_node_count = property(*base_descriptors("MaxNodeCount"))
    max_step_count = property(*base_descriptors("MaxStepCount"))
    max_tasks_per_node = property(*base_descriptors("MaxTasksPerNode"))
    mcs_parameters = property(*base_descriptors("MCSParameters"))
    mcs_plugin = property(*base_descriptors("MCSPlugin"))
    message_timeout = property(*base_descriptors("MessageTimeout"))
    min_job_age = property(*base_descriptors("MinJobAge"))
    mpi_default = property(*base_descriptors("MpiDefault"))
    mpi_params = property(*base_descriptors("MpiParams"))
    over_time_limit = property(*base_descriptors("OverTimeLimit"))
    plugin_dir = property(*base_descriptors("PluginDir"))
    plug_stack_config = property(*base_descriptors("PlugStackConfig"))
    power_parameters = property(*base_descriptors("PowerParameters"))
    power_plugin = property(*base_descriptors("PowerPlugin"))
    preempt_mode = property(*base_descriptors("PreemptMode"))
    preempt_parameters = property(*base_descriptors("PreemptParameters"))
    preempt_type = property(*base_descriptors("PreemptType"))
    preempt_exempt_time = property(*base_descriptors("PreemptExemptTime"))
    prep_parameters = property(*base_descriptors("PrEpParameters"))
    prep_plugins = property(*base_descriptors("PrEpPlugins"))
    priority_calcp_period = property(*base_descriptors("PriorityCalcpPeriod"))
    priority_decay_half_life = property(*base_descriptors("PriorityDecayHalfLife"))
    priority_favor_small = property(*base_descriptors("PriorityFavorSmall"))
    priority_flags = property(*base_descriptors("PriorityFlags"))
    priority_max_age = property(*base_descriptors("PriorityMaxAge"))
    priority_parameters = property(*base_descriptors("PriorityParameters"))
    priority_site_factor_parameters = property(*base_descriptors("PrioritySiteFactorParameters"))
    priority_site_factor_plugin = property(*base_descriptors("PrioritySiteFactorPlugin"))
    priority_type = property(*base_descriptors("PriorityType"))
    priority_usage_reset_period = property(*base_descriptors("PriorityUsageResetPeriod"))
    priority_weight_age = property(*base_descriptors("PriorityWeightAge"))
    priority_weight_assoc = property(*base_descriptors("PriorityWeightAssoc"))
    priority_weight_fair_share = property(*base_descriptors("PriorityWeightFairShare"))
    priority_weight_job_size = property(*base_descriptors("PriorityWeightJobSize"))
    priority_weight_partition = property(*base_descriptors("PriorityWeightPartition"))
    priority_weight_qos = property(*base_descriptors("PriorityWeightQOS"))
    priority_weight_tres = property(*base_descriptors("PriorityWeightTRES"))
    private_data = property(*base_descriptors("PrivateData"))
    proctrack_type = property(*base_descriptors("ProctrackType"))
    prolog = property(*base_descriptors("Prolog"))
    prolog_epilog_timeout = property(*base_descriptors("PrologEpilogTimeout"))
    prolog_flags = property(*base_descriptors("PrologFlags"))
    prolog_slurmctld = property(*base_descriptors("PrologSlurmctld"))
    propagate_prio_process = property(*base_descriptors("PropagatePrioProcess"))
    propagate_resource_limits = property(*base_descriptors("PropagateResourceLimits"))
    propagate_resource_limits_except = property(*base_descriptors("PropagateResourceLimitsExcept"))
    reboot_program = property(*base_descriptors("RebootProgram"))
    reconfig_flags = property(*base_descriptors("ReconfigFlags"))
    requeue_exit = property(*base_descriptors("RequeueExit"))
    requeue_exit_hold = property(*base_descriptors("RequeueExitHold"))
    resume_fail_program = property(*base_descriptors("ResumeFailProgram"))
    resume_program = property(*base_descriptors("ResumeProgram"))
    resume_rate = property(*base_descriptors("ResumeRate"))
    resume_timeout = property(*base_descriptors("ResumeTimeout"))
    resv_epilog = property(*base_descriptors("ResvEpilog"))
    resv_over_run = property(*base_descriptors("ResvOverRun"))
    resv_prolog = property(*base_descriptors("ResvProlog"))
    return_to_service = property(*base_descriptors("ReturnToService"))
    route_plugin = property(*base_descriptors("RoutePlugin"))
    scheduler_parameters = property(*base_descriptors("SchedulerParameters"))
    scheduler_time_slice = property(*base_descriptors("SchedulerTimeSlice"))
    scheduler_type = property(*base_descriptors("SchedulerType"))
    scron_parameters = property(*base_descriptors("ScronParameters"))
    select_type = property(*base_descriptors("SelectType"))
    select_type_parameters = property(*base_descriptors("SelectTypeParameters"))
    slurmctld_addr = property(*base_descriptors("SlurmctldAddr"))
    slurmctld_debug = property(*base_descriptors("SlurmctldDebug"))
    slurmctld_host = property(*base_descriptors("SlurmctldHost"))
    slurmctld_log_file = property(*base_descriptors("SlurmctldLogFile"))
    slurmctld_parameters = property(*base_descriptors("SlurmctldParameters"))
    slurmctld_pid_file = property(*base_descriptors("SlurmctldPidFile"))
    slurmctld_port = property(*base_descriptors("SlurmctldPort"))
    slurmctld_primary_off_prog = property(*base_descriptors("SlurmctldPrimaryOffProg"))
    slurmctld_primary_on_prog = property(*base_descriptors("SlurmctldPrimaryOnProg"))
    slurmctld_syslog_debug = property(*base_descriptors("SlurmctldSyslogDebug"))
    slurmctld_timeout = property(*base_descriptors("SlurmctldTimeout"))
    slurmd_debug = property(*base_descriptors("SlurmdDebug"))
    slurmd_log_file = property(*base_descriptors("SlurmdLogFile"))
    slurmd_parameters = property(*base_descriptors("SlurmdParameters"))
    slurmd_pid_file = property(*base_descriptors("SlurmdPidFile"))
    slurmd_port = property(*base_descriptors("SlurmdPort"))
    slurmd_spool_dir = property(*base_descriptors("SlurmdSpoolDir"))
    slurmd_syslog_debug = property(*base_descriptors("SlurmdSyslogDebug"))
    slurmd_timeout = property(*base_descriptors("SlurmdTimeout"))
    slurmd_user = property(*base_descriptors("SlurmdUser"))
    slurm_sched_log_file = property(*base_descriptors("SlurmSchedLogFile"))
    slurm_sched_log_level = property(*base_descriptors("SlurmSchedLogLevel"))
    slurm_user = property(*base_descriptors("SlurmUser"))
    srun_epilog = property(*base_descriptors("SrunEpilog"))
    srun_port_range = property(*base_descriptors("SrunPortRange"))
    srun_prolog = property(*base_descriptors("SrunProlog"))
    state_save_location = property(*base_descriptors("StateSaveLocation"))
    suspend_exc_nodes = property(*base_descriptors("SuspendExcNodes"))
    suspend_exc_parts = property(*base_descriptors("SuspendExcParts"))
    suspend_exc_states = property(*base_descriptors("SuspendExcStates"))
    suspend_program = property(*base_descriptors("SuspendProgram"))
    suspend_rate = property(*base_descriptors("SuspendRate"))
    suspend_time = property(*base_descriptors("SuspendTime"))
    suspend_timeout = property(*base_descriptors("SuspendTimeout"))
    switch_parameters = property(*base_descriptors("SwitchParameters"))
    switch_type = property(*base_descriptors("SwitchType"))
    task_epilog = property(*base_descriptors("TaskEpilog"))
    task_plugin = property(*base_descriptors("TaskPlugin"))
    task_plugin_param = property(*base_descriptors("TaskPluginParam"))
    task_prolog = property(*base_descriptors("TaskProlog"))
    tcp_timeout = property(*base_descriptors("TCPTimeout"))
    tmp_fs = property(*base_descriptors("TmpFS"))
    topology_param = property(*base_descriptors("TopologyParam"))
    topology_plugin = property(*base_descriptors("TopologyPlugin"))
    track_wc_key = property(*base_descriptors("TrackWCKey"))
    tree_width = property(*base_descriptors("TreeWidth"))
    unkillable_step_program = property(*base_descriptors("UnkillableStepProgram"))
    unkillable_step_timeout = property(*base_descriptors("UnkillableStepTimeout"))
    use_pam = property(*base_descriptors("UsePAM"))
    vsize_factor = property(*base_descriptors("VSizeFactor"))
    wait_time = property(*base_descriptors("WaitTime"))
    x11_parameters = property(*base_descriptors("X11Parameters"))

    @property
    def nodes(self) -> NodeMap:
        """Get the current nodes in the Slurm configuration."""
        return NodeMap(self._register["nodes"])

    @property
    def frontend_nodes(self) -> FrontendNodeMap:
        """Get the current frontend nodes in the Slurm configuration."""
        return FrontendNodeMap(self._register["frontend_nodes"])

    @property
    def down_nodes(self) -> DownNodesList:
        """Get the current down nodes in the Slurm configuration."""
        return DownNodesList(self._register["down_nodes"])

    @property
    def node_sets(self) -> NodeSetMap:
        """Get the current node sets in the Slurm configuration."""
        return NodeSetMap(self._register["node_sets"])

    @property
    def partitions(self) -> PartitionMap:
        """Get the current partitions in the Slurm configuration."""
        return PartitionMap(self._register["partitions"])
