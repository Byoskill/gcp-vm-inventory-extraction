from typing import Dict

from model.infrastructure.disk import Disk
from model.infrastructure.label import Label


class VirtualMachine:
    labels : list[Label] = []
    disks: list[Disk] = []
    
    def __init__(self, 
                 project_id, 
                 kind, 
                 instance_name, 
                 machine_type, 
                 cpu_platform, 
                 status, 
                 zone, 
                 os, 
                 ram_gb, 
                 cpu_cores, 
                 is_virtual=True, 
                 is_shared_cpu=False):
        self.project_id = project_id
        self.kind = kind
        self.instance_name = instance_name
        self.machine_type = machine_type
        self.cpu_platform = cpu_platform
        self.status = status
        self.zone = zone
        self.os = os
        self.ram_gb = ram_gb
        self.cpu_cores = cpu_cores
        self.is_virtual = is_virtual
        self.is_shared_cpu = is_shared_cpu
        self.monitoring_enabled = False
        self.logging_enabled = False

