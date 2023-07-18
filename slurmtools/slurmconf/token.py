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

"""SLURM configuration option tokens."""

from typing import NamedTuple

from .callback import (
    Callback,
    acct_storage_external_host,
    acct_storage_param,
    acct_storage_tres,
    acct_store_flags,
    auth_alt_param,
    auth_alt_types,
    auth_info,
    bcast_exclude,
    bcast_param,
    cli_filter_plugins,
    communication_params,
    cpu_freq_def,
    cpu_freq_governors,
    debug_flags,
    dependency_param,
    down_name,
    down_reason,
    federation_param,
    frontend_allow_groups,
    frontend_allow_users,
    frontend_deny_groups,
    frontend_deny_users,
    frontend_reason,
    health_check_node_state,
    job_acct_gather_frequency,
    job_comp_params,
    job_submit_plugins,
    launch_parameters,
    licenses,
    node_cpu_spec_list,
    node_features,
    node_gres,
    node_reason,
    partition_alloc_nodes,
    partition_allow_accounts,
    partition_allow_groups,
    partition_allow_qos,
    partition_deny_accounts,
    partition_deny_qos,
    partition_nodes,
    partition_tres_billing_weights,
    plugin_dir,
    power_parameters,
    preempt_mode,
    preempt_param,
    prep_plugins,
    priority_weight_tres,
    private_data,
    prolog_flags,
    propagate_resource_limits,
    propagate_resource_limits_except,
    scheduler_param,
    scron_param,
    slurmctld_param,
    slurmd_param,
    switch_param,
    task_plugin,
    task_plugin_param,
    topology_param,
)


