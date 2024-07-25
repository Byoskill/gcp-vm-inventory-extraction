#################################################

from datetime import datetime
from google.cloud import compute_v1
from google.cloud import monitoring_v3
from datetime import datetime, timedelta
from google.cloud import resourcemanager_v3
import logging
from collector.perf_metrics import get_vm_metrics, obtain_performance_metrics
from model.infrastructure.disk import Disk
from model.infrastructure.label import Label
from model.infrastructure.timeserie import Timeserie
from model.infrastructure.virtual_machine import VirtualMachine
from model.infrastructure.gcp_infrastructure import GcpInfrastructure


def get_folders(
    parent_id = "organizations/ORGANIZATION_ID",
    folders = None):

    # This function will return a list of folder_id for all the folders and 
    # subfolders respectively

    if folders is None:
        folders = []

    # Creating folder client 
    client = resourcemanager_v3.FoldersClient()
    request = resourcemanager_v3.ListFoldersRequest(
        parent=parent_id,
    )

    page_result = client.list_folders(request=request)
    for pages in page_result:
        folders.append(pages.name)
        get_folders(parent_id=pages.name, folders=folders)
    return folders


def search_projects(folder_id):
    # This function will take folder_id input and returns
    # the list of project_id under a given folder_id

    client = resourcemanager_v3.ProjectsClient()

    query = f"parent:{folder_id}"
    request = resourcemanager_v3.SearchProjectsRequest(query=query)
    page_result = client.search_projects(request=request)
    search_result = []
    for pages in page_result:
        search_result.append(pages)
    return search_result


def list_projects(organization_id= None, project_id=None):
    """
    Retrieves a list of GCP projects the user has access to.

    Returns:
        list: A list of GCP project IDs.
    """
    # will returns the list of all active projects(project_id)

    active_project = []
    if organization_id != None:
        for folders in get_folders(parent_id=organization_id, folders=None):
            for projects in search_projects(folders):
                if str(projects.state) == "State.ACTIVE":
                    active_project.append(projects.project_id)
    elif project_id != None:
        active_project.append(project_id)
    else:
        logging.error("No organization_id or project_id provided")
    return active_project


def get_zones(project_id, regions):
    """
    Retrieves a list of zones in a given GCP project, filtering by regions.

    Args:
        project_id (str): The ID of the GCP project.
        regions (list): A list of region names to filter zones by.

    Returns:
        list: A list of zone names within the specified regions.
    """
    logging.info("Get list of zones")
    client = compute_v1.ZonesClient()
    zones = client.list(project=project_id)
    filtered_zones = []
    for zone in zones:
        if zone.region.split('/')[-1] in regions:
            filtered_zones.append(zone.name)
    return filtered_zones

def get_vm_instances(project_id, regions) -> list[VirtualMachine]:
    """
    Retrieves a list of virtual machine instances in a given GCP project, filtering by regions.

    Args:
        project_id (str): The ID of the GCP project.
        regions (list): A list of region names to filter zones by.

    Returns:
        list: A list of dictionaries containing VM instance information.
    """
    client = compute_v1.InstancesClient()
    
    all_vm_data = []

    # Iterate through zones
    for zone in get_zones(project_id, regions):
        logging.info(f"Processing zone: {zone} in project: {project_id}")  # Log zone and project
        instances = client.list(project=project_id, zone=zone)
        for instance in instances:
            # Extract instance type from machine_type
            instance_type = instance.machine_type.split('/')[-1]  # Split by '/' and take the last part

            # Get machine type details
            machine_type_client = compute_v1.MachineTypesClient()
            machine_type_details = machine_type_client.get(project=project_id, zone=zone, machine_type=instance_type)

            logging.debug(instance)
            logging.debug("-----------------------------------------")
            logging.debug(machine_type_details)

            # Extract RAM and CPU
            ram_gb = machine_type_details.memory_mb / 1024  # Convert MB to GB
            cpu_cores = machine_type_details.guest_cpus
                     
            vm = VirtualMachine(
                project_id=project_id,
                kind=instance.kind,
                instance_name=instance.name,
                machine_type=instance.machine_type,
                cpu_platform=instance.cpu_platform,
                status=instance.status,
                zone=zone,  # Add zone information
                os=instance.disks[0].architecture,  # Assuming the first disk is the OS disk
                ram_gb=ram_gb,  # Add RAM in GB
                cpu_cores=cpu_cores,  # Add CPU cores
                is_virtual=True,
                is_shared_cpu=machine_type_details.is_shared_cpu,                          
            )

            # Initialize variables for monitoring and logging
            monitoring_enabled = False
            logging_enabled = False

            # Iterate through metadata items
            for item in instance.metadata.items:
                if item.key == "google-monitoring-enable":
                    monitoring_enabled = item.value == "1"  # True if value is "1"
                elif item.key == "google-logging-enable":
                    logging_enabled = item.value == "1"  # True if value is "1"

            # Now you have the variables set:
            vm.monitoring_enabled = monitoring_enabled
            vm.logging_enabled = logging_enabled

            
            # Add labels
            for key in instance.labels.keys():
                lbl = Label(key, str(instance.labels.get(key) or ""))
                vm.labels.append(lbl) 
            
            # Add Disks
            scan_disks(instance, vm)
            disk_utilization = disk_utilization(project_id, vm)
            print("Disk utililzation", disk_utilization)
            vm.disk_utilization = disk_utilization
            ## Check for monitoring metrics
            obtain_performance_metrics(project_id, vm)
            
            all_vm_data.append(vm)
            
        logging.info(f"Processing zone: {zone} in project: {project_id}, now {len(all_vm_data)} instances")  # Log zone and project
    return all_vm_data

def scan_disks(instance, vm):
    for diskinfo in instance.disks:
        print("Disk", diskinfo)
        disk = Disk( diskinfo.device_name, diskinfo.mode, diskinfo.type, diskinfo.disk_size_gb, [] )
        for license in diskinfo.licenses:             
            #print(  "License ", license, project_id)
            license_name = license.split('/')[-1]
            disk.add_license(license_name)                    
        vm.disks.append(disk)
        
        #print(disk)

def extract_model_from_gcp(organization_id= None, project_id=None, regions:list[str] = ["us-central1", "us-east1", "us-west1"]) -> GcpInfrastructure:
    projects = list_projects(organization_id, project_id)
    
    all_vm_data = GcpInfrastructure()
    for project in projects:
        vm_data = get_vm_instances(project, regions)
        all_vm_data.add_new_virtual_machines(vm_data)
    return all_vm_data
