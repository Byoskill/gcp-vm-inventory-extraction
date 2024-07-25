#################################################

from datetime import datetime
from google.cloud import compute_v1
from google.cloud import monitoring_v3
from datetime import datetime, timedelta
from google.cloud import resourcemanager_v3
import logging
from model.infrastructure.disk import Disk
from model.infrastructure.label import Label
from model.infrastructure.timeserie import Timeserie
from model.infrastructure.virtual_machine import VirtualMachine
from model.infrastructure.gcp_infrastructure import GcpInfrastructure


def obtain_performance_metrics(project_id: str, vm: VirtualMachine):
  
    # Get CPU usage metrics
    cpu_data = get_vm_metrics(project_id, vm, 'cpu')

    # Get memory usage metrics
    memory_data = get_vm_metrics(project_id, vm, 'memory')

    vm.memory_data = memory_data
    vm.cpu_data = cpu_data
    
    # Print the results
    logging.debug("CPU Usage:")
    for data_point in cpu_data:
        logging.debug(f"Timestamp: {data_point.timestamp}, Value: {data_point.value}")

    logging.debug("\nMemory Usage:")
    for data_point in memory_data:
        logging.debug(f"Timestamp: {data_point.timestamp}, Value: {data_point.value_in_gb()}")


def get_vm_metrics(project_id, instance, metric_type) -> list[Timeserie]:    
    """
    Retrieves memory or CPU usage metrics for a VM instance over a specified time period.

    Args:
        project_id (str): The ID of the GCP project.
        instance_name (str): The name of the VM instance.
        zone (str): The zone where the VM instance is located.
        metric_type (str): The type of metric to retrieve ('memory' or 'cpu').
        start_time (datetime): The start time of the time period.
        end_time (datetime): The end time of the time period.

    Returns:
        list: A list of metric data points, or an empty list if no data is found.
    """
    instance_name = instance.instance_name
    client = monitoring_v3.QueryServiceClient()
    
    metric_data : list[Timeserie] = []

    # Loop through the last 30 days
    #for i in range(1,2):
    end_time = datetime.now()
    start_time = end_time - timedelta(days=(30))

    query = ""
    if metric_type == 'memory':
        query= f"""
        fetch gce_instance
        | metric 'compute.googleapis.com/instance/memory/balloon/ram_used'
        | filter (metric.instance_name == '{instance_name}')
        | group_by 1d, [value_ram_used_mean: mean(value.ram_used)]
        | every 1d
        | within   d'{start_time.strftime("%Y/%m/%d-%H:%M:%S")}', d'{end_time.strftime("%Y/%m/%d-%H:%M:%S")}'
        """
    else: 
        query = f"""
        fetch gce_instance
        | metric 'compute.googleapis.com/instance/cpu/utilization'
        | filter (metric.instance_name == '{instance_name}')
        | group_by 1d, [value_utilization_mean: mean(value.utilization)]
        | every 1d
        | within   d'{start_time.strftime("%Y/%m/%d-%H:%M:%S")}', d'{end_time.strftime("%Y/%m/%d-%H:%M:%S")}'
        """
    logging.info(query)

    # Execute the query
    response = client.query_time_series(
        monitoring_v3.QueryTimeSeriesRequest(
            name=f"projects/{project_id}",
            query=query,
        )
    )    

    # Extract metric data points
    for time_series in response.time_series_data:
        i = 1
        for point in time_series.point_data:
            timestamp = end_time - timedelta(days=(i))
            value = point.values[0].double_value
            metric_data.append(Timeserie(
                timestamp,
                value
            ))
            i = i + 1
    
    return metric_data


def fetch_disk_utilization(project_id: str, instance_id: str):
    query= f"""
fetch gce_instance
| metric 'agent.googleapis.com/disk/percent_used'
| filter (resource.project_id == '{project_id}')
| filter (resource.instance_id == '{instance_id}')
| filter (metric.device !~ '/dev/loop.*' && metric.state == 'used')
| group_by 2m, [value_percent_used_mean: mean(value.percent_used)]
| every 2m
    """ 
    logging.info(query)
    
    client = monitoring_v3.QueryServiceClient()

    # Execute the query
    response = client.query_time_series(
        monitoring_v3.QueryTimeSeriesRequest(
            name=f"projects/{project_id}",
            query=query,
        )
    )  
    # Extract metric data points
    for time_series in response.time_series_data:
        for point in time_series.point_data:
            value = point.values[0].double_value
            return value

    return 0