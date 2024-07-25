
import csv
from model.infrastructure.gcp_infrastructure import GcpInfrastructure
from model.generator import Generator
import logging

class CSVGenerator(Generator):
    """Generates a CSV file from the GCP infrastructure data."""

    def export(self, gcp_infrastructure: GcpInfrastructure):
        # Implement CSV export logic here
        logging.info("Exporting to CSV...")
        
        
    def export_to_csv(data):
        """
        Exports the collected VM instance data to a CSV file.

        Args:
            data (list): A list of dictionaries containing VM instance information.
        """
        with open('gcp_vm_instances.csv', 'w', newline='') as csvfile:
            fieldnames = ['project_id', 'instance_name', 'machine_type', 'zone', 'kind',  'cpu_cores','ram_gb', 'cpu_platform', 'status', 'os']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)