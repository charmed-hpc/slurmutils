# Copyright 2024-2025 Canonical Ltd.
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

EXAMPLE_GRES_CONFIG = """#
# `gres.conf` file generated at 2024-12-10 14:17:35.161642 by slurmutils.
#
AutoDetect=nvml
Name=gpu Type=gp100  File=/dev/nvidia0 Cores=0,1
Name=gpu Type=gp100  File=/dev/nvidia1 Cores=0,1
Name=gpu Type=p6000  File=/dev/nvidia2 Cores=2,3
Name=gpu Type=p6000  File=/dev/nvidia3 Cores=2,3
Name=mps Count=200  File=/dev/nvidia0
Name=mps Count=200  File=/dev/nvidia1
Name=mps Count=100  File=/dev/nvidia2
Name=mps Count=100  File=/dev/nvidia3
Name=bandwidth Type=lustre Count=4G Flags=countonly
Name=gpu NodeName=juju-abc654-1 Type=tesla_t4 File=/dev/nvidia[0-1] Count=8G
Name=gpu NodeName=juju-abc654-1 Type=l40s File=/dev/nvidia[2-3] Count=12G
"""

EXAMPLE_OCI_CONFIG = """#
# `oci.conf` file generated at 2024-09-18 19:05:45.723019 by slurmutils.
#
IgnoreFileConfigJson=true
EnvExclude="^(SLURM_CONF|SLURM_CONF_SERVER)="
RunTimeEnvExclude="^(SLURM_CONF|SLURM_CONF_SERVER)="
RunTimeRun="singularity exec --userns %r %@"
RunTimeKill="kill -s SIGTERM %p"
RunTimeDelete="kill -s SIGKILL %p"
"""

EXAMPLE_SLURM_CONFIG = """#
# `slurm.conf` file generated at 2024-01-30 17:18:36.171652 by slurmutils.
#
SlurmctldHost=juju-c9fc6f-0(10.152.28.20)
SlurmctldHost=juju-c9fc6f-1(10.152.28.100)

ClusterName=charmed-hpc
AuthType=auth/munge
Epilog=/usr/local/slurm/epilog
Prolog=/usr/local/slurm/prolog
FirstJobId=65536
InactiveLimit=120
JobCompType=jobcomp/filetxt
JobCompLoc=/var/log/slurm/jobcomp
KillWait=30
MaxJobCount=10000
MinJobAge=3600
PluginDir=/usr/local/lib:/usr/local/slurm/lib
ReturnToService=0
SchedulerType=sched/backfill
SlurmctldLogFile=/var/log/slurm/slurmctld.log
SlurmdLogFile=/var/log/slurm/slurmd.log
SlurmctldPort=7002
SlurmdPort=7003
SlurmdSpoolDir=/var/spool/slurmd.spool
StateSaveLocation=/var/spool/slurm.state
TmpFS=/tmp
WaitTime=30

#
# Node configurations
#
NodeName=juju-c9fc6f-2 NodeAddr=10.152.28.48 CPUs=1 RealMemory=1000 TmpDisk=10000
NodeName=juju-c9fc6f-3 NodeAddr=10.152.28.49 CPUs=1 RealMemory=1000 TmpDisk=10000
NodeName=juju-c9fc6f-4 NodeAddr=10.152.28.50 CPUs=1 RealMemory=1000 TmpDisk=10000
NodeName=juju-c9fc6f-5 NodeAddr=10.152.28.51 CPUs=1 RealMemory=1000 TmpDisk=10000

#
# Down node configurations
#
DownNodes=juju-c9fc6f-5 State=down Reason="Maintenance Mode"

#
# Partition configurations
#
PartitionName=DEFAULT MaxTime=30 MaxNodes=10 State=up
PartitionName=batch Nodes=juju-c9fc6f-2,juju-c9fc6f-3,juju-c9fc6f-4,juju-c9fc6f-5 MinNodes=4 MaxTime=120 AllowGroups=admin
"""

EXAMPLE_SLURMDBD_CONFIG = """#
# `slurmdbd.conf` file generated at 2024-01-30 17:18:36.171652 by slurmutils.
#
ArchiveEvents=yes
ArchiveJobs=yes
ArchiveResvs=yes
ArchiveSteps=no
ArchiveTXN=no
ArchiveUsage=no
ArchiveScript=/usr/sbin/slurm.dbd.archive
AuthInfo=socket=/var/run/munge/munge.socket.2
AuthType=auth/munge
AuthAltTypes=auth/jwt
AuthAltParameters=jwt_key=16549684561684@
DbdHost=slurmdbd-0
DbdBackupHost=slurmdbd-1
DebugLevel=info
PluginDir=/all/these/cool/plugins
PurgeEventAfter=1month
PurgeJobAfter=12month
PurgeResvAfter=1month
PurgeStepAfter=1month
PurgeSuspendAfter=1month
PurgeTXNAfter=12month
PurgeUsageAfter=24month
LogFile=/var/log/slurmdbd.log
PidFile=/var/run/slurmdbd.pid
SlurmUser=slurm
StoragePass=supersecretpasswd
StorageType=accounting_storage/mysql
StorageUser=slurm
StorageHost=127.0.0.1
StoragePort=3306
StorageLoc=slurm_acct_db
"""

EXAMPLE_CGROUP_CONFIG = """#
# `cgroup.conf` file generated at 2024-09-18 15:10:44.652017 by slurmutils.
#
ConstrainCores=yes
ConstrainDevices=yes
ConstrainRAMSpace=yes
ConstrainSwapSpace=yes
"""

EXAMPLE_ACCT_GATHER_CONFIG = """#
# `acct_gather.conf` file generated at 2024-09-18 15:10:44.652017 by slurmutils.
#
EnergyIPMIFrequency=1
EnergyIPMICalcAdjustment=yes
EnergyIPMIPowerSensors=node=16,19;socket1=19,26;knc=16,19
EnergyIPMIUsername=testipmiusername
EnergyIPMIPassword=testipmipassword
EnergyIPMITimeout=10
ProfileHDF5Dir=/mydir
ProfileHDF5Default=all
ProfileInfluxDBDatabase=acct_gather_db
ProfileInfluxDBDefault=all
ProfileInfluxDBHost=testhostname
ProfileInfluxDBPass=testpassword
ProfileInfluxDBRTPolicy=testpolicy
ProfileInfluxDBUser=testuser
ProfileInfluxDBTimeout=10
InfinibandOFEDPort=0
SysfsInterfaces=enp0s1
"""
