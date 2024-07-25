from model.infrastructure.gcp_infrastructure import GcpInfrastructure
from model.generator import Generator


class YAMLGenerator(Generator):
    """Generates a YAML file from the GCP infrastructure data."""

    def export(self, gcp_infrastructure: GcpInfrastructure):
        # Implement YAML export logic here
        print("Exporting to YAML...")