class _SlurmConfOpts(NamedTuple):
    """Top-level SLURM configuration options."""

    Include: Callback = Callback()
    AccountingStorageBackupHost: Callback = Callback()
    AccountingStorageEnforce: Callback = Callback()
    AccountStorageExternalHost: Callback = acct_storage_external_host
    AccountingStorageHost: Callback = Callback()
    AccountingStorageParameters: Callback = acct_storage_param
    AccountingStoragePass: Callback = Callback()
    AccountingStoragePort: Callback = Callback()
    AccountingStorageTRES: Callback = acct_storage_tres
    AccountingStorageType: Callback = Callback()
    AccountingStorageUser: Callback = Callback()
    AccountingStoreFlags: Callback = acct_store_flags
    AcctGatherNodeFreq: Callback = Callback()
    AcctGatherEnergyType: Callback = Callback()
    AcctGatherInterconnectType: Callback = Callback()
    AcctGatherFilesystemType: Callback = Callback()
    AcctGatherProfileType: Callback = Callback()
    AllowSpecResourcesUsage: Callback = Callback()
    AuthAltTypes: Callback = auth_alt_types
    AuthAltParameters: Callback = auth_alt_param
    AuthInfo: Callback = auth_info
    AuthType: Callback = Callback()
    BatchStartTimeout: Callback = Callback()
    BcastExclude: Callback = bcast_exclude
    BcastParameters: Callback = bcast_param
    BurstBufferType: Callback = Callback()
    CliFilterPlugins: Callback = cli_filter_plugins
    ClusterName: Callback = Callback()
    CommunicationParameters: Callback = communication_params
    CompleteWait: Callback = Callback()
    CoreSpecPlugin: Callback = Callback()
    CpuFreqDef: Callback = cpu_freq_def
    CpuFreqGovernors: Callback = cpu_freq_governors
    CredType: Callback = Callback()
    DebugFlags: Callback = debug_flags
    DefCpuPerGPU: Callback = Callback()
    DefMemPerCPU: Callback = Callback()
    DefMemPerGPU: Callback = Callback()
    DefMemPerNode: Callback = Callback()
    DependencyParameters: Callback = dependency_param
    DisableRootJobs: Callback = Callback()
    EioTimeout: Callback = Callback()
    EnforcePartLimits: Callback = Callback()
    Epilog: Callback = Callback()
    EpilogMsgTime: Callback = Callback()
    EpilogSlurmctld: Callback = Callback()
    ExtSensorsFreq: Callback = Callback()
    ExtSensorsType: Callback = Callback()
    FairShareDampeningFactor: Callback = Callback()
    FederationParameters: Callback = federation_param
    FirstJobId: Callback = Callback()
    GetEnvTimeout: Callback = Callback()
    GresTypes: Callback = Callback()
    GroupUpdateForce: Callback = Callback()
    GroupUpdateTime: Callback = Callback()
    GpuFreqDef: Callback = Callback()
    HealthCheckInterval: Callback = Callback()
    HealthCheckNodeState: Callback = health_check_node_state
    HealthCheckProgram: Callback = Callback()
    InactiveLimit: Callback = Callback()
    InteractiveStepOptions: Callback = Callback()
    JobAcctGatherType: Callback = Callback()
    JobAcctGatherFrequency: Callback = job_acct_gather_frequency
    JobAcctGatherParams: Callback = Callback()
    JobCompHost: Callback = Callback()
    JobCompLoc: Callback = Callback()
    JobCompParams: Callback = job_comp_params
    JobCompPass: Callback = Callback()
    JobCompPort: Callback = Callback()
    JobCompType: Callback = Callback()
    JobCompUser: Callback = Callback()
    JobContainerType: Callback = Callback()
    JobFileAppend: Callback = Callback()
    JobRequeue: Callback = Callback()
    JobSubmitPlugins: Callback = job_submit_plugins
    KillOnBadExit: Callback = Callback()
    KillWait: Callback = Callback()
    MaxBatchRequeue: Callback = Callback()
    NodeFeaturesPlugins: Callback = Callback()
    LaunchParameters: Callback = launch_parameters
    Licenses: Callback = licenses
    LogTimeFormat: Callback = Callback()
    MailDomain: Callback = Callback()
    MailProg: Callback = Callback()
    MaxArraySize: Callback = Callback()
    MaxJobCount: Callback = Callback()
    MaxJobId: Callback = Callback()
    MaxMemPerCPU: Callback = Callback()
    MaxMemPerNode: Callback = Callback()
    MaxNodeCount: Callback = Callback()
    MaxStepCount: Callback = Callback()
    MaxTasksPerNode: Callback = Callback()
    MCSParameters: Callback = Callback()
    MCSPlugin: Callback = Callback()
    MessageTimeout: Callback = Callback()
    MinJobAge: Callback = Callback()
    MpiDefault: Callback = Callback()
    MpiParams: Callback = Callback()
    OverTimeLimit: Callback = Callback()
    PluginDir: Callback = plugin_dir
    PlugStackConfig: Callback = Callback()
    PowerParameters: Callback = power_parameters
    PowerPlugin: Callback = Callback()
    PreemptMode: Callback = preempt_mode
    PreemptParameters: Callback = preempt_param
    PreemptType: Callback = Callback()
    PreemptExemptTime: Callback = Callback()
    PrEpParameters: Callback = Callback()
    PrEpPlugins: Callback = prep_plugins
    PriorityCalcpPeriod: Callback = Callback()
    PriorityDecayHalfLife: Callback = Callback()
    PriorityFavorSmall: Callback = Callback()
    PriorityFlags: Callback = Callback()
    PriorityMaxAge: Callback = Callback()
    PriorityParameters: Callback = Callback()
    PrioritySiteFactorParameters: Callback = Callback()
    PrioritySiteFactorPlugin: Callback = Callback()
    PriorityType: Callback = Callback()
    PriorityUsageResetPeriod: Callback = Callback()
    PriorityWeightAge: Callback = Callback()
    PriorityWeightAssoc: Callback = Callback()
    PriorityWeightFairShare: Callback = Callback()
    PriorityWeightJobSize: Callback = Callback()
    PriorityWeightPartition: Callback = Callback()
    PriorityWeightQOS: Callback = Callback()
    PriorityWeightTRES: Callback = priority_weight_tres
    PrivateData: Callback = private_data
    ProctrackType: Callback = Callback()
    Prolog: Callback = Callback()
    PrologEpilogTimeout: Callback = Callback()
    PrologFlags: Callback = prolog_flags
    PrologSlurmctld: Callback = Callback()
    PropagatePrioProcess: Callback = Callback()
    PropagateResourceLimits: Callback = propagate_resource_limits
    PropagateResourceLimitsExcept: Callback = propagate_resource_limits_except
    RebootProgram: Callback = Callback()
    ReconfigFlags: Callback = Callback()
    RequeueExit: Callback = Callback()
    RequeueExitHold: Callback = Callback()
    ResumeFailProgram: Callback = Callback()
    ResumeProgram: Callback = Callback()
    ResumeRate: Callback = Callback()
    ResumeTimeout: Callback = Callback()
    ResvEpilog: Callback = Callback()
    ResvOverRun: Callback = Callback()
    ResvProlog: Callback = Callback()
    ReturnToService: Callback = Callback()
    RoutePlugin: Callback = Callback()
    SchedulerParameters: Callback = scheduler_param
    SchedulerTimeSlice: Callback = Callback()
    SchedulerType: Callback = Callback()
    ScronParameters: Callback = scron_param
    SelectType: Callback = Callback()
    SelectTypeParameters: Callback = Callback()
    SlurmctldAddr: Callback = Callback()
    SlurmctldDebug: Callback = Callback()
    SlurmctldHost: Callback = Callback()
    SlurmctldLogFile: Callback = Callback()
    SlurmctldParameters: Callback = slurmctld_param
    SlurmctldPidFile: Callback = Callback()
    SlurmctldPort: Callback = Callback()
    SlurmctldPrimaryOffProg: Callback = Callback()
    SlurmctldPrimaryOnProg: Callback = Callback()
    SlurmctldSyslogDebug: Callback = Callback()
    SlurmctldTimeout: Callback = Callback()
    SlurmdDebug: Callback = Callback()
    SlurmdLogFile: Callback = Callback()
    SlurmdParameters: Callback = slurmd_param
    SlurmdPidFile: Callback = Callback()
    SlurmdPort: Callback = Callback()
    SlurmdSpoolDir: Callback = Callback()
    SlurmdSyslogDebug: Callback = Callback()
    SlurmdTimeout: Callback = Callback()
    SlurmdUser: Callback = Callback()
    SlurmSchedLogFile: Callback = Callback()
    SlurmSchedLogLevel: Callback = Callback()
    SlurmUser: Callback = Callback()
    SrunEpilog: Callback = Callback()
    SrunPortRange: Callback = Callback()
    SrunProlog: Callback = Callback()
    StateSaveLocation: Callback = Callback()
    SuspendExcNodes: Callback = Callback()
    SuspendExcParts: Callback = Callback()
    SuspendExcStates: Callback = Callback()
    SuspendProgram: Callback = Callback()
    SuspendRate: Callback = Callback()
    SuspendTime: Callback = Callback()
    SuspendTimeout: Callback = Callback()
    SwitchParameters: Callback = switch_param
    SwitchType: Callback = Callback()
    TaskEpilog: Callback = Callback()
    TaskPlugin: Callback = task_plugin
    TaskPluginParam: Callback = task_plugin_param
    TaskProlog: Callback = Callback()
    TCPTimeout: Callback = Callback()
    TmpFS: Callback = Callback()
    TopologyParam: Callback = topology_param
    TopologyPlugin: Callback = Callback()
    TrackWCKey: Callback = Callback()
    TreeWidth: Callback = Callback()
    UnkillableStepProgram: Callback = Callback()
    UnkillableStepTimeout: Callback = Callback()
    UsePAM: Callback = Callback()
    VSizeFactor: Callback = Callback()
    WaitTime: Callback = Callback()
    X11Parameters: Callback = Callback()


