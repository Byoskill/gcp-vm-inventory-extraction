import csv
import argparse
import logging

from collector.gcp_compute_api import extract_model_from_gcp
from generators.factory import get_generator

# Set up logging
logging.basicConfig(filename='gcp_vm_extraction.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
# Add a stream handler to output to console as well
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logging.getLogger().addHandler(console_handler)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract VM instance data from GCP projects.')
    parser.add_argument('--organization_id', required=False, help='The ID of the organization.')
    parser.add_argument('--project_id', required=False, help='The ID of the project.')
    parser.add_argument('--regions', required=False, help='A comma-separated list of regions to filter zones by. By default, only the regions us-central1, us-east1, and us-west1 are used.', default="us-central1,us-east1,us-west1")
    parser.add_argument('--output_format', required=False, help='Output format for the discovery data (csv,json,yaml,me,mpa,ads,cloudoptimizer)', default="csv")
    args = parser.parse_args()

    regions = args.regions.split(',')
    gcp_infrastructure = extract_model_from_gcp(args.organization_id, args.project_id, regions)

    # Display some stats about the GCP infrastructure
    num_projects = len(set([vm.project_id for vm in gcp_infrastructure.vm_instances]))
    num_vms = len(gcp_infrastructure.vm_instances)
    largest_instance = max(gcp_infrastructure.vm_instances, key=lambda vm: vm.ram_gb)

    print(f"Organization present: {bool(args.organization_id)}")
    print(f"Number of projects: {num_projects}")
    print(f"Number of virtual machines: {num_vms}")
    print(f"Largest instance: {largest_instance.instance_name} ({largest_instance.ram_gb} GB RAM)")


    # Get the generator based on the output format
    generator = get_generator(args.output_format)

    

    # Export the data using the selected generator
    generator.export(gcp_infrastructure)