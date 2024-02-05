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

"""Data models for the slurmdbd daemon."""

from types import MappingProxyType

from ._model import (
    BaseModel,
    ColonSeparatorCallback,
    CommaSeparatorCallback,
    SlurmDictCallback,
    base_descriptors,
)


class SlurmdbdConfig(BaseModel):
    """Object representing the slurmdbd.conf configuration file.

    Top-level configuration definition and data validators sourced from
    the slurmdbd.conf manpage. `man slurmdbd.conf.5`
    """

    primary_key = None
    callbacks = MappingProxyType(
        {
            "auth_alt_types": CommaSeparatorCallback,
            "auth_alt_parameters": SlurmDictCallback,
            "communication_parameters": SlurmDictCallback,
            "debug_flags": CommaSeparatorCallback,
            "parameters": CommaSeparatorCallback,
            "plugin_dir": ColonSeparatorCallback,
            "private_data": CommaSeparatorCallback,
            "storage_parameters": SlurmDictCallback,
        }
    )

    archive_dir = property(*base_descriptors("ArchiveDir"))
    archive_events = property(*base_descriptors("ArchiveEvents"))
    archive_jobs = property(*base_descriptors("ArchiveJobs"))
    archive_resvs = property(*base_descriptors("ArchiveResvs"))
    archive_script = property(*base_descriptors("ArchiveScript"))
    archive_steps = property(*base_descriptors("ArchiveSteps"))
    archive_suspend = property(*base_descriptors("ArchiveSuspend"))
    archive_txn = property(*base_descriptors("ArchiveTXN"))
    archive_usage = property(*base_descriptors("ArchiveUsage"))
    auth_info = property(*base_descriptors("AuthInfo"))
    auth_alt_types = property(*base_descriptors("AuthAltTypes"))
    auth_alt_parameters = property(*base_descriptors("AuthAltParameters"))
    auth_type = property(*base_descriptors("AuthType"))
    commit_delay = property(*base_descriptors("CommitDelay"))
    communication_parameters = property(*base_descriptors("CommunicationParameters"))
    dbd_backup_host = property(*base_descriptors("DbdBackupHost"))
    dbd_addr = property(*base_descriptors("DbdAddr"))
    dbd_host = property(*base_descriptors("DbdHost"))
    dbd_port = property(*base_descriptors("DbdPort"))
    debug_flags = property(*base_descriptors("DebugFlags"))
    debug_level = property(*base_descriptors("DebugLevel"))
    debug_level_syslog = property(*base_descriptors("DebugLevelSyslog"))
    default_qos = property(*base_descriptors("DefaultQOS"))
    log_file = property(*base_descriptors("LogFile"))
    log_time_format = property(*base_descriptors("LogTimeFormat"))
    max_query_time_range = property(*base_descriptors("MaxQueryTimeRange"))
    message_timeout = property(*base_descriptors("MessageTimeout"))
    parameters = property(*base_descriptors("Parameters"))
    pid_file = property(*base_descriptors("PidFile"))
    plugin_dir = property(*base_descriptors("PluginDir"))
    private_data = property(*base_descriptors("PrivateData"))
    purge_event_after = property(*base_descriptors("PurgeEventAfter"))
    purge_job_after = property(*base_descriptors("PurgeJobAfter"))
    purge_resv_after = property(*base_descriptors("PurgeResvAfter"))
    purge_step_after = property(*base_descriptors("PurgeStepAfter"))
    purge_suspend_after = property(*base_descriptors("PurgeSuspendAfter"))
    purge_txn_after = property(*base_descriptors("PurgeTXNAfter"))
    purge_usage_after = property(*base_descriptors("PurgeUsageAfter"))
    slurm_user = property(*base_descriptors("SlurmUser"))
    storage_host = property(*base_descriptors("StorageHost"))
    storage_backup_host = property(*base_descriptors("StorageBackupHost"))
    storage_loc = property(*base_descriptors("StorageLoc"))
    storage_parameters = property(*base_descriptors("StorageParameters"))
    storage_pass = property(*base_descriptors("StoragePass"))
    storage_port = property(*base_descriptors("StoragePort"))
    storage_type = property(*base_descriptors("StorageType"))
    storage_user = property(*base_descriptors("StorageUser"))
    tcp_timeout = property(*base_descriptors("TCPTimeout"))
    track_slurmctld_down = property(*base_descriptors("TrackSlurmctldDown"))
    track_wc_key = property(*base_descriptors("TrackWCKey"))