class _NodeConfOpts(NamedTuple):
    """SLURM node configuration options."""

    NodeName: Callback = Callback()
    NodeHostname: Callback = Callback()
    NodeAddr: Callback = Callback()
    BcastAddr: Callback = Callback()
    Boards: Callback = Callback()
    CoreSpecCount: Callback = Callback()
    CoresPerSocket: Callback = Callback()
    CpuBind: Callback = Callback()
    CPUs: Callback = Callback()
    CpuSpecList: Callback = node_cpu_spec_list
    Features: Callback = node_features
    Gres: Callback = node_gres
    MemSpecLimit: Callback = Callback()
    Port: Callback = Callback()
    Procs: Callback = Callback()
    RealMemory: Callback = Callback()
    Reason: Callback = node_reason
    Sockets: Callback = Callback()
    SocketsPerBoard: Callback = Callback()
    State: Callback = Callback()
    ThreadsPerCore: Callback = Callback()
    TmpDisk: Callback = Callback()
    Weight: Callback = Callback()


class _DownNodeConfOpts(NamedTuple):
    """SLURM down node configuration options."""

    DownNodes: Callback = down_name
    Reason: Callback = down_reason
    State: Callback = Callback()


class _FrontendNodeConfOpts(NamedTuple):
    """SLURM frontend node configuration options."""

    FrontendName: Callback = Callback()
    FrontendAddr: Callback = Callback()
    AllowGroups: Callback = frontend_allow_groups
    AllowUsers: Callback = frontend_allow_users
    DenyGroups: Callback = frontend_deny_groups
    DenyUsers: Callback = frontend_deny_users
    Port: Callback = Callback()
    Reason: Callback = frontend_reason
    State: Callback = Callback()


