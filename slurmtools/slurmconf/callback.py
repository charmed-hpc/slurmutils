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

"""Callbacks for processing SLURM configuration data."""

from functools import singledispatch
from typing import Callable, NamedTuple, Optional


class Callback(NamedTuple):
    """Data struct for holding conf option parser and render methods."""

    parse: Optional[Callable] = None
    render: Optional[Callable] = None


# Common manipulators for SLURM configuration data.
def _from_slurm_dict(value):
    """Convert configuration value from a SLURM dict to Python dict.

    Args:
        value: SLURM configuration value to convert to Python dict.
    """
    result = {}
    for val in value.split(","):
        if "=" in val:
            sub_opt, sub_val = val.split("=", 1)
            result.update({sub_opt: sub_val})
        else:
            result.update({val: True})

    return result


@singledispatch
def _to_slurm_dict(value):
    """Convert configuration value to SLURM dict.

    Notes:
        Value my either be a Python dict or already in SLURM format,
        so a dispatch is used to handle both cases.
    """
    raise TypeError(f"Expected str or dict, not {type(value)}")


@singledispatch
def _to_slurm_comma_sep(value):
    """Convert configuration value to SLURM comma-separated list.

    Notes:
        Value my either be a Python list or already in SLURM format,
        so a dispatch is used to handle both cases.
    """
    raise TypeError(f"Expected str or list, not {type(value)}")


@singledispatch
def _to_slurm_colon_sep(value):
    """Convert configuration value to SLURM colon-separated list.

    Notes:
        Value my either be a Python list or already in SLURM format,
        so a dispatch is used to handle both cases.
    """
    raise TypeError(f"Expected str or list, not {type(value)}")


@_to_slurm_comma_sep.register
@_to_slurm_colon_sep.register
@_to_slurm_dict.register
def _(value: str):
    return value


@_to_slurm_comma_sep.register
def _(value: list):
    return ",".join(value)


@_to_slurm_colon_sep.register
def _(value: list):
    return ":".join(value)


@_to_slurm_dict.register
def _(value: dict):
    result = []
    for sub_opt, sub_val in value.items():
        if type(sub_val) != bool:
            result.append(f"{sub_opt}={sub_val}")
        elif sub_val:
            result.append(sub_opt)

    return ",".join(result)


# Handler macros.
# SLURM configuration values.
acct_storage_external_host = Callback(lambda val: val.split(","), _to_slurm_comma_sep)
acct_storage_param = Callback(_from_slurm_dict, _to_slurm_dict)
acct_storage_tres = Callback(lambda val: val.split(","), _to_slurm_comma_sep)
acct_store_flags = Callback(lambda val: val.split(","), _to_slurm_comma_sep)
auth_alt_types = Callback(lambda val: val.split(","), _to_slurm_comma_sep)
auth_alt_param = Callback(_from_slurm_dict, _to_slurm_dict)
auth_info = Callback(_from_slurm_dict, _to_slurm_dict)
bcast_exclude = Callback(lambda val: val.split(","), _to_slurm_comma_sep)
bcast_param = Callback(_from_slurm_dict, _to_slurm_dict)
cli_filter_plugins = Callback(lambda val: val.split(","), _to_slurm_comma_sep)
communication_params = Callback(_from_slurm_dict, _to_slurm_dict)
cpu_freq_def = Callback(lambda val: val.split(","), _to_slurm_comma_sep)
cpu_freq_governors = Callback(lambda val: val.split(","), _to_slurm_comma_sep)
debug_flags = Callback(lambda val: val.split(","), _to_slurm_comma_sep)
dependency_param = Callback(_from_slurm_dict, _to_slurm_dict)
federation_param = Callback(lambda val: val.split(","), _to_slurm_comma_sep)
health_check_node_state = Callback(lambda val: val.split(","), _to_slurm_comma_sep)
job_acct_gather_frequency = Callback(_from_slurm_dict, _to_slurm_dict)
job_comp_params = Callback(_from_slurm_dict, _to_slurm_dict)
job_submit_plugins = Callback(lambda val: val.split(","), _to_slurm_comma_sep)
launch_parameters = Callback(_from_slurm_dict, _to_slurm_dict)
licenses = Callback(lambda val: val.split(","), _to_slurm_comma_sep)
plugin_dir = Callback(lambda val: val.split(":"), _to_slurm_colon_sep)
power_parameters = Callback(_from_slurm_dict, _to_slurm_dict)
preempt_mode = Callback(lambda val: val.split(","), _to_slurm_comma_sep)
preempt_param = Callback(_from_slurm_dict, _to_slurm_dict)
prep_plugins = Callback(lambda val: val.split(","), _to_slurm_comma_sep)
priority_weight_tres = Callback(_from_slurm_dict, _to_slurm_dict)
private_data = Callback(lambda val: val.split(","), _to_slurm_comma_sep)
prolog_flags = Callback(lambda val: val.split(","), _to_slurm_comma_sep)
propagate_resource_limits = Callback(lambda val: val.split(","), _to_slurm_comma_sep)
propagate_resource_limits_except = Callback(lambda val: val.split(","), _to_slurm_comma_sep)
scheduler_param = Callback(_from_slurm_dict, _to_slurm_dict)
scron_param = Callback(lambda val: val.split(","), _to_slurm_comma_sep)
slurmctld_param = Callback(_from_slurm_dict, _to_slurm_dict)
slurmd_param = Callback(lambda val: val.split(","), _to_slurm_comma_sep)
switch_param = Callback(_from_slurm_dict, _to_slurm_dict)
task_plugin = Callback(lambda val: val.split(","), _to_slurm_comma_sep)
task_plugin_param = Callback(_from_slurm_dict, _to_slurm_dict)
topology_param = Callback(lambda val: val.split(","), _to_slurm_comma_sep)

# Node configuration values.
node_cpu_spec_list = Callback(lambda val: val.split(","), _to_slurm_comma_sep)
node_features = Callback(lambda val: val.split(","), _to_slurm_comma_sep)
node_gres = Callback(lambda val: val.split(","), _to_slurm_comma_sep)
node_reason = Callback(None, lambda val: f'"{val}"')

# DownNode configuration values.
down_name = Callback(lambda val: val.split(","), _to_slurm_comma_sep)
down_reason = Callback(None, lambda val: f'"{val}"')

# FrontendNode configuration values.
frontend_allow_groups = Callback(lambda val: val.split(","), _to_slurm_comma_sep)
frontend_allow_users = Callback(lambda val: val.split(","), _to_slurm_comma_sep)
frontend_deny_groups = Callback(lambda val: val.split(","), _to_slurm_comma_sep)
frontend_deny_users = Callback(lambda val: val.split(","), _to_slurm_comma_sep)
frontend_reason = Callback(None, lambda val: f'"{val}"')

# Partition configuration values.
partition_alloc_nodes = Callback(lambda val: val.split(","), _to_slurm_comma_sep)
partition_allow_accounts = Callback(lambda val: val.split(","), _to_slurm_comma_sep)
partition_allow_groups = Callback(lambda val: val.split(","), _to_slurm_comma_sep)
partition_allow_qos = Callback(lambda val: val.split(","), _to_slurm_comma_sep)
partition_deny_accounts = Callback(lambda val: val.split(","), _to_slurm_comma_sep)
partition_deny_qos = Callback(lambda val: val.split(","), _to_slurm_comma_sep)
partition_nodes = Callback(lambda val: val.split(","), _to_slurm_comma_sep)
partition_tres_billing_weights = Callback(_from_slurm_dict, _to_slurm_dict)
