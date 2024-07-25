from model.infrastructure.gcp_infrastructure import GcpInfrastructure
from model.generator import Generator
import logging
import pandas as pd
import openpyxl

class MPAGenerator(Generator):
    """Generates a Excel file compatible with MPA"""

    def export(self, gcp_infrastructure: GcpInfrastructure):
        # Implement CSV export logic here
        logging.info("Exporting to Migration Portfolio Assessment (MPA)...")
        logging.info("Exporting to Migration Portfolio Assessment (MPA)...")
        workbook = openpyxl.Workbook()
        worksheet = workbook.active
        worksheet.title = "GCP VM Inventory"

        # Set column headers
        headers = [
            "Serverid",
            "isPhysical",
            "hypervisor",
            "HOSTNAME",
            "osName",
            "osVersion",
            "numCpus",
            "numCoresPerCpu",
            "numThreadsPerCore",
            "maxCpuUsagePctDec (%)",
            "avgCpuUsagePctDec (%)",
            "totalRAM (GB)",
            "maxRamUsagePctDec (%)",
            "avgRamUtlPctDec (%)",
            "Uptime",
            "Environment Type",
            "Storage-Total Disk Size (GB)",
            "Storage-Utilization %",
            "Storage-Max Read IOPS Size (KB)",
            "Storage-Max Write IOPS Size (KB)"
        ]
        worksheet.append(headers)



        # Iterate through GCP VM instances and populate data
        for instance  in gcp_infrastructure.vm_instances:
            # Filter for instances in RUNNING state
            if instance.status == 'RUNNING':
                
                # Compute metrics using pandas
                #pd.DataFrame(instance.cpu_data, columns=['timestamp', 'value'])
                cpu_df = instance.cpu_data_frame()
                memory_df = instance.memory_data_frame()

                # Calculate CPU stats
                max_cpu_usage = cpu_df['value'].max() * 100  # Convert to percentage
                avg_cpu_usage = cpu_df['value'].mean() * 100  # Convert to percentage

                # Calculate RAM stats
                max_ram_usage = memory_df['value'].max() / 1024 / 1024  # Convert to GB
                avg_ram_usage = memory_df['value'].mean() / 1024 / 1024  # Convert to GB

                row = [
                    instance.instance_name,  # Serverid
                    instance.is_virtual,  # isPhysical
                    "Google Compute Engine",  # hypervisor
                    instance.instance_name,  # HOSTNAME
                    instance.os,  # osName
                    None,  # osVersion (You'll need to extract this from thesse OS string)
                    instance.cpu_cores,  # numCpus
                    1,  # numCoresPerCpu (Assuming 1 core per CPU)
                    1,  # numThreadsPerCore (Assuming 1 thread per core)
                    max_cpu_usage,  # maxCpuUsagePctDec (%)
                    avg_cpu_usage,  # avgCpuUsagePctDec (%)
                    instance.ram_gb,  # totalRAM (GB)
                    max_ram_usage / (instance.ram_gb * 1024) ,  # maxRamUsagePctDec (%)
                    avg_ram_usage / (instance.ram_gb * 1024) ,  # avgRamUtlPctDec (%)
                    None,  # Uptime (You'll need to calculate this)
                    "Production",  # Environment Type (You might need to adjust this based on your environment)
                    sum([disk.disk_size_gb for disk in instance.disks]),  # Storage-Total Disk Size (GB)
                    instance.disk_utilization,  # Storage-Utilization %
                    instance.max_read_iops,  # Storage-Max Read IOPS Size (KB)
                    instance.max_write_iops,  # Storage-Max Write IOPS Size (KB)
                ]
                worksheet.append(row)

        # Save the Excel file
        workbook.save("gcp_vm_inventory_mpa.xlsx")