class _NodeSetConfOpts(NamedTuple):
    """SLURM nodeset configuration options."""

    NodeSet: Callback = Callback()
    Feature: Callback = Callback()
    Nodes: Callback = Callback()


class _PartitionConfOpts(NamedTuple):
    """SLURM partition configuration options."""

    PartitionName: Callback = Callback()
    AllocNodes: Callback = partition_alloc_nodes
    AllowAccounts: Callback = partition_allow_accounts
    AllowGroups: Callback = partition_allow_groups
    AllowQos: Callback = partition_allow_qos
    Alternate: Callback = Callback()
    CpuBind: Callback = Callback()
    Default: Callback = Callback()
    DefaultTime: Callback = Callback()
    DefCpuPerGPU: Callback = Callback()
    DefMemPerCPU: Callback = Callback()
    DefMemPerGPU: Callback = Callback()
    DefMemPerNode: Callback = Callback()
    DenyAccounts: Callback = partition_deny_accounts
    DenyQos: Callback = partition_deny_qos
    DisableRootJobs: Callback = Callback()
    ExclusiveUser: Callback = Callback()
    GraceTime: Callback = Callback()
    Hidden: Callback = Callback()
    LLN: Callback = Callback()
    MaxCPUsPerNode: Callback = Callback()
    MaxCPUsPerSocket: Callback = Callback()
    MaxMemPerCPU: Callback = Callback()
    MaxMemPerNode: Callback = Callback()
    MaxNodes: Callback = Callback()
    MaxTime: Callback = Callback()
    MinNodes: Callback = Callback()
    Nodes: Callback = partition_nodes
    OverSubscribe: Callback = Callback()
    OverTimeLimit: Callback = Callback()
    PowerDownOnIdle: Callback = Callback()
    PreemptMode: Callback = Callback()
    PriorityJobFactor: Callback = Callback()
    PriorityTier: Callback = Callback()
    QOS: Callback = Callback()
    ReqResv: Callback = Callback()
    ResumeTimeout: Callback = Callback()
    RootOnly: Callback = Callback()
    SelectTypeParameters: Callback = Callback()
    State: Callback = Callback()
    SuspendTime: Callback = Callback()
    SuspendTimeout: Callback = Callback()
    TRESBillingWeights: Callback = partition_tres_billing_weights


SlurmConfOpts = _SlurmConfOpts()
NodeConfOpts = _NodeConfOpts()
DownNodeConfOpts = _DownNodeConfOpts()
FrontendNodeConfOpts = _FrontendNodeConfOpts()
NodeSetConfOpts = _NodeSetConfOpts()
PartitionConfOpts = _PartitionConfOpts()
