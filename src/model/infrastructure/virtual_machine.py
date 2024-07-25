from typing import Dict
import pandas as pd

from model.infrastructure.disk import Disk
from model.infrastructure.label import Label
from model.infrastructure.timeserie import Timeserie


class VirtualMachine:
    labels : list[Label] = []
    disks: list[Disk] = []
    memory_data : list[Timeserie] = []
    cpu_data : list[Timeserie] = []
    disk_utilization = 0.75
    max_read_iops = 0
    max_write_iops = 0
    
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

    def cpu_data_frame(self):
        liste = []
        for instance in self.cpu_data:
            liste.append([instance.timestamp, instance.value])        
        return pd.DataFrame(liste, columns=['timestamp', 'value'])
    
    def memory_data_frame(self):
        liste = []
        for instance in self.memory_data:
            liste.append([instance.timestamp, instance.value])        
        return pd.DataFrame(liste, columns=['timestamp', 'value'])